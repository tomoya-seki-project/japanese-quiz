# Quiz AJAX Error Handling Report

## 目的

今次改動係補完整 Quiz play page 嘅 AJAX form validation flow，避免正常嘅 form validation failure 跌入 Django `FormView` 預設 HTML rendering flow，最後錯誤地變成 HTTP 500。

同時建立一個清楚嘅前後端 response contract：

```text
成功
→ JSON：success=true
→ 前端更新 Quiz partial HTML

Form validation失敗
→ HTTP 400 JSON：success=false + errors
→ 前端顯示全部 field errors
```

目前已完成 JSON success／validation flow，以及非JSON HTML response、network failure同JSON parsing failure嘅通用 fallback。

## 目錄

- [目的](#目的)
- [問題背景](#問題背景)
- [涉及檔案](#涉及檔案)
- [Backend設計](#backend設計)
- [Frontend設計](#frontend設計)
- [今次驗證結果](#今次驗證結果)
- [常見錯誤與今次修正](#常見錯誤與今次修正)
- [非JSON response與network failure處理](#非json-response與network-failure處理)
- [建議補測試](#建議補測試)
- [重點心智模型](#重點心智模型)

## 問題背景

Quiz play page唔會喺每次 Submit、Next、Skip或Summary時重新載入完整頁面。JavaScript會攔截 `.quiz-ajax-form` submission，再用 `fetch()`向對應 endpoint送出 POST：

```javascript
fetch(form.action, {
    method: form.method,
    body: new FormData(form),
    headers: {
        "X-Requested-With": "XMLHttpRequest"
    }
})
```

成功時，後端回傳兩段 partial HTML：

```json
{
  "main_html": "...",
  "input_panel_html": "..."
}
```

前端再更新：

```javascript
quizAreaContainer.innerHTML = data.main_html;
quizInputPanelContainer.innerHTML = data.input_panel_html;
```

問題出現喺 form validation失敗時。`FormView`概念流程係：

```text
收到 POST
  ↓
建立並驗證 form
  ├── valid   → form_valid(form)
  └── invalid → form_invalid(form)
```

Quiz AJAX views原本只實作 `form_valid()`。Django預設 `form_invalid()`係為普通完整HTML頁面而設，會嘗試重新render view template；但 AJAX action views冇 `template_name`，所以普通輸入錯誤可能變成template-related exception及500。

例如：

```python
answer = forms.CharField(required=True)
```

User未輸入答案就提交時，本來只應該係「答案必填」validation error，唔應該成為「伺服器內部錯誤」。

## 涉及檔案

- `quiz/views.py`
  - 新增共用 `QuizAjaxFormMixin`。
  - 四個 AJAX `FormView`使用相同 invalid-form JSON contract。
  - 成功 response加入 `success=True`。
- `quiz/helper.py`
  - Next／Skip共用 payload加入 `success=True`。
- `quiz/templates/quiz/quiz_play.html`
  - 新增 `#quiz-error-message`容器。
- `static/js/quiz/quiz_play.js`
  - 按 `data.success`分流成功與validation failure。
  - 遍歷並安全顯示全部 form errors。
  - 解析前檢查 response `Content-Type`，避免將HTML error page當JSON。
  - 用 `.catch()`處理非JSON、network同JSON parsing failure，並顯示通用恢復提示。

## Backend設計

### 共用 `QuizAjaxFormMixin`

四個 AJAX action views共用同一個 `form_invalid()`：

```python
class QuizAjaxFormMixin:
    def form_invalid(self, form):
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )
```

作用：

- 阻止 invalid AJAX form跌入預設HTML `form_invalid()`。
- 明確回傳 HTTP 400。
- 使用 `form.errors.get_json_data()`保留 field name、message同error code。
- 令所有 Quiz AJAX forms使用一致response格式。

### Mixin inheritance次序

Mixin必須放喺 `FormView`之前：

```python
class QuizSubmitAnswerView(
    LoginRequiredMixin,
    QuizSettingRequiredMixin,
    QuizSessionRequiredMixin,
    QuizAjaxFormMixin,
    FormView,
):
    ...
```

原因係 Python會按照method resolution order（MRO）尋找 `form_invalid()`。`QuizAjaxFormMixin`放喺 `FormView`之前，先會優先使用自訂JSON版本。

目前以下 views已接入：

- `QuizSubmitAnswerView`
- `QuizNextView`
- `QuizSkipView`
- `QuizSummaryView`

Next、Skip同Summary forms目前冇fields，正常情況下幾乎一定valid；仍然接入mixin可以保持contract一致，並避免將來新增欄位後重新出現同一問題。

### 成功response contract

成功response統一加入：

```python
"success": True
```

完整例子：

```python
return JsonResponse({
    "success": True,
    "main_html": main_html,
    "input_panel_html": input_panel_html,
})
```

Next／Skip透過 `build_next_question_payload()`共用：

```python
return {
    "success": True,
    "main_html": main_html,
    "input_panel_html": input_panel_html,
}
```

### Invalid response contract

例如空答案會回傳：

```json
{
  "success": false,
  "errors": {
    "answer": [
      {
        "message": "This field is required.",
        "code": "required"
      }
    ]
  }
}
```

資料來源：

```text
Form field validation rules
  ↓
form.is_valid() == False
  ↓
form.errors
  ↓
form.errors.get_json_data()
  ↓
JsonResponse
```

呢個HTTP 400係 view主動回傳嘅JSON，唔會經過全域 `handler400`。全域handler負責完整HTML error page；AJAX action endpoint要維持JSON contract。

## Frontend設計

### Error message container

Quiz完整頁面加入：

```html
<div id="quiz-error-message"></div>
```

佢放喺會被partial replacement更新嘅containers之外，因此更新 `quiz-area-container`時唔會一併刪除error容器。

### 成功與validation failure分流

前端收到JSON後先檢查：

```javascript
if (data.success === false) {
    renderFormErrorMessages(data.errors, errorContainer);
    return;
}
```

`return`會停止今次callback，避免invalid response冇 `main_html`時仍然執行：

```javascript
quizAreaContainer.innerHTML = data.main_html;
quizInputPanelContainer.innerHTML = data.input_panel_html;
```

成功時會先清除舊錯誤：

```javascript
errorContainer.replaceChildren();
```

再更新兩個partial containers。

使用嚴格判斷：

```javascript
data.success === false
```

比以下寫法清楚：

```javascript
!data.success
```

因為 `!undefined`亦係 `true`，可能將缺少 `success` key嘅舊成功payload錯誤分類成失敗。

### 遍歷全部 form errors

`errors`係一個以field name做key、error array做value嘅object：

```json
{
  "answer": [
    {"message": "This field is required.", "code": "required"}
  ],
  "tips_count": [
    {"message": "Ensure this value is less than or equal to 50.", "code": "max_value"}
  ]
}
```

唔可以只寫死：

```javascript
data.errors.answer[0].message
```

否則會漏咗其他fields同同一field嘅其他messages。

目前使用雙層iteration：

```javascript
function renderFormErrorMessages(errors, container) {
    container.replaceChildren();

    Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
        fieldErrors.forEach(error => {
            const errorMsg = document.createElement("p");

            if (fieldName === "__all__") {
                errorMsg.textContent = error.message;
            } else {
                const label = getErrorLabel(fieldName);
                errorMsg.textContent = `${label}: ${error.message}`;
            }

            container.appendChild(errorMsg);
        });
    });
}
```

### `__all__` non-field errors

如果validation error唔屬於單一field，例如兩個fields組合先構成錯誤，Django會將佢放喺：

```json
"__all__": [...]
```

前端遇到 `__all__`時只顯示message，唔顯示技術key。

### Field label fallback同 `??`

技術field name未必適合直接顯示，所以建立label map：

```javascript
function getErrorLabel(fieldName) {
    const labels = {
        answer: "答案",
        tips_count: "提示次數",
        user_vocab_id: "Quiz資料",
    };

    return labels[fieldName] ?? fieldName;
}
```

`??`係nullish coalescing operator：

```text
左邊唔係null／undefined → 使用左邊
左邊係null／undefined   → fallback到右邊
```

例子：

```javascript
getErrorLabel("answer");
// "答案"

getErrorLabel("unknown_field");
// "unknown_field"
```

### 點解使用 `textContent`

Error message係文字，唔係可信HTML。使用：

```javascript
errorMsg.textContent = error.message;
```

而唔係將error文字拼入 `innerHTML`，可以避免browser將response內容解讀成HTML。

## 今次驗證結果

已確認：

- Django system check通過。
- Python syntax compilation通過。
- 四個 AJAX views嘅MRO全部使用 `QuizAjaxFormMixin.form_invalid()`。
- 直接建立invalid form並呼叫Next view時，回傳 `400 application/json`及structured errors。
- 直接模擬Submit Answer空答案POST時，回傳 `400 application/json`及 `answer` required error，唔再變成500。
- 成功payload已統一加入 `success=True`。
- Code-path review確認非JSON response會喺 `Content-Type` guard拋出error，network／parse／callback error會由 `.catch()`顯示通用提示，而400 JSON仍會進入structured validation error分支。

目前 `quiz` app顯示 `0 tests`，所以上述證據係system check、syntax check、MRO inspection同直接request驗證，唔代表已有automated test suite coverage。

## 常見錯誤與今次修正

### JavaScript method名稱大小寫

正確：

```javascript
Object.entries(errors)
fieldErrors.forEach(...)
```

錯誤例子：

```javascript
Object.extries(errors)
fieldErrors.foreach(...)
```

JavaScript大小寫敏感。

### `__all__`必須係字串

正確：

```javascript
fieldName === "__all__"
```

如果寫成：

```javascript
fieldName === __all__
```

JavaScript會將 `__all__`當成未定義變數並拋出 `ReferenceError`。

### Template literal插值

正確：

```javascript
`${label}: ${error.message}`
```

`$(label)`只係普通文字，唔會插入變數值。

## 非JSON response與network failure處理

單純直接執行以下程式並不足夠：

```javascript
.then(res => res.json())
```

但Ajax request唔保證任何情況都收到JSON，例如：

- 未處理exception觸發500 HTML page；
- CSRF失敗回傳403 HTML；
- login或quiz session失效後redirect到完整HTML頁；
- URL錯誤回傳404 HTML；
- 網絡中斷或server無法連接。

如果response係HTML：

```html
<!DOCTYPE html>
```

`res.json()`可能拋出：

```text
Unexpected token '<'
```

HTTP 400／500本身通常唔會令 `fetch()`自動reject。只要server成功回傳response，Promise一般仍然fulfilled；前端要自行檢查：

```javascript
response.ok
response.status
response.headers.get("content-type")
```

但 `response.ok === false`唔可以一律當非JSON錯誤，因為invalid form係有用嘅HTTP 400 JSON。

目前已在解析response前檢查 `Content-Type`：

```javascript
.then(async response => {
    const contentType =
        response.headers.get("content-type") || "";

    if (!contentType.includes("application/json")) {
        throw new Error("Expected a JSON response");
    }

    return response.json();
})
```

並已加入通用fallback：

```javascript
.catch(error => {
    console.error(error);

    const errorContainer =
        document.getElementById("quiz-error-message");

    errorContainer.textContent =
        "系統暫時發生問題，請重新整理頁面再試。";
});
```

目前完整分流係：

```text
200 JSON + success=true
→ 更新Quiz partials

400 JSON + success=false
→ 顯示全部form errors

403／404／500 HTML或其他非JSON內容
→ 停止JSON處理，顯示通用錯誤提示

網絡失敗
→ .catch()顯示通用錯誤提示
```

目前實作已形成以上四條分流。要留意 `.catch()`同時會捕捉network failure、非JSON response、JSON parsing failure，以及前面Promise callback內拋出嘅JavaScript error；browser console保留技術error，頁面就只向user顯示安全、可恢復嘅通用訊息。

## 建議補測試

### Backend

- 空答案回傳HTTP 400 JSON，errors包含 `answer` required。
- 無效 `tips_count`回傳HTTP 400 JSON及對應field error。
- 有效答案回傳HTTP 200、`success=True`及兩個partial keys。
- Submit／Next／Skip／Summary views全部使用相同 `form_invalid()` contract。

### Frontend／integration

- 400 JSON會顯示全部field errors，唔會將 `undefined`插入畫面。
- 成功提交會清除舊error messages。
- `__all__`只顯示message。
- 未知field name會fallback顯示原key。
- 403／404／500 HTML唔會被當JSON或partial HTML使用。
- Network failure及JSON parsing failure會顯示通用恢復提示。

目前已用code-path review確認 `Content-Type` guard、throw同 `.catch()`接線正確；執行環境冇Node，因此仍未有JavaScript runtime syntax check或browser integration test。以上項目應保留作之後嘅automated／manual browser verification清單。

## 重點心智模型

遇到AJAX error handling時，可以逐次問：

```text
1. Request可能有邊幾種結果？
2. 每種結果係HTML定JSON？
3. 每種結果HTTP status係幾多？
4. 前端收到後會行邊條分支？
5. User見到咩提示，同埋可以點恢復？
```

今次Quiz flow可以濃縮成：

```text
Django Form validation
  ↓
HTTP status
  ↓
JSON response contract
  ↓
fetch／Promise處理
  ↓
前端錯誤顯示與恢復
```

# Quiz AJAX Response Contract 與錯誤處理

## Report 基準

- 產生時間：2026-09-12 03:51:46 JST
- Repository：`/home/seki/projects/self_projects/japanese-quiz`
- 目前 `HEAD`：`89d30308cf0aa55919a002d8063954d92c1dcb8b`
- 原始修改基準：`11634f6^..11634f6`（建立 Quiz AJAX validation／fallback flow）
- 補充修改基準：`HEAD` 對目前 working tree（收緊 `success` contract；尚未 commit）
- 目前安裝版本：Python package `Django==6.0.5`
- 檢查範圍：`quiz/views.py`、`quiz/helper.py`、`quiz/templates/quiz/quiz_play.html`、`static/js/quiz/quiz_play.js`、相關 forms、tests、commit diff及現有 `ajax_error_handling.md`
- 排除範圍：目前 working tree 內 README、event ordering、VocabRequest notification、status docs及其他與 Quiz AJAX contract 無關嘅修改
- 文件狀態：呢份 report 包含已 commit 嘅原始修改，以及尚未 commit 嘅 strict-success frontend 修改；唔會將後者描述成已 commit。

## 完成度檢查

核心修改已接通，可以建立學習報告：

- 四個 AJAX `FormView` 都透過 `QuizAjaxFormMixin` 使用同一個 invalid-form JSON response。
- Invalid form 會回傳 HTTP 400、`application/json`、`success: false` 同 structured errors。
- 目前各個正常、stale、提早完成及 summary payload 都明確包含 boolean `success: true`。
- Frontend 會分開處理 `false`、`true` 同無效／缺少 `success` 三種情況。
- 非 JSON response、JSON parsing failure、network failure及 callback 內拋出嘅 protocol error會進入同一個 `.catch()` fallback。

未有永久 AJAX contract regression tests，但呢個屬測試覆蓋限制，唔代表核心 flow 未實作。

## 修改目的 1：令 invalid Django form 維持 JSON contract

### 修改目的／理由

Quiz play page用 `fetch()` 提交 form，唔係以普通 full-page POST 運作。原本 views只自訂 `form_valid()`；當 form invalid，Django `FormMixin.form_invalid()`會按一般 HTML view責任 render response。呢啲 action views無 `template_name`，所以普通 validation failure有機會跌入錯誤嘅 HTML／template path，而唔係回傳前端預期嘅 JSON。

修改後將 invalid form定義為預期內嘅 client input failure：

```text
form.is_valid() == False
→ HTTP 400
→ application/json
→ success=false + structured errors
```

### 受影響檔案與責任

- `quiz/views.py`：`QuizAjaxFormMixin.form_invalid()` 建立共用 invalid response；四個 AJAX views透過 MRO取得呢個實作。
- `quiz/forms.py`：提供 validation規則及產生 `form.errors`，本次無需修改。

### 修改前

`quiz/views.py`（`11634f6^`，`QuizSubmitAnswerView`）：

```python
class QuizSubmitAnswerView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, FormView):
    form_class = QuizForm
```

當時無 project-defined `form_invalid()`；invalid branch會繼承 `FormView`／`FormMixin`預設行為。

### 修改後

`quiz/views.py`，`QuizAjaxFormMixin`（目前第 59 行）：

```python
class QuizAjaxFormMixin:
    def form_invalid(self, form):
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status = 400,
        )
```

`quiz/views.py`，AJAX view inheritance（目前第 206 行；其餘 views使用相同次序）：

```python
class QuizSubmitAnswerView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, QuizAjaxFormMixin, FormView):
    form_class = QuizForm
```

### 前後差異與運作解釋

POST進入 `FormView`後，form valid會呼叫 `form_valid()`，invalid就呼叫 `form_invalid()`。將 `QuizAjaxFormMixin`放喺 `FormView`之前，Python MRO會先搵到自訂方法，唔再落入預設 HTML render。

`form.errors.get_json_data()`回傳仍然係 Python dictionary，結構保留每個 field嘅多個 `message`／`code`；外層再由 `JsonResponse`一次過序列化。Non-field errors會使用 `__all__` key，所以 frontend唔可以只處理 `answer`。

HTTP 400喺呢度代表「request格式可處理，但 form data invalid」，並唔等同 server crash。由於 browser Fetch遇到 HTTP 400仍通常會 resolve `Response`，frontend仍可解析呢份 JSON並顯示具體 validation errors。

### 新使用技術

- Django 6.0.5 `JsonResponse`：`HttpResponse` subclass，會序列化 dictionary並預設設定 `Content-Type: application/json`。
- Django `Form.errors.get_json_data()`：將 error data轉成適合 JSON serialization嘅 dictionary，而唔係預先轉成 JSON string。
- Python MRO／CBV mixin：以 inheritance次序覆寫 `FormMixin.form_invalid()`；`QuizAjaxFormMixin`必須排喺 `FormView`之前先會優先命中。

## 修改目的 2：用明確 boolean 區分成功、validation failure同壞 contract

### 修改目的／理由

只靠 `main_html` 是否存在，frontend無法可靠判斷 response語意。第一輪修改加入 `success: true／false`，但 frontend最初只特別處理 `false`；如果 backend漏咗 `success`、回傳 `null` 或字串 `"true"`，程式仍會當成功並把 `undefined` 寫入畫面。

最終 contract係：

```text
success === true  → 唯一成功狀態
success === false → 預期內 form validation failure
其他值            → response contract壞咗，進入通用 fallback
```

### 受影響檔案與責任

- `quiz/views.py`：直接建立嘅 success responses加入 `success: True`。
- `quiz/helper.py`：正常下一題、pool終止及 summary payload統一包含 `success: True`。
- `static/js/quiz/quiz_play.js`：嚴格檢查 response discriminant，拒絕 ambiguous JSON shape。

### 修改前

`quiz/helper.py`（`11634f6^`，正常下一題 payload）：

```python
return {
    "main_html": main_html,
    "input_panel_html": input_panel_html,
}
```

`static/js/quiz/quiz_play.js`（目前 `HEAD`，strict-success 修改之前）：

```javascript
if(data.success === false){
    console.log(data.errors);
    renderFormErrorMessages(data.errors, errorContainer);
    return;
}

errorContainer.replaceChildren();
quizAreaContainer.innerHTML = data.main_html;
quizInputPanelContainer.innerHTML = data.input_panel_html;
```

呢個版本會將 `undefined !== false` 視為可以繼續行成功 branch。

### 修改後

`quiz/helper.py`，`build_next_question_payload()`（目前第 69–97 行）：

```python
if user_vocab_id is None:
    return {
        "success": True,
        "quiz_ended": True,
    }

return {
    "success": True,
    "main_html": main_html,
    "input_panel_html": input_panel_html,
}
```

`quiz/helper.py`，`build_quiz_summary_payload()`（目前第 117–121 行）：

```python
return {
    "success":True,
    "main_html": main_html,
    "input_panel_html": "",
}
```

`static/js/quiz/quiz_play.js`，`quizAreaHandler()`（目前第 34–48 行；呢部分尚未 commit）：

```javascript
if(data.success === false){
    renderFormErrorMessages(data.errors, errorContainer);
    return;
}

if (data.success !== true) {
    throw new Error(
        "Invalid quiz response: missing valid success state"
    );
}

errorContainer.replaceChildren();
quizAreaContainer.innerHTML = data.main_html;
quizInputPanelContainer.innerHTML = data.input_panel_html;
```

### 前後差異與運作解釋

`success`而家係一個 discriminant：佢唔只係方便閱讀，而係決定 frontend可以進入邊條 control-flow branch。

使用 `data.success !== true` 比 truthy check更嚴格：

| 值 | 結果 |
| --- | --- |
| `true` | 更新 partial HTML |
| `false` | 顯示 structured validation errors |
| `undefined`／`null` | protocol error |
| `"true"`／`1` | protocol error |

呢個設計可以令 backend漏 field時即時暴露問題，避免畫面被 `undefined` 靜默破壞。後來嘅 quiz-session recovery會先將 `quiz_ended`轉成 summary payload，再交畀 frontend；所以送到 frontend嘅成功 response仍維持相同 `main_html`／`input_panel_html` shape。

### 新使用技術

- JavaScript strict equality：`===`／`!==`同時比較值及類型，唔會將 `1`、`"true"`等值轉型成 boolean。
- Response discriminant pattern：用固定 field將同一 endpoint family嘅 success、expected failure及invalid contract分流。
- Promise error propagation：`.then()`內 `throw` 會令後續 Promise變成 rejected，交由同一條 `.catch()`處理。

## 修改目的 3：安全顯示所有 Django validation errors

### 修改目的／理由

Django error payload係「field → error array」，一個 field可以有多個 errors，亦可能有 `__all__` non-field errors。Frontend如果只讀 `data.errors.answer[0]`，會漏掉其他欄位同訊息。

Error message亦係文字資料，唔應該直接拼入 `innerHTML`，否則會擴大 HTML injection風險。

### 受影響檔案與責任

- `quiz/templates/quiz/quiz_play.html`：提供 partial replacement範圍外嘅固定 error container。
- `static/js/quiz/quiz_play.js`：將 field key轉成 user-facing label，逐項建立文字節點。

### 修改前

`quiz/templates/quiz/quiz_play.html`（`11634f6^`）：

```html
<h1>Quiz</h1>
<div id="quiz-area-container">
    {% include "quiz/partials/quiz_question_partial.html" %}
</div>
```

當時無專用 AJAX error container，JavaScript亦無 structured error renderer。

### 修改後

`quiz/templates/quiz/quiz_play.html`（目前第 4–7 行）：

```html
<h1>クイズ</h1>
<div id="quiz-error-message" role="alert" aria-live="assertive"></div>
<div id="quiz-area-container" aria-live="polite" aria-atomic="true">
    {% include "quiz/partials/quiz_question_partial.html" %}
</div>
```

`static/js/quiz/quiz_play.js`，`renderFormErrorMessages()`（目前第 72–88 行）：

```javascript
Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
    fieldErrors.forEach(error => {
        const errorMsg = document.createElement("p");

        if (fieldName === "__all__"){
            errorMsg.textContent = error.message;
        } else {
            const label = getErrorLabel(fieldName);
            errorMsg.textContent = `${label}: ${error.message}`;
        }

        container.appendChild(errorMsg);
    });
});
```

### 前後差異與運作解釋

Error container放喺 `quiz-area-container`同 input-panel container之外；更新 partial時唔會順手刪除佢。新 validation response會清走上一輪 errors，再逐個 field、逐個 error建立 `<p>`。

`__all__`本身係 Django transport key，唔適合顯示俾 user，所以只顯示 message。已知 fields透過 label map轉成日文；未知 field使用原 key作 fallback，至少唔會靜默消失。

使用 `textContent`令 browser將 message當純文字，而唔係 HTML。Django 6.0 forms文件亦特別建議 AJAX client用 `textContent`／等效文字 API處理未預先 escape嘅 error JSON。

### 新使用技術

- `Object.entries()`：將 error object展開成 `[fieldName, fieldErrors]` pairs。
- `forEach()`雙層 iteration：完整處理所有 fields及每個 field內多個 errors。
- Nullish coalescing `??`：label只有喺 `null`／`undefined`時先 fallback到原 field name。
- DOM `textContent`：以文字方式插入 server-provided message，避免將內容解讀成 markup。
- ARIA live region：目前 error container使用 `role="alert"`及 `aria-live="assertive"`；呢項 accessibility強化係後續修改，唔係原始 `11634f6` commit本身。

## 修改目的 4：將非 JSON同非預期 failure導向可恢復 fallback

### 修改目的／理由

AJAX endpoint唔保證每次都回 JSON。Login／session guard redirect、CSRF failure、404、未處理 500或 proxy error都可能回完整 HTML；network亦可能直接失敗。原本無條件執行 `res.json()`，user只會見到畫面無反應，console可能出現 JSON parsing error。

### 受影響檔案與責任

- `static/js/quiz/quiz_play.js`：解析前驗證 `Content-Type`，並用 `.catch()`統一顯示通用恢復提示。

### 修改前

`static/js/quiz/quiz_play.js`（`11634f6^`）：

```javascript
fetch(form.action, {
    method: form.method,
    body: new FormData(form),
    headers:{
        'X-Requested-With': "XMLHttpRequest"
    }
})
.then(res => res.json())
.then(data => {
    quizAreaContainer.innerHTML = data.main_html;
    quizInputPanelContainer.innerHTML = data.input_panel_html;
})
```

### 修改後

`static/js/quiz/quiz_play.js`，response parsing及 fallback（目前第 20–29、51–59 行）：

```javascript
.then(async res => {
    const contentType = res.headers.get("content-type") || "";

    if(!contentType.includes("application/json")){
        throw new Error(
            `Expected JSON, received ${contentType}`
        );
    }

    return res.json();
})
.catch(error => {
    console.error(error);

    const errorContainer =
        document.getElementById("quiz-error-message");

    errorContainer.textContent =
        "エラーが発生しました。ページを再読み込みして、もう一度お試しください。";
});
```

### 前後差異與運作解釋

Fetch嘅 Promise唔會單純因為 server回 400／404／500而 reject；佢通常會先 resolve一個 `Response`。本 project刻意唔將所有 `response.ok === false`直接丟去 generic error，因為 HTTP 400 JSON係有用嘅 form-validation contract。

所以解析順序係：

```text
收到 Response
→ Content-Type係咪 JSON？
→ 解析 JSON
→ success係 false、true，定無效？
→ 顯示 field errors、更新畫面，或 throw到 fallback
```

以下情況會落入 `.catch()`：

- network failure；
- response唔係 JSON；
- JSON body syntax錯誤；
- JSON成功解析，但缺少合法 boolean `success`；
- 前面 Promise callback拋出其他 JavaScript exception。

Console保留技術 error方便開發者調查；頁面只顯示安全、可恢復嘅日文提示，避免向 user洩漏 stack trace或內部資料。

### 新使用技術

- Fetch API `Response.headers`／`Response.json()`：先檢查 media type，再非同步解析 body。
- Promise `.catch()`：集中處理 transport、parsing及 protocol failures。
- `Content-Type` guard：避免將 HTML error page當成 JSON contract。

## 整體行為改變

```text
Quiz form submit
  ↓
Django FormView驗證
  ├─ invalid
  │    ↓
  │  400 JSON：success=false + errors
  │    ↓
  │  frontend安全顯示每項error，保留目前題目
  │
  └─ valid
       ↓
     200 JSON：success=true + partial HTML
       ↓
     frontend清除舊error並更新畫面

任何非JSON／parse failure／非法success值
  ↓
Promise rejected
  ↓
顯示通用重新整理提示
```

修改前，frontend只假設收到兩段 HTML；修改後，HTTP content type、Django validation errors、application success state同 protocol failure各有明確責任。

## 測試及驗證結果

今次實際執行：

```text
git diff --check
```

- 通過；相關 diff無 whitespace error。

```text
.venv/bin/python manage.py check
```

- 通過：`System check identified no issues (0 silenced).`

```text
.venv/bin/python manage.py test quiz core
```

- 建立隔離 test database並執行 10 tests，全部通過。
- `quiz`目前無專用 AJAX contract test；10 tests主要來自既有 `core` suite，因此唔應理解為 strict contract已被完整 regression coverage。

今次即場 read-only Django shell probe：

- 建立 invalid `QuizForm`。
- 直接呼叫 `QuizAjaxFormMixin.form_invalid()`。
- 驗證 HTTP status係400。
- 驗證 `Content-Type`係 `application/json`。
- 驗證 payload包含 `success: false`，以及三個 required field errors。
- 驗證 `QuizSubmitAnswerView`、`QuizNextView`、`QuizSkipView`、`QuizSummaryView`嘅 `form_invalid`都 resolve到 `QuizAjaxFormMixin.form_invalid`。

```text
node --check static/js/quiz/quiz_play.js
```

- 通過；strict-success working-tree修改無 JavaScript syntax error。

## 已知限制／未驗證事項

- 未有 browser integration test實際餵入 `success`缺失、`null`、字串值或 malformed JSON，strict branch目前由 code inspection及 syntax check支持。
- 未有永久 backend regression test覆蓋各 AJAX endpoint嘅 valid／invalid response status、content type及 keys。
- `renderFormErrorMessages()`假設 `success: false`必定附帶正確 shape嘅 `errors` object；如果 error payload本身 malformed，函式會拋 exception並由 generic `.catch()`處理，而唔會提供更精細訊息。
- 目前只檢查 response `Content-Type`同 application-level `success`，無為每種 success state建立完整 runtime schema validation，例如確認 `main_html`一定係 string。
- Submit期間未 disable form；快速雙擊／並行POST屬另一個 idempotency問題，唔係呢份 response-contract修改已解決嘅範圍。
- 原始 `ajax_error_handling.md`內「無下一題 payload缺少 `success=True`」同「缺少 `success`仍當成功」已經過時；本 report按目前 code修正咗呢兩點。

## 官方參考資料

- [Django 6.0 — `JsonResponse`](https://docs.djangoproject.com/en/6.0/ref/request-response/#jsonresponse-objects)：確認 dictionary serialization同預設 `application/json` content type。
- [Django 6.0 — Forms API／`get_json_data()`](https://docs.djangoproject.com/en/6.0/ref/forms/api/#django.forms.Form.errors.get_json_data)：確認 structured error dictionary，同以 `textContent`安全顯示 AJAX error文字嘅建議。
- [Django 6.0 — `FormMixin.form_invalid()`](https://docs.djangoproject.com/en/6.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_invalid)：確認預設 invalid branch會 render包含 invalid form嘅 response。
- [Django 6.0 — CBV mixins](https://docs.djangoproject.com/en/6.0/topics/class-based-views/mixins/)：說明以 mixin重用 JSON response責任嘅模式。
- [MDN — Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)：確認 HTTP error status通常唔會令 Fetch Promise自動 reject、Content-Type guard、`Response.json()`及 Promise error handling行為。

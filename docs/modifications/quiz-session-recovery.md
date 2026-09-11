# M-01：Quiz 失效 Session 終止及復原

## Report 基準

- 產生時間：2026-09-12 00:40:39 JST
- Git branch：`main`
- 修改前基準：`HEAD` commit `9062a2ea41e4e46f5f3b27fcaedf303be0e4f0d4`（`feat: add email verification for new user accounts`）
- 修改後狀態：目前 working tree；本報告記錄嘅 M-01 修改尚未 commit
- 使用者指定主題：上一份 project review 嘅 M-01——失效 quiz session 缺少 terminal recovery，而且 unfinished flow 可以重新開啟已不符合出題資格嘅題目
- 主要檢查範圍：
  - `quiz/helper.py`
  - `quiz/service/quiz.py`
  - `quiz/views.py`
  - `quiz/templates/quiz/partials/quiz_summary_partial.html`
  - `quiz/tests.py`、`core/tests.py`
  - `dictionary/models.py` 中 `Vocab.is_active`、`UserVocab.in_use` 與兩者關係
- 背景 commit：
  - `9062a2e`：Email activation；無修改上述 quiz recovery 檔案
  - `012ae67`：加入 full-pool 確認流程，取消無匹配時自動 fallback，亦集中處理開始 quiz 前嘅不足 pool 情況；M-01 係呢個設計之後嘅「進行中 session 失效」邊界
- 排除嘅無關 working-tree 修改：Email canonicalization、accounts migration、README、status docs、文件目錄搬遷，以及其他唔屬於 M-01 嘅學習文件

## 完成度檢查

M-01 嘅核心行為已經接通，可以建立本報告：

1. Resume unfinished quiz 時，會重新檢查目前題目係咪仍屬於該 user、`UserVocab.in_use=True`，以及相關 `Vocab.is_active=True`。
2. Submit answer 時，無論正常提交定 stale／duplicate form 分支，都會重新檢查 session 目前題目嘅出題資格。
3. Skip 時，service 會先檢查出題資格；題目已失效就唔會再修改 weight、streak 或 last quiz time。
4. Answer／skip 後再抽下一題，如果 pool 已經變空，會顯示提早結束 summary，而唔係停留喺無法完成嘅 session。
5. 結束 summary 或 resume 失敗時，會移除 `quiz_session`，避免設定頁再次將 user 送返失效 unfinished flow。

完成度結論只代表控制流程經 code inspection 已齊全，唔代表所有邊界已有自動化驗證。`quiz/tests.py` 仍然係 placeholder，未有 M-01 integration tests；呢點記錄於「已知限制／未驗證事項」。

## 修改目的 1：將「下一題已不存在」變成明確終止狀態

### 修改目的／理由

修改前，`build_next_question_payload()` 遇到空 pool，只係回傳「無題目」HTML。佢無清除 `quiz_session`，亦無明確話俾 caller 知 quiz 已經結束。

因此 browser 畫面雖然顯示無題，但 server session 仍然保留「未達目標題數、目前無題目」嘅狀態。User 再返 setting 時，`QuizSettingView` 會將呢個 session 當成 unfinished quiz，再 redirect 去 `QuizUnfinishedView`，形成無法正常完結嘅循環。

修改後將責任分開：

- `build_next_question_payload()` 負責抽題；抽唔到就回傳 `quiz_ended=True` 呢個狀態訊號。
- `QuizNextView`／`QuizSkipView` 負責理解訊號，決定提早完結。
- `build_quiz_summary_payload()` 負責建立 summary payload 同清除 session。

### 受影響檔案與責任

- `quiz/helper.py`：由抽題 helper 回報 terminal state；新增共用 summary builder。
- `quiz/views.py`：`QuizNextView`、`QuizSkipView` 將 `quiz_ended` 轉成提早完結 response。
- `quiz/templates/quiz/partials/quiz_summary_partial.html`：向 user 解釋點解 quiz 提早完結。

### 修改前

`quiz/helper.py` — `build_next_question_payload()`（`HEAD`）

```python
if user_vocab_id is None:
    return {
        "main_html": render_to_string(
            "quiz/partials/quiz_no_question_partial.html",
            request=request,
        ),
        "input_panel_html": "",
    }
```

`quiz/views.py` — `QuizNextView.form_valid()`（`HEAD`）

```python
def form_valid(self, form):
    payload = build_next_question_payload(request=self.request)
    return JsonResponse(payload)
```

修改前嘅 helper 直接選擇畫面內容，但無改變 session lifecycle；view 亦只係原樣送出 payload，無 terminal transition。

### 修改後

`quiz/helper.py:64` — `build_next_question_payload()`

```python
if user_vocab_id is None:
    #request.session.pop("quiz_session", None)
    return {
        "success": True,
        "quiz_ended": True,
    }
```

`quiz/views.py:334` — `QuizNextView.form_valid()`

```python
payload = build_next_question_payload(request=self.request)
if payload.get("quiz_ended"):
    summary_payload = build_quiz_summary_payload(
        request=self.request,
        end_reason="no_question_pool",
        ended_early=True,
    )
    return JsonResponse(summary_payload)
return JsonResponse(payload)
```

`quiz/views.py:374` — `QuizSkipView.form_valid()` 抽取下一題嘅同類分支

```python
payload = build_next_question_payload(request=self.request, is_skip=True)
if payload.get("quiz_ended"):
    summary_payload = build_quiz_summary_payload(
        request=self.request,
        end_reason="no_question_pool",
        ended_early=True,
    )
    return JsonResponse(summary_payload)
return JsonResponse(payload)
```

### 前後差異與運作解釋

正常 Next 流程變成：

1. `QuizNextView` 呼叫 `build_next_question_payload()`。
2. Helper 重新按目前 quiz settings 建立 eligible pool。
3. Pool 有題：照常寫入新 `question_user_vocab_id`，增加 `quizzed_count`，回傳題目 HTML。
4. Pool 無題：helper 唔再自行決定 UI，而係回傳 `quiz_ended=True`。
5. View 收到 terminal signal，呼叫 `build_quiz_summary_payload()`。
6. Summary builder 先用現有統計 render 結果，再 `pop()` 掉 `quiz_session`。
7. Frontend 沿用原本 AJAX contract，將 `main_html` 換成 summary，並清空 input panel。

Skip 流程同樣會處理「成功 skip 當前題後，已經再無下一題」嘅情況。`is_skip=True` 保留原有題數語意：skip 已經計入 `skipped_count`，抽下一題時唔額外增加 `quizzed_count`。

`quiz_ended` 只係 helper 同 view 之間嘅內部控制訊號，最終送到 browser 嘅仍然係既有格式：

```python
{
    "success": True,
    "main_html": "...",
    "input_panel_html": "",
}
```

所以 `static/js/quiz/quiz_play.js` 唔需要為 M-01 加新分支。

### 新使用技術

#### 明確狀態訊號（established project technique）

`quiz_ended=True` 將「抽唔到題」由一段指定 HTML 提升成 domain state。Helper 唔再假設 caller 一定要顯示某個 partial；由 view 決定係終止、redirect，定採用其他產品流程。呢個唔係新 library，而係將 control flow 同 presentation responsibility 分開。

#### Django `JsonResponse`

Project 使用 Django `6.0.5`。`JsonResponse` 係 `HttpResponse` subclass，會將 dict 編碼成 JSON，預設 `Content-Type` 為 `application/json`。M-01 沿用現有 AJAX response contract，所以前端仍可用同一段 `fetch(...).then(res => res.json())` 處理正常題目同 terminal summary。

## 修改目的 2：每次操作目前題目之前重新驗證 eligibility

### 修改目的／理由

Question pool 只代表「抽題嗰一刻」嘅資料狀態，唔保證 user 作答／skip 嗰一刻仍然有效。例如：

- User 喺另一個 browser tab 將目前 `UserVocab.in_use` 關閉。
- Admin 將相關 `Vocab.is_active` 關閉。
- Session 保存嘅 `UserVocab` 已被刪除。

修改前嘅 submit、stale form recovery 同 skip 只按 primary key 及 user 查 object。只要 row 仲存在，即使已經不應出題，仍會顯示、批改或施加 skip punishment。

修改後將以下條件視為「目前題目有效」嘅完整判斷：

```text
UserVocab.pk == session／form 題目 ID
AND UserVocab.user == request.user
AND UserVocab.in_use == True
AND UserVocab.vocab.is_active == True
```

任何條件失敗，都會提早終止 quiz，而唔係靜靜抽另一題。呢個符合今次產品決定：目前畫面上嗰題失效係 session 狀態改變，user 應該收到明確通知；其他未顯示題目嘅變動，就由下一次建立 pool 時自然反映。

### 受影響檔案與責任

- `quiz/views.py`：submit answer 前檢查 session／posted question；失效時建立 terminal summary。
- `quiz/service/quiz.py`：skip punishment 前做同一套 eligibility 檢查，並以 Boolean 回報有冇成功修改資料。
- `dictionary/models.py`：既有 `UserVocab.in_use` 與 `Vocab.is_active` 欄位係 eligibility 判斷來源；M-01 無修改 model 或 schema。

### 修改前

`quiz/views.py` — stale／duplicate submit 分支（`HEAD`）

```python
target_vocab = get_object_or_404(
    UserVocab,
    pk=session_question_user_vocab_id,
    user=self.request.user,
)
```

`quiz/views.py` — 正常 submit 分支（`HEAD`）

```python
question_vocab = get_object_or_404(
    UserVocab,
    pk=form.cleaned_data.get("user_vocab_id"),
    user=self.request.user
)
```

`quiz/service/quiz.py` — `QuizService.skip_question_punish()`（`HEAD`）

```python
skipped_user_vocab = UserVocab.objects.filter(pk=user_vocab_id, user=user).first()
if skipped_user_vocab is not None:
    skipped_user_vocab.weight += QUIZ_CONFIG["weight"]["skip"]
    if skipped_user_vocab.streak > 0:
        skipped_user_vocab.streak = 0
    else:
        skipped_user_vocab.streak -= 1
    skipped_user_vocab.last_quiz_at = timezone.now()
    skipped_user_vocab.save(
        update_fields=["weight","streak","last_quiz_at"]
    )
```

呢三個查詢都無檢查 `in_use` 或相關 vocabulary 嘅 `is_active`。

### 修改後

`quiz/views.py:233` — stale／duplicate submit 嘅目前題目查詢

```python
target_vocab = (
    UserVocab.objects
    .filter(
        pk=session_question_user_vocab_id,
        user=self.request.user,
        in_use=True,
        vocab__is_active=True,
    ).select_related("vocab").first()
)
if target_vocab is None:
    payload = build_quiz_summary_payload(
        request=self.request,
        end_reason="question_unavailable",
        ended_early=True,
    )
    return JsonResponse(payload)
```

`quiz/views.py:261` — 正常 submit 嘅題目查詢

```python
question_vocab = (
    UserVocab.objects
    .filter(
        pk=form.cleaned_data.get("user_vocab_id"),
        user=self.request.user,
        in_use=True,
        vocab__is_active=True,
    ).select_related("vocab").first()
)
if question_vocab is None:
    payload = build_quiz_summary_payload(
        request=self.request,
        end_reason="question_unavailable",
        ended_early=True
    )
    return JsonResponse(payload)
```

`quiz/service/quiz.py:88` — `QuizService.skip_question_punish()`

```python
skipped_user_vocab = UserVocab.objects.filter(
    pk=user_vocab_id,
    user=user,
    in_use=True,
    vocab__is_active=True,
).first()
if skipped_user_vocab is None:
    return False

skipped_user_vocab.weight += QUIZ_CONFIG["weight"]["skip"]
if skipped_user_vocab.streak > 0:
    skipped_user_vocab.streak = 0
else:
    skipped_user_vocab.streak -= 1
skipped_user_vocab.last_quiz_at = timezone.now()
skipped_user_vocab.save(
    update_fields=["weight","streak","last_quiz_at"]
)
return True
```

`quiz/views.py:351` — `QuizSkipView.form_valid()`

```python
skip_succeeded = QuizService.skip_question_punish(user=self.request.user, user_vocab_id=skipped_question_vocab_id)
if not skip_succeeded:
    summary_payload = build_quiz_summary_payload(
        request=self.request,
        end_reason="question_unavailable",
        ended_early=True,
    )
    return JsonResponse(summary_payload)
```

### 前後差異與運作解釋

#### 點解由 `get_object_or_404()` 改做 `.filter(...).first()`

喺普通 detail page，object 唔存在通常代表 URL 指向無效 resource，回傳 HTTP 404 合理。但 M-01 呢度嘅「object 搵唔到」亦可能代表題目剛剛被停用；呢個係預期嘅 domain transition，唔係整個 AJAX endpoint 消失。

`.first()` 搵唔到會回傳 `None`，view 因而可以：

1. 保留目前 quiz 統計；
2. render 一個有原因嘅 summary；
3. 清除失效 session；
4. 以正常 JSON response 完成 UI transition。

如果繼續用 `get_object_or_404()`，frontend 會收到 HTML 404 response，而 `quiz_play.js` 預期 JSON，結果只會落入 generic error handling，user 唔會得到正確嘅「題目已失效」說明。

#### 點解 skip service 要回傳 `True`／`False`

修改前，service 搵唔到 object 時只係乜都唔做，caller 無法分辨：

- punishment 成功；或
- 題目已不存在／已失效。

修改後嘅 Boolean 係 service outcome contract：

- `True`：已驗證 eligibility，亦已更新 weight、streak、last quiz time。
- `False`：無符合條件嘅 object，任何 punishment 同 skip count 都唔應該寫入。

View 只會喺 `True` 後清空目前題目同增加 `skipped_count`，避免將一次無效操作記成真實 skip。

### 新使用技術

#### Django relationship lookup：`vocab__is_active=True`

Double underscore lookup 俾 QuerySet 沿 model relationship 過濾欄位。呢度由 `UserVocab.vocab` 呢個 `ForeignKey` 跨到 `Vocab.is_active`，由 database query 一次判斷 row 同相關 vocabulary 嘅狀態。

#### Django `select_related("vocab")`

`select_related()` 會用 SQL join 預先載入指定嘅 `ForeignKey`／`OneToOneField` object。要留意：`vocab__is_active=True` 本身已經可以跨 relationship 過濾，唔需要靠 `select_related()` 先「拎到」欄位；今次加 `select_related("vocab")` 嘅用途係查詢成功後，render／批改會再讀 `question_vocab.vocab`，預先載入可避免額外一次 lazy-load query。

#### QuerySet `.first()` 作為可處理失敗結果

`.first()` 將「無符合資料」表達成 `None`。今次唔係忽略錯誤，而係刻意將資料失效納入 application flow，再由 view 決定 terminal response。

## 修改目的 3：安全恢復 unfinished quiz，無法恢復就清理 session

### 修改目的／理由

User 重開 quiz setting 時，如果 session 仍有 `question_user_vocab_id`，會進入 `QuizUnfinishedView`。修改前只要該 ID 屬於 user，就會重新顯示題目；即使 `in_use=False` 或 vocabulary 已經 inactive，仍會 HTTP 200 開返題目。

另外，如果 session 目前無題，而重新建立 pool 又抽唔到題，修改前只 redirect 去 user vocabulary list，但保留 `quiz_session`。User 再返 setting，就會再次被判定為 unfinished session。

修改後將 resume 分成三個明確結果：

1. Session 有 current question，而且仍 eligible：繼續顯示同一題。
2. Session 有 current question，但已失效／刪除：清除 session，通知 user，返 quiz setting。
3. Session 無 current question：由最新 pool 抽題；如果 pool 已空，清除 session，通知 user，返 quiz setting。

### 受影響檔案與責任

- `quiz/views.py`：`QuizUnfinishedView.get()` 驗證保存咗嘅題目 ID，處理 invalid ID 同 empty pool，並建立新題目時先更新 session。
- `quiz/helper.py`／`quiz/service/quiz.py`：沿用最新 quiz settings 建立符合 `in_use`／active 規則嘅 pool。

### 修改前

`quiz/views.py` — `QuizUnfinishedView.get()`（`HEAD`）

```python
if unfinished_question_user_vocab_id:
    user_vocab_id = unfinished_question_user_vocab_id
    messages.warning(
        request,
        "まだ回答していない問題があります。"
    )
else:
    question_pool_qs = get_question_pool(request=self.request)
    user_vocab_id = get_target_user_vocab_id(user=self.request.user, pool_queryset=question_pool_qs)
    quiz_session["quizzed_count"] += 1

if user_vocab_id is None:
    messages.warning(
        request,
        "出題できる単語がありません。マイ単語帳で単語を出題対象に設定してください。"
    )
    return redirect("dictionary:user_vocab_list")

quiz_session["question_user_vocab_id"] = user_vocab_id
request.session["quiz_session"] = quiz_session
self.question_vocab = get_object_or_404(UserVocab, pk=user_vocab_id, user=self.request.user)
```

問題有兩個：existing ID 無 eligibility check；而 pool 空嗰條 return path 無移除 session。

### 修改後

`quiz/views.py:387` — `QuizUnfinishedView.get()` existing question 分支

```python
if unfinished_question_user_vocab_id is not None:
    unfinished_question_user_vocab = (
        UserVocab.objects
        .filter(
            user=request.user,
            pk=unfinished_question_user_vocab_id,
            in_use=True,
            vocab__is_active=True,
        ).select_related("vocab").first()
    )
    if unfinished_question_user_vocab is None:
        request.session.pop("quiz_session", None)
        messages.warning(
            request,
            "現在の問題が出題対象から外れたため、クイズを終了しました。"
        )
        return redirect("quiz:quiz_setting")

    self.question_vocab = unfinished_question_user_vocab
```

`quiz/views.py:415` — 無 current question、重新抽題分支

```python
question_pool_qs = get_question_pool(request=self.request)
user_vocab_id = get_target_user_vocab_id(
    user=self.request.user,
    pool_queryset=question_pool_qs
)

if user_vocab_id is None:
    self.request.session.pop("quiz_session", None)
    messages.warning(
        request,
        "出題できる問題がないため、クイズを終了しました。"
    )
    return redirect("quiz:quiz_setting")

self.question_vocab = get_object_or_404(question_pool_qs, pk=user_vocab_id, user=self.request.user)
quiz_session["quizzed_count"] += 1
```

最後只會將已驗證／已由 eligible pool 抽出嘅 object 寫返 session：

```python
quiz_session["question_user_vocab_id"] = self.question_vocab.pk
request.session["quiz_session"] = quiz_session
```

### 前後差異與運作解釋

#### 用 `is not None`，唔用 truthiness

Session 欄位嘅語意係：

- `None`：目前未有題目，應抽下一題。
- Integer ID：應嘗試恢復該題。

`is not None` 直接表達呢個 state boundary，唔會將其他 falsy value 誤當「無題目」。正常 database primary key 唔會係 `0`，所以原本 truthiness 多數時間都 work，但新寫法更貼近資料語意。

#### 點解失效後返 quiz setting，而唔係靜靜換題

目前題目已經顯示俾 user；另一個 tab 或 admin 改變咗佢嘅 eligibility，代表 quiz 嘅可見狀態同 server 真實狀態已分歧。直接換另一題會令 user 唔知道發生過乜，亦可能覺得題數突然改變。

因此 M-01 將目前題目失效視為 terminal event：清 session、顯示原因、返 setting。至於其他未顯示題目被停用，下一次 `get_question_pool()` 自然排除即可，唔需要中止當前有效題目。

#### 點解要先 `pop()` session 再 redirect

只 redirect 唔會改變 server state。若 `quiz_session` 仍保存，而且 `aims_quiz_num > quizzed_count`，`QuizSettingView` 下一次仍會當佢係 unfinished，重新 redirect 去 unfinished route。`pop("quiz_session", None)` 先真正完成 state transition，redirect 只係之後嘅 navigation。

### 新使用技術

#### Django session dictionary API：`pop()`

Project 使用 Django `6.0.5`。`request.session` 係 dictionary-like object；`pop("quiz_session", None)` 會安全移除 key，就算 key 已經不存在亦唔會拋 `KeyError`。刪除 session key 會令 session 被標記為已修改，response 完成時由 session middleware 儲存新狀態。

#### QuerySet 作為 `get_object_or_404()` 第一個參數

新題先由 `question_pool_qs` 抽出 ID，再用同一個 eligible QuerySet 取 object：

```python
get_object_or_404(question_pool_qs, pk=user_vocab_id, user=self.request.user)
```

相對於直接由 `UserVocab` manager 查詢，呢種寫法保留 QuerySet 已有嘅 pool eligibility 條件，令「抽中」同「實際載入」使用同一套範圍。

## 修改目的 4：統一正常完成與提早完成嘅 summary lifecycle

### 修改目的／理由

正常完成、pool 中途變空、目前題目失效，三者最後都要做相同基本工作：

1. 用 session 統計 render summary；
2. 清空 input panel；
3. 移除 `quiz_session`。

如果每個 view 各自複製呢段程式，任何一條分支漏咗 session cleanup，就會重現 M-01。修改後集中到 `build_quiz_summary_payload()`，再用 `ended_early` 同 `end_reason` 表達 UI 差異。

### 受影響檔案與責任

- `quiz/helper.py`：建立共用 summary response payload，並成為 session terminal cleanup 嘅單一位置。
- `quiz/views.py`：正常 `QuizSummaryView` 同各個 recovery branch 共用 helper。
- `quiz/templates/quiz/partials/quiz_summary_partial.html`：只喺提早完結時顯示相應原因。

### 修改前

`quiz/views.py` — `QuizSummaryView.form_valid()`（`HEAD`）

```python
main_html = render_to_string(
    "quiz/partials/quiz_summary_partial.html",
    context={
        "current_quiz_num": quiz_session["quizzed_count"],
        "total_quiz_num": quiz_session["aims_quiz_num"],
        "correct_count":quiz_session["correct_count"],
        "wrong_count":quiz_session["wrong_count"],
        "skipped_count":quiz_session["skipped_count"],
        "total_tips_count":quiz_session["total_tips_count"],
    },
    request=self.request,
)
self.request.session.pop("quiz_session", None)
return JsonResponse({
            "success": True,
            "main_html": main_html,
            "input_panel_html": "",
        })
```

只有正常 summary view 擁有完整 render + cleanup 流程，其他提早結束路徑無可重用入口。

### 修改後

`quiz/helper.py:99` — `build_quiz_summary_payload()`

```python
def build_quiz_summary_payload(*, request, end_reason=None, ended_early=False):
    quiz_session = request.session.get("quiz_session",{})
    main_html = render_to_string(
        "quiz/partials/quiz_summary_partial.html",
        context={
            "current_quiz_num": quiz_session["quizzed_count"],
            "total_quiz_num": quiz_session["aims_quiz_num"],
            "correct_count":quiz_session["correct_count"],
            "wrong_count":quiz_session["wrong_count"],
            "skipped_count":quiz_session["skipped_count"],
            "total_tips_count":quiz_session["total_tips_count"],
            "ended_early": ended_early,
            "end_reason": end_reason,
        },
        request=request,
    )

    request.session.pop("quiz_session", None)
    return {
        "success":True,
        "main_html": main_html,
        "input_panel_html": "",
    }
```

`quiz/templates/quiz/partials/quiz_summary_partial.html:1`

```django
<h2 class="quiz-content-heading" tabindex="-1">クイズ結果</h2>
{% if ended_early %}
    {% if end_reason == "question_unavailable" %}
        <p>現在の問題が出題対象から外れたため、クイズを終了しました。</p>
    {% elif end_reason == "no_question_pool" %}
        <p>出題できる問題がなくなったため、クイズを終了しました。</p>
    {% endif %}
{% endif %}
```

`quiz/views.py:458` — 正常完成亦改用同一 helper

```python
quiz_session = self.request.session.get("quiz_session",{})
payload = build_quiz_summary_payload(request=self.request)
logger.info(
    "Quiz completed: "
    "operation=%s user_id=%s quiz_count=%s target_count=%s correct_count=%s wrong_count=%s skipped_count=%s total_tips_count=%s",
    "quiz_complete",
    self.request.user.pk,
    quiz_session["quizzed_count"],
    quiz_session["aims_quiz_num"],
    quiz_session["correct_count"],
    quiz_session["wrong_count"],
    quiz_session["skipped_count"],
    quiz_session["total_tips_count"],
)
return JsonResponse(payload)
```

### 前後差異與運作解釋

`build_quiz_summary_payload()` 嘅操作次序特別重要：

1. 先用 `quiz_session` render HTML；
2. 再移除 session；
3. 最後回傳 payload。

如果先 `pop()` 再 render，就無法取得統計數字。正常 `QuizSummaryView` 要寫 completion log，所以佢喺呼叫 helper 前先將 session dict 保存到 local variable；helper 清除 request session 後，local variable 仍可用嚟記錄數字。

`ended_early=False` 係預設值，正常完成唔會顯示警告。提早完結 caller 會同時傳：

- `ended_early=True`
- `end_reason="question_unavailable"` 或 `"no_question_pool"`

Template 唔需要理解 database object，只需要將穩定 reason code 轉成 user-facing 日文。

### 新使用技術

#### `render_to_string()` 共用 partial rendering

`render_to_string()` 用指定 template 同 context 產生 HTML string。今次唔係首次在 project 使用，但 M-01 將佢包入共用 terminal helper，令多個 AJAX endpoint 可以返回同一種 summary UI 同 cleanup 行為。

#### Reason code 與 presentation mapping

`question_unavailable`、`no_question_pool` 係 server-side reason code；日文文字留喺 template。呢個做法避免 view 到處複製完整 UI 句子，亦容許日後改 wording 而唔改 control flow。

## 整體行為改變

### 修改前

```text
進行中 quiz
  ├─ 下一題 pool 空
  │    └─ 顯示「無題」partial，但 quiz_session 保留
  │          └─ 再返 setting → 又被送去 unfinished
  ├─ current UserVocab 被關閉／Vocab inactive
  │    ├─ submit：仍可批改
  │    ├─ skip：仍可修改 weight／streak
  │    └─ resume：仍可重新顯示
  └─ session current ID 已刪除
       └─ 404／無法以正常 quiz UI 解釋
```

### 修改後

```text
進行中 quiz
  ├─ 操作目前題目
  │    ├─ eligible → 正常 submit／skip／resume
  │    └─ unavailable → reason=question_unavailable
  │                         → summary／message
  │                         → 清除 quiz_session
  └─ 抽下一題
       ├─ pool 有題 → 寫入新 question ID，繼續
       └─ pool 空 → reason=no_question_pool
                     → summary／redirect message
                     → 清除 quiz_session
```

最重要嘅語意改變係：失效資料唔再當成普通「搵唔到 object」，而係 quiz session 嘅 terminal state。畫面 navigation 同 server session state 會一齊完成 transition。

## 測試及驗證結果

### 實際執行

1. `git diff --check`
   - 結果：通過；無 whitespace error。
2. `.venv/bin/python manage.py check`
   - Django：`6.0.5`
   - 結果：`System check identified no issues (0 silenced).`
3. `.venv/bin/python manage.py test`
   - 結果：10 個 tests 全部通過。
   - 執行時間：1.102 秒。
   - 使用 Django 自動建立及銷毀 test database，無操作開發用 `db.sqlite3`。

### 只作檢查、未有自動測試證據

- `quiz/tests.py` 只有 Django placeholder，無 M-01 專用 tests。
- `rg` 搜尋現有 test files，無發現覆蓋以下 reason／symbol 嘅測試：
  - `question_unavailable`
  - `no_question_pool`
  - `quiz_ended`
  - `QuizUnfinishedView`
  - `QuizNextView`
  - `QuizSkipView`
  - `skip_question_punish`
- 現有 10 個 tests 位於 `core/tests.py`，主要驗證 template、語言切換、通知文字同 vocabulary label；全綠只能證明 M-01 無破壞呢批既有行為，唔能夠證明 recovery 分支本身正確。

### Code inspection 覆蓋嘅分支

- stale／duplicate answer，而 session current question 仍有效：重新顯示正確 current question。
- stale／duplicate answer，而 session current question 已失效：提早 summary + 清 session。
- 正常 answer，但 posted／current question 已失效：唔批改，提早 summary + 清 session。
- skip current question 已失效：唔更新 UserVocab，唔增加 skip count，提早 summary + 清 session。
- answer／skip 後下一題 pool 空：提早 summary + 清 session。
- unfinished session current question 有效：恢復同一題。
- unfinished session current question 已失效／刪除：清 session + warning + redirect setting。
- unfinished session 無 current question，而且 pool 空：清 session + warning + redirect setting。

## 已知限制／未驗證事項

1. **未有 M-01 integration tests。** 呢個係目前最大嘅驗證缺口。應以 Django test client 建立 session，再模擬另一個 tab／admin 改 `in_use`、改 `is_active` 或刪除 `UserVocab`，逐一驗證 response、統計數字、database mutation 同 session cleanup。
2. **抽出 ID 同重新載入 object 之間仍有短暫 race window。** `build_next_question_payload()` 先由 eligible QuerySet 抽 ID，再由 `UserVocab` manager 取 object；如果資料啱啱喺兩次 query 之間被刪除或停用，仍可能出現 404 或載入剛失效 object。`QuizUnfinishedView` 新抽題分支已用原本 `question_pool_qs` 重新載入，`build_next_question_payload()` 同 `QuizPlayView` 尚未完全統一呢個做法。
3. **Terminal summary helper 依賴完整 session schema。** `build_quiz_summary_payload()` 用 `quiz_session["..."]` 讀必需統計欄位；如果 session 本身損壞或由舊版本留下缺欄位，會拋 `KeyError`。M-01 處理嘅係題目 eligibility／empty pool，唔包括任意 session corruption recovery。
4. **Stale／duplicate submit 而 `question_user_vocab_id is None` 仍屬另一個行為。** 呢條既有分支會回傳 no-question partial，唔會經 M-01 summary helper；佢較接近 duplicate request／idempotency 問題，應同 review M-03 一併處理，而唔應誤稱已由 M-01 解決。
5. **有非功能性 cleanup 可後補。** `quiz/helper.py` 有已註解嘅 `request.session.pop(...)`；`QuizUnfinishedView` 有未再使用嘅 local `user_vocab_id`，以及位於 `else` 內但仍重複檢查 `unfinished_question_user_vocab_id is None`。佢哋唔阻止核心功能，但會增加閱讀成本。

## 官方參考資料

以下文件版本同 project 安裝嘅 Django `6.0.5` 相符：

- [Django 6.0 — QuerySet API reference](https://docs.djangoproject.com/en/6.0/ref/models/querysets/)：`filter()`、`first()`、`select_related()` 嘅行為。
- [Django 6.0 — Making queries](https://docs.djangoproject.com/en/6.0/topics/db/queries/#lookups-that-span-relationships)：以 double underscore 跨 model relationship 查詢，例如 `vocab__is_active=True`。
- [Django 6.0 — How to use sessions](https://docs.djangoproject.com/en/6.0/topics/http/sessions/#using-sessions-in-views)：`request.session` dictionary API、`pop()` 同 session 儲存時機。
- [Django 6.0 — `JsonResponse` objects](https://docs.djangoproject.com/en/6.0/ref/request-response/#jsonresponse-objects)：dict 到 JSON response 嘅轉換及預設 content type。
- [Django 6.0 — The Django template language: Python API](https://docs.djangoproject.com/en/6.0/ref/templates/api/#django.template.loader.render_to_string)：`render_to_string()` 將 template 同 context render 成字串。
- [Django 6.0 — Form handling with class-based views](https://docs.djangoproject.com/en/6.0/topics/class-based-views/generic-editing/)：`FormView.form_valid()` 喺有效 POST 後處理資料並回傳 `HttpResponse`；本 project 喺呢個位置回傳 AJAX `JsonResponse`。

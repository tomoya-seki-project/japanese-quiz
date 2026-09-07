# Coding Reference

呢份文件用嚟整理開發期間遇過嘅問題、核心概念同解決方法，方便之後遇到類似情況時快速查閱。
內容係個人 coding reference，唔代表 project 仲有 bug，亦唔係待辦事項或未完成學習清單。

## 目錄

- [Django Admin 與 User 管理](#GROUP-DJANGO-ADMIN)
  - [DJANGO-CUSTOM-USER-ADMIN — #### `[DJANGO-CUSTOM-USER-ADMIN]` Django Custom User Admin](#DJANGO-CUSTOM-USER-ADMIN)
  - [DJANGO-ADMIN-REVIEW-LIFECYCLE — #### `[DJANGO-ADMIN-REVIEW-LIFECYCLE]` Django Admin approve / reject 完整生命週期與分工](#DJANGO-ADMIN-REVIEW-LIFECYCLE)
  - [DJANGO-ADMIN-FIELD-BUTTON-CUSTOM-URL — #### `[DJANGO-ADMIN-FIELD-BUTTON-CUSTOM-URL]` Admin change form 用 readonly field 顯示 action link 嘅做法](#DJANGO-ADMIN-FIELD-BUTTON-CUSTOM-URL)
  - [DJANGO-ADMIN-RESPONSE-CHANGE-CHANGEFORM-VIEW — #### `[DJANGO-ADMIN-RESPONSE-CHANGE-CHANGEFORM-VIEW]` Admin approve / reject 點樣處理 form save 同 row lock](#DJANGO-ADMIN-RESPONSE-CHANGE-CHANGEFORM-VIEW)
  - [DJANGO-ADMIN-GET-FORM-BASE-FIELDS — #### `[DJANGO-ADMIN-GET-FORM-BASE-FIELDS]` Django Admin `get_form()` 同 `form.base_fields`](#DJANGO-ADMIN-GET-FORM-BASE-FIELDS)
  - [DJANGO-ADMIN-MESSAGE-USER — #### `[DJANGO-ADMIN-MESSAGE-USER]` `ModelAdmin.message_user()` 係咩](#DJANGO-ADMIN-MESSAGE-USER)
  - [DJANGO-ADMIN-M2M-WIDGET — #### `[DJANGO-ADMIN-M2M-WIDGET]` Django Admin 入面 ManyToManyField 點樣改成 checkbox widget](#DJANGO-ADMIN-M2M-WIDGET)
  - [DJANGO-ADMIN-RELATED-OBJECTS-IN-USER-PAGE — #### `[DJANGO-ADMIN-RELATED-OBJECTS-IN-USER-PAGE]` Admin User page 入面顯示 related `UserVocab`](#DJANGO-ADMIN-RELATED-OBJECTS-IN-USER-PAGE)
  - [DJANGO-DATETIME-LOCALTIME-ADMIN-FORMAT — #### `[DJANGO-DATETIME-LOCALTIME-ADMIN-FORMAT]` Django admin datetime localtime 同 format](#DJANGO-DATETIME-LOCALTIME-ADMIN-FORMAT)

- [Django Forms、CBV 與 Request Handling](#GROUP-DJANGO-FORMS-CBV)
  - [DJANGO-HANDWRITTEN-CHECKBOX-POST-FORM — #### `[DJANGO-HANDWRITTEN-CHECKBOX-POST-FORM]` 手寫 checkbox HTML，再用 Django Form 接 POST data](#DJANGO-HANDWRITTEN-CHECKBOX-POST-FORM)
  - [DJANGO-MODEL-MULTIPLE-CHOICE-BULK-SELECT-FLOW — #### `[DJANGO-MODEL-MULTIPLE-CHOICE-BULK-SELECT-FLOW]` 用 `ModelMultipleChoiceField` 做批量選擇 object 嘅處理流程](#DJANGO-MODEL-MULTIPLE-CHOICE-BULK-SELECT-FLOW)
  - [DJANGO-MODEL-MULTIPLE-CHOICE-FIELD-M2M-SET — #### `[DJANGO-MODEL-MULTIPLE-CHOICE-FIELD-M2M-SET]` `ModelMultipleChoiceField`、ManyToManyField 同 `.set()` 嘅關係](#DJANGO-MODEL-MULTIPLE-CHOICE-FIELD-M2M-SET)
  - [DJANGO-SLICED-QUERYSET-MULTIPLE-CHOICE — #### `[DJANGO-SLICED-QUERYSET-MULTIPLE-CHOICE]` Sliced QuerySet 點解唔可以直接交俾 `ModelMultipleChoiceField`](#DJANGO-SLICED-QUERYSET-MULTIPLE-CHOICE)
  - [DJANGO-CBV-OBJECT-ID — #### `[DJANGO-CBV-OBJECT-ID]` Detail／Update／Delete View 點樣取得目標 Object](#DJANGO-CBV-OBJECT-ID)
  - [DJANGO-DETAILVIEW-WITH-MINI-FORM — #### `[DJANGO-DETAILVIEW-WITH-MINI-FORM]` DetailView 入面放一張小型 Form](#DJANGO-DETAILVIEW-WITH-MINI-FORM)
  - [DJANGO-AJAX-FORMVIEW-INVALID-JSON — #### `[DJANGO-AJAX-FORMVIEW-INVALID-JSON]` AJAX FormView 驗證失敗時點解要回傳 JSON](#DJANGO-AJAX-FORMVIEW-INVALID-JSON)

- [Django ORM、Database 與 Model Relations](#GROUP-DJANGO-ORM-DATABASE)
  - [DJANGO-QUERYSET-SUBSET-ORDERING — #### `[DJANGO-QUERYSET-SUBSET-ORDERING]` 分開 QuerySet 後 `order_by()` 只會喺各自 subset 入面排序](#DJANGO-QUERYSET-SUBSET-ORDERING)
  - [DJANGO-QUERYSET-EXCLUDE-RECENT-IDS — #### `[DJANGO-QUERYSET-EXCLUDE-RECENT-IDS]` 由原本 queryset 排除最近問過嘅 vocab](#DJANGO-QUERYSET-EXCLUDE-RECENT-IDS)
  - [DJANGO-QUERYSET-VALUES-LIST-PERFORMANCE — #### `[DJANGO-QUERYSET-VALUES-LIST-PERFORMANCE]` QuerySet `values_list()` 同避免重複 SQL](#DJANGO-QUERYSET-VALUES-LIST-PERFORMANCE)
  - [DJANGO-RELATION-FIELD-RELATED-NAME — #### `[DJANGO-RELATION-FIELD-RELATED-NAME]` Relation 應該用 field name 定 `related_name`](#DJANGO-RELATION-FIELD-RELATED-NAME)
  - [DJANGO-UNIQUE-CONSTRAINT — #### `[DJANGO-UNIQUE-CONSTRAINT]` `UniqueConstraint` 同 conditional unique constraint](#DJANGO-UNIQUE-CONSTRAINT)
  - [DJANGO-CATCH-INTEGRITY-ERROR-AROUND-ATOMIC — #### `[DJANGO-CATCH-INTEGRITY-ERROR-AROUND-ATOMIC]` 點解要喺 `transaction.atomic()` 外面捕捉 `IntegrityError`](#DJANGO-CATCH-INTEGRITY-ERROR-AROUND-ATOMIC)
  - [DJANGO-PRIMARY-SYNC-EVENT-TRANSACTION-BOUNDARY — #### `[DJANGO-PRIMARY-SYNC-EVENT-TRANSACTION-BOUNDARY]` 主操作、vocab sync 同 event 應該點分 transaction](#DJANGO-PRIMARY-SYNC-EVENT-TRANSACTION-BOUNDARY)
  - [DJANGO-POST-SAVE-SIGNAL-CREATED-GET-OR-CREATE — #### `[DJANGO-POST-SAVE-SIGNAL-CREATED-GET-OR-CREATE]` `post_save` signal、`created` 同 `get_or_create()`](#DJANGO-POST-SAVE-SIGNAL-CREATED-GET-OR-CREATE)

- [Ajax、JavaScript 與 Partial UI](#GROUP-AJAX-JAVASCRIPT-PARTIAL-UI)
  - [JS-PARTIAL-REPLACE-EVENT-BINDING — #### `[JS-PARTIAL-REPLACE-EVENT-BINDING]` Ajax partial replace 後 event listener 點樣處理](#JS-PARTIAL-REPLACE-EVENT-BINDING)
  - [HTML-JS-CHECKBOX-SELECT-ALL — #### `[HTML-JS-CHECKBOX-SELECT-ALL]` Checkbox 全選 / 全取消點樣用 JavaScript 做](#HTML-JS-CHECKBOX-SELECT-ALL)
  - [AJAX-GET-LINK-VS-POST-FORM — #### `[AJAX-GET-LINK-VS-POST-FORM]` Ajax 入面 GET link 同 POST form 嘅分工](#AJAX-GET-LINK-VS-POST-FORM)
  - [AJAX-EVENT-TRIGGER-FETCH — #### `[AJAX-EVENT-TRIGGER-FETCH]` Ajax 唔一定要由 button submit 觸發](#AJAX-EVENT-TRIGGER-FETCH)
  - [DJANGO-AJAX-PARTIAL-ACTION-ENDPOINT — #### `[DJANGO-AJAX-PARTIAL-ACTION-ENDPOINT]` Ajax partial flow 入面，View 係 action endpoint，Partial 係 UI state](#DJANGO-AJAX-PARTIAL-ACTION-ENDPOINT)
  - [DJANGO-PAGINATION-KEEP-SEARCH-QUERY — #### `[DJANGO-PAGINATION-KEEP-SEARCH-QUERY]` Search form + pagination + Ajax partial update 點樣保留 GET filter](#DJANGO-PAGINATION-KEEP-SEARCH-QUERY)

- [Python、CSV 與 Configuration](#GROUP-PYTHON-DATA-CONFIG)
  - [PYTHON-SET-DIFFERENCE-CSV-HEADERS — #### `[PYTHON-SET-DIFFERENCE-CSV-HEADERS]` 點樣用 set 差集檢查 CSV 缺少嘅 headers](#PYTHON-SET-DIFFERENCE-CSV-HEADERS)
  - [PYTHON-ENUMERATE-CSV-ROWS — #### `[PYTHON-ENUMERATE-CSV-ROWS]` `enumerate()` 點樣提供 CSV 行數同資料](#PYTHON-ENUMERATE-CSV-ROWS)
  - [PYTHON-JSON-CONFIG-MAP-LOOKUP — #### `[PYTHON-JSON-CONFIG-MAP-LOOKUP]` 用 JSON config map 查 subtype / 設定值](#PYTHON-JSON-CONFIG-MAP-LOOKUP)
  - [PYTHON-LOGGING-FILTER — #### `[PYTHON-LOGGING-FILTER]` Logging filter 除左篩選 level 仲可以做什麼](#PYTHON-LOGGING-FILTER)
  - [PYTHON-EXCEPTION-RAISE-AND-LOGGER-EXCEPTION — #### `[PYTHON-EXCEPTION-RAISE-AND-LOGGER-EXCEPTION]` Exception、`raise`、`from e` 同 `logger.exception()`](#PYTHON-EXCEPTION-RAISE-AND-LOGGER-EXCEPTION)
  - [PYTHON-DATACLASS-2D-LIST-DP-STATE — #### `[PYTHON-DATACLASS-2D-LIST-DP-STATE]` 用 `dataclass` 同 2D list 保存 DP state](#PYTHON-DATACLASS-2D-LIST-DP-STATE)

- [Project Architecture 與 Domain Design](#GROUP-PROJECT-ARCHITECTURE-DOMAIN)
  - [DOMAIN-VOCAB-USERVOCAB-IN-USE — #### `[DOMAIN-VOCAB-USERVOCAB-IN-USE]` `Vocab` 同 `UserVocab.in_use` 嘅設計心智模型](#DOMAIN-VOCAB-USERVOCAB-IN-USE)
  - [DJANGO-CONTEXT-PROCESSOR-NAVBAR-DATA — #### `[DJANGO-CONTEXT-PROCESSOR-NAVBAR-DATA]` 全站 navbar data 應該用 context processor](#DJANGO-CONTEXT-PROCESSOR-NAVBAR-DATA)

<a id="GROUP-DJANGO-ADMIN"></a>

## Django Admin 與 User 管理

<a id="DJANGO-CUSTOM-USER-ADMIN"></a>

### `[DJANGO-CUSTOM-USER-ADMIN]` Django Custom User Admin

#### 問題背景

Django User 的 `password` 欄位唔可以當普通文字欄位直接儲存。真正存入 database 的內容應該係經過 `set_password()` 產生的 password hash。

Custom User Admin 需要分開處理兩個流程：

1. 新增 User
2. 修改現有 User

#### 研究方向

- `UserAdmin.form` 同 `UserAdmin.add_form` 分別喺邊個頁面使用。
- `fieldsets` 同 `add_fieldsets` 點樣控制 change/add 頁顯示的欄位。
- 點解 `ReadOnlyPasswordHashField` 只適合 change form。
- Django 原生 `UserCreationForm` 同自訂 `ModelForm` 的差異。
- Django Admin 正式修改密碼的 password change flow 點樣運作。

#### 概念整理與解答

##### 修改現有 User

目前使用：

```python
form = UserChangeAdminForm
```

而 `UserChangeAdminForm` 使用：

```python
password = ReadOnlyPasswordHashField(...)
```

目的：

- 唔俾 admin 將現有 password hash 當普通文字直接修改。
- `clean_password()` 返回原本的 password hash，避免儲存表單時破壞密碼。

呢部分目前理解為已經正確。

##### 新增 User

目前使用：

```python
add_form = RegistForm
```

`RegistForm` 的密碼欄位名稱係：

```python
password
password2
```

`CustomizedUserAdmin.add_fieldsets` 目前亦已配合使用：

```python
password
password2
```

`add_fieldsets` 列出的欄位名稱必須同 `add_form` 真正提供的欄位名稱一致，否則 Django Admin 的 Add User 頁可能會出現 unknown field error。目前兩邊欄位名稱已經一致。

##### 目前採用的做法

- 繼續使用 `RegistForm`
  - `add_fieldsets` 配合使用 `password`、`password2`。
  - `RegistForm.save()` 已呼叫 `set_password()`。

另一個可研究的做法係建立專用的 `UserCreationAdminForm`：

  - 使用慣常的 `password1`、`password2` 命名。
  - 在 `save()` 內呼叫 `set_password(password1)`。
  - 將 `add_form` 改成這個專用表單。

#### 理解內容

-

<a id="DJANGO-ADMIN-REVIEW-LIFECYCLE"></a>

### `[DJANGO-ADMIN-REVIEW-LIFECYCLE]` Django Admin approve / reject 完整生命週期與分工

#### 核心概念

Custom submit button、`get_queryset()`、`get_form()`、`save_model()`、`response_change()` 同 service 唔係六個互相獨立嘅做法，而係同一個 POST request 入面唔同階段嘅 hook。

以 `VocabRequestAdmin` 為例，完整主線係：

```text
change_form.html submit button
    → Django Admin 收到 POST
    → get_queryset() 取得目標 object
    → get_readonly_fields() / get_form() 組成 ModelForm
    → form.is_valid()
    → save_model() / save_related()
    → response_change()
    → VocabRequestService approve / reject
    → message_user() + redirect
```

如果 form 驗證失敗，例如按 Reject 但 `review_note` 空白，流程會喺 `form.is_valid()` 停止，唔會進入 `save_model()`、`response_change()` 或 service。

#### 各部分責任

| 部分 | 負責 | 唔應該負責 |
|---|---|---|
| `change_form.html` | 顯示按鈕；透過 `_approve` / `_reject` 表達 admin 意圖 | 直接改 database、做權限或業務驗證 |
| `get_queryset()` | Django Admin 取得 object 嘅查詢方式；review POST 時提早 `select_for_update()` | 決定 approve 定 reject |
| `get_readonly_fields()` | 根據 object 狀態限制普通 model fields | 執行審批 |
| `get_form()` | 建立／調整本次 ModelForm class；Reject 時令 `review_note` required；處理 form field 狀態 | 寫入審批結果 |
| ModelForm validation | 將 POST 轉成可信嘅 `cleaned_data`，擋住缺少 required field 等輸入錯誤 | 執行 domain transaction |
| `save_model()` | 保存已通過驗證嘅普通 model fields；阻止 reviewed request 再被保存 | 代替 approve / reject service |
| `response_change()` | 保存後辨認按鈕、檢查 admin permission、呼叫 service、顯示 message、redirect | 承擔最終 data consistency |
| `VocabRequestService` | transaction、row lock、重新檢查 pending、執行 vocab 變更、更新審批狀態、建立通知 | 處理 admin HTML 或 redirect |

#### Custom button 點樣將意圖放入 POST

```django
<button type="submit" name="_approve" value="1">Approve</button>
<button type="submit" name="_reject" value="1">Reject</button>
```

Browser 只會提交被按嗰個 submit button 嘅 name/value。因此：

- 按 Approve：`request.POST` 有 `_approve`。
- 按 Reject：`request.POST` 有 `_reject`。

按鈕本身唔會 call Python method；Django Admin 收到同一條 change-form POST 後，各 hook 再讀 `request.POST` 判斷意圖。

#### Reject 點解可以動態要求 `review_note`

```python
def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)

    if "_reject" in request.POST and "review_note" in form.base_fields:
        form.base_fields["review_note"].required = True
        form.base_fields["review_note"].error_messages["required"] = (
            "A review note is required when rejecting a request."
        )

    return form
```

Model field 可以保持 `blank=True`，因為「資料庫層面容許空白」同「某個 action 要求必填」係兩件事。Approve 可以唔填 note；只有今次 POST 包含 `_reject` 時，admin form field 先變成 required。

重要次序：`get_form()` 唔係負責驗證輸入；佢係設定規則。之後 form instance 執行 `is_valid()`，先真正檢查 `review_note`。

#### `save_model()` 同 `response_change()` 點解兩個都要有

當 form valid，Django Admin 會先保存 form，再問 `response_change()` 應該回傳邊個 response。呢個 project 亦利用後者辨認自訂按鈕：

```python
def response_change(self, request, obj):
    if "_approve" in request.POST:
        return handle_approve(...)
    if "_reject" in request.POST:
        return handle_reject(...)
    return super().response_change(request, obj)
```

因此兩者分工係：

- `save_model()`：保存 admin form 資料，例如 `review_note`。
- `response_change()`：保存完成後，開始 approve / reject action，然後決定 message 同 redirect。

如果 override `save_model()` 而正常分支冇 call `super().save_model(...)`，form 表面驗證成功都唔會真正保存。

#### 點解 service 仲要重新 lock 同 check status

Admin layer 嘅 early lock 保護今次 admin POST；service 仍然要自己做：

```python
with transaction.atomic():
    locked_request = (
        VocabRequest.objects
        .select_for_update()
        .get(pk=vocab_request.pk)
    )

    if locked_request.status != VocabRequestStatus.PENDING:
        return False
```

原因係 service 可能日後由 admin 以外嘅 API、command 或 test 呼叫。最終業務規則應由 service 自己保證，而唔係假設 caller 一定鎖好資料。

`select_for_update()` 只係令同時處理同一 row 嘅 transaction 排隊；真正防止重複審批嘅判斷仍然係重新讀取後檢查 `status == PENDING`。

#### Approve 同 Reject 嘅差異

共同部分：

- 都要有 change permission。
- 都用 transaction + row lock。
- 都重新檢查 request 仍然 pending。
- 都保存 `reviewed_by`，並用 `review_note` 建立結果通知。

不同部分：

- Approve 會按 request type 執行 create / update / restore / deactivate vocab，亦可能產生 domain `ValidationError`。
- Reject 唔改 vocab，只將 request 轉為 rejected；但 admin form 要求 `review_note` 必填。

#### 三條要記住嘅失敗路線

1. Reject note 空白：form invalid，留喺 change page；未保存、未 call service。
2. 冇 change permission：`response_change()` 唔 call service，顯示錯誤並 redirect。
3. 第二個 reviewer 處理同一 request：service lock 後見到已非 pending，回傳 `False`；唔重複改 vocab。

#### Project 圖解

詳細圖解同逐步例子：[`vocab_request_admin_review_flow.html`](../modification/example/vocab_request_admin_review_flow.html)。

#### 理解內容

-

<a id="DJANGO-ADMIN-FIELD-BUTTON-CUSTOM-URL"></a>

### `[DJANGO-ADMIN-FIELD-BUTTON-CUSTOM-URL]` Admin change form 用 readonly field 顯示 action link 嘅做法

#### 問題背景

之前曾經試過喺 `VocabRequestAdmin` 入面用一個 readonly field / display method 顯示 approve / reject button link。

大概做法係：

- 定義 `review_buttons()`。
- 用 `@admin.display(description="Review")` 將佢包裝成 admin 顯示欄位。
- 喺 `readonly_fields` / `fields` 入面加入 `review_buttons`。
- 用 `format_html()` 回傳 approve / reject `<a>` link。
- override `get_urls()` 加入 admin custom URLs。
- custom URL 進入 `approve_view()` / `reject_view()`，再 call service。

#### 研究方向

- `@admin.display` 點樣令 method 變成 admin 欄位。
- `readonly_fields` 入面除咗 model field，點解亦可以放 admin method name。
- `format_html()` 點解比直接拼 HTML string 安全。
- `ModelAdmin.get_urls()` 點樣加 custom admin URL。
- `self.admin_site.admin_view()` 點樣套用 admin permission / staff check / CSRF 等 admin protection。
- 點解用 `<a href="...">` 做 approve / reject 會有 GET side effect 問題。
- 點解之後改用 change form submit button + POST flow。

#### 概念整理與解答

##### 1. 用 admin method 當 readonly field

Django Admin 嘅 `readonly_fields` 除咗可以放 model field name，亦可以放 `ModelAdmin` method name。

例如：

```python
@admin.display(description="Review")
def review_buttons(self, obj):
    ...
```

然後：

```python
readonly_fields = (
    "review_buttons",
)

fields = (
    ...,
    "review_buttons",
)
```

Admin change form 就會喺指定位置顯示呢個 method 回傳嘅內容。

##### 2. 用 `format_html()` 產生 admin button link

原本概念大概係：

```python
@admin.display(description="Review")
def review_buttons(self, obj):
    if not obj.pk:
        return "---"

    if obj.status != VocabRequestStatus.PENDING:
        return "Already Reviewed"

    approve_url = reverse(
        "admin:vocabrequest_approve",
        args=[obj.pk],
    )

    reject_url = reverse(
        "admin:vocabrequest_reject",
        args=[obj.pk],
    )

    return format_html(
        '<a class="button" href="{}">Approve</a>&nbsp;'
        '<a class="button" href="{}">Reject</a>',
        approve_url,
        reject_url,
    )
```

`format_html()` 會 escape 傳入嘅 arguments，避免直接拼 HTML 時出現 XSS 風險。
如果需要喺 Django Admin 顯示少量 HTML，通常應該用 `format_html()`，而唔係普通 f-string。

##### 3. 用 `get_urls()` 加 admin custom URL

`ModelAdmin.get_urls()` 可以為某個 model admin 加入額外 URL。

概念：

```python
def get_urls(self):
    urls = super().get_urls()

    custom_urls = [
        path(
            "<int:object_id>/approve/",
            self.admin_site.admin_view(self.approve_view),
            name="vocabrequest_approve",
        ),
        path(
            "<int:object_id>/reject/",
            self.admin_site.admin_view(self.reject_view),
            name="vocabrequest_reject",
        ),
    ]

    return custom_urls + urls
```

`self.admin_site.admin_view(...)` 會將 view 包成 admin view，加入 admin site 相關保護，例如 staff check、permission-related behavior、CSRF/cache handling 等。

##### 4. Custom approve / reject view

原本 view 概念係：

```python
@method_decorator(require_POST)
def approve_view(self, request, object_id):
    vocab_request = get_object_or_404(
        VocabRequest,
        pk=object_id,
    )

    VocabRequestService.approve_vocab_request(
        vocab_request=vocab_request,
        reviewed_by=request.user,
    )

    self.message_user(
        request,
        f"Vocab request approved by : {request.user}",
        messages.SUCCESS,
    )

    return redirect(
        reverse("admin:dictionary_vocabrequest_changelist")
    )
```

Reject view 同 approve view 類似，只係 call `reject_vocab_request()`。

##### 5. 呢個做法有咩問題

如果 `review_buttons()` 回傳嘅係：

```html
<a href="/admin/.../approve/">Approve</a>
```

咁 click link 本質上係 GET request。
但 approve / reject 係會改 database state 嘅 action，唔應該用 GET 做。

原因：

- GET 應該係 safe / read-only。
- Browser prefetch、crawler、refresh、copy link 等情況可能誤觸。
- 用 GET 做 state change 容易造成 CSRF / accidental action 風險。

後來加 `@require_POST` 可以令 custom view 只接受 POST，但如果前端仍然係普通 `<a href>`，click 後就唔會正常工作，因為 link 發出嘅係 GET。

要用 custom URL approach，button 應該改成 `<form method="post">`，並加入 CSRF token。

##### 6. 點解最後改用 change form submit button

目前 project 最後改成喺 custom admin `change_form.html` 入面放 submit buttons：

```django
<button type="submit" name="_approve" value="1" class="default">Approve</button>
<button type="submit" name="_reject" value="1" class="default">Reject</button>
```

然後喺 `response_change()` 入面判斷：

```python
if "_approve" in request.POST:
    ...

if "_reject" in request.POST:
    ...
```

呢個做法嘅好處：

- 使用原本 admin change form POST。
- 唔需要額外維護 approve / reject custom URL。
- 可以同 admin form validation / save flow 接軌。
- 較容易配合 `get_queryset()` conditional `select_for_update()`、`get_readonly_fields()`、`save_model()` 等 admin lifecycle hook。

##### 7. 兩種做法點樣選

Readonly field + custom URL approach 適合：

- action 真係想做成獨立 endpoint。
- 想將 action 同 admin change form save flow 分開。
- 願意自己處理 POST form、CSRF、permission、transaction、redirect。

Change form submit button approach 適合：

- action 本身係 review / approve 呢類 change form workflow。
- 想保留 admin 原生 form validation / save / message / redirect flow。
- 想喺同一頁 review proposed data 後直接 approve / reject。

今次 project 最後選擇 change form submit button，因為 approve / reject 係 `VocabRequest` review workflow，跟 change form 關係較密切。

#### 理解內容

-

<a id="DJANGO-ADMIN-RESPONSE-CHANGE-CHANGEFORM-VIEW"></a>

### `[DJANGO-ADMIN-RESPONSE-CHANGE-CHANGEFORM-VIEW]` Admin approve / reject 點樣處理 form save 同 row lock

#### 問題背景

`VocabRequestAdmin` 目前喺 admin change form 入面用 custom buttons 做 approve / reject，並喺 `response_change()` 入面判斷：

```python
if "_approve" in request.POST:
    ...
if "_reject" in request.POST:
    ...
```

但 `response_change()` 係 Django Admin 保存 change form 之後先呼叫嘅 hook。即係如果 admin 同一次 POST 又修改 proposed data、又撳 approve，Django Admin 可能已經先保存咗 form data，然後先進入 approve service。

目前 service 入面雖然使用 `transaction.atomic()` 同 `select_for_update()`，但個 row lock 主要保護 approve / reject 階段，未必保護到 admin form save proposed data 嗰一下。

#### 研究方向

- `ModelAdmin.response_change()` 喺 Django Admin save lifecycle 入面幾時被呼叫。
- 點樣偵測 admin 撳 approve / reject 時，form 有冇 unsaved changes。
- 點解簡單解法可以先要求 admin save changes，再 approve / reject。
- 如果要真正將「form validation + save + approve / reject」放入同一個 transaction / row lock，點樣 override `changeform_view()`。
- `select_for_update()` 必須放喺 `transaction.atomic()` 裡面先有意義。

#### 概念整理與解答

##### 1. 簡單解法：approve / reject 前擋住 unsaved changes

短期比較易理解嘅做法係將 review 分成兩步：

1. Admin 先修改 proposed data，撳普通 Save。
2. Save 完確認資料正確，再撳 Approve / Reject。

為咗避免純靠 admin 自覺，可以喺 approve / reject branch 入面檢查 submitted form 有冇改動。如果有改動，就停止 approve / reject，提示 admin 先 Save。

概念：

```python
def response_change(self, request, obj):
    if "_approve" in request.POST or "_reject" in request.POST:
        form_class = self.get_form(request, obj)
        form = form_class(request.POST, request.FILES, instance=obj)

        if form.is_valid() and form.has_changed():
            self.message_user(
                request,
                "Please save changes before approve/reject.",
                messages.ERROR,
            )
            return redirect(
                reverse(
                    "admin:dictionary_vocabrequest_change",
                    args=[obj.pk],
                )
            )

    ...
```

重點：

- 如果 admin 無改資料，只係撳 approve / reject，就照常執行 service。
- 如果 admin 改咗資料又直接 approve / reject，就擋住佢，叫佢先 Save。
- 呢個做法唔係完整 concurrency lock，但可以避免「同一次 POST 同時改資料同 approve」呢種容易混亂嘅情況。

##### 2. 呢個簡單解法未解決咩

簡單解法只係流程保護，唔係真正 database-level solution。

例如兩個 admin 同時打開同一個 request：

1. Admin A save proposed data。
2. Admin B 用舊畫面 save proposed data。
3. 後 save 嗰個可能覆蓋前一個。

如果要完整處理呢類 concurrency，就要喺更早位置控制 transaction boundary。

##### 3. 長遠解法：override `changeform_view()`

`changeform_view()` 係 Django Admin 處理 add / change form request 嘅更外層 hook。相比 `response_change()`，佢包住更完整嘅 admin form lifecycle。

長遠可以研究喺 `changeform_view()` 入面偵測 `_approve` / `_reject`，然後：

1. 進入 `transaction.atomic()`。
2. 用 `select_for_update()` 鎖住目標 `VocabRequest` row。
3. 讓 admin form validation / save 使用被鎖住嘅 object。
4. save proposed data。
5. 執行 approve / reject service。
6. commit transaction。

概念方向：

```python
from django.db import transaction

def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
    is_review_action = (
        request.method == "POST"
        and object_id is not None
        and ("_approve" in request.POST or "_reject" in request.POST)
    )

    if not is_review_action:
        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context,
        )

    with transaction.atomic():
        locked_obj = (
            VocabRequest.objects
            .select_for_update()
            .get(pk=object_id)
        )

        # 之後要研究點樣令 Django Admin 使用 locked_obj
        # 去完成原本嘅 form validation / save flow，
        # 再喺同一個 transaction 內 approve / reject。

        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context,
        )
```

上面只係概念骨架，唔係可以直接完成所有問題嘅最終 code。真正實作時要研究 Django Admin 內部點樣取得 object、建立 form、save model、save related objects，否則可能只係鎖咗 row，但 admin 仍然用自己重新查出嚟嘅 object。

##### 4. 點解呢個比 `response_change()` 更適合長遠解法

`response_change()` 適合做「save 完之後 redirect 去邊、顯示咩 message、額外做咩 action」。

但如果目標係控制：

- form validation
- object save
- approve / reject action
- row lock
- transaction boundary

就需要喺更外層嘅 lifecycle 介入，所以 `changeform_view()` 會係更值得研究嘅 hook。

##### 5. 目前建議

短期：

- 先喺 `response_change()` approve / reject branch 偵測 `form.has_changed()`。
- 如果 admin 有 unsaved changes，就要求先 Save。
- 保留目前 service 入面嘅 `transaction.atomic()` + `select_for_update()` 保護 approve / reject 階段。

長期：

- 研究 `changeform_view()` 同 Django Admin save lifecycle。
- 再考慮將 form save + approve / reject 放入同一個 locked transaction。

##### 6. 今次 project 實際採用嘅處理手法

今次最後採用嘅做法唔係 override `changeform_view()`，而係用較簡單、較貼近現有 admin flow 嘅方式處理。

核心思路：

- 喺 admin approve / reject POST 時，盡早鎖住 `VocabRequest` row。
- Service 入面仍然保留自己嘅 status check 同 row lock。
- Request 一旦 reviewed，就唔再俾 admin 改 proposed data。

###### 6.1 Admin POST 時 early lock

喺 `VocabRequestAdmin.get_queryset()` 入面，只喺 approve / reject POST 時加 `select_for_update()`：

```python
def get_queryset(self, request):
    qs = super().get_queryset(request)

    if (
        request.method == "POST"
        and ("_approve" in request.POST or "_reject" in request.POST)
    ):
        qs = qs.select_for_update()

    return qs
```

呢個做法嘅目的係：當 Django Admin 處理 approve / reject submit 時，取得 object 嗰刻已經鎖住 row，令 admin change form save proposed data 前先有 row lock。

唔應該無條件喺所有 `get_queryset()` 都加 `select_for_update()`，因為 admin list page、GET change page 都會用 `get_queryset()`；如果唔喺 transaction 入面使用 `select_for_update()`，某啲 database / Django 設定下可能會出錯。

###### 6.2 Service 仍然保留 self-lock

雖然 admin 已經 early lock，但 `VocabRequestService.approve_vocab_request()` / `reject_vocab_request()` 仍然保留：

```python
locked_request = (
    VocabRequest.objects
    .select_for_update()
    .get(pk=vocab_request.pk)
)
```

原因：

- Admin layer 只係其中一個 caller。
- 日後可能有 management command、API、tests 或其他 view 直接 call service。
- Service 自己保留 lock，可以作為 domain logic 最後防線。
- 同一個 transaction 入面再次 lock 同一 row 通常唔係問題，反而令 service contract 更安全。

###### 6.3 Reviewed request 變 readonly

如果 request 已經唔係 `PENDING`，admin change form 會將欄位變 readonly：

```python
def get_readonly_fields(self, request, obj=None):
    readonly_fields = list(super().get_readonly_fields(request, obj))

    if obj is not None and obj.status != VocabRequestStatus.PENDING:
        return [field.name for field in self.model._meta.fields]

    return readonly_fields
```

目的：

- Approved / rejected request 可以入去睇。
- 但唔應該再修改 proposed data、status、reviewer 等 review record。
- 減少舊頁面 submit 覆蓋 reviewed record 嘅風險。

###### 6.4 `save_model()` 做最後防線

Readonly 主要係 admin form / UI 層防護。為咗更保險，`save_model()` 再擋住非 pending request 被保存：

```python
def save_model(self, request, obj, form, change):
    if change and obj.status != VocabRequestStatus.PENDING:
        self.message_user(
            request,
            "Reviewed request cannot be changed",
            messages.ERROR,
        )
        return

    super().save_model(request, obj, form, change)
```

重點係：如果 override `save_model()`，最後一定要喺允許保存嘅情況 call：

```python
super().save_model(request, obj, form, change)
```

否則 pending request 都會變成無法保存。

###### 6.5 呢個做法解決咗咩

今次做法主要處理：

- Admin approve / reject POST 時，form save 前盡早 lock row。
- Service approve / reject 階段仍然有 transaction + row lock + pending status check。
- Reviewed request 唔再俾 admin 修改，避免舊頁面或第二個 admin 覆蓋已 review record。

###### 6.6 仲有咩要之後驗證

呢個做法比純粹喺 `response_change()` 做 service call 穩陣好多，但之後仍然值得用 tests 驗證：

- 兩個 admin 同時打開同一個 pending request。
- Admin A approve 後，Admin B 用舊頁面 submit。
- Admin A / B 幾乎同時 approve。
- Reviewed request 是否確實無法再 save proposed data。

如果之後發現 admin lifecycle 仍然有更深層嘅 race condition，再研究 override `changeform_view()` 或獨立 custom admin view。

#### 理解內容

-

<a id="DJANGO-ADMIN-GET-FORM-BASE-FIELDS"></a>

### `[DJANGO-ADMIN-GET-FORM-BASE-FIELDS]` Django Admin `get_form()` 同 `form.base_fields`

#### 問題背景

`VocabRequestAdmin` 入面，reviewed request 應該只可以查看，唔應該再修改 proposed data。

普通 model field 可以用 `get_readonly_fields()` 變 readonly，但 `proposed_categories` 係 `ManyToManyField`，admin form 入面通常係以 form field / widget 方式處理，未必會完全受 `readonly_fields` 控制。

所以如果想 reviewed request 入面連 M2M checkbox 都唔可以改，可以喺 `get_form()` 入面將該 form field disable。

#### 研究方向

- `ModelAdmin.get_form()` 喺 admin lifecycle 入面幾時被 call。
- `form.base_fields` 同平時 template 入面見到嘅 `form.fields` 有咩關係。
- `disabled=True` 對 Django form validation / cleaned data 有咩影響。
- 點解 `ManyToManyField` 有時要喺 form 層另外處理 readonly / disabled。

#### Codex 解答

##### 1. `get_form()` 係咩

`get_form()` 係 `ModelAdmin` 提供嘅 hook，用嚟決定 admin change page / add page 要用邊一個 form class。

簡化理解：

```python
def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    return form
```

`super().get_form(...)` 會根據目前 `ModelAdmin` 設定，例如 `fields`、`readonly_fields`、`exclude`、model fields 同 custom widgets，動態生成一個 admin form class。

呢度 return 嘅 `form` 通常係一個 form class，唔係某一張已經 bind data 嘅 form instance。

##### 2. `base_fields` 係咩

`form.base_fields` 可以理解成「呢個 form class 預設有邊啲 fields」。

例如：

```python
form.base_fields["proposed_categories"]
```

就係攞到 admin form 入面 `proposed_categories` 對應嘅 form field object。

你可以喺呢個階段改佢嘅設定：

```python
form.base_fields["proposed_categories"].disabled = True
```

意思係：之後 Django Admin 建立呢張 form 時，`proposed_categories` 呢個欄位會係 disabled。

##### 3. 點解要檢查 field 是否存在

安全寫法通常會咁：

```python
if "proposed_categories" in form.base_fields:
    form.base_fields["proposed_categories"].disabled = True
```

因為 admin form 可能因為 `fields`、`readonly_fields`、permission 或其他設定，令某個 field 唔存在於 `base_fields`。

直接寫 `form.base_fields["proposed_categories"]`，如果 field 唔存在，就會 `KeyError`。

##### 4. 今次用法

```python
def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)

    if obj is not None and obj.status != VocabRequestStatus.PENDING:
        if "proposed_categories" in form.base_fields:
            form.base_fields["proposed_categories"].disabled = True

    return form
```

意思係：

- 新增頁 / 無 object：唔處理。
- Request 仍然 pending：admin 可以 review / 修改 proposed categories。
- Request 已經 approved / rejected：`proposed_categories` checkbox disabled。

##### 5. 打字位要小心

正確屬性係：

```python
disabled
```

唔係：

```python
diabled
```

如果寫錯成 `diabled = True`，Python 未必會報錯，因為佢可能只係喺 object 上加咗一個新 attribute。

結果係畫面唔會 disable，但 system check / syntax check 都未必會發現，所以呢類 typo 要靠實際 UI 測試或細心 review。

##### 6. 同 `save_model()` 嘅分工

`get_form()` + `disabled=True` 主要係 UI / form 層：

- 令 admin 頁面唔容易改到 reviewed request。
- 令使用者操作上更清楚。

`save_model()` 係後端防線：

- 即使有人 submit 舊頁面或繞過 UI，都唔應該保存 reviewed request。

所以兩者唔係互相取代，而係一前一後配合。

#### 理解內容

-

<a id="DJANGO-ADMIN-MESSAGE-USER"></a>

### `[DJANGO-ADMIN-MESSAGE-USER]` `ModelAdmin.message_user()` 係咩

#### 問題背景

目前喺 `dictionary/admin.py` approve / reject flow 使用：

```python
self.message_user(
    request,
    "Message content",
    messages.SUCCESS,
)
```

但仲未理解 `self.message_user()` 係邊個 class 提供、訊息儲存喺邊、點樣顯示，同 Django messages framework 有咩關係。

#### 研究方向

- `self` 點解係 `VocabRequestAdmin` instance，而唔係 Django view。
- `ModelAdmin.message_user()` 同 `django.contrib.messages` 嘅關係。
- `request` 參數點解必須傳入。
- `messages.SUCCESS`、`WARNING`、`ERROR` 等 level 有咩作用。
- 訊息係暫存在 session、cookie，定係 database。
- 點解 redirect 去另一個 admin page 後，訊息仍然可以顯示一次。
- `message_user()` 同直接使用 `messages.success(request, ...)` 有咩分別。

#### 概念整理與解答

##### 1. `self.message_user()` 係邊度嚟

`VocabRequestAdmin` 繼承自：

```python
admin.ModelAdmin
```

所以 admin class method 入面嘅 `self`，係目前 `VocabRequestAdmin` object。`message_user()` 係 `ModelAdmin` 提供嘅 method：

```python
self.message_user(
    request,
    "Vocab request approved.",
    messages.SUCCESS,
)
```

佢用嚟將一個短暫訊息加入目前 request，等下一個 Django Admin page 顯示。

##### 2. 點解一定要傳入 `request`

訊息係屬於目前進行操作嘅 user/request，而唔係屬於 `VocabRequest` model。

`request` 可以令 Django messages framework 知道：

- 邊一個 user/browser 應該收到訊息。
- 應該將訊息暫存喺邊個 session 或 cookie。
- Redirect 後下一個頁面應該顯示邊啲訊息。

##### 3. Message level 有咩作用

第三個參數係訊息級別：

```python
messages.DEBUG
messages.INFO
messages.SUCCESS
messages.WARNING
messages.ERROR
```

例如：

```python
self.message_user(request, "Approved.", messages.SUCCESS)
self.message_user(request, "Already reviewed.", messages.WARNING)
self.message_user(request, "Invalid data.", messages.ERROR)
```

Level 主要用嚟表達訊息語意，同俾 template/admin CSS 顯示唔同樣式。

##### 4. 點解 redirect 後仲見到訊息

一般 HTTP response redirect 之後，原本 response body 唔會繼續存在。Django messages framework 會先將訊息暫存，再由下一個 request 取出。

大概流程：

```text
Admin 按 Approve
-> message_user() 加入 SUCCESS message
-> redirect 去 VocabRequest list
-> browser 發出新 GET request
-> Django Admin template 讀取 messages
-> 顯示訊息一次
```

訊息顯示及讀取後通常會被清除，所以 refresh 下一次未必再見到。

實際儲存位置取決於 Django `MESSAGE_STORAGE` 設定，可以使用 session、cookie，或者 fallback storage；唔會預設永久寫入 project database 做歷史紀錄。

因此 `message_user()` 適合即時 UI feedback，唔適合代替 event、notification 或 audit log model。

##### 5. 同 `messages.success()` 有咩分別

以下兩種寫法目的相近：

```python
self.message_user(request, "Approved.", messages.SUCCESS)
```

```python
messages.success(request, "Approved.")
```

`message_user()` 係 `ModelAdmin` 提供嘅方便接口，適合 admin class 內使用；`messages.success()` 係通用 messages framework API，可以喺一般 Django view 使用。

##### 6. `"; ".join(...)` 係咩

`join()` 係 Python string method，用指定字串將一組 strings 連接成一條 string。

例如：

```python
errors = [
    "Meaning is required",
    "Level is required",
    "Category is required",
]

message = "; ".join(errors)
```

結果係：

```text
Meaning is required; Level is required; Category is required
```

呢度：

```python
"; "
```

係每一項之間使用嘅分隔符號。可以理解成：

```text
第一項 + "; " + 第二項 + "; " + 第三項
```

常見例子：

```python
", ".join(["A", "B", "C"])
# "A, B, C"

"\n".join(["line 1", "line 2"])
# "line 1\nline 2"

"".join(["日", "本", "語"])
# "日本語"
```

`join()` 要求 iterable 入面全部都係 string。如果有 integer：

```python
"; ".join([1, 2, 3])
```

會出現 `TypeError`。需要先轉換：

```python
"; ".join(str(value) for value in [1, 2, 3])
```

##### 7. 用嚟顯示 `ValidationError`

如果捕捉到：

```python
except ValidationError as exc:
```

`exc.messages` 通常係一個 message list，所以可以：

```python
self.message_user(
    request,
    "; ".join(exc.messages),
    messages.ERROR,
)
```

將多個 validation errors 合併成一條適合 Admin 顯示嘅訊息。

但如果 `ValidationError` 使用 field error dictionary 建立，亦可能需要處理 `exc.message_dict`，唔一定所有情況都只靠 `exc.messages` 呈現得最好。

官方參考：

- [ModelAdmin.message_user()](https://docs.djangoproject.com/en/6.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.message_user)
- [Django messages framework](https://docs.djangoproject.com/en/6.0/ref/contrib/messages/)
- [Python `str.join()`](https://docs.python.org/3/library/stdtypes.html#str.join)

#### 理解內容

-

<a id="DJANGO-ADMIN-M2M-WIDGET"></a>

### `[DJANGO-ADMIN-M2M-WIDGET]` Django Admin 入面 ManyToManyField 點樣改成 checkbox widget

#### 問題背景

`Vocab.categories` 改成 `ManyToManyField` 後，希望喺 Django admin vocab change page 入面用 multi-select checkbox 形式顯示 categories。

查到兩種做法：

- `formfield_for_manytomany()`
- `formfield_overrides`

暫時未完全肯定兩者分別，以及係咪一個 `formfield_overrides` 就會改晒所有 fields。

#### 研究方向

- Django admin default 點樣 render `ManyToManyField`。
- `formfield_for_manytomany()` 係針對咩時候用。
- `formfield_overrides` 係針對咩範圍用。
- 如果只想改 `Vocab.categories`，邊個做法較清楚。
- `filter_horizontal`、`filter_vertical`、`autocomplete_fields` 會唔會影響 widget。

#### 概念整理與解答

##### 1. `formfield_for_manytomany()`：針對 ManyToMany field 做客製

喺 `ModelAdmin` 入面可以 override：

```python
from django import forms

class VocabAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["widget"] = forms.CheckboxSelectMultiple
        return super().formfield_for_manytomany(db_field, request, **kwargs)
```

意思係：

```text
當 admin 建立 ManyToManyField 對應嘅 form field 時，
如果 field name 係 categories，
就用 CheckboxSelectMultiple。
```

呢個做法適合：

- 只想改某一個 ManyToMany field。
- 想根據 `db_field.name` 做不同處理。
- 想之後加 queryset filter、help text、label 等 field-specific customization。

##### 2. `formfield_overrides`：按 model field class 批量改 form field option

另一種做法：

```python
from django import forms
from django.db import models

class VocabAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {
            "widget": forms.CheckboxSelectMultiple,
        },
    }
```

意思係：

```text
喺呢個 ModelAdmin 入面，
凡係 ManyToManyField，
預設都用 CheckboxSelectMultiple。
```

所以你問：

```text
係咪只改一個 formfield_overrides 就會改晒？
```

答案係：**喺該 ModelAdmin 內，對應 field class 嘅 fields 會一齊受影響。**

例如 `VocabAdmin` 入面如果將來有多個 `ManyToManyField`，佢哋都有機會一齊變成 checkbox widget。

##### 3. 兩者分別

```text
formfield_for_manytomany()
-> 針對 ManyToManyField 嘅 hook
-> 可以用 db_field.name 指定某一個 field
-> field-specific，控制細

formfield_overrides
-> 按 model field class 批量套用
-> 例如所有 models.ManyToManyField 都改 widget
-> 寫法短，但影響範圍較大
```

如果只係想改：

```python
Vocab.categories
```

我會偏向用：

```python
formfield_for_manytomany()
```

因為清楚寫明只改 `categories`，之後加其他 M2M field 時唔會意外受影響。

##### 4. 不是所有 admin widget 設定都會同時用

Django admin 仲有其他 M2M display option：

```python
filter_horizontal = ("categories",)
filter_vertical = ("categories",)
autocomplete_fields = ("categories",)
```

呢啲都會影響 widget。

通常唔應該同時為同一 field 混用太多 widget 設定，例如：

```python
filter_horizontal = ("categories",)
```

再同時喺 `formfield_for_manytomany()` 強行改 checkbox，會令意圖唔清楚。

簡單規則：

```text
少量 categories -> CheckboxSelectMultiple 可以
大量 categories -> filter_horizontal / autocomplete_fields 更適合
```

你而家 categories 數量少，例如十幾個固定分類，用 checkbox 係合理。

##### 5. Checkbox widget 只係 admin form 顯示方式，不改 DB schema

無論 admin 用：

```python
CheckboxSelectMultiple
```

定係 default multi-select，背後保存都係同一個：

```python
Vocab.categories
```

亦即係 ManyToMany through table。

所以 widget 只影響：

```text
admin change page 點樣顯示 / 提交 categories
```

唔會改 database structure。

##### 6. 暫時建議

對目前 project，我會用：

```python
from django import forms

class VocabAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["widget"] = forms.CheckboxSelectMultiple
        return super().formfield_for_manytomany(db_field, request, **kwargs)
```

理由：

- `Vocab.categories` 係明確單一 field。
- categories 數量少，checkbox 易睇。
- 影響範圍細，日後加其他 M2M field 唔會被意外改 widget。

#### 理解內容

-

<a id="DJANGO-ADMIN-RELATED-OBJECTS-IN-USER-PAGE"></a>

### `[DJANGO-ADMIN-RELATED-OBJECTS-IN-USER-PAGE]` Admin User page 入面顯示 related `UserVocab`

#### 問題背景

想喺 Django admin 嘅 User change page 入面睇到該 user 擁有邊啲 `UserVocab`。

`UserVocab` 係由 user 指向 vocab 嘅 related model，所以 admin 入面有兩種常見做法：

1. 用 inline 直接喺 User page 下方列出 `UserVocab`
2. 喺 User page 顯示 count / link，跳去 filtered `UserVocab` admin list

#### 研究方向

- `TabularInline` / `StackedInline` 點樣喺 parent model admin 入面顯示 child model。
- Inline 適合少量 related data，但 related rows 太多時會令 admin page 好慢、好長。
- 用 count / filtered link 可以避免 User page 載入大量 `UserVocab`。
- 長期管理大量 related records 時，filtered admin list 通常比 inline 更易用。

#### 你的解答

##### 方法一：Inline 顯示 `UserVocab`

如果 `UserVocab` 有 `user = ForeignKey(User, related_name="user_vocabs", ...)`，可以喺 User admin 加 inline：

```python
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from dictionary.models import UserVocab

User = get_user_model()


class UserVocabInline(admin.TabularInline):
    model = UserVocab
    extra = 0
    fields = ("vocab", "in_use")
    readonly_fields = ("vocab",)
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserVocabInline]
```

優點：

- 入 User change page 就可以直接睇到 related `UserVocab`。
- Development / debug 時好直觀。
- 少量 rows 時操作方便。

缺點：

- 如果一個 user 有幾百甚至幾千個 vocab，User page 會變慢。
- Page 會好長，admin UX 會差。
- Inline 本身唔太適合大量資料管理。

##### 方法二：顯示 count / link 去 filtered admin list

如果想長期穩陣啲，可以喺 User admin 顯示 user vocab count，或者一條 link 去 `UserVocab` admin list。

例如 count：

```python
def user_vocab_count(self, obj):
    return obj.user_vocabs.count()

user_vocab_count.short_description = "User vocab count"
```

之後可以放入 `readonly_fields` 或 `list_display`。

如果要做 link，就可以 reverse 去 `UserVocab` changelist，再用 query string filter 指定 user。概念上係：

```text
/admin/dictionary/uservocab/?user__id__exact=<user_id>
```

優點：

- User page 唔會一次過載入大量 `UserVocab`。
- 真正要管理 vocab 時先入 filtered list。
- 對大量 data 比 inline 更穩定。

缺點：

- 無 inline 咁即場一眼睇晒。
- 要多 click 一次先見到完整 list。

#### 理解內容

- Inline 適合「少量、附屬、需要喺 parent page 快速睇或改」嘅 related data。
- Count / filtered link 適合「數量可能好多、需要獨立管理」嘅 related data。
- `UserVocab` 長遠可能好多，所以長期方案偏向 count / link；development debug 可以先用 inline。
- Admin page 設計唔只係能不能顯示，仲要考慮資料量同操作體驗。

<a id="DJANGO-DATETIME-LOCALTIME-ADMIN-FORMAT"></a>

### `[DJANGO-DATETIME-LOCALTIME-ADMIN-FORMAT]` Django admin datetime localtime 同 format

#### 問題背景

Admin page 入面會顯示好多 datetime，例如 `last_login`、`date_joined`、`create_at`、`update_at`、`last_vocab_sync_at`。

如果 database 存 UTC，但 project 設定係日本時間，就要理解 Django 係邊啲情況會自動轉 localtime，邊啲情況要自己處理。

另外，admin list display 嘅 datetime 格式可能用 `SHORT_DATETIME_FORMAT`，唔一定係 `DATETIME_FORMAT`。

#### 研究方向

- `USE_TZ=True` 時 Django 點樣保存 aware datetime。
- `TIME_ZONE="Asia/Tokyo"` 對 admin/template 顯示有咩影響。
- `FORMAT_MODULE_PATH` 點樣控制 global date/datetime display format。
- `DATETIME_FORMAT` 同 `SHORT_DATETIME_FORMAT` 分別喺咩位置使用。
- 自己 `.strftime()` 同 return datetime object 俾 admin format 有咩分別。

#### 你的解答

如果 settings 係：

```python
TIME_ZONE = "Asia/Tokyo"
USE_TZ = True
```

Django admin / template 直接顯示 model `DateTimeField` 時，通常會自動將 datetime 轉成目前 active timezone，即係 `Asia/Tokyo`。

例如直接顯示：

```python
@admin.display(description="Join at")
def create_at(self, obj):
    return obj.date_joined
```

呢種情況通常會由 Django admin 自己 localtime 同 format。

但如果自己手動 `.strftime()`：

```python
return obj.date_joined.strftime("%B %d, %Y, %H:%M:%S")
```

就已經繞過 Django admin 嘅 formatting。呢個時候應該先轉 localtime：

```python
from django.utils import timezone

return timezone.localtime(obj.date_joined).strftime("%B %d, %Y, %H:%M:%S")
```

如果想用 global format，要建立 format module，例如：

```text
core/
  formats/
    __init__.py
    en_US/
      __init__.py
      formats.py
```

`settings.py`：

```python
LANGUAGE_CODE = "en-us"
FORMAT_MODULE_PATH = ["core.formats"]
```

`core/formats/en_US/formats.py`：

```python
DATETIME_FORMAT = "F j, Y, H:i:s"
SHORT_DATETIME_FORMAT = "F j, Y, H:i:s"
```

注意：

- Django format string 用 `F j, Y, H:i:s`
- Python `.strftime()` 用 `"%B %d, %Y, %H:%M:%S"`
- `LANGUAGE_CODE="en-us"` 對應嘅 folder 係 `en_US`，唔係 `en-us`
- Admin changelist 入面嘅 datetime，例如 `last_login`，好多時會用 `SHORT_DATETIME_FORMAT`
- 改完 format module 後要 restart dev server，因為 format setting 可能已經被 cache

#### 理解內容

- 直接 return datetime object：Django admin 幫手 localtime + format。
- 自己 `.strftime()`：要自己 `timezone.localtime()`，global format 唔會再影響。
- 想全 admin datetime 統一，應該盡量 return datetime object，交俾 Django formatting system。
- `DATETIME_FORMAT` 同 `SHORT_DATETIME_FORMAT` 都要留意，admin list page 未必用你以為嗰個。

<a id="GROUP-DJANGO-FORMS-CBV"></a>

## Django Forms、CBV 與 Request Handling

<a id="DJANGO-HANDWRITTEN-CHECKBOX-POST-FORM"></a>

### `[DJANGO-HANDWRITTEN-CHECKBOX-POST-FORM]` 手寫 checkbox HTML，再用 Django Form 接 POST data

#### 問題背景

`UserVocabListView` 想用 table 形式顯示 user vocab：

```text
[checkbox] word / kana / meaning
```

UI 需要自己排 table，所以唔適合直接用 `{{ form.as_p }}` render 成個 form。
但 submit 後仍然想用 Django Form 驗證 POST data。

#### 研究方向

- 點解唔一定要喺 `get_context_data()` pass form 出去先可以用 form validate。
- Template 手寫 input 時，點樣同 Django Form field name 對應。
- `selectable_ids` 同 `selected_ids` 分別代表咩。
- 點解 checkbox 未勾選時唔會 submit。
- 點解要用 hidden input 記低畫面顯示過嘅 rows。

#### 概念整理與解答

##### 1. Form render 同 Form validation 可以分開

Django Form 有兩個常見用途：

- render HTML fields
- validate submitted data

平時可以用：

```django
{{ form.as_p }}
```

但如果 UI 要自訂 table layout，就可以手寫 HTML input，然後喺 view 入面用 Django Form 接 `request.POST` 做 validation。

重點係：Django Form 接收嘅係 `request.POST` 入面嘅 key/value。
只要 HTML input 嘅 `name` 對得上 form field name，form 就可以接到。

##### 2. Template 手寫 input

每一行 `UserVocab` 可以寫：

```django
<input type="hidden" name="selectable_ids" value="{{ user_vocab.id }}">
<input
    type="checkbox"
    class="in-use-checkbox"
    name="selected_ids"
    value="{{ user_vocab.id }}"
    {% if user_vocab.in_use %}checked{% endif %}
>
```

意思：

- `selectable_ids`：今次畫面顯示過嘅 `UserVocab.id`
- `selected_ids`：user 勾選咗、想設為 `in_use=True` 嘅 `UserVocab.id`

Hidden input 一定會 submit。
Checkbox 只有 checked 先會 submit。

##### 3. POST data 會變成點

如果畫面有三行：

```text
10 checked
11 unchecked
12 checked
```

POST 後會收到：

```text
selectable_ids = ["10", "11", "12"]
selected_ids = ["10", "12"]
```

所以：

- 10：畫面有 show，而且 checked -> `in_use=True`
- 11：畫面有 show，但無 checked -> `in_use=False`
- 12：畫面有 show，而且 checked -> `in_use=True`

唔喺 `selectable_ids` 入面嘅 rows，代表今次畫面無顯示，通常唔應該被更新。

##### 4. 用 Django Form 接住 POST data

Form 可以寫：

```python
class UserVocabInUseUpdateForm(forms.Form):
    selectable_ids = forms.ModelMultipleChoiceField(
        queryset=UserVocab.objects.none(),
        required=False,
    )
    selected_ids = forms.ModelMultipleChoiceField(
        queryset=UserVocab.objects.none(),
        required=False,
    )

    def __init__(self, *args, user_vocab_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user_vocab_queryset is not None:
            self.fields["selectable_ids"].queryset = user_vocab_queryset
            self.fields["selected_ids"].queryset = user_vocab_queryset
```

View 入面：

```python
form = UserVocabInUseUpdateForm(
    request.POST,
    user_vocab_queryset=user_vocab_queryset,
)
```

呢個 form 唔一定負責 render UI，而係負責：

- 驗證 submitted ids 必須屬於 `user_vocab_queryset`
- 將 raw ids 轉成 `UserVocab` objects

##### 5. 點解可以唔 pass form 去 context

如果 template 用手寫 input：

```django
<input name="selected_ids" ...>
```

就唔需要：

```python
context["update_form"] = UserVocabInUseUpdateForm(...)
```

因為 browser submit 時只理 HTML input 嘅 `name` / `value`，唔理 input 係 Django Form render 出嚟，定係手寫出嚟。

只有當 template 想用：

```django
{{ update_form.selected_ids }}
```

先需要 pass `update_form` 入 context。

#### 理解內容

-

<a id="DJANGO-MODEL-MULTIPLE-CHOICE-BULK-SELECT-FLOW"></a>

### `[DJANGO-MODEL-MULTIPLE-CHOICE-BULK-SELECT-FLOW]` 用 `ModelMultipleChoiceField` 做批量選擇 object 嘅處理流程

#### 問題背景

之前為 `UserVocabSelectVocabView` 設計過一個 flow：

- View 顯示一批 user 未擁有嘅 `Vocab`。
- User 用 checkbox 選擇想加入自己 list 嘅 vocab。
- Submit 後 view 將選中 vocab 交俾 service 建立 `UserVocab` relationship。

目前新設計改成 login 後自動建立 `UserVocab(in_use=False)`，所以暫時唔用呢個 flow 做加字。
但呢個 pattern 之後仍然可能用喺其他「從一批 model objects 入面勾選多個」嘅功能，所以保留做學習筆記。

#### 研究方向

- `ModelMultipleChoiceField` 點樣將 POST ids 轉成 model objects。
- 點解 field 初始 queryset 要用 `Model.objects.none()`。
- 點解要喺 form `__init__()` 動態注入 queryset。
- `FormView.get_form_kwargs()` 點樣將 view context 傳入 form。
- `cleaned_data["vocabs"]` 點解唔係 raw ids，而係 queryset / model objects。
- 點解 sliced queryset 可能令 `ModelMultipleChoiceField` POST validation 出問題。

#### 概念整理與解答

##### 1. Form 負責接收一批可選 vocab

原本 form：

```python
class UserVocabSelectForm(forms.Form):
    vocabs = forms.ModelMultipleChoiceField(
        queryset=Vocab.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, vocab_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)

        if vocab_queryset is not None:
            self.fields["vocabs"].queryset = vocab_queryset
```

`queryset=Vocab.objects.none()` 係安全 default：

- Form class 定義時未知道目前 user 係邊個。
- 唔應該喺 class level 放全站所有 vocab。
- 真正可選範圍應由 view 根據 `request.user` 動態傳入。

##### 2. View 決定目前 user 可選邊批 vocab

原本 view：

```python
class UserVocabSelectVocabView(LoginRequiredMixin, FormView):
    template_name = "dictionary/select_vocab.html"
    form_class = UserVocabSelectForm
    success_url = reverse_lazy("dictionary:user_vocab_list")

    def get_new_vocab(self):
        return UserVocabService.get_new_vocab(
            user=self.request.user,
            limit=50,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["vocab_queryset"] = self.get_new_vocab()
        return kwargs

    def form_valid(self, form):
        UserVocabService.create_user_vocabs(
            user=self.request.user,
            vocabs=form.cleaned_data["vocabs"],
        )
        return super().form_valid(form)
```

流程：

1. `get_new_vocab()` 取得目前 user 未擁有嘅 vocab。
2. `get_form_kwargs()` 將 `vocab_queryset` 傳入 form。
3. Form `__init__()` 將 field queryset 改成呢批 vocab。
4. Template render checkbox。
5. POST submit 後，`ModelMultipleChoiceField` 驗證 submitted ids 必須屬於 field queryset。
6. `form.cleaned_data["vocabs"]` 會係通過驗證嘅 `Vocab` objects。
7. View 將 objects 交俾 service 建立 `UserVocab`。

##### 3. `ModelMultipleChoiceField` 做緊咩

如果 checkbox submit：

```text
vocabs = [1, 2, 5]
```

`ModelMultipleChoiceField` 會：

- 用 field queryset 檢查 `1, 2, 5` 是否都係合法選項。
- 將 ids 轉成對應 model objects。
- 如果有 id 唔喺 queryset 入面，就 form invalid。

所以 service 收到嘅：

```python
form.cleaned_data["vocabs"]
```

唔係純 list of ids，而係一批已經 validate 過嘅 `Vocab` objects / queryset。

##### 4. Service 負責建立 relationship

原本 service：

```python
@staticmethod
def create_user_vocabs(*, user, vocabs):
    for vocab in vocabs:
        with transaction.atomic():
            user_vocab, created = UserVocab.objects.get_or_create(
                user=user,
                vocab=vocab,
            )
```

`get_or_create()` 令重複提交唔會建立 duplicate relationship。

之後如果沿用 `UserVocab.in_use=False` 設計，建立時可以依靠 model default，或者明確寫：

```python
defaults={"in_use": False}
```

##### 5. 點解要小心 sliced queryset

如果 service 用：

```python
Vocab.objects.exclude(...).order_by("-id")[:50]
```

呢個係 sliced queryset。
`ModelMultipleChoiceField` 喺 POST validation 時可能需要再對 queryset 做 filter，例如檢查 submitted ids 是否屬於 queryset。

Sliced queryset 再 filter 可能會出現問題。

較穩陣寫法係先取 ids：

```python
vocab_ids = (
    Vocab.objects
    .exclude(user_vocab__user=user)
    .order_by("-id")
    .values_list("id", flat=True)[:limit]
)

return Vocab.objects.filter(id__in=vocab_ids)
```

外層 `Vocab.objects.filter(id__in=vocab_ids)` 係未 sliced queryset，較適合交俾 form field 做 validation。

##### 6. 呢個 pattern 之後可以用喺邊

呢個 flow 適合：

- 從候選 vocab 入面批量加入 user list。
- 從候選 users 入面批量 assign permission / group。
- 從候選 items 入面批量建立 relationship。
- 任何「畫面 show 一批合法 objects，user checkbox 選多個，submit 後建立關係」嘅情境。

如果 UI 係一個 list table，每行要顯示 word / kana / meaning，再手寫 checkbox，仍然可以保留同一個核心概念：

- 用 hidden / checkbox value 提交 object id。
- 用 form field 或 view queryset 驗證 ids 屬於目前 user 可操作範圍。
- service 只處理通過 validation 嘅 objects。

#### 理解內容

-

<a id="DJANGO-MODEL-MULTIPLE-CHOICE-FIELD-M2M-SET"></a>

### `[DJANGO-MODEL-MULTIPLE-CHOICE-FIELD-M2M-SET]` `ModelMultipleChoiceField`、ManyToManyField 同 `.set()` 嘅關係

#### 問題背景

今次將 vocab category 改成最多三個 categories 時，用咗：

```python
categories = forms.ModelMultipleChoiceField(
    queryset=Category.objects.all(),
    required=False,
    widget=forms.CheckboxSelectMultiple,
)
```

保存時又用咗：

```python
vocab.categories.set(categories)
```

疑問係：

- `ModelMultipleChoiceField` 做緊咩？
- `vocab.categories.set()` 又係咩？
- `.set()` 係咪只係配合 `ModelMultipleChoiceField` 先用？
- 呢個係 form 嘅功能，定係 ManyToMany relationship 嘅功能？

#### 研究方向

- `ModelMultipleChoiceField` cleaned_data 回傳咩。
- `ManyToManyField` 喺 model instance 上會變成咩 object。
- `.set()` 係邊個 object 嘅 method。
- 點解 M2M 要先 save main object，之後先可以 `.set()`。
- `create` / `update` / `request approve` flow 入面點樣傳 categories。

#### 概念整理與解答

##### 1. `ModelMultipleChoiceField` 係 form field

`ModelMultipleChoiceField` 負責喺 form layer 接收多個 model objects。

例如：

```python
categories = forms.ModelMultipleChoiceField(
    queryset=Category.objects.all(),
    required=False,
)
```

佢會做幾件事：

- 顯示多個可選 `Category`。
- POST 時接收多個 category ids。
- 驗證 submitted ids 必須存在於 `queryset`。
- `form.cleaned_data["categories"]` 會變成一個 `Category` QuerySet。

概念：

```python
form.cleaned_data["categories"]
# -> <QuerySet [Category(...), Category(...)]>
```

所以 `ModelMultipleChoiceField` 只係負責：

```text
HTML / POST data -> Python/Django model objects
```

##### 2. `ManyToManyField` 係 model relationship

model 入面：

```python
class Vocab(models.Model):
    categories = models.ManyToManyField(Category, related_name="vocabs")
```

意思係：

```text
一個 Vocab 可以有多個 Category
一個 Category 可以屬於多個 Vocab
```

Django 會喺背後建立一張 through table，大概概念係：

```text
vocab_id | category_id
```

例如：

```text
1 | 3
1 | 5
1 | 8
```

代表 vocab 1 有三個 categories。

##### 3. `vocab.categories` 係 relationship manager

當你有一個已 save 嘅 vocab：

```python
vocab = Vocab.objects.get(pk=1)
```

你寫：

```python
vocab.categories
```

得到嘅唔係一個普通 list，而係 Django 嘅 ManyRelatedManager。

佢有一堆 method，例如：

```python
vocab.categories.all()
vocab.categories.add(category)
vocab.categories.remove(category)
vocab.categories.clear()
vocab.categories.set(categories)
```

所以：

```python
vocab.categories.set(...)
```

係 **ManyToManyField relationship manager** 嘅 method，唔係 `ModelMultipleChoiceField` 嘅 method。

##### 4. `.set()` 係用嚟同步整組 M2M 關係

```python
vocab.categories.set(categories)
```

意思係：

```text
將呢個 vocab 目前嘅 categories 改成傳入去嗰一組 categories
```

例如原本：

```text
vocab.categories = [A, B]
```

執行：

```python
vocab.categories.set([B, C, D])
```

之後會變成：

```text
vocab.categories = [B, C, D]
```

Django 會幫你：

- 保留 B
- 移除 A
- 加入 C、D

所以 `.set()` 好適合 form submit 後「以今次表單選擇為準」嘅情況。

##### 5. `.set()` 唔係只可以配合 `ModelMultipleChoiceField`

`.set()` 可以接收好多種 iterable：

```python
vocab.categories.set(category_queryset)
vocab.categories.set([category1, category2])
vocab.categories.set([1, 2, 3])
```

所以佢唔係 form 專用。

只係因為：

```python
ModelMultipleChoiceField.cleaned_data
```

剛好會回傳一個 QuerySet，所以可以直接傳入：

```python
categories = form.cleaned_data["categories"]
vocab.categories.set(categories)
```

##### 6. 點解要先 `vocab.save()` 再 `.set()`

ManyToMany relationship 需要 main object 有 primary key。

如果 vocab 未 save：

```python
vocab = Vocab(...)
vocab.categories.set(categories)  # 不可以
```

因為 through table 需要：

```text
vocab_id
category_id
```

但未 save 嘅 vocab 仲未有 `id`。

正確順序：

```python
vocab = Vocab(...)
vocab.full_clean()
vocab.save()
vocab.categories.set(categories)
```

##### 7. 今次 project 入面嘅 flow

Create vocab：

```python
categories = form.cleaned_data["categories"]

vocab = Vocab(...)
vocab.save()
vocab.categories.set(categories)
```

Create / update request：

```python
request = VocabRequest.objects.create(...)
request.proposed_categories.set(form.cleaned_data["categories"])
```

Approve request：

```python
vocab_data = {
    "categories": vocab_request.proposed_categories.all(),
}

VocabActionService.create_vocab(vocab_data, approved_by)
```

Import CSV：

```python
categories = Category.objects.filter(name__in=category_names)
VocabActionService.create_vocab(
    {
        "categories": categories,
        ...
    },
    approved_by=user,
)
```

##### 8. 重點總結

```text
ModelMultipleChoiceField
-> form layer
-> 將 POST 入面多個 ids 變成 Category QuerySet

ManyToManyField
-> model relationship
-> 保存 Vocab 同 Category 嘅多對多關係

vocab.categories.set(...)
-> relationship manager method
-> 將某個 vocab 嘅 categories 同步成指定一組 categories
```

所以：

```text
.set() 係 MTOM / ManyToManyField 嘅東西
唔係 ModelMultipleChoiceField 專用
```

只係 `ModelMultipleChoiceField` 嘅 cleaned_data 格式剛好好適合交俾 `.set()`。

#### 理解內容

-

<a id="DJANGO-SLICED-QUERYSET-MULTIPLE-CHOICE"></a>

### `[DJANGO-SLICED-QUERYSET-MULTIPLE-CHOICE]` Sliced QuerySet 點解唔可以直接交俾 `ModelMultipleChoiceField`

#### 問題背景

目前選擇新 vocab 嘅 service 會限制只回傳頭 50 筆：

```python
return (
    Vocab.objects
    .exclude(user_vocab__user=user)
    .order_by("-id")[:50]
)
```

呢個 QuerySet 會交俾：

```python
forms.ModelMultipleChoiceField(...)
```

雖然自己冇再呼叫 `.filter()`，但 form POST validation 時仍然可能出現：

```text
TypeError: Cannot filter a query once a slice has been taken
```

#### 研究方向

- QuerySet slicing `[:50]` 會點樣改變 QuerySet。
- 點解 sliced QuerySet 唔可以再使用 `.filter()`。
- `ModelMultipleChoiceField` 驗證 submitted IDs 時會做咩。
- 點解 GET 顯示正常，但 POST validation 先出錯。
- 點樣限制候選數量，同時保留可以再 filter 嘅 QuerySet。

#### 概念整理與解答

##### 1. `[:50]` 會建立 sliced QuerySet

以下寫法代表 SQL 查詢只取頭 50 筆：

```python
qs = Vocab.objects.order_by("-id")[:50]
```

概念上等同 SQL：

```sql
SELECT ...
FROM vocab
ORDER BY id DESC
LIMIT 50;
```

Django 會將呢個 QuerySet 標記為已經設定 limit。

##### 2. 點解 sliced QuerySet 唔可以再 filter

例如：

```python
qs = Vocab.objects.order_by("-id")[:50]
qs.filter(pk__in=[1, 2, 3])
```

Django 唔容許呢種操作，因為「先取頭 50 筆，再 filter」同「先 filter，再取頭 50 筆」可能得到完全唔同嘅結果。

為咗避免產生語意不清嘅 SQL，Django 會直接拋出：

```text
TypeError: Cannot filter a query once a slice has been taken
```

##### 3. 自己冇 `.filter()`，點解仍然會出錯

`ModelMultipleChoiceField` 收到 POST 提交嘅 IDs 後，需要確認：

- 每個 ID 真係存在。
- 每個 object 都屬於 field 容許選擇嘅 QuerySet。
- User 冇修改 POST data，提交畫面以外嘅 ID。

所以 Django 內部會對 field queryset 做類似：

```python
queryset.filter(pk__in=submitted_ids)
```

如果原本交俾 field 嘅 QuerySet 已經 `[:50]`，內部 validation 再 filter 時就會出錯。

因此：

```text
GET 顯示選項
-> 只需要讀取 sliced QuerySet，通常正常

POST 驗證選項
-> ModelMultipleChoiceField 需要再 filter
-> sliced QuerySet 引發 TypeError
```

##### 4. 解法：先取得有限數量嘅 IDs

先用 slicing 取得最多 50 個 IDs：

```python
vocab_ids = (
    Vocab.objects
    .filter(is_active=True)
    .exclude(user_vocab__user=user)
    .order_by("-id")
    .values_list("id", flat=True)[:limit]
)
```

呢個 sliced QuerySet 只負責決定允許嘅 IDs。

##### 5. 再建立一個未 sliced QuerySet

使用 IDs 建立新 QuerySet：

```python
return Vocab.objects.filter(id__in=vocab_ids)
```

最後回傳嘅外層 QuerySet本身冇使用 `[:limit]`，所以 `ModelMultipleChoiceField` 可以安全再做：

```python
queryset.filter(pk__in=submitted_ids)
```

完整例子：

```python
@staticmethod
def get_new_vocab(*, user, limit=50):
    vocab_ids = (
        Vocab.objects
        .filter(is_active=True)
        .exclude(user_vocab__user=user)
        .order_by("-id")
        .values_list("id", flat=True)[:limit]
    )

    return Vocab.objects.filter(id__in=vocab_ids)
```

##### 6. 排序注意事項

外層：

```python
Vocab.objects.filter(id__in=vocab_ids)
```

唔會自動保證跟返內層 `-id` 次序。如果畫面需要最新 vocab 排先，可以再加：

```python
return (
    Vocab.objects
    .filter(id__in=vocab_ids)
    .order_by("-id")
)
```

呢個 `.order_by()` 係加喺未 sliced 嘅外層 QuerySet，所以可以正常使用。

##### 7. `id__in` 解法嘅核心概念

```text
內層 QuerySet
-> 排序及限制頭 50 個 IDs

外層 QuerySet
-> 根據呢批 IDs 重新查詢
-> 本身冇 slice
-> 可以交俾 ModelMultipleChoiceField 再 filter
```

#### 理解內容

-

<a id="DJANGO-CBV-OBJECT-ID"></a>

### `[DJANGO-CBV-OBJECT-ID]` Detail／Update／Delete View 點樣取得目標 Object

#### 問題背景

目前對 User detail、Vocab detail、UpdateView 同 DeleteView 點樣指定及取得目標 object 的 pk／ID 仲未完全理解。

#### 研究方向

- URL pattern 入面 `<int:pk>`、`<int:vocab_id>` 等參數有咩分別。
- URL 傳入的 ID 點樣進入 `self.kwargs`。
- Django generic `DetailView`、`UpdateView`、`DeleteView` 預設點樣使用 `pk_url_kwarg` 尋找 object。
- 使用預設 `pk` 同自訂 `vocab_id` 時，需要喺 View 加咩設定。
- `get_object()`、`get_queryset()` 同 `get_context_data()` 各自負責咩。
- 點解目前 User detail 可以直接使用登入中的 `request.user`，但 Vocab detail 需要根據 URL ID 查詢。

#### 概念整理與解答

##### 1. ID 由 URL 開始傳入

以目前 dictionary URL 為例：

```python
path(
    "vocab/<int:vocab_id>",
    VocabDetailView.as_view(),
    name="vocab_detail",
)
```

假設瀏覽器進入：

```text
/dictionary/vocab/15
```

Django URL resolver 會將 `15` 轉成 integer，並用 URL 中設定的名稱儲存：

```python
{"vocab_id": 15}
```

之後 `VocabDetailView.as_view()` 建立及執行 view instance。Django CBV 的 `setup()` 會將 URL keyword arguments 放入：

```python
self.kwargs
```

因此 view 入面可以讀取：

```python
self.kwargs["vocab_id"]  # 15
```

`vocab_id` 只係 URL parameter 的自訂名稱，唔係 Django 特別保留的字。

##### 2. 目前 Vocab detail 點樣取得 Object

目前 `VocabDetailView` 繼承 `TemplateView`，所以 Django唔會自動根據 ID 查詢 `Vocab`。現有 code 係自己處理：

```python
context["vocab"] = get_object_or_404(
    Vocab,
    pk=self.kwargs["vocab_id"],
)
```

流程係：

```text
URL 的 vocab_id
-> self.kwargs["vocab_id"]
-> Vocab.objects 根據 pk 查詢
-> 找到的 object 放入 context["vocab"]
-> template 使用 {{ vocab }}
```

如果 ID 不存在，`get_object_or_404()` 會回傳 HTTP 404。

##### 3. 目前 Update／Delete 點樣取得 Object

目前 update/delete views 繼承 `FormView`，唔係 Django generic `UpdateView` 或 `DeleteView`，所以亦唔會自動查詢 object。

兩個 views 都用自訂 property：

```python
@property
def target_vocab(self):
    if not hasattr(self, "_target_vocab"):
        self._target_vocab = get_object_or_404(
            Vocab,
            pk=self.kwargs["vocab_id"],
        )
    return self._target_vocab
```

第一次使用 `self.target_vocab` 時，先根據 URL 的 `vocab_id` 查詢 database；之後暫存在 `self._target_vocab`，同一個 request 內再次使用時唔需要重新查詢。

##### 4. Generic DetailView／UpdateView／DeleteView 的預設行為

`DetailView`、`UpdateView` 同 `DeleteView` 都會使用 `SingleObjectMixin`。只要設定：

```python
model = Vocab
```

Django 的 `get_object()` 就會由 URL kwargs 尋找 primary key。預設參數名稱係：

```python
pk_url_kwarg = "pk"
```

所以最直接的 URL 寫法係：

```python
path("vocab/<int:pk>/", VocabDetailView.as_view())
```

View 可以寫成：

```python
class VocabDetailView(DetailView):
    model = Vocab
    template_name = "dictionary/vocab_detail.html"
    context_object_name = "vocab"
```

Django 會自動做近似以下查詢：

```python
Vocab.objects.get(pk=self.kwargs["pk"])
```

並將結果存入：

```python
self.object
```

##### 5. 想保留 vocab_id 名稱時

如果 URL 想繼續使用：

```python
<int:vocab_id>
```

Generic view 要設定：

```python
pk_url_kwarg = "vocab_id"
```

例如：

```python
class VocabDetailView(DetailView):
    model = Vocab
    pk_url_kwarg = "vocab_id"
    context_object_name = "vocab"
```

否則 generic view 預設會尋找 `self.kwargs["pk"]`，但 URL 只有 `vocab_id`，因而無法自動取得 object。

##### 6. get_object、get_queryset、get_context_data 的分工

- `get_queryset()`
  - 決定容許由邊一批 records 之中尋找 object。
  - 可以加入 `is_active=True`、user ownership、permission scope 等限制。

- `get_object()`
  - 從 queryset 中，根據 URL 的 pk 或 slug 取得單一 object。
  - 結果通常存入 `self.object`。

- `get_context_data()`
  - 將已取得的 object 及其他資料交俾 template。
  - 唔應將所有 object lookup 邏輯都塞入呢度，除非使用的係 `TemplateView` 並選擇手動處理。

##### 7. 點解 User detail 無傳 ID

目前 accounts URL 係：

```python
path("user_detail/", UserView.as_view())
```

URL 無 `<int:pk>`，而 `UserView` 亦只係 `TemplateView`。呢頁代表「目前已登入的使用者自己」，唔係「由 URL 指定的任意 User」。

因為 Django auth context processor 會將目前登入的 user 放入 template context，所以 template 可以直接使用：

```django
{{ user.email }}
```

呢個 `user` 來自：

```python
request.user
```

如果將來要做 admin/public user profile，例如：

```text
/accounts/users/15/
```

先需要在 URL 傳入 User ID，並使用 `DetailView` 或手動根據該 ID 查詢。亦要加入權限檢查，避免任何人只改 URL ID 就睇到其他人的私人資料。

##### 8. 最重要的分別

```text
TemplateView／FormView
-> URL kwargs 仍然存在
-> 但要自己用 self.kwargs 查 object

DetailView／UpdateView／DeleteView
-> 使用 SingleObjectMixin
-> 可以根據 pk_url_kwarg 自動查 object
-> object 會放入 self.object
```

官方參考：

- [SingleObjectMixin](https://docs.djangoproject.com/en/6.0/ref/class-based-views/mixins-single-object/)
- [DetailView](https://docs.djangoproject.com/en/6.0/ref/class-based-views/generic-display/#detailview)
- [UpdateView／DeleteView](https://docs.djangoproject.com/en/6.0/ref/class-based-views/generic-editing/)

#### 理解內容

-

<a id="DJANGO-DETAILVIEW-WITH-MINI-FORM"></a>

### `[DJANGO-DETAILVIEW-WITH-MINI-FORM]` DetailView 入面放一張小型 Form

#### 問題背景

`UserVocabDetailView` 本身係 `DetailView`，主要責任係根據 URL 入面嘅 `pk` 取得一個 `UserVocab` object，然後 render detail page。

但 detail page 入面又想加入一個細功能：只更新目前呢一個 `UserVocab.in_use`。

呢種情況唔係完整 `FormView`，而係：

```text
DetailView 負責顯示 object
同一頁額外放一張 mini form
POST 時手動處理呢張 form
```

#### 研究方向

- `DetailView` 同 `FormView` 分工有咩唔同。
- 點解 `DetailView` 唔會自動提供 `get_form()` / `form_valid()` lifecycle。
- 點樣喺 `get_context_data()` 放一張 initial form。
- 點樣喺 `post()` 入面手動建立 bound form。
- `get_queryset()` ownership guard 點樣保護 user 只能改自己嘅 object。
- 點解某啲 form 需要額外 kwargs，例如 queryset / target object，而某啲簡單 form 唔需要。

#### 概念整理與解答

##### 1. FormView 係「form 做主角」

`FormView` 內建 form lifecycle：

```text
get_form_class()
get_form()
get_form_kwargs()
form_valid()
form_invalid()
```

所以 create / update / request submission 呢類「submit form 係主流程」嘅頁面，用 `FormView` 會自然好多。

##### 2. DetailView 係「object 做主角」

`DetailView` 主要使用 `SingleObjectMixin`：

```python
self.object = self.get_object()
```

然後將 object 放入 context：

```python
context["object"]
context["user_vocab"]  # 如果 context_object_name = "user_vocab"
```

所以 detail page 入面想加 form，就要自己處理：

- GET：喺 `get_context_data()` 放 initial form。
- POST：喺 `post()` 手動 instantiate form、validate、save object。

##### 3. UserVocab detail in_use form pattern

Form 可以好簡單：

```python
class UserVocabInUseSingleUpdateForm(forms.Form):
    in_use = forms.BooleanField(required=False)
```

因為 checkbox 無 tick 時，browser 不會 submit 該欄位，所以 `required=False` 好重要。

DetailView 可以用：

```python
class UserVocabDetailView(LoginRequiredMixin, DetailView):
    model = UserVocab
    template_name = "dictionary/user_vocab_detail.html"
    context_object_name = "user_vocab"

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user,
            vocab__is_active=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["in_use_form"] = UserVocabInUseSingleUpdateForm(
            initial={"in_use": self.object.in_use}
        )
        return context

    def post(self, request, *args, **kwargs):
        user_vocab = self.get_object()
        form = UserVocabInUseSingleUpdateForm(request.POST)

        if form.is_valid():
            user_vocab.in_use = form.cleaned_data["in_use"]
            user_vocab.save(update_fields=["in_use", "update_at"])
            return redirect(request.get_full_path())

        self.object = user_vocab
        context = self.get_context_data(object=user_vocab)
        context["in_use_form"] = form
        return self.render_to_response(context)
```

##### 4. 點解今次 form 唔需要傳 `user_vocab`

今次 form 只做：

```python
in_use = forms.BooleanField(required=False)
```

佢只需要接收一個 boolean value。

真正要保護「只能更新自己嘅 UserVocab」嘅地方，係：

```python
def get_queryset(self):
    return super().get_queryset().filter(user=self.request.user)
```

然後 `post()` 入面：

```python
user_vocab = self.get_object()
```

會經過同一個 queryset guard。

所以呢張 form 唔需要：

```python
UserVocabInUseSingleUpdateForm(request.POST, user_vocab=user_vocab)
```

除非 form 本身要根據 `user_vocab` 做 validation，先需要自訂 `__init__()` 接額外 kwarg。

##### 5. Template 寫法

```django
<form method="POST">
    {% csrf_token %}
    {{ in_use_form.in_use }}
    <button type="submit">Update</button>
</form>
```

Checkbox 勾選時會 submit `in_use=on`，form 會 clean 成 `True`。

Checkbox 無勾時不會 submit `in_use`，因為 `required=False`，form 會 clean 成 `False`。

##### 6. 重點

```text
DetailView + mini form
= object 顯示由 DetailView 負責
= form GET context 自己加
= POST validation 自己寫
= object ownership 仍然靠 get_queryset() 收窄
```

呢個 pattern 適合細型 toggle / update，例如：

- 單一 `UserVocab.in_use`
- mark one item as read
- toggle favorite
- update one small setting

如果 form 開始變複雜，或者有多個 action，就可以考慮拆成獨立 `FormView` / action endpoint。

#### 理解內容

-

<a id="DJANGO-AJAX-FORMVIEW-INVALID-JSON"></a>

### `[DJANGO-AJAX-FORMVIEW-INVALID-JSON]` AJAX FormView 驗證失敗時點解要回傳 JSON

#### 問題背景

Quiz play page 使用 JavaScript `fetch()` 提交答案、Next、Skip 同 Summary forms，成功時由後端回傳：

```json
{
  "main_html": "...",
  "input_panel_html": "..."
}
```

前端收到 JSON 後，將兩段 partial HTML 放入對應 containers。問題係 `QuizSubmitAnswerView` 只實作咗 `form_valid()`，但冇實作 AJAX 專用嘅 `form_invalid()`，而且亦冇完整頁面用嘅 `template_name`。

例如 user 未輸入答案就提交時，`QuizForm.answer` 因為 `required=True` 而驗證失敗。呢個只係預期內嘅輸入錯誤，唔應該變成 server 500。

#### 研究方向

- `FormView.post()` 點樣按 `form.is_valid()` 分流到 `form_valid()` 或 `form_invalid()`。
- Django 預設 `form_invalid()` 點解會嘗試 render template。
- AJAX endpoint 點解成功與失敗都應維持清楚、穩定嘅 JSON response contract。
- `fetch()` 點樣用 `response.ok` 區分 2xx 同 4xx response。
- 點解 `fetch()` 收到 HTTP 400／403／404／500 通常仍然係 fulfilled，而唔會自動進入 `.catch()`。
- 解析前點樣用 response `Content-Type` 分辨 JSON contract 同 HTML error page。
- HTTP 400 JSON response 同全域 `handler400` error page 有咩分別。
- 多個 AJAX `FormView` 何時適合共用一個 invalid-form mixin。

#### 你的解答

##### 1. `FormView` 有成功與失敗兩條路

概念流程係：

```text
收到 POST
  ↓
Django 建立並驗證 form
  ├── valid   → form_valid(form)
  └── invalid → form_invalid(form)
```

目前 Quiz AJAX views 嘅成功路線會回傳 `JsonResponse`。但 Django 預設 `form_invalid()` 係為普通完整頁面 form 而設，會將有 errors 嘅 form放入 context，再嘗試重新 render view template。

`QuizSubmitAnswerView` 冇 `template_name`，因為佢本身只係 AJAX endpoint。如果 invalid POST 跌入預設 `form_invalid()`，Django可能因搵唔到要 render 嘅 template 而拋出 exception，令普通 validation error錯誤地變成 500。

##### 2. 預期輸入錯誤唔係 server exception

以下情況屬於 form validation failure：

- `answer` 為空；
- `user_vocab_id` 遺失或唔係整數；
- `tips_count` 遺失、細過 0 或大過 50。

呢啲情況代表 client提交嘅資料唔符合 form規則。後端應回傳可預期嘅 4xx JSON，讓前端提示 user修正，而唔係交畀全域 500 page處理。

##### 3. AJAX view 應自訂 `form_invalid()`

概念例子：

```python
def form_invalid(self, form):
    return JsonResponse(
        {
            "success": False,
            "errors": form.errors.get_json_data(),
        },
        status=400,
    )
```

呢個 response係 view主動回傳嘅 HTTP 400 JSON，唔會經過全域 `handler400`。全域 `handler400` 負責通用 HTML error page；AJAX endpoint就要回傳前端預期嘅 JSON格式。

如果多個 AJAX `FormView` 都要採用相同格式，可以抽成共用 mixin，並將 mixin放喺 inheritance list嘅 `FormView`之前，確保自訂 `form_invalid()` 會被使用。

##### 4. 前端唔可以假設所有 response都成功

目前 JavaScript直接執行：

```javascript
.then(res => res.json())
.then(data => {
    quizAreaContainer.innerHTML = data.main_html;
    quizInputPanelContainer.innerHTML = data.input_panel_html;
})
```

如果 invalid response只有 `errors`，前端仍然讀取 `main_html`，就會得到 `undefined`。如果 server意外回傳 HTML error page，`res.json()`亦會因內容唔係 JSON而失敗。

前端唔可以只靠 `response.ok`決定要唔要解析 JSON，因為預期內嘅 HTTP 400 validation response本身就係有用嘅 JSON。應先確認 response係 JSON並解析，再按 `success`處理成功或 validation failure；如果 response係 HTML或JSON parsing失敗，就交由通用錯誤分支處理。

##### 5. 前端應遍歷所有 field errors，唔應只寫死 `answer`

`form.errors.get_json_data()` 嘅 key係發生錯誤嘅 field name，每個 field可以同時有多個 errors。例如：

```json
{
  "success": false,
  "errors": {
    "answer": [
      {"message": "This field is required.", "code": "required"}
    ],
    "tips_count": [
      {"message": "Ensure this value is less than or equal to 50.", "code": "max_value"}
    ]
  }
}
```

如果前端只讀：

```javascript
data.errors.answer[0].message
```

就只會處理 `answer` 第一個 error，會漏咗其他 fields同同一 field嘅其他 errors。通用做法係用 `Object.entries()`遍歷全部 fields，再遍歷每個 field嘅 error array：

```javascript
function renderFormErrors(errors, container) {
    container.replaceChildren();

    Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
        fieldErrors.forEach(error => {
            const message = document.createElement("p");
            message.textContent = `${fieldName}: ${error.message}`;
            container.appendChild(message);
        });
    });
}
```

失敗分支可以呼叫：

```javascript
if (data.success === false) {
    renderFormErrors(data.errors, errorContainer);
    return;
}
```

成功分支先清走舊錯誤並更新 partial HTML：

```javascript
errorContainer.replaceChildren();
quizAreaContainer.innerHTML = data.main_html;
quizInputPanelContainer.innerHTML = data.input_panel_html;
```

Form-level validation如果唔屬於單一 field，Django會用 `__all__`做 key。前端可以將 `__all__`只顯示 message，唔顯示 field name。

另外，`user_vocab_id`同`tips_count`係 hidden/internal fields，直接向普通 user顯示技術 field name未必有幫助。UI可以將已知 user-facing field errors顯示具體訊息，而 internal state errors統一顯示「Quiz資料已失效，請重新載入頁面」。無論 wording點設計，前端邏輯仍應先收集全部 errors，避免靜默漏掉問題。

使用 `textContent`配合新建 DOM element顯示 error message，可以避免將 response文字直接當HTML插入畫面。

##### 6. `fetch()` 收到 HTTP error唔代表 Promise自動 reject

`fetch()`通常只會喺網絡層失敗，例如無法連線、DNS問題或request被中止時 reject。Server成功回傳 HTTP response時，即使 status係400或500，第一個 `.then()`一般仍然會執行：

```text
HTTP 200 → fetch fulfilled
HTTP 400 → fetch fulfilled
HTTP 500 → fetch fulfilled
網絡失敗 → fetch rejected → .catch()
```

因此要自行查看：

```javascript
response.ok
response.status
response.headers.get("content-type")
```

但 `response.ok === false`唔可以一律當成非JSON錯誤，因為目前 invalid form正正係 HTTP 400 JSON：

```json
{
  "success": false,
  "errors": {}
}
```

呢種response仍應先用 `response.json()`解析，再由 `data.success === false`分支顯示 field errors。

##### 7. 非JSON response點解會令 `res.json()`失敗

AJAX endpoint並唔保證任何情況都回傳JSON。例如：

- 未處理exception觸發500 HTML page；
- CSRF失敗回傳403 HTML；
- login或quiz session失效後redirect到完整HTML頁；
- URL錯誤回傳404 HTML。

如果內容以HTML開頭：

```html
<!DOCTYPE html>
```

而JavaScript仍執行：

```javascript
response.json()
```

JSON parser可能拋出 `Unexpected token '<'`。後面處理 `data.main_html`或`data.errors`嘅 `.then()`唔會執行；如果冇 `.catch()`，user只會覺得按鈕冇反應。

最低限度處理方向係先檢查 `Content-Type`：

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

再用 `.catch()`顯示通用、可恢復訊息，而唔係將403／500 HTML插入partial container：

```javascript
.catch(error => {
    console.error(error);
    const errorContainer =
        document.getElementById("quiz-error-message");
    errorContainer.textContent =
        "系統暫時發生問題，請重新整理頁面再試。";
});
```

目前專案已實作以上 `Content-Type` guard同 `.catch()`。因此400 JSON仍會正常解析並顯示structured field errors；403／404／500 HTML、network failure同JSON parsing failure就會顯示通用恢復提示。Code-path review確認接線正確，但目前環境冇Node，仍未完成JavaScript runtime或browser integration自動驗證。

完整心智模型應分四條路：

```text
200 JSON + success=true
→ 更新Quiz partials

400 JSON + success=false
→ 顯示form field errors

403／404／500 HTML或其他非JSON內容
→ 停止JSON處理，顯示通用錯誤提示

網絡失敗
→ .catch()顯示通用錯誤提示
```

##### 8. 應驗證嘅行為

- 空答案回傳 HTTP 400 JSON，errors包含 `answer` required，唔係500。
- 無效 `tips_count` 回傳 HTTP 400 JSON及對應 field error。
- 有效答案維持 HTTP 200，並回傳 `main_html`同 `input_panel_html`。
- 前端收到4xx JSON時顯示可恢復提示，唔會將 `undefined`插入畫面。
- 前端收到403／404／500 HTML時唔會嘗試當partial JSON使用，並會顯示通用錯誤提示。
- 網絡或JSON parsing失敗會進入 `.catch()`，而唔係無聲停止。

#### 理解內容

- AJAX `FormView` 唔只要設計成功 response，亦要設計 invalid form response。
- Form validation failure係預期內 client input問題；真正未處理 exception先應成為500。
- Response格式係前後端共同 contract：後端回傳400 JSON後，前端要解析JSON並按 `success`顯示 errors，唔可以單靠 `response.ok`判斷response格式。
- `errors`係以 field name對應 error array；前端應遍歷全部 fields同全部 messages，而唔係只寫死 `answer[0]`。
- `__all__`代表 form-level／non-field error；hidden/internal field errors可以轉成較易理解嘅恢復提示。
- HTTP 400／500唔會令 `fetch()`自動 reject；HTTP status、response格式同JSON內嘅 `success`係三個不同層次。
- 預期400 JSON應解析並顯示field errors；非JSON HTML、網絡失敗或JSON parsing failure先進入通用恢復提示。
- 通用400 HTML頁同 AJAX 400 JSON用途唔同；前者畀browser完整頁面，後者畀JavaScript處理。

<a id="GROUP-DJANGO-ORM-DATABASE"></a>

## Django ORM、Database 與 Model Relations

<a id="DJANGO-QUERYSET-SUBSET-ORDERING"></a>

### `[DJANGO-QUERYSET-SUBSET-ORDERING]` 分開 QuerySet 後 `order_by()` 只會喺各自 subset 入面排序

#### 問題背景

設計 vocab sync event 時，希望做到：

- CREATE：自上次 sync 後曾經 create 就通知。
- UPDATE / RESTORE / DELETE：只通知每個 vocab 最後一次非 CREATE 改動。

於是將 query 拆成兩條：

```python
create_vocab_request = VocabRequest.objects.filter(
    request_type=VocabRequestType.CREATE,
    proposed_word=vocab.word,
    proposed_kana=vocab.kana,
    status=VocabRequestStatus.APPROVED,
).order_by("-update_at").first()

other_vocab_request = VocabRequest.objects.filter(
    proposed_word=vocab.word,
    proposed_kana=vocab.kana,
    status=VocabRequestStatus.APPROVED,
).exclude(
    request_type=VocabRequestType.CREATE
).order_by("-update_at").first()
```

初初以為外層 `Vocab.objects.filter(update_at__gt=last_sync)` 已經保證 vocab 係新近改過，所以 create query 唔需要再加 `update_at__gt=last_sync`。

#### 研究方向

- QuerySet filter 後嘅資料集合係點樣決定。
- `order_by("-update_at").first()` 係喺全體資料排序，定係只喺目前 QuerySet subset 排序。
- 點解拆開 CREATE / non-CREATE query 後，要分別考慮各自 sync window。
- 點樣避免舊 CREATE request 被新 UPDATE 觸發後再次算成 CREATE notification。

#### Codex 解答

##### 1. `order_by()` 只會排序目前 QuerySet

呢句：

```python
create_vocab_request = VocabRequest.objects.filter(
    request_type=VocabRequestType.CREATE,
    proposed_word=vocab.word,
    proposed_kana=vocab.kana,
    status=VocabRequestStatus.APPROVED,
).order_by("-update_at").first()
```

意思係：

```text
先篩出 approved CREATE requests
再喺呢批 CREATE requests 入面按 update_at 排序
最後攞最新一筆 CREATE request
```

佢唔會理同一個 vocab 有無更新嘅 UPDATE / RESTORE / DELETE request。

因為 UPDATE / RESTORE / DELETE 一開始已經被：

```python
request_type=VocabRequestType.CREATE
```

排除咗。

##### 2. 外層 vocab 新，不代表內層 create request 新

例如：

```text
7/1  CREATE request approved
     Vocab A created

7/10 user sync
     user.profile.last_vocab_sync_at = 7/10

7/14 UPDATE request approved
     Vocab A updated
```

外層 query：

```python
Vocab.objects.filter(update_at__gt=last_sync)
```

會拎到 `Vocab A`，因為佢 7/14 update 過。

但 create query：

```python
VocabRequest.objects.filter(
    request_type=VocabRequestType.CREATE,
    proposed_word=vocab.word,
    proposed_kana=vocab.kana,
    status=VocabRequestStatus.APPROVED,
).order_by("-update_at").first()
```

仍然會搵到 7/1 嗰筆 CREATE request。

如果無再加：

```python
update_at__gt=last_sync
```

就會將 7/1 嘅舊 CREATE request 當成今次 sync 要通知嘅 create event。

##### 3. 兩層 filter 嘅責任唔同

外層 vocab filter：

```python
Vocab.objects.filter(update_at__gt=last_sync)
```

負責決定：

```text
邊啲 vocab 自上次 sync 後有變化，需要檢查
```

內層 request filter：

```python
VocabRequest.objects.filter(update_at__gt=last_sync)
```

負責決定：

```text
邊啲 request 係自上次 sync 後發生，可以代表今次 sync window 入面嘅事件
```

呢兩個條件唔係重複，而係控制唔同資料集合。

##### 4. 修正方向

CREATE query 應該限制喺今次 sync window：

```python
create_vocab_request = VocabRequest.objects.filter(
    request_type=VocabRequestType.CREATE,
    proposed_word=vocab.word,
    proposed_kana=vocab.kana,
    status=VocabRequestStatus.APPROVED,
    update_at__gt=last_sync,
).order_by("-update_at").first()
```

non-CREATE query 亦應該限制喺今次 sync window：

```python
other_vocab_request = VocabRequest.objects.filter(
    proposed_word=vocab.word,
    proposed_kana=vocab.kana,
    status=VocabRequestStatus.APPROVED,
    update_at__gt=last_sync,
).exclude(
    request_type=VocabRequestType.CREATE
).order_by("-update_at").first()
```

咁就可以表達：

```text
CREATE = 自上次 sync 後曾經 create
UPDATE / RESTORE / DELETE = 自上次 sync 後最後一次非 CREATE 改動
```

##### 5. 重點

```text
filter() 決定資料集合
order_by() 只會排序呢個集合
first() 只會攞呢個集合排序後第一筆
```

如果拆開兩條 QuerySet，每條 QuerySet 都要自己帶齊時間範圍、狀態、類型等條件。

唔可以假設外層 query 已經幫內層 query 限制咗所有語意。

#### 理解內容

-

<a id="DJANGO-QUERYSET-EXCLUDE-RECENT-IDS"></a>

### `[DJANGO-QUERYSET-EXCLUDE-RECENT-IDS]` 由原本 queryset 排除最近問過嘅 vocab

#### 問題背景

Quiz 出題想避免太快重複問返最近問過嘅字。

一開始容易諗成直接：

```python
filtered_qs.order_by("-last_quiz_at")[10:]
```

但呢個寫法有兩個容易混亂嘅位：

- `last_quiz_at=None` 嘅新字喺唔同 database 排序行為可能唔同。
- 如果先將 `last_quiz_at__isnull=False` 分出嚟再直接用，可能會唔小心令未問過嘅新字消失。

#### 研究方向

- `NULL` datetime 排序喺唔同 database 入面可能有咩差異。
- 點樣只排除「最近問過嘅 10 隻字」，而唔影響未問過嘅字。
- `values_list("id", flat=True)` 點樣用嚟做第二段 query 嘅 exclude 條件。
- `exclude(id__in=...)` 同直接 slice queryset 有咩語意分別。

#### 你的解答

比較清楚嘅做法係分兩步：

第一步，先由目前已經套好 user / in_use / type / level / category filter 嘅 `filtered_qs` 入面，搵出「有 `last_quiz_at` 而且最近問過」嘅 10 個 id：

```python
recently_quizzed_ids = (
    filtered_qs
    .filter(last_quiz_at__isnull=False)
    .order_by("-last_quiz_at")
    .values_list("id", flat=True)[:10]
)
```

第二步，再由原本完整嘅 `filtered_qs` 入面抽走呢 10 個 id：

```python
filtered_qs = filtered_qs.exclude(id__in=recently_quizzed_ids)
```

重點係最後用返原本嘅 `filtered_qs.exclude(...)`，而唔係只用 `last_quiz_at__isnull=False` 嗰個 queryset。

所以結果係：

- 未問過嘅字：`last_quiz_at=None`，唔會入 `recently_quizzed_ids`，會保留。
- 問過但唔係最近 10 隻：會保留。
- 最近問過 10 隻：會暫時抽走，避免太快重複出題。

#### 我的理解

即係先喺 `filtered_qs` 入面搵有 `last_quiz_at` 嘅最新 10 個 id 出嚟，再由原本 `filtered_qs` 入面抽走呢 10 個。

呢個理解重點係：「搵最近 10 個」只係用嚟建立排除名單，真正出題 pool 仍然係原本嗰個 `filtered_qs` 減走最近 10 個。

<a id="DJANGO-QUERYSET-VALUES-LIST-PERFORMANCE"></a>

### `[DJANGO-QUERYSET-VALUES-LIST-PERFORMANCE]` QuerySet `values_list()` 同避免重複 SQL

#### 問題背景

Quiz weighted random 抽題時，最初做法係：

```python
if queryset.count() == 0:
    return None

vocab_list = list(queryset)
```

呢個寫法清楚，但會有兩個成本：

1. `queryset.count()` 會打一個 SQL 問 database 有幾多 row。
2. `list(queryset)` 又會再打一個 SQL，並將完整 model objects 拉入 Python。

如果最後只需要 `id` 同 `weight` 去抽題，拉完整 `UserVocab` object 其實多咗。

#### 研究方向

- QuerySet 幾時真正打 SQL。
- `count()`、`exists()`、`list(queryset)` 分別會觸發咩查詢。
- `values_list("id", "weight")` 同完整 model object 嘅差異。
- 先將必要欄位拉成 Python list，再喺 memory 入面做計算，適合咩場景。

#### 我的理解

可以改成一次過只拉需要嘅欄位：

```python
weight_rows = list(queryset.values_list("id", "weight"))

if not weight_rows:
    return None
```

`weight_rows` 會係一個 tuple list，例如：

```python
[
    (12, 5),
    (18, 20),
    (25, 3),
]
```

所以之後 loop 時唔可以再寫：

```python
for user_vocab in weight_rows:
    total_weight += user_vocab.weight
```

因為 `user_vocab` 已經唔係 `UserVocab` object，而係 tuple。

正確方向係拆開 tuple：

```python
for user_vocab_id, weight in weight_rows:
    total_weight += weight
    cumulative_weight.append(total_weight)
```

最後抽中 index 後，直接回傳 tuple 入面第 0 個值：

```python
return weight_rows[index][0]
```

#### 重點

- `count()` 只係問 database 數量。
- `list(queryset)` 會真正拉資料。
- 如果本身都要拉資料，就可以用 `if not list_data` 判斷有冇資料，未必需要先 `.count()`。
- `values_list()` 適合用喺「只需要少數欄位」嘅情況。
- `values_list("id", "weight")` 回傳 tuple，不再係 model object。

#### 理解內容

-

<a id="DJANGO-RELATION-FIELD-RELATED-NAME"></a>

### `[DJANGO-RELATION-FIELD-RELATED-NAME]` Relation 應該用 field name 定 `related_name`

#### 問題背景

目前 `Vocab`、`User` 同 `UserVocab` 之間使用帶有 through model 嘅 Many-to-Many relationship：

```python
class Vocab(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="UserVocab",
        related_name="vocabs",
    )


class UserVocab(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_vocab",
        on_delete=models.CASCADE,
    )
    vocab = models.ForeignKey(
        Vocab,
        related_name="user_vocab",
        on_delete=models.CASCADE,
    )
```

未完全理解由 `Vocab` 取得 users 或 `UserVocab` records 時，應該使用 model field name 定係 `related_name`。

#### 研究方向

- 正向 relation 同 reverse relation 有咩分別。
- 乜嘢情況使用 field name。
- 乜嘢情況使用 `related_name`。
- `vocab.users` 同 `vocab.user_vocab` 回傳嘅 object type 有咩不同。
- Through model 額外 fields，例如 `weight` 同 `streak`，應該經邊條 relation 取得。
- ORM filter 入面 relation name 點樣使用。

#### 概念整理與解答

##### 1. 核心規則

可以先記住：

```text
由定義 relation field 嗰邊出發
-> 使用 field name

由被指向嘅 model 反方向行返去
-> 使用 related_name
```

例如：

```python
class UserVocab(models.Model):
    vocab = models.ForeignKey(
        Vocab,
        related_name="user_vocab",
    )
```

`vocab` field 定義喺 `UserVocab`：

```python
user_vocab.vocab
```

由 `Vocab` 反方向取得相關 `UserVocab`，就使用 `related_name`：

```python
vocab.user_vocab.all()
```

##### 2. 由 `Vocab` 直接取得 users

`users` field 直接定義喺 `Vocab`：

```python
class Vocab(models.Model):
    users = models.ManyToManyField(...)
```

所以由一個 vocab object 出發，可以直接用 field name：

```python
users = vocab.users.all()
```

回傳嘅係 `User` QuerySet：

```text
Vocab
-> users field
-> User objects
```

即使呢個 Many-to-Many 使用 `through="UserVocab"`，讀取相關 users 時仍然可以使用 `vocab.users.all()`。

##### 3. 由 `Vocab` 取得 `UserVocab` records

如果需要中間表資料，例如：

- `weight`
- `correct_count`
- `incorrect_count`
- `streak`
- `last_quiz_at`

就唔應該只取 `User` object，而係要取得 `UserVocab` records：

```python
user_vocab_records = vocab.user_vocab.all()
```

呢個 `user_vocab` 來自：

```python
UserVocab.vocab.related_name
```

回傳嘅係 `UserVocab` QuerySet：

```python
for user_vocab in vocab.user_vocab.select_related("user"):
    print(user_vocab.user)
    print(user_vocab.weight)
    print(user_vocab.streak)
```

`select_related("user")` 可以喺同一個 query 一併取得每筆 record 對應嘅 user，避免 loop 時逐筆再查 database。

##### 4. 由 `UserVocab` 取得兩邊 object

`user` 同 `vocab` 都係直接定義喺 `UserVocab` 嘅 fields，所以使用 field name：

```python
user_vocab.user
user_vocab.vocab
```

呢度唔使用 `related_name`，因為行緊嘅係正向 relation。

##### 5. 由 `User` 反方向取得資料

`Vocab.users` 設定：

```python
related_name="vocabs"
```

所以由 user 取得相關 vocabs：

```python
user.vocabs.all()
```

回傳 `Vocab` QuerySet。

而 `UserVocab.user` 設定：

```python
related_name="user_vocab"
```

所以由 user 取得中間表 records：

```python
user.user_vocab.all()
```

回傳 `UserVocab` QuerySet。

兩者分別係：

```text
user.vocabs.all()
-> Vocab objects

user.user_vocab.all()
-> UserVocab objects
```

##### 6. 目前 model 嘅 relation 對照

| 起點 | 寫法 | 結果 |
| --- | --- | --- |
| `Vocab` | `vocab.users.all()` | `User` QuerySet |
| `Vocab` | `vocab.user_vocab.all()` | `UserVocab` QuerySet |
| `User` | `user.vocabs.all()` | `Vocab` QuerySet |
| `User` | `user.user_vocab.all()` | `UserVocab` QuerySet |
| `UserVocab` | `user_vocab.user` | 單一 `User` object |
| `UserVocab` | `user_vocab.vocab` | 單一 `Vocab` object |

##### 7. ORM filter 嘅例子

直接查 through model：

```python
UserVocab.objects.filter(vocab=vocab)
UserVocab.objects.filter(user=user)
```

由 vocab 篩選 users：

```python
vocab.users.filter(is_active=True)
```

由 user 篩選 vocabs：

```python
user.vocabs.filter(is_active=True)
```

由 `Vocab` QuerySet 根據中間表資料篩選：

```python
Vocab.objects.filter(
    user_vocab__user=user,
    user_vocab__weight__gte=50,
)
```

ORM lookup 使用雙底線 `__` 穿過 relation：

```text
user_vocab__user
-> 經 Vocab reverse related_name 去 UserVocab
-> 再使用 UserVocab.user field
```

##### 8. 今次問題嘅直接答案

如果目標只係由 vocab 取得 users：

```python
vocab.users.all()
```

如果要同時使用 `UserVocab` 入面嘅 quiz data：

```python
vocab.user_vocab.select_related("user")
```

所以唔係永遠只用 field name，亦唔係永遠只用 `related_name`；要睇 relation field 定義喺起點 model，定係由另一邊反向查詢。

#### 理解內容

-

<a id="DJANGO-UNIQUE-CONSTRAINT"></a>

### `[DJANGO-UNIQUE-CONSTRAINT]` `UniqueConstraint` 同 conditional unique constraint

#### 問題背景

目前 `Vocab` 同 `VocabRequest` 使用 database constraints 防止重複資料：

```python
models.UniqueConstraint(
    fields=["word", "kana"],
    name="word_kana_unique",
)
```

`VocabRequest` 亦使用帶有 `condition=Q(...)` 嘅 conditional unique constraints，只限制符合特定狀態嘅 records。

#### 研究方向

- `UniqueConstraint` 同 field 上嘅 `unique=True` 有咩分別。
- 多個 fields 放入同一個 constraint 代表咩。
- `condition=Q(...)` 點樣令 unique rule 只套用喺部分 records。
- 點解 service 已經用 `.exists()` 檢查，database 仍然需要 constraint。
- Constraint 觸發時點解會出現 `IntegrityError`。
- SQLite 同 PostgreSQL 對 conditional unique constraint 嘅支援有咩差異。

#### 概念整理與解答

##### 1. 普通 `UniqueConstraint`

`UniqueConstraint` 會由 database 保證指定欄位組合唔可以重複：

```python
models.UniqueConstraint(
    fields=["word", "kana"],
    name="word_kana_unique",
)
```

呢個 constraint 唔代表 `word` 同 `kana` 各自都必須 unique，而係兩個值嘅組合必須 unique。

例如以下 records 可以同時存在：

```text
word="生", kana="せい"
word="生", kana="なま"
```

因為 `(word, kana)` 組合唔同。

但以下組合只可以存在一次：

```text
word="犬", kana="いぬ"
```

##### 2. 同 `unique=True` 嘅分別

單一 field 可以直接使用：

```python
email = models.EmailField(unique=True)
```

如果 uniqueness 涉及多個 fields、需要條件，或者想明確命名 constraint，就使用 model `Meta.constraints`：

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["word", "kana"],
            name="word_kana_unique",
        ),
    ]
```

##### 3. Conditional unique constraint

Conditional unique constraint 只會限制符合 `condition` 嘅 records：

```python
models.UniqueConstraint(
    fields=["original_vocab"],
    condition=Q(
        status=VocabRequestStatus.PENDING,
        original_vocab__isnull=False,
    ),
    name="unique_pending_vocab_request_on_other",
)
```

意思係：

- Request status 必須係 `PENDING`。
- `original_vocab` 必須有值。
- 符合以上條件時，同一個 `original_vocab` 最多只可以有一個 request。

所以同一個 vocab 可以保留多筆已完成嘅歷史 requests：

```text
original_vocab=10, status="approved"
original_vocab=10, status="rejected"
```

但同一時間只可以有一筆：

```text
original_vocab=10, status="pending"
```

##### 4. Create request 使用嘅 constraint

Create request 未有 `original_vocab`，所以使用 proposed data 判斷重複：

```python
models.UniqueConstraint(
    fields=["proposed_word", "proposed_kana"],
    condition=Q(
        status=VocabRequestStatus.PENDING,
        original_vocab__isnull=True,
    ),
    name="unique_pending_vocab_request_on_create",
)
```

意思係當 request：

- status 係 `PENDING`
- `original_vocab` 係 `NULL`

相同嘅 `(proposed_word, proposed_kana)` 最多只可以有一筆。

Approved 或 rejected request 唔再符合條件，因此唔會阻止將來為相同字建立新 request。

##### 5. `Q()` 係咩

`Q()` 用嚟表示 database query condition：

```python
Q(
    status=VocabRequestStatus.PENDING,
    original_vocab__isnull=False,
)
```

同一個 `Q()` 入面多個 keyword arguments 預設以 `AND` 連接，大致等於：

```text
status = "pending"
AND original_vocab IS NOT NULL
```

`Q()` 亦可以使用：

```python
Q(condition_a) | Q(condition_b)  # OR
Q(condition_a) & Q(condition_b)  # AND
~Q(condition_a)                  # NOT
```

##### 6. 點解 `.exists()` 之後仍需要 constraint

Service 可以先檢查：

```python
VocabRequest.objects.filter(...).exists()
```

呢個檢查可以提早提供清楚嘅 user feedback，但唔可以完全阻止 concurrency race condition。

例如兩個 requests 幾乎同時執行：

```text
Request A check：不存在 pending request
Request B check：不存在 pending request
Request A create
Request B create
```

如果只有 application check，兩筆都可能成功。

Database constraint 會喺真正寫入時再次保證規則。第二筆寫入違反 constraint 時，database 會拒絕並令 Django 拋出 `IntegrityError`。

所以兩者分工係：

```text
Application check
-> 提供較早、較清楚嘅 feedback

Database constraint
-> 處理 concurrency，保證資料最終一致性
```

##### 7. Migration 同 database 支援

新增或修改 constraint 後，需要建立及套用 migration：

```bash
python manage.py makemigrations
python manage.py migrate
```

Conditional unique constraint 會依賴 database 對 partial unique index 嘅支援。SQLite 新版本同 PostgreSQL 支援呢種設計，但實際部署前仍應以目標 database 測試 constraint 行為。

#### 理解內容

-

<a id="DJANGO-CATCH-INTEGRITY-ERROR-AROUND-ATOMIC"></a>

### `[DJANGO-CATCH-INTEGRITY-ERROR-AROUND-ATOMIC]` 點解要喺 `transaction.atomic()` 外面捕捉 `IntegrityError`

#### 問題背景

建立 `UserVocab` 時可能因為 unique constraint 或其他 database constraint 而出現 `IntegrityError`。

未理解點解建議寫成：

```python
try:
    with transaction.atomic():
        UserVocab.objects.create(...)
except IntegrityError:
    ...
```

而唔係只用 `try` 包住：

```python
with transaction.atomic():
    try:
        UserVocab.objects.create(...)
    except IntegrityError:
        ...
```

#### 研究方向

- `transaction.atomic()` 點樣判斷應該 commit 定 rollback。
- Database error 發生後，transaction 點解會進入 broken state。
- 點解 exception 要穿過 atomic context manager。
- `TransactionManagementError` 通常喺咩情況出現。
- 如果只得單一 `objects.create()`，仲需唔需要額外使用 `atomic()`。

#### 概念整理與解答

##### 1. `atomic()` 需要見到 exception

`with transaction.atomic():` 係一個 context manager。離開區塊時，佢會根據有冇 exception 決定：

```text
正常離開 atomic block
-> commit

有 exception 穿過 atomic block
-> rollback
```

因此建議寫法係：

```python
try:
    with transaction.atomic():
        UserVocab.objects.create(
            user=user,
            vocab=vocab,
        )
except IntegrityError:
    # atomic 已經完成 rollback
    ...
```

執行次序係：

```text
objects.create() 觸發 IntegrityError
-> exception 離開 atomic block
-> atomic 知道操作失敗
-> rollback transaction/savepoint
-> 離開 atomic 後由 except 處理
```

##### 2. Catch 喺 atomic 入面有咩問題

唔建議：

```python
with transaction.atomic():
    try:
        UserVocab.objects.create(
            user=user,
            vocab=vocab,
        )
    except IntegrityError:
        pass
```

`IntegrityError` 係 database error。發生後，Django 會將目前 transaction 標記成需要 rollback，即係 broken transaction。

但 `except` 喺 atomic block 入面將 exception 吞咗，atomic context manager 無法由正常 Python exception flow 清楚見到原本錯誤。

更重要嘅係，喺 rollback 發生之前繼續查 database：

```python
with transaction.atomic():
    try:
        UserVocab.objects.create(...)
    except IntegrityError:
        UserVocab.objects.filter(...).exists()
```

可能出現：

```text
TransactionManagementError
```

因為目前 transaction 已經 broken，Django 唔容許喺 rollback 前繼續執行 database queries。

##### 3. `except` 放喺外面嘅安全邊界

```python
try:
    with transaction.atomic():
        UserVocab.objects.create(...)
except IntegrityError:
    already_exists = UserVocab.objects.filter(...).exists()
```

去到 `except` 時：

- 已經離開 atomic block。
- Django 已經 rollback。
- Transaction 唔再處於 broken state。
- 可以安全執行新 query、顯示訊息或記錄 log。

所以 `try` 包住 `atomic()` 唔只係寫法偏好，而係將 error handling 放喺 rollback 完成之後。

##### 4. 如果 atomic 入面有多個操作

例如：

```python
try:
    with transaction.atomic():
        user_vocab = UserVocab.objects.create(...)
        create_quiz_history(user_vocab)
        update_user_stats(user)
except IntegrityError:
    ...
```

任何一步出現 `IntegrityError`，整個 atomic block 都會 rollback，避免只完成其中一部分。

如果 `try` 只包住 `objects.create()`，就容易令 error handling 同 transaction boundary 分開，之後新增第二、第三個 database operation 時亦較容易漏咗 rollback 範圍。

##### 5. 只有一個 `objects.create()` 時

Django 預設使用 autocommit。單一 SQL statement 失敗時，database 本身唔會保存嗰次失敗寫入。

所以如果真係只有：

```python
try:
    UserVocab.objects.create(...)
except IntegrityError:
    ...
```

通常已經可以安全捕捉單一 create 嘅 constraint error，未必需要額外 `atomic()`。

但如果呢個 service operation 代表一個完整業務動作，之後可能加入多個 database writes，保留 atomic transaction 會令邊界更清楚。

##### 6. 逐筆 transaction 同整批 transaction

逐筆建立：

```python
for vocab in vocabs:
    try:
        with transaction.atomic():
            UserVocab.objects.create(user=user, vocab=vocab)
    except IntegrityError:
        continue
```

每個 vocab 獨立成功或 rollback。某一筆失敗，之前成功嘅 records 會保留。

整批建立：

```python
try:
    with transaction.atomic():
        for vocab in vocabs:
            UserVocab.objects.create(user=user, vocab=vocab)
except IntegrityError:
    ...
```

任何一筆失敗，成批 records 全部 rollback。

應該選擇邊種方式，取決於業務要求係「可以部分成功」定「必須全部成功」。

##### 7. `transaction.on_commit()`：commit 成功後先做 side effect

`transaction.on_commit()` 用嚟註冊一個 callback：

```python
transaction.on_commit(callback)
```

意思係：

- 如果目前 transaction 成功 commit，callback 先會執行。
- 如果 transaction rollback，callback 唔會執行。

呢個適合處理「主 database 操作成功後先做」嘅 side effect，例如：

- 建立 notification / event
- 發 email
- call external API
- 更新 cache
- 寫非核心 log

例如 vocab request rejected 後先建立 event：

```python
with transaction.atomic():
    locked_request = (
        VocabRequest.objects
        .select_for_update()
        .get(pk=vocab_request.pk)
    )

    if locked_request.status != VocabRequestStatus.PENDING:
        return False

    locked_request.status = VocabRequestStatus.REJECTED
    locked_request.reviewed_by = reviewed_by
    locked_request.save(
        update_fields=["status", "reviewed_by", "update_at"]
    )

    if locked_request.created_by is not None:
        user = locked_request.created_by
        request_type = locked_request.request_type

        def create_reject_event():
            event = EventService.create_event(
                event_type=EventType.VOCAB_REQUEST_RESULT,
                event_title=(
                    f"Your {request_type} vocab request "
                    f"has been rejected by {reviewed_by}"
                ),
                event_msg="",
            )
            EventService.assign_event_to_user(
                event=event,
                user=user,
            )

        transaction.on_commit(create_reject_event)
```

重點係 callback 入面嘅 code 會等 `with transaction.atomic()` 成功完成後先執行。

如果中途 rollback，例如 save request status 失敗，event 就唔會建立，避免出現「通知話 rejected，但 request 其實無成功 rejected」嘅不一致。

###### 點解先存 local variables

例子入面先存：

```python
user = locked_request.created_by
request_type = locked_request.request_type
```

因為 `on_commit()` callback 係之後先執行。先將需要嘅資料存入 local variables，會比 callback 入面再依賴 `locked_request` object 清楚。

###### callback 要帶參數時點寫

`transaction.on_commit()` 需要接收一個「之後可以直接執行」嘅 callback。

即係：

```python
transaction.on_commit(callback)
```

`callback` 本身唔應該喺呢一刻需要你再傳參數。

如果想抽 helper，例如：

```python
def create_event_for_admin(*, word, kana, request_type):
    ...
```

就有三種常見寫法。

第一種：用 `lambda` 包一層。

```python
transaction.on_commit(
    lambda: create_event_for_admin(
        word=word,
        kana=kana,
        request_type=request_type,
    )
)
```

意思係：交俾 `on_commit()` 嘅係一個無參數 function，但呢個 function 執行時會 call 真正 helper 並帶入參數。

第二種：用 inner function。

```python
def create_event_after_commit():
    create_event_for_admin(
        word=word,
        kana=kana,
        request_type=request_type,
    )

transaction.on_commit(create_event_after_commit)
```

呢個同 `lambda` 概念一樣，但如果 callback 內容多過一行，inner function 會清楚好多。

第三種：用 `functools.partial`。

```python
from functools import partial

transaction.on_commit(
    partial(
        create_event_for_admin,
        word=word,
        kana=kana,
        request_type=request_type,
    )
)
```

`partial()` 會預先幫 function 塞好參數，產生一個之後可以直接呼叫嘅 callback。

簡單選擇：

- Callback 只得一行：`lambda` 可以接受。
- Callback 有幾行 logic：用 inner function。
- 想明確表達「預先綁定參數」：用 `partial`。

目前 project 學習階段，inner function 最易讀。

###### 放 transaction 入面、出面、on_commit 嘅分別

放喺 `transaction.atomic()` 入面：

- Event failure 會令主操作 rollback。
- 適合 event 係核心業務資料，缺少 event 就唔應該完成主操作。

放喺 `transaction.atomic()` 出面：

- 主操作成功後，即使 event failure，主操作都已經保留。
- 但如果主操作 rollback，而你太早建立 event，就可能出現假通知。

用 `transaction.on_commit()`：

- 主操作 commit 成功先建立 event。
- 主操作 rollback 就唔建立 event。
- Event failure 唔會 rollback 已經 commit 嘅主操作。

所以 notification / event 呢類 side effect，通常 `on_commit()` 係最平衡嘅選擇。

##### 8. 最簡單記法

```text
預計捕捉 database error
-> try 放喺 atomic 外面

原因
-> 先讓 atomic 見到 exception 並 rollback
-> rollback 完成後先處理 error
```

推薦結構：

```python
try:
    with transaction.atomic():
        # database operations
        transaction.on_commit(callback)
except IntegrityError:
    # rollback 已完成
    # safe error handling
```

#### 理解內容

-

<a id="DJANGO-PRIMARY-SYNC-EVENT-TRANSACTION-BOUNDARY"></a>

### `[DJANGO-PRIMARY-SYNC-EVENT-TRANSACTION-BOUNDARY]` 主操作、vocab sync 同 event 應該點分 transaction

#### 問題背景

Register、login 同 user detail flow 會順便執行：

```text
主要操作
-> sync vocab 去 UserVocab
-> 建立 vocab sync event 並 assign 俾 user
-> 更新 event checkpoint
```

業務決定係：

- Vocab sync 失敗：保留主要操作，記錄 log，今次停止；下次再 sync。
- Sync 成功但 event 失敗：保留 sync，只 rollback 今次 event 相關操作並記錄 log。
- Admin approve／reject 同結果 event：視為同一個完整操作，任何一步失敗就一齊 rollback。

因此，以下寫法唔符合「sync 成功後要保留」嘅要求：

```python
with transaction.atomic():
    UserVocabService.sync_new_vocab(user=user)
    EventService.gen_vocab_sync_event(user=user)
```

因為 event 一旦失敗，外層 transaction 會連已完成嘅 vocab sync 一齊 rollback。

#### 研究方向

- Transaction boundary 應該跟技術 function 分，定係跟業務上「要一齊成功／失敗」嘅單位分。
- 點樣保留可重試嘅 vocab sync，同時防止 event 只建立一半。
- 點解 sync 失敗後唔應繼續產生「sync 成功」event。
- 點樣避免 Register、Login、User detail 三個 View 重複 try／except 同 logging。

#### 概念整理與解答

##### 1. Transaction boundary 由業務結果決定

`transaction.atomic()` 入面嘅 database writes 會一齊 commit 或 rollback。因此，只有「必須一齊成功」嘅操作先應放入同一個 atomic block。

今次三層操作嘅關係係：

| 操作 | 失敗時點處理 | 原因 |
|---|---|---|
| Register／login／user detail | 保留 | 呢啲係主要操作 |
| Vocab sync | 記 log，等下次重試 | Sync 可由目前 database 狀態重新計算 |
| Event 建立、assign、checkpoint | 一組 rollback | 避免 event 建立一半或 checkpoint 錯誤前移 |

所以唔應該用一個大 transaction 包住 sync 同 event。

##### 2. 建議由共用 orchestration function 控制流程

概念寫法：

```python
import logging

logger = logging.getLogger(__name__)


def sync_vocab_and_generate_event_safely(*, user):
    try:
        UserVocabService.sync_new_vocab(user=user)
    except Exception:
        logger.exception(
            "Vocab sync failed",
            extra={"user_id": user.pk},
        )
        return

    try:
        EventService.gen_vocab_sync_event(user=user)
    except Exception:
        logger.exception(
            "Vocab sync event generation failed",
            extra={"user_id": user.pk},
        )
```

執行結果：

```text
sync 失敗
-> 記 log
-> return
-> 唔會建立錯誤嘅成功 event

sync 成功、event 失敗
-> sync 已保留
-> event 自己 rollback
-> 記 log
```

共用 function 可以避免三個 View 各自複製相同 error handling。Register flow 傳新建立嘅 user；login 同 user detail flow 傳目前登入 user。

##### 3. Event service 自己擁有 atomic boundary

Event generation 可能包含多個 database writes：

```text
建立一個或多個 Event
-> 建立 UserEvent assignment
-> 更新 last_vocab_sync_at checkpoint
```

呢幾步應該係同一組：

```python
class EventService:
    @staticmethod
    @transaction.atomic
    def gen_vocab_sync_event(*, user):
        # create event rows
        # assign events to user
        # update last_vocab_sync_at
        ...
```

如果中途任何一步失敗，event rows、assignments 同 checkpoint 全部 rollback。外層 orchestration function 喺 atomic 結束並完成 rollback 後先捕捉 exception 同記 log。

如果 event service 無自己嘅 atomic boundary，可能出現：

```text
第一個 event 已建立
-> 第二個 event／assignment 失敗
-> checkpoint 未更新
-> 下次重試又重新建立第一個 event
```

結果可能係 orphan event、部分通知或重複 event。

##### 4. 點解 vocab sync 適合失敗後重試

目前 sync 思路係計算 user 尚未擁有嘅 vocab，再建立欠缺嘅 `UserVocab`；database 亦應用 `(user, vocab)` unique constraint 防止同一配對重複。配合 `bulk_create(..., ignore_conflicts=True)`，重試通常只會補回仍然欠缺嘅 records。

不過「可重試」唔代表可以忽略所有錯誤。仍然要用 `logger.exception()` 保存 traceback，否則 database、程式或資料問題可能長期被靜默跳過。

##### 5. Admin approve／reject 係另一種業務要求

Approve／reject status 同結果 event 已決定要一齊成功，所以應保留同一個 transaction：

```python
with transaction.atomic():
    update_request_status(...)
    create_or_update_vocab_if_needed(...)
    create_result_event(...)
    assign_event_to_user(...)
```

Event failure 時，status change 亦 rollback。呢個同 login／register 嘅附帶 vocab sync event 唔同，唔應套用同一個「記 log 後保留主要操作」政策。

##### 6. 最簡單記法

```text
要一齊成功／失敗
-> 放同一個 transaction

附帶流程失敗都要保留主要操作
-> 分開 transaction boundary，再記 log

後一步依賴前一步成功
-> 前一步失敗就立即停止，唔好繼續製造成功 event
```

以上係建議實作方向；正式完成仍要檢查三個 View 已改用共用 orchestration、event service 已有 atomic boundary，並用 failure-path tests 驗證 rollback 範圍。

#### 理解內容

-

<a id="DJANGO-POST-SAVE-SIGNAL-CREATED-GET-OR-CREATE"></a>

### `[DJANGO-POST-SAVE-SIGNAL-CREATED-GET-OR-CREATE]` `post_save` signal、`created` 同 `get_or_create()`

#### 問題背景

想做到 create user 時自動建立對應嘅 `UserProfile`。

如果只係喺 registration view 入面手動 create profile，admin create user、management command create user、test data create user 呢啲入口就可能會漏。

所以可以考慮用 Django `post_save` signal，喺 User save 完之後自動補返 profile。

#### 研究方向

- `post_save` 會喺 create 同 update 時都觸發。
- Signal callback 入面嘅 `created` 參數點樣分辨今次係新建 object 定更新 object。
- `get_or_create()` 點樣避免重複 create profile。
- Signal 適合處理「每次 user 建立後都應該存在」嘅 companion model。

#### 你的解答

`post_save` signal 會喺 model `save()` 完成後觸發。對 User 嚟講，create user 同 update user 都會觸發同一個 signal。

Django 會傳一個 `created` boolean 入 signal receiver：

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
```

`created=True` 代表今次係新建 User。

`created=False` 代表今次係更新已存在 User。

所以如果寫咗 `if created:`，update user 時 signal 雖然會觸發，但唔會入去 create profile。

`get_or_create()` 係第二層保險。即使 profile 已經存在，佢都只會拎返現有 object，而唔會再 create 多一個。

如果想「舊 user 如果無 profile，之後 update user 時都自動補返」，可以唔加 `if created`，每次 save 都 `get_or_create()`。不過一般做法係 create 時建立 profile，舊資料另外用 management command 或 migration 去補。

#### 理解內容

- `post_save` 唔等於只係 create 後觸發；update save 都會觸發。
- `created` 先係判斷「今次係 create 定 update」嘅關鍵。
- `if created: get_or_create(...)` 係常見穩陣寫法。
- Signal 適合防止多個 create user 入口漏做 profile creation。

<a id="GROUP-AJAX-JAVASCRIPT-PARTIAL-UI"></a>

## Ajax、JavaScript 與 Partial UI

<a id="JS-PARTIAL-REPLACE-EVENT-BINDING"></a>

### `[JS-PARTIAL-REPLACE-EVENT-BINDING]` Ajax partial replace 後 event listener 點樣處理

#### 問題背景

`UserVocabListView` 拆成 main template + partial template 後，Ajax pagination 會用：

```javascript
container.innerHTML = html;
```

替換 list 區域。  
問題係 partial 入面原本嘅 checkbox、select all、pagination links 都會變成新 DOM。舊 DOM 上面綁過嘅 event listener 會消失。

今次試咗將 checkbox setup logic 包成 function，喺 initial page load 同 Ajax replace 後都 call 一次，結果可以 work。

#### 研究方向

- 點解 `innerHTML = html` 之後舊 event listener 會失效。
- 用 function 包住重新 bind event 是否正路。
- Event delegation 係咩，點解可以避免每次 replace 後重新 bind。
- 什麼時候值得用 HTMX / Alpine.js 呢類小工具。
- 邊種做法最適合目前 project 階段。

#### 概念整理與解答

##### 1. 方法一：replace 完再 call setup function

目前做法概念：

```javascript
function selectorReload() {
    const selectAll = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".in-use-checkbox");

    selectAll.addEventListener("change", function () {
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = selectAll.checked;
        });
    });

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            // update select-all state
        });
    });
}

selectorReload();

// after Ajax replace
container.innerHTML = html;
selectorReload();
```

呢個做法係正路，因為：

- `innerHTML = html` 會建立一批新 DOM elements。
- 舊 checkbox 已經被移除，舊 listener 跟住消失。
- replace 完重新 call setup function，就可以幫新 checkbox bind event。

建議加 guard，避免 partial 暫時冇 checkbox 時 JS 爆：

```javascript
function selectorReload() {
    const selectAll = document.getElementById("select-all");
    if (!selectAll) return;

    const checkboxes = document.querySelectorAll(".in-use-checkbox");
    // bind events...
}
```

優點：

- 直覺、易明、易 debug。
- 適合目前自己手寫 Django template + JavaScript 嘅階段。

缺點：

- 如果冇 replace DOM，而係對同一批 DOM 重複 call setup，可能會重複 bind listener。
- function 入面要小心 selector 是否存在。

##### 2. 方法二：Event delegation

Event delegation 係將 listener 綁喺穩定存在嘅 parent container，而唔係每次綁喺新 checkbox 上。

概念：

```javascript
const container = document.getElementById("user-vocab-list-container");

container.addEventListener("change", function (e) {
    if (e.target.id === "select-all") {
        const checkboxes = container.querySelectorAll(".in-use-checkbox");
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = e.target.checked;
        });
        updateSelectAllState();
    }

    if (e.target.classList.contains("in-use-checkbox")) {
        updateSelectAllState();
    }
});
```

因為 listener 係掛喺 `container`，而 `container` 本身冇被 replace，所以 partial 入面 checkbox 換咗都仍然可以收到事件。

`updateSelectAllState()` 入面放嘅，就係原本每個 checkbox `change` listener 入面嗰段「重新計算 All checkbox 狀態」嘅 logic。

原本做法大概係：

```javascript
checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
        const allChecked = Array.from(checkboxes).every(function (box) {
            return box.checked;
        });
        const noneChecked = Array.from(checkboxes).every(function (box) {
            return !box.checked;
        });

        selectAll.checked = allChecked;
        selectAll.indeterminate = !allChecked && !noneChecked;
    });
});
```

Event delegation 之後，可以抽成：

```javascript
function updateSelectAllState() {
    const selectAll = document.getElementById("select-all");
    if (!selectAll) return;

    const checkboxes = document.querySelectorAll(".in-use-checkbox");

    const allChecked = Array.from(checkboxes).every(function (box) {
        return box.checked;
    });

    const noneChecked = Array.from(checkboxes).every(function (box) {
        return !box.checked;
    });

    selectAll.checked = allChecked;
    selectAll.indeterminate = !allChecked && !noneChecked;
}
```

分工：

```text
select-all change
-> 將目前畫面所有 checkbox 跟住 select-all checked 狀態改變
-> 再 call updateSelectAllState()

single checkbox change
-> 不改其他 checkbox
-> 只 call updateSelectAllState() 重新計算 select-all 應該係 checked / unchecked / indeterminate
```

優點：

- partial replace 後唔需要重新 bind checkbox listeners。
- 對動態新增 / 替換 DOM 特別適合。
- pagination click handler 其實已經係用緊類似 delegation：

```javascript
container.addEventListener("click", function (e) {
    if (e.target.classList.contains("page-change")) {
        // Ajax pagination
    }
});
```

缺點：

- 對初學階段抽象少少。
- function 要小心用 `e.target` 判斷事件來源。
- 如果 DOM 結構變複雜，有時要用 `closest()` 搵真正目標。

##### 3. 方法三：用 HTMX / Alpine.js 等小工具

之後可以考慮用 HTMX 處理：

- click link 後 fetch partial。
- replace 指定 container。
- 保留 server-rendered Django template flow。

或者用 Alpine.js 管理小型互動狀態，例如 checkbox select-all。

優點：

- 少寫低層 fetch / event binding code。
- 對 partial update 呢類 server-rendered interaction 好方便。

缺點：

- 會引入新 dependency / 新概念。
- 如果未理解原生 JS flow，太早用工具可能會遮住底層原理。

##### 4. 目前建議

目前 project 階段可以先用：

```text
方法一：setup function reload
```

原因：

- 已經 work。
- 容易理解。
- 同目前 Django template + vanilla JavaScript 學習階段配合。

之後 `UserVocabListView` 穩定後，可以再嘗試 refactor 成：

```text
方法二：event delegation
```

因為 event delegation 更適合長期維護動態 partial DOM。

#### 理解內容

-

<a id="HTML-JS-CHECKBOX-SELECT-ALL"></a>

### `[HTML-JS-CHECKBOX-SELECT-ALL]` Checkbox 全選 / 全取消點樣用 JavaScript 做

#### 問題背景

`UserVocab` list 想加一個額外 checkbox，控制目前畫面所有 `selected_ids` checkbox：

- tick all：當前頁全部設為 checked
- untick all：當前頁全部設為 unchecked
- 如果部分 checked，all checkbox 顯示 indeterminate

#### 研究方向

- `id`、`class`、`name` 喺 HTML input 入面分別負責咩。
- 點樣用同一個 class group 起所有 row checkbox。
- `querySelectorAll()` 點樣一次搵晒同一 class 嘅 elements。
- checkbox 嘅 `checked` 同 `indeterminate` 狀態點樣更新。
- 「All」應該只代表當前 page / 當前 filter 顯示嘅 rows。

#### 概念整理與解答

##### 1. `name` 俾 form submit 用，`class` 俾 JavaScript group 用

每個 row checkbox 可以同時有：

```html
name="selected_ids"
class="in-use-checkbox"
```

用途：

- `name="selected_ids"`：submit POST 時俾 Django 收資料。
- `class="in-use-checkbox"`：俾 JavaScript 一次搵晒所有 row checkbox。

可以記：

- `id`：一頁通常一個，用 `getElementById()`
- `class`：一頁可以好多個，用 `querySelectorAll()`
- `name`：form submit 時用，Django 會喺 `request.POST` 收到呢個 key

##### 2. Template 例子

```django
<input type="checkbox" id="select-all">

{% for user_vocab in user_vocabs %}
    <input type="hidden" name="selectable_ids" value="{{ user_vocab.id }}">
    <input
        type="checkbox"
        class="in-use-checkbox"
        name="selected_ids"
        value="{{ user_vocab.id }}"
        {% if user_vocab.in_use %}checked{% endif %}
    >
{% endfor %}
```

`id="select-all"` 用嚟搵全選 checkbox。
`class="in-use-checkbox"` 用嚟搵所有 row checkboxes。

##### 3. JavaScript 例子

```html
<script>
document.addEventListener("DOMContentLoaded", function () {
    const selectAll = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".in-use-checkbox");

    selectAll.addEventListener("change", function () {
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = selectAll.checked;
        });
    });

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const allChecked = Array.from(checkboxes).every(function (box) {
                return box.checked;
            });

            const noneChecked = Array.from(checkboxes).every(function (box) {
                return !box.checked;
            });

            selectAll.checked = allChecked;
            selectAll.indeterminate = !allChecked && !noneChecked;
        });
    });
});
</script>
```

##### 4. 點解要用 `querySelectorAll(".in-use-checkbox")`

因為每個 row checkbox 都有同一個 class：

```html
class="in-use-checkbox"
```

所以：

```javascript
document.querySelectorAll(".in-use-checkbox")
```

會搵晒所有 row checkbox，之後可以用 `forEach()` 逐個改 `checked` 狀態。

##### 5. All 只代表當前畫面

如果有 pagination / filter，All checkbox 通常只代表目前頁面顯示嘅 rows。

原因係 POST 只會提交目前頁面嘅：

```text
selectable_ids
selected_ids
```

所以 all checked / unchecked 只應影響當前 page / 當前 filter，而唔係全 database 所有 `UserVocab`。

#### 理解內容

-

<a id="AJAX-GET-LINK-VS-POST-FORM"></a>

### `[AJAX-GET-LINK-VS-POST-FORM]` Ajax 入面 GET link 同 POST form 嘅分工

#### 問題背景

之前 `vocab_list` pagination / search 用 Ajax 做 partial update：

```text
click page link
-> fetch link URL
-> view return partial HTML
-> replace list container
```

今次 quiz flow 想做到：

```text
submit answer
-> check answer
-> update quiz stats
-> return result partial
```

一開始容易混淆：既然 vocab list 可以用 `<a href="...">` + `fetch(url)`，quiz submit answer 係咪都可以用同一種寫法？

#### 研究方向

- GET request 同 POST request 嘅語意分別。
- `<a href>` 適合做咩，`<form method="POST">` 適合做咩。
- Ajax 是否只係「唔 reload 成頁」，而唔係改變 GET / POST 本質。
- `FormData(form)` 點樣將 form fields、hidden inputs 同 CSRF token 一齊送去 view。
- Django `FormView.form_valid()` 需要用咩 request method 先會正常觸發。

#### 你的解答

##### 1. Vocab list pagination 適合 GET link

`vocab_list` pagination / search 主要係讀資料：

```text
/vocab/list?page=2&keyword=abc
```

資料放喺 URL query string 入面，所以可以用：

```html
<a href="/vocab/list?page=2&keyword=abc">2</a>
```

配合：

```javascript
fetch(url)
```

呢種 pattern 適合：

- pagination
- search
- filter
- sort
- 其他唔改 database 嘅讀取操作

##### 2. Quiz submit answer 適合 POST form

Quiz answer submit 會帶住：

- `answer`
- hidden `user_vocab_id`
- hidden `tips_count`
- CSRF token

而且 submit 後會更新 database：

- `correct_count`
- `incorrect_count`
- `streak`
- `last_quiz_at`
- `last_answer`

所以應該用：

```html
<form method="POST" action="{% url 'quiz:quiz_submit_answer' %}">
    {% csrf_token %}
    <input type="hidden" name="user_vocab_id" value="{{ question_vocab.id }}">
    <input type="hidden" name="tips_count" value="0">
    <input type="text" name="answer">
    <button type="submit">Enter</button>
</form>
```

如果要 Ajax，就攔截 form submit：

```javascript
fetch(form.action, {
    method: form.method,
    body: new FormData(form),
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
    },
})
```

重點係：Ajax 只係令畫面唔 full reload；佢唔會令 POST action 變成 GET link。

##### 3. Logout form 同 quiz form 其實係同類概念

Logout flow 通常係：

```text
POST form -> logout -> redirect
```

Quiz flow 係：

```text
POST form -> answer checking -> return partial HTML
```

所以 quiz 更似：

```text
logout-form 嘅 POST action
+
vocab list 嘅 partial replace
```

##### 4. Ajax 指向邊個 view，取決於 form action

Answer form：

```django
action="{% url 'quiz:quiz_submit_answer' %}"
```

代表 Ajax POST 會打去：

```text
QuizSubmitAnswerView
```

Next form：

```django
action="{% url 'quiz:quiz_next' %}"
```

代表 Ajax POST 會打去：

```text
QuizNextView
```

JavaScript 唔需要硬寫 view 名，只需要讀取：

```javascript
form.action
```

咁 template 決定 action URL，JS 只負責 submit 同 replace partial。

#### 理解內容

- GET link Ajax：適合「去某個 URL 讀資料，再局部更新畫面」。
- POST form Ajax：適合「提交 form data 去做 action，再局部更新畫面」。
- Quiz answer / next 屬於 action flow，所以應該用 form submit，而唔係單純 `<a href="#">`。
- `FormData(form)` 會將 form 入面所有有 `name` 嘅 input 一齊提交，包括 hidden input 同 CSRF token。

<a id="AJAX-EVENT-TRIGGER-FETCH"></a>

### `[AJAX-EVENT-TRIGGER-FETCH]` Ajax 唔一定要由 button submit 觸發

#### 問題背景

Event list 想用 dropdown filter，例如：

```text
All / Unread / Read
```

一開始容易以為 Ajax 一定係：

```text
click button / submit form
-> fetch
-> replace partial
```

但其實 Ajax 只係「由 JavaScript 發 request」。觸發時機可以係好多種 event，例如：

- button `click`
- form `submit`
- select `change`
- text input `input`
- checkbox `change`

#### 研究方向

- JavaScript event listener 同 Ajax request 嘅關係。
- 點解 dropdown change 可以直接 fetch filtered result。
- `form.submit()` 同 `fetch()` 嘅分別。
- 點樣由 form data 砌 GET query string。
- `history.pushState()` 係做咩。
- Dropdown `change` event 入面，點解唔可以用 `e.target.href`。

#### 概念整理與解答

##### 1. Ajax 唔綁死 button / submit

Ajax 本質係：

```text
某個 JS event 發生
-> JS 決定要打邊條 URL
-> fetch request
-> 用 response 更新 DOM
```

所以可以係 form submit：

```javascript
form.addEventListener("submit", function(e) {
    e.preventDefault();
    fetch(form.action, ...);
});
```

亦可以係 dropdown change：

```javascript
statusSelector.addEventListener("change", function(e) {
    fetch(url, ...);
});
```

分別只係 user action 唔同，Ajax flow 本身一樣。

##### 2. 普通 GET submit

用：

```javascript
form.submit();
```

browser 會正式前往 form action 加 query string，例如：

```text
/events/?status=read
```

所以頁面會 full reload，URL 亦會自動更新。

##### 3. Ajax fetch

用：

```javascript
fetch("/events/?status=read")
```

意思係用 JavaScript 背景打 request，攞 response 返嚟自己處理。

所以：

- Browser address bar 不會自動改。
- Page 不會 full reload。
- 要自己將 response HTML 放入指定 container。

##### 4. Dropdown change 要自己砌 URL

Dropdown `change` event 入面，`e.target` 係 `<select>`。`<select>` 無 `href`，所以唔可以寫：

```javascript
const url = e.target.href;
```

正確方向係用 form data 砌 query string：

```javascript
const params = new URLSearchParams(new FormData(form));
const url = `${form.action}?${params.toString()}`;
```

如果 user 揀咗 `read`，`params.toString()` 會變成：

```text
status=read
```

之後就可以：

```javascript
fetch(url, {
    headers: {
        "X-Requested-With": "XMLHttpRequest"
    }
})
.then(res => res.text())
.then(html => {
    container.innerHTML = html;
});
```

##### 5. 手動同步 address bar

Ajax 成功更新畫面後，如果想 URL 都變，要自己加：

```javascript
history.pushState(null, "", url);
```

例如：

```javascript
.then(html => {
    container.innerHTML = html;
    history.pushState(null, "", url);
});
```

##### 6. 重點

```text
Ajax 可以由 submit / click / change / input 等任何 JS event 觸發

form.submit()
= browser 正式轉頁，所以 URL 自動變

fetch()
= JavaScript 背景 request，所以 URL 不會自動變

history.pushState()
= 手動同步 address bar 狀態
```

#### 理解內容

-

<a id="DJANGO-AJAX-PARTIAL-ACTION-ENDPOINT"></a>

### `[DJANGO-AJAX-PARTIAL-ACTION-ENDPOINT]` Ajax partial flow 入面，View 係 action endpoint，Partial 係 UI state

#### 問題背景

Quiz flow 想做到同一個 quiz page 入面局部切換：

```text
question partial
-> submit answer by Ajax
-> replace 成 result partial
-> click Next
-> replace 成下一題 question partial
```

一開始容易諗成：

```text
QuizQuestionView render question partial
QuizResultView render result partial
QuizResultView 入面再處理 Next
```

但其實更重要係分清：

```text
View = 處理 request / user action
Partial = 顯示某個 UI state
```

#### 研究方向

- `render_to_response()` 適合咩場景。
- `form_valid()` / `post()` 適合咩場景。
- 點分 full page shell、question partial、result partial。
- 點避免為每個 partial 都硬開一個同名 View。

#### 我的理解

`quiz_result_partial.html` 只係「答完題後要顯示嘅畫面狀態」，唔一定需要一個 `QuizResultView`。

如果 result partial 入面有 Next button，Next button 應該 call 嘅係「抽下一題」呢個 action endpoint，例如：

```text
QuizNextView
```

而唔係一定要 call `QuizResultView`。

比較清楚嘅 flow 係：

```text
QuizPlayView GET
-> render quiz_play.html full page shell
-> shell 入面顯示第一題 question partial

Submit answer POST
-> check answer
-> update correct_count / incorrect_count / streak / last_quiz_at / weight
-> return quiz_result_partial.html

Next button POST/GET
-> pick next question
-> return quiz_question_partial.html
```

所以：

- submit answer action -> render `quiz_result_partial.html`
- next question action -> render `quiz_question_partial.html`
- partial file 名稱唔代表一定要有同名 View

#### 你嘅解答

##### 1. `render_to_response()` 適合 list page partial fallback

`render_to_response()` 比較適合呢種情況：

```text
同一個 ListView
普通 request -> render full page
Ajax request -> render partial list
```

例如 vocab list / user vocab list：

```python
def render_to_response(self, context, **response_kwargs):
    if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            self.request,
            "dictionary/partials/vocab_list_partial.html",
            context,
        )
    return super().render_to_response(context, **response_kwargs)
```

呢種情況入面，同一條 URL 同一個 view 可以同時服務：

```text
full page request
partial update request
```

##### 2. Quiz answer / next 更似 action endpoint

Quiz 呢個 case 唔係「同一條 list URL 有 full / partial 兩種 render」。

Quiz 更似：

```text
answer action -> result partial
next action -> question partial
```

所以可以直接喺 `form_valid()` 或 `post()` 入面 return partial：

```python
return render(
    self.request,
    "quiz/partials/quiz_result_partial.html",
    context,
)
```

或者：

```python
return render(
    request,
    "quiz/partials/quiz_question_partial.html",
    context,
)
```

唔需要靠 `render_to_response()` 再判斷 Ajax header。

##### 3. 答題 checking 應該放喺 submit action 入面

Answer checking 會改 database：

- `correct_count`
- `incorrect_count`
- `streak`
- `last_quiz_at`
- `weight`

所以唔應該放喺 `get_context_data()`。

`get_context_data()` 適合準備畫面資料，最好盡量避免 side effects。

答題 checking 應放喺：

```text
form_valid()
```

或：

```text
post()
```

因為呢兩個位置代表 user submit 咗 action。

##### 4. Result partial 唔需要獨立 View

如果 answer submit 後即時 return result partial：

```text
QuizPlayView.form_valid()
-> check answer
-> build context
-> render quiz_result_partial.html
```

咁 `QuizResultView` 可以完全唔需要。

Result partial 入面嘅 Next button 可以直接 call：

```text
QuizNextView
```

然後 `QuizNextView` 再 return：

```text
quiz_question_partial.html
```

##### 5. Full page shell 同 partial 要分開諗

`quiz_play.html` 可以係唯一 full page shell：

```django
<div id="quiz-area">
    {% include "quiz/partials/quiz_question_partial.html" %}
</div>
```

之後 Ajax 只 replace：

```text
#quiz-area
```

而唔需要成頁 reload。

#### 理解內容

-

<a id="DJANGO-PAGINATION-KEEP-SEARCH-QUERY"></a>

### `[DJANGO-PAGINATION-KEEP-SEARCH-QUERY]` Search form + pagination + Ajax partial update 點樣保留 GET filter

#### 問題背景

`VocabListView` 使用 GET form 做 search/filter，並將 vocab list 拆成 partial，再用 Ajax click pagination link 局部更新 list。

問題係 pagination link 如果只寫：

```django
?page={{ num }}
```

當 user 已經 search 咗 `word=...`、`kana=...`、`level=...` 時，一按下一頁就會失去原本 search filter。

#### 研究方向

- `request.GET` 入面保存咗咩 query string 資料。
- 點解 pagination link 要保留原本 query string。
- 點解要移除舊嘅 `page` parameter 再重新加新 page。
- `QueryDict.copy()`、`pop()`、`urlencode()` 各自做咩。
- Ajax partial update 同普通 pagination link 其實係咪用同一條 URL。

#### 概念整理與解答

##### 1. Search filter 其實係 URL query string

GET search form submit 後，URL 會變成類似：

```text
/dictionary/vocab/list?word=水&kana=みず
```

呢啲資料會出現喺：

```python
self.request.GET
```

所以 view 入面可以用 `VocabSearchForm(self.request.GET)` 去 filter queryset。

##### 2. Pagination link 要保留原本 filter

如果 pagination link 只寫：

```django
<a href="?page=2">2</a>
```

click 後 URL 會變成：

```text
/dictionary/vocab/list?page=2
```

原本嘅 `word=水&kana=みず` 會消失，queryset 就會變返無 filter。

正確方向係：

```text
/dictionary/vocab/list?word=水&kana=みず&page=2
```

##### 3. View 入面準備一條不包含 page 嘅 query string

可以喺 `get_context_data()` 入面做：

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context["search_form"] = VocabSearchForm(self.request.GET)

    query_params = self.request.GET.copy()
    query_params.pop("page", None)
    context["query_string"] = query_params.urlencode()

    return context
```

意思：

- `self.request.GET.copy()`：複製目前 URL query parameters。
- `query_params.pop("page", None)`：移除舊 page，避免 URL 變成 `page=1&page=2`。
- `query_params.urlencode()`：將 QueryDict 重新變回 URL query string，例如 `word=水&kana=みず`。

##### 4. Template 入面重新加新 page

Pagination link 可以寫：

```django
<a href="?{% if query_string %}{{ query_string }}&{% endif %}page={{ num }}" class="page-change">
    {{ num }}
</a>
```

如果有 search filter：

```text
?word=水&kana=みず&page=2
```

如果冇 search filter：

```text
?page=2
```

`{% if query_string %}` 係用嚟避免出現唔靚嘅：

```text
?&page=2
```

##### 5. Ajax partial update 都係用同一條 URL

Ajax click pagination 時：

```javascript
fetch(url, {
    headers: {
        "X-Requested-With": "XMLHttpRequest"
    }
})
```

`url` 仍然係 pagination link 嘅 `href`。

所以只要 pagination link 本身保留咗 search query，Ajax request 一樣會帶住 filter 去 view。

View 可以用 header 判斷是否回傳 partial：

```python
def render_to_response(self, context, **response_kwargs):
    if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            self.request,
            "dictionary/partials/vocab_list_partial.html",
            context,
        )
    return super().render_to_response(context, **response_kwargs)
```

##### 6. 重點

```text
Search state = URL query string
Pagination link = 原本 query string + 新 page
Ajax partial update = fetch 同一條 pagination URL
```

所以問題唔係 Ajax 特有，而係 pagination link 要正確保存 GET parameters。

#### 理解內容

-

<a id="GROUP-PYTHON-DATA-CONFIG"></a>

## Python、CSV 與 Configuration

<a id="PYTHON-SET-DIFFERENCE-CSV-HEADERS"></a>

### `[PYTHON-SET-DIFFERENCE-CSV-HEADERS]` 點樣用 set 差集檢查 CSV 缺少嘅 headers

#### 問題背景

目前 `import_vocab.py` 使用：

```python
missing_headers = required_headers - set(reader.fieldnames or [])
```

檢查 CSV 有冇缺少 command 要求嘅 headers，但仲未完全理解 set 減法同 `or []` 點樣運作。

#### 研究方向

- Python `set` 係咩資料結構。
- 兩個 sets 使用 `-` 時會得到咩結果。
- `csv.DictReader.fieldnames` 會提供咩資料。
- 點解要將 `reader.fieldnames` 轉成 set。
- 點解要寫成 `reader.fieldnames or []`。
- 空 CSV 或冇 header 時會發生咩事。

#### 概念整理與解答

##### 1. Set 差集

`required_headers` 代表 command 必須要有嘅欄位：

```python
required_headers = {
    "word",
    "kana",
    "meaning",
}
```

假設 CSV 實際只有：

```python
reader.fieldnames = ["word", "kana"]
```

先將佢轉成 set：

```python
set(reader.fieldnames)
# {"word", "kana"}
```

之後做減法：

```python
required_headers - set(reader.fieldnames)
# {"meaning"}
```

Set 嘅 `A - B` 代表「存在於 A，但不存在於 B」嘅項目。因此完整概念係：

```text
必須有嘅 headers
減去
CSV 實際有嘅 headers
等於
CSV 缺少嘅 headers
```

如果 CSV 所有必要 headers 都齊全，結果會係空 set：

```python
set()
```

空 set 喺 `if` 判斷入面係 `False`，所以：

```python
if missing_headers:
```

只會喺確實有缺少 header 時執行。

##### 2. `reader.fieldnames or []`

正常情況下，`reader.fieldnames` 係一個 header list。但如果 CSV 係空嘅，佢可能係 `None`。

以下寫法會出錯：

```python
set(None)
# TypeError
```

所以使用：

```python
reader.fieldnames or []
```

Python 嘅 `or` 會回傳第一個 truthy value：

- `reader.fieldnames` 有內容時，使用原本嘅 header list。
- `reader.fieldnames` 係 `None` 或空值時，改用 `[]`。

因此：

```python
set(reader.fieldnames or [])
```

即使 CSV 冇 header，都會安全變成：

```python
set([])
# set()
```

最後所有 `required_headers` 都會被判定為 missing，而唔係先出現 `TypeError`。

##### 3. 完整流程

```python
missing_headers = required_headers - set(reader.fieldnames or [])

if missing_headers:
    raise CommandError(
        f"Missing CSV headers: {', '.join(sorted(missing_headers))}"
    )
```

流程係：

1. 取得 CSV 實際 headers。
2. 將 headers 轉成 set。
3. 用 set 差集搵出缺少嘅 headers。
4. 有缺少時，將名稱排序及連接成 error message。
5. 用 `CommandError` 停止 import，避免逐行先出現 `KeyError`。

#### 理解內容

-

<a id="PYTHON-ENUMERATE-CSV-ROWS"></a>

### `[PYTHON-ENUMERATE-CSV-ROWS]` `enumerate()` 點樣提供 CSV 行數同資料

#### 問題背景

目前 `import_vocab.py` 使用：

```python
for row_number, data in enumerate(reader, start=2):
```

逐行讀取 CSV，但仲想進一步理解 `enumerate()`、`row_number`、`data` 同 `start=2` 各自有咩作用。

#### 研究方向

- `csv.DictReader` 每次 iteration 會回傳咩資料。
- `enumerate()` 點樣為 iterable 加上編號。
- 點解可以同時寫 `row_number, data`。
- `start=2` 係咪會跳過 CSV 頭兩行。
- 點樣用真實 CSV 行數顯示清楚嘅 error message。

#### 概念整理與解答

##### 1. `reader` 每次提供一行資料

`csv.DictReader` 會先讀取 CSV header，之後每次 loop 回傳一行 dictionary：

```python
{
    "word": "犬",
    "kana": "いぬ",
    "type": "vocab",
}
```

如果只需要資料，可以寫：

```python
for data in reader:
    print(data)
```

##### 2. `enumerate()` 加入編號

`enumerate(reader, start=2)` 會將每行資料包成一組 `(編號, 資料)`：

```python
(2, {"word": "犬", "kana": "いぬ"})
(3, {"word": "猫", "kana": "ねこ"})
```

所以 loop 可以將兩個值分別 unpack 到：

```python
row_number, data
```

完整寫法：

```python
for row_number, data in enumerate(reader, start=2):
```

- `row_number`：目前資料喺 CSV 入面嘅實際行數。
- `data`：目前嗰行由 `DictReader` 產生嘅 dictionary。

##### 3. 點解使用 `start=2`

CSV 第 1 行通常係 header：

```csv
word,kana,type
犬,いぬ,vocab
```

`DictReader` 已經先讀取第 1 行做欄位名稱，因此 loop 第一次取得嘅資料實際位於 CSV 第 2 行。

```python
enumerate(reader, start=2)
```

令第一次 loop 嘅 `row_number` 直接係 `2`，方便顯示：

```text
Row 2: invalid category
```

`start=2` 只會改變編號起點，唔會跳過兩行資料。

##### 4. 點解唔可以直接寫 `for row_number, data in reader`

`reader` 每次只回傳一個 dictionary，唔會自動附帶行數。直接要求拆成 `row_number` 同 `data`，Python 會嘗試拆解 dictionary keys，通常會出現 unpacking error。

要同時取得編號同資料，需要由 `enumerate()` 將每項包成兩個 values。

#### 理解內容

-

<a id="PYTHON-JSON-CONFIG-MAP-LOOKUP"></a>

### `[PYTHON-JSON-CONFIG-MAP-LOOKUP]` 用 JSON config map 查 subtype / 設定值

#### 問題背景

Quiz answer compare 需要根據兩個 kana 判斷 wrong subtype，例如：

```text
correct=は, user=ば -> DAKUTEN
correct=つ, user=っ -> SMALL_KANA
```

呢類資料本質上係 mapping data，唔一定適合硬寫喺 function 入面。抽成 JSON 後，可以集中維護 data，function 只負責查表。

#### 研究方向

- `json.load()` 點樣將 JSON file 讀成 Python dict。
- 共用 `load_json()` 時，path 應該用 project root 做基準，避免因為 caller 喺唔同 app 而搵錯 file。
- nested dict 點樣安全讀取資料。
- `.get()` 同直接用 `dict[key]` 嘅差異。

#### 我的理解

JSON 可以設計成簡單 nested map：

```json
{
  "は": {
    "ば": "DAKUTEN",
    "ぱ": "HANDAKUTEN"
  },
  "つ": {
    "っ": "SMALL_KANA"
  }
}
```

讀入 Python 後會變成：

```python
COMPARE_SUBTYPE = load_json(path="quiz/config/compare_answer_subtype.json")
```

安全查 subtype 可以寫：

```python
subtype = COMPARE_SUBTYPE.get(correct_letter, {}).get(user_letter)
return subtype if subtype is not None else "NORMAL"
```

意思：

1. `COMPARE_SUBTYPE.get(correct_letter, {})`
   - 如果有 correct letter，就回傳入面嗰個 dict。
   - 如果冇，就回傳空 dict `{}`。

2. `.get(user_letter)`
   - 喺內層 dict 搵 user letter。
   - 搵唔到就回傳 `None`。

3. 如果最後係 `None`，就當普通錯誤：

```python
"NORMAL"
```

#### 點解唔直接用 `COMPARE_SUBTYPE[correct_letter][user_letter]`

直接用 square bracket：

```python
COMPARE_SUBTYPE[correct_letter][user_letter]
```

如果其中一層 key 唔存在，就會直接 `KeyError`。

例如：

```text
correct=あ, user=か
```

呢組唔係特別 subtype，只係普通 wrong。如果用 `[]`，程式會爆 error；如果用 `.get()`，就可以正常 fallback 去 `NORMAL`。

#### 重點

- JSON config 適合放「查表式 data」。
- Function 應該負責查資料同 fallback，不應該塞大量 hard-coded mapping。
- 巢狀 dict 查資料時，用 `.get(key, {})` 可以避免第一層 key 唔存在時爆 `KeyError`。
- 如果 `None` 係不合法結果，就要顯式轉成 default value，例如 `NORMAL`。

#### 理解內容

-

<a id="PYTHON-LOGGING-FILTER"></a>

### `[PYTHON-LOGGING-FILTER]` Logging filter 除左篩選 level 仲可以做什麼

#### 問題背景

Logging handler 嘅 `level` 係「最低接受 level」，唔係「只接受呢個 level」。

例如：

```python
"level": "DEBUG"
```

會收到 `DEBUG`、`INFO`、`WARNING`、`ERROR` 同 `CRITICAL`。如果 `debug_log.log` 只想收 `DEBUG`，就需要 filter 再做精確判斷。

#### Filter 嘅核心作用

Filter 會喺每條 log 交俾 handler 之前收到一個 `LogRecord`。佢可以：

- return `True`：保留條 log。
- return `False`：丟棄條 log。
- 在 return 之前修改 `record`：為 log 加入共同資料或遮蔽資料。

#### 1. 只保留某個精確 level

Django 現成嘅 `CallbackFilter` 可以配合 callback：

```python
"filters": {
    "debug_only": {
        "()": "django.utils.log.CallbackFilter",
        "callback": lambda record: record.levelname == "DEBUG",
    },
},
```

Handler 再引用佢：

```python
"debug_file": {
    "class": "logging.handlers.TimedRotatingFileHandler",
    "level": "DEBUG",
    "filters": ["debug_only"],
}
```

結果係 `debug_file` 只收 `DEBUG`，唔會再收 INFO 或 ERROR。

#### 2. 排除無價值嘅高頻 log

例如 health-check endpoint 每幾秒就被 request 一次，可以用 filter 排除：

```python
def skip_health_check(record):
    return "/health/" not in record.getMessage()
```

這類 filter 適合處理大量重複、而對除錯無幫助嘅 log。唔應該用佢掩蓋真正 exception。

#### 3. 根據 operation 或 flow 分流

Logger 可以透過 `extra` 加入 operation：

```python
logger.info(
    "Import completed",
    extra={"operation": "vocab_import"},
)
```

Filter 就可以只接受 import flow：

```python
def import_only(record):
    return getattr(record, "operation", None) == "vocab_import"
```

呢個做法可以將 import、audit 或 security event 寫入獨立 handler。Project 小時未必需要即時分太多檔案。

#### 4. 根據 HTTP status 或 record 資料篩選

如果 record 有 `status_code`，可以只保留 server errors：

```python
def server_error_only(record):
    return getattr(record, "status_code", 0) >= 500
```

不過單純 ERROR 分流通常先用 handler 嘅：

```python
"level": "ERROR"
```

只有需要更精確嘅條件時才加 filter。

#### 5. 為 record 加入共同 context

Custom filter 可以補充 formatter 會用嘅欄位：

```python
class ContextFilter(logging.Filter):
    def filter(self, record):
        record.environment = "development"
        return True
```

Formatter 就可以使用：

```python
"{asctime} [{levelname}] [{environment}] {message}"
```

同類資料包括：

- environment
- request ID
- user ID
- operation name

Filter 唔會自動知道當前 user 或 request ID；這些資料通常需要 middleware、context variable 或 `extra` 配合。

#### 6. 遮蔽敏感資料

Filter 可以修改 record，例如將某個欄位改成 `[REDACTED]`。不過呢個只係最後防線，更安全嘅做法係從源頭唔好將敏感資料傳入 logger。

不應該寫入 log 嘅資料包括：

- password
- cookie 或 session key
- CSRF token
- access token
- 完整 POST body

#### 目前 project 嘅最小做法

現階段只需要 `debug_only` filter，將 DEBUG 同其他 level 分開。其他 filter 等基礎 logging 已經運作，而且真正出現高頻噪音、operation 分流或 request context 需求時先加。

簡單原則：

```text
Handler level = 先做最低 level 門檻
Filter        = 再做精確條件／排除／補資料
Formatter     = 決定最後輸出格式
```

<a id="PYTHON-EXCEPTION-RAISE-AND-LOGGER-EXCEPTION"></a>

### `[PYTHON-EXCEPTION-RAISE-AND-LOGGER-EXCEPTION]` Exception、`raise`、`from e` 同 `logger.exception()`

#### 問題背景

喺 `import_vocab` management command 加 logging 時，需要分辨預期輸入問題、未預期 exception、重新拋出原本錯誤，以及將底層錯誤轉成 `CommandError`。目前對 Python exception flow 尚未完全理解，呢項先保存基本概念同之後研究方向。

#### 研究方向

- Exception object 係咩，以及程式點樣由 `try` 跳去對應嘅 `except`。
- `except SomeError as e` 入面嘅 `e` 保存咗咩資料。
- 捕捉 exception、處理 exception、吞掉 exception同重新拋出 exception 嘅分別。
- 單獨 `raise` 同 `raise NewError(...) from e` 嘅分別。
- Traceback 點樣顯示錯誤發生位置同 function call path。
- `logger.error()`、`logger.exception()` 同 `exc_info=True` 嘅關係。

#### 目前概念整理

Exception 係 Python 表示「程式執行期間發生問題，原本流程無法繼續」嘅機制。`try` 包住可能出錯嘅程式；出現匹配嘅 exception 時，Python 會停止執行 `try` 剩低部分，跳入對應嘅 `except`。

```python
try:
    open("missing.csv")
except FileNotFoundError as e:
    print(e)
```

`e` 只係保存今次 `FileNotFoundError` object 嘅變數名，可以用嚟讀取原始錯誤資料。

單獨使用：

```python
except Exception:
    raise
```

代表將目前捕捉緊嘅同一個 exception 原封不動重新拋出。常見用途係先記錄問題，再讓外層知道操作失敗，避免 exception 被靜默吞掉。

使用：

```python
except FileNotFoundError as e:
    raise CommandError("CSV file not found") from e
```

代表拋出新嘅 `CommandError`，同時用 `from e` 保存「新錯誤由原本 `FileNotFoundError` 引起」嘅因果關係。

#### `logger.exception()` 並唔係 logging level

標準 logging levels 仍然係：

```text
DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
```

`logger.exception()` 係方便寫法，會使用 `ERROR` level，並自動加入目前 exception 嘅 traceback：

```python
try:
    run_import()
except Exception:
    logger.exception("Unexpected import failure")
    raise
```

概念上接近：

```python
logger.error("Unexpected import failure", exc_info=True)
```

因此 `logger.exception()` 一般只應放喺 `except` 裏面。預期嘅 invalid row、missing header 或 missing file 通常用清楚嘅 `WARNING` message；真正未預期、需要 traceback 追查嘅程式或系統故障先使用 `logger.exception()`。

#### 暫時記法

```text
except SpecificError  = 已知道可能發生咩問題，作對應處理
except Exception      = 捕捉其他未預期問題
raise                 = 將目前同一個錯誤繼續拋出
raise NewError from e = 轉成新錯誤並保留原始原因
logger.exception()    = ERROR level + 目前 exception traceback
```

#### 理解內容

- 目前已確認 `logger.exception()` 唔係獨立 logging level。
- Exception flow、重新拋出與 exception chaining 仍待之後進一步理解。

<a id="PYTHON-DATACLASS-2D-LIST-DP-STATE"></a>

### `[PYTHON-DATACLASS-2D-LIST-DP-STATE]` 用 `dataclass` 同 2D list 保存 DP state

#### 問題背景

將 `QuizService.answer_compare()` 由 recursive search 改寫成 bottom-up dynamic programming 時，每個 `dp[i][j]` 唔只要保存一個分數，仲要保存多項互相關聯嘅資料，例如：

- `cost`
- `match_count`
- `non_normal_wrong_count`
- 呢格揀中嘅 `operation`

C++ 可以用 `struct` 封裝一格嘅資料，再建立 2D array；Python 對應做法係使用 `@dataclass` 配合 nested list。

#### 研究方向

- Python `@dataclass` 同 C++ `struct` 喺資料建模上嘅對應關係。
- `list[list[...]]` 點樣表示 2D table。
- `Optional[T]`／`T | None` 表示咩，以及佢同「參數可以省略」嘅分別。
- Python nested list 點解唔應該用 `[[value] * width] * height` 建立。
- 邊啲 state 必須保存，邊啲資料可以由其他欄位推算，避免 duplicate state。

#### 你的解答

##### 1. 用 `dataclass` 表示一個 DP cell

Python `@dataclass` 可以將一組相關資料包成一個有名稱、有 type hint 嘅 object，角色接近 C++ `struct`：

```python
from dataclasses import dataclass


@dataclass
class DPCell:
    cost: int
    match_count: int
    non_normal_wrong_count: int
    operation: str | None
```

之後可以清楚噉讀取每項資料：

```python
cell.cost
cell.match_count
cell.non_normal_wrong_count
cell.operation
```

如果欄位固定，`dataclass` 通常比 dictionary 更適合，因為 dictionary 嘅 key 係任意 string，拼錯亦未必即時發現；`dataclass` 就可以清楚定義 object 應有嘅欄位。

##### 2. 建立 2D list

答案長度分別係 `m` 同 `n` 時，DP table 通常需要 `(m + 1) × (n + 1)`，額外一行同一列代表其中一邊已經去到字串結尾：

```python
dp: list[list[DPCell | None]] = [
    [None for _ in range(n + 1)]
    for _ in range(m + 1)
]
```

未計算嘅格係 `None`；計算完成後，就可以放入一個 `DPCell`：

```python
dp[i][j] = DPCell(
    cost=1,
    match_count=2,
    non_normal_wrong_count=0,
    operation="MISSING",
)
```

終點 `dp[m][n]` 已經無下一個 operation，所以 `operation=None`：

```python
dp[m][n] = DPCell(
    cost=0,
    match_count=0,
    non_normal_wrong_count=0,
    operation=None,
)
```

##### 3. 普通 nested `for` 同 list comprehension 對比

以下係較完整、容易逐步理解嘅普通寫法：

```python
dp_table = []

for row_index in range(len(correct_answer) + 1):
    row = []

    for column_index in range(len(user_answer) + 1):
        row.append(None)

    dp_table.append(row)
```

執行流程係：

1. 外層 `for` 決定建立幾多行，行數係 `len(correct_answer) + 1`。
2. 每次進入外層 loop，都會建立一個全新嘅 `row`。
3. 內層 `for` 向呢行加入 `len(user_answer) + 1` 個 `None`。
4. 一行完成後，將 `row` 加入 `dp_table`。

同一段邏輯可以縮寫成 list comprehension：

```python
dp_table: list[list[DPCell | None]] = [
    [None for _ in range(len(user_answer) + 1)]
    for _ in range(len(correct_answer) + 1)
]
```

內層：

```python
[None for _ in range(len(user_answer) + 1)]
```

負責建立一行。外層：

```python
for _ in range(len(correct_answer) + 1)
```

負責重複建立新行，最後組成整張 2D table。

`_` 只係一個普通變數名。慣例上，loop counter 無需使用時會命名為 `_`，表示「只需要重複指定次數，唔需要使用今次係第幾次」。如果填表時需要座標，就應該改用 `i`、`j`：

```python
for i in range(len(correct_answer) + 1):
    for j in range(len(user_answer) + 1):
        dp_table[i][j] = ...
```

例如 `correct_answer="がっこう"`、`user_answer="かこう"`：

```text
len(correct_answer) + 1 = 5 行
len(user_answer) + 1    = 4 列
結果                      = 5 × 4 = 20 格
```

括號位置要留意。正確係先計字串長度，再加一：

```python
len(user_answer) + 1
```

以下寫法會先嘗試執行 `user_answer + 1`，即係將 string 同 integer 相加，因而產生 `TypeError`：

```python
len(user_answer + 1)  # 錯誤
```

##### 4. `Optional`／`| None` 嘅意思

以下兩種 type hint 意思相同：

```python
from typing import Optional

operation: Optional[str]
operation: str | None
```

兩者都表示值可以係 `str`，亦可以係 `None`。佢唔代表 constructor parameter 可以省略；如果想省略，必須另外提供 default value：

```python
operation: str | None = None
```

##### 5. 唔需要保存可以推算嘅 next position

原本可以喺每格同時保存 `next_i` 同 `next_j`，但目前四種 operation 已經唯一決定下一格：

```text
MATCH / WRONG -> dp[i + 1][j + 1]
MISSING       -> dp[i + 1][j]
EXTRA         -> dp[i][j + 1]
```

因此只保存 `operation` 已經足夠。重建路線時再由 operation 推算下一格，可以避免 `operation` 與 next position 互相矛盾嘅 duplicate state。

##### 6. Nested list 嘅 shared-row 陷阱

唔應該噉建立 2D list：

```python
dp = [[None] * (n + 1)] * (m + 1)
```

外層重複嘅係同一個 inner list reference；修改其中一行嘅元素時，其他行相同位置亦會一齊改變。

應該逐行建立獨立 list：

```python
dp = [
    [None for _ in range(n + 1)]
    for _ in range(m + 1)
]
```

#### 理解內容

- C++ `struct + 2D array/vector` 同 Python `dataclass + nested list` 係相同資料建模思路，主要分別係語法同 container。
- 每個 `dp[i][j]` 應該保存該 state 嘅最佳 score 同所選 operation。
- Nested list comprehension 係普通 nested `for` 嘅縮寫：內層建立一行，外層重複建立多行；`_` 表示 loop counter 無需使用。
- `(len(answer) + 1)` 代表字串長度加一；唔可以寫成 `len(answer + 1)`。
- `str | None` 表示值可以係 string 或 `None`；唔等於 parameter 自動變成 optional。
- 只保存必要 state；由 operation 已經可以推算下一格，就唔需要重複保存座標。
- 建立 mutable 2D list 時要逐行建立，避免多行共用同一個 inner list。

<a id="GROUP-PROJECT-ARCHITECTURE-DOMAIN"></a>

## Project Architecture 與 Domain Design

<a id="DOMAIN-VOCAB-USERVOCAB-IN-USE"></a>

### `[DOMAIN-VOCAB-USERVOCAB-IN-USE]` `Vocab` 同 `UserVocab.in_use` 嘅設計心智模型

#### 問題背景

目前 `Vocab` 代表全站共用嘅 vocabulary pool，而 `UserVocab` 代表某個 user 同某個 vocab 之間嘅個人 learning relationship。

新增設計：

- 新 vocab 可以自動加入 user 嘅 `UserVocab`。
- 但新建立嘅 `UserVocab.in_use` 預設係 `False`。
- User 之後可以喺自己嘅 vocab list 入面決定邊啲字要啟用。
- Quiz question pool 只應使用 `in_use=True` 嘅 `UserVocab`。

#### 研究方向

- 點解唔應該因為 user 暫時唔想練某個字，就刪除 `Vocab`。
- 點解 `UserVocab` 唔只係 many-to-many join table，而係 user 個人 learning state。
- `in_use=False` 同刪除 `UserVocab` 有咩分別。
- EventNotice 系統點樣通知 user 有新字可啟用。
- Quiz pool 點樣只取 user 已啟用嘅 vocab。

#### 概念整理與解答

##### 1. 連鎖餐廳 menu 比喻

可以將整個設計想像成一間連鎖餐廳：

- 總公司 menu = `Vocab`
- 分店 menu = `UserVocab`
- 分店有冇提供某個 menu item = `UserVocab.in_use`

當總公司推出新 menu：

- 新 menu 會加入總公司 menu list。
- 各分店可以收到呢個 menu item。
- 但某間分店可以因為實際情況，暫時唔提供某個 menu item。
- 某間分店唔提供，唔代表總公司要刪除嗰個 menu item。

對應返 project：

- Admin approve / CSV import 建立新 `Vocab`。
- 系統可以為相關 user 建立 `UserVocab`。
- `UserVocab.in_use=False` 表示個字已經喺 user 個人 list 入面，但暫時唔加入 quiz。
- User click on 想練嘅字後，將 `in_use` 改成 `True`。
- Quiz 只抽 `in_use=True` 嘅 `UserVocab`。

##### 2. `Vocab` 係總資料，`UserVocab` 係個人狀態

`Vocab` 保存全站共用資料：

- word
- kana
- meaning
- type
- level
- category
- detail model

`UserVocab` 保存 user 個人 learning state：

- user 是否啟用呢個字：`in_use`
- 抽題 weight
- correct / incorrect count
- streak
- last quiz time

所以 `UserVocab` 唔應該只當普通 join table 睇。佢係「user 對呢個 vocab 嘅個人狀態 record」。

##### 3. 點解用 `in_use=False`，而唔係唔建立 `UserVocab`

如果唔建立 `UserVocab`：

- 系統唔容易知道呢個 user 有冇收過呢個字。
- EventNotice 之後難以追蹤 user 有邊啲新字未處理。
- User list 入面無法顯示「可啟用但未啟用」嘅字。

如果建立 `UserVocab(in_use=False)`：

- 系統知道呢個字已經派到 user 個人 list。
- User 可以 filter `in_use=False` 睇未啟用字。
- EventNotice 可以提醒 user 有新字可處理。
- Quiz pool 仍然可以保持乾淨，只抽 `in_use=True`。

##### 4. 點解唔直接刪 `UserVocab`

刪除 `UserVocab` 代表失去 user 對呢個 vocab 嘅個人 record。

但 `in_use=False` 代表：

- 個 record 仲存在。
- User 暫時唔練。
- 之後可以重新啟用。
- 如有需要，quiz stats / learning history 可以繼續保留。

所以 `in_use` 比 delete 更適合表示「暫時不用」。

##### 5. 對 quiz pool 嘅影響

Quiz 出題時唔應該直接由全站 `Vocab` 抽題，而應該由目前 user 嘅 `UserVocab` 抽：

```python
UserVocab.objects.filter(
    user=request.user,
    in_use=True,
)
```

之後再喺呢個 pool 上套用：

- vocab type filter
- level filter
- category filter
- weighted random
- recent 10 skip
- overdue boost

咁可以確保 user 未啟用嘅字唔會突然出題。

#### 理解內容

-

<a id="DJANGO-CONTEXT-PROCESSOR-NAVBAR-DATA"></a>

### `[DJANGO-CONTEXT-PROCESSOR-NAVBAR-DATA]` 全站 navbar data 應該用 context processor

#### 問題背景

`core/base.html` 係所有 page 共用嘅 base template，頂部 menu 會顯示 Home、Profile、Sign in / Login、Vocab 等 link。

如果想加一個 Event link，並且喺有 unread event 時顯示類似：

```text
Event(2)
```

就需要每個 render 出嚟嘅 template 都可以拎到 unread event count。

問題係：應唔應該每個 view 都喺 `get_context_data()` 入面加 `unread_event_count`？定係用 middleware？

#### 研究方向

- `get_context_data()` 適合單一 view / page-specific data。
- Middleware 適合每個 request 前後都要執行嘅 request-level logic。
- Context processor 適合「所有 template 都想用到嘅共用顯示資料」。
- Navbar unread count 屬於 template display data，唔係每個 view 嘅業務邏輯。

#### 你的解答

呢個情況最適合用 **context processor**。

Context processor 會喺 template render 時，自動將指定資料加入 template context。咁 `base.html` 就可以直接用同一個變數，而唔需要每個 view 都手動 pass。

例子：

```python
# core/context_processors.py

from core.service.event import EventService

def unread_event_count(request):
    if not request.user.is_authenticated:
        return {
            "unread_event_count": 0,
        }

    return {
        "unread_event_count": EventService.get_unread_events(user=request.user).count(),
    }
```

然後喺 `settings.py` 註冊：

```python
TEMPLATES = [
    {
        "OPTIONS": {
            "context_processors": [
                # Django default context processors...
                "core.context_processors.unread_event_count",
            ],
        },
    },
]
```

之後 `base.html` 可以直接寫：

```django
<a href="{% url 'core:event_list' %}">
    Event{% if unread_event_count %}({{ unread_event_count }}){% endif %}
</a>
```

#### Middleware 同 context processor 分工

Middleware 係 request / response 層：

```text
Request -> Middleware -> URL/View -> Middleware -> Response
```

適合做：

- request logging
- permission / redirect
- language / timezone setup
- login user request-level sync
- 每次 request 前後都一定要做嘅 side effect

Context processor 係 template render 層，適合做：

- navbar unread count
- site-wide display data
- common user display info
- base template 需要嘅 shared context

#### 理解內容

- `get_context_data()` 唔應該為咗全站 navbar data 喺每個 view 重複寫。
- Middleware 可以做到全 request 共用 logic，但 unread count 主要係 template 顯示資料，context processor 更啱。
- Context processor 每次 render template 都可能會查一次 DB，例如 `.count()` unread events；project 細時 OK，將來可以再加 cache 或節流。
- 簡單記法：middleware 管 request flow，context processor 管 template 共用 context。

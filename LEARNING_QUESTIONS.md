# 學習疑問與研究筆記

呢份文件用嚟記錄學習過程中仍然有疑問、值得之後深入研究的概念。內容未必代表 project 仲有 bug。

## [ ] `[DJANGO-CUSTOM-USER-ADMIN]` Django Custom User Admin

### 問題背景

Django User 的 `password` 欄位唔可以當普通文字欄位直接儲存。真正存入 database 的內容應該係經過 `set_password()` 產生的 password hash。

Custom User Admin 需要分開處理兩個流程：

1. 新增 User
2. 修改現有 User

### 研究方向

- `UserAdmin.form` 同 `UserAdmin.add_form` 分別喺邊個頁面使用。
- `fieldsets` 同 `add_fieldsets` 點樣控制 change/add 頁顯示的欄位。
- 點解 `ReadOnlyPasswordHashField` 只適合 change form。
- Django 原生 `UserCreationForm` 同自訂 `ModelForm` 的差異。
- Django Admin 正式修改密碼的 password change flow 點樣運作。

### 概念整理與解答

#### 修改現有 User

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

#### 新增 User

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

#### 目前採用的做法

- 繼續使用 `RegistForm`
  - `add_fieldsets` 配合使用 `password`、`password2`。
  - `RegistForm.save()` 已呼叫 `set_password()`。

另一個可研究的做法係建立專用的 `UserCreationAdminForm`：

  - 使用慣常的 `password1`、`password2` 命名。
  - 在 `save()` 內呼叫 `set_password(password1)`。
  - 將 `add_form` 改成這個專用表單。

### 理解內容

-

## [ ] `[DJANGO-HANDWRITTEN-CHECKBOX-POST-FORM]` 手寫 checkbox HTML，再用 Django Form 接 POST data

### 問題背景

`UserVocabListView` 想用 table 形式顯示 user vocab：

```text
[checkbox] word / kana / meaning
```

UI 需要自己排 table，所以唔適合直接用 `{{ form.as_p }}` render 成個 form。
但 submit 後仍然想用 Django Form 驗證 POST data。

### 研究方向

- 點解唔一定要喺 `get_context_data()` pass form 出去先可以用 form validate。
- Template 手寫 input 時，點樣同 Django Form field name 對應。
- `selectable_ids` 同 `selected_ids` 分別代表咩。
- 點解 checkbox 未勾選時唔會 submit。
- 點解要用 hidden input 記低畫面顯示過嘅 rows。

### 概念整理與解答

#### 1. Form render 同 Form validation 可以分開

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

#### 2. Template 手寫 input

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

#### 3. POST data 會變成點

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

#### 4. 用 Django Form 接住 POST data

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

#### 5. 點解可以唔 pass form 去 context

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

### 理解內容

-

## [ ] `[HTML-JS-CHECKBOX-SELECT-ALL]` Checkbox 全選 / 全取消點樣用 JavaScript 做

### 問題背景

`UserVocab` list 想加一個額外 checkbox，控制目前畫面所有 `selected_ids` checkbox：

- tick all：當前頁全部設為 checked
- untick all：當前頁全部設為 unchecked
- 如果部分 checked，all checkbox 顯示 indeterminate

### 研究方向

- `id`、`class`、`name` 喺 HTML input 入面分別負責咩。
- 點樣用同一個 class group 起所有 row checkbox。
- `querySelectorAll()` 點樣一次搵晒同一 class 嘅 elements。
- checkbox 嘅 `checked` 同 `indeterminate` 狀態點樣更新。
- 「All」應該只代表當前 page / 當前 filter 顯示嘅 rows。

### 概念整理與解答

#### 1. `name` 俾 form submit 用，`class` 俾 JavaScript group 用

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

#### 2. Template 例子

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

#### 3. JavaScript 例子

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

#### 4. 點解要用 `querySelectorAll(".in-use-checkbox")`

因為每個 row checkbox 都有同一個 class：

```html
class="in-use-checkbox"
```

所以：

```javascript
document.querySelectorAll(".in-use-checkbox")
```

會搵晒所有 row checkbox，之後可以用 `forEach()` 逐個改 `checked` 狀態。

#### 5. All 只代表當前畫面

如果有 pagination / filter，All checkbox 通常只代表目前頁面顯示嘅 rows。

原因係 POST 只會提交目前頁面嘅：

```text
selectable_ids
selected_ids
```

所以 all checked / unchecked 只應影響當前 page / 當前 filter，而唔係全 database 所有 `UserVocab`。

### 理解內容

-

## [ ] `[DJANGO-MODEL-MULTIPLE-CHOICE-BULK-SELECT-FLOW]` 用 `ModelMultipleChoiceField` 做批量選擇 object 嘅處理流程

### 問題背景

之前為 `UserVocabSelectVocabView` 設計過一個 flow：

- View 顯示一批 user 未擁有嘅 `Vocab`。
- User 用 checkbox 選擇想加入自己 list 嘅 vocab。
- Submit 後 view 將選中 vocab 交俾 service 建立 `UserVocab` relationship。

目前新設計改成 login 後自動建立 `UserVocab(in_use=False)`，所以暫時唔用呢個 flow 做加字。
但呢個 pattern 之後仍然可能用喺其他「從一批 model objects 入面勾選多個」嘅功能，所以保留做學習筆記。

### 研究方向

- `ModelMultipleChoiceField` 點樣將 POST ids 轉成 model objects。
- 點解 field 初始 queryset 要用 `Model.objects.none()`。
- 點解要喺 form `__init__()` 動態注入 queryset。
- `FormView.get_form_kwargs()` 點樣將 view context 傳入 form。
- `cleaned_data["vocabs"]` 點解唔係 raw ids，而係 queryset / model objects。
- 點解 sliced queryset 可能令 `ModelMultipleChoiceField` POST validation 出問題。

### 概念整理與解答

#### 1. Form 負責接收一批可選 vocab

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

#### 2. View 決定目前 user 可選邊批 vocab

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

#### 3. `ModelMultipleChoiceField` 做緊咩

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

#### 4. Service 負責建立 relationship

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

#### 5. 點解要小心 sliced queryset

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

#### 6. 呢個 pattern 之後可以用喺邊

呢個 flow 適合：

- 從候選 vocab 入面批量加入 user list。
- 從候選 users 入面批量 assign permission / group。
- 從候選 items 入面批量建立 relationship。
- 任何「畫面 show 一批合法 objects，user checkbox 選多個，submit 後建立關係」嘅情境。

如果 UI 係一個 list table，每行要顯示 word / kana / meaning，再手寫 checkbox，仍然可以保留同一個核心概念：

- 用 hidden / checkbox value 提交 object id。
- 用 form field 或 view queryset 驗證 ids 屬於目前 user 可操作範圍。
- service 只處理通過 validation 嘅 objects。

### 理解內容

-

## [ ] `[DOMAIN-VOCAB-USERVOCAB-IN-USE]` `Vocab` 同 `UserVocab.in_use` 嘅設計心智模型

### 問題背景

目前 `Vocab` 代表全站共用嘅 vocabulary pool，而 `UserVocab` 代表某個 user 同某個 vocab 之間嘅個人 learning relationship。

新增設計：

- 新 vocab 可以自動加入 user 嘅 `UserVocab`。
- 但新建立嘅 `UserVocab.in_use` 預設係 `False`。
- User 之後可以喺自己嘅 vocab list 入面決定邊啲字要啟用。
- Quiz question pool 只應使用 `in_use=True` 嘅 `UserVocab`。

### 研究方向

- 點解唔應該因為 user 暫時唔想練某個字，就刪除 `Vocab`。
- 點解 `UserVocab` 唔只係 many-to-many join table，而係 user 個人 learning state。
- `in_use=False` 同刪除 `UserVocab` 有咩分別。
- EventNotice 系統點樣通知 user 有新字可啟用。
- Quiz pool 點樣只取 user 已啟用嘅 vocab。

### 概念整理與解答

#### 1. 連鎖餐廳 menu 比喻

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

#### 2. `Vocab` 係總資料，`UserVocab` 係個人狀態

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

#### 3. 點解用 `in_use=False`，而唔係唔建立 `UserVocab`

如果唔建立 `UserVocab`：

- 系統唔容易知道呢個 user 有冇收過呢個字。
- EventNotice 之後難以追蹤 user 有邊啲新字未處理。
- User list 入面無法顯示「可啟用但未啟用」嘅字。

如果建立 `UserVocab(in_use=False)`：

- 系統知道呢個字已經派到 user 個人 list。
- User 可以 filter `in_use=False` 睇未啟用字。
- EventNotice 可以提醒 user 有新字可處理。
- Quiz pool 仍然可以保持乾淨，只抽 `in_use=True`。

#### 4. 點解唔直接刪 `UserVocab`

刪除 `UserVocab` 代表失去 user 對呢個 vocab 嘅個人 record。

但 `in_use=False` 代表：

- 個 record 仲存在。
- User 暫時唔練。
- 之後可以重新啟用。
- 如有需要，quiz stats / learning history 可以繼續保留。

所以 `in_use` 比 delete 更適合表示「暫時不用」。

#### 5. 對 quiz pool 嘅影響

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

### 理解內容

-

## [ ] `[DJANGO-ADMIN-FIELD-BUTTON-CUSTOM-URL]` Admin change form 用 readonly field 顯示 action link 嘅做法

### 問題背景

之前曾經試過喺 `VocabRequestAdmin` 入面用一個 readonly field / display method 顯示 approve / reject button link。

大概做法係：

- 定義 `review_buttons()`。
- 用 `@admin.display(description="Review")` 將佢包裝成 admin 顯示欄位。
- 喺 `readonly_fields` / `fields` 入面加入 `review_buttons`。
- 用 `format_html()` 回傳 approve / reject `<a>` link。
- override `get_urls()` 加入 admin custom URLs。
- custom URL 進入 `approve_view()` / `reject_view()`，再 call service。

### 研究方向

- `@admin.display` 點樣令 method 變成 admin 欄位。
- `readonly_fields` 入面除咗 model field，點解亦可以放 admin method name。
- `format_html()` 點解比直接拼 HTML string 安全。
- `ModelAdmin.get_urls()` 點樣加 custom admin URL。
- `self.admin_site.admin_view()` 點樣套用 admin permission / staff check / CSRF 等 admin protection。
- 點解用 `<a href="...">` 做 approve / reject 會有 GET side effect 問題。
- 點解之後改用 change form submit button + POST flow。

### 概念整理與解答

#### 1. 用 admin method 當 readonly field

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

#### 2. 用 `format_html()` 產生 admin button link

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

#### 3. 用 `get_urls()` 加 admin custom URL

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

#### 4. Custom approve / reject view

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

#### 5. 呢個做法有咩問題

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

#### 6. 點解最後改用 change form submit button

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

#### 7. 兩種做法點樣選

Readonly field + custom URL approach 適合：

- action 真係想做成獨立 endpoint。
- 想將 action 同 admin change form save flow 分開。
- 願意自己處理 POST form、CSRF、permission、transaction、redirect。

Change form submit button approach 適合：

- action 本身係 review / approve 呢類 change form workflow。
- 想保留 admin 原生 form validation / save / message / redirect flow。
- 想喺同一頁 review proposed data 後直接 approve / reject。

今次 project 最後選擇 change form submit button，因為 approve / reject 係 `VocabRequest` review workflow，跟 change form 關係較密切。

### 理解內容

-

## [ ] `[DJANGO-ADMIN-RESPONSE-CHANGE-CHANGEFORM-VIEW]` Admin approve / reject 點樣處理 form save 同 row lock

### 問題背景

`VocabRequestAdmin` 目前喺 admin change form 入面用 custom buttons 做 approve / reject，並喺 `response_change()` 入面判斷：

```python
if "_approve" in request.POST:
    ...
if "_reject" in request.POST:
    ...
```

但 `response_change()` 係 Django Admin 保存 change form 之後先呼叫嘅 hook。即係如果 admin 同一次 POST 又修改 proposed data、又撳 approve，Django Admin 可能已經先保存咗 form data，然後先進入 approve service。

目前 service 入面雖然使用 `transaction.atomic()` 同 `select_for_update()`，但個 row lock 主要保護 approve / reject 階段，未必保護到 admin form save proposed data 嗰一下。

### 研究方向

- `ModelAdmin.response_change()` 喺 Django Admin save lifecycle 入面幾時被呼叫。
- 點樣偵測 admin 撳 approve / reject 時，form 有冇 unsaved changes。
- 點解簡單解法可以先要求 admin save changes，再 approve / reject。
- 如果要真正將「form validation + save + approve / reject」放入同一個 transaction / row lock，點樣 override `changeform_view()`。
- `select_for_update()` 必須放喺 `transaction.atomic()` 裡面先有意義。

### 概念整理與解答

#### 1. 簡單解法：approve / reject 前擋住 unsaved changes

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

#### 2. 呢個簡單解法未解決咩

簡單解法只係流程保護，唔係真正 database-level solution。

例如兩個 admin 同時打開同一個 request：

1. Admin A save proposed data。
2. Admin B 用舊畫面 save proposed data。
3. 後 save 嗰個可能覆蓋前一個。

如果要完整處理呢類 concurrency，就要喺更早位置控制 transaction boundary。

#### 3. 長遠解法：override `changeform_view()`

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

#### 4. 點解呢個比 `response_change()` 更適合長遠解法

`response_change()` 適合做「save 完之後 redirect 去邊、顯示咩 message、額外做咩 action」。

但如果目標係控制：

- form validation
- object save
- approve / reject action
- row lock
- transaction boundary

就需要喺更外層嘅 lifecycle 介入，所以 `changeform_view()` 會係更值得研究嘅 hook。

#### 5. 目前建議

短期：

- 先喺 `response_change()` approve / reject branch 偵測 `form.has_changed()`。
- 如果 admin 有 unsaved changes，就要求先 Save。
- 保留目前 service 入面嘅 `transaction.atomic()` + `select_for_update()` 保護 approve / reject 階段。

長期：

- 研究 `changeform_view()` 同 Django Admin save lifecycle。
- 再考慮將 form save + approve / reject 放入同一個 locked transaction。

#### 6. 今次 project 實際採用嘅處理手法

今次最後採用嘅做法唔係 override `changeform_view()`，而係用較簡單、較貼近現有 admin flow 嘅方式處理。

核心思路：

- 喺 admin approve / reject POST 時，盡早鎖住 `VocabRequest` row。
- Service 入面仍然保留自己嘅 status check 同 row lock。
- Request 一旦 reviewed，就唔再俾 admin 改 proposed data。

##### 6.1 Admin POST 時 early lock

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

##### 6.2 Service 仍然保留 self-lock

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

##### 6.3 Reviewed request 變 readonly

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

##### 6.4 `save_model()` 做最後防線

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

##### 6.5 呢個做法解決咗咩

今次做法主要處理：

- Admin approve / reject POST 時，form save 前盡早 lock row。
- Service approve / reject 階段仍然有 transaction + row lock + pending status check。
- Reviewed request 唔再俾 admin 修改，避免舊頁面或第二個 admin 覆蓋已 review record。

##### 6.6 仲有咩要之後驗證

呢個做法比純粹喺 `response_change()` 做 service call 穩陣好多，但之後仍然值得用 tests 驗證：

- 兩個 admin 同時打開同一個 pending request。
- Admin A approve 後，Admin B 用舊頁面 submit。
- Admin A / B 幾乎同時 approve。
- Reviewed request 是否確實無法再 save proposed data。

如果之後發現 admin lifecycle 仍然有更深層嘅 race condition，再研究 override `changeform_view()` 或獨立 custom admin view。

### 理解內容

-

## [ ] `[DJANGO-CATCH-INTEGRITY-ERROR-AROUND-ATOMIC]` 點解要喺 `transaction.atomic()` 外面捕捉 `IntegrityError`

### 問題背景

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

### 研究方向

- `transaction.atomic()` 點樣判斷應該 commit 定 rollback。
- Database error 發生後，transaction 點解會進入 broken state。
- 點解 exception 要穿過 atomic context manager。
- `TransactionManagementError` 通常喺咩情況出現。
- 如果只得單一 `objects.create()`，仲需唔需要額外使用 `atomic()`。

### 概念整理與解答

#### 1. `atomic()` 需要見到 exception

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

#### 2. Catch 喺 atomic 入面有咩問題

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

#### 3. `except` 放喺外面嘅安全邊界

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

#### 4. 如果 atomic 入面有多個操作

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

#### 5. 只有一個 `objects.create()` 時

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

#### 6. 逐筆 transaction 同整批 transaction

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

#### 7. 最簡單記法

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
except IntegrityError:
    # rollback 已完成
    # safe error handling
```

### 理解內容

-

## [ ] `[DJANGO-SLICED-QUERYSET-MULTIPLE-CHOICE]` Sliced QuerySet 點解唔可以直接交俾 `ModelMultipleChoiceField`

### 問題背景

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

### 研究方向

- QuerySet slicing `[:50]` 會點樣改變 QuerySet。
- 點解 sliced QuerySet 唔可以再使用 `.filter()`。
- `ModelMultipleChoiceField` 驗證 submitted IDs 時會做咩。
- 點解 GET 顯示正常，但 POST validation 先出錯。
- 點樣限制候選數量，同時保留可以再 filter 嘅 QuerySet。

### 概念整理與解答

#### 1. `[:50]` 會建立 sliced QuerySet

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

#### 2. 點解 sliced QuerySet 唔可以再 filter

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

#### 3. 自己冇 `.filter()`，點解仍然會出錯

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

#### 4. 解法：先取得有限數量嘅 IDs

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

#### 5. 再建立一個未 sliced QuerySet

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

#### 6. 排序注意事項

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

#### 7. `id__in` 解法嘅核心概念

```text
內層 QuerySet
-> 排序及限制頭 50 個 IDs

外層 QuerySet
-> 根據呢批 IDs 重新查詢
-> 本身冇 slice
-> 可以交俾 ModelMultipleChoiceField 再 filter
```

### 理解內容

-

## [ ] `[DJANGO-RELATION-FIELD-RELATED-NAME]` Relation 應該用 field name 定 `related_name`

### 問題背景

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

### 研究方向

- 正向 relation 同 reverse relation 有咩分別。
- 乜嘢情況使用 field name。
- 乜嘢情況使用 `related_name`。
- `vocab.users` 同 `vocab.user_vocab` 回傳嘅 object type 有咩不同。
- Through model 額外 fields，例如 `weight` 同 `streak`，應該經邊條 relation 取得。
- ORM filter 入面 relation name 點樣使用。

### 概念整理與解答

#### 1. 核心規則

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

#### 2. 由 `Vocab` 直接取得 users

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

#### 3. 由 `Vocab` 取得 `UserVocab` records

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

#### 4. 由 `UserVocab` 取得兩邊 object

`user` 同 `vocab` 都係直接定義喺 `UserVocab` 嘅 fields，所以使用 field name：

```python
user_vocab.user
user_vocab.vocab
```

呢度唔使用 `related_name`，因為行緊嘅係正向 relation。

#### 5. 由 `User` 反方向取得資料

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

#### 6. 目前 model 嘅 relation 對照

| 起點 | 寫法 | 結果 |
| --- | --- | --- |
| `Vocab` | `vocab.users.all()` | `User` QuerySet |
| `Vocab` | `vocab.user_vocab.all()` | `UserVocab` QuerySet |
| `User` | `user.vocabs.all()` | `Vocab` QuerySet |
| `User` | `user.user_vocab.all()` | `UserVocab` QuerySet |
| `UserVocab` | `user_vocab.user` | 單一 `User` object |
| `UserVocab` | `user_vocab.vocab` | 單一 `Vocab` object |

#### 7. ORM filter 嘅例子

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

#### 8. 今次問題嘅直接答案

如果目標只係由 vocab 取得 users：

```python
vocab.users.all()
```

如果要同時使用 `UserVocab` 入面嘅 quiz data：

```python
vocab.user_vocab.select_related("user")
```

所以唔係永遠只用 field name，亦唔係永遠只用 `related_name`；要睇 relation field 定義喺起點 model，定係由另一邊反向查詢。

### 理解內容

-

## [ ] `[DJANGO-UNIQUE-CONSTRAINT]` `UniqueConstraint` 同 conditional unique constraint

### 問題背景

目前 `Vocab` 同 `VocabRequest` 使用 database constraints 防止重複資料：

```python
models.UniqueConstraint(
    fields=["word", "kana"],
    name="word_kana_unique",
)
```

`VocabRequest` 亦使用帶有 `condition=Q(...)` 嘅 conditional unique constraints，只限制符合特定狀態嘅 records。

### 研究方向

- `UniqueConstraint` 同 field 上嘅 `unique=True` 有咩分別。
- 多個 fields 放入同一個 constraint 代表咩。
- `condition=Q(...)` 點樣令 unique rule 只套用喺部分 records。
- 點解 service 已經用 `.exists()` 檢查，database 仍然需要 constraint。
- Constraint 觸發時點解會出現 `IntegrityError`。
- SQLite 同 PostgreSQL 對 conditional unique constraint 嘅支援有咩差異。

### 概念整理與解答

#### 1. 普通 `UniqueConstraint`

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

#### 2. 同 `unique=True` 嘅分別

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

#### 3. Conditional unique constraint

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

#### 4. Create request 使用嘅 constraint

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

#### 5. `Q()` 係咩

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

#### 6. 點解 `.exists()` 之後仍需要 constraint

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

#### 7. Migration 同 database 支援

新增或修改 constraint 後，需要建立及套用 migration：

```bash
python manage.py makemigrations
python manage.py migrate
```

Conditional unique constraint 會依賴 database 對 partial unique index 嘅支援。SQLite 新版本同 PostgreSQL 支援呢種設計，但實際部署前仍應以目標 database 測試 constraint 行為。

### 理解內容

-

## [ ] `[DJANGO-ADMIN-MESSAGE-USER]` `ModelAdmin.message_user()` 係咩

### 問題背景

目前喺 `dictionary/admin.py` approve / reject flow 使用：

```python
self.message_user(
    request,
    "Message content",
    messages.SUCCESS,
)
```

但仲未理解 `self.message_user()` 係邊個 class 提供、訊息儲存喺邊、點樣顯示，同 Django messages framework 有咩關係。

### 研究方向

- `self` 點解係 `VocabRequestAdmin` instance，而唔係 Django view。
- `ModelAdmin.message_user()` 同 `django.contrib.messages` 嘅關係。
- `request` 參數點解必須傳入。
- `messages.SUCCESS`、`WARNING`、`ERROR` 等 level 有咩作用。
- 訊息係暫存在 session、cookie，定係 database。
- 點解 redirect 去另一個 admin page 後，訊息仍然可以顯示一次。
- `message_user()` 同直接使用 `messages.success(request, ...)` 有咩分別。

### 概念整理與解答

#### 1. `self.message_user()` 係邊度嚟

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

#### 2. 點解一定要傳入 `request`

訊息係屬於目前進行操作嘅 user/request，而唔係屬於 `VocabRequest` model。

`request` 可以令 Django messages framework 知道：

- 邊一個 user/browser 應該收到訊息。
- 應該將訊息暫存喺邊個 session 或 cookie。
- Redirect 後下一個頁面應該顯示邊啲訊息。

#### 3. Message level 有咩作用

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

#### 4. 點解 redirect 後仲見到訊息

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

#### 5. 同 `messages.success()` 有咩分別

以下兩種寫法目的相近：

```python
self.message_user(request, "Approved.", messages.SUCCESS)
```

```python
messages.success(request, "Approved.")
```

`message_user()` 係 `ModelAdmin` 提供嘅方便接口，適合 admin class 內使用；`messages.success()` 係通用 messages framework API，可以喺一般 Django view 使用。

#### 6. `"; ".join(...)` 係咩

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

#### 7. 用嚟顯示 `ValidationError`

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

### 理解內容

-

## [ ] `[PYTHON-SET-DIFFERENCE-CSV-HEADERS]` 點樣用 set 差集檢查 CSV 缺少嘅 headers

### 問題背景

目前 `import_vocab.py` 使用：

```python
missing_headers = required_headers - set(reader.fieldnames or [])
```

檢查 CSV 有冇缺少 command 要求嘅 headers，但仲未完全理解 set 減法同 `or []` 點樣運作。

### 研究方向

- Python `set` 係咩資料結構。
- 兩個 sets 使用 `-` 時會得到咩結果。
- `csv.DictReader.fieldnames` 會提供咩資料。
- 點解要將 `reader.fieldnames` 轉成 set。
- 點解要寫成 `reader.fieldnames or []`。
- 空 CSV 或冇 header 時會發生咩事。

### 概念整理與解答

#### 1. Set 差集

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

#### 2. `reader.fieldnames or []`

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

#### 3. 完整流程

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

### 理解內容

-

## [ ] `[DJANGO-CBV-OBJECT-ID]` Detail／Update／Delete View 點樣取得目標 Object

### 問題背景

目前對 User detail、Vocab detail、UpdateView 同 DeleteView 點樣指定及取得目標 object 的 pk／ID 仲未完全理解。

### 研究方向

- URL pattern 入面 `<int:pk>`、`<int:vocab_id>` 等參數有咩分別。
- URL 傳入的 ID 點樣進入 `self.kwargs`。
- Django generic `DetailView`、`UpdateView`、`DeleteView` 預設點樣使用 `pk_url_kwarg` 尋找 object。
- 使用預設 `pk` 同自訂 `vocab_id` 時，需要喺 View 加咩設定。
- `get_object()`、`get_queryset()` 同 `get_context_data()` 各自負責咩。
- 點解目前 User detail 可以直接使用登入中的 `request.user`，但 Vocab detail 需要根據 URL ID 查詢。

### 概念整理與解答

#### 1. ID 由 URL 開始傳入

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

#### 2. 目前 Vocab detail 點樣取得 Object

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

#### 3. 目前 Update／Delete 點樣取得 Object

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

#### 4. Generic DetailView／UpdateView／DeleteView 的預設行為

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

#### 5. 想保留 vocab_id 名稱時

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

#### 6. get_object、get_queryset、get_context_data 的分工

- `get_queryset()`
  - 決定容許由邊一批 records 之中尋找 object。
  - 可以加入 `is_active=True`、user ownership、permission scope 等限制。

- `get_object()`
  - 從 queryset 中，根據 URL 的 pk 或 slug 取得單一 object。
  - 結果通常存入 `self.object`。

- `get_context_data()`
  - 將已取得的 object 及其他資料交俾 template。
  - 唔應將所有 object lookup 邏輯都塞入呢度，除非使用的係 `TemplateView` 並選擇手動處理。

#### 7. 點解 User detail 無傳 ID

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

#### 8. 最重要的分別

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

### 理解內容

- 

## [ ] `[PYTHON-ENUMERATE-CSV-ROWS]` `enumerate()` 點樣提供 CSV 行數同資料

### 問題背景

目前 `import_vocab.py` 使用：

```python
for row_number, data in enumerate(reader, start=2):
```

逐行讀取 CSV，但仲想進一步理解 `enumerate()`、`row_number`、`data` 同 `start=2` 各自有咩作用。

### 研究方向

- `csv.DictReader` 每次 iteration 會回傳咩資料。
- `enumerate()` 點樣為 iterable 加上編號。
- 點解可以同時寫 `row_number, data`。
- `start=2` 係咪會跳過 CSV 頭兩行。
- 點樣用真實 CSV 行數顯示清楚嘅 error message。

### 概念整理與解答

#### 1. `reader` 每次提供一行資料

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

#### 2. `enumerate()` 加入編號

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

#### 3. 點解使用 `start=2`

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

#### 4. 點解唔可以直接寫 `for row_number, data in reader`

`reader` 每次只回傳一個 dictionary，唔會自動附帶行數。直接要求拆成 `row_number` 同 `data`，Python 會嘗試拆解 dictionary keys，通常會出現 unpacking error。

要同時取得編號同資料，需要由 `enumerate()` 將每項包成兩個 values。

### 理解內容

-

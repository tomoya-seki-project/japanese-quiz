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

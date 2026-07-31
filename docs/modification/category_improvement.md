# Category Improvement Report

## 目的

今次改動係將 dictionary app 原本單一 category 設計，改成一個 vocab 可以擁有 1 至 3 個 categories。

舊設計：

- `Vocab.category`：單一 `CharField`
- `VocabRequest.proposed_category`：單一 proposed category
- choices 由 `VocabCategory` `TextChoices` 固定寫死

新設計：

- `Category` model 管理 category master data
- `Vocab.categories` 使用 `ManyToManyField`
- `VocabRequest.proposed_categories` 使用 `ManyToManyField`
- Vocab create / update / restore request 都保存 proposed categories snapshot
- Vocab list / user vocab list search 改用 M2M categories filter

## 設計原因

單一 category 太限制 vocab 分類。部分字可以同時屬於多個語義場景，例如：

- `食事・料理`
- `日常生活`
- `文化・娯楽`

改成最多三個 categories 後，可以保持資料彈性，同時避免 category 過多令 quiz / filter / admin review 變得混亂。

## Database / Model 變更

### 新增 `Category`

新增 `Category` model 作為 category master table。

主要欄位：

- `name`：系統內部使用，unique
- `display`：畫面顯示文字

`__str__()` 使用：

```python
return self.display or self.name
```

避免 `display` 為空時 admin / form dropdown 出現問題。

### `Vocab` 改動

新增：

```python
categories = models.ManyToManyField(
    Category,
    related_name="vocabs",
)
```

移除：

```python
category = models.CharField(...)
```

即係 `Vocab` 不再保存 legacy single category，category 資料以 M2M `categories` 作為唯一來源。

### `VocabRequest` 改動

新增：

```python
proposed_categories = models.ManyToManyField(
    Category,
    related_name="vocab_requests",
    blank=True,
)
```

移除：

```python
proposed_category = models.CharField(...)
```

即係 review request 亦不再保存單一 proposed category，而係保存 proposed categories snapshot。

### 移除 `VocabCategory`

舊有 `VocabCategory(TextChoices)` 已移除。

Category choices 由 database `Category` table 提供，不再硬編碼喺 model enum 入面。

## Migration

相關 migration：

- `0020_categories_prepare.py`
  - 新增 `Category`
  - 新增 `Vocab.categories`
  - 新增 `VocabRequest.proposed_categories`

- `0021_category_change.py`
  - 調整 `Category.display`
  - 調整 `VocabRequest.proposed_categories` blank 設定

- `0022_remove_vocab_category_and_more.py`
  - 移除 `Vocab.category`
  - 移除 `VocabRequest.proposed_category`

`0022` 已經成功套用：

```text
Applying dictionary.0022_remove_vocab_category_and_more... OK
```

## Category Seed Data

新增：

```text
resource/categories.csv
```

用作 category master data seed source。

新增 management command：

```text
dictionary/management/commands/setup_categories.py
```

用途：

- 從 CSV 建立 category
- 已存在時 update display
- 支援重複執行
- 會記錄成功 / 失敗 rows

已測試成功建立 / 更新 18 筆 `Category` records。

## Form 變更

### `BaseVocabRequestForm`

新增：

```python
categories = forms.ModelMultipleChoiceField(
    queryset=Category.objects.all(),
    required=False,
    widget=forms.CheckboxSelectMultiple,
)
```

並加入：

```python
def clean_categories(self):
    categories = self.cleaned_data["categories"]
    if categories.count() > 3:
        raise forms.ValidationError("Allow 3 type of category only")
    return categories
```

作用：

- 由 database `Category` records 產生選項
- admin / user request form 可選多個 categories
- 限制最多三個 categories

### `VocabCreateRequestForm`

Create request 仍然容許 user submit 時留空：

- `meaning`
- `level`
- `categories`

原因係 admin review 時可以再補齊。

### `VocabUpdateRequestForm`

Update request 透過 view initial 將現有 categories 帶入 form。

## View 變更

### `VocabUpdateRequestView.get_initial()`

新增：

```python
"categories": vocab.categories.all()
```

令 update form 可以 tick 返現有 categories。

舊有：

```python
"category": vocab.category
```

已移除。

### `VocabListView`

Search form category 改成 `ModelChoiceField` 後，filter 改成：

```python
qs = qs.filter(categories=category)
```

### `UserVocabListView`

User vocab list 要經 `UserVocab -> Vocab -> categories` filter：

```python
qs = qs.filter(vocab__categories=category)
```

## Service 變更

### `VocabRequestService.gen_create_vocab_request()`

Create request 建立後：

```python
create_request.proposed_categories.set(form.cleaned_data["categories"])
```

不再寫 `proposed_category`。

### `VocabRequestService.gen_update_vocab_request()`

Update request 建立後：

```python
update_request.proposed_categories.set(form.cleaned_data["categories"])
```

`original_data` 入面改為保存原本 category names snapshot：

```python
"categories": list(
    form.target_vocab.categories.values_list("name", flat=True)
)
```

### `VocabRequestService.gen_restore_vocab_request()`

Restore request 會保存原 vocab 嘅 categories snapshot：

```python
restore_request.proposed_categories.set(vocab.categories.all())
```

Approve restore 時仍然只做：

```python
original_vocab.is_active = True
```

即係 proposed categories 主要係 review record / snapshot，用嚟保持 request data 完整。

### `VocabRequestService.validate_for_approval()`

舊檢查：

```python
proposed_category
```

已改成：

```python
if not vocab_request.proposed_categories.exists():
    errors["proposed_categories"] = "Category is required."
```

Create / update approve 前必須有最少一個 proposed category。

### `VocabRequestService.build_vocab_data()`

傳俾 vocab action 嘅資料改成：

```python
"categories": vocab_request.proposed_categories.all()
```

不再傳 `"category"`。

### `VocabActionService.create_vocab()`

建立 `Vocab` 時不再設定 single category。

流程：

1. 建立 `Vocab` main object
2. `vocab.full_clean()`
3. `vocab.save()`
4. `vocab.categories.set(vocab_data["categories"])`

M2M 要等 main object 有 primary key 後先可以 `.set()`。

### `VocabActionService.update_vocab()`

Update vocab 時不再更新 single category。

改成：

```python
target_vocab.categories.set(vocab_data["categories"])
```

## Admin 變更

### `CategoryAdmin`

新增 `CategoryAdmin`，方便管理 category master data。

顯示：

- `name`
- `display`
- `create_at`

### `VocabAdmin`

`categories` 改成 checkbox widget：

```python
def formfield_for_manytomany(self, db_field, request, **kwargs):
    if db_field.name == "categories":
        kwargs["widget"] = forms.CheckboxSelectMultiple
    return super().formfield_for_manytomany(db_field, request, **kwargs)
```

### `VocabRequestAdmin`

Review form 加入：

```python
proposed_categories
```

移除：

```python
proposed_category
```

`proposed_categories` 同樣使用 checkbox widget。

Reviewed request 會透過 `get_form()` disable M2M field：

```python
if obj is not None and obj.status != VocabRequestStatus.PENDING:
    if "proposed_categories" in form.base_fields:
        form.base_fields["proposed_categories"].disabled = True
```

原因係 `ManyToManyField` 未必完全受 `readonly_fields` 控制，所以要額外喺 form 層 disable。

## Import Command 變更

`import_vocab` CSV header 使用：

```text
category1, category2, category3
```

流程：

1. 讀取 `category1`、`category2`、`category3`
2. 忽略空值及 `---`
3. 用 `Category.objects.filter(name__in=category_names)` 取得 categories
4. 檢查 CSV 入面嘅 category name 是否存在
5. 傳入 `VocabActionService.create_vocab()`

傳入資料：

```python
"categories": categories
```

不再傳：

```python
"category": data["category1"]
```

## Search / Filter 變更

### Form

`VocabSearchForm` / `UserVocabSearchForm` category field 改為：

```python
category = forms.ModelChoiceField(
    queryset=Category.objects.all(),
    required=False,
    empty_label="-----",
)
```

### Query

Vocab list：

```python
qs.filter(categories=category)
```

User vocab list：

```python
qs.filter(vocab__categories=category)
```

## 測試 / 驗證

已完成檢查：

```text
manage.py check
```

結果：

```text
System check identified no issues (0 silenced).
```

已完成 migration 檢查：

```text
manage.py makemigrations --check --dry-run
```

結果：

```text
No changes detected
```

已完成 syntax compile：

```text
py_compile
```

結果：通過。

已完成 migration：

```text
manage.py migrate
```

結果：

```text
Applying dictionary.0022_remove_vocab_category_and_more... OK
```

已手動測試：

- categories checkbox selection
- reviewed request 入面 `proposed_categories` disabled
- create / restore / update / delete request
- approve / reject flow
- vocab list category filter
- user vocab list category filter

## 最終狀態

目前 category system 已完成由 single category 遷移到 1 至 3 個 M2M categories。

目前唯一 category source：

- `Vocab.categories`
- `VocabRequest.proposed_categories`

舊欄位已移除：

- `Vocab.category`
- `VocabRequest.proposed_category`

舊 enum 已移除：

- `VocabCategory`

## 之後注意事項

### 1. Existing data migration

如果 production / long-lived database 已有舊 `Vocab.category` data，要喺 drop column 前做 data migration，將舊 category 搬去 M2M table。

今次 development flow 已經直接清走舊欄位。

### 2. Category count rule

目前 form 層限制最多三個 categories。

如果將來有其他入口直接 call service，例如 API / command，可能要考慮喺 service 或 model validation 再加一次限制。

### 3. Query performance

M2M filter 會 join through table。

目前資料量細，無問題。之後如果 vocab / user_vocab 數量大，可以再考慮：

- index
- prefetch
- query optimization

### 4. UI display

目前 list item 未必完整顯示 categories。

如果之後需要，可以喺 vocab list / user vocab list 加 category badges。

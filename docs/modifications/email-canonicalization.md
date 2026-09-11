# Email 大小寫統一：由不同 identity 到 lowercase 與唯一性保護

## Report 基準

- 產生時間：2026-09-11 21:18 JST。
- 主題：將 email 大小寫變體統一視作同一個登入 identity。
- 修改前：`HEAD`／`9062a2ea41e4e46f5f3b27fcaedf303be0e4f0d4`。
- 修改後：本次檢查時嘅 working tree；**尚未 commit**。
- 範圍：`accounts/models.py`、`accounts/forms.py`、新增 `accounts/migrations/0007_email_upper_lower_problem.py`。
- 周邊證據：既有 registration／login／resend views、admin form wiring、Django manager 實作及現有 tests。最近兩個 commits `9062a2e`（email activation）同 `012ae67`（quiz／review workflow）作背景；唔將其功能重算成今次修改。
- 排除：quiz M01、四份 status docs，以及 working tree 內舊 modification 文件刪除／新目錄整理。報告只建立本文件。
- Django 版本：requirements 固定 `6.0.5`，框架資料採用 Django 6.0 官方文件。
- 所有 after-code 行號指本次 working tree；例子 email 使用虛構 `example.com` 地址。

## 完成度檢查

目前已接通 public registration、login、activation resend、admin create／change，同 custom manager 嘅共用 normalize 規則；database migration 已套用，model state 無 migration drift。核心修改可記錄為已實作。

呢個完成範圍係現有入口嘅 lowercase policy 同 database 唯一性保護，唔包括舊資料自動合併、全部 Unicode email equivalence，或並行 duplicate request 嘅友善錯誤處理。現有 tests 未專門覆蓋 email identity，驗證限制見文末。

## 修改目的 1：統一所有入口使用嘅 email 標準形式

### 修改目的／理由

之前 custom user 用 email 登入，但普通 `unique=True` 按目前 SQLite 比較方式，唔會將 local-part 大小寫變體當成相同值。例如 `Learner@example.com` 同 `learner@example.com` 可以代表兩筆不同記錄。

Django 預設 `normalize_email()` 只將 domain 轉小寫，唔會將 `@` 前面全部轉小寫。今次產品決定係將**整個 email** 統一 lowercase；呢個係本 project identity policy，唔係聲稱世界上所有 mail server 都無視 local-part 大小寫。

### 受影響檔案與責任

- `accounts/models.py:8`：custom `UserManager` 保存唯一一份 normalize 規則。
- 既有 `create_user()`／`create_superuser()`：透過原有呼叫自動採用新規則。
- 各個 form：呼叫 manager，避免自行複製 `.lower()` 邏輯。

### 修改前

`accounts/models.py`，manager 冇 override `normalize_email()`；`create_user()` 原本已經有：

```python
email = self.normalize_email(email)
user = self.model(email=email, username=username, **extra_fields)
```

呢時使用繼承自 Django 嘅 domain-only normalization。例如輸入 `Learner@EXAMPLE.COM`，manager 會得到 `Learner@example.com`。

### 修改後

`accounts/models.py:11`，新增 override：

```python
@classmethod
def normalize_email(cls, email):
    return super().normalize_email(email).strip().lower()
```

### 前後差異與運作解釋

呼叫父類 normalize 後，再移除頭尾空白、將整個字串轉小寫：` Learner@EXAMPLE.COM ` 最終得到 `learner@example.com`。`create_user()` 原本用 `self.normalize_email()`，所以唔使改 caller 都會用到 override；`create_superuser()` 又會呼叫 `create_user()`，亦會經同一路。

但 ModelForm 保存 model 唔等於呼叫 `objects.create_user()`。因此只改 manager 並不足夠，下面各 form 仲需要明確使用呢個共用方法。

### 新使用技術

`BaseUserManager.normalize_email()` 原本已間接使用，今次新增 override。父類只處理 domain lowercase，所以需要額外 `.lower()` 先符合產品政策。[Django custom user manager](https://docs.djangoproject.com/en/6.0/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.normalize_email)

Python `@classmethod` 收到 class 作第一個參數 `cls`，唔需要依賴某一個 User record。`super()` 由繼承鏈取得父類行為。`.strip()` 同 `.lower()` 產生新字串，唔會自行修改 database；必須使用回傳值並保存先有作用。

## 修改目的 2：建立或修改帳戶時提早攔截重複 email

### 修改目的／理由

儲存前先查詢大小寫不敏感嘅 duplicate，可以喺 email field 顯示清楚錯誤。Admin 修改現有 user 時亦要排除自己，否則保留原 email 都會被誤判重複。

### 受影響檔案與責任

- `accounts/forms.py:36`：public `RegistForm.clean_email()`。
- `accounts/forms.py:128`：`UserCreationAdminForm.clean_email()`。
- `accounts/forms.py:100`：`UserChangeAdminForm.clean_email()`。
- 既有 admin 已將 add／change 指向上述獨立 forms，唔需要新增 admin wiring。

### 修改前

三個 forms 冇自訂 `clean_email()`，由 EmailField／ModelForm 做既有格式及 uniqueness validation。`RegistForm.save()` 嘅保存部分如下，今次無改動：

```python
user = super().save(commit=False)
user.set_password(self.cleaned_data['password'])
user.is_active = False
if commit:
    user.save()
return user
```

之前冇喺 form field cleaning 階段統一完整 email lowercase，亦冇本次新增嘅 `iexact` duplicate guard。

### 修改後

`accounts/forms.py:36`，public registration 新增：

```python
def clean_email(self):
    email = User.objects.normalize_email(
        self.cleaned_data["email"]
    )

    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError(
            "このメールアドレスはすでに登録されています。"
        )
    return email
```

Admin create 使用同一查詢結構，錯誤文字保留英文。Admin change 嘅差異係排除當前 user：`accounts/forms.py:105`。

```python
duplicated = (
    User.objects.filter(
        email__iexact = email
    ).exclude(
        pk=self.instance.pk
    ).exists()
)
if duplicated:
    raise ValidationError(
        "A user with this email address already exists."
    )
return email
```

### 前後差異與運作解釋

Form 先做 field 基本驗證，再呼叫 `clean_email()`。呢個 method 嘅回傳值會成為該 field 嘅 cleaned value，之後 ModelForm 用佢更新 model。漏咗 `return email` 就唔會保留你計好嘅 email 值。

`email__iexact` 係比較規則，唔會將已存在 record 改成小寫。`.exists()` 只問「有冇符合記錄」，因為呢度唔需要取得 User object。

Admin change 例如編輯 user A：查詢要排除 A 自己；如果另一個 B 用咗相同 lowercase email，仍然會拒絕。`self.instance.pk` 係目前編輯對象 ID，唔係登入中 admin 嘅 ID。

### 新使用技術

`clean_<fieldname>()` 係 Django form validation hook，唔需要 view 手動呼叫；`ValidationError` 會附加到該 field。它同跨欄位 `clean()` 嘅責任不同，呢度只處理 email 最適合 field hook。[Django form validation](https://docs.djangoproject.com/en/6.0/ref/forms/validation/)

QuerySet `filter()`／`exclude()`／`exists()` 已係 project 常用 pattern；今次組合成大小寫 duplicate check，同編輯時排除自身嘅規則。

## 修改目的 3：登入與重寄亦接受同一套 identity 輸入

### 修改目的／理由

只將註冊資料轉小寫，登入輸入仍保留大寫，就可能令同一個 user 用唔同大小寫登入失敗。Resend 亦應使用相同 normalize 入口，令各條 flow 對 email 嘅理解一致。

### 受影響檔案與責任

- `accounts/forms.py:88`：`UserLoginForm.clean_username()`。
- `accounts/forms.py:170`：`ResendActivationEmailForm.clean_email()`。
- 既有 LoginView／ResendActivationEmailView 已使用呢兩個 forms，views 無需修改。

### 修改前

`accounts/forms.py`，原 login form 使用 email 輸入 widget，但 field 名仍係 `username`：

```python
username = forms.EmailField(label='メールアドレス')
```

原 resend form 只有 field declaration，冇額外 clean hook：

```python
email = forms.EmailField(
    label="メールアドレス",
    max_length=254,
)
```

### 修改後

`accounts/forms.py:88`，login：

```python
def clean_username(self):
    return User.objects.normalize_email(
        self.cleaned_data["username"]
    )
```

`accounts/forms.py:170`，resend：

```python
def clean_email(self):
    return User.objects.normalize_email(
        self.cleaned_data["email"]
    )
```

### 前後差異與運作解釋

Login 唔係寫 `clean_email()`，因為 Django AuthenticationForm 嘅輸入 field 叫 `username`。Custom user `USERNAME_FIELD = 'email'` 決定 backend 用邊個 model field 查 identity，唔會自動改名 form field。

Field hook 先轉好 lowercase，再交畀 AuthenticationForm 嘅 authentication 步驟。因此已透過現有入口保存成小寫嘅 user，可以用大小寫變體登入。

Resend 原 view 已經使用 `email__iexact`；今次唔係首次令 resend 忽略大小寫，而係統一輸入規則，並靠其他建立入口與 database constraint 消除「查到多個帳戶，再任取 first」嘅根源。

### 新使用技術

冇新增 authentication backend；仍然使用既有 AuthenticationForm，只新增 field hook。Django form field cleaning 早於 form-level `clean()`，因此 normalize 可以喺 authentication 前完成。[Django cleaning 次序](https://docs.djangoproject.com/en/6.0/ref/forms/validation/)

## 修改目的 4：由 database 保證大小寫變體不能同時存在

### 修改目的／理由

Form check 同真正寫入唔係同一刻。兩個 request 可以同時查到「冇 duplicate」，所以 `.exists()` 唔能夠單獨保證唯一性。亦可能有 caller 繞過 forms。

### 受影響檔案與責任

- `accounts/models.py:51`：`Meta.constraints` 宣告 functional unique constraint。
- `accounts/migrations/0007_email_upper_lower_problem.py`：將 constraint 加入 database。

### 修改前

`accounts/models.py`，User 已有：

```python
email = models.EmailField(unique=True)
```

但冇本次新增嘅 `Lower("email")` constraint。原有 `unique=True` 今次仍然保留。

### 修改後

`accounts/models.py:51`：

```python
class Meta(AbstractUser.Meta):
    constraints = [
        models.UniqueConstraint(
            Lower("email"),
            name="user_email_ci_unique",
        ),
    ]
```

新 migration 嘅 operation：

```python
migrations.AddConstraint(
    model_name='user',
    constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('email'), name='user_email_ci_unique'),
),
```

### 前後差異與運作解釋

Database 比較 `LOWER(email)` 嘅結果是否唯一。即使 caller 傳入大寫變體，亦唔可以同既有 lowercase 等價記錄同時存在。

要分清楚：Python `.lower()` 轉換將要使用／儲存嘅值；database `Lower("email")` 定義比較表達式。Constraint **唔會自動將儲存值改為 lowercase**，亦唔會幫你合併舊資料。

`Meta(AbstractUser.Meta)` 保留父類 model metadata，同時加入 constraints。直接宣告全新 `class Meta:` 曾會令 migration 偵測到額外 model options 改變；最後版本只需要 AddConstraint。

Migration 冇 data-cleaning step。對其他已有資料嘅 database 套用之前，要先掃描 collisions、決定邊個帳戶保留同關聯資料處理方式；不能假設加 constraint 會自動處理。

### 新使用技術

Project 已用過 UniqueConstraint，但今次新用法係傳入 `Lower()` expression，建立 functional uniqueness，而唔只係 `fields=[...]`。實際由 database unique index／constraint 執行保護；Model Meta 只係宣告，migration 套用後先有 schema 保護。[Django UniqueConstraint](https://docs.djangoproject.com/en/6.0/ref/models/constraints/#uniqueconstraint)

並行寫入撞 constraint 時 database 會拒絕其中一次；呢個保證資料唔重複，唔等於 view 已有完整 IntegrityError-to-form-error handling。

## 整體行為改變

| 層次 | 負責乜 | 唔負責乜 |
| --- | --- | --- |
| Manager normalize | 統一完整 email lowercase／頭尾空白 | 唔自行寫 database |
| Form clean hooks | normalize、建立／編輯 duplicate check、提供錯誤 | 唔保證並行寫入唯一性 |
| Database Lower constraint | 防止 lowercase 等價值重複寫入 | 唔改寫原值、唔合併舊 records |

例如註冊 `Learner@EXAMPLE.COM`：form 得到 `learner@example.com`，檢查冇 duplicate 後保存。再註冊 `LEARNER@example.com` 會被攔截；登入輸入同樣轉為 lowercase。Admin 編輯同一個 user 保留原 email，因排除自己而唔會誤報。

## 測試及驗證結果

本次實際執行：

- `manage.py check`：0 issues。
- `manage.py showmigrations accounts`：`0007_email_upper_lower_problem` 顯示 `[X]`。
- `manage.py makemigrations --check --dry-run`：No changes detected。
- `manage.py test accounts core`：10 tests 通過，使用臨時 test database。
- `git diff --check`：通過。

已檢視既有測試分工：accounts 專用 tests 尚未建立，10 個既有 tests 主要係 UI／語系 regression。呢次冇新增測試，亦冇將全綠結果當作已覆蓋 duplicate、mixed-case login 或 concurrency。

已核對本機 Django BaseUserManager 源碼，確認預設 normalize 只 lowercase domain，同本次 override 嘅差別。

## 已知限制／未驗證事項

- Migration 已套用，但檔案仍 untracked；其他 clone 要取得 model、forms 同 migration 三者，先可以重建同一狀態。
- 此 migration 只加 constraint，冇 normalize 舊資料。歷史 mixed-case records 應先檢查；尤其 login 現在轉小寫，舊儲存值若仍有大寫可能受影響。
- 直接 `User(...).save()`、`QuerySet.update()` 或 raw SQL 未必經 manager normalize。Constraint 防 duplicate，唔保證每筆儲存值本身 lowercase。
- Python lowercase、SQL LOWER 同 database collation 對非 ASCII 字元未必完全等價；目前冇聲稱處理所有 Unicode／國際化 email equivalence，轉 PostgreSQL 時要重新驗證。
- 唔會移除 email 中間空白、dots 或 plus-address tag，亦唔合併 mail provider aliases。
- 並行 duplicate registration 嘅 constraint rejection 尚未有本次新增嘅友善錯誤處理；資料一致性同 response UX 係兩層工作。
- 專用自動 tests 尚待補：manager／forms normalize、admin 排除自己、mixed-case login／resend、database duplicate rejection。

## 官方參考資料

- [Django 6.0：BaseUserManager.normalize_email](https://docs.djangoproject.com/en/6.0/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.normalize_email)
- [Django 6.0：Form and field validation](https://docs.djangoproject.com/en/6.0/ref/forms/validation/)
- [Django 6.0：UniqueConstraint 與 functional expressions](https://docs.djangoproject.com/en/6.0/ref/models/constraints/#uniqueconstraint)

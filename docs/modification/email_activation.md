# Email Activation Improvement Report

## 目的

今次改動係為 public registration加入 email activation。新註冊帳戶唔可以即時登入，必須先經 email入面嘅認證連結確認地址，先會將帳戶設成 active。

同時加入 activation email resend flow，處理以下情況：

- User遺失或收唔到第一次認證信。
- 第一次寄信失敗，但 inactive account已經建立。
- Activation link已過期或無效。
- User嘗試喺未完成認證前登入。

今次選用 Django stateless token generator，唔建立 token model。Password reset暫時未實作，之後會使用 Django內建 password reset flow及獨立 generator用途。

## 原有流程

原本 public registration流程：

```text
提交 RegistForm
→ 建立預設 is_active=True user
→ 立即建立 UserVocab
→ redirect 到受 login保護嘅 user home
```

主要問題：

- Email未經確認已經可以登入。
- 無法確認註冊者是否真正控制該 email address。
- Registration時已經為未確認身份嘅 user建立大量 `UserVocab`。
- 未有 activation link、有效期限、無效狀態及 resend處理。

## 新流程

新 registration及 activation流程：

```text
提交 RegistForm
→ 建立 is_active=False user
→ 產生 uidb64及 activation token
→ 寄出 activation email
→ redirect 到檢查 email頁面
→ user GET打開 activation link
→ 顯示確認頁，但唔改 database
→ user POST確認啟用
→ is_active=True
→ 建立／同步 UserVocab
→ 顯示成功頁及登入連結
```

Resend流程：

```text
User輸入 email
→ 驗證 email格式
→ 只查找同 email相符嘅 inactive user
→ 檢查每個 user嘅 resend cooldown
→ 符合條件先重新寄信
→ 所有有效格式輸入都顯示同一個完成頁
```

## 設計決定：Stateless Token

今次比較過兩個方向：

- 方案 A：建立 database model保存 token、expires time及使用狀態。
- 方案 B：使用 `PasswordResetTokenGenerator`衍生專用 activation token。

最終選用方案 B，原因係目前需求只係一次性帳戶啟用，暫時唔需要：

- 保存每一條 token嘅 audit history；
- 由 admin撤銷指定 token；
- 同一 user管理多條獨立 token；
- 為每次寄送保存 database record。

Stateless方案減少 token table、migration、過期資料清理及 plaintext token洩漏風險。詳細方案比較另見：

```text
docs/modification/email_activation_token_strategy_comparison.html
```

## `User.is_active`

Custom `User`繼承 Django `AbstractUser`，所以本身已經有：

```python
is_active
```

因此今次毋須新增 model field或 migration。

狀態含義：

```text
is_active=False
→ 未完成 email認證
→ Django預設 authentication backend唔容許登入

is_active=True
→ Email認證完成
→ 可以正常登入
```

Public registration同 Django Admin add-user採用兩個不同 forms：

- `RegistForm`會明確設定 `is_active=False`。
- `UserCreationAdminForm`無覆寫呢個狀態，沿用 `AbstractUser`嘅 active預設值，管理員建立嘅 user可直接使用。

## Registration Form 變更

檔案：

```text
accounts/forms.py
```

`RegistForm.save()`新增：

```python
user.is_active = False
```

完整保存次序：

```python
user = super().save(commit=False)
user.set_password(self.cleaned_data["password"])
user.is_active = False
user.save()
```

各部分作用：

- `commit=False`：先建立尚未寫入database嘅 user object，方便保存前調整欄位。
- `set_password()`：將原始密碼做安全 hash；唔可以直接將 plaintext放入 `password`欄位。
- `is_active=False`：禁止未認證帳戶登入。
- `user.save()`：取得 primary key；之後產生 `uidb64`及token都需要呢個 user身份。

## Activation Token Generator

新增檔案：

```text
accounts/tokens.py
```

核心 class：

```python
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            f"{user.pk}"
            f"{user.password}"
            f"{timestamp}"
            f"{user.email}"
            f"{user.is_active}"
        )
```

### `PasswordResetTokenGenerator`

雖然 class名包含 password reset，但佢提供嘅核心能力可以重用於一次性、有期限嘅 user token：

- 將 user狀態、timestamp同 project `SECRET_KEY`組合成簽章。
- 將 timestamp放入 token，方便驗證期限。
- 使用 constant-time compare降低 timing attack風險。
- 支援 secret rotation相關fallback行為。

### `_make_hash_value()`

呢個 method定義「邊啲資料改變時，舊 token要失效」。

每一部分作用：

- `user.pk`：token只屬於指定 user。
- `user.password`：密碼改變後舊 activation link失效。
- `timestamp`：每條 token包含產生時間，支援期限判斷。
- `user.email`：email address改變後舊 link失效。
- `user.is_active`：帳戶由 inactive變成 active後，原 token失效。

### Generator Instance

```python
account_activation_token = AccountActivationTokenGenerator()
```

Registration寄信同 activation view都import同一個 generator instance：

```python
from .tokens import account_activation_token
```

`make_token(user)`只產生 token，唔會修改 user；`check_token(user, token)`只驗證 token，亦唔會自動將帳戶啟用。

真正啟用帳戶嘅係 activation view：

```python
user.is_active = True
user.save(update_fields=["is_active"])
```

狀態改變後，重新計算嘅 hash同原 token唔同，所以舊 link不可再用。

## Token Timeout

檔案：

```text
config/settings.py
```

新增：

```python
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24
```

即係 token有效24小時。

目前 activation generator繼承 Django `PasswordResetTokenGenerator`，所以會讀取呢個 setting。將來加入 password reset時，兩種用途預設會共用24小時期限；如果產品要求不同期限，需要再拆開 activation timeout策略。

## `uidb64` 與 Token

Activation URL格式：

```text
/accounts/activate/<uidb64>/<token>/
```

兩個值責任不同：

```text
uidb64 → 搵邊一個 user
token  → 驗證操作是否由系統授權及仍然有效
```

### 產生 `uidb64`

```python
uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
```

流程：

```text
user.pk
→ force_bytes轉成bytes
→ urlsafe_base64_encode轉成適合URL使用嘅文字
```

Base64係編碼，唔係加密。任何人都可以解碼，所以 `uidb64`唔負責安全驗證。

### 解碼 `uidb64`

```python
user_id = force_str(urlsafe_base64_decode(uidb64))
user = User.objects.get(pk=user_id)
```

View先用 `uidb64`取得 user，之後先有足夠 user資料交俾 `check_token()`重新計算簽章。

如果只修改 `uidb64`指向另一個 user，原 token唔會符合另一個 user嘅資料，因此驗證失敗。

## 共用 Activation Email Function

檔案：

```text
accounts/views.py
```

建立：

```python
send_activation_email(*, request, user)
```

Registration同 resend共用同一個 function，避免複製 token、URL、template及寄信邏輯。

### Keyword-only Arguments

Function signature入面嘅 `*`：

```python
def send_activation_email(*, request, user):
```

代表 caller必須明確寫出參數名：

```python
send_activation_email(request=self.request, user=self.object)
```

避免將 `request`同 `user`位置調轉而不易發現。

### 建立 Activation Path

```python
activation_path = reverse(
    "accounts:user_activate",
    kwargs={
        "uidb64": uidb64,
        "token": token,
    },
)
```

`reverse()`根據URL name及kwargs建立相對路徑，避免將路徑字串寫死。

### 建立完整 URL

```python
activation_url = request.build_absolute_uri(activation_path)
```

`reverse()`結果只係：

```text
/accounts/activate/.../...
```

`build_absolute_uri()`會加入目前request嘅scheme及host，成為email可直接開啟嘅完整URL：

```text
http://127.0.0.1:8000/accounts/activate/.../...
```

正式部署時要配合正確 `ALLOWED_HOSTS`、HTTPS及site domain設定。

### Render Email Templates

Email context：

```python
email_context = {
    "user": user,
    "activation_url": activation_url,
}
```

Subject：

```python
subject = render_to_string(
    "accounts/email/user_activation_subject.txt",
    email_context,
).strip()
```

`.strip()`避免subject template首尾換行。Email subject唔可以包含不受控換行，否則可能引起invalid header或header injection問題。

Body：

```python
message = render_to_string(
    "accounts/email/user_activation_body.txt",
    email_context,
)
```

日文文案保留喺template，而唔係全部塞入Python view，方便之後維護或加入HTML版本。

### 寄信及回傳結果

```python
sent_count = send_mail(..., fail_silently=False)
```

成功寄出一封時回傳 `1`。Function只會喺 `sent_count == 1`時回傳 `True`；回傳 `0`或拋出exception都會記錄錯誤並回傳 `False`。

```text
True  → caller可以進入成功流程及建立cooldown
False → caller按registration或resend情境處理失敗
```

`logger.exception()`只喺exception branch使用，會保留traceback，但log內容只記operation及user id，唔記完整token、activation URL、password或email body。

### Development URL Output

Console email backend遇到較長日文內容時，可能將整個body顯示成MIME Base64。URL亦會包含喺encoded body，難以直接複製。

因此development mode額外使用：

```python
if settings.DEBUG:
    print(f"Development activation URL: {activation_url}")
```

呢個輸出只供local測試。完整token唔會寫入正式logger；production必須使用 `DEBUG=False`。

## Email Settings

檔案：

```text
config/settings.py
```

Development設定：

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "Japanese Quiz <noreply@japanese-quiz.local>"
```

Console backend唔會真正寄信，只會將email以原始MIME格式輸出到runserver terminal。

正式部署時需要改成真正SMTP或email provider backend，所有credentials都應由environment variables提供，唔可以寫死喺repository。

## Registration View 變更

`RegistUserView.success_url`由user home改成：

```python
reverse_lazy("accounts:activation_email_sent")
```

原因係新user仍然inactive，未有資格進入受 `LoginRequiredMixin`保護嘅home。

`form_valid()`依次執行：

1. `super().form_valid(form)`保存inactive user並建立 `self.object`。
2. `send_activation_email()`產生及寄出認證信。
3. 寄信成功後建立resend cooldown。
4. 記錄registration成功log。
5. Redirect去activation email完成頁。

如果寄信失敗：

- Inactive user仍然保留，避免database同已提交registration狀態互相混淆。
- 唔建立cooldown，user可以立即重試。
- 使用messages framework顯示稍後重試提示。
- Redirect去resend頁，而唔係回傳500。

目前project無啟用 `ATOMIC_REQUESTS`，亦無以 `transaction.atomic()`包住registration request；`super().form_valid()`保存user後先呼叫外部email backend。因此email失敗唔會令已建立user消失，resend flow負責恢復。

## Activation Email Sent Page

新增：

```text
accounts/templates/accounts/activation_email_sent.html
```

頁面提供：

- 檢查email提示；
- 檢查垃圾郵件提示；
- 返回登入頁連結；
- 進入resend頁連結。

頁面使用統一文字：

```text
入力されたメールアドレスに未認証のアカウントがある場合、
認証メールを送信しました。
```

唔會根據email存在、active狀態、cooldown或實際寄送結果顯示不同內容。

## Activation View

Class：

```python
ActivateUserView(View)
```

Template：

```text
accounts/templates/accounts/user_activate.html
```

### `get_user()`

```python
def get_user(self, uidb64):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None
```

處理以下失敗情況：

- Base64格式錯誤；
- 解碼結果唔係有效user id；
- 數值超出可用範圍；
- Database無相應user。

### GET：只顯示狀態

GET request唔會啟用帳戶，會按情況顯示：

- `already_active`：帳戶已經active。
- `invalid`：token無效或過期，HTTP status為400。
- `confirm`：user及token有效，等待user確認。

使用GET確認頁而唔係立即改database，係因為email provider或安全工具可能自動掃描link。若GET直接啟用，user未真正按下確認已經可能改變account狀態。

### POST：真正啟用

POST會重新取得user及重新驗證token，唔會假設之前GET驗證結果仍然有效。

成功後：

```python
user.is_active = True
user.save(update_fields=["is_active"])
```

`update_fields`限制今次SQL update只保存 `is_active`，避免無意覆蓋其他user欄位。

接住執行：

```python
UserVocabService.sync_vocab_safely(user=user)
```

將原本registration時嘅vocab sync延遲到身份確認完成後。Sync wrapper會記錄side-effect失敗，避免可重試嘅vocab初始化問題取消已完成嘅account activation。

### 點解確認按鈕有 HTML Form但無 Django Form？

Template使用：

```django
<form method="post">
    {% csrf_token %}
    <button type="submit">アカウントを有効にする</button>
</form>
```

HTML `<form>`負責令browser發出POST request；今次無輸入field需要clean或validate，所以唔需要另外建立 `forms.Form` class。

`uidb64`同token仍然留喺目前URL，browser會將POST提交到同一條URL。CSRF token由Django middleware驗證，唔依賴Django Form class。

## Resend Activation Email Form

新增：

```python
class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(
        label="メールアドレス",
        max_length=254,
    )
```

今次需要Django Form，因為user真係提交email field，需要：

- required validation；
- email格式驗證；
- 首尾空白清理；
- 最大長度限制；
- field error顯示。

Form唔會查詢email是否存在。Account lookup留俾view處理，亦避免form直接顯示「email不存在」而洩漏account資料。

## Resend Activation Email View

Class：

```python
ResendActivationEmailView(FormView)
```

Template：

```text
accounts/templates/accounts/resend_activation_email.html
```

View使用：

```python
User.objects.filter(
    email__iexact=email,
    is_active=False,
).first()
```

各部分作用：

- `email__iexact`：以case-insensitive方式比對email。
- `is_active=False`：只為未完成認證帳戶寄activation email。
- `.first()`：無結果時回傳 `None`，唔需要用exception分支處理 `DoesNotExist`。

以下情況唔寄信：

- Email對應active user；
- Email不存在；
- User仍處於cooldown；
- Email backend回報失敗。

除email格式錯誤會保留喺表單顯示field error之外，所有有效格式輸入都redirect去相同完成頁。

## Account Enumeration 防護

Account enumeration指攻擊者透過畫面、status或response差異，逐個測試某個email有冇註冊。

Resend flow採用統一回應：

```text
Inactive account並成功寄信
Active account
不存在account
Cooldown中
寄信失敗
→ 全部顯示相同完成頁
```

Log亦唔記錄訪客輸入嘅不存在email；真正寄出時只記內部user id。

## Resend Cooldown

Setting：

```python
ACTIVATION_EMAIL_RESEND_COOLDOWN_SECONDS = 60
```

Cache key：

```python
f"activation-email-resend:{user.pk}"
```

使用user id而唔係原始email，避免將email address放入cache key及相關diagnostic output。

### `cache.add()`

```python
can_send = cache.add(
    cache_key,
    True,
    timeout=settings.ACTIVATION_EMAIL_RESEND_COOLDOWN_SECONDS,
)
```

`cache.add()`只會喺key不存在時寫入並回傳 `True`；已有key會回傳 `False`。相對於先 `cache.get()`再 `cache.set()`，`add()`可以將「檢查及建立」合成一個cache operation，降低兩個同時request一齊通過檢查嘅機會。

流程：

```text
第一次寄信
→ key不存在
→ add成功
→ 寄信

60秒內再提交
→ key存在
→ add失敗
→ 唔寄信

60秒後
→ key過期
→ 可以再次寄信
```

Registration第一次寄信成功後亦會 `cache.set()`相同key，避免user註冊後立即再補發第二封。

如果resend寄信失敗：

```python
cache.delete(cache_key)
```

會釋放預先取得嘅cooldown，等下一次request可以立即重試。

目前未額外記錄每次被cooldown擋住嘅request，避免正常重試或濫用造成大量無價值log。

### Development 與 Production Cache

Django預設local-memory cache足夠單一development process測試，但每個process有自己嘅cache，無法為多worker或多instance production提供一致cooldown。

Production應使用共享cache，例如Redis，並另外考慮web server／gateway層嘅IP rate limit。現有cooldown主要防止同一個已知inactive account被大量寄信，唔係完整DoS防護。

## Resend 與舊 Token

Stateless token無database record可以單獨撤銷。Resend產生新token後，只要user資料未改變，舊token喺原本期限內仍可能有效。

呢個行為對目前一次性activation可接受：

```text
任何一條有效link成功啟用帳戶
→ is_active由False變True
→ 所有根據False狀態產生嘅舊token一齊失效
```

如果將來產品要求「每次resend必須立即撤銷上一條link」，就需要加入會改變hash嘅version／timestamp欄位，或者改用database token model。

## Login Flow 變更

Inactive user輸入正確密碼時，Django預設authentication backend通常會直接拒絕該user，`AuthenticationForm`得到嘅結果同錯誤密碼相同。

為咗避免透過不同登入錯誤洩漏account狀態，`UserLoginForm`使用日文通用錯誤：

```text
メールアドレスまたはパスワードが正しくありません。
メール認証が完了しているかもご確認ください。
```

Login page固定提供resend入口，而唔係只喺系統確認email存在及inactive後先顯示。

因此以下情況得到相同錯誤：

- Inactive user加正確密碼；
- Active user加錯誤密碼；
- 不存在email。

Active user加正確密碼仍然正常登入。

## URL 變更

檔案：

```text
accounts/urls.py
```

新增routes：

```text
/accounts/activate/<uidb64>/<token>/
/accounts/activation-email-sent/
/accounts/resend-activation-email/
```

URL names：

```text
accounts:user_activate
accounts:activation_email_sent
accounts:resend_activation_email
```

URL pattern入面嘅kwargs名稱必須同view method一致：

```python
def get(self, request, uidb64, token):
def post(self, request, uidb64, token):
```

Django會自動將URL兩段值傳入相應參數。

## Template 變更

新增：

```text
accounts/templates/accounts/user_activate.html
accounts/templates/accounts/activation_email_sent.html
accounts/templates/accounts/resend_activation_email.html
accounts/templates/accounts/email/user_activation_subject.txt
accounts/templates/accounts/email/user_activation_body.txt
```

修改：

```text
accounts/templates/accounts/user_login.html
```

`user_activate.html`按 `activation_status`顯示四種狀態：

- `confirm`
- `success`
- `already_active`
- `invalid`

Invalid狀態及login頁都提供resend入口。

## Database / Migration

今次無新增model或field，所以無新migration。

檢查：

```text
manage.py makemigrations --check --dry-run
```

結果：

```text
No changes detected
```

## Logging 與敏感資料

新增主要operation logs：

```text
user_registration
user_account_activation
activation_email_send
activation_email_resend
```

Log會記錄：

- operation名稱；
- internal user id；
- 寄送結果或sent count；
- exception traceback。

Log唔應記錄：

- password；
- activation token；
- 完整activation URL；
- email body；
- 完整POST payload。

Development `print()`包含activation URL，但受 `settings.DEBUG`限制，唔使用production logger。

## 驗證結果

### Django Checks

```text
manage.py check
→ System check identified no issues

manage.py makemigrations --check --dry-run
→ No changes detected
```

### Token 行為

已用無database寫入嘅user object驗證：

```text
Inactive user token             → 有效
is_active改成True後同一token   → 無效
24小時前                        → 有效
24小時後                        → 無效
Malformed token                 → 無效
```

### Registration 與 Activation

已用temporary transaction及test client驗證：

```text
Registration                    → 302到activation email sent頁
新user                           → is_active=False
Email數量                       → 1
Email body                      → 包含activation URL
Activation GET                  → 200確認頁
Activation POST                 → 200成功頁
Activation後                    → is_active=True
Activation後vocab sync          → 呼叫1次
重開舊link                      → already active頁
```

### Resend 與 Cooldown

```text
Inactive email                  → 寄信
Active email                    → 唔寄信、同一完成頁
不存在email                     → 唔寄信、同一完成頁
錯誤email格式                   → form field error
Registration後立即resend        → cooldown擋住
Cooldown後resend                → 寄信
Cooldown內重複resend            → 唔再寄
寄信失敗                        → cache key釋放
```

### 寄信失敗

以mock分別模擬：

```text
send_mail回傳1                  → helper回傳True
send_mail回傳0                  → helper回傳False
send_mail拋exception            → helper回傳False並記traceback
Registration寄信失敗           → 保留inactive user、redirect resend、無cooldown
Resend寄信失敗                 → 統一完成頁、釋放cooldown
```

所有temporary database資料已rollback。

### Login

```text
Inactive＋正確密碼              → 登入失敗、日文通用訊息
Active＋錯誤密碼                → 相同日文通用訊息
不存在email                     → 相同日文通用訊息
Active＋正確密碼                → 302到user home並建立session
```

### Existing Regression Suite

```text
Ran 10 tests
OK
```

今次未新增及提交activation專用automated test cases；以上feature checks係開發期間嘅temporary integration diagnostics。專用test coverage按目前決定押後。

## 涉及檔案

新增：

```text
accounts/tokens.py
accounts/templates/accounts/user_activate.html
accounts/templates/accounts/activation_email_sent.html
accounts/templates/accounts/resend_activation_email.html
accounts/templates/accounts/email/user_activation_subject.txt
accounts/templates/accounts/email/user_activation_body.txt
```

修改：

```text
accounts/forms.py
accounts/views.py
accounts/urls.py
accounts/templates/accounts/user_login.html
config/settings.py
```

無model及migration改動。

## 最終狀態

目前development環境已完成：

- Public registration建立inactive account。
- 24小時stateless activation token。
- 日文activation email及本地console測試。
- GET確認、POST啟用及一次性失效行為。
- Activation後先初始化UserVocab。
- Resend form、統一回應及account enumeration防護。
- 每個inactive user 60秒resend cooldown。
- Registration及resend寄信失敗處理。
- Inactive login日文通用提示及resend入口。

## 尚未完成 / Production 注意事項

### 1. Activation Automated Tests

仍需將目前temporary diagnostics轉成正式 `accounts/tests.py` test cases，至少覆蓋：

- registration建立inactive user及email內容；
- valid、expired、malformed及reused token；
- GET唔改狀態、POST先啟用；
- activation後vocab sync；
- resend account enumeration及cooldown；
- send failure recovery；
- inactive login。

### 2. Production Email Backend

Console backend只供development。Production需要：

- SMTP或transactional email provider；
- environment-based credentials；
- verified sender/domain；
- HTTPS activation URL；
- delivery、bounce及provider quota監察。

### 3. Production Cache

Production多worker／多instance環境需要Redis等共享cache，否則local-memory cooldown只對單一process有效。

### 4. Secret Key

Activation token安全性依賴 `SECRET_KEY`。Production必須由安全environment／secret store提供，唔可以沿用development hard-coded key。

### 5. Password Reset

Password reset之後應使用Django內建views、forms及 `default_token_generator`，同activation使用不同URL及email templates。若兩者需要不同有效期限，再拆分timeout設計。

### 6. Service Boundary

`send_activation_email()`目前放喺 `accounts/views.py`，已足夠支援registration及resend。若之後再有admin resend、background task或其他caller，可以移去 `accounts/service/`，令view只負責request／response。

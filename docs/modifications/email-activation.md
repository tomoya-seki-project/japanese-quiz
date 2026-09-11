# Email activation：註冊、確認啟用與重寄流程

## Report 基準

- 產生時間：2026-09-10 22:30 JST。
- 主題：已提交嘅 account email activation 修改。
- 修改前：`012ae6701b925c4509e36e8f52e122f0ae0a3baf`。
- 修改後：`9062a2ea41e4e46f5f3b27fcaedf303be0e4f0d4`，亦係報告建立時嘅 `HEAD`。
- 按 user 指定比較 `012ae67 → 9062a2e`；下文行號全部指修改後 commit，唔係 editor 當前行號。程式片段係該版本嘅局部原文，唔代表完整 function。
- 直接證據：`accounts/forms.py`、`accounts/views.py`、`accounts/tokens.py`、`accounts/urls.py`、accounts activation／login／email templates，同 `config/settings.py` 嘅相關 diff。
- 周邊核對：custom user、admin form、profile signal、`sync_vocab_safely()`、requirements 同現有 tests。
- Working tree 有未提交嘅 email lowercase／unique constraint 修改、quiz M01 修改、四份 status docs 修改，另有未追蹤 accounts migration；全部排除於本報告嘅 before／after 範圍。
- 同一 commit 內其他 modification notes、status docs、dictionary URL 同 ignore 規則唔屬於今次 activation 實作解釋。現有 `docs/modification/email_activation.md` 保留；本文件係新報告。
- Repository 固定 `Django==6.0.5`；框架說明參考 Django 6.0 官方文件，token 細節亦核對本機安裝版本源碼。

## 完成度檢查

以 development console-email workflow 為範圍，核心接線完整：public registration 保存 inactive user、建立 activation link、GET 顯示確認、POST 驗證後啟用、同步 UserVocab，亦有重寄入口同寄信失敗處理。所需 forms、URLs、templates 同 token object 均存在；沿用既有 `is_active`，毋須為本修改新增 migration。

呢個判斷唔代表已驗證真實收信或全部安全邊界。`accounts/tests.py` 仍然只有 placeholder；本次現有 suite 通過只提供有限 regression 證據，詳見末段。

## 修改目的 1：將「建立帳戶」與「容許登入」分開

### 修改目的／理由

之前提交有效 registration form 就建立可用帳戶，亦立即同步個人字庫。新流程要求先證明 user 可以取得寄去該 email 嘅 link，先容許登入及初始化字庫。

### 受影響檔案與責任

- `accounts/forms.py`：`RegistForm.save()` 決定 public registration 儲存嘅 active state。
- `accounts/views.py`：`RegistUserView` 保存帳戶後安排寄信；`ActivateUserView.post()` 啟用後先安排 vocab sync。
- `accounts/admin.py`／`UserCreationAdminForm`：既有獨立 admin creation path，唔套用 public form 嘅 inactive policy。

### 修改前

`accounts/forms.py`，`RegistForm.save()`：

```python
user = super().save(commit=False)
user.set_password(self.cleaned_data['password'])
if commit:
    user.save()
return user
```

`accounts/views.py`，`RegistUserView.form_valid()` 原本註冊後執行：

```python
UserVocabService.sync_vocab_safely(user=self.object)
return result
```

### 修改後

`accounts/forms.py:55`，`RegistForm.save()`：

```python
user = super().save(commit=False)
user.set_password(self.cleaned_data['password'])
user.is_active = False
if commit:
    user.save()
return user
```

`accounts/views.py:225`，`ActivateUserView.post()` 通過驗證後：

```python
user.is_active = True
user.save(update_fields=["is_active"])

UserVocabService.sync_vocab_safely(user=user)
```

### 前後差異與運作解釋

`super().save(commit=False)` 先取得尚未保存嘅 model object，令 form 可以先 hash password 同設定 inactive，最後先寫 database。`commit=False` 唔代表 rollback transaction，亦唔係將 password 明文保存落 database。

`CreateView.form_valid()` 會呼叫 form save 並設定 `self.object`。所以新 registration view 先 call `super().form_valid(form)`，之後就有真正 user ID 可以產生 link。呢個 call 只係產生 response object；自己嘅 method 未 return 前仍可寄信或改為另一個 redirect。

Activation 成功先 sync 字庫。既有 `UserProfile` post-save signal 仍然會喺建立 user 時執行；「延後 UserVocab」唔等於延後所有 related records。Admin 使用獨立 form，仍保留原有 active 預設。

### 新使用技術

呢次新用到 `is_active` 作 public onboarding gate；Django 預設 authentication backend 會拒絕 inactive user，唔需要自行喺每個登入 view 重寫 permission check。呢個行為依賴所用 backend，唔係所有自訂 backend 必然遵守。[Django User.is_active](https://docs.djangoproject.com/en/6.0/ref/contrib/auth/#django.contrib.auth.models.User.is_active)

`ModelForm.save(commit=False)`、`set_password()`、CreateView 同 resilient service wrapper 都係 project 已有手法；重點係今次改咗狀態設定同 sync 時機。

## 修改目的 2：用可過期、隨帳戶狀態失效嘅 token 證明 link 有效

### 修改目的／理由

URL 有 user ID 唔足以授權啟用。User ID 可以猜測，亦可以由 URL encoding 還原；需要額外可驗證嘅 token，並限制使用時間。

### 受影響檔案與責任

- `accounts/tokens.py:1`：新增 `AccountActivationTokenGenerator` 同共用 instance。
- `accounts/views.py:48`：建立 uid、token 同完整 URL；`:185` 解碼 uid 後取得 user。
- `accounts/urls.py`：將 uid／token 傳入 activation view。
- `config/settings.py:137`：設定 token timeout。

### 修改前

無對應 before-code：baseline 冇 `accounts/tokens.py` 或 activation route，registration 唔需要驗證 link。

### 修改後

`accounts/tokens.py:3`，新 subclass：

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

account_activation_token = AccountActivationTokenGenerator()
```

`accounts/views.py:48`，`send_activation_email()`：

```python
uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

token = account_activation_token.make_token(user)

activation_path = reverse(
    "accounts:user_activate",
    kwargs={
        "uidb64": uidb64,
        "token": token,
    },
)

activation_url = request.build_absolute_uri(activation_path)
```

`config/settings.py:137`：

```python
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24
```

### 前後差異與運作解釋

呢個 class 沿用父類 `make_token()`／`check_token()`，只 override「用邊啲帳戶資料參與 hash」。父類使用 server secret 同 HMAC 產生驗證值，再附帶 timestamp；唔係將密碼或 secret 放入 URL。`user.password` 係 database 已 hash 嘅 password field。

驗證時會用 URL timestamp 同當前 user state 重算，再比對 token，同時檢查 timeout。`False → True` 改變 `is_active` 後，重算值不同，之前 token 就唔再通過；email 或 password 改變亦一樣。呢個係根據狀態失效，冇額外 token table 或 used-token record。

要分清楚三件事：

- `uidb64` 只係 URL-safe encoding，用嚟定位 user，唔係加密或權限證明。
- Token 才係驗證依據；持有有效 link 嘅人可以進入確認流程。
- Resend 只重新產生 token，冇保存「最新 token」或撤銷版本，所以唔保證舊 link 即時失效。同一 user state、同一秒內亦可能產生相同 token。

當前 subclass 唔包含 `last_login`，亦冇另設 `key_salt`。唔應誤寫成完整照搬預設 password-reset hash fields，或者聲稱已建立獨立 token 儲存系統。

### 新使用技術

`PasswordResetTokenGenerator` 係 Django Auth 既有 generator；今次將其 timestamp、HMAC 同 timeout 機制重用於 activation。`_make_hash_value()` 係 framework 內部方法，升級 Django 時應重新核對。本次已直接讀取安裝版本 `django/contrib/auth/tokens.py`；官方 source 入口本次載入失敗，因此細節以本機 6.0.5 源碼為證據。

`PASSWORD_RESET_TIMEOUT` 以秒計；呢個 subclass 沿用同一設定，所以將來若加入 password reset，兩個用途會共用 timeout。[Django timeout 設定](https://docs.djangoproject.com/en/6.0/ref/settings/#password-reset-timeout)

`force_bytes()`／URL-safe Base64 配對處理 uid；反方向用 `urlsafe_base64_decode()` 同 `force_str()`。`reverse()` 依 named route 建立 path，而 `build_absolute_uri()` 補上 request 嘅 scheme 同 host，令 email 裏面條 link 可以獨立開啟。[Django build_absolute_uri](https://docs.djangoproject.com/en/6.0/ref/request-response/#django.http.HttpRequest.build_absolute_uri)

## 修改目的 3：讀取確認頁同真正啟用分成 GET／POST

### 修改目的／理由

Email preview 或 link scanner 可以自動 GET URL。單純讀取 link 唔應立即改變 account state；user 確認提交後先啟用。

### 受影響檔案與責任

- `accounts/views.py:182`：`ActivateUserView` 提供 user lookup、GET 同 POST。
- `accounts/templates/accounts/user_activate.html:6`：按 `activation_status` 顯示確認、成功、已啟用或無效狀態。
- `accounts/urls.py`：activation route 交畀 `View.as_view()` 分派 HTTP method。

### 修改前

無 activation view 或確認表單；原 registration 儲存後直接走 account 頁面，冇第二階段啟用操作。

### 修改後

`accounts/views.py:192`，GET 通過 user／active／token guards 後：

```python
return render(
    request,
    self.template_name,
    context={
        "activation_status":"confirm"
    },
)
```

`accounts/templates/accounts/user_activate.html:9`：

```html
<form method="post">
    {% csrf_token %}
    <button type="submit">アカウントを有効にする</button>
</form>
```

`accounts/views.py:225`，POST 再次檢查 token 嘅分支：

```python
if not account_activation_token.check_token(user, token):
    return render(
        request,
        self.template_name,
        context={
            "activation_status": "invalid"
        },
        status=400,
    )
```

### 前後差異與運作解釋

Form 冇寫 `action`，會 POST 回當前 activation URL，因此仍帶住 uid 同 token。POST 必須重新查 user 同驗 token：user 開住確認頁期間，token 可能過期或 account 已由另一個 request 啟用。唔可以將之前 GET 通過當作永久授權。

| 條件 | GET | POST |
| --- | --- | --- |
| 無法取得 user | 404 | 404 |
| user 已 active | 顯示 already_active | 顯示 already_active，唔再 sync |
| inactive 但 token 無效／過期 | 400 invalid | 400 invalid，唔啟用 |
| inactive 且 token 有效 | 顯示 confirm | 保存 active、sync、顯示 success |

兩條 method 都先判斷 already-active，再驗 token。因此啟用後重開 link 係見 already-active 頁，唔係一定見 invalid token。成功 POST 冇自動 login；template 提供登入入口。

### 新使用技術

`View.get()`／`View.post()` 分派同 `render()` 係既有 Django 手法；今次新責任係將讀取同狀態更新分開。CSRF token 保護瀏覽器 POST，activation token 證明該 link 有效，兩者用途唔同。既有 resilient sync 失敗會記 log，唔會將已保存嘅 activation rollback。

## 修改目的 4：建立可重試嘅寄信流程

### 修改目的／理由

帳戶保存成功唔代表寄信成功。需要保留 inactive account，通知 user 重試，避免未收信就被當成可登入。

### 受影響檔案與責任

- `accounts/views.py:48`：`send_activation_email()` 建立信件並回傳 boolean。
- `accounts/views.py:118`：registration 根據寄信結果選擇 response。
- `accounts/templates/accounts/email/`：新增 subject 同 body，將信件文案同 Python 分開。
- `config/settings.py:139`：指定 development backend。

### 修改前

`accounts/views.py`，registration 原本嘅目的地：

```python
success_url = reverse_lazy('accounts:user_home')
```

Baseline 冇 email helper、mail templates 或 delivery result handling。

### 修改後

`accounts/views.py:113`，新目的地及寄信結果分支：

```python
success_url = reverse_lazy('accounts:activation_email_sent')
```

```python
email_sent = send_activation_email(request=self.request, user=self.object)

if not email_sent:
    messages.error(
        self.request,
        "認証メールを送信できませんでした。しばらくしてから再送してください。",
    )
    return redirect("accounts:resend_activation_email")
```

`accounts/views.py:48`，helper 內嘅寄信呼叫：

```python
sent_count = send_mail(
    subject=subject,
    message=message,
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[user.email],
    fail_silently=False,
)
```

`config/settings.py:139`：

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

### 前後差異與運作解釋

Helper 用 `render_to_string()` 產生 subject 同 body；subject 會 `.strip()` 去掉外圍換行。`send_mail()` exception 會被記錄並回傳 `False`；即使冇 exception，`sent_count != 1` 亦當失敗。Registration 已保存 inactive user，所以此時唔會刪除 user，而係導向 resend。

要留意 try/except 只包住 `send_mail()`：URL construction 同 template rendering 發生喺 try 之前，唔係所有 helper exception 都會轉成 `False`。呢啲 components 已存在，但後續重構時唔好誤解 exception boundary。

正常寄出後先設 registration cooldown。DEBUG 時會輸出 activation URL；URL 帶有啟用能力，唔應複製到公開 log 或報告。

### 新使用技術

`django.core.mail.send_mail()` 透過設定嘅 backend 送出純文字信件，回傳處理成功數量。Console backend 只將信件輸出到 terminal，唔會寄到 mailbox；即使 SMTP backend 回報成功，亦唔等於 user 已收到或已閱讀。`fail_silently=False` 令 caller 可以處理寄送 exception。[Django email API 與 backend](https://docs.djangoproject.com/en/6.0/topics/email/)

`render_to_string()` 同 logging 係 project 既有技術，今次新增嘅係 email templates 同 delivery result 判斷。冇新增第三方 mail SDK 或 background queue。

## 修改目的 5：容許重寄，同時減少重複寄送及帳戶狀態洩漏

### 修改目的／理由

User 可能冇收到首封信，或者 link 已過期。Resend 要提供恢復入口，亦唔應直接回覆某 email 是否存在、active 或 inactive。

### 受影響檔案與責任

- `accounts/forms.py:121`：`ResendActivationEmailForm` 驗證 email 格式。
- `accounts/views.py:269`：尋找 inactive user、取得 cooldown、安排寄信、統一回應。
- `accounts/templates/accounts/resend_activation_email.html` 同 `activation_email_sent.html`：輸入及統一通知。
- `accounts/forms.py:63` 同 login template：登入錯誤提示同 resend 入口。
- `config/settings.py`：60 秒 cooldown。

### 修改前

無 resend form／view／cache gate。`UserLoginForm` 冇本次加入嘅 `error_messages` override，login template 亦冇 resend link。

### 修改後

`accounts/views.py:274`，`ResendActivationEmailView.form_valid()` 查詢及 cache gate：

```python
user = User.objects.filter(
    email__iexact=email,
    is_active=False,
).first()

if user is not None:
    cache_key = f"activation-email-resend:{user.pk}"

    can_send = cache.add(
        cache_key,
        True,
        timeout=settings.ACTIVATION_EMAIL_RESEND_COOLDOWN_SECONDS,
    )
```

同一 method 嘅寄信分支：

```python
if can_send:
    email_sent = send_activation_email(
        request=self.request,
        user=user,
    )
    if not email_sent:
        cache.delete(cache_key)
```

`accounts/forms.py:63`，`UserLoginForm` 新增錯誤文字：

```python
error_messages = {
    "invalid_login": (
        "メールアドレスまたはパスワードが正しくありません。"
        "メール認証が完了しているかもご確認ください。"
    ),
    "inactive": (
        "このアカウントは現在利用できません。"
    ),
}
```

### 前後差異與運作解釋

Resend FormView 只喺 form valid 後查 user；唔存在或已 active 嘅 email 唔寄信，但仍走同一 success URL。Inactive user 若 cooldown 未滿亦唔寄；寄送失敗會釋放 key，方便下一次重試，同樣唔喺 response 洩漏 account state。

`cache.add()` 只喺 key 未存在先保存並回報成功，適合搶一次寄信機會。首封 registration 信用 `cache.set()` 建立同名 key，令立即 resend 亦受 cooldown 限制。兩個 API 唔同：set 會覆蓋；add 唔會覆蓋現有 key。

例如首封信成功後 10 秒就 resend：key 仲存在，唔再寄。TTL 到期後 resend：add 成功，才寄信。寄送失敗：delete key；user 可重試。呢個係暫時節流，唔係永久寄送紀錄。

登入仍交畀 Django authentication flow；預設 backend 對 inactive user 會拒絕 authentication，通常落入 generic invalid_login。唔應聲稱 inactive 一定會顯示自訂 `inactive` message。

### 新使用技術

Django cache API 係本次 cooldown 嘅新用途：`add()`、`set()`、`delete()` 同 TTL 配合控制重試。當前未設定共享 backend，預設 LocMem 係 process-local；多 worker 唔會共享同一份節流狀態，亦唔構成 IP／全域 rate limit。[Django cache API](https://docs.djangoproject.com/en/6.0/topics/cache/)

`forms.EmailField`、FormView 同 named redirects 係既有手法。Email 格式驗證只檢查輸入形狀；mailbox 控制權仍由有效 activation link 證明。

## 整體行為改變

以前係註冊後即建立可用 user 同同步字庫。依家係註冊後保存 inactive user，再由 email link 嘅 GET 確認頁同 POST 啟用完成第二階段。成功啟用後先 sync，user 再自行登入。

| 事件 | 帳戶狀態 | 字庫／回應 |
| --- | --- | --- |
| 註冊有效、首封信處理成功 | inactive | 檢查 email 頁，暫不 sync UserVocab |
| 首封信處理失敗 | inactive 保留 | 引導 resend |
| GET 有效 link | inactive 不變 | confirm |
| POST 有效 link | active | resilient sync，success |
| 無效／過期 link、user 存在且 inactive | inactive 不變 | 400 invalid |
| user 已 active 後重開 link | active | already_active |
| Resend 冇符合條件 user／仍在 cooldown | 不變 | 統一通知，唔寄信 |

## 測試及驗證結果

本次實際執行：

- `git diff --check 012ae67 9062a2e`：通過。
- `git diff --check`：當前 working tree 通過。
- `.venv/bin/python manage.py check`：0 issues。
- `.venv/bin/python manage.py test accounts core`：10 tests 通過，使用 test database，執行後銷毀。

重要範圍限制：Django commands 係喺當前 working tree 執行，當中包含未提交 accounts 同 quiz 修改；唔係喺 isolated `9062a2e` checkout 執行。因此唔可以聲稱已獨立重跑指定 commit 嘅全部行為。

本次只檢視而未新增嘅 tests：`9062a2e:accounts/tests.py` 係 placeholder；`core/tests.py` 主要覆蓋 templates／語系等既有 regression。10 tests 全綠唔代表已驗證 token expiry、cooldown、mail failure、POST activation 或併發啟用。

Code inspection 已核對 registration → helper → URL → activation view → token → sync，同 resend → cache → helper → generic response；冇執行真實郵件寄送或 production data 修改。

## 已知限制／未驗證事項

- `9062a2e` 尚未包含完整 email lowercase policy 或 case-insensitive unique constraint；resend 嘅 `iexact(...).first()` 喺有大小寫變體帳戶時存在歧義。之後 working-tree M02 修正唔屬於本報告 after state。
- Console backend 只適合 development。真實 mail provider、HTTPS host／proxy configuration、共享 cache 同寄送監控仍待部署時完成。
- Resend 統一 response 減少直接透露 account state，但唔代表已消除 timing difference；registration duplicate validation 同 already-active activation response 亦唔係同一保密邊界。
- Activation 嘅「使用後失效」係狀態變化帶來嘅循序行為；POST 冇鎖定 user row 或條件式狀態更新，唔保證併發請求下 side effects exactly once。
- `is_active` 同時承擔「未驗證」及「停用」語意。若 admin 用 False 封禁已驗證帳戶，現有 resend 亦會選中該帳戶；需要另定停權政策，唔應將本機 onboarding 實作當成完整封禁管理。
- 冇獨立驗證 timestamp 過期、tampered uid／token、email exception／0 return、重寄節流、sync failure 同多 worker 行為。本報告唔新增 tests。
- `sync_vocab_safely()` 為既有 best-effort wrapper；sync 失敗唔撤銷 active state，之後 login／profile flow仍有重試同步入口。

## 官方參考資料

- [Django 6.0：User.is_active 與 backend 行為](https://docs.djangoproject.com/en/6.0/ref/contrib/auth/#django.contrib.auth.models.User.is_active)
- [Django 6.0：PASSWORD_RESET_TIMEOUT](https://docs.djangoproject.com/en/6.0/ref/settings/#password-reset-timeout)
- [Django 6.0：build_absolute_uri](https://docs.djangoproject.com/en/6.0/ref/request-response/#django.http.HttpRequest.build_absolute_uri)
- [Django 6.0：Sending email](https://docs.djangoproject.com/en/6.0/topics/email/)
- [Django 6.0：Cache framework](https://docs.djangoproject.com/en/6.0/topics/cache/)

Token 實作補充證據：本機 Django 6.0.5 嘅 `django/contrib/auth/tokens.py`；官方 source 頁本次未能成功載入，冇將其他版本源碼當成 6.0.5 證據。

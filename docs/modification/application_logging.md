# Application Logging Implementation Report

## 目的

今次改動係為 project 建立正式 application logging，令重要資料變更、業務結果同未預期 exception 有足夠紀錄，同時避免正常 validation、重複 submission、普通 read request同高頻操作製造大量低價值 log。

整體目標：

```text
重要成功結果
→ INFO + operation + user/object IDs + result/count

預期但值得留意嘅拒絕／權限問題
→ INFO 或 WARNING

真正未預期 exception
→ ERROR + traceback

普通 validation／read flow／零資料變更
→ 唔記，或者只記必要嘅業務結果
```

Logging唔係用嚟記低程式每一步，而係回答以下問題：

- 發生咗咩重要操作？
- 邊個 user觸發？
- 影響咗邊個 object或幾多 records？
- 操作成功、被拒絕、跳過定崩潰？
- 如果係未預期錯誤，traceback喺邊？

## 目錄

- [目的](#目的)
- [問題背景](#問題背景)
- [涉及檔案](#涉及檔案)
- [Logging基礎設定](#logging基礎設定)
- [Level使用原則](#level使用原則)
- [Log message格式](#log-message格式)
- [Vocab request同admin review](#vocab-request同admin-review)
- [UserVocab flow](#uservocab-flow)
- [Quiz flow](#quiz-flow)
- [Account flow](#account-flow)
- [Event同Feedback flow](#event同feedback-flow)
- [Management commands](#management-commands)
- [Exception ownership同traceback](#exception-ownership同traceback)
- [Transaction同成功log位置](#transaction同成功log位置)
- [點解部分位置唔加log](#點解部分位置唔加log)
- [敏感資料邊界](#敏感資料邊界)
- [今次驗證結果](#今次驗證結果)
- [建議補測試](#建議補測試)
- [重點心智模型](#重點心智模型)

## 問題背景

Project原本主要依靠：

- browser畫面 message；
- management command terminal output；
- Django開發環境 exception page；
- 臨時 `print()`／人手觀察。

呢啲方法可以俾目前操作嘅 user知道結果，但唔能夠可靠回答「之前發生過咩事」。例如：

- Admin approve咗邊個 VocabRequest？
- Quiz answer係正常接受，定因 stale submission被忽略？
- Import成功幾多 rows、失敗幾多 rows？
- UserVocab sync係零變更，定真係新增咗資料？
- 真正500發生時，完整 traceback有冇保留？

另一方面，如果每個 view entry、query、question pick同 helper call都寫 log，會出現另一個問題：

```text
log數量太多
→ 重要事件被噪音淹沒
→ file增長更快
→ debug時更難搵真正原因
→ 同一 exception可能被重複記錄
```

因此今次設計重點唔係「到處加 logger」，而係建立清楚 logging boundary。

## 涉及檔案

### 設定

- `config/settings.py`
  - Formatter、filters、handlers同app loggers。
- `.gitignore`
  - 排除 runtime `.log` files。
- `log/.gitkeep`
  - 保留 log directory。

### Vocab／UserVocab

- `dictionary/views.py`
  - Vocab request results。
  - UserVocab bulk／single `in_use`變更。
- `dictionary/admin.py`
  - VocabRequest approve／reject audit result。
- `dictionary/service/user_vocab_action.py`
  - UserVocab sync success／failure。
  - Vocab sync event generation failure。

### Quiz

- `quiz/views.py`
  - Setting、resume、answer、skip同summary outcomes。

### Account／Event／Feedback

- `accounts/views.py`
  - Registration同login success。
- `core/views.py`
  - Event mark-read。
  - Feedback create／duplicate／reply。
  - Admin-only feedback permission denial。

### Management commands

- `dictionary/management/commands/import_vocab.py`
- `dictionary/management/commands/setup_categories.py`
- `dictionary/management/commands/dev_clear_vocab.py`

## Logging基礎設定

### Formatter

目前 formatter：

```python
"format": "{asctime} [{levelname}] {name} : {message}"
```

每條 log會包含：

- Timestamp；
- Level；
- Logger name，例如 `dictionary.views`；
- 完整 message同 context fields。

例子：

```text
2026-08-31 12:00:00 [INFO] dictionary.admin : Vocab request review result: operation=vocab_request_review reviewer_user_id=1 vocab_request_id=42 request_type=create result=approved
```

### Handlers

目前使用：

| Handler | 接收內容 | 用途 |
| --- | --- | --- |
| Console | `INFO+` | 開發期間即時觀察 |
| Debug file | Exact `DEBUG` | 只保存 debug資料 |
| Full-flow file | `INFO+` | 保存正常重要flow、warning同error |
| Error file | `ERROR+` | 集中保存未預期錯誤 |

File handlers使用每日 rotation：

```python
"when": "midnight",
"interval": 1,
"backupCount": 7,
```

即係：

- 每日產生新 log file；
- 保留7份舊檔；
- 避免單一 log file無限增長。

### Exact-DEBUG filter

Handler嘅 `level="DEBUG"`代表最低門檻，並唔係「只接收 DEBUG」。如果冇filter，DEBUG handler亦會收到 INFO、WARNING同ERROR。

因此加入：

```python
"debug_only": {
    "()": "django.utils.log.CallbackFilter",
    "callback": lambda record: record.levelname == "DEBUG",
}
```

令 debug file只保存 exact DEBUG。

### App loggers

目前為以下 namespaces設定 handlers：

- `accounts`
- `core`
- `dictionary`
- `errorHandler`
- `quiz`
- `django.request`

每個 module使用：

```python
import logging

logger = logging.getLogger(__name__)
```

`__name__`會自動產生例如：

```text
dictionary.views
dictionary.admin
quiz.views
core.views
```

方便由 log反查來源檔案。

## Level使用原則

### `DEBUG`

只供開發期間短期診斷詳細狀態。唔應將所有正常flow長期寫成 DEBUG。

### `INFO`

用於正常但重要嘅業務結果：

- VocabRequest created／approved／rejected／skipped；
- Quiz setting accepted、answer checked、question skipped、quiz completed；
- User registration／login completed；
- UserVocab實際新增；
- Feedback created／duplicate skipped／reply completed；
- Import／setup／clear command started或completed。

預期 business validation可以使用 INFO，因為佢唔代表server壞咗。

### `WARNING`

用於預期內但值得注意嘅情況：

- Permission denied；
- CSV file或required headers不存在；
- Import row因validation／integrity問題被拒絕；
- 非admin嘗試進入admin-only feedback頁面。

WARNING唔代表500，亦唔一定需要工程師立即處理。

### `ERROR`

用於真正未預期、令操作無法完成嘅問題。

一般唔直接寫：

```python
logger.error("Something failed")
```

而係喺 `except`內使用：

```python
logger.exception("Operation failed unexpectedly")
```

`logger.exception()`唔係新level；佢係：

```text
ERROR level + 目前exception traceback
```

### `CRITICAL`

目前project未有需要。CRITICAL通常表示整個system或核心依賴已無法運作，唔應用嚟代替普通ERROR。

## Log message格式

目前統一使用：

```text
Human-readable outcome: operation=... user_id=... object_id=... result=...
```

例子：

```python
logger.info(
    "Feedback created: "
    "operation=%s user_id=%s feedback_id=%s feedback_type=%s",
    "feedback_create",
    self.request.user.pk,
    user_feedback.pk,
    feedback_type,
)
```

### 點解用 `%s`，而唔係f-string

Logging module會延遲格式化：

```python
logger.info("user_id=%s", user.pk)
```

只有當對應level真係會輸出時，先組合完整message。

相比：

```python
logger.info(f"user_id={user.pk}")
```

`%s` placeholders更符合Python logging慣例，亦方便logger處理原始arguments。

### Operation命名

Operation統一使用snake_case：

```text
vocab_request_create
vocab_request_review
user_vocab_sync
quiz_submit_answer
feedback_reply
dev_clear_vocab
```

Operation代表「呢件事屬於邊個flow」，human-readable message代表「今次結果係咩」。

### Context field命名

ID fields明確以 `_id`結尾：

```text
user_id
reviewer_user_id
vocab_id
vocab_request_id
feedback_id
event_id
```

避免以下含糊名稱：

```text
review_by
user
target
object
```

## Vocab request同admin review

### User request flow

Create／restore／update／delete request記錄三類結果：

```text
created
skipped
rejected by business validation
```

Created例子：

```python
logger.info(
    "Vocab update request created: "
    "operation=%s user_id=%s vocab_id=%s",
    "vocab_request_update",
    self.request.user.pk,
    self.target_vocab.pk,
)
```

Duplicate pending request唔係server error：

```python
logger.info(
    "Vocab update request skipped: "
    "operation=%s user_id=%s vocab_id=%s reason=%s",
    "vocab_request_update",
    self.request.user.pk,
    self.target_vocab.pk,
    "pending_request_exists",
)
```

Business `ValidationError`亦使用 INFO，而唔係ERROR：

```python
logger.info(
    "Vocab update request rejected by business validation: "
    "operation=%s user_id=%s vocab_id=%s error=%s",
    ...,
)
```

原因：validation已被view正常處理，user會收到form error，request唔應變成500。

### Admin review flow

Approve／reject共用：

```python
def log_review_result(
    self,
    *,
    request,
    review_action,
    vocab_request,
    result,
    level=logging.INFO,
):
    logger.log(level, ...)
```

使用 `logger.log(level, ...)`，可以由caller選擇：

```python
logging.INFO
logging.WARNING
```

目前結果包括：

- `approved`
- `rejected`
- `skipped`
- `validation_rejected`
- `permission_denied`

Permission denied使用WARNING，其餘預期review結果使用INFO。

成功log由admin orchestration layer負責，而唔係在 `VocabActionService`每個CRUD method重複記錄。原因會喺「點解部分位置唔加log」再解釋。

## UserVocab flow

### `in_use`更新

Bulk update只喺實際有records改變時記錄：

```python
if (activated_count + deactivated_count) > 0:
    logger.info(
        "User vocab usage updated: "
        "operation=%s user_id=%s "
        "activated_count=%s deactivated_count=%s",
        ...,
    )
```

Single update亦先比較舊值同新值：

```python
if user_vocab.in_use != new_in_use:
    ...
    logger.info(...)
```

即係no-change submission唔會製造log。

### Sync success

UserVocab sync可能喺以下位置觸發：

- Registration；
- Login；
- User detail refresh。

如果每次sync成功都記log，即使零新增都會製造大量噪音。因此success log只喺database實際新增`UserVocab`時出現。

`sync_new_vocab()`使用：

```python
with transaction.atomic():
    User.objects.select_for_update().get(pk=user.pk)
```

作用：

- 同一user嘅sync串行化；
- 避免兩個sync同時準備同一批rows；
- 令before／after count比較更可靠。

實際created count：

```python
before_sync_count = UserVocab.objects.filter(user=user).count()

UserVocab.objects.bulk_create(
    user_vocabs,
    ignore_conflicts=True,
)

after_sync_count = UserVocab.objects.filter(user=user).count()
return max(after_sync_count - before_sync_count, 0)
```

Wrapper只喺count大過0時記：

```python
if created_count > 0:
    logger.info(
        "User vocab sync completed: "
        "operation=%s user_id=%s created_count=%s",
        "user_vocab_sync",
        user.pk,
        created_count,
    )
```

結果：

```text
實際新增12 rows → INFO created_count=12
零新增          → 冇success log
sync exception  → ERROR + traceback
```

### Sync failure boundary

Primary UserVocab sync同event generation分開處理：

```python
try:
    created_count = UserVocabService.sync_new_vocab(user=user)
except Exception:
    logger.exception("User vocab sync failed: ...")
    return

try:
    EventService.gen_vocab_sync_event(user=user)
except Exception:
    logger.exception("User vocab sync event generation failed: ...")
```

咁做令：

- UserVocab sync失敗會保留traceback，之後可以重試；
- Sync成功後event generation失敗，已sync資料唔會被回滾；
- 兩類failure可以由operation分辨。

## Quiz flow

Quiz logging集中記錄會影響flow理解或learning state嘅事件：

- Setting saved；
- Redirect去unfinished question／session；
- Insufficient active vocab；
- No question available；
- Stale／duplicate answer ignored；
- Answer checked；
- Question skipped；
- Quiz completed summary。

Answer log例子：

```python
logger.info(
    "Quiz answer checked: "
    "operation=%s user_id=%s question_user_vocab_id=%s "
    "user_answer=%s is_correct=%s",
    ...,
)
```

Summary log會保存：

- Quiz count；
- Target count；
- Correct／wrong count；
- Skipped count；
- Tips count；
- Fallback有冇使用。

普通question pick同Next唔記，因為：

- 出現頻率高；
- 冇直接修改learning state；
- 由answer／skip／summary logs已足夠重建主要flow。

## Account flow

### Registration

User成功保存後記：

```python
logger.info(
    "User registration completed: "
    "operation=%s user_id=%s",
    "user_registration",
    self.object.pk,
)
```

只記user ID，唔記email、username、password或form data。

### Login

Login完成同session expiry設定後記：

```python
logger.info(
    "User login completed: "
    "operation=%s user_id=%s remember_me=%s",
    "user_login",
    self.request.user.pk,
    remember,
)
```

Invalid password屬於預期authentication failure，唔記成ERROR。

Logout冇額外log，因為要純為logging override `LogoutView` lifecycle，收益不足。

## Event同Feedback flow

### Event bulk mark-read

`QuerySet.update()`會回傳實際updated row count：

```python
updated_count = get_select_qs.update(
    is_read=True,
    read_at=now,
)
```

只在count大過0時記：

```python
if updated_count > 0:
    logger.info(
        "User events marked as read: "
        "operation=%s user_id=%s updated_count=%s",
        ...,
    )
```

零變更保持安靜。

### Feedback create

成功時記：

```text
operation=feedback_create
user_id
feedback_id
feedback_type
```

Duplicate pending feedback使用INFO：

```text
result=skipped
reason=duplicate_pending_feedback
```

Feedback context／message body永遠唔寫入log。

### Feedback reply

Admin reply transaction成功return後記：

```text
operation=feedback_reply
admin_user_id
feedback_id
event_id
```

Reply body唔寫入log。

### Permission denial

非admin進入admin-only feedback list／detail／reply時使用WARNING：

```python
logger.warning(
    "Feedback admin access denied: "
    "operation=%s user_id=%s view=%s",
    "feedback_admin_access",
    self.request.user.pk,
    self.__class__.__name__,
)
```

## Management commands

### `import_vocab`

記錄：

- Import started；
- CSV file；
- 執行admin user ID；
- Missing file／headers；
- Row validation／integrity rejection；
- Success／failed counts；
- Unexpected failure traceback。

每個failed row只記row number同error，唔記完整raw row。

### `setup_categories`

記錄：

- Setup started／completed；
- CSV file；
- Missing file／headers；
- Invalid row；
- Success／failed counts；
- Unexpected failure traceback。

### `dev_clear_vocab`

呢個係destructive command，所以最少需要：

```text
started
completed
failed unexpectedly
```

核心結構：

```python
logger.info("Clear vocab started: ...")

try:
    with transaction.atomic():
        ...
except Exception:
    logger.exception("Clear vocab failed unexpectedly: ...")
    raise

logger.info("Clear vocab completed: ...")
```

Completed log放喺atomic block外面，只有所有delete成功並正常離開transaction後先會出現。

## Exception ownership同traceback

### 預期exception

例如：

- Form validation；
- Business `ValidationError`；
- Duplicate pending request；
- Missing CSV header；
- Permission denied。

呢啲係application知道點樣處理嘅結果，唔應全部變成ERROR或500。

### 未預期exception

如果application主動捕捉並繼續運作，例如safe sync：

```python
except Exception:
    logger.exception(...)
    return
```

必須用`logger.exception()`保存traceback，否則錯誤會被吞掉。

如果exception冇被application處理，會自然向上成為HTTP 500，則交由：

```text
django.request
```

記錄traceback。

唔應喺每個service layer都：

```python
except Exception:
    logger.exception(...)
    raise
```

然後又由view／Django再記一次。否則同一個exception會出現多份traceback。

簡單原則：

```text
邊一層真正處理／吞掉exception
→ 邊一層負責記traceback

完全唔處理、讓佢成為500
→ 交俾django.request
```

## Transaction同成功log位置

成功log必須代表資料真係完成，而唔係「準備開始」。

錯誤例子：

```python
with transaction.atomic():
    logger.info("Completed")
    do_more_database_work()
```

如果之後database work失敗，transaction會rollback，但log已錯誤寫成completed。

正確概念：

```python
with transaction.atomic():
    do_all_database_work()

logger.info("Completed")
```

Project例子：

- `dev_clear_vocab` completed放喺atomic外面；
- Feedback reply log放喺service成功return後；
- Admin review log放喺approve／reject service成功return後；
- UserVocab sync success使用transaction完成後回傳嘅created count。

## 點解部分位置唔加log

### 普通read views

例如：

- Vocab list／detail；
- UserVocab list／detail GET；
- Event list／detail；
- Feedback list／detail。

正常GET唔修改資料，亦唔係重要audit event。每次page load都記INFO只會製造噪音。Request traffic應由web access log處理。

### `VocabActionService`每個CRUD

唔在底層每個create／update／restore／deactivate都記success，原因：

- Admin review已經有request type同result audit；
- `create_vocab()`亦由CSV import逐row呼叫；
- 底層加log會令import產生大量重複success logs；
- 要分辨來源就要新增source parameter；
- CREATE review要準確記新vocab ID可能要改service return contract。

呢啲logic／interface成本高過額外log價值。

### `EventService.create_event()`／assign helpers

底層event helper呼叫頻密，正常成功逐次記錄會太嘈，而且event message可能包含feedback reply等敏感內容。

因此由外層業務flow記結果：

- Feedback reply；
- Admin review；
- UserVocab sync event failure。

### Quiz question pick／Next

呢啲操作頻率高、價值低，而且唔一定修改learning state。主要flow已有answer、skip、rejection同summary logs。

### Logout

要記logout success需要override Django `LogoutView` lifecycle。純為一條低價值log改view control flow唔值得。

### 零資料變更

以下情況保持安靜：

- UserVocab `in_use`提交但冇改變；
- UserVocab sync新增0 rows；
- Event mark-read更新0 rows。

原則係：

```text
冇資料變更 + 冇重要拒絕結果
→ 唔記success log
```

## 敏感資料邊界

永遠唔應寫入log：

- Password；
- Password hash；
- Cookie；
- Session key；
- CSRF token；
- Access token；
- 完整POST body；
- Feedback context／reply body；
- 其他credential或secret。

目前主要保留：

- User／object IDs；
- Operation；
- Request／vocab／feedback type；
- Result／reason；
- Counts；
- 非敏感boolean，例如`remember_me`、`is_correct`。

敏感資料filter只可以當最後防線。最安全做法係由logger call源頭已經唔傳敏感資料。

## 今次驗證結果

已完成：

- Python compile；
- Django system check；
- `git diff --check`；
- Console／DEBUG／INFO+／ERROR+ file routing手動驗證；
- Formatter、filter同rotation設定檢查；
- Code inspection確認預期validation唔記成ERROR；
- Code inspection確認safe sync failure保留traceback；
- Code inspection確認success log placement同transaction boundary。

目前project test discovery結果：

```text
Found 0 test(s).
NO TESTS RAN
```

因此現有驗證主要係system check、compile、manual routing同code review，尚未有自動log assertions。

## 建議補測試

### Vocab／UserVocab

- Created／skipped／validation rejected message同level；
- Admin approved／rejected／permission denied；
- `in_use` no-change唔產生log；
- Sync實際新增先記created count；
- Concurrent sync只有實際新增嘅執行記success。

### Quiz

- Setting／resume／pool rejection；
- Answer accepted／ignored；
- Skip／summary counts；
- Message placeholders同IDs輸出正確。

### Account／Event／Feedback

- Registration／login success；
- Invalid credentials唔記ERROR；
- Event zero-change mark-read唔記log；
- Feedback duplicate同permission denied level；
- Feedback body唔出現喺log。

### Management commands

- Started／completed；
- Missing file／headers；
- Row rejection；
- Unexpected failure包含traceback；
- Destructive command completed只在transaction成功後出現。

### Exception duplication

- 真正500只出現一次完整traceback；
- Application已處理嘅exception唔再由Django重複記錄；
- Validation／duplicate唔變成ERROR或500。

## 重點心智模型

```text
Logging唔係施工紀錄
Logging係重要業務結果同故障證據
```

判斷一個位置應唔應該加log，可以順序問：

1. 呢件事有冇修改資料或改變重要業務狀態？
2. 之後出問題時，呢條log可唔可以幫我知道發生過咩？
3. 同一資料係咪已經由外層audit log記錄？
4. 呢個操作會唔會高頻到製造噪音？
5. 有冇敏感資料可能被寫入？
6. Success log係咪放喺真正commit／完成之後？
7. Exception traceback應由邊一層擁有？

最終原則：

```text
重要資料變更
→ 記一條清楚summary

預期拒絕
→ INFO／WARNING，唔當500

未預期故障而application會吞掉
→ logger.exception()

未處理故障
→ 交俾django.request

普通read／高頻低價值／零變更
→ 唔記
```

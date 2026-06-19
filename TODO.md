# Project TODO

呢份 TODO 主要記低之後要補嘅位，同埋已經處理咗嘅 decision。  
寫法會盡量用廣東話 + English technical terms，方便自己返嚟睇嗰陣快啲入腦。

## 已 Check 到嘅問題 / Fix Tracking

呢部分係之前檢查 project 時搵到嘅問題，同埋相關 fix progress。

- `[ ]`：仲係待 fix / 待決定。
- `[x]`：已經 fix 或已有明確 decision。

### VocabRequest / Admin Review Flow

- [ ] **第 1 點：真正實作 approve / reject request 嘅處理 flow。**
  - 目前狀態：刻意留返未完成。
  - 要等 approve / reject 真係成功處理完，先可以 show success message。

- [x] **第 2 點：Admin 入面嘅 approve / reject action 由 GET link 改做 POST。**
  - 避免誤 click、refresh page 時重複執行，或者連續 click 造成重複處理。
  - 當 request 已經唔係 `PENDING` 狀態，就唔可以再處理多次。

- [ ] **第 3 點：幫 admin custom approve / reject view 加 permission check。**
  - 等學清楚 Django admin permission flow 之後再補。
  - 要 check reviewer 係咪有 permission 去 change `VocabRequest`。

- [x] **第 4 點：將 `VocabUpdateRequestForm` 入面嘅 `vocab_type` set 做 readonly。**
  - 避免 user 喺 update vocab request 期間改咗 vocab type，令 detail model 關係變亂。

- [x] **第 9 點：Admin 入面由 workflow 控制嘅 fields 要 set 做 readonly。**
  - 例如：`status`、`request_type`、`reviewed_by`，同埋適合 readonly 嘅 proposed data。
  - 狀態變更應該經 approve / reject service 處理，唔應該喺 admin form 直接亂改。

- [x] **第 5A 點：建立 `VocabRequest` 嘅操作要有 transaction atomic。**
  - 避免 create request 中途 exception、server stop，或者其中一部分 save 咗但另一部分冇 save。
  - 目前 create / update / restore / delete request creation 已經用咗 `transaction.atomic()`。

- [ ] **第 5B 點：approve / reject review flow 都要有 transaction atomic。**
  - 之後做第 1 點 approve / reject workflow 嗰陣一齊處理。
  - 如果 review 時要同時 update `VocabRequest`、`Vocab`、`VocabDetail`、`KatakanaDetail` 等資料，應該包喺同一個 transaction 入面。

- [x] **第 7 點：防止同時建立多筆 duplicate pending request。**
  - 目前方向：喺 `Vocab` 加 field，當有 pending request 時 mark / lock 住嗰個 vocab。
  - 亦要考慮 database constraint 或 row lock，因為淨係 check Boolean field，遇到 concurrent request 時仍然可能有 race condition。

- [ ] **第 11 點：決定唔同 vocab type 專屬 fields 嘅 validation rule。**
  - 例如：Katakana type 係咪一定要填 `native_japanese`。

### Vocab

- [x] **第 8 點：公開 vocab list 只 show active vocab。**
  - 喺適合位置加 `is_active=True` filter。

- [x] **第 4 點補充：決定改 vocab type 時，validation 同 related detail 要點處理。**
  - 目前決定：喺 `VocabUpdateRequestForm` 將 vocab type set 做 readonly。

- [x] **第 10 點：保留 `VocabRequest.original_vocab` 目前嘅 `CASCADE` 行為。**
  - 正常 delete vocab 嘅方式係 soft delete / disable，而唔係 database 入面永久 delete。
  - 如果 vocab 真係被永久 delete，目前接受相關 review record 一齊消失。

### Account Admin

- [x] **第 6 點：檢查 custom User Admin 寫法。**
  - `CustomizedUserAdmin` 已繼承 Django standard `UserAdmin`。
  - Add form 會用 `set_password()`，change form 會用 readonly password hash field。
  - 相關原理同之後想深入研究的問題記錄喺 `LEARNING_QUESTIONS.md`。
  - 目前 public registration 同 admin Add User 共用 `RegistForm`。
  - 實作 email activation 時，拆成 public registration form 同 `UserCreationAdminForm`：
    - Public registration 建立 `is_active=False` 的 user，等待 email activation。
    - Admin 建立 user 時可以直接設定 `is_active=True`。

## Data Import / Export / Database Migration

- [ ] **實作由 CSV import vocab list 嘅 management command。**
  - 預計用法：`python manage.py import_vocab list.csv`。
  - `import_vocab.py` 目前只係 command skeleton，仲要加入 CSV file path argument 同真正嘅 import logic。
  - 要 validate CSV headers、required fields、vocab type 同各類 detail data。
  - 遇到 duplicate vocab 或 invalid row 時，要決定 skip、update、停止 import，定係輸出 error report。
  - Import 過程應該用 transaction，避免行到一半失敗後留低 incomplete data。
  - 完成後要 show imported / skipped / failed rows summary。

- [ ] **實作 whole database export command，方便 backup 同日後轉 DB。**
  - 暫定 command name：`python manage.py export_whole <output_folder>`。
  - 將主要 models / database tables 分開 export 成幾個 CSV，而唔係全部塞落同一個 file。
  - CSV 要保留 primary key、foreign key 同必要 relationship，方便之後 restore 或搬去另一個 database。
  - 要考慮 export `User`、`Profile`、`Vocab`、各種 vocab detail、`VocabRequest`、quiz data、notification data 等。
  - Password hash、email 同其他 sensitive data 要決定係咪 export、mask，或者另外加 protected option。
  - Export folder 可以附帶 manifest file，記低 export time、schema version、model list 同 row count。

- [ ] **實作 whole database restore / import command。**
  - 配合 `export_whole` 產生嘅 CSV files，將完整資料 restore 去新 database。
  - 要按 model dependency 決定 import order，避免 foreign key data 未存在。
  - Restore 前要做 schema / version check，並提供 dry-run mode 預先檢查 errors。
  - 呢個功能可以用喺 SQLite 轉 PostgreSQL，或者其他 database migration。

## User Message to Admin

- [ ] **俾一般 user 用普通 message 發一堆想加入嘅字俾 admin。**
  - 呢個係普通 user-to-admin message，唔係 structured request form。
  - User 唔需要逐個字建立 `VocabRequest`，可以喺同一個 message 入面貼上一批 words / phrases。
  - Message 淨係有想加入嘅字都完全可以，唔需要 user 自己填 reading、meaning、type、category 或其他 detail data。
  - 可以另外提供說明，但唔係 required field。
  - Model name 可以考慮 `UserMessage` 或 `AdminInboxMessage`；唔建議叫 `UserEvent`，因為 event 主要係系統用嚟通知 user。

- [ ] **建立 admin inbox 同 message handling flow。**
  - Admin 可以喺後台睇 user message，知道邊個 user 提交咗邊一批字。
  - Message 可以有簡單狀態，例如 `UNREAD`、`READ`、`PROCESSING` 同 `DONE`。
  - Admin 先做資料搜集，確認 vocab、reading、meaning、type 同各種 detail data。
  - 整理完成後建立符合格式嘅 CSV，再用 `python manage.py import_vocab list.csv` 一次過加入 database。
  - 資料搜集、補 details 同整 CSV 全部都係 admin 負責，唔需要 user 再補 form。
  - 可以保留原本 user message 同最後 import batch 嘅關係，方便之後追蹤處理結果。

- [ ] **處理完 user message 後經 event system 通知 user。**
  - Import 時要記低成功加入咗邊啲 vocab、邊啲已存在、邊啲失敗。
  - 系統根據原本 message 建立 user event，等 user 下次 login 時收到結果。
  - 如果同一批 vocab 由多個 users 提出，要確保每個相關 user 都收到自己嘅 event。
  - 要再決定 user 按 OK 後，係一次過將所有成功 vocab 加入 `UserVocab`，定係俾 user 自己揀想加入邊啲。

## Quiz Question Logic

- [ ] **用 weighted random 揀下一條 vocab question。**
  - Question pool 會來自目前 user 嘅 `UserVocab`。
  - 每個 `UserVocab` 已經有 `weight` field，抽題時 weight 越高，被抽中嘅機會就越高。
  - 每次答完題後，會根據答題結果、用咗幾多個 tips 同目前 `streak`，計算今次要加定減幾多 weight。
  - 用越多 tips 先答中，得到嘅 weight reduction 應該越少；詳細 formula 之後再決定。
  - 答錯時亦要結合 tips used 同 streak，決定 weight 要增加幾多。
  - Weight 要設定合理 min / max，避免某啲 vocab 永遠抽唔到，或者長期霸住大部分出題機會。

- [ ] **最近出過嘅 10 題要暫時 skip。**
  - 每次抽下一題前，先排除最近 10 次出現過嘅 vocab，避免同一個字太快重出。
  - 要建立 quiz answer / question history，或者其他 per-user recent question tracking。
  - 唔可以只靠 `last_quiz_at`，因為單一 timestamp 冇辦法準確保留最近 10 題嘅順序。
  - 如果 user 擁有嘅 vocab 少過或接近 10 個，要設計 fallback，避免排除後完全冇題可以抽。

- [ ] **實作 `UserVocab.streak` 更新規則。**
  - Default streak 係 `0`。
  - Streak 大過或等於 `0` 時答中：`streak + 1`。
  - Streak 細過或等於 `0` 時答錯：`streak - 1`。
  - 正 streak 無論去到幾高，第一次答錯只會 reset 做 `0`；再答錯先變 `-1`。
  - 負 streak 無論去到幾低，第一次答中只會 reset 做 `0`；再答中先變 `+1`。
  - 例子：`0 -> 1 -> 2 -> 3 -> 0 -> -1 -> -2`。
  - 相反例子：`0 -> -1 -> -2 -> -3 -> 0 -> 1 -> 2`。

- [ ] **每次答題後更新 `UserVocab` quiz stats。**
  - 答中要增加 `correct_count`；答錯要增加 `incorrect_count`。
  - 同時按上面規則更新 `streak`，並更新 `last_quiz_at`。
  - 要記錄今次答題用咗幾多個 tips，俾 weight calculation 使用。
  - 每次答完題都要即時計算新 weight，而唔係只靠之後嘅 background task。
  - Stats update 同 quiz answer history 應該放入同一個 transaction，避免只 save 到其中一部分。

- [ ] **用 `last_quiz_at` 幫太耐冇出現嘅 vocab 做 overdue weight boost。**
  - 如果某個 vocab 太耐冇被抽中，就自動增加佢嘅 weight，提高重新出題嘅機會。
  - 如果再過一段時間仍然冇被抽中，就再提高 weight，最少拉到該 user 全部 `UserVocab.weight` 嘅平均值。
  - 如果去到更長時間仍然抽唔到，就強制將 weight 提高到一個預設 high value。
  - 每次真正出題後要更新 `last_quiz_at`，並重新開始計算 overdue 時間。
  - 各階段要等幾耐、每次加幾多、high value 係幾多，暫時未決定。

- [ ] **研究自動執行 overdue weight update 嘅方法。**
  - 呢部分留到學識 background / scheduled task 後先實作。
  - 可以研究 Django management command 配合 cron、Celery Beat，或者其他 scheduler。
  - 要避免每次執行都重複無限加 weight，可以記錄 boost stage，或者由 overdue duration 直接計算 target weight。
  - 計算 average weight 時要以每個 user 自己嘅 `UserVocab` 為範圍，唔係全站所有 users 一齊計。

## Event Notification System

- [ ] **建立 site event / announcement model。**
  - Admin 可以建立重要公告，例如新功能、maintenance、quiz event、data update 或 policy change。
  - Event 可以有 title、content、publish time、expire time、importance level 同 active status。
  - 要決定通知係全體 users、指定 user group，定係單一 user。

- [ ] **記錄每個 user 嘅 notification read status。**
  - User login 後可以分到 unread 同已讀 notifications。
  - 要記低邊個 user 已讀、read time，同埋有冇 dismiss。
  - 避免為每個全站公告即時建立大量 duplicate rows，可以考慮 event + user read record 嘅結構。

- [ ] **User login 後顯示重要 event notifications。**
  - Login 後喺首頁、navbar notification icon 或 notification page 顯示未讀消息。
  - High priority event 可以用較明顯提示，但唔應該每次 refresh 都重複彈出。
  - User 可以 mark as read、mark all as read，同查看之前嘅 notification history。
  - Vocab request result 唔會經 email notification，會統一經 site 入面嘅 event system 處理。

## General Improvements

- [ ] **改善 A：** 幫 `Vocab`、`VocabRequest` 等 model 加 `__str__()`，admin 同 debug 時會易睇好多。
- [ ] **改善 B：** 考慮將 `vocabRequestService` rename 做 `VocabRequestService`，跟返 class naming style。
- [ ] **改善 C：** 清走未用嘅 import 同舊嘅 commented query code。
- [ ] **改善 D：** 幫 duplicate request、create / update / delete flow、approve / reject flow 加 tests。
- [ ] **改善 E：** 加 `requirements.txt` 或 `pyproject.toml`，正式記低 project dependencies。
- [ ] **改善 F：** 正式 deploy 前，將 `SECRET_KEY`、`DEBUG` 等 settings 搬去 environment variables。
- [ ] **改善 G：** 清理 `git diff --check` 報告嘅 trailing whitespace。
- [ ] **改善 H：** 實作 `Vocab.word_slug` 嘅產生同同步規則。
  - 目前 `word_slug` 暫時容許 `blank=True, null=True`，create / update vocab 時未處理 slug。
  - 之後要決定 slug 由 `word`、`kana` 定其他資料產生。
  - 要處理 duplicate slug、word 更新時係咪同步更新 slug，以及舊資料 backfill。

## VocabRequest Result / UserVocab Flow

- [ ] **Approve / reject request 後建立 user event。**
  - Vocab request review 完成後，唔會即時寄 email。
  - 系統會建立一個對應 user 嘅 event record，記低 request 係 approved 定 rejected，同埋發生咗咩事。
  - User 下次 login 時先 show 呢個未處理 event。

- [ ] **User 確認 approved request 後，先將 vocab 加入 `UserVocab`。**
  - Approved 唔代表即時將 vocab 加入 user 嘅 `UserVocab`。
  - User login 後先睇 request result，按 OK / confirm 之後，系統先完成 `UserVocab` relationship。
  - 要確保重複 click OK 唔會建立 duplicate `UserVocab` record。
  - Confirm action 應該同 event read / handled status 一齊放入 transaction。

- [ ] **處理 rejected request event。**
  - User login 後可以睇到 request 被 reject，同埋之後可能加入 reviewer reason。
  - User 按 OK 後，將 event mark 做 handled，但唔會改動 `UserVocab`。

## Account Email Activation

- [ ] **研究同設計 account email activation flow。**
  - 呢部分暫時未有確定 idea，之後再決定 implementation。
  - 要再考慮 registration 後係咪即時限制 login、activation link 幾耐 expire，同 resend activation email flow。

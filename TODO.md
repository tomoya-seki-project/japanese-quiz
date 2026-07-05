# Project TODO

呢份 TODO 主要記低之後要補嘅位，同埋已經處理咗嘅 decision。  
寫法會盡量用廣東話 + English technical terms，方便自己返嚟睇嗰陣快啲入腦。

## 目錄

- [已 Check 到嘅問題 / Fix Tracking](#已-check-到嘅問題--fix-tracking)
- [Vocab Future Work](#vocab-future-work)
- [Data Import / Export / Database Migration](#data-import--export--database-migration)
- [User Message to Admin](#user-message-to-admin)
- [Quiz Question Logic](#quiz-question-logic)
- [Event Notification System](#event-notification-system)
- [Logging / Audit Trail](#logging--audit-trail)
- [General Improvements](#general-improvements)
- [VocabRequest Result / UserVocab Flow](#vocabrequest-result--uservocab-flow)
- [Account Email Activation](#account-email-activation)
- [UI / UX](#ui--ux)

## 已 Check 到嘅問題 / Fix Tracking

呢部分係之前檢查 project 時搵到嘅問題，同埋相關 fix progress。

- `[ ]`：仲係待 fix / 待決定。
- `[x]`：已經 fix 或已有明確 decision。
- 必要 fix 用 `第 X 點` 編號追蹤。
- 改善項目用 `改善 A`、`改善 B`...，去到 `改善 Z` 之後用 `改善 AA`、`改善 AB`...。
- 新功能／之後想做嘅功能保持按 category 分類，唔納入 fix / 改善編號。

- [x] **第 1 點（VocabRequest / Admin Review）：真正實作 approve / reject request 嘅處理 flow。**
  - Approve 已按 CREATE / UPDATE / RESTORE / DELETE request type 呼叫對應 vocab action。
  - Reject 會更新 request status 同 reviewer，但唔會改動 vocab。
  - Admin 會根據 service 回傳結果顯示成功或已處理 warning。
  - 已用 browser / admin 手動測試 create、restore、update、delete request，以及 approve / reject 正常 flow。

- [x] **第 2 點（VocabRequest / Admin Review）：Admin 入面嘅 approve / reject action 由 GET link 改做 POST。**
  - 避免誤 click、refresh page 時重複執行，或者連續 click 造成重複處理。
  - 當 request 已經唔係 `PENDING` 狀態，就唔可以再處理多次。

- [ ] **第 3 點（VocabRequest / Admin Review）：確認 admin approve / reject flow 嘅 permission boundary。**
  - 目前 approve / reject 已改為喺 admin change form 入面經 `response_change()` 處理，而唔係獨立 custom URL。
  - 正常入到 admin change page 已經會受 Django admin permission 控制。
  - 之後要再確認呢個 permission boundary 是否足夠，定係需要喺 approve / reject branch 入面額外 call `has_change_permission()`。

- [x] **第 4 點（VocabRequest Form）：將 `VocabUpdateRequestForm` 入面嘅 `vocab_type` set 做 readonly。**
  - 避免 user 喺 update vocab request 期間改咗 vocab type，令 detail model 關係變亂。

- [x] **第 5 點（VocabRequest Transaction）：建立 `VocabRequest` 嘅操作要有 transaction atomic。**
  - 避免 create request 中途 exception、server stop，或者其中一部分 save 咗但另一部分冇 save。
  - 目前 create / update / restore / delete request creation 已經用咗 `transaction.atomic()`。

- [x] **第 6 點（VocabRequest / Admin Review）：approve / reject review flow 都要有 transaction atomic。**
  - Approve / reject 已使用 `transaction.atomic()`、`select_for_update()` 同 `PENDING` status check。
  - Review 時更新 `VocabRequest` 同執行 vocab action 會放喺同一個 transaction 入面。

- [x] **第 7 點（VocabRequest Duplicate Check）：防止同時建立多筆 duplicate pending request。**
  - Service 會先檢查有冇 pending request，提供較清楚嘅正常 flow feedback。
  - Database 已加入 conditional unique constraints，防止 concurrent requests 同時通過 application check。

- [x] **第 8 點（VocabRequest View Error Handling）：處理建立 `VocabRequest` 時 service 拋出嘅 `ValidationError`。**
  - Create / update / restore / delete request 遇到 concurrent duplicate 時，service 會將 `IntegrityError` 轉成 `ValidationError`。
  - `VocabCreateRequestView`、`VocabUpdateRequestView` 同 `VocabDeleteRequestView` 已喺 call service 時捕捉 `ValidationError`。
  - View 會將錯誤加入 form non-field errors，並回到 `form_invalid()`，避免 exception 穿出 request flow。

- [x] **第 9 點（VocabRequest / Admin Review）：擴大 admin review concurrency protection 範圍。**
  - `VocabRequestAdmin.get_queryset()` 會喺 approve / reject POST 時使用 `select_for_update()`，令 admin change form save 前先鎖住目標 request row。
  - `VocabRequestService.approve_vocab_request()` / `reject_vocab_request()` 仍保留 service-level `select_for_update()`，避免日後其他 caller 繞過 admin protection。
  - Reviewed request 會經 `get_readonly_fields()` 設為 readonly，並由 `save_model()` 擋住非 pending request 被再次保存。
  - 已手動測試 approve / reject 正常操作；之後可以再用 automated tests 驗證兩個 admin 同時 review 同舊頁面 submit 嘅情況。

- [x] **第 10 點（VocabRequest / Admin Review）：Admin 入面由 workflow 控制嘅 fields 要 set 做 readonly。**
  - 例如：`status`、`request_type`、`reviewed_by`，同埋適合 readonly 嘅 proposed data。
  - 狀態變更應該經 approve / reject service 處理，唔應該喺 admin form 直接亂改。

- [x] **第 11 點（VocabRequest Form）：統一 request form required fields 同 submission 設計。**
  - TODO 原本決定 user submit CREATE request 時可以將 `meaning`、`level`、`category` 留空，由 admin review 時補返。
  - `VocabCreateRequestForm` 已將 `meaning`、`level`、`category` 設為 optional。
  - Approve 前會再經 `validate_for_approval()` 檢查最終 proposed data 是否足夠。
  - `VocabUpdateRequestForm` 仍保留較嚴格 required fields，因為 update form 會由原本 vocab data 提供 initial value。

- [x] **第 12 點（VocabRequest Validation）：決定唔同 vocab type 專屬 fields 嘅 validation rule。**
  - CREATE / UPDATE Katakana request 喺 approve 時必須有 `proposed_native_japanese`。

- [x] **第 13 點（Vocab List）：公開 vocab list 只 show active vocab。**
  - 喺適合位置加 `is_active=True` filter。

- [x] **第 14 點（Vocab Type）：決定改 vocab type 時，validation 同 related detail 要點處理。**
  - 目前決定：喺 `VocabUpdateRequestForm` 將 vocab type set 做 readonly。

- [x] **第 15 點（VocabRequest Model）：保留 `VocabRequest.original_vocab` 目前嘅 `CASCADE` 行為。**
  - 正常 delete vocab 嘅方式係 soft delete / disable，而唔係 database 入面永久 delete。
  - 如果 vocab 真係被永久 delete，目前接受相關 review record 一齊消失。

- [x] **第 16 點（Vocab Model Integrity）：確保 `Vocab.type` 同對應 detail model 保持一致。**
  - `vocab` type 應該有 `VocabDetail`；`katakana` type 應該有 `KatakanaDetail`。
  - 正式 create vocab path 交由 `VocabActionService` 處理，確保 create 主表時同時建立對應 detail model。
  - `VocabAdmin.has_add_permission()` 已禁止 admin 直接新增 vocab，避免繞過 service create flow。
  - `VocabAdmin.readonly_fields` 已將 `type` 設為 readonly，避免 admin 直接改 existing vocab type 造成 type/detail mismatch。
  - 舊資料或 future bypass service 嘅情況仍要靠之後 data audit / tests 留意。

- [x] **第 17 點（VocabRequest Form）：清理已移除嘅 `similar_word` form 設計。**
  - `Vocab.similar_word` 已經移除，但 `BaseVocabRequestForm` 仲保留 `similar_word` input。
  - `BaseVocabRequestForm` 入面嘅 `similar_word` field 已停用。
  - Vocab request creation / update flow 入面 related save code 亦已停用，避免 user 以為提交咗但實際被忽略。

- [x] **第 18 點（Account Admin）：檢查 custom User Admin 寫法。**
  - `CustomizedUserAdmin` 已繼承 Django standard `UserAdmin`。
  - Add form 會用 `set_password()`，change form 會用 readonly password hash field。
  - 相關原理同之後想深入研究的問題記錄喺 `LEARNING_POINTS.md`。
  - 目前 public registration 同 admin Add User 共用 `RegistForm`。
  - 實作 email activation 時，拆成 public registration form 同 `UserCreationAdminForm`：
    - Public registration 建立 `is_active=False` 的 user，等待 email activation。
    - Admin 建立 user 時可以直接設定 `is_active=True`。

- [x] **第 19 點（Account Login）：移除 login flow 入面冇實際作用嘅 `user.save()`。**
  - Django `LoginView` 已經會透過 authentication flow 更新 `last_login`。
  - 已移除 login 成功後無欄位改動嘅額外 `user.save()`，避免多餘 database write。

- [x] **第 20 點（UserVocab Flow）：穩定 UserVocab 選擇頁 GET / POST 之間嘅候選範圍。**
  - 原本嘅 `UserVocabSelectVocabView` 會每次 request 重新計算候選 vocab，GET / POST 之間可能出現候選範圍變動。
  - 目前加字主流程已改成 login 後自動 sync 新 vocab，先建立 `UserVocab(in_use=False)`。
  - 舊 selection flow 暫時唔作為主要加字入口，相關 `ModelMultipleChoiceField` pattern 已移入 `LEARNING_POINTS.md` 保留做之後參考。

## Vocab Future Work

- [ ] **實作 `Vocab.word_slug` 嘅產生同同步規則。**
  - 目前 `word_slug` 暫時容許 `blank=True, null=True`，create / update vocab 時未處理 slug。
  - 之後要決定 slug 由 `word`、`kana` 定其他資料產生。
  - 要處理 duplicate slug、word 更新時係咪同步更新 slug，以及舊資料 backfill。

- [ ] **將 vocab category 改成最多可以選擇三個 category。**
  - 已完成：
    - 已決定之後支援一個 vocab 最多三個 categories。
    - CSV import header 已暫定使用 `category1`、`category2`、`category3`。
  - 未完成：
    - 目前 `Vocab.category` 仍係單一 `CharField`，只可以保存一個 category。
    - 之後要改用 category model 配合 `ManyToManyField` 處理一個 vocab 對多個 categories。
    - 每個 vocab 最多只可以有三個 categories，需要喺 form / service validation 限制數量。
    - CSV import 要安全跳過空白 category 欄位，亦要檢查每個 category value 是否合法。
    - 改 schema 時要處理現有 `Vocab.category` 資料 migration，避免舊 category 資料遺失。

## Data Import / Export / Database Migration

- [ ] **完善由 CSV import vocab list 嘅 management command。**
  - 預計用法：`python manage.py import_vocab list.csv`。
  - 已完成：
    - 已加入 CSV path argument。
    - 已加入 superuser authentication。
    - 已加入 header validation。
    - 已加入 row-level validation / error handling。
    - 已經經 `VocabActionService` creation flow 建立 vocab。
    - Duplicate vocab 或 invalid row 目前會輸出錯誤並繼續處理下一行。
    - 每筆 vocab creation 已經由 service transaction 保護，避免只建立主表但冇建立 detail。
    - 完成後會 show imported / failed rows count。
    - 已保留每個 failed row 嘅行數及錯誤原因。
  - 未完成：
    - 如之後需要更細分，可以再加 skipped rows count。
    - 之後可以再考慮輸出 summary log file，方便大量 import 後 review。

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
  - 成功加入嘅 vocab 會先建立 `UserVocab(in_use=False)`，之後由 user 自己喺 list 入面啟用想練嘅字。

## Quiz Question Logic

- [ ] **按 vocab type / level / category 篩選 quiz 出題範圍。**
  - Quiz 開始前，user 可以選擇今次想練習嘅 `type`、`level` 同 `category`。
  - Filter 條件應套用喺目前 user 擁有且 `in_use=True` 嘅 `UserVocab` question pool，而唔係全站所有 vocab。
  - 要支援單一條件、複數條件，以及唔設定條件時使用全部可用 vocab。
  - 如果 filter 後冇任何可出題 vocab，要顯示清楚提示，唔應直接抽題失敗。
  - Weighted random、最近 10 題排除同 overdue boost，都應該喺 filter 後嘅 question pool 上運作。

- [ ] **用 weighted random 揀下一條 vocab question。**
  - 已完成：
    - `UserVocab` 已有 `weight` field。
    - 已決定 question pool 會來自目前 user 嘅 `UserVocab`。
    - 已決定抽題時 weight 越高，被抽中嘅機會越高。
  - 未完成：
    - 未實作 weighted random selection logic。
    - 每次答完題後，要根據答題結果、tips used 同目前 `streak`，計算今次要加定減幾多 weight。
    - 用越多 tips 先答中，得到嘅 weight reduction 應該越少；詳細 formula 之後再決定。
    - 答錯時亦要結合 tips used 同 streak，決定 weight 要增加幾多。
    - Weight 要設定合理 min / max，避免某啲 vocab 永遠抽唔到，或者長期霸住大部分出題機會。

- [ ] **最近出過嘅 10 題要暫時 skip。**
  - 每次抽下一題前，先排除最近 10 次出現過嘅 vocab，避免同一個字太快重出。
  - 要建立 quiz answer / question history，或者其他 per-user recent question tracking。
  - 唔可以只靠 `last_quiz_at`，因為單一 timestamp 冇辦法準確保留最近 10 題嘅順序。
  - 如果 user 擁有嘅 vocab 少過或接近 10 個，要設計 fallback，避免排除後完全冇題可以抽。

- [ ] **實作 `UserVocab.streak` 更新規則。**
  - 已完成：
    - `UserVocab` 已有 `streak` field，default 係 `0`。
    - 已決定 streak 更新規則。
  - 未完成：
    - 未實作答題後更新 streak 嘅 service / logic。
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

- [x] **建立 event / user-event data model foundation。**
  - 已建立 `Event` model，用嚟保存 event type、title 同 message。
  - 已建立 `UserEvent` through model，用嚟保存每個 user 對 event 嘅 read status。
  - `UserEvent` 已加入 `(user, event)` unique constraint，避免同一個 user 對同一個 event 出現 duplicate read record。
  - `Event` 已註冊到 admin，方便之後檢查 event data。

- [ ] **完善 site announcement / notification model fields。**
  - Admin 可以建立重要公告，例如新功能、maintenance、quiz event、data update 或 policy change。
  - 之後再決定是否加入 publish time、expire time、importance level、active status、target user group 等欄位。
  - 要決定通知係全體 users、指定 user group，定係單一 user。

- [x] **記錄每個 user 嘅 notification read status。**
  - `UserEvent.is_read` 同 `read_at` 已可記低 user 是否已讀同已讀時間。
  - Event + UserEvent relationship 可以避免為每個全站公告直接複製完整 event content。

- [ ] **實作 notification read / dismiss 操作。**
  - User login 後可以分到 unread 同已讀 notifications。
  - User 可以 mark as read、mark all as read，同查看之前嘅 notification history。
  - 之後要決定是否需要 dismiss 狀態；如果需要，可能要喺 `UserEvent` 加欄位。

- [ ] **User login 後顯示重要 event notifications。**
  - Login 後喺首頁、navbar notification icon 或 notification page 顯示未讀消息。
  - High priority event 可以用較明顯提示，但唔應該每次 refresh 都重複彈出。
  - Vocab request result 唔會經 email notification，會統一經 site 入面嘅 event system 處理。

## Logging / Audit Trail

- [ ] **為 CSV vocab import command 加正式 log / import report。**
  - 目前 `import_vocab` 已開始整理 import 結果資料，例如 `success_count`、`failed_rows`、`row_number` 同 `error_message`。
  - 之後可以基於呢批 structured data 輸出正式 log，而唔只係即時 print terminal message。
  - Log 應記低 import file、執行 admin、執行時間、成功筆數、失敗筆數、每個 failed row 嘅 row number 同錯誤原因。
  - 可以先做成 terminal summary + log file，之後再考慮 database import history model。
  - 如果 user message / admin inbox 之後會觸發 CSV import，可以用 import report 回寫處理結果，再經 event system 通知相關 user。

## General Improvements

- [x] **改善 A：** 幫 `Vocab`、`VocabRequest` 等 model 加 `__str__()`，admin 同 debug 時會易睇好多。
- [x] **改善 B：** 將 `vocabRequestService` rename 做 `VocabRequestService`，跟返 class naming style。
- [ ] **改善 C：** 清走未用嘅 import 同舊嘅 commented query code。
- [ ] **改善 D：** 幫 duplicate request、create / update / delete flow、approve / reject flow 加 tests。
- [ ] **改善 E：** 加 `requirements.txt` 或 `pyproject.toml`，正式記低 project dependencies。
- [ ] **改善 F：** 正式 deploy 前，將 `SECRET_KEY`、`DEBUG` 等 settings 搬去 environment variables。
- [ ] **改善 G：** 清理 `git diff --check` 報告嘅 trailing whitespace。

- [x] **改善 H：** Approve request 時驗證 review 後嘅最終 proposed data 是否足夠。
  - User submit CREATE request 時，容許 `meaning`、`level`、`category` 等 proposed fields 留空，由 admin review 時補返或修改。
  - UPDATE request 會由原本 vocab 放 initial data；如果原本資料係空，admin review 時同樣可以補返。
  - Nullable proposed fields 係 request submission / review workflow 嘅設計，唔代表 user submit 時必須填齊。
  - 只係 admin 撳 Approve 嗰刻，先要驗證最終 proposed data 能否安全寫入 `Vocab` 同相關 detail model。
  - 資料仍然不足時，應留喺 review page 顯示清楚錯誤，唔執行 vocab action，亦唔將 request 標成 approved。

- [ ] **改善 I：** Approve UPDATE / RESTORE / DELETE request 前驗證 `original_vocab`。
  - 呢三種 request 都依賴 `original_vocab` 作為目標。
  - 如果 `original_vocab` 係 `None`、已被刪除，或者資料狀態唔符合 request type，應停止處理並回傳清楚 error result。

- [ ] **改善 J：** 收窄 `UserVocab` bulk in-use update 嘅 POST validation 範圍。
  - 目前 `UserVocabInUseUpdateForm` 使用 `UserVocabListView.get_queryset()` 作為 validation queryset。
  - 呢個 queryset 會限制喺目前 user 同 filter 條件內，但未必只限當前 pagination page 顯示嘅 rows。
  - 正常 browser submit 只會提交當前 page 嘅 `selectable_ids`，而且 update 時有 `user=request.user` 保護，暫時唔會改到其他 user 資料。
  - 之後如要更嚴謹，可以喺 POST 時重新 paginate queryset，將當前 page `object_list` 傳入 form 作 validation queryset。

## VocabRequest Result / UserVocab Flow

- [ ] **Approve / reject request 後建立 user event。**
  - Vocab request review 完成後，唔會即時寄 email。
  - 系統會建立一個對應 user 嘅 event record，記低 request 係 approved 定 rejected，同埋發生咗咩事。
  - Approved / imported 新字會先建立 `UserVocab` record，但預設 `in_use=False`。
  - User 下次 login 時先 show event notice，提醒有新字可查看／啟用。

- [ ] **UserVocab 新字預設 `in_use=False`，由 user 自己啟用。**
  - 已完成：
    - `UserVocab` 已加入 `in_use` field，default 為 `False`。
    - `UserVocabListView` 已可以按 `in_use=True / False` filter。
    - 新 `UserVocab` relationship 可先建立，但未必即時加入 quiz pool。
    - Login 成功後會呼叫 `UserVocabService.sync_new_vocab()`，自動為 user 建立未擁有 vocab 嘅 `UserVocab` records。
    - Register 成功後亦會呼叫 `UserVocabService.sync_new_vocab()`，為新 user 建立現有 vocab 嘅 `UserVocab` records。
    - `UserVocabListView` 已加入 POST bulk update flow，用 `selectable_ids` / `selected_ids` 更新當前顯示項目嘅 `in_use` 狀態。
    - UserVocab list template 已加入 checkbox UI，提交 `selectable_ids` 同 `selected_ids`。
    - 已用 browser 測試 select all / checkbox 更新 `in_use` flow。
  - 未完成：
    - Quiz question pool 要只使用 `in_use=True` 嘅 `UserVocab`。
    - EventNotice system 要通知 user 有新字已加入個人 list，但仍未啟用。
    - 可以再整理 `sync_new_vocab()` 是否每次 login sync 全部未擁有 vocab，定係之後改成 event-driven / batch flow。

- [ ] **處理 rejected request event。**
  - User login 後可以睇到 request 被 reject，同埋之後可能加入 reviewer reason。
  - User 按 OK 後，將 event mark 做 handled，但唔會改動 `UserVocab`。

## Account Email Activation

- [ ] **研究同設計 account email activation flow。**
  - 呢部分暫時未有確定 idea，之後再決定 implementation。
  - 要再考慮 registration 後係咪即時限制 login、activation link 幾耐 expire，同 resend activation email flow。

## UI / UX

- [ ] **整一個 50 音假名 keyboard。**
  - 只用喺 user 回答 quiz 嘅介面。
  - Vocab search、create request、update request 等其他 forms 繼續使用普通 keyboard。
  - 俾冇安裝日文輸入法，或者答 quiz 時需要假名提示嘅 user 使用。
  - 按下假名後，將文字插入 quiz answer input，而唔係覆蓋原有內容。
  - 考慮平假名／片假名切換、濁音／半濁音、拗音、促音同長音符號。
  - 可以加入簡單提示，幫 user 確認讀音或輸入方式。

- [ ] **為 vocab / user vocab list 加入 Ajax partial pagination。**
  - 已完成：
    - `VocabListView` 已拆成 main template + partial template。
    - `VocabListView.render_to_response()` 已可根據 `X-Requested-With` header 回傳 partial。
    - `vocab_list.html` 已加入 Ajax click handler，pagination click 可以局部更新 vocab list 區域。
    - `VocabListView.get_context_data()` 已建立 `query_string`，pagination link 可以保留現有 GET search filter。
    - Pagination link 保留普通 `<a href>`，所以 non-JavaScript fallback 仍可完整 reload page。
    - 相關 query string / pagination 處理方法已記錄喺 `LEARNING_POINTS.md`。
    - 已用 browser 實際測試 search + pagination + Ajax partial update flow。
    - `UserVocabListView` 已開始拆成 main template + partial template。
    - `UserVocabListView.render_to_response()` 已可根據 `X-Requested-With` header 回傳 partial。
    - `user_vocab_list.html` 已加入 Ajax pagination click handler，並喺 partial replace 後重新 call checkbox setup function。
    - `UserVocabListView.get_context_data()` 已建立 `query_string`，pagination link 可以保留現有 GET search filter。
    - Checkbox setup reload / event delegation / HTMX 等處理方法已記錄喺 `LEARNING_POINTS.md`。
    - 已用 browser 測試 `UserVocabListView` search + pagination + Ajax partial update + checkbox select-all flow。
  - 未完成：
    - 之後可以考慮將 checkbox event binding 由 setup reload function refactor 成 event delegation。

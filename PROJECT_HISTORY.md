# Project History

呢份文件記錄 Japanese Quiz project 嘅主要開發里程碑，集中描述功能、架構決定、資料模型演進同重要技術學習。一般檔案建立、template 微調、URL 整理等基礎操作不會逐項記錄。

## 2026-05-20 - Project foundation

Commit: `ad4deee`

### 主要改動

- 建立 Django project 基礎架構，加入 `accounts`、`dictionary`、`quiz` 同 `core` apps。
- 開始設計 custom user、user profile、vocab、user vocab relationship 同 vocab detail models。

### Database 改動

- 建立 custom `User` 同 `UserProfile` tables。
- `UserProfile` 以 One-to-One relationship 連接 user，並保存建立／更新時間。

### 理由

### 學到咩

## 2026-05-20 - Initial schema and custom user manager

Commit: `adf7f9e`

### 主要改動

- 建立以 email 為登入識別嘅 custom user 架構。
- 加入 custom `UserManager`，統一一般 user 同 superuser 嘅建立流程。

### Database 改動

- 建立 `Vocab`、`UserVocab`、`KanjiDetail` 同 `KatakanaDetail` tables。
- 建立 user-vocab Many-to-Many through relationship。
- 為 vocab 加入 `(word, answer)` unique constraint。
- 將 `User` model manager 切換成 custom `UserManager`。

### 理由

### 學到咩

## 2026-05-25 - Authentication flow

Commit: `be08b3d`

### 主要改動

- 完成 user registration、login 同 logout 基本流程。
- 建立共用 authentication forms，令 project 開始支援實際 user session。

### Database 改動

- 無 schema 變更。

### 理由

### 學到咩

## 2026-05-29 - User area and initial vocab creation flow

Commit: `c67a9d0`

### 主要改動

- 建立 user account pages，並開始實作 vocab creation flow。
- 加入 `AdminMessage`，準備保存 user 與 admin 之間嘅訊息關係。
- 整理 vocab 與 quiz tracking 欄位命名。

### Database 改動

- 建立 `AdminMessage` table，並連接 custom user。
- `UserVocab` 加入 `weight`、答對／答錯次數同 `last_quiz_at`，準備記錄 quiz 表現。
- `Vocab.answer` rename 為 `kana`。
- `UserVocab` 答題統計欄位 rename 為 `correct_count`、`incorrect_count`，並加入 `streak`。
- Detail models 加入 `similar_kanji`、`native_japanese` 等 type-specific fields。
- 調整 vocab type/category choices，統一使用程式可處理嘅 value。
- 建立 `(word, kana)` 同 `(user, vocab)` unique constraints。

### 理由

### 學到咩

## 2026-06-02 - VocabRequest foundation

Commit: `e8b7bb8`

### 主要改動

- 將 vocab create、update、delete 改成 request-based workflow，避免 user 直接修改正式 vocab data。
- 建立 request forms 同初步處理流程。

### Database 改動

- 無已套用 migration；`VocabRequest` schema 仍處於設計階段。

### 理由

### 學到咩

## 2026-06-02 - Create request completion and account metadata

Commit: `cdcd761`

### 主要改動

- 完成 create vocab request 嘅主要提交及 validation flow。
- 改善 request proposed fields 同 model relationships。

### Database 改動

- 調整 `User.last_login` 欄位設定。
- 建立 `VocabRequest` table，保存 request type、review status、proposed data、申請人、reviewer 同原始 vocab 關係。
- 從 `Vocab` 移除舊 `status`，改由 `VocabRequest.status` 管理審批狀態。
- `Vocab` 暫時加入 `has_submission`，標示是否存在 submission。

### 理由

### 學到咩

## 2026-06-04 - Restore request and request module separation

Commit: `bc37573`

### 主要改動

- 加入 restore vocab request flow。
- 將一般 vocab views 同 request views 分開，降低兩類流程嘅耦合。

### Database 改動

- 修正 `VocabRequest` proposed category/similar field 命名。
- `request_type` 加入 `RESTORE` choice。

### 理由

### 學到咩

## 2026-06-06 - Update request workflow

Commit: `259ce8e`

### 主要改動

- 完成 vocab update request flow。
- 開始保存 update 前嘅 vocab snapshot，方便 review 時比較 proposed data。

### Database 改動

- 無已套用 migration；相關 model changes 喺下一個 commit 正式寫入 schema。

### 理由

### 學到咩

## 2026-06-07 - Vocab browsing and request schema refinement

Commit: `0280a4d`

### 主要改動

- 完成 vocab list、detail 同 update pages 嘅主要瀏覽流程。
- 整合 authentication 後嘅 vocab navigation。

### Database 改動

- `approved_by` rename 為 `reviewed_by`，令 request reviewer 語意更準確。
- 移除 `Vocab.has_submission`。
- `VocabRequest` 加入 `original_data` JSON field。
- 將 request type `edit` 統一為 `update`。

### 理由

### 學到咩

## 2026-06-09 - User vocab list and nullable request data

Commit: `99e7214`

### 主要改動

- 加入 user 專屬 vocab list。
- 改善 request validation，支援唔同 request type 只保存相關 proposed data。

### Database 改動

- 多個 `VocabRequest.proposed_*` fields 改成 nullable/blank，容許 request submission 階段保存未完整資料。

### 理由

### 學到咩

## 2026-06-10 - Create/delete request completion

Commit: `144c719`

### 主要改動

- 完成 create 同 delete vocab request 嘅 user flow。
- 統一 dictionary request routing 同頁面流程。

### Database 改動

- 將 `VocabRequest` database table 明確命名為 `vocab_request`。

### 理由

### 學到咩

## 2026-06-12 - Dictionary admin foundation and vocab detail redesign

Commit: `d16bdd6`

### 主要改動

- 建立 accounts、core 同 dictionary 嘅 admin 管理基礎。
- 開始準備 CSV import command。
- 將一般 vocab detail 同 katakana-specific detail 分開處理。

### Database 改動

- `Vocab.type` 由 `kanji` 調整為較通用嘅 `vocab`。
- `KanjiDetail` 改為 `VocabDetail`。
- `similar_word` 移到 `Vocab`，並同步調整 request proposed field。

### 理由

### 學到咩

## 2026-06-14 - Admin data cleanup and schema labels

Commit: `80c655f`

### 主要改動

- 改善 dictionary admin 顯示同資料管理設定。
- 準備 vocab CSV import/export commands。
- 清理已經唔再使用嘅 original word 設計。

### Database 改動

- 移除 `VocabRequest.proposed_original_word` 同 `KatakanaDetail.original_word`。
- 為主要 vocab、request 同 quiz tracking fields 加入 `verbose_name`。
- 整理 `VocabRequest` foreign key related names。

### 理由

### 學到咩

## 2026-06-15 - Admin VocabRequest review architecture

Commit: `244c793`

### 主要改動

- 建立 admin approve/reject review interface。
- 將 request business logic 抽到 `VocabRequestService`，減少 admin/view 直接處理 domain logic。
- 建立 custom admin change form，讓 reviewer 可以逐筆檢查 request。

### Database 改動

- 無 schema 變更。

### 理由

### 學到咩

## 2026-06-17 - Transaction-safe request creation

Commit: `d65b3df`

### 主要改動

- 使用 `transaction.atomic()` 保護 request creation，避免流程中途失敗留下不完整資料。
- 擴充 vocab categories 同 level choices。
- 加入 database-level duplicate pending request protection。

### Database 改動

- 擴充 `Vocab.category`／`proposed_category` choices，並加入未定義 level。
- 為有 `original_vocab` 嘅 pending request 建立 conditional unique constraint。
- 為 create request 嘅 `(proposed_word, proposed_kana)` 建立 conditional unique constraint。

### 技術重點

- `transaction.atomic()` 令區塊內操作全部成功先 commit；發生 exception 時會 rollback。
- Application check 可以提供清楚 feedback，database constraint 則負責最後一道 concurrency protection。

### 理由

### 學到咩

## 2026-06-19 - Custom UserAdmin and vocab action preparation

Commit: `c1979dc`

### 主要改動

- 將 custom user admin 改為建基於 Django `UserAdmin`。
- 分開 user add/change form，避免 password hash 被當成普通文字欄位處理。
- 建立 `VocabActionService` 架構，準備集中管理正式 vocab mutation。

### Database 改動

- 無 schema 變更；主要完成 admin/form architecture 同 service preparation。

### 理由

### 學到咩

## 2026-06-20 - Admin user creation and VocabActionService

Commit: `913e765`

### 主要改動

- 完成 admin 專用 user creation form，包括 password confirmation、Django password validation 同 `set_password()`。
- 實作 `VocabActionService`，集中處理 vocab create、update、deactivate 同 restore。
- 建立 request data mapper，將 `VocabRequest` proposed data 轉成 service input。

### Database 改動

- 移除暫時未使用嘅 `Vocab.similar_word`。
- 移除 detail tables 不必要嘅 timestamp fields。
- `Vocab.word_slug` 暫時改成 nullable/blank，等待正式 slug strategy。

### 理由

### 學到咩

## 2026-06-20 - Quiz filtering and kana keyboard design

Status: Design planning

### 主要決定

- Quiz question pool 將按 vocab type、level 同 category 篩選。
- Filter 後再套用 weighted random、recent-question exclusion 同 overdue weight boost。
- 50 音 keyboard 只會用於 quiz 作答；search 同 vocab request 繼續使用一般輸入法。

### Database 改動

- 無；目前屬設計階段。

### 理由

### 學到咩

## 2026-06-21 - Transactional request review workflow

Commit: `b483c51`

### 主要改動

- 將 admin approve/reject 正式接駁到 `VocabActionService`。
- Approve 前驗證最終 proposed data，成功後同步更新 request status 同 reviewer。
- 使用 row locking 同最新 `PENDING` 狀態檢查，防止 double click 或 concurrent review 重複處理。
- Admin 會收到成功、已處理或 validation failure feedback。

### Database 改動

- 移除未使用嘅 `VocabRequest.proposed_similar_word`。
- 將 level database values 統一為 `0` 至 `5`。
- 移除未實作嘅 `REVIEW` request type。
- 修正 `User.last_login` field metadata。

### 技術重點

- `select_for_update()` 會鎖定 request row 直到 transaction 完結；必須配合 `transaction.atomic()` 使用。
- SQLite 對 row-level locking 支援有限，正式使用 PostgreSQL 時先會完整發揮效果。
- Approve/reject 嘅 vocab mutation 同 request status update 放喺同一 transaction，避免兩邊狀態不一致。

### 理由

### 學到咩

## 2026-06-22 - Admin-authenticated CSV vocab import

Commit: `567adc4`

### 主要改動

- 實作 CSV vocab import 核心流程，要求 superuser authentication。
- Import 前驗證必要 headers，逐行將資料交俾 `VocabActionService.create_vocab()`。
- Invalid row 或 database integrity error 會顯示 CSV 行數並跳過；檔案不存在或結構錯誤會停止 command。
- `VocabActionService` 會先執行 `full_clean()`，再保存 vocab 同對應 detail。

### Database 改動

- 無 schema 變更。
- Import 寫入會沿用 `VocabActionService` transaction，確保 `Vocab` 同 detail 一同成功或 rollback。

### 技術重點

- `CommandError` 用於整份 command 無法繼續嘅問題；單一 row error 會寫入 stderr 後繼續下一行。

### 理由

### 學到咩

## 2026-06-23 - UserVocab selection foundation and service naming cleanup

Commit: `595ad0b`

### 主要改動

- 建立 `UserVocabService`，集中處理候選 vocab 查詢同建立 user-vocab relationship。
- 加入 `UserVocabSelectForm` 同 selection view，開始建立 user 從候選 vocab 批量加入個人清單嘅流程。
- 候選查詢會排除 user 已經擁有嘅 vocab，並限制每批最多 50 筆。
- 使用 `get_or_create()` 建立 `UserVocab`，令重複提交唔會建立 duplicate relationship。
- 將 vocab action、request 同 UserVocab service methods 統一由 camelCase 改成 Python 慣用嘅 snake_case。
- `update_vocab()` 保存前加入 `full_clean()`，令 model validation 同 unique constraint 問題可以喺寫入前被發現。
- Admin 將 `VocabRequest.original_vocab` 設為 readonly，避免 review 時改變 request 真正操作嘅目標。
- 移除 login flow 入面冇實際資料改動嘅額外 `user.save()`。

### Database 改動

- 無 schema 變更。
- 沿用 `UserVocab` 現有 `(user, vocab)` unique constraint，配合 `get_or_create()` 保持建立流程 idempotent。

### 技術重點

- 先限制候選 vocab IDs，再用 `id__in` 建立未 sliced QuerySet，避免 `ModelMultipleChoiceField` POST validation 無法再次 filter sliced QuerySet。
- Service method naming 統一使用 snake_case，並同步更新所有 call sites。

### 理由

### 學到咩

## 2026-06-27 - UserVocab activation model and admin review hardening

Status: Work in progress

### 主要改動

- `UserVocab` 加入 `in_use` 狀態，用嚟分開「已加入 user 個人 list」同「目前 quiz 會使用」嘅 vocab。
- `UserVocabListView` 改用專用 search form，支援按 `in_use`、word、kana、level 同 category 篩選 user 個人 vocab。
- 建立新設計方向：新 vocab 可以先建立 `UserVocab(in_use=False)`，之後由 user 自己決定是否啟用。
- `VocabRequest` create / restore / update / delete view 會捕捉 service 拋出嘅 `ValidationError`，並轉成 form non-field error。
- `VocabRequestAdmin` approve / reject POST 時會 early `select_for_update()`，並保留 service-level row lock。
- Reviewed request 會變成 readonly，`save_model()` 會擋住非 pending request 被再次保存。
- `VocabAdmin` 禁止 admin direct add vocab，並將 `type` 設為 readonly，避免繞過 service create flow 或造成 type/detail mismatch。
- 清理 admin 入面舊嘅 commented approve/reject custom URL approach，相關概念改以學習筆記保存。
- 進行一次較全面嘅 code flow review，重新檢查 request、admin review、service、UserVocab 同 import flow，確認自己理解每個主要流程。

### Database 改動

- `UserVocab` 新增 `in_use` boolean field，default 為 `False`。
- 呢個欄位代表 user 是否啟用該 vocab 進入 quiz pool，而唔影響全站 `Vocab` 是否存在。

### 技術重點

- `UserVocab` 由單純 relationship 進一步變成 user 對 vocab 嘅個人 learning state，包括 `in_use`、weight、streak 同答題統計。
- Admin change form custom action 要注意 `response_change()` 係 form save 後先執行；今次用 admin early lock、service self-lock、readonly reviewed state 同 `save_model()` guard 組成多層防線。
- View layer 要捕捉 service-level `ValidationError`，避免 race condition 或 database constraint error 直接穿出 request flow。
- 定期做 full coding review 可以防止 project 快速累積後，出現「功能寫咗但自己已經唔清楚 flow」嘅情況。

### 理由

- `Vocab` 應代表全站共用 vocabulary pool；單一 user 暫時唔想練某個字，唔應該刪除 `Vocab`。
- `UserVocab.in_use=False` 可以保留「已派到 user、但未啟用」嘅狀態，方便之後 EventNotice 通知 user 有新字可處理。
- Quiz question pool 之後只應使用 `in_use=True` 嘅 `UserVocab`，避免未啟用 vocab 突然出題。

### 學到咩

- Django Admin custom action 唔只係加 button，仲要理解 form save lifecycle、transaction boundary、row lock 同 stale page submit。
- `select_for_update()` 應放喺 transaction 入面；admin POST change form 通常有 atomic wrapper，但 service 仍應保留自己嘅 transaction / lock 作最後防線。
- Domain model 可以用現實比喻幫助釐清責任：`Vocab` 似總公司 menu，`UserVocab` 似分店 menu，`in_use` 代表該分店目前是否提供該 item。
- 全面 review 自己寫過嘅 flow，可以幫助重新確認 URL、view、form、service、transaction、error handling 同 data model 之間嘅責任分工。

## 2026-06-28 - Login-time UserVocab sync and in-use bulk update draft

Status: Work in progress

### 主要改動

- `UserLoginView.form_valid()` 於成功 login 後呼叫 `UserVocabService.sync_new_vocab()`，自動為 user 建立尚未擁有 vocab 嘅 `UserVocab` records。
- `UserVocabService.sync_new_vocab()` 會重用候選查詢同 `get_or_create()` 建立 relationship，配合 `UserVocab.in_use=False` default。
- `UserVocabListView` 開始加入 POST bulk update flow，使用 `selectable_ids` 表示目前畫面顯示項目，`selected_ids` 表示 user 勾選為 in-use 嘅項目。
- `UserVocabInUseUpdateForm` 使用 `ModelMultipleChoiceField` 驗證 submitted ids 必須屬於目前 user 可操作嘅 `UserVocab` queryset。
- 舊 `UserVocabSelectVocabView` / `UserVocabSelectForm` flow 暫時不再作為主要加字入口，但保留為之後可重用嘅批量選擇 pattern。

### Database 改動

- 無新增 schema 變更；沿用 `UserVocab.in_use` 同 `(user, vocab)` unique constraint。

### 技術重點

- Checkbox UI 不能單靠位置對應資料，因為未勾選嘅 checkbox 不會 submit；需要用 id 明確表示「畫面顯示過」同「user 勾選咗」嘅項目。
- Bulk update 應只更新狀態真正改變嘅 rows，避免每次 submit 都刷新所有 visible rows 嘅 `update_at`。
- `request.get_full_path()` 可以保留 path + query string，方便 POST 後 redirect 回原本 filter / pagination 狀態。
- `.update()` 不會觸發 `auto_now`，如使用 bulk update 需要手動設定 `update_at`。

### 理由

- Login-time sync 令 user 每次登入後都可以收到最新 vocab relationship，配合 `in_use=False` 保持 quiz pool 由 user 自己控制。
- `selectable_ids` / `selected_ids` 設計可以同 pagination、filter 一起使用，只更新目前畫面顯示嘅項目。

### 學到咩

- 一個頁面可以同時有 GET search form 同 POST bulk update form；ListView 亦可以加 `post()` 處理批量狀態更新。
- `ModelMultipleChoiceField` 除咗 render checkbox，亦可以作為 submitted ids 嘅 validation layer。
- 舊 flow 即使暫時不用，只要整理成 learning note，就可以保留成之後 project 可重用嘅 pattern。

## 2026-06-29 - Dictionary normal flow stabilization and pre-test checkpoint

Commit: `5cdf658`

Status: Ready for manual flow testing

### 主要改動

- Register flow 亦加入 `UserVocabService.sync_new_vocab()`，令新 user 建立後即時獲得現有 vocab 嘅 `UserVocab` records。
- `UserVocabListView` 同 template 已形成較完整嘅 in-use management flow：user 可以透過 list checkbox 批量啟用或停用個人 vocab。
- `UserVocab` 新字派發設計由手動選字，調整成 login / register sync 後預設加入個人 list，再由 user 決定是否 `in_use=True`。
- `import_vocab` management command 加入 import summary，會記錄成功筆數、失敗筆數、failed row number 同錯誤原因。
- 開始為之後 logging / audit trail 預留資料形態，import command 已整理出可重用嘅 `success_count`、`failed_rows`、`row_number` 同 `error_message`。
- Dictionary 相關正常流程已接近可實際試用，下一步會以真實操作方式跑一次完整 flow，確認行為是否符合預期。

### Database 改動

- 無新增 schema 變更。
- 目前沿用 `Vocab`、`VocabRequest`、`UserVocab(in_use)`、detail tables 同 existing unique constraints 支撐 dictionary normal flow。

### 技術重點

- Register 後 sync 應使用 `self.object`，因為 `CreateView` save 完 user 後不代表 request 已經自動 login。
- Import command 嘅 row-level error handling 可以先整理成 structured data，再決定輸出到 terminal、log file、database import history 或 event system。
- Dictionary flow 由單純 CRUD 逐步變成完整 workflow：user request、admin review、vocab action、UserVocab 派發、user activation 同 import support。
- 實際 manual testing 會成為下一個重要 checkpoint，用嚟驗證目前設計唔只係 code path 成立，而係使用起來符合原本想像。

### 理由

- Dictionary module 已經包含多個互相連動嘅核心流程，繼續加新功能前需要先實際跑一次，確認正常使用場景、error handling 同 user/admin 分工都合理。
- 先完成可運作嘅 normal flow，再進入 quiz、event notification、logging 等後續功能，可以減少後面建喺不穩基礎上嘅風險。

### 學到咩

- 一個看似簡單嘅 dictionary，其實一旦加入 user-specific state、admin review、import、concurrency 同 data integrity，就會變成完整 domain workflow。
- 開發到一個階段後，manual flow testing 同 code review 一樣重要；前者驗證「用起來係咪啱」，後者驗證「寫法同責任分工係咪清楚」。
- 文檔唔只係記錄已完成事項，亦可以幫自己標示 project 由「功能建設」進入「實際驗證」嘅節點。

## 2026-07-01 - Event notification data model foundation

Commit: `f51693a`

Status: Foundation completed; service flow pending

### 主要改動

- 建立 event notification system 嘅初步 data model，加入 `Event` 同 `UserEvent`。
- `Event` 保存 event type、title 同 message，準備用作 vocab request result、new vocab、system update 等通知。
- `UserEvent` 保存每個 user 對每個 event 嘅 read status，包括 `is_read` 同 `read_at`。
- 將 `Event` 註冊到 Django admin，方便之後檢查同管理 event data。
- 建立 `core.service.event.EventService` 初稿，暫時保留 message generation、create event、assign event to user 等 service entry points。
- 將 `UserVocab` reverse related name 由 singular `user_vocab` 整理成 plural `user_vocabs`，令 reverse relation 語意更自然。

### Database 改動

- 新增 `Event` table。
- 新增 `UserEvent` table，作為 `Event` 同 user 之間嘅 through relationship。
- `UserEvent` 加入 `(user, event)` unique constraint，防止同一 user 對同一 event 建立重複 read-status record。
- `Event.message` 使用 `TextField`，避免之後 approve/reject result 或 import summary message 太長。
- `UserVocab.user` 同 `UserVocab.vocab` 嘅 `related_name` 改成 `user_vocabs`；呢個係 Django model option 層面嘅命名整理，方便日後 query。

### 技術重點

- Event content 同 user read state 分開保存，可以避免同一個 event 因為派俾多個 users 而重複複製完整 message。
- Through model 適合保存 relationship 自己嘅狀態，例如 `is_read`、`read_at`，之後亦可以擴展 dismiss / handled state。
- `related_name` 應該反映 reverse side 會回傳多筆 records；plural naming 會令 `user.user_vocabs.all()` / `vocab.user_vocabs.all()` 更直覺。
- Event service 暫時只建立 interface，真正 create / assign / mark-read flow 之後再按 vocab request result 同 login notification 需要實作。

### 理由

- Vocab request approve / reject、CSV import result、new vocab notification 等功能都需要一個統一通知基礎，而唔應該各自散落喺不同 app 入面。
- 先建立 data model foundation，可以之後逐步將 admin review result、UserVocab sync notice 同 user message handling 接入同一套 event system。

### 學到咩

- Notification system 最少可以拆成「event 本體」同「user 對 event 嘅狀態」兩層，唔需要一開始就將所有通知複製成 per-user message。
- Naming cleanup 雖然唔改 database 資料，但會影響 ORM query 可讀性；趁 project 未太大時處理成本最低。

## 2026-07-02 - Kanji CSV resources and dictionary admin hardening

Commit: `9a746a1`

Status: Dictionary admin controls tightened; import resources prepared

### 主要改動

- 加入 kanji vocab CSV resource files，準備之後用 `import_vocab` command 做實際 import 測試。
- 將 dictionary admin 嘅 direct add / delete 操作進一步收緊，避免 admin 繞過既有 service flow 直接建立或刪除核心資料。
- `VocabAdmin` 禁止 direct add / delete，並將 `created_by`、`approved_by` 設為 readonly。
- `VocabAdmin` 加入 level、type、active status list filters，令 admin 檢查 vocab data 時更易篩選。
- `UserVocabAdmin` 禁止 direct add / delete，並將 user / vocab relationship 同 quiz stats 設為 readonly。
- `VocabRequestAdmin` 禁止 direct add / delete，保持 request lifecycle 由 user submission 同 approve / reject workflow 控制。
- 改善 `Vocab.__str__()` 顯示格式，令 admin、debug 同 import review 時更易辨認 word / kana。

### Database 改動

- 無 schema 變更。
- 新增 `resource/kanji*.csv` files 作為之後 import / test data source。
- Admin control changes 屬於 Django admin behavior，不影響現有 table structure。

### 技術重點

- 當 project 已經有 service layer 管理 create / update / delete 時，admin direct mutation 要收緊，否則好容易繞過 validation、transaction、detail model creation 或 audit flow。
- Admin readonly fields 可以保護 ownership / approval metadata，避免後台手動修改破壞資料來源。
- Admin list filters 係實際 manual review 好重要嘅工具，尤其係 vocab data 逐漸變多後，需要按 level、type、active status 快速排查。
- CSV resource files 令 import command 可以進入較接近真實資料嘅測試階段，而唔只係用 placeholder CSV 驗證 reader 能否讀取。

### 理由

- Dictionary normal flow 即將進入實際使用測試，admin 後台需要先收緊可變更範圍，避免測試資料期間出現繞過正式 workflow 嘅資料。
- Kanji CSV resources 會作為 import command、vocab validation、admin review 同 UserVocab sync flow 嘅實際測試材料。

### 學到咩

- Admin 介面唔只係方便 data entry；喺有 workflow 嘅系統入面，admin 亦需要配合 domain rules 限制邊啲操作可以做、邊啲只可以睇。
- 準備 realistic resource data 係 manual testing 前嘅重要一步，可以更早暴露 import、filter、admin display 同 user-facing flow 嘅問題。

## 2026-07-02 - Ajax pagination partial for vocab list

Commit: `e1e56df`

Status: Vocab list Ajax pagination tested; UserVocab list reuse pending

### 主要改動

- 將 vocab list table 同 pagination 拆成 `vocab_list_partial.html`，由 main template include。
- `VocabListView.render_to_response()` 可根據 `X-Requested-With` header 回傳 partial HTML，供 Ajax pagination 使用。
- `vocab_list.html` 加入 client-side fetch handling，click pagination link 時只更新 vocab list 區域。
- Pagination link 會保留現有 GET search filters，避免 search 後轉頁時失去 filter 條件。
- 保留普通 `<a href>` pagination link，即使 JavaScript 不執行亦可以完整 reload page。
- 新增 `user_vocab_list_partial.html` placeholder，準備之後將同一 pattern 套用到 UserVocab list。
- `EventService` 補上 read-state handling 相關 placeholder methods，為之後 notification read flow 留出 service entry points。

### Database 改動

- 無 schema 變更。
- 今次主要係 template 分拆、view response 分流同 frontend interaction。

### 技術重點

- Partial template 可以令同一份 list markup 同時服務 initial page render 同 Ajax response，減少重複 HTML。
- Ajax pagination 嘅核心唔係另一套 URL，而係 fetch 原本 pagination link，並用 `X-Requested-With` 令 view 回傳 partial。
- Search state 由 GET query string 保存；pagination link 要將原有 query string 去除舊 `page` 後，再加上新 page number。
- 保留 `<a href>` fallback 可以令功能不完全依賴 JavaScript，亦方便 debug。

### 理由

- Vocab list 之後資料量會增加，Ajax partial pagination 可以令列表操作感覺更順，同時保留 server-rendered template 架構。
- 先喺較簡單嘅 VocabListView 驗證 pattern，再考慮套用到 UserVocabListView，風險較低。

### 學到咩

- Ajax partial update 同傳統 server-side pagination 可以共存；只要 URL、query string 同 fallback link 設計好，就唔需要一開始轉成完整 frontend app。
- Query string 係 search/filter state 嘅來源，pagination、Ajax 同 normal reload 都應該圍繞同一份 state 運作。

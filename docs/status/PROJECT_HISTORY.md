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

## 2026-07-06 - UserVocab Ajax pagination and dictionary full-flow verification

Commit: `e61baea`

Status: Dictionary app normal flow manually verified

### 主要改動

- 將 `UserVocabListView` 嘅 table、bulk update form 同 pagination 拆成 `user_vocab_list_partial.html`。
- `UserVocabListView.render_to_response()` 可根據 `X-Requested-With` header 回傳 partial HTML，完成 UserVocab list Ajax pagination flow。
- `UserVocabListView` pagination 已保留 GET search filters，避免 search / filter 後換頁失去條件。
- UserVocab list partial replace 後會重新初始化 checkbox select-all handling，確保 Ajax 換頁後 checkbox 互動仍然生效。
- 將 `VocabDetailView` 改用 Django `DetailView`，令 object lookup flow 更貼近 CBV standard pattern。
- Vocab list rows 加入 vocab detail link，vocab detail page 加入 update / delete action links。
- 補上 delete request form rendering，完成 delete request manual flow。
- `UserVocabAdmin` list 顯示加入 `in_use` 狀態，方便 admin 檢查 user vocab 是否啟用。
- 將 `LEARNING_QUESTIONS.md` rename 成 `LEARNING_POINTS.md`，並加入目錄同 Ajax partial event binding 筆記。
- 完成一次 dictionary app full manual test，覆蓋 vocab request create / restore / update / delete、admin approve / reject、vocab list、UserVocab list、Ajax pagination、select-all 更新 `in_use` 等正常流程。

### Database 改動

- 無 schema 變更。
- 今次主要係 view/template interaction、admin display、document rename 同 manual verification。

### 技術重點

- Ajax partial replace 會替換 DOM，因此 partial 內 checkbox listener 需要在更新後重新初始化，或者之後改用 event delegation。
- 用 Network tab 檢查 request `Type: fetch`，並確認 response 只包含 partial HTML，可以驗證局部更新確實成功。
- Django `DetailView` 適合處理標準 single-object detail page，可減少手動 `get_object_or_404()` boilerplate。
- Manual full-flow testing 可以補足目前缺少 automated tests 時嘅信心，但 concurrency / permission boundary 等仍然需要日後用 tests 或更嚴格 review 補強。

### 理由

- Dictionary app 已經接近 feature-complete，做 full manual test 可以確認主要 user/admin flow 真正按預期運作，而唔只係 code path 理論成立。
- UserVocab list 需要同 vocab list 一樣支援 search、pagination 同局部更新，因為之後 quiz pool 會依賴 user 是否將 vocab 設為 `in_use=True`。

### 學到咩

- DOM replacement 後事件綁定係 Ajax partial UI 必須處理嘅問題；簡單做法係 replace 後重新 call setup function，長期可研究 event delegation。
- 一個 app 到達「功能完整」階段後，測試重點會由單點功能轉成完整 workflow：user request、admin review、正式 vocab 變更、user vocab sync / activation。
- Network tab 係確認 Ajax 是否真係局部更新嘅最直接工具，`fetch` / `document` type 同 response content 都可以用嚟判斷。

## 2026-07-10 - Category model-backed M2M migration

Commit: `bf579ac`

Status: Dictionary category system migrated from single field to 1-3 categories

### 主要改動

- 將 dictionary category system 由 hard-coded single category 改成 database-backed `Category` model。
- `Vocab` 改用 `categories` ManyToMany relationship，支援一個 vocab 擁有最多三個 categories。
- `VocabRequest` 改用 `proposed_categories` ManyToMany relationship，令 create / update / restore request 可以保存 proposed categories snapshot。
- 移除 legacy single category flow，包括 `Vocab.category`、`VocabRequest.proposed_category` 同 `VocabCategory` choices enum。
- `BaseVocabRequestForm` 加入 `ModelMultipleChoiceField`，並用 `clean_categories()` 限制最多三個 categories。
- `VocabUpdateRequestView.get_initial()` 會帶入現有 `vocab.categories.all()`，令 update form 可 tick 返原本 categories。
- `VocabRequestService` create / update / restore request flow 已改為保存 `proposed_categories`，approve create / update 時再交由 `VocabActionService` 同步到正式 vocab。
- `VocabActionService.create_vocab()` / `update_vocab()` 已改用 `vocab.categories.set(...)` 同步 M2M relationship。
- `VocabSearchForm` / `UserVocabSearchForm` category filter 改用 `ModelChoiceField`，並支援 vocab list / user vocab list 以 M2M category 篩選。
- `import_vocab` command 改用 `category1`、`category2`、`category3` CSV headers，並檢查 category 是否存在於 `Category` table。
- 新增 `setup_categories` command 同 `resource/categories.csv`，方便重建 development database 後快速 seed category master data。
- `CategoryAdmin`、`VocabAdmin`、`VocabRequestAdmin` 已加入 categories 管理與 checkbox display。
- `VocabRequestAdmin` 針對 reviewed request 使用 `get_form()` disable `proposed_categories`，避免 reviewed request 嘅 M2M field 仍可修改。
- 撰寫 `doc/modification/category_improvement.md`，記錄今次 single category -> M2M categories migration 嘅完整流程同設計原因。

### Database 改動

- 新增 `Category` table。
- 新增 `Vocab.categories` ManyToMany relationship。
- 新增 `VocabRequest.proposed_categories` ManyToMany relationship。
- 移除 `Vocab.category` column。
- 移除 `VocabRequest.proposed_category` column。
- 新增並套用 migration：
  - `0020_categories_prepare.py`
  - `0021_category_change.py`
  - `0022_remove_vocab_category_and_more.py`
- 已執行 `manage.py migrate`，`0022_remove_vocab_category_and_more` 套用成功。

### 技術重點

- `ModelMultipleChoiceField` 負責喺 form 層收多個 model objects；真正同步 M2M relationship 要喺 model instance save 後使用 `.set(...)`。
- ManyToMany relationship 需要 main object 已有 primary key，所以 `VocabActionService.create_vocab()` 要先 `vocab.save()`，再 `vocab.categories.set(...)`。
- `ModelChoiceField` 適合用 database records 做 filter choices；form validate 後取得嘅係 `Category` instance，而唔係舊 choices string。
- M2M filter 需要用 relationship lookup，例如 `Vocab.objects.filter(categories=category)` 同 `UserVocab.objects.filter(vocab__categories=category)`。
- `readonly_fields` 未必完整處理 admin M2M field，所以 reviewed request 入面嘅 `proposed_categories` 需要透過 `get_form()` / `form.base_fields["proposed_categories"].disabled = True` 額外保護。
- Legacy field 移除前要確定所有 form / view / service / admin / import command 都已改用新 M2M source，否則 schema migration 後容易出現 runtime error。

### 理由

- 單一 category 無法準確表達 vocab 可能同時屬於多個使用場景，限制之後 search、quiz pool selection 同 data organization。
- Database-backed `Category` 比 hard-coded choices 更易維護，之後可以透過 seed command / admin 調整 display 或新增 category。
- 將 request flow 同正式 vocab flow 一起改成 M2M，可以保持 user submission、admin review、approve action 同 import command 使用一致資料模型。
- 移除 legacy single category field 可以避免同一份資料有兩個 source of truth，減少日後 category 不一致問題。

### 學到咩

- Schema refactor 唔只係改 model；要沿住整條資料流檢查 form、view、service、admin、command、migration 同 manual test。
- M2M data 同普通 field lifecycle 唔同，尤其係 create 時必須先 save main object，再處理 relationship table。
- Admin form lifecycle 有好多細節，`get_form()`、`base_fields`、`readonly_fields`、`save_model()` 係唔同層次嘅保護。
- 將大型改動寫成 modification report 有助整理設計原因、實作步驟同之後維護注意事項，亦方便將來 review 自己嘅架構決策。

## 2026-07-11 - Vocab request event notification wiring

Commit: `0d8b401`

Status: Vocab request flow connected to initial event notification service

### 主要改動

- 完善 `EventService` 基本 helper，包括 create event、assign event to user/users、get unread events 同 mark as read。
- `EventService.create_event()` 改為每次建立新 event record，避免一般通知被 `get_or_create()` 重用成舊 event。
- `EventService.assign_event_to_user()` 改用 `UserEvent.objects.get_or_create()`，避免同一 event 重複 assign 同一 user 時撞 unique constraint。
- `EventService.get_unread_events()` 加入 `select_related("event")`，減少之後 notification template 顯示 event content 時嘅 query。
- `VocabRequestService` 新增 `create_event_for_admin()` helper，統一建立 staff-facing `NEW_VOCAB_REQUEST` notification。
- CREATE / UPDATE / RESTORE / DELETE vocab request 建立成功後，會通知 `is_staff=True` users 有新 request 需要 review。
- Staff notification 使用 `transaction.on_commit()`，確保 request 成功 commit 後先建立 event。
- Approve / reject request 後會建立 `VOCAB_REQUEST_RESULT` event，通知 request owner review result。
- Approve request 後會額外建立 `VOCAB` event，通知 users vocab data 有變更。
- 清理 `vocab_request.py` 入面 event 相關無用 import，只保留實際需要嘅 `EventType`。
- 將 `transaction.on_commit()`、callback 帶參數方式、`lambda` / inner function / `functools.partial` 寫入 `LEARNING_POINTS.md`。

### Database 改動

- 無新增 schema 變更。
- `EventType` 目前已包含 `NEW_VOCAB_REQUEST`，model / migration 狀態已通過 `makemigrations --check --dry-run`。
- 今次主要係 service flow wiring，同現有 `Event` / `UserEvent` table 互動。

### 技術重點

- User submit vocab request 時，request 本身係核心資料；staff notification event 係輔助通知。
- 因此 request creation flow 使用 `transaction.on_commit()` 建立 notification，避免 event 建立失敗令 user request rollback。
- `transaction.on_commit()` 只會喺 transaction 成功 commit 後執行 callback；如果 request 建立失敗 rollback，就唔會建立假通知。
- Callback 要帶參數時，可以用 inner function 包住 helper call，令 `on_commit()` 收到一個無參數 callback。
- Approve / reject flow 暫時將 result event 放喺 review transaction 入面；如果 event 建立失敗，admin 可以即時重新 approve / reject。
- 呢個設計係按失敗成本區分 transaction boundary：user submit failure 成本較高，admin review failure 可重試成本較低。

### 理由

- Event notification system 需要先接入現有 vocab request workflow，先可以進一步做 navbar unread count、notification page 同 mark as read。
- Staff 需要知道有新 vocab request 需要 review，但呢個通知唔應該影響 user 成功提交 request。
- Request owner 需要知道 approve / reject result，所以 review 完成後要建立 per-user result event。
- 先用 service helper 串起 core event flow，可以避免 view/admin layer 直接操作 `Event` / `UserEvent`，之後擴展 notification UI 時會更集中。

### 學到咩

- `transaction.on_commit()` 適合處理「主資料成功後先做」嘅 side effect，例如 notification、email、cache update。
- Event 是否放入 transaction 入面，唔係固定答案，而係要睇 event failure 應否令主流程 rollback。
- `get_or_create()` 適合 idempotent relationship，例如 `UserEvent` assignment；一般通知 event 本體通常應該用 `create()`，避免不同事件被誤判成同一筆通知。
- 抽 helper 後要留意 keyword-only arguments 是否同 callback 傳入嘅 keyword 一致，否則 syntax check 未必發現 runtime `TypeError`。

## 2026-07-14 - Vocab sync summary event foundation

Commit: `14c04a6`

Status: Initial vocab sync summary event flow added; login/home integration and UI handling are still pending

### 主要改動

- `UserProfile` 新增 `last_vocab_sync_at`，用作記錄每個 user 上次同步 vocab changes 嘅時間點。
- `EventService.gen_vocab_sync_event()` 加入初版 vocab sync summary flow，根據 `last_vocab_sync_at` 搵出上次同步後有變化嘅 vocab。
- CREATE request 獨立計算；只要 sync window 入面有 approved CREATE request，就會當作新字通知。
- UPDATE / RESTORE / DELETE request 使用同一個 non-CREATE 分支，只取 sync window 入面最新一次 approved request 作為該 vocab 嘅變更 summary。
- 如果 vocab 有更新但搵唔到對應 approved request，暫時當作 admin / import 直接建立嘅 vocab，歸類為 new vocab fallback。
- 產生 new / updated / restored / deleted vocab summary event，並 assign 俾該 user。
- 第一次 sync 目前只設定 baseline，不會一次過通知所有歷史 vocab。
- 將 QuerySet subset ordering 相關理解寫入 `LEARNING_POINTS.md`，並同步更新 `TODO.md` 入面 event system 未完成項目。

### Database 改動

- 新增 `UserProfile.last_vocab_sync_at` 欄位。
- 新增 migration `accounts/migrations/0005_add_sync_field.py`。
- `Event` / `UserEvent` schema 無改動；今次係利用現有 event table 建立 vocab summary notification。

### 技術重點

- `Vocab.objects.filter(update_at__gt=last_sync)` 用嚟搵需要檢查嘅 vocab。
- 內層 `VocabRequest` query 仍然需要自己加 `update_at__gt=last_sync`，因為外層 vocab query 唔會自動限制入面另一個 QuerySet。
- CREATE 同 non-CREATE 分開處理，避免「新字」通知被後續 update / delete 覆蓋。
- Non-CREATE request 只取最新一次變更，令 user 收到嘅係 summary，而唔係每一次歷史操作。
- 使用 `last_vocab_sync_at` 而唔係 `last_login`，可以將「登入時間」同「vocab notification sync 時間」分開處理。

### 理由

- 避免每次 approve vocab 時即時為所有 user 建立大量 event。
- 將 notification 由 per-action event 改成 per-user sync summary，可以減少 user 收到一堆重複 vocab notification。
- Vocab request owner 嘅 approve / reject result event 仍然保留；一般 user 嘅 vocab change notification 則改為 summary flow。
- 第一次 sync 先建立 baseline，可以避免舊資料一次過湧入通知中心。

### 學到咩

- QuerySet 分開後，每個 QuerySet 都有自己嘅 filter / order_by 範圍；外層 query 條件唔會自動傳入內層 query。
- 做時間區間 summary 時，需要一個 domain-specific sync timestamp，而唔一定應該借用 login timestamp。
- Event system 要分清楚 audit trail 同 user-facing notification；user 未必需要知道每一次內部操作，只需要知道對佢有用嘅 summary。

## 2026-07-19 - Event and admin management polish

Commit: `f616e5c`

Status: Event notification and admin management flows are more usable; documentation format started to settle

### 主要改動

- User admin detail page 改用 summary field 顯示 `UserVocab` count，並提供 filtered `UserVocabAdmin` link，取代大量 inline rows。
- User admin detail page 加入 `last_vocab_sync_at`、`date_joined`、`last_login` readonly display，方便 review user sync 狀態。
- `UserVocab.in_use` default 改為 `True`，新 sync 入 user list 嘅 vocab 會預設進入可用範圍，由 user 自己再停用。
- `UserEventListView` 加入 no unread event template，避免無未讀 event 時仍顯示空 list。
- `UserEventDetailView` 已限制只能查看目前 user 自己嘅 event。
- `EventAdmin` / `UserVocabAdmin` 管理畫面整理過，令 event 同 user vocab data 更易檢查。
- `Event` 同 `UserVocab` 補上更易讀嘅 `__str__()`。
- Admin datetime format 加入 project-level format module，統一顯示到年月日時分秒。
- `TODO.md` 開始重整成較固定嘅 tracking format，並新增 `PROJECT_DOC_FORMAT.md` 記錄 TODO / learning points / project history 嘅分工。

### Database 改動

- 新增 migration `dictionary/migrations/0023_in_use_default_true.py`。
- `UserVocab.in_use` default 由 `False` 改為 `True`。
- 無新增 event schema；今次主要係 admin display、view flow 同 default behavior 調整。

### 技術重點

- 大量 related records 唔適合長期用 admin inline 顯示；改用 count + filtered changelist link，admin page 會更快、更清楚。
- `UserVocab.in_use=True` 更適合大量 vocab sync flow，避免新 user 或久未 login user 要手動啟用大量新 vocab。
- Event list / detail 已開始形成基本 notification UI：navbar count、unread list、detail page、mark as read。
- Django datetime global format 需要 `FORMAT_MODULE_PATH` + locale folder，例如 `core/formats/en_US/formats.py`。

### 理由

- Dictionary app 目前已進入整體 logic review 階段，UI 只需要能顯示必要資料，避免過早投入 polish。
- User admin inline 喺 user vocab 數量增加時會變慢，因此改用 summary/link pattern。
- 新 vocab 預設 in use 可以減少 user 初次使用成本，之後再由 quiz filter 或 user 自己停用控制練習範圍。
- Documentation format 開始固定，可以避免 TODO、learning notes 同 history 互相混淆。

### 學到咩

- Admin 頁面要按資料量選擇呈現方式；inline 適合少量 child rows，大量資料應交俾 filtered changelist。
- Default value 係 product behavior decision，不只係 model 設定。
- Event notification flow 可以先完成資料同基本可視化，再逐步 polish UI。
- Project 文件要分工清楚：`TODO.md` 追狀態，`LEARNING_POINTS.md` 放學習理解，`PROJECT_HISTORY.md` 記重要階段同決策。

## 2026-07-20 - Initial quiz question flow foundation

Commit: `615dc9f`

Status: Quiz app has its first working foundation; flow is still rough and will need refinement

### 主要改動

- 建立 quiz setting form，讓 user 選擇今次 quiz 要使用嘅 vocab type、level 同 categories。
- 建立 `QuizService.create_question_pool()` 初稿，由目前 user 嘅 `UserVocab` 產生 question pool。
- Question pool 已開始套用 `in_use=True`、vocab type、level、categories filter。
- 建立 `QuizService.pick_random_vocab()` 初稿，使用 total weight、cumulative weight 同 `bisect_left` 抽出下一題。
- 建立 quiz view / URL 初稿，形成 setting -> question -> answer -> result 嘅基本 flow。
- 建立 quiz templates 初稿，包括 home、setting、question、result 同 kana keyboard partial。
- Answer checking 初稿已開始更新 `correct_count`、`incorrect_count`、`streak` 同 `last_quiz_at`。

### Database 改動

- `UserVocab.weight` 加入 `MinValueValidator(1)`，避免正常 form / admin validation 接受 0 或負數。
- 新增 migration `dictionary/migrations/0024_weight_add_min.py`。
- 無新增 quiz-specific table；quiz answer history / result tracking 仍未正式建立。

### 技術重點

- Weighted random selection 暫時選擇自行計算 total weight，再建立 cumulative weights，最後用 `bisect_left` 找出命中項目。
- Quiz question pool 使用 `UserVocab` 而唔係直接使用全站 `Vocab`，因為出題範圍需要尊重每個 user 自己嘅 `in_use` 設定同 quiz stats。
- M2M categories filter 需要留意重複 row，所以 category filter 後使用 `distinct()`。
- `QuizView` 取題目時用 `get_object_or_404(UserVocab, pk=..., user=request.user)`，避免 user 改 URL 操作其他 user 嘅 vocab。

### 理由

- Quiz app 係 project 核心功能之一，今日先建立可逐步接駁嘅骨架，之後再慢慢完善 result、history、weight update 同 UI。
- 先完成 setting -> question -> answer -> result 嘅大方向，可以更容易測試整個 quiz flow 是否符合預期。
- Question selection 先用可理解、可 debug 嘅 weighted random 寫法，方便之後按 learning behavior 調整 weight 規則。

### 學到咩

- FormView 做 dynamic redirect 時，固定 `success_url` 未必適合；需要帶 URL kwargs 時，直接喺 `form_valid()` 入面 `redirect(...)` 會更清楚。
- CBV 入面 URL parameter 會放喺 `self.kwargs`，例如 `self.kwargs["user_vocab_id"]`。
- Service function return object 定 pk 要事先諗清楚，因為會影響 view redirect、template display 同後續 result flow。
- 初版 feature 可以先粗略接通，再用 TODO tracking 記低 no question fallback、result passing、answer history 同 weight update 等後續要執嘅位。

## 2026-07-23 - Quiz partial endpoint flow restructure

Commit: `3beeeb3`

Status: Quiz play flow restructured around action endpoints and partial rendering; UI templates and full Ajax behavior still need completion

### 主要改動

- Quiz flow 由 question/result URL redirect 方向，改成 full page shell + partial endpoints。
- `QuizPlayView` 負責 quiz play shell 同第一題 context。
- 新增 `QuizSubmitAnswerView`，負責接收 answer submit、執行 answer checking，並回傳 `quiz_result_partial.html`。
- `QuizNextView` 負責處理 result partial 入面嘅 Next action，抽下一題後回傳 `quiz_question_partial.html`。
- 新增 `QuizSettingRequiredMixin`，喺 quiz play / submit / next actions 前檢查 session 是否已有 quiz settings。
- `QuizForm` 加入 hidden `user_vocab_id` 同 `tips_count`，令 answer submit 可以知道目前題目同 tips 使用狀態。
- `QuizNextForm` 建立成空 form，避免 Next action 被 answer fields validation 阻塞。
- Recent-question skip 加入簡單 fallback：question pool 少於或等於 10 題時暫時不 skip，避免直接無題目。

### Database 改動

- `UserVocab` 新增 `last_answer`，準備保存 user 最近一次提交嘅答案。
- 新增 migration `dictionary/migrations/0025_add_last_answer.py`。
- `UserVocabAdmin` 顯示 `last_answer`，方便測試 quiz answer flow。

### 技術重點

- Ajax quiz flow 要分清楚 action endpoint 同 UI partial：partial file 不一定需要同名 view。
- Submit answer action 應直接處理 answer checking / stats update，然後 render result partial。
- Next action 應只負責抽下一題，然後 render question partial。
- `render_to_response()` 適合 list page full/partial fallback；quiz 呢類 action-based endpoint 更適合喺 `form_valid()` / `post()` 直接 `render(...)`。
- `dispatch()` 適合作為多個 quiz views 共用嘅 session gatekeeper。

### 理由

- Quiz 需要在同一頁內反覆切換 question / result state，獨立 full page result view 會令 flow 變得冗長。
- 將 answer submit 同 next question 拆成兩個 action endpoints，可以避免第一題同後續題目使用不同處理路徑。
- Hidden `user_vocab_id` 令每次 answer submit 都能明確對應到當前題目，而唔只依賴 session 最新狀態。

### 學到咩

- View 應該按 user action 分工，而 partial 只代表畫面狀態。
- `get_context_data()` 應主要負責準備 render data，不適合放 answer checking 呢類會修改 database 嘅 side effect。
- `FormView` 可以用喺 action endpoint，但要確保 form class 同該 action 真正需要提交嘅 fields 對應。
- Session 適合保存 quiz settings；每題 submit 對應邊個 vocab 則更適合用 hidden field 跟住 form 一齊提交。

## 2026-07-25 - Quiz fallback handling and active vocab guard

Commit: `7cc32df`

Status: Quiz question selection is more defensive; fallback behavior and minimum active vocab checks are now defined

### 主要改動

- `QuizSettingView` 加入 minimum active vocab guard，user 啟用 vocab 數量不足時會 redirect 去 user vocab list，避免進入無題可抽嘅 quiz flow。
- 新增 `QUIZ_MIN_IN_USE_VOCAB_COUNT` project setting，集中管理開始 quiz 前需要嘅最低 active vocab 數量。
- `QuizService.create_question_pool()` 加入 fallback behavior：當 user filter 條件抽唔到題時，會 fallback 返 user 嘅 full active vocab pool。
- Quiz session 開始保存每題嘅 `fallback_used` flag，令 result partial 可以知道今次題目是否使用 fallback pool。
- `QuizPlayView` / `QuizNextView` 已處理 no-question case，避免 random picker 收到空 pool 後直接爆錯。
- Recent-question skip 改成先搵出最近 quiz 過嘅 10 個 `UserVocab` id，再由原本 pool exclude，保留 `last_quiz_at=None` 嘅新 vocab。
- Answer checking 會保存 `last_answer`，方便 result partial 顯示 user 上一次提交嘅答案。
- Base template 加入 messages display block，讓 quiz guard / fallback warning 可以顯示俾 user。

### Database 改動

- 無新增 schema migration。
- 今次主要係 quiz service、view guard、session state 同 template message display 調整。

### 技術重點

- No-question handling 應盡量喺進入 quiz flow 前做第一道檢查，但 picker 仍要保留 defensive handling，避免 direct request 或 edge case 令空 queryset 流入 random selection。
- Filtered quiz pool 為空時，fallback 到 full active pool 可以令 user 繼續練習，同時用 `fallback_used` 保留「今次已偏離原本 filter」嘅狀態。
- Recent skip 不應直接依賴 `order_by("-last_quiz_at")[10:]`，因為 `NULL` datetime 排序容易令人誤判；抽最近 id 再 exclude 會更清楚。
- `last_answer` 屬於 quiz result display state，可以直接保存喺 `UserVocab`，方便目前階段快速顯示答題結果。

### 理由

- Quiz flow 開始進入實際可測階段，需要先處理「無足夠 vocab」、「filter 無結果」、「最近題目重複」呢類正常使用中會遇到嘅狀況。
- 先用簡單 fallback 同 warning message 保持 flow 可用，之後再視乎 UX 需要決定是否禁止 next、要求 user 改 filter，或提供更清楚嘅 result state。
- Recent-question skip 目前只需要避免短時間重複出現同一批 vocab，暫時未需要建立完整 question history model。

### 學到咩

- Guard 可以分層：setting page 做正常入口檢查，service / picker 再處理 defensive edge cases。
- QuerySet 可以先用一段 query 取得排除名單，再用原本 query exclude，避免因為中途 filter 而不小心縮窄最終 pool。
- `last_quiz_at=None` 呢類未發生過嘅狀態要特別考慮，唔可以假設 database 排序一定符合直覺。
- Feature flow 接近可用時，錯誤處理同 fallback path 會開始變得同 happy path 一樣重要。

## 2026-07-28 - Ajax quiz play interface and kana input panel

Commit: `41db40d`

Status: First working Ajax quiz play interface with custom kana input; result UI and other answer types still need refinement

### 主要改動

- 建立 `quiz_play.html` 作為 quiz play shell，將 main question/result area 同 input panel area 分成兩個可獨立更新嘅 containers。
- Quiz answer submit / next question flow 改成回傳 JSON，分別提供 `main_html` 同 `input_panel_html`，由前端局部替換對應區域。
- 建立 `quiz_input_panel_partial.html`，按題目 type render hiragana keyboard、katakana keyboard 或 multiple choice panel placeholder。
- 新增 `quiz/constants.py`，集中保存 hiragana / katakana keyboard rows。
- 建立 `static/js/quiz/kana_input.js`，處理假名 keyboard 對 hidden answer input 嘅輸入、backspace、濁音、半濁音、小假名同相關轉換。
- Quiz answer form 改用 hidden `answer` input，由 custom keyboard 更新答案，避免 user 直接使用一般輸入法輸入。
- 已手動測試 50 音 keyboard + Ajax quiz flow：keyboard 輸入答案、submit answer、result partial、Next 抽下一題可以串起來運作。

### Database 改動

- 無新增 schema migration。
- 今次主要係 quiz frontend flow、template partial、static JavaScript 同 view response contract 調整。

### 技術重點

- Ajax response 由單一 HTML partial 進一步演進成 JSON contract，令 main content 同 input panel 可以分開更新。
- Form action 仍然負責決定 submit answer / next question 指向邊個 view；Ajax 只負責攔截 submit、送出 `FormData` 同替換 partial。
- Input panel 係跟題目 type 變化嘅 UI component，因此比固定 page-level keyboard 更適合獨立成 partial。
- Hidden input 可以作為 backend form validation 所需嘅正式 answer field，而可見答案區域只負責 user feedback。
- 假名處理適合拆成純 JavaScript string helper，將 DOM / Ajax 控制同 kana conversion logic 分開。

### 理由

- Quiz 需要避免普通輸入法提示影響答題，因此 custom kana keyboard 係核心互動設計之一。
- Hiragana、katakana 同 multiple choice 將來會有不同輸入面板，將 input panel 同 main question/result area 分開能保留較大彈性。
- 先完成可操作嘅 Ajax quiz loop，可以確認 view、form、session、service、template 同 JavaScript 之間嘅整體 contract 可行。

### 學到咩

- GET link partial update 同 POST form partial update 係兩個不同 pattern；quiz answer 屬於 POST action，不應直接照搬 pagination link pattern。
- 外層 container 如果無被 replace，可以只取得一次 DOM reference；partial 入面被替換嘅元素，例如 answer input，Ajax 後需要重新取得。
- `FormData(form)` 會帶住 hidden input 同 CSRF token，適合用嚟配合 Django `FormView`。
- 前端 keyboard 操作只需要改 DOM / hidden input，唔需要每次按鍵都 Ajax；只有 submit answer / next question 先需要 backend。

## 2026-07-30 - Initial Ajax quiz play UI completion

Commit: `726517e`

Status: Quiz play UI now has a usable first-pass interaction loop; weight tuning and non-vocab answer types remain future work

### 主要改動

- `quiz_result_partial.html` 加入基本答題結果顯示，包括題目、正確答案、user submitted answer 同 correct / wrong 狀態。
- `QuizService.check_kana_answer()` 開始回傳 `is_correct`，令 result partial 可以用明確嘅 answer result 顯示結果，而唔只依賴 streak 推斷。
- `quiz_no_question_partial.html` 加入基本 no-question message 同返回 setting link，避免 Ajax flow 遇到無題時顯示空白。
- Quiz input panel 加入 show / hide flow，keyboard 預設可以收起，由 user 決定幾時打開。
- Tips button 完成前端初稿：可讀取 form 上嘅 correct answer data、修正或補完 hidden answer input，並同步更新 answer display。
- `tips_count` 會隨 tips click 遞增並跟 answer form submit 到 backend，準備之後納入 weight calculation。
- Quiz page JavaScript 進一步拆到 `static/js/quiz/quiz_play.js`，template 主要負責載入 script 同初始化 handler。
- Cleanup quiz UI wording 同 JavaScript comments，令目前互動流程更易讀。

### Database 改動

- 無新增 schema migration。
- 今次集中於 quiz UI、frontend behavior、answer result display 同 view context 調整。

### 技術重點

- Result display 應使用明確嘅 `is_correct` context，比 template 直接依賴 streak rule 更清楚。
- Tips 係一個 learning signal：user 即使已輸入完整正確答案，只要按 tips，就代表需要確認，因此 `tips_count` 仍應增加。
- Tips 前端邏輯要同時處理未輸入、部分輸入、錯字、超長輸入同完整正確答案等 edge cases。
- Show / hide keyboard 屬於純前端 DOM state，不需要 Ajax 或 backend 參與。
- Inline JavaScript 可以先用作驗證 flow，當互動邏輯穩定後再拆成 static JS file，讓 template 保持較清晰。

### 理由

- Quiz flow 已經能完成 question -> answer -> result -> next，但 user 需要明確知道自己答啱或答錯，先算有基本答題體驗。
- Tips button 會直接影響學習判斷同之後 weight adjustment，因此先建立 `tips_count` 提交路徑，再處理正式 weight rule。
- Keyboard show / hide 令 quiz 畫面不會長期被大型 input panel 佔住，亦保留 custom input 嘅可用性。

### 學到咩

- UI result state 應盡量由 view 提供語意清楚嘅 context，例如 `is_correct`，避免 template 知道太多 domain rule。
- Hidden input、data attribute 同 visible display 可以分別承擔 backend submit、frontend reference 同 user feedback 三種不同責任。
- Tips 呢類「輔助答題」功能要先定義產品語意，再寫 code；否則 edge cases 會令邏輯變得混亂。
- 將已穩定嘅 JavaScript 由 template 搬到 static file，可以自然形成「DOM/Ajax handler」同「kana string helper」兩層分工。

## 2026-07-30 - Quiz skip flow and shared Ajax payload helpers

Commit: `23b8327`

Status: Quiz play flow now supports answer, result, next and skip actions through the same Ajax partial response contract

### 主要改動

- 加入 `QuizSkipForm`、`QuizSkipView` 同 `quiz_skip` route，令 user 可以喺答題中 skip 目前題目。
- `quiz_question_partial.html` 加入獨立 skip form，避免 skip action 同 answer submit action 混喺同一個 POST intent。
- Skip flow 會先對目前 session 入面嘅 question vocab 執行 skip penalty，再抽下一題。
- `QuizService.skip_question_punish()` 會增加 skipped vocab weight、更新 streak，並寫入 `last_quiz_at`，避免 skip 後立即再抽中同一題。
- 抽下一題嘅共用流程抽成 `build_next_question_payload()`，讓 `QuizNextView` 同 `QuizSkipView` 重用同一套 JSON partial response contract。
- Input panel rows selection 抽成 helper，集中決定 hiragana keyboard、katakana keyboard 或 multiple choice panel。
- No-question partial 開始顯示 messages，令 fallback / no available question 狀態可以透過 Ajax response 顯示俾 user。

### Database 改動

- 無新增 schema migration。
- 今次主要係 quiz view routing、service stats update、session state、template partial 同 Ajax response flow 調整。

### 技術重點

- 同一個 quiz page 可以有多個 form，但每個 form 最好代表一個清晰 action，例如 submit answer、next question、skip question。
- Skip 不應只係「抽下一題」，亦係一次 learning signal；因此要更新 weight、streak 同 `last_quiz_at`。
- Ajax partial response 建立成共用 helper 後，可以減少 Next / Skip 兩條 flow 重複 render question partial、input panel partial 同 no-question partial。
- View-layer helper 可以暫時放喺 `views.py`，但當 helper 開始增加時，之後可考慮搬到 `quiz/view_helpers.py`，保持 service layer 專注 domain logic。

### 理由

- Quiz flow 需要提供 user 不懂或不想答時嘅正式出口，否則 user 只能亂答或離開頁面。
- Skip 後仍應影響抽題權重，因為 skip 代表該 vocab 對 user 仍未穩定掌握。
- Next 同 Skip 都係「取得下一題」嘅 UI action，共用 payload 建立流程可以降低之後改 JSON contract 或 input panel 時漏改嘅機會。

### 學到咩

- Button / form 嘅 action 應該反映 user intention；skip 同 submit answer 雖然都係 POST，但 domain 意義唔同，分開 endpoint 會清楚好多。
- Ajax response 可以用 structured payload 承載多個 partial，例如 `main_html` 同 `input_panel_html`，前端再按固定 contract replace 對應 DOM。
- Session 可以保存目前題目狀態，但使用時仍要用 user ownership query 再確認資料屬於目前 user。
- Helper 抽取有層次之分：render partial / build response payload 屬於 view helper；weight、streak、抽題則屬於 service logic。

## 2026-08-01 - Kana visual assets and image generation tools

Commit: `7af87d6`

Status: Quiz visual asset pipeline now has source files, exported kana images and a configurable background generator

### 主要改動

- 加入 hiragana / katakana kana image assets，準備用於 quiz answer display 同 wrong-answer visual feedback。
- 加入 normal / incorrect answer state 對應嘅 exported kana image folders。
- 加入 source PSD files，方便之後繼續調整 kana visual assets。
- 建立 `devtools/image_generator/generate_kana_bg.py`，用嚟生成 seamless kana background tile。
- 背景 generator 支援由 project root 執行，並固定輸出到 `assets/export/background/kana_bg_output_blue/`。
- 將 generator 常調參數抽到 `kana_bg_config.json`，包括字色、底色、字體大小、大小比例、字數、字距同同字重複距離。
- 加入 generator 專用 README，記錄 config 欄位用途同執行方式。
- 加入 `requirements.txt` 同 `requirements-dev.txt`，開始明確分開 runtime dependencies 同 development / asset generation dependencies。
- Project documents 已整理到 `docs/status/`，令 repo root 更集中保留 project entry files 同 source folders。

### Database 改動

- 無新增 schema migration。
- 今次集中於 visual assets、development tooling、dependency files 同 project documentation layout。

### 技術重點

- 原始素材、輸出素材同 runtime static assets 應分開管理；目前先用 `assets/source/` 保存 source files，用 `assets/export/` 保存 generated / exported assets。
- 生成工具應使用 script file location 推導 project root，避免因為 CLI current working directory 不同而輸出到 repo 外。
- Visual tuning values 放入 JSON config 後，可以反覆調色、密度同大小，而唔需要每次改 generator logic。
- WSL 環境要特別處理 Windows font path，否則可能 fallback 到無日文字形嘅 font，生成出一堆 missing glyph boxes。
- JSON 不支援 comments，因此需要用同層 README 解釋 config key 嘅語意。

### 理由

- Quiz 之後會越來越依賴視覺 feedback，例如 kana answer display、wrong-answer display 同背景氣氛，因此需要先建立可重用嘅 asset pipeline。
- 保留 PSD source files 可以避免之後只得 exported PNG，令視覺調整變得困難。
- 將 background generator 做成 configurable tool，可以用較低成本試唔同顏色、密度同字體大小，適合目前仍在探索 quiz UI 風格嘅階段。
- Dependency files 開始補齊後，project 更容易喺新環境重建。

### 學到咩

- Asset pipeline 亦係 project architecture 一部分；source assets、exported assets 同 app static assets 要有清楚分工。
- `Path(__file__).resolve()` 比相對路徑更適合 CLI tools，因為 script 可以由不同 working directory 執行。
- 字體 fallback 要實際打開 preview 驗證，command 成功輸出唔代表圖像內容一定正確。
- JSON config 適合保存 machine-readable values；人類解釋同調整指引應放喺 README。

## 2026-08-11 - Kana answer comparison visual feedback

Commit: `a8af3c5`

Status: Quiz result page can now render kana-by-kana answer comparison feedback using generated image mapping data

### 主要改動

- 建立 `QuizService.answer_compare()`，將 correct answer 同 user answer 拆成 `MATCH`、`WRONG`、`MISSING`、`EXTRA` result。
- Answer compare 已支援長度不同嘅答案，包括 user 漏字同多字。
- 加入 `match_count` tie-break，讓 diff result 優先保留更多位置上仍然對得返嘅 kana。
- 加入 `non_normal_wrong_count` tie-break，當 cost 同 match count 相同時，優先保留 `DAKUTEN`、`HANDAKUTEN`、`SMALL_KANA` 等更有教學意義嘅 wrong subtype。
- 建立 `compare_answer_subtype.json`，用 data map 判斷 kana pair 屬於 `NORMAL`、`DAKUTEN`、`HANDAKUTEN` 或 `SMALL_KANA`。
- 建立 `kana_graphic_map.json`，將 kana、compare type 同 subtype 對應到 static image path 同 font width。
- 將 exported kana font images copy 到 `static/rec/font/...`，讓 template 可以透過 Django static path 顯示。
- `QuizSubmitAnswerView` 開始產生 compare result graphic data，並傳入 `quiz_result_partial.html`。
- `quiz_result_partial.html` 已可 render 初版錯位 kana 圖。

### Database 改動

- 無新增 schema migration。
- 今次集中於 quiz answer comparison service、JSON config data、static image mapping 同 result partial rendering。

### 技術重點

- Answer diff 唔只係計最低 edit cost；同分時要再用 domain-specific signal 決定邊條 route 更適合教學顯示。
- `NORMAL` wrong 同 `DAKUTEN` / `HANDAKUTEN` / `SMALL_KANA` wrong 對 user feedback 價值唔同，因此需要額外 tie-break 權重。
- Compare subtype 判斷同 image selection 應分開：前者係 answer logic，後者係 presentation mapping。
- JSON mapping 適合保存大量固定 kana data，但 service 讀取時要有 fallback，避免未知 pair 直接變成 exception。
- Template 顯示 static image 時，JSON 應保存 static-relative path，例如 `rec/font/...`，再由 `{% static %}` 轉成實際 URL。

### 理由

- User 答錯時只顯示 correct / wrong 唔足夠；逐 kana 顯示錯位能更清楚指出係漏字、多字、濁音錯、半濁音錯，定係普通錯字。
- 使用 image feedback 可以延續 quiz 內自訂 kana keyboard 同 visual asset pipeline，令答題結果更直觀。
- 先用 `_red` 圖完成初版 flow，再將 missing underline / extra crossout 放入改良，可以避免 visual polish 阻住核心 logic。

### 學到咩

- Recursive diff algorithm 要先處理 base case，再進入 index access，否則長短答案會造成 out-of-range error。
- Python `min(..., key=lambda result: (...))` 可以用 tuple 做多層 tie-break，例如 cost、match count、non-normal subtype count。
- 字串比較應用 `!=`，唔應用 `is not`；後者係 object identity comparison。
- 一份 config file 最好只負責一種責任：`compare_answer_subtype.json` 判斷錯誤類型，`kana_graphic_map.json` 判斷顯示圖片。

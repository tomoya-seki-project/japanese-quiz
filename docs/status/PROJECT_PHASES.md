# Japanese Quiz - Development Phases

呢份文件以開發階段整理 Japanese Quiz 嘅產品演進同工程決策，主要供 portfolio 閱讀。
佢唔逐個 commit 重述施工紀錄；需要精確追蹤日期、commit 同 database 變更時，可以參考 [PROJECT_HISTORY.md](PROJECT_HISTORY.md)。

## Project Snapshot

Japanese Quiz 係一個以 Django 開發嘅日文詞彙學習系統。Project 由單純 dictionary 起步，逐步建立 user-specific vocabulary、受審核嘅字庫修改流程、weighted quiz、Ajax 答題介面、事件通知、feedback、application-level error handling 同 logging foundation。

核心方向包括：

- 將全域 `Vocab` master data 同每個 user 嘅 `UserVocab` learning state 分開。
- 所有正式字庫變更經 `VocabRequest` review workflow，而唔係由一般 user 直接修改 master data。
- 將跨 model、transaction 同 domain rules 集中到 service layer。
- Quiz 依據 user 自己嘅 weight、streak、recent history 同 `in_use` 狀態出題。
- 使用 Django Templates + vanilla JavaScript 建立 Ajax partial interaction，保留傳統 server-rendered 架構。

## Phase Overview

| Phase | 時間 | 主要成果 |
| --- | --- | --- |
| [Phase 1](#phase-1-project-foundation-and-account-system) | 2026-05-20 ～ 2026-05-29 | Django foundation、custom user、authentication |
| [Phase 2](#phase-2-dictionary-and-reviewed-vocab-workflow) | 2026-06-02 ～ 2026-06-22 | Dictionary、VocabRequest、admin review、service transactions |
| [Phase 3](#phase-3-personal-vocabulary-data-operations-and-notifications) | 2026-06-23 ～ 2026-07-19 | UserVocab、CSV operations、M2M categories、event system |
| [Phase 4](#phase-4-quiz-core-and-ajax-interaction) | 2026-07-20 ～ 2026-07-30 | Weighted quiz、session lifecycle、Ajax answer/next/skip |
| [Phase 5](#phase-5-visual-learning-feedback) | 2026-08-01 ～ 2026-08-11 | Kana assets、answer diff、custom keyboard、visual feedback |
| [Phase 6](#phase-6-user-facing-workflows-and-domain-hardening) | 2026-08-13 ～ 2026-08-22 | Feedback、UserVocab detail、permissions、data integrity |
| [Phase 7](#phase-7-extensibility-and-application-resilience) | 2026-08-24 ～ 2026-08-28 | MC sense foundation、error handling、resilient sync、logging foundation |
| [Phase 8](#phase-8-workflow-observability-and-project-review) | 2026-08-31 | Domain logging coverage、MCSense migration、全 project review |
| [Phase 9](#phase-9-quiz-performance-and-interface-language) | 2026-09-02 ～ 2026-09-06 | Bottom-up DP、unsupported-type isolation、日文 UI／語系分流、初步 regression tests |
| [Phase 10](#phase-10-explicit-quiz-pool-choice-and-review-context) | 2026-09-07 ～ 2026-09-08 | Explicit full-pool confirmation、VocabRequest reason／review note |
| [Phase 11](#phase-11-account-verification-and-email-identity-integrity) | 2026-09-09 ～ 2026-09-12 | Email activation、canonical identity、database uniqueness |
| [Phase 12](#phase-12-quiz-session-terminal-recovery) | 2026-09-12 | Current-question revalidation、empty-pool termination、shared summary lifecycle |

## Phase 1: Project Foundation and Account System

**時間：2026-05-20 ～ 2026-05-29**

### 目標

建立可持續擴展嘅 Django project foundation，同時先處理身份驗證，令之後所有 dictionary、quiz 同 personal learning data 都有穩定 user boundary。

### 主要成果

- 建立 `accounts`、`dictionary`、`quiz`、`core` app boundaries。
- 實作 custom `User` model，以 email 作 login identifier，並建立 custom user manager。
- 完成 registration、login、logout、remember-me session 同基本 profile flow。
- 建立 `UserProfile` extension，為之後保存 sync checkpoint 同 user-specific metadata 預留空間。
- 建立最初版 `Vocab`、detail models 同 timestamp foundation。

### 工程決策

- Project 初期已採用 custom user model，避免日後轉換 Django default user 帶來高成本 migration。
- Shared timestamp 行為集中到 abstract base model，減少各 app 重複欄位。
- Account、dictionary、quiz 同 shared concerns 分 app 管理，令責任範圍由一開始已經清晰。

### 階段結果

Project 由空白 Django scaffold 進入可登入、有 user identity、可開始承載 domain data 嘅狀態。

## Phase 2: Dictionary and Reviewed Vocab Workflow

**時間：2026-06-02 ～ 2026-06-22**

### 目標

建立一套「user 可以提議修改，但 master dictionary 必須經 admin review」嘅字庫治理流程。

### 主要成果

- 完成 active vocab list、detail、search，以及 create、update、delete、restore request flows。
- `VocabRequest` 保存 proposed snapshot、request type、status、creator 同 reviewer metadata。
- 建立 `VocabActionService` 同 `VocabRequestService`，集中處理正式 vocab mutation 同 request lifecycle。
- Django Admin 加入逐筆 review、approve、reject、readonly reviewed state 同 permission guard。
- Request creation 同 review 使用 `transaction.atomic()`；approve/reject 使用 `select_for_update()`、`PENDING` guard 同 POST action。
- 以 application check、conditional unique constraint 同 `IntegrityError` handling 防止 duplicate pending requests。
- 建立 admin-authenticated CSV import foundation，所有正式 vocab creation 共用同一 service path。

### 工程決策

- View/Form 負責 HTTP input 同 user feedback；service 負責跨 model rules、transaction 同 side effects。
- Admin 唔直接建立正式 vocab，避免繞過 detail model、validation 同 audit workflow。
- Soft delete 使用 `is_active`，保留歷史資料及 restore 能力。
- 預期內 concurrency conflict 轉成 `ValidationError`，回到 form，而唔係暴露 database exception。

### 階段結果

Dictionary 由一般 CRUD 提升成有審核、狀態、transaction、permission 同 concurrency protection 嘅 workflow system。

## Phase 3: Personal Vocabulary, Data Operations and Notifications

**時間：2026-06-23 ～ 2026-07-19**

### 目標

將全域字庫轉化成每個 user 自己可以管理同學習嘅資料，同時建立大量資料操作及 notification foundation。

### 主要成果

- 建立 `UserVocab`，分開 master vocab 同 user-specific `in_use`、weight、streak、answer counts、last answer、last quiz time。
- Login／registration 後自動補齊 user 未擁有嘅 active vocab，並用 `bulk_create(ignore_conflicts=True)` 降低大量同步成本。
- UserVocab list 支援 filtering、pagination、select-all 同 page-scoped bulk `in_use` update。
- `Vocab.categories` 由單一 category 演進成 Many-to-Many，支援一至三個 categories；request snapshot、admin review、filter 同 import 全部同步調整。
- 建立 category seed、vocab import 同 development clear commands，支援可重建嘅開發資料流程。
- 建立 `Event`／`UserEvent` models、unread count、event history、mark-as-read 同 vocab sync summary。
- Vocab sync event 使用 `last_vocab_sync_at` 作 checkpoint，將多次字庫變更濃縮成 user 可理解嘅 summary。

### 工程決策

- `Vocab` 代表全域 master data；`UserVocab` 代表 branch-specific learning state，兩者 lifecycle 唔應混合。
- Bulk operations 先取得 server-side allowed scope，再套用 submitted IDs，避免 user 修改 POST data 操作其他 user records。
- M2M categories 使用 `.set()` 管理關聯，避免將 multiple selection 當成普通 scalar field。
- 第一次 vocab event sync 只建立 checkpoint，唔向新 user 補發整個歷史字庫事件。

### 階段結果

System 開始具備 personalized learning data、可管理嘅資料匯入流程，同埋跨 session 嘅 notification history。

## Phase 4: Quiz Core and Ajax Interaction

**時間：2026-07-20 ～ 2026-07-30**

### 目標

將 `UserVocab` learning state 轉化成真正可操作嘅 quiz flow，而唔只係顯示字庫資料。

### 主要成果

- Quiz setting 可按 vocab type、JLPT level 同 categories 建立 question pool。
- Filter 無結果時 fallback 到 user 全部 active／in-use vocab，並保留 `fallback_used` state。
- Weighted random 使用 total weight、cumulative weights 同 `bisect_left` 抽題。
- 避開最近問過嘅 vocab，降低短時間內重複出題。
- `quiz_settings` 同 `quiz_session` 分開管理，支援有限題／無限題、resume、summary、skip 同途中離開。
- 建立 full-page shell + Ajax partial architecture；answer、result、next、skip 同 summary 使用清晰 endpoint responsibilities。
- Answer submit 驗證 session current question 同 `UserVocab` ownership，避免 hidden ID tampering 污染其他 records。
- Correct、wrong、tips、skip 同 streak 會更新 user-specific weight 及學習統計。

### 工程決策

- Partial template 表示 UI state；view endpoint 表示 user action，兩者唔應一對一混為同一概念。
- Submit answer、next、skip 使用獨立 forms／endpoints，令 POST intent 清晰。
- Quiz session 只保存流程狀態，真正 object ownership 仍由 database query 驗證。
- 抽題只讀取需要嘅 ID 同 weight，避免額外 `.count()` 及完整 model payload。

### 階段結果

Quiz 已形成可連續使用嘅核心 loop：設定 → 出題 → 作答／提示／跳題 → 結果 → 下一題 → summary。

## Phase 5: Visual Learning Feedback

**時間：2026-08-01 ～ 2026-08-11**

### 目標

令 quiz 唔只回覆 correct／wrong，而係指出 user 答案實際錯喺邊個 kana，同時建立一致嘅日文輸入及 visual asset pipeline。

### 主要成果

- 建立 hiragana／katakana custom keyboard，支援 backspace、濁音、半濁音、小假名、促音同長音符號。
- Keyboard state、answer hidden input 同 visible display 由 JavaScript 同步，毋須 reload 或額外 Ajax request。
- 建立 configurable kana background generator、web-size PNG resize helper，同 source／export／runtime assets 分層。
- `answer_compare()` 將答案拆成 `MATCH`、`WRONG`、`MISSING`、`EXTRA`。
- Domain-specific tie-break 會優先保留較多 match，以及 `DAKUTEN`、`HANDAKUTEN`、`SMALL_KANA` 等具教學價值嘅 subtype。
- JSON mappings 將錯誤分類同 image selection 分開，result partial 可逐 kana 顯示 visual feedback。

### 工程決策

- Answer diff 唔只追求最低 edit cost；同分時要選擇對 learner 最有解釋力嘅 alignment。
- Error subtype logic 同 presentation mapping 分離，避免 static asset naming 進入 comparison algorithm。
- 原始素材、generated exports 同 Django runtime static assets 分開保存，令設計調整唔污染 runtime structure。
- 先用 resize 後 PNG 支援 web display，避免將 bitmap 強行 trace 成複雜 SVG。

### 階段結果

Quiz 由功能性答題工具提升成可以呈現逐字錯誤差異嘅 learning interface；missing／extra overlay polish 則保留喺 UI task。

## Phase 6: User-Facing Workflows and Domain Hardening

**時間：2026-08-13 ～ 2026-08-22**

### 目標

補齊 dictionary／quiz 以外嘅 user workflows，並以全面 review 收緊 object boundary、permission 同資料一致性。

### 主要成果

- 建立 login-required feedback flow；普通 user 可提交，superuser 可 list、detail、reply，reply 後產生 event。
- Feedback duplicate policy 只阻擋內容相同而仍為 `PENDING` 嘅 submission，已回覆內容可再次提交。
- 建立 UserVocab detail，集中顯示 personal learning state、master vocab data、last-answer comparison 同單項 `in_use` control。
- Active vocab policy 套用到 sync、list、detail、request action、quiz setting count 同 question pool。
- DetailView 透過 `get_queryset()` 同 ownership filter 防止 URL guessing 存取其他 user 或 inactive records。
- Admin review 加強 original vocab active/inactive guard、custom action permission 同 reviewed-state readonly protection。
- Vocab types 擴展至 adverb、mimetic、conjunction 同 colloquial，準備支援更多題型。

### 工程決策

- Access control 應盡量收窄 object queryset，令不存在同無權存取都自然進入 404 boundary。
- Feedback reply 涉及 event、assignment 同 status update，集中到 service transaction 處理。
- Duplicate 規則要包含 lifecycle state；永久 unique constraint 未必適合「pending 時不可重複、resolved 後可以再提交」嘅 domain。
- Dictionary app 完成基本 flow 後，review 重點由單一 function 轉向跨入口 policy consistency。

### 階段結果

Project 已具備較完整嘅 user-facing support flow，同時將多個原本只靠正常 UI 路徑成立嘅假設，提升成 server-side boundary。

## Phase 7: Extensibility and Application Resilience

**時間：2026-08-24 ～ 2026-08-28**

### 目標

為 multiple-choice content 建立可擴展 schema，並處理 production-style failure response、Ajax recovery、非核心 side-effect isolation 同可追蹤嘅 runtime logging。

### 主要成果

- 建立 `MCSense` model foundation，讓同一 vocab 可有多個 stable、ordered sense records，保存 meaning、question prompts 同 distractors。
- 為 `(vocab, sense_no)` 同 `sense_key` 設定清晰 uniqueness responsibilities。
- 新增 `400`、`403`、`404`、`500` 全域 handlers 同基礎 templates。
- Quiz Ajax endpoints 統一 success／invalid-form JSON contract；前端會先檢查 response type，再處理 JSON 或通用 error fallback。
- Login、registration 同 profile 使用 resilient vocab sync wrapper；sync／event failure 會記錄 traceback，而唔會無必要中斷 account flow。
- Vocab sync event generation 使用 atomic transaction，確保 event rows、assignment 同 checkpoint 一致。
- 建立統一 logging formatter、console output、DEBUG-only file、INFO+ full-flow file 同 ERROR+ file，每日 rotate 並保留七日。
- 為五個 application apps 同 `django.request` 設定 logger routing，並為 vocab create / restore request 加入初步 operation logging。
- Custom `500` handler 使用獨立 template render path，避免錯誤頁再次執行可能失敗嘅 request context processors。
- Repository workflows 加入 Git root validation，避免同機多 clone 時寫入錯誤 workspace。

### 工程決策

- 預期內 validation error、HTTP error page 同真正 server exception 要有不同 response contract。
- Ajax client 必須處理 network failure、HTML error page、invalid JSON 同 structured form errors，唔可以假設所有 response 都係成功 JSON。
- 主操作同附帶 side effect 要按重要性分開 transaction boundary；可重試 sync／notification failure 唔應阻止 login 或 registration。
- Logging 要區分 normal operation、business rejection、warning 同 unexpected exception；handler level、filter 同 propagation 要一起設計，而且不可記錄 credentials 或完整 request payload。
- 500 fallback 要盡量減少 dependencies，不使用 database-backed navigation 或全站 context，避免 error handler 自己再失敗。
- Model definition 未等於 database rollout；呢個 phase 完結時 `MCSense` migration 尚未建立，並於之後嘅 Phase 8 工作目錄補上。

### 階段結果

Project 由「主要正常流程可用」進入處理 failure modes、recovery、schema extensibility、repository safety 同 observability foundation 嘅階段；domain workflow logging coverage 於 Phase 8 再擴展。

## Phase 8: Workflow Observability and Project Review

**時間：2026-08-31**

### 目標

將 logging foundation 擴展到主要 domain workflow，補上 `MCSense` database migration，並以全 project review 分清真正 defect、未完成 feature 同 deployment-stage work。

### 主要成果

- Vocab request／admin review、UserVocab sync／in-use、quiz、accounts、events、feedback 同 management commands 已加入 outcome-oriented logging。
- Logging fields 統一使用 operation、IDs、counts 同 result；避免 credentials、feedback body、session 或完整 POST payload。
- `MCSense` migration `0027_add_mc_sense.py` 已建立並在目前 local database 套用；migration graph 同 model state 一致，但檔案仍未 commit。
- 全 project review 由日語學習者、內容設計、software/data integrity 同 product/UX 四個角度完成，確認 quiz answer comparison、filter fallback 同未完成 MC 路徑係最優先處理範圍。
- Django system check 同 migration dry-run 通過；test discovery 仍然係 0 tests，production deploy check 有 7 個 warnings。

### 工程決策

- 未完成 feature 本身唔等於 defect；只有當 unsupported path 已公開畀 user 選擇或破壞現有 flow，先列入必要修正。
- Logging 應記錄有 audit 價值嘅 state change、business rejection 同 unexpected exception，避免每個 read/query 都產生噪音。
- 未 commit migration 只代表目前 working tree 狀態，唔可以當成其他 clone 已具備嘅 database rollout。

### 階段結果

Project 嘅主要 workflow 已有較完整 observability，同時將下一輪工作收斂到三個 quiz／state correctness 問題、最小 regression suite，以及尚未接通嘅 multiple-choice vertical flow。

## Phase 9: Quiz Performance and Interface Language

**時間：2026-09-02 ～ 2026-09-06**

### 目標

處理 project review 發現嘅 quiz 最壞效能及 unsupported-type exposure，並將一般 user interface 統一成日文，同時保留管理員英文操作環境。

### 主要成果

- Kana answer comparison 由指數級 recursive branch search 改成 `O(m × n)` bottom-up DP，保留原有 result contract、score ranking、wrong subtype preference 同 deterministic tie-breaking。
- 新舊 implementation 以 24,336 組 0 至 3 字元輸入作完整 equivalence comparison，結果無 mismatch；25 對 25 全 mismatch 約 0.0018 秒。
- 未完成嘅 `adverb`、`mimetic`、`conjunction`、`colloquial` choices 暫時停用，並以 migration `0028_vocabtype_cut_out_mc.py` 同步 model state；`MCSense` schema foundation 保留。
- 一般 user-facing templates、forms、validation、events、feedback、quiz result 同 dictionary labels 統一使用日文；管理員後台及管理員專用 feedback handling 保留英文。
- 新增 request-level interface language middleware，按頁面切換 `ja`／`en-us` 並於 response 後還原，避免不同 request 互相污染 active language。
- 五個 UI-label migrations 已建立、套用並隨 `ee31424` commit，保留 choices database values，只同步 model state 同 display metadata。
- 建立首批 10 個 regression tests，覆蓋 project templates compilation、語系 boundary、built-in validation、shared choices、keyboard values、output escaping、notification language 同 detail labels。

### 工程決策

- 未完成 MC feature 保留 model／migration foundation，但 active choices 暫時只公開 runtime 已完整支援嘅 `vocab` 同 `katakana`。
- Answer comparison 將「計最佳 score」同「重建逐字 result」分開；DP cell 只保存必要 state，下一格由 operation 推算。
- 語系以頁面 responsibility 分流，而唔係單純按登入 user role：管理員開啟一般使用者頁面仍見日文，只有管理員專用頁面使用英文。
- 共用 enum／choice 保留穩定 database value，只修改 display label；假名 keyboard data attributes 同 JavaScript event contract 同樣保持不變。

### 階段結果

Quiz answer comparison 嘅 request-time performance risk 已解除，未完成 MC 路徑亦唔再向 user 公開。Project 由零 automated tests 進入有基本 UI／language regression protection嘅狀態；下一輪核心 correctness 工作係修正 filter fallback continuation，並逐步補齊 domain、concurrency 同 quiz integration tests。

## Phase 10: Explicit Quiz Pool Choice and Review Context

**時間：2026-09-07 ～ 2026-09-08**

### 目標

移除會違反 user quiz setting 意圖嘅自動 fallback，並為 vocab request 補上申請理由與審批說明，令兩條 workflow 嘅決策背景更清楚。

### 主要成果

- Filtered question pool 無題時唔再靜默抽取設定範圍外題目；user 會先選擇返回 setting，或者明確確認使用 full active／in-use pool。
- Full-pool confirmation 使用 POST，並以 session `use_full_pool` flag 令 initial、Next 同 Skip 沿用相同決定；full pool 數量不足時直接返回 UserVocab list 並顯示 warning。
- `VocabRequest` 分開保存 user optional `request_reason` 同 admin `review_note`，覆蓋 CREATE／UPDATE／RESTORE／DELETE request creation flow。
- Admin 將 request reason 設為 readonly；Reject submit 透過動態 ModelForm rule 要求 review note 必填，Approve 則維持 optional。
- Approve／reject 結果 event 會包含 review note，將 reviewer 補充說明傳回申請人。
- Django system check 同現有 10 個 automated regression tests 通過。

### 工程決策

- User 明確設定嘅 quiz scope 唔應被系統靜默放寬；full pool 係需要 user 確認嘅替代路徑，而唔係自動 fallback。
- 申請人理由同 reviewer 說明代表兩個唔同責任與時間點，所以使用獨立 fields，而唔共用一個含義模糊嘅 `reason`。
- 「Reject 必須解釋」屬於 action-specific form rule；model 仍容許 review note 空白，令 Approve workflow 唔被迫填寫。

### 階段結果

Quiz no-pool 行為已由隱式 fallback 改為明確選擇，VocabRequest review 亦可以保存雙方決策背景。主要剩餘工作係補足相應 integration／concurrency tests，以及繼續 multiple-choice vertical flow。

## Phase 11: Account Verification and Email Identity Integrity

**時間：2026-09-09 ～ 2026-09-12**

### 目標

將 email login 由單純識別欄位提升成可驗證、具一致 canonical form 同 database integrity 保護嘅 account identity flow。

### 主要成果

- Public registration 先建立 inactive user，經 24 小時內有效嘅一次性 email link 確認後先啟用；GET 顯示確認，POST 先改動 account state。
- Registration email、activation confirmation／success／invalid states、resend form 同 login resend 入口已建立，並使用日文 user-facing wording。
- Resend 對 account 狀態使用統一回應，並以 per-user cache cooldown 限制重複寄送；email delivery failure 會記錄 audit context並保留可重試路徑。
- Activation 成功後先執行 resilient vocab sync，避免未驗證帳戶預先建立完整 `UserVocab`。
- Email canonicalization 集中到 custom manager，registration、login、resend 同 admin forms 均保存／查詢完整 lowercase email。
- `Lower("email")` functional unique constraint 已透過 migration `0007_email_upper_lower_problem.py` 套用；現有資料無 case collision 或非 lowercase email，system check 同 migration drift check通過。

### 工程決策

- Activation token 綁定 password、email 同 active state，令 account 啟用或 identity 改動後舊 token 自動失效。
- Email 作為 login identity 時採用完整 lowercase policy；form validation 提供易明錯誤，database constraint 負責最終 concurrency／bypass guard。
- Email activation delivery 暫時使用 development console backend；真實 mail provider、shared cache、HTTPS domain 同 secrets management 留作 production gate。

### 階段結果

Account 已具備完整 activation happy path，同一 email 嘅大小寫變體亦唔再可以建立多個 identity。Activation／canonicalization 正式 automated tests 尚待補充；email identity foundation 已完成並由 database constraint 保護。

## Phase 12: Quiz Session Terminal Recovery

**時間：2026-09-12**

### 目標

處理 quiz 開始後資料狀態改變嘅邊界，令目前題目失效或 question pool 中途變空時，server session、Ajax UI 同 learning state可以一致地終止，而唔係停留喺無法恢復嘅 unfinished flow。

### 主要成果

- Resume、正常／stale answer submit 同 skip 會重新驗證目前 `UserVocab` ownership、`in_use=True` 及相關 `Vocab.is_active=True`。
- 目前畫面題目失效時會終止 quiz，而唔會靜默換題；無效 answer／skip亦唔會修改 weight、streak、answer count或skip count。
- Answer／skip 後 question pool 變空時，抽題 helper 會回傳 `quiz_ended` terminal signal，由 view 建立提早結束 summary。
- 新增共用 `build_quiz_summary_payload()`，統一正常完成與提早完成嘅統計 rendering、input-panel cleanup同 `quiz_session` 移除。
- Summary 以 `question_unavailable`／`no_question_pool` reason code顯示相應日文說明；unfinished GET 無法恢復時會清 session、顯示 warning並返回 quiz setting。
- Commit `89d3030` 同時完成 email identity hardening及 quiz session recovery；Django system check、migration drift check同現有10個tests通過。

### 工程決策

- 已經顯示俾 user 嘅 current question 如中途失效，屬於明確 session state change，應終止並解釋原因，唔應突然換成另一題。
- 其他未顯示題目嘅 `in_use`／active變化唔需要即時終止 quiz；下一次建立 pool時自然反映最新database state。
- 查唔到 eligible current question係可預期 domain outcome，所以用 `.filter(...).first()` 轉成 terminal flow，而唔係直接用404打斷Ajax contract。
- `quiz_ended` 負責由 helper向view傳遞狀態，summary helper負責唯一 terminal cleanup，避免某一個endpoint漏清session。

### 階段結果

Review M-01 嘅核心 session recovery 已完成；專用 integration tests同抽題後重新載入object嘅短暫race window仍列作待測試／改良。下一個 correctness工作係處理 VocabRequest 已commit後 notification callback失敗所造成嘅HTTP結果矛盾；answer／skip並行idempotency則留待attempt ID同PostgreSQL方向一併設計。

## Current Architecture

```text
Browser / Django Templates / Vanilla JavaScript
                    |
             Forms and CBV Views
                    |
      +-------------+--------------+
      |             |              |
Vocab services  Quiz service   Core services
      |             |         Event / Feedback
      +-------------+--------------+
                    |
      Django ORM / Transactions / Constraints
                    |
 Accounts | Dictionary | UserVocab | Events | Feedback
```

主要 responsibility boundaries：

- **Middleware / Views / Forms**：interface language boundary、HTTP input、validation presentation、redirect／JSON response。
- **Services**：domain rules、跨 model orchestration、transactions、side effects。
- **Models / Constraints**：持久化結構、uniqueness、relationship 同基本 integrity。
- **Templates / JavaScript**：server-rendered UI、Ajax partial replacement、custom kana input。
- **Management Commands**：大量資料匯入、category seed 同 development reset。

## Engineering Themes Demonstrated

- Django custom authentication 同 admin customization。
- Service-layer separation 同 reusable mutation paths。
- Database transactions、row locking、conditional constraints 同 concurrency handling。
- ForeignKey／Many-to-Many modelling，以及 master data 與 user-specific state 分離。
- Session-driven quiz lifecycle、weighted random selection 同 learning statistics。
- Server-rendered Ajax partial architecture，同 structured frontend error recovery。
- Domain-specific answer diff、JSON-driven mappings 同 visual asset tooling。
- Permission、ownership、active-state boundary 同 soft-delete workflow。
- Severity-based application logging、daily rotation、retention 同 sensitive-data boundary。

## Current State and Remaining Work

目前 dictionary、VocabRequest review、UserVocab management、account email activation、event history、feedback 同 kana quiz core flows 已形成可操作嘅完整路徑。Kana answer comparison 已改用 bottom-up DP；filtered pool 無題時會由 user 明確選擇是否使用 full pool；進行中題目失效或pool變空時會明確結束並清理session；email identity 已統一 lowercase 並受 database case-insensitive uniqueness 保護；一般 user interface 已日文化並具備 request-level語系分流。Project 仍然係 development-stage，以下項目未完成：

- Automated test suite 已有 10 個 UI／language regression tests，但 account activation／identity、主要 domain、concurrency、quiz correctness 同 no-pool／full-pool integration coverage 尚未建立。
- Production settings 尚未 harden，包括 environment-based secrets、`DEBUG=False` deployment、hosts、static files 同 production database。
- Application logging handler、formatter、routing、daily rotation、retention 同主要 domain coverage 已建立；log assertions、rotation／retention 同 concurrent sync 尚待自動驗證。
- `MCSense` migration 已 commit；正式 multiple-choice import、admin/request 同 quiz flow尚未完成，相關 active choices 暫時停用。
- Quiz initial filtered no-pool／full-pool choice 同進行中 session terminal recovery 已完成；initial、Next、Skip、Submit、resume、失效題目同 insufficient-pool integration tests仍未補齊。
- VocabRequest 建立後嘅 staff notification 使用非 robust `transaction.on_commit()` callback；callback失敗可令主request已commit但HTTP仍報錯，下一輪會先決定best-effort或durable delivery policy再修正。
- Whole-database export／restore 尚未建立。
- Japanese UI wording 同語系分流已完成 code-level implementation；browser visual verification、layout 同 answer overlay 仍需 polish。

詳細工作狀態可參考 [TODO.md](TODO.md)，未納入目前 scope 嘅方向可參考 [FUTURE_IDEAS.md](FUTURE_IDEAS.md)。

# Japanese Quiz - Development Phases

呢份文件以開發階段整理 Japanese Quiz 嘅產品演進同工程決策，主要供 portfolio 閱讀。
佢唔逐個 commit 重述施工紀錄；需要精確追蹤日期、commit 同 database 變更時，可以參考 [PROJECT_HISTORY.md](PROJECT_HISTORY.md)。

## Project Snapshot

Japanese Quiz 係一個以 Django 開發嘅日文詞彙學習系統。Project 由單純 dictionary 起步，逐步建立 user-specific vocabulary、受審核嘅字庫修改流程、weighted quiz、Ajax 答題介面、事件通知、feedback 同 application-level error handling。

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
| [Phase 7](#phase-7-extensibility-and-application-resilience) | 2026-08-24 ～ 2026-08-25 | MC sense foundation、error handling、resilient sync |

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

**時間：2026-08-24 ～ 2026-08-25**

### 目標

為 multiple-choice content 建立可擴展 schema，並處理 production-style failure response、Ajax recovery 同非核心 side-effect isolation。

### 主要成果

- 建立 `MCSense` model foundation，讓同一 vocab 可有多個 stable、ordered sense records，保存 meaning、question prompts 同 distractors。
- 為 `(vocab, sense_no)` 同 `sense_key` 設定清晰 uniqueness responsibilities。
- 新增 `400`、`403`、`404`、`500` 全域 handlers 同基礎 templates。
- Quiz Ajax endpoints 統一 success／invalid-form JSON contract；前端會先檢查 response type，再處理 JSON 或通用 error fallback。
- Login、registration 同 profile 使用 resilient vocab sync wrapper；sync／event failure 會記錄 traceback，而唔會無必要中斷 account flow。
- Vocab sync event generation 使用 atomic transaction，確保 event rows、assignment 同 checkpoint 一致。
- Repository workflows 加入 Git root validation，避免同機多 clone 時寫入錯誤 workspace。

### 工程決策

- 預期內 validation error、HTTP error page 同真正 server exception 要有不同 response contract。
- Ajax client 必須處理 network failure、HTML error page、invalid JSON 同 structured form errors，唔可以假設所有 response 都係成功 JSON。
- 主操作同附帶 side effect 要按重要性分開 transaction boundary；可重試 sync／notification failure 唔應阻止 login 或 registration。
- Model definition 未等於 database rollout；`MCSense` migration 尚待建立，文件必須保留呢個限制。

### 階段結果

Project 由「主要正常流程可用」進入開始處理 failure modes、recovery、schema extensibility 同 repository safety 嘅階段。

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

- **Views / Forms**：HTTP input、validation presentation、redirect／JSON response。
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

## Current State and Remaining Work

目前 dictionary、VocabRequest review、UserVocab management、event history、feedback 同 kana quiz core flows 已形成可操作嘅完整路徑。Project 仍然係 development-stage，以下項目未完成：

- Automated test suite 尚未建立，目前主要依賴 Django system check、targeted inspection 同 manual browser testing。
- Production settings 尚未 harden，包括 environment-based secrets、`DEBUG=False` deployment、hosts、static files 同 production database。
- Application logging 仍要完成正式 handler／formatter／retention 設定。
- `MCSense` migration 同正式 multiple-choice quiz flow 尚未完成。
- Whole-database export／restore 尚未建立。
- Japanese UI wording、layout 同 answer overlay 仍需 polish。

詳細工作狀態可參考 [TODO.md](TODO.md)，未納入目前 scope 嘅方向可參考 [FUTURE_IDEAS.md](FUTURE_IDEAS.md)。

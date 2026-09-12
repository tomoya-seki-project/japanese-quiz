# Japanese Quiz

一個用 Django 開發嘅 Japanese vocabulary learning project。

Project 目前集中處理 user account、vocab dictionary、`VocabRequest` review workflow、`UserVocab` learning data、event notification、user feedback flow、Ajax quiz flow、application error handling 同 logging foundation。

> **Project status：開發中**
>
> 呢個 project 暫時未適合 production 使用。Dictionary、VocabRequest review flow、CSV vocab import、`UserVocab` sync flow、account email activation及identity canonicalization、event notification、user feedback、Ajax quiz play、quiz session terminal recovery、bottom-up DP answer comparison、日文 user interface、HTTP error pages 同 rotating-file logging foundation 已經建立，但 multiple-choice flow、quiz scoring balance、完整 import/export、完整 automated regression coverage 同 production settings 仍然未完成。

## Current Features

### Accounts

- Custom `User` model，以 email 作為 login identifier。
- User registration 會先建立 inactive account，經有時限嘅一次性 email link 確認後先啟用；亦支援統一回應及 cooldown 保護嘅 activation email resend。
- Registration、login、resend 同 admin user forms 會將 email 統一成 lowercase；database 亦以 case-insensitive unique constraint 防止大小寫變體帳戶。
- Login、logout 同 profile page。
- Login session 可以選擇 remember me。
- Django Admin 可以管理 users。

### Dictionary

- 顯示 active vocab list。
- 支援按 word、kana、JLPT level 同 category search。
- Vocab detail page。
- Logged-in user 可以查看自己嘅 `UserVocab` list。
- `UserVocab` 支援 `in_use` 狀態，方便將「已加入但未啟用」同「正在 quiz 使用」嘅 vocab 分開。
- 支援一般 vocab 同 katakana vocab data。

### VocabRequest

- Logged-in user 可以建立 vocab create request。
- 可以為現有 vocab 建立 update、delete 或 restore request。
- 使用 database constraints 防止 duplicate pending requests。
- Request creation flow 使用 `transaction.atomic()`。
- Django Admin 已經有 approve / reject UI，經 POST request 處理。
- Approve 會按 request type 執行 create、update、restore 或 deactivate vocab。
- User 可為 create、update、restore 同 delete request 提供 optional request reason；reviewer 亦可另外填寫 review note。
- Reject 會更新 request status 同 reviewer，但唔會改動 vocab，並要求 reviewer 必須填寫 review note。
- Approve／reject 結果通知會包含 reviewer note。
- Approve / reject flow 使用 `transaction.atomic()`、`select_for_update()` 同 pending status check，減少重複 review 風險。

> **未完善：** DELETE request 已保存完整 proposed snapshot；additional vocab types 同 `MCSense` schema foundation 已建立，但 request、import、admin 同 quiz runtime flow 仍未接通。

### Admin

- 管理 `Vocab`、`UserVocab` 同 `VocabRequest`。
- VocabRequest admin page 有 custom approve / reject buttons。
- Vocab admin 禁止直接新增 vocab，正式 creation path 會經 `VocabActionService`。
- Vocab type 喺 admin change form 入面設為 readonly，避免 type/detail mismatch。
- 可以查看 user learning stats，例如 weight、correct count、incorrect count 同 streak。

### Quiz

- 已有 quiz setting form，可按 vocab type、JLPT level 同 category 選擇出題範圍。
- Quiz question pool 來自目前 user 嘅 `UserVocab(in_use=True)`。
- 支援 weighted random selection，weight 越高越容易被抽中。
- 會避開最近 quiz 過嘅 10 個 vocab，減少短時間重複出題。
- Filter 無題時唔會自動提供設定範圍外嘅題目；user 會先進入確認頁，選擇返回 setting 或經 POST 明確改用 full active／in-use pool。
- Full active pool 數量不足最低出題要求時會返回 `UserVocab` list 並顯示 warning；確認使用 full pool 後，Next／Skip 會沿用同一 pool。
- Resume、answer submit同skip會重新驗證目前題目仍屬於該user、`in_use=True`及related vocab active；題目中途失效時會終止quiz，避免繼續更新無效learning state。
- Answer／skip後如果question pool中途變空，會顯示提早結束summary並清除`quiz_session`，避免user再次被送返無法完成嘅unfinished flow。
- Quiz play page 已使用 Ajax partial flow：answer submit、result、next question 同 skip question 都可以局部更新。
- Hiragana / katakana custom keyboard panel 已有初稿，answer 會寫入 hidden input 再提交到 backend。
- Tips button 已有前端提示邏輯，並會提交 `tips_count` 俾 backend 納入 weight calculation。
- Skip question flow 已建立，會增加 skipped vocab weight、更新 streak 同 `last_quiz_at`。
- Quiz result 已可顯示 kana-by-kana answer comparison visual feedback，支援 match、wrong、missing 同 extra kana 顯示。
- Answer comparison 會判斷 `NORMAL`、`DAKUTEN`、`HANDAKUTEN`、`SMALL_KANA` wrong subtype，並用 static kana image assets 顯示初版錯位圖。
- Answer comparison 已由指數級 recursive branch search 改為 `O(m × n)` bottom-up DP，保留原有 score ranking、subtype preference、deterministic tie-breaking 同 result contract。
- Quiz summary flow 已可統計答題數、正確數、錯誤數、skip 數同 tips 使用量。

### Interface Language

- 一般 user-facing UI 使用日文；Django Admin 同只供管理員處理 feedback／審批嘅介面維持英文。
- Request-level language middleware 會按頁面切換 `ja`／`en-us`，response 後還原原本語系，避免相鄰 requests 互相污染。
- Model／form choices 保留原有 database values，只調整顯示 label；假名 keyboard 同 JavaScript event values亦保持不變。

### Events

- 已建立 `Event` / `UserEvent` data model foundation。
- Vocab request result event 同 vocab sync summary event 已有 service flow 初稿。
- User event list / detail page 已可顯示基本 notification data。

### Feedback

- Logged-in user 可以提交 feedback，例如 vocab suggestion、bulk vocab request、bug report 或 feature request。
- Feedback 入口會按 user role redirect：superuser 去 feedback list，普通 user 去 feedback create。
- Superuser 可以查看 feedback list / detail。
- Superuser 可以 reply feedback。
- Reply 後會將 feedback status 由 `PENDING` 更新成 `REPLIED`，並建立 `FEEDBACK_REPLY` event 通知提交者。

### Error Handling and Logging

- 已註冊全域 `400`、`403`、`404` 同 `500` error handlers。
- Quiz Ajax action 會將 form validation failure 回傳 structured `400` JSON，前端亦會處理非 JSON response、network failure 同 parsing failure。
- Account entry points 使用 resilient vocab sync wrapper，sync 或 event side effect 失敗時會保留 traceback，避免無必要中斷 login、registration 或 profile flow。
- Application logging 已有 console、DEBUG-only、INFO+ 同 ERROR+ handlers，file logs 每日 rotate 並保留七日。
- Vocab request／admin review、UserVocab sync／in-use、quiz、accounts、events、feedback 同 vocab management commands 已加入 outcome-oriented logging，並避免記錄 credentials、feedback body或完整 POST payload。

## Planned Features

- 根據 `last_quiz_at` 提升太耐冇出現嘅 vocab weight。
- `MCSense` CSV import、admin/request integration 同 multiple-choice quiz answer flow。
- Whole database CSV export / restore。

完整規劃可以睇 [docs/status/TODO.md](docs/status/TODO.md)。

## Tech Stack

| Item | Current choice |
| --- | --- |
| Backend | Django |
| Language | Python |
| Database | SQLite |
| Frontend | Django Templates |
| Authentication | Django Auth + custom `User` model |
| Time zone | Asia/Tokyo |

`config/settings.py` 顯示 project 由 Django `6.0.5` 建立。

## Main Data Models

### Accounts

- `User`：使用 email login 嘅 custom user。
- `UserProfile`：user profile extension。

### Dictionary

- `Vocab`：word、kana、meaning、type、level、category 等基本資料。
- `VocabDetail`：一般 vocab 嘅 detail extension。
- `KatakanaDetail`：katakana 專用資料，例如 native Japanese。
- `UserVocab`：連接 user 同 vocab，保存 `in_use`、weight、answer counts、streak 同 last quiz time。
- `VocabRequest`：保存 create、update、delete、restore request。
- `MCSense`：multiple-choice vocab 嘅多義 sense foundation，保存 question prompts 同 distractors；migration `0027_add_mc_sense.py` 已 commit，實際 import/admin/request/quiz flow仍未接通。

### Core

- `TimeStampedModel`：共用 create/update timestamps。
- `Event`：系統事件 master record。
- `UserEvent`：連接 user 同 event，保存 read status。
- `Feedback`：保存 user feedback、suggestion、bug report、reply status 同 admin reply metadata。

## Project Structure

```text
accounts/      User model、authentication、account pages
assets/        Source and exported visual assets
config/        Django settings、root URLs、WSGI / ASGI
core/          Shared models、base templates、general pages
devtools/      Development-only helper tools, including image generators
dictionary/    Vocab models、forms、views、admin、request service
docs/          Project status and development documentation
errorHandler/  Global HTTP error handlers and templates
log/           Runtime application logs; generated .log files are ignored
quiz/          Quiz settings、weighted random service、Ajax quiz play flow
```

其他 project documents：

- [docs/status/PROJECT_PHASES.md](docs/status/PROJECT_PHASES.md)：按開發階段整理嘅 portfolio 技術總覽。
- [docs/status/PROJECT_HISTORY.md](docs/status/PROJECT_HISTORY.md)：主要開發歷史。
- [docs/status/TODO.md](docs/status/TODO.md)：已發現問題、planned features 同 implementation notes。

## Local Setup

### 1. Clone Project

```bash
git clone https://github.com/tomoya-seki-project/japanese-quiz.git
cd japanese-quiz
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Windows：

```powershell
.venv\Scripts\activate
```

macOS / Linux：

```bash
source .venv/bin/activate
```

部分環境需要將 `python` 改成 `py` 或 `python3`。

### 3. Install Dependencies

Runtime dependencies：

```bash
python -m pip install -r requirements.txt
```

Development / asset-generation dependencies：

```bash
python -m pip install -r requirements-dev.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

Custom user model 會要求 email、username 同 password。

### 6. Start Development Server

```bash
python manage.py runserver
```

預設 development URL：

- Website: `http://127.0.0.1:8000/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## Main URLs

| URL | Purpose |
| --- | --- |
| `/` | Project home |
| `/accounts/` | Account home |
| `/accounts/user_regist/` | User registration |
| `/accounts/user_login/` | Login |
| `/accounts/user_detail/` | User detail |
| `/dictionary/` | Dictionary home |
| `/dictionary/vocab/list` | Active vocab list |
| `/dictionary/vocab/create` | Create vocab request |
| `/dictionary/user_vocab/list` | Current user vocab list |
| `/quiz/` | Quiz home |
| `/quiz/setting` | Quiz setting |
| `/quiz/play` | Ajax quiz play page |
| `/core/feedback/` | Feedback entry redirect |
| `/core/feedback/create/` | Submit feedback |
| `/core/feedback/list/` | Superuser feedback list |
| `/admin/` | Django Admin |

## Management Commands

### Import Vocab

`import_vocab` 已開始實作，用嚟俾 admin 由 CSV 匯入 vocab：

```bash
python manage.py import_vocab list.csv
```

目前 command 會：

- 要求輸入 admin email / password。
- 只容許 superuser 執行。
- 檢查必要 CSV headers。
- 逐行呼叫 `VocabActionService.create_vocab()` 建立 vocab 同對應 detail model。
- 支援 `category1`、`category2`、`category3`，配合 `Vocab.categories` ManyToManyField。
- row-level validation / integrity error 會輸出錯誤並繼續處理下一行。
- 輸出成功 / 失敗 row summary。

預期 CSV headers：

```bash
word,kana,meaning,type,level,category1,category2,category3,native_japanese
```

### Setup Categories

`setup_categories` 用嚟由 CSV seed category data：

```bash
python manage.py setup_categories resource/categories.csv
```

### Development Clear Vocab

`dev_clear_vocab` 用嚟喺開發期間清理 vocab 相關資料，方便重建測試資料：

```bash
python manage.py dev_clear_vocab
```

> **注意：** 呢個 command 只應用喺 local development / testing。

### Export / Restore

計劃中嘅 command interface：

```bash
python manage.py export_whole <output_folder>
```

`export_vocab_to_csv` 目前只係 placeholder；完整 database export / restore flow 尚未實作。

## Visual Assets / Dev Tools

Quiz visual assets are stored outside the Django static runtime folders while they are still being designed.

Current asset layout:

```text
assets/source/      Source files, such as PSD files
assets/export/      Exported/generated assets
devtools/           Development helper scripts
```

### Kana Background Generator

`devtools/image_generator/generate_kana_bg.py` generates reusable kana background tiles:

```bash
python devtools/image_generator/generate_kana_bg.py
```

The generator writes output to:

```text
assets/export/background/kana_bg_output_blue/
```

Visual tuning values such as font colors, background color, font sizes, density and character counts are configured in:

```text
devtools/image_generator/kana_bg_config.json
```

The generator has its own notes in [devtools/image_generator/README.md](devtools/image_generator/README.md).

## Testing

> **初步建立，尚未完整**

目前已有 10 個 UI／language regression tests，覆蓋 templates compile、public/admin language boundary、built-in validation language、共用 choices、假名 keyboard event values、answer escaping、notification language 同主要 detail labels。

之後預計加入：

- VocabRequest create/update/delete/restore tests。
- Duplicate pending request tests。
- Admin approve/reject tests。
- UserVocab streak 同 weight calculation tests。
- Weighted random 同 recent 10 questions tests。
- Event notification tests。
- Quiz answer comparison correctness／performance tests。
- Quiz filtered no-pool confirmation、full-pool initial／Next／Skip integration tests。

預計 test command：

```bash
python manage.py test
```

## Current Limitations

- Kana quiz 已有 Ajax play、weight adjustment 同 answer comparison flow，但 multiple-choice answer flow 仍未接通。
- Kana answer comparison performance 問題已用 bottom-up DP 解決；filter 無題改為由 user 明確確認是否使用 full pool，唔再靜默 fallback。
- `MCSense` model 同 migration foundation 已建立並 commit；validation、import、admin、request 同 quiz integration 仍未完成。四種未完成 MC vocab choices 暫時停用，避免 user 進入未接通流程。
- VocabRequest approve/reject 已有 transaction、row lock、permission、`original_vocab` state guard、完整 DELETE proposed snapshot，以及分開嘅 request reason／review note；Reject 必須提供 review note。
- Event notification system 已有 request result、vocab sync summary 同 feedback reply flow，UI / wording 同更多 event type 仍可改善。
- Feedback flow 已建立，但 UI wording、public contact form 同更細緻 admin handling status 仍未 polish。
- Logging handlers 同主要 domain flow coverage 已建立；log assertions、concurrent sync 同 rotation／retention 仍待自動驗證。
- 完整 export / restore 尚未完成。
- Automated tests 已有初步 UI／language coverage，但主要 domain、concurrency、quiz correctness 同 no-pool/full-pool integration tests 仍未建立。
- User-facing wording 已完成日文化及語系分流；UI layout、answer overlay 同 browser visual verification 仍需繼續整理。
- Production deployment settings 未準備。

## Security Notes

目前 settings 只適合 local development：

- `SECRET_KEY` 仍然直接寫喺 settings。
- `DEBUG=True`。
- `ALLOWED_HOSTS` 未設定。
- 未使用 environment variables。
- 未完成 production static files、HTTPS、database 同 deployment configuration。

正式 deployment 前必須處理以上項目。

## Development History

Project 由 2026-05-20 開始，主要改動同相關 code paths 記錄喺 [docs/status/PROJECT_HISTORY.md](docs/status/PROJECT_HISTORY.md)。

## Contributing

> **未準備**

Project 目前主要係 personal learning project，暫時未有正式 contribution guide、issue template 或 pull request rules。

## License

> **未決定**

Project 暫時未加入 license。未選擇 license 前，請唔好假設 project code 可以自由複製、修改或重新發布。

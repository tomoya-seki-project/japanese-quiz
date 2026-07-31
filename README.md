# Japanese Quiz

一個用 Django 開發嘅 Japanese vocabulary learning project。

Project 目前集中處理 user account、vocab dictionary、`VocabRequest` review workflow、`UserVocab` learning data，同初步 Ajax quiz flow。

> **Project status：開發中**
>
> 呢個 project 暫時未適合 production 使用。Dictionary、VocabRequest review flow、CSV vocab import、`UserVocab` sync flow、event notification foundation 同初步 quiz play flow 已經建立，但 quiz scoring balance、完整 import/export、automated tests 同 production settings 仍然未完成。

## Current Features

### Accounts

- Custom `User` model，以 email 作為 login identifier。
- User registration、login、logout 同 profile page。
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
- Reject 會更新 request status 同 reviewer，但唔會改動 vocab。
- Approve / reject flow 使用 `transaction.atomic()`、`select_for_update()` 同 pending status check，減少重複 review 風險。

> **未完善：** Approve UPDATE / RESTORE / DELETE request 前仍要補強 `original_vocab` validation；event notification flow 已有初稿，但仍要補 UI / wording 同更多 event type。

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
- Filter 無題時會 fallback 到 user full active vocab pool，並保留 `fallback_used` state。
- Quiz play page 已使用 Ajax partial flow：answer submit、result、next question 同 skip question 都可以局部更新。
- Hiragana / katakana custom keyboard panel 已有初稿，answer 會寫入 hidden input 再提交到 backend。
- Tips button 已有前端提示邏輯，並會提交 `tips_count` 俾 backend 之後計算 weight 用。
- Skip question flow 已建立，會增加 skipped vocab weight、更新 streak 同 `last_quiz_at`。

### Events

- 已建立 `Event` / `UserEvent` data model foundation。
- Vocab request result event 同 vocab sync summary event 已有 service flow 初稿。
- User event list / detail page 已可顯示基本 notification data。

## Planned Features

- 根據 answer、tips used 同 streak 更新 vocab weight。
- 根據 `last_quiz_at` 提升太耐冇出現嘅 vocab weight。
- Multiple choice quiz answer flow。
- Katakana quiz answer checking。
- User-to-admin vocab message inbox。
- Whole database CSV export / restore。
- Account email activation。

完整規劃可以睇 [TODO.md](TODO.md)。

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

### Core

- `TimeStampedModel`：共用 create/update timestamps。
- `Event`：系統事件 master record。
- `UserEvent`：連接 user 同 event，保存 read status。
- `AdminMessage`：初步 message model，功能仍未完善。

## Project Structure

```text
accounts/      User model、authentication、account pages
config/        Django settings、root URLs、WSGI / ASGI
core/          Shared models、base templates、general pages
dictionary/    Vocab models、forms、views、admin、request service
quiz/          Quiz settings、weighted random service、Ajax quiz play flow
```

其他 project documents：

- [PROJECT_HISTORY.md](PROJECT_HISTORY.md)：主要開發歷史。
- [TODO.md](TODO.md)：已發現問題、planned features 同 implementation notes。

## Local Setup

### Requirements Status

> **未準備完善**

Project 暫時未有 `requirements.txt` 或 `pyproject.toml`。根據目前 settings，開發環境需要 Python 同 Django；其他 dependency 尚未正式整理。

以下步驟只係目前嘅 provisional setup。

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

### 3. Install Django

正式 dependency file 未建立前，可以暫時安裝 settings 所顯示嘅 Django version：

```bash
python -m pip install Django==6.0.5
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
python manage.py setup_categories
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

## Testing

> **未準備完善**

各 app 已有 `tests.py`，但目前未有實際 automated tests。

之後預計加入：

- VocabRequest create/update/delete/restore tests。
- Duplicate pending request tests。
- Admin approve/reject tests。
- UserVocab streak 同 weight calculation tests。
- Weighted random 同 recent 10 questions tests。
- Event notification tests。

預計 test command：

```bash
python manage.py test
```

## Current Limitations

- Quiz app 已有初步 Ajax play flow，但 weight adjustment、multiple choice answer flow 同 katakana checking 仍要完善。
- VocabRequest approve/reject 已有基本 service flow，但 `original_vocab` validation 仍要補強。
- Event notification system 已有 foundation，但 UI / wording 同更多 event type 仍要完善。
- User-to-admin message flow 未建立。
- 完整 export / restore 尚未完成。
- Requirements file 未建立。
- Automated tests 未建立。
- UI 仍然係 development / temporary version。
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

Project 由 2026-05-20 開始，主要改動同相關 code paths 記錄喺 [PROJECT_HISTORY.md](PROJECT_HISTORY.md)。

## Contributing

> **未準備**

Project 目前主要係 personal learning project，暫時未有正式 contribution guide、issue template 或 pull request rules。

## License

> **未決定**

Project 暫時未加入 license。未選擇 license 前，請唔好假設 project code 可以自由複製、修改或重新發布。

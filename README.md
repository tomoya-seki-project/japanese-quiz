# Japanese Quiz

一個用 Django 開發嘅 Japanese vocabulary learning project。

Project 目前集中處理 user account、vocab dictionary、`VocabRequest` review workflow，同之後 quiz system 需要用到嘅 `UserVocab` learning data。

> **Project status：開發中**
>
> 呢個 project 暫時未適合 production 使用。部分頁面同 data flow 已經建立，但 quiz、request approval、notification、CSV import/export 等功能仍然未完成。

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
- 支援一般 vocab 同 katakana vocab data。

### VocabRequest

- Logged-in user 可以建立 vocab create request。
- 可以為現有 vocab 建立 update、delete 或 restore request。
- 使用 database constraints 防止 duplicate pending requests。
- Request creation flow 使用 `transaction.atomic()`。
- Django Admin 已經有 custom approve / reject UI。

> **未完善：** `approveVocabRequest()` 同 `rejectVocabRequest()` 目前仍然係 placeholder，未有真正更新 vocab/request data。

### Admin

- 管理 `Vocab`、`UserVocab` 同 `VocabRequest`。
- VocabRequest admin page 有 custom approve / reject buttons。
- 可以查看 user learning stats，例如 weight、correct count、incorrect count 同 streak。

## Planned Features

- Weighted random quiz question selection。
- Skip 最近出過嘅 10 題。
- 根據 answer、tips used 同 streak 更新 vocab weight。
- 根據 `last_quiz_at` 提升太耐冇出現嘅 vocab weight。
- Event / notification system。
- User-to-admin vocab message inbox。
- Admin 整理資料後用 CSV 一次過 import vocab。
- VocabRequest result event 同 `UserVocab` confirmation flow。
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
- `UserVocab`：連接 user 同 vocab，保存 weight、answer counts、streak 同 last quiz time。
- `VocabRequest`：保存 create、update、delete、restore request。

### Core

- `TimeStampedModel`：共用 create/update timestamps。
- `AdminMessage`：初步 message model，功能仍未完善。

## Project Structure

```text
accounts/      User model、authentication、account pages
config/        Django settings、root URLs、WSGI / ASGI
core/          Shared models、base templates、general pages
dictionary/    Vocab models、forms、views、admin、request service
quiz/          Quiz app placeholder，核心 logic 尚未實作
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
| `/quiz/` | Quiz placeholder |
| `/admin/` | Django Admin |

## Management Commands

以下 commands 已經有 file structure，但 implementation 尚未完成：

```bash
python manage.py import_vocab
python manage.py export_vocab_to_csv
```

目前兩個 commands 只會輸出 `success`，未會讀取或寫出 CSV。

計劃中嘅 command interface：

```bash
python manage.py import_vocab list.csv
python manage.py export_whole <output_folder>
```

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

- Quiz app 暫時只係 placeholder。
- VocabRequest approve/reject 未真正實作。
- Event notification system 未建立。
- User-to-admin message flow 未建立。
- CSV import/export commands 未實作。
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

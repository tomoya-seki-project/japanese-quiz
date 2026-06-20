# Project History

呢份記錄係用 git commit history 整理返出嚟，主要記低 project 到目前為止每次大改動做過啲乜。

每個記錄下面會列出比較重要嘅 updated code。

「理由」同「學到咩」會留空，方便之後自己補返當時嘅 decision 同 learning。

## 2026-05-20 - Project initial setup

Commit: `ad4deee`

一開始建立 project 基礎結構，準備好主要 apps 同基本 models，令 Japanese Quiz 呢個 project 有第一個可以繼續發展落去嘅 base。

比較重要嘅 updated code：

- `config/settings.py`、`config/urls.py`：建立 Django project 基本 settings 同 routing。
- `accounts/models.py`：建立 user / profile 基礎 models。
- `dictionary/models.py`：建立 dictionary domain 嘅基本 models。
- `quiz/models.py`：準備 quiz app 嘅 model structure。
- `manage.py`：加入 Django management entry point。

理由：

學到咩：

## 2026-05-20 - First migrate 同 custom user manager

Commit: `adf7f9e`

做咗第一次 migration 之後，加入 user manager 相關設定，開始將 accounts app 嘅 user handling 整得完整啲。

比較重要嘅 updated code：

- `accounts/models.py`：加入 custom user manager 相關設定。
- `accounts/migrations/0002_alter_user_managers.py`：記錄 user manager schema change。
- `dictionary/models.py`：整理第一版 vocab model。
- `dictionary/migrations/0001_first_ver_vocab_model.py`：建立第一版 dictionary database schema。

理由：

學到咩：

## 2026-05-25 - Login system

Commit: `be08b3d`

加入 login system，開始有 user login/logout/register 相關 flow，令 project 唔再只係 model level，而係開始有 user 可以實際用嘅入口。

比較重要嘅 updated code：

- `accounts/forms.py`：加入 account login / register 相關 forms。
- `accounts/views.py`：處理 user authentication flow。
- `core/templates/core/base.html`：建立共用 page layout 同 navigation 基礎。

理由：

學到咩：

## 2026-05-29 - User pages, AdminMessage, create vocab flow

Commit: `c67a9d0`

加咗 accounts 相關 templates，例如 user detail、home、login、logout、regist。  
同時加入 `AdminMessage` model，調整 core view/template，dictionary 方面亦開始加入 forms、model field changes，同 create vocab flow 嘅基礎。

比較重要嘅 updated code：

- `accounts/views.py`、`accounts/forms.py`：完善 account pages 同 form handling。
- `accounts/templates/accounts/`：加入 login、logout、register、home 同 user detail pages。
- `core/models.py`：加入 `AdminMessage` model。
- `dictionary/forms.py`、`dictionary/views.py`：開始建立 create vocab flow。
- `dictionary/models.py`：調整 vocab fields、language choices 同 streak data。

理由：

學到咩：

## 2026-06-02 - Prepare VocabRequest create/update/delete

Commit: `e8b7bb8`

開始準備 `VocabRequest` 機制，將 create、update、delete vocab 呢啲行為包成 request flow，而唔係直接改 vocab data。

比較重要嘅 updated code：

- `dictionary/models.py`：建立 / 調整 `VocabRequest` data structure。
- `dictionary/forms.py`：準備 create、update、delete request forms。
- `dictionary/views.py`：開始處理 vocab request flow。
- `dictionary/urls.py`：加入 request 相關 URL routes。

理由：

學到咩：

## 2026-06-02 - Finish VocabCreateRequestView and improve VocabRequest

Commit: `cdcd761`

完成 `VocabCreateRequestView` 相關處理，改善 `VocabRequest` model/form/view。  
同時 accounts 加入 `last_login` migration，令 user data 記錄更完整。

比較重要嘅 updated code：

- `dictionary/views.py`：完成 `VocabCreateRequestView` 嘅主要 logic。
- `dictionary/forms.py`：改善 create request validation 同 input handling。
- `dictionary/models.py`：改善 `VocabRequest` fields 同 model relationship。
- `dictionary/migrations/0004_improve_vocab_request.py`：套用 request model schema change。
- `accounts/models.py`：加入 / 修正 `last_login` support。

理由：

學到咩：

## 2026-06-04 - Restore vocab request flow and split dictionary views

Commit: `bc37573`

加入 restore vocab request flow，修正 model field name。  
同時將原本單一 `dictionary/views.py` 拆成 `dictionary/views/request.py` 同 `dictionary/views/vocab.py`，令 request logic 同 vocab page logic 分開管理。

比較重要嘅 updated code：

- `dictionary/views/request.py`：集中處理 vocab request / restore flow。
- `dictionary/views/vocab.py`：集中處理一般 vocab pages。
- `dictionary/urls.py`：配合 views 拆分更新 routes。
- `dictionary/models.py`、`dictionary/forms.py`：修正 field name 同相關 form handling。
- `dictionary/migrations/0005_correct_field_name.py`：套用 field rename。

理由：

學到咩：

## 2026-06-06 - Vocab update flow and basic vocab templates

Commit: `259ce8e`

建立 vocab update flow，移除 `Vocab` 入面唔需要嘅 field。  
同時加咗 vocab create/delete/detail/edit/home/list templates，令 vocab CRUD 頁面開始完整成形。

比較重要嘅 updated code：

- `dictionary/views/vocab.py`：加入 vocab update 同其他 CRUD page logic。
- `dictionary/views/request.py`：配合 update request flow。
- `dictionary/forms.py`、`dictionary/models.py`：調整 update fields 同移除冇用 field。
- `dictionary/templates/dictionary/`：加入 create、delete、detail、edit、home、list pages。

理由：

學到咩：

## 2026-06-07 - Vocab list flow, page detail, login/register check

Commit: `0280a4d`

改善 vocab list flow，同 detail page / template 呈現。  
檢查 user register 同 login flow，亦將 `vocab_edit.html` rename 做 `vocab_update.html`，令命名同 update 行為更加一致。

比較重要嘅 updated code：

- `dictionary/views/vocab.py`：改善 vocab list / detail / update flow。
- `dictionary/views/request.py`：改善 request handling。
- `dictionary/templates/dictionary/`：補完整各 vocab pages 嘅 HTML。
- `dictionary/templates/dictionary/vocab_update.html`：由 `vocab_edit.html` rename，統一 naming。
- `accounts/templates/accounts/`：檢查同調整 login / register pages。
- `core/templates/core/index.html`：加入 core index page。

理由：

學到咩：

## 2026-06-09 - HTML fixes and user vocab list

Commit: `99e7214`

修正 typo 同 HTML 細節，加入 `user_vocab_list.html`。  
同時調整 `VocabRequest` nullable 設定，令 request data 喺唔同狀態下可以更穩定咁保存。

比較重要嘅 updated code：

- `dictionary/templates/dictionary/user_vocab_list.html`：加入 user 自己嘅 vocab list page。
- `dictionary/views/vocab.py`：加入 user vocab list 同相關 page handling。
- `dictionary/views/request.py`、`dictionary/forms.py`：改善 request flow 同 validation。
- `dictionary/models.py`：調整 `VocabRequest` nullable fields。
- `dictionary/migrations/0007_set_vocab_request_null_ok.py`：套用 nullable schema change。

理由：

學到咩：

## 2026-06-10 - URL cleanup, temp HTML, table rename, create/delete request flow

Commit: `144c719`

整理 URL routing，同時加咗 temporary version HTML。  
將 vocab request table rename，並完成 create/delete vocab request flow，令 user 對 vocab 嘅新增同刪除可以透過 request 機制處理。

比較重要嘅 updated code：

- `dictionary/views/request.py`：完成 create / delete vocab request flow。
- `dictionary/views/vocab.py`：配合 request flow 更新 vocab pages。
- `dictionary/urls.py`：整理 dictionary routes。
- `accounts/urls.py`、`accounts/views.py`：整理 account routing 同 page flow。
- `dictionary/migrations/0008_rename_table_vocab_request.py`：rename vocab request database table。

理由：

學到咩：

## 2026-06-12 - Admin page preparation and similar_kanji role change

Commit: `d16bdd6`

開始準備 admin page，調整 accounts/core/dictionary admin 設定。  
加入 `import_vocab` management command 基礎，並改動 `similar_kanji` field 嘅 role / structure。

比較重要嘅 updated code：

- `dictionary/admin.py`：開始建立 dictionary admin management UI。
- `accounts/admin.py`、`core/admin.py`：調整其他 apps 嘅 admin registration / display。
- `dictionary/management/commands/import_vocab.py`：加入 vocab CSV import command 基礎。
- `dictionary/models.py`、`dictionary/forms.py`：改動 `similar_kanji` field 同相關 input handling。
- `dictionary/migrations/0009_similar_kanji_field_change.py`：套用 `similar_kanji` schema change。

理由：

學到咩：

## 2026-06-14 - CSV import/export and admin setting

Commit: `80c655f`

準備從 CSV import vocab，同時加入 export vocab to CSV command。  
調整 admin page、accounts model/admin、dictionary model/form，並加咗 verbose name 相關 migration，令 admin 顯示同資料匯入匯出更易用。

比較重要嘅 updated code：

- `dictionary/management/commands/import_vocab.py`：完善 vocab CSV import。
- `dictionary/management/commands/export_vocab_to_csv.py`：加入 vocab CSV export。
- `dictionary/admin.py`：改善 dictionary admin settings 同 display。
- `dictionary/models.py`、`dictionary/forms.py`：整理 fields、labels 同 form handling。
- `dictionary/migrations/0012_add_verbose_name.py`：加入 model / field verbose names。
- `accounts/admin.py`、`accounts/models.py`：同步調整 account admin 同 model。

理由：

學到咩：

## 2026-06-15 - VocabRequest review flow in admin

Commit: `244c793`

修 bug 同改善 dictionary admin page，完成 `VocabRequest` review flow。  
將 request 相關 logic 移去 `dictionary/service/vocab_request.py`，新增 admin custom change form template，並清理舊有 `dictionary/views/request.py`。

比較重要嘅 updated code：

- `dictionary/service/vocab_request.py`：抽出 vocab request business logic 做 service。
- `dictionary/admin.py`：加入 admin approve / reject review handling。
- `dictionary/templates/admin/dictionary/vocabrequest/change_form.html`：加入 custom review actions UI。
- `dictionary/forms.py`、`dictionary/models.py`：配合 review workflow 更新 form 同 status data。
- `dictionary/views.py`、`dictionary/urls.py`：整理一般 vocab views 同 routes。
- `dictionary/views/request.py`：刪除舊 request view module，將 responsibility 搬去 service / admin。

理由：

學到咩：

## 2026-06-17 - Safer vocab request create flow and more vocab categories

Commit: `d65b3df`

將 vocab request create flow 改到更安全，加入更多 vocab category。  
同時加咗 `VocabRequest` unique setting migration，更新 `dictionary/models.py` 同 `dictionary/service/vocab_request.py`，並新增 `TODO.md` 記錄之後要做嘅嘢。

比較重要嘅 updated code：

- `dictionary/service/vocab_request.py`：改善 request creation safety 同 transaction handling。
- `dictionary/models.py`：加入更多 vocab categories 同 duplicate pending request protection。
- `dictionary/migrations/0013_vocabrequest_unique_setting.py`：加入 `VocabRequest` unique constraint。
- `TODO.md`：記低未完成 workflow、風險同之後要改善嘅項目。

理由：

學到咩：

## 2026-06-18 - Project documentation and development tracking

Commit: `1167023`

整理 project development records，同時重整 TODO tracking，將已發現嘅 bug、logic risk、未完成功能同之後想研究嘅方向分開記錄。

比較重要嘅 updated code：

- `PROJECT_HISTORY.md`：整理 project 由初始 setup 到目前為止嘅主要改動。
- `TODO.md`：重整 fix tracking、future features、quiz logic、event system 同 data import/export 規劃。

理由：

學到咩：

## 2026-06-19 - Custom User Admin and learning notes

Commit: `c1979dc`

改善 custom User Admin 架構，開始將 admin add/change user flow 分開處理。  
同時新增 project README 同 learning questions，記錄 password hashing、Django UserAdmin、CBV object ID 傳遞等需要再深入理解嘅概念，並準備 vocab action service。

比較重要嘅 updated code：

- `accounts/admin.py`：改用 Django `UserAdmin`，分開 add form 同 change form 設定。
- `accounts/forms.py`：加入 admin user creation/change forms，保護 password hash。
- `dictionary/service/vocab_action.py`：建立 vocab action service 檔案基礎。
- `LEARNING_QUESTIONS.md`：記錄 Django Custom User Admin 同 CBV object ID 等研究問題。
- `README.md`：整理 project 介紹、目前功能、架構同開發方向。
- `PROJECT_HISTORY.md`：統一 project history 檔名同內容。
- `TODO.md`：補充 quiz、event、user message 同後續功能規劃。

理由：

學到咩：

## 2026-06-20 - Admin user creation and VocabActionService

Commit: `913e765`

完成較完整嘅 admin user creation form，加入 password validation 同 password hashing。  
Dictionary 方面建立 `VocabActionService`，準備集中處理 vocab create、update、deactivate 同 restore，並調整 vocab detail models 同暫時放寬 `word_slug`。

比較重要嘅 updated code：

- `accounts/forms.py`：加入 `UserCreationAdminForm`、password confirmation、Django password validation 同 `set_password()`。
- `accounts/admin.py`：將 admin Add User flow 接去專用 creation form。
- `dictionary/service/vocab_action.py`：加入 vocab create、update、deactivate、restore actions。
- `dictionary/service/vocab_request.py`：加入由 `VocabRequest` 整理 vocab data 嘅 mapper。
- `dictionary/models.py`：調整 vocab detail structure，暫時將 `word_slug` 設為可空。
- `dictionary/migrations/0014_cut_similar_word.py`：調整 similar word schema。
- `dictionary/migrations/0015_two_vocab_detail_base_normal.py`：調整兩種 vocab detail model。
- `dictionary/migrations/0016_word_slug_able_blank_now.py`：暫時容許 `word_slug` 為空。
- `TODO.md`：記錄之後要實作 slug 產生、同步同舊資料 backfill。

理由：

學到咩：

## 2026-06-20 - Quiz filtering and kana keyboard planning

狀態：未 commit，記錄目前設計決定。

補充 quiz 出題範圍同 UI 規劃。Quiz 將來會按 user 選擇嘅 vocab type、level、category 篩選 question pool；另外計劃喺 quiz answer 畫面提供 50 音 keyboard。

比較重要嘅 updated code：

- `TODO.md`：加入按 `type`、`level`、`category` 篩選 quiz question pool 嘅規劃。
- `TODO.md`：加入只供 quiz 作答使用嘅 50 音假名 keyboard 規劃。
- Filter 後嘅 question pool 會再套用 weighted random、最近題目排除同 overdue weight boost。
- 50 音 keyboard 唔會用喺 vocab search 或 request forms，嗰啲位置繼續使用一般 keyboard。

理由：

學到咩：

# Project History

呢份記錄係用 git commit history 整理返出嚟，主要記低 project 到目前為止每次大改動做過啲乜。

每個記錄下面嘅「理由」留咗空位，方便之後自己補返當時點解咁改。

## 2026-05-20 - Project initial setup

Commit: `ad4deee`

一開始建立 project 基礎結構，準備好主要 apps 同基本 models，令 Japanese Quiz 呢個 project 有第一個可以繼續發展落去嘅 base。

理由：

## 2026-05-20 - First migrate 同 custom user manager

Commit: `adf7f9e`

做咗第一次 migration 之後，加入 user manager 相關設定，開始將 accounts app 嘅 user handling 整得完整啲。

理由：

## 2026-05-25 - Login system

Commit: `be08b3d`

加入 login system，開始有 user login/logout/register 相關 flow，令 project 唔再只係 model level，而係開始有 user 可以實際用嘅入口。

理由：

## 2026-05-29 - User pages, AdminMessage, create vocab flow

Commit: `c67a9d0`

加咗 accounts 相關 templates，例如 user detail、home、login、logout、regist。  
同時加入 `AdminMessage` model，調整 core view/template，dictionary 方面亦開始加入 forms、model field changes，同 create vocab flow 嘅基礎。

理由：

## 2026-06-02 - Prepare VocabRequest create/update/delete

Commit: `e8b7bb8`

開始準備 `VocabRequest` 機制，將 create、update、delete vocab 呢啲行為包成 request flow，而唔係直接改 vocab data。

理由：

## 2026-06-02 - Finish VocabCreateRequestView and improve VocabRequest

Commit: `cdcd761`

完成 `VocabCreateRequestView` 相關處理，改善 `VocabRequest` model/form/view。  
同時 accounts 加入 `last_login` migration，令 user data 記錄更完整。

理由：

## 2026-06-04 - Restore vocab request flow and split dictionary views

Commit: `bc37573`

加入 restore vocab request flow，修正 model field name。  
同時將原本單一 `dictionary/views.py` 拆成 `dictionary/views/request.py` 同 `dictionary/views/vocab.py`，令 request logic 同 vocab page logic 分開管理。

理由：

## 2026-06-06 - Vocab update flow and basic vocab templates

Commit: `259ce8e`

建立 vocab update flow，移除 `Vocab` 入面唔需要嘅 field。  
同時加咗 vocab create/delete/detail/edit/home/list templates，令 vocab CRUD 頁面開始完整成形。

理由：

## 2026-06-07 - Vocab list flow, page detail, login/register check

Commit: `0280a4d`

改善 vocab list flow，同 detail page / template 呈現。  
檢查 user register 同 login flow，亦將 `vocab_edit.html` rename 做 `vocab_update.html`，令命名同 update 行為更加一致。

理由：

## 2026-06-09 - HTML fixes and user vocab list

Commit: `99e7214`

修正 typo 同 HTML 細節，加入 `user_vocab_list.html`。  
同時調整 `VocabRequest` nullable 設定，令 request data 喺唔同狀態下可以更穩定咁保存。

理由：

## 2026-06-10 - URL cleanup, temp HTML, table rename, create/delete request flow

Commit: `144c719`

整理 URL routing，同時加咗 temporary version HTML。  
將 vocab request table rename，並完成 create/delete vocab request flow，令 user 對 vocab 嘅新增同刪除可以透過 request 機制處理。

理由：

## 2026-06-12 - Admin page preparation and similar_kanji role change

Commit: `d16bdd6`

開始準備 admin page，調整 accounts/core/dictionary admin 設定。  
加入 `import_vocab` management command 基礎，並改動 `similar_kanji` field 嘅 role / structure。

理由：

## 2026-06-14 - CSV import/export and admin setting

Commit: `80c655f`

準備從 CSV import vocab，同時加入 export vocab to CSV command。  
調整 admin page、accounts model/admin、dictionary model/form，並加咗 verbose name 相關 migration，令 admin 顯示同資料匯入匯出更易用。

理由：

## 2026-06-15 - VocabRequest review flow in admin

Commit: `244c793`

修 bug 同改善 dictionary admin page，完成 `VocabRequest` review flow。  
將 request 相關 logic 移去 `dictionary/service/vocab_request.py`，新增 admin custom change form template，並清理舊有 `dictionary/views/request.py`。

理由：

## 2026-06-17 - Safer vocab request create flow and more vocab categories

Commit: `d65b3df`

將 vocab request create flow 改到更安全，加入更多 vocab category。  
同時加咗 `VocabRequest` unique setting migration，更新 `dictionary/models.py` 同 `dictionary/service/vocab_request.py`，並新增 `TODO.md` 記錄之後要做嘅嘢。

理由：

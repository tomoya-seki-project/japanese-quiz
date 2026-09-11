# UI 日文化與用字修改實作報告

## 1. 報告範圍

本報告記錄 commit `ee31424`（`feat: localize the user interface in Japanese`）內與 UI 文案、語言顯示及相關程式支援有關的修改。比較基準為上一個 commit `e78408e`。

最終語言規則如下：

- 一般使用者會見到的介面使用日文。
- 使用者與管理員都會見到的共用介面文字使用日文。
- 只有管理員會見到的管理頁面、審批操作及驗證訊息保留英文，並修正文法和用字。
- 資料庫儲存值、URL、表單欄位名稱和答案比較代碼不因翻譯而改變。
- 答案比較表是開發檢查資料，因此保留 `MATCH`、`WRONG`、`DAKUTEN` 等原始代碼。

原始逐項盤點保留在 [ui_text_review_2026-09-05.csv](ui_text_review_2026-09-05.csv)。CSV 的原句和行數是修改前快照；本報告描述最終實作。

## 2. 文案設計原則

### 2.1 用語統一

| 概念 | 最終主要用語 |
|---|---|
| Vocabulary | `単語`、`単語帳`、`マイ単語帳` |
| Notification/Event | `お知らせ` |
| Quiz inclusion | `出題対象` |
| Hint | `ヒント` |
| Correct/incorrect | `正解`／`不正解` |
| Vocabulary request | `追加申請`／`変更申請`／`削除申請`／`復元申請` |
| Reading | 表單使用 `読み方（かな）`，列表表頭使用較短的 `読み方` |
| Pagination | `前へ`／`次へ` |

### 2.2 按鈕縮短

初版把完整操作說明放進按鈕，後來按實際畫面語境縮短。最終採用：

| 初版日文 | 最終文字 |
|---|---|
| `単語の追加を申請する` | `単語の追加`（入口）／`申請`（提交按鈕） |
| `回答する` | `回答` |
| `スキップする` | `スキップ` |
| `すべて既読にする` | `すべて` |
| `選択したお知らせを既読にする` | `既読にする` |
| `すべて出題対象にする` | `すべて` |
| `フィードバックを送信する` | 標題 `フィードバック`、按鈕 `送信` |
| `出題対象を保存する`／`出題設定を保存する` | `保存` |
| `変更を申請する` | `変更申請` |
| `削除を申請する` | `削除申請` |
| `検索する` | `検索` |
| `登録する` | `登録` |
| `単語一覧を見る` | `単語一覧` |
| `単語を選択する` | `単語の選択` |
| `クイズを始める` | `開始` |
| `クイズを終了して結果を見る` | `結果へ` |
| `次の問題へ` | `次へ` |
| `キーボードを表示する` | `キーボード表示` |
| `キーボードを隠す` | `隠す` |
| `クイズ設定に戻る` | `設定に戻る` |
| `マイ単語帳に戻る` | `一覧に戻る` |
| `この単語の削除を申請することを確認しました` | `削除申請を確認しました` |
| `ログイン状態を保持する` | `ログイン状態を保持` |
| `前回の設定を使う` | `前回の設定を使用` |
| `すべての種類`／`すべてのレベル`／`すべてのカテゴリー` | 各篩選欄內統一為 `すべて` |

`結果へ` 實際會結束目前測驗並前往摘要。此處接受不在短按鈕內重複解釋「結束測驗」的取捨。

## 3. 使用者介面文案變更

### 3.1 帳戶

| 修改前 | 修改後 |
|---|---|
| `user detail` | `プロフィール` |
| `My Vocab List` | `マイ単語帳` |
| `user home` | `マイページ` |
| `user login`／`Login` | `ログイン` |
| `user logout` | `ログアウトしました。` |
| `user regist` | `新規登録` |
| `Regist` | `登録` |
| `Username` | `ユーザー名` |
| `Email`／`Email : ` | `メールアドレス` |
| `Password` | `パスワード` |
| `Password(confirm)` | `パスワード（確認用）` |
| `Remember Me` | `ログイン状態を保持` |
| `Password and Password(confirm) have to be the same` | `パスワードが一致しません。` |
| 重複 email 的 Django 預設訊息 | `このメールアドレスはすでに登録されています。` |

管理員建立／修改使用者的表單仍使用英文：

| 修改前 | 修改後 |
|---|---|
| `password` | `Password` |
| `Password(Confirm)` | `Confirm password` |
| `password and password(confirm) have to be the same` | `The passwords do not match.` |
| `Please enter both password` | `Please fill in both password fields.` |

### 3.2 共用導覽及首頁

| 修改前 | 修改後 |
|---|---|
| `home` | `ホーム` |
| `profile` | `プロフィール` |
| `Event` | `お知らせ` |
| `vocab` | `単語帳` |
| `logout` | `ログアウト` |
| 註冊入口誤寫 `sign in` | `登録` |
| `login` | `ログイン` |
| `feedback` | `フィードバック` |
| `Welcome back to the project!` | `日本語クイズへようこそ！` |
| `Quiz` | `クイズ` |
| `Create Vocab` | `単語の追加` |
| `temptemptemptemp` | `このページは準備中です。` |

管理員有待回覆數量時顯示 `Feedback (n)`；這部分是管理員專用提示，因此保留英文。其餘共用導覽即使由管理員查看，仍顯示日文。

### 3.3 お知らせ

| 修改前 | 修改後 |
|---|---|
| `user event list` | `お知らせ` |
| `no unread event` | `未読のお知らせはありません。` |
| `All` | `すべて` |
| `Unread` | `未読` |
| `read` | `既読` |
| `Type` | `種類` |
| `Title` | `件名` |
| `Confirm` | `既読にする` |
| `Prev`／`Next` | `前へ`／`次へ` |
| 詳情頁誤用 `vocab detail` | `お知らせの詳細` |

通知類型不再顯示 `vocab_request_result` 等儲存代碼，改由 template filter 顯示可讀標籤：

| 儲存值 | 顯示文字 |
|---|---|
| `vocab_request_result` | `単語申請の審査結果` |
| `new_vocab_request` | `New vocabulary request` |
| `vocab` | `単語` |
| `weight_update_by_system` | `出題優先度の自動更新` |
| `feedback_reply` | `フィードバックへの返信` |

`new_vocab_request` 只會發送給管理員，因此保留英文。

同步通知標題改為：

- `前回の単語同期以降に追加された単語：{count}件`
- `前回の単語同期以降に更新された単語：{count}件`
- `前回の単語同期以降に復元された単語：{count}件`
- `前回の単語同期以降に削除された単語：{count}件`

歷史通知不會被批次改寫，只有之後新建立的通知採用新文案。

### 3.4 フィードバック

一般使用者頁面：

| 修改前 | 修改後 |
|---|---|
| `feedback Create` | `フィードバック` |
| `Create` | `送信` |
| `Feedback type` | `種類` |
| `Context` | `内容` |
| `There is a same feedback pending for admin checking` | `同じ内容のフィードバックはすでに送信されています。管理者の確認をお待ちください。` |
| `Same feedback` | `このフィードバックは送信済みです。管理者の確認をお待ちください。` |
| `Thank you for your feedback!` | `フィードバックをお寄せいただき、ありがとうございます。` |

共用回饋類型：

| 儲存值 | 顯示文字 |
|---|---|
| `vocab_suggestion` | `単語に関する提案` |
| `bulk_vocab_request` | `単語の一括追加申請` |
| `bug_report` | `不具合の報告` |
| `feature_request` | `機能の追加・改善要望` |
| `others` | `その他` |

管理員專用回饋頁保留英文並修正標題和欄名：

| 修改前 | 修改後 |
|---|---|
| 詳情頁誤用 `vocab detail` | `Feedback details` |
| `feedback list` | `Feedback` |
| 回覆頁誤用 `feedback Create` | `Reply to feedback` |
| `user` | `User` |
| `context` | `Message` |
| `check it` | `Details` |
| `Detail` | `View details` |
| `Prev` | `Previous` |
| `feedback id : {id} has been replied` | `Your reply to feedback #{id} has been sent.` |

### 3.5 単語帳與申請

表單欄位：

| 修改前 | 修改後 |
|---|---|
| `type`／`Type` | `種類` |
| `Word` | `単語` |
| `Meaning` | `意味` |
| `Kana` | `読み方（かな）` |
| 自動產生的 `Level` | `JLPTレベル` |
| 自動產生的 `Categories` | `カテゴリー` |
| `Native japanese` | `対応する日本語表現` |
| `No Matter` | `すべて` |
| `Yes`／`No` | `はい`／`いいえ` |
| `In use` | `出題対象` |
| 篩選空選項 `-----` | `すべて` |

共用單語 choices：

| 儲存值 | 修改前 | 修改後 |
|---|---|---|
| `vocab` | `Vocab` | `一般語彙` |
| `katakana` | `Katakana` | `カタカナ語` |
| `0` | `未定義` | `未設定` |
| `1`–`5` | `N1`–`N5` | 保持不變 |

表單驗證及操作訊息：

| 修改前 | 修改後 |
|---|---|
| `vocab type unsupported` | `この単語の種類には対応していません。` |
| `You can select up to 3 categories only.` | `カテゴリーは3つまで選択できます。` |
| `The same word already exists on the active list.` | `同じ単語と読み方の有効な項目がすでに登録されています。` |
| `Target vocab is missing` | `更新対象の単語が見つかりません。` |
| 已停用的重複單語英文訊息 | `同じ単語と読み方の無効な項目がすでに登録されています。` |
| `Please confirm the action` | `この単語の削除を申請する場合は、確認欄にチェックを入れてください。` |
| pending request 英文訊息 | `この単語には、すでに審査待ちの申請があります。` |
| 新增申請成功訊息 | `単語の追加申請を送信しました。管理者の審査をお待ちください。` |
| 復元申請成功訊息 | `同じ単語と読み方の無効な項目がすでに登録されています。復元申請を送信しました。管理者の審査をお待ちください。` |
| 重複申請訊息 | `この単語と読み方については、すでに申請があり、管理者の審査待ちです。` |

主要頁面及操作：

| 修改前 | 修改後 |
|---|---|
| `vocab home`／`vocab list` | `単語帳` |
| `user vocab list` | `マイ単語帳` |
| `vocab detail` | `単語の詳細` |
| `user vocab detail` | `マイ単語帳の詳細` |
| `vocab create` | `単語の追加` |
| `vocab update` | `単語の変更申請` |
| `vocab delete` | `単語の削除申請` |
| `List` | `単語一覧` |
| `Create` | `単語の追加` |
| `MyList` | `マイ単語帳` |
| `confirm`（搜尋） | `検索` |
| `create`（提交申請） | `申請` |
| `更新`／更新入口 | `変更申請` |
| `del`／刪除入口 | `削除申請` |
| `last page` | `一覧に戻る` |
| `Update`／`Update InUse` | `保存` |

個人單語詳情標籤：

| 修改前 | 修改後 |
|---|---|
| `in use` | `出題対象` |
| `weight` | `出題優先度` |
| `correct count` | `正解数` |
| `incorrect count` | `不正解数` |
| `streak` | `連続正解・不正解数` |
| `last quit at` | `最終出題日時` |
| `last answer` | `前回の回答` |
| `None` | `回答履歴はありません。` |
| `vocab section` | `単語の詳細` |
| `level` | `JLPTレベル` |
| `categories` | `カテゴリー` |

`streak` 額外加入說明：`正の数は連続正解、負の数は連続不正解を表します。`。最後出題時間沒有值時顯示 `未出題`。分類改用 `Category.__str__()`，顯示日文 `display`，不再外露 `daily_life` 等內部名稱。

### 3.6 クイズ

設定和狀態：

| 修改前 | 修改後 |
|---|---|
| `Quiz Home`／`Quiz` | `クイズ` |
| `Quiz Settings` | `クイズ設定` |
| `Start Quiz`／`Start` | `開始` |
| `Quiz num` | `問題数` |
| `No Limit` | `無制限` |
| `Type` | `種類` |
| `Level` | `JLPTレベル` |
| `Categories` | `カテゴリー` |
| `Use last setting` | `前回の設定を使用` |
| `No previous quiz settings were found.` | `前回のクイズ設定が見つかりません。` |

答題操作：

| 修改前 | 修改後 |
|---|---|
| `Tip` | `ヒント` |
| `Enter` | `回答` |
| `Skip` | `スキップ` |
| `Summary` | `結果へ` |
| `Next` | `次へ` |
| `Show Keyboard` | `キーボード表示` |
| `Hide` | `隠す` |
| `BS` | `1文字削除` |
| `Back to Settings` | `設定に戻る` |
| `Correct`／`Wrong` | `正解`／`不正解` |
| `Back to Home` | `ホームに戻る` |
| `No questions are available.` | `出題できる問題がありません。` |

題數顯示由 `current/total問` 改為 `第{current}問／全{total}問`；無上限模式維持 `第{current}問`。

摘要改為：

- 標題：`クイズ結果`
- `回答・スキップした問題数：{total}問`
- `正解数`
- `不正解数`
- `スキップ数`
- `ヒント使用回数`

其他使用者訊息：

- 篩選無結果：`条件に一致する単語がありません。今回は、出題対象に設定したすべての単語から出題します。`
- 出題數不足：`クイズを始めるには、出題対象の単語が{min_count}語以上必要です。マイ単語帳で出題対象を追加してください。`
- 沒有可出題單語：`出題できる単語がありません。マイ単語帳で単語を出題対象に設定してください。`
- 尚有未回答問題：`まだ回答していない問題があります。`
- AJAX 錯誤：`エラーが発生しました。ページを再読み込みして、もう一度お試しください。`
- AJAX 欄位名稱：`回答`、`ヒント使用回数`、`問題`

### 3.7 錯誤頁

原本 400、403、404、500 頁只顯示狀態碼，現在加入完整 HTML、`lang`、標題及說明：

| 狀態 | 日文訊息 |
|---|---|
| 400 | `リクエストを処理できません。内容を確認して、もう一度お試しください。` |
| 403 | `このページを表示する権限がありません。` |
| 404 | `ページが見つかりません。URLを確認してください。` |
| 500 | `エラーが発生しました。しばらくしてから、もう一度お試しください。` |

錯誤頁亦保留英文分支，讓管理員英文介面可顯示相應英文訊息。

## 4. 管理員英文修正

管理員專用文案沒有改成日文，只修正文法、拼字和清晰度：

| 修改前 | 修改後 |
|---|---|
| `User Info` | `User information` |
| `Premission` | `Permissions` |
| `Last Vocab Sync At` | `Last vocabulary sync` |
| `There are not syncing record yet!` | `No vocabulary sync has been recorded yet.` |
| `User Vocab Count` | `Vocabulary count` |
| `View user vocab` | `View user vocabulary` |
| `Native Japanese` | `Japanese equivalent` |
| `Reviewed request cannot be changed` | `A request cannot be changed after it has been reviewed.` |
| `Vocab request approved by {user}` | `Vocabulary request approved by {user}.` |
| `Vocab request rejected by {user}` | `Vocabulary request rejected by {user}.` |
| 已被審查時仍顯示本次 user reviewed | `This request has already been reviewed. No changes were made.` |
| `Vocab type is required.` | `Vocabulary type is required.` |
| `Category is required.` | `Select at least one category.` |
| `Native Japanese is required for Katakana` | `A Japanese equivalent is required for katakana words.` |
| active/inactive original vocab 訊息 | 改用完整的 `original vocabulary entry` 句子 |

管理員新申請通知改為：

- 標題：`A new vocabulary request has been submitted: {Creation|Update|Deletion|Restoration}.`
- 內容：`{word} ({kana}) was requested by {request_by}.`

申請人收到的審批結果則使用日文：

- `単語の{追加|変更|削除|復元}申請が{reviewed_by}さんに承認されました。`
- `単語の{追加|変更|削除|復元}申請が{reviewed_by}さんに却下されました。`

## 5. 程式碼變更

### 5.1 介面語言 middleware

新增 `core.middleware.InterfaceLanguageMiddleware`，並加入 `MIDDLEWARE`：

- 一般使用者頁面使用 `ja`。
- Django admin 及 `feedback_list`、`feedback_detail`、`feedback_reply` 使用 `en-us`。
- 語言按頁面決定，不按登入者是否 `is_staff` 決定；管理員打開一般使用者頁面時仍顯示日文。
- 使用 `translation.override()` 將語言限制在單一 request 內，防止語言狀態污染下一個 request。
- 如 response 尚未 render，會在語言 context 內完成 render，確保延遲渲染表單使用正確語言。
- 設定 `request.LANGUAGE_CODE` 和 `Content-Language` response header。
- `LANGUAGE_CODE` 預設仍為 `en-us`，沒有把全站設定硬改成日文。

### 5.2 UI 顯示字典

新增 `core/ui.py`，集中保存：

- `VOCAB_TYPES`
- `VOCAB_LEVELS`
- `FEEDBACK_TYPES`
- `EVENT_TYPES`
- `REQUEST_TYPES_JA`
- `REQUEST_TYPES_EN`

用途是將穩定的內部值映射成人類可讀文字。例如資料庫仍保存 `create`，顯示時可按對象用 `追加` 或 `Creation`。

### 5.3 Template filters

新增 `core/templatetags/ui_labels.py`：

- `event_label`：通知類型代碼轉顯示文字。
- `vocab_type_label`：`vocab`／`katakana` 轉日文標籤。
- `vocab_level_label`：`0`–`5` 轉 `未設定`／`N1`–`N5`。
- `kana_key_label`：鍵盤事件值 `"`／`。` 顯示為濁點 `゛`／半濁點 `゜`。

`kana_key_label` 只改按鍵畫面，`data-kana` 仍保留原值，所以既有 JavaScript 輸入邏輯不需要更改。

曾加入的 `answer_result_label` 已刪除。答案逐字比較資料是開發用途，翻成日文反而妨礙檢查。

### 5.4 開發用答案結果表

`quiz_result_partial.html` 原本用一行顯示：

```text
type correct answer sub_type
```

現在改成 Bootstrap table，欄位為：

| type | correct | user | sub_stype |
|---|---|---|---|
| `item.type` | `item.correct` | `item.answer` | `item.sub_type` |

欄名 `sub_stype` 按使用者指定保留。資料值維持原始英文代碼，Django template 自動 escape 使用者答案。

### 5.5 Model choices 和 verbose_name

Model choices 的儲存值沒有改，只改顯示 label。另改善管理員欄位名稱：

- 時間欄：`Created at`、`Updated at`
- Event：`Notification type`
- Category：`Display name`
- Vocab：`Active`、`JLPT level`
- UserVocab：`Include in quizzes`、`Selection weight`、`Correct answers`、`Incorrect answers`、`Answer streak`、`Last practiced`、`Last answer`
- VocabRequest：`Request type`、`Created by`、`Reviewed by`、`Original vocabulary entry`、`Proposed categories`、`Japanese equivalent`、`Previous data`

這些屬 Django model state 變更，因此產生 migration；資料欄型和實際資料值沒有改。

### 5.6 顯示資料方式

- 通知 template 使用 `event_label`，不直接顯示事件代碼。
- 個人單語詳情使用 `vocab_level_label` 和 `vocab_type_label`。
- Category 顯示改用 model 的 `__str__()`，優先使用日文 `display`。
- `last_quiz_at` 為 `None` 時顯示 `未出題`。
- 摘要完成題數由 `correct_count + wrong_count + skipped_count` 計算。

## 6. Migration 與資料庫操作

新增五個 migration：

| App | Migration | 作用 |
|---|---|---|
| accounts | `0006_improve_ui_labels` | UserProfile 時間欄位的英文 `verbose_name` |
| core | `0008_improve_ui_labels` | Event／Feedback 欄位名稱及第一版英文 choices |
| core | `0009_shared_japanese_labels` | 將使用者與管理員共用 choices 改為日文 |
| dictionary | `0029_improve_ui_labels` | 單語相關管理員欄位名稱及第一版 choices |
| dictionary | `0030_shared_japanese_labels` | 將共用單語種類和等級 choices 改為日文 |

之所以有 `0008 → 0009` 和 `0029 → 0030` 兩段，是因為需求中途由「管理員英文、使用者日文」補充為「使用者與管理員都見到的共用文字用日文」。migration 保留完整演進順序。

本地資料庫操作紀錄：

1. 首輪執行 `migrate`，套用 `accounts.0006`、`core.0008`、`dictionary.0029`。
2. 共用文案規則更新後，再套用 `core.0009`、`dictionary.0030`。
3. 最後一次執行 `migrate --noinput` 顯示 `No migrations to apply`。
4. `makemigrations --check --dry-run` 顯示 `No changes detected`。

這些 migration 只更新 Django model state／choice 顯示文字，沒有資料搬移、刪除或批次改寫歷史內容。

## 7. 測試變更

`core/tests.py` 新增 10 個測試，覆蓋以下內容：

1. 所有專案 template 可以成功編譯。
2. 假名鍵盤顯示 `゛`／`゜`，但 `data-kana` 事件值維持原值。
3. 共用 vocab、level、feedback choices 顯示日文。
4. 管理員專用表單欄名維持英文。
5. 開發答案結果保留 `WRONG`、`DAKUTEN` 等原始代碼。
6. 使用者答案會 HTML escape，避免直接輸出 `<script>`。
7. 一般頁面和 admin 頁面的語言不會跨 request 污染。
8. Django 內建 required validation 在使用者頁顯示日文、admin 顯示英文。
9. 管理員打開一般使用者頁面時仍採日文；管理員專用 feedback 頁採英文。
10. 管理員新申請通知為英文，申請人審批結果通知為日文。
11. 單語詳情顯示 N1、一般語彙和日文分類，不外露內部 category code。

上列部分行為合併在同一個 test method，實際 test runner 顯示共 10 tests。

最後驗證結果：

- 全部 10 個 Django tests：通過。
- 其後文案縮短及開發表格調整所跑的 4 個 template tests：通過。
- `manage.py check`：通過，0 issues。
- `makemigrations --check --dry-run`：`No changes detected`。
- `git diff --check`：通過。

測試使用 Django 獨立測試資料庫，完成後自動刪除；它與本地 `migrate` 操作不同。

## 8. 未改動的內容與限制

- 沒有改 database choice 的儲存值，例如 `vocab`、`katakana`、`create`、`delete`。
- 沒有改 URL name、form field name、session key 或 quiz 判分邏輯。
- 沒有翻譯日文學習資料 CSV 內的單語、讀音和意思。
- 沒有批次改寫資料庫中既有通知、使用者回饋或管理員回覆。
- 開發用答案比較內容保留英文代碼。
- 本輪主要以原始碼及 Django tests 驗證，沒有完成瀏覽器逐頁視覺驗收。
- `ui_text_review` CSV 保留修改前來源位置；程式修改後部分行數已移動。

## 9. 主要修改檔案

| 類別 | 檔案 |
|---|---|
| 語言分流 | `core/middleware.py`、`config/settings.py` |
| 顯示文字映射 | `core/ui.py` |
| Template filters | `core/templatetags/ui_labels.py` |
| 帳戶 UI | `accounts/forms.py`、`accounts/templates/accounts/` |
| 通知／回饋 UI | `core/forms.py`、`core/models.py`、`core/views.py`、`core/service/`、`core/templates/core/` |
| 單語 UI | `dictionary/forms.py`、`dictionary/models.py`、`dictionary/views.py`、`dictionary/service/vocab_request.py`、`dictionary/templates/` |
| Quiz UI | `quiz/forms.py`、`quiz/helper.py`、`quiz/views.py`、`quiz/templates/`、`static/js/quiz/quiz_play.js` |
| 錯誤頁 | `errorHandler/templates/errorHandler/` |
| Migration | `accounts/migrations/0006_*`、`core/migrations/0008_*`、`core/migrations/0009_*`、`dictionary/migrations/0029_*`、`dictionary/migrations/0030_*` |
| 測試 | `core/tests.py` |

## 10. 程式碼修改 Before／After

本節集中記錄實際 coding 改法。純文字替換已在第 3、4 節完整列出；這裏說明文字以外的程式結構、資料流和模板寫法。

### 10.1 在 Django middleware 啟用介面語言分流

檔案：`config/settings.py`

修改前沒有自訂語言 middleware：

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
]
```

修改後在 session middleware 之後加入：

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "core.middleware.InterfaceLanguageMiddleware",
    "django.middleware.common.CommonMiddleware",
]
```

新增檔案：`core/middleware.py`

```python
from django.urls import Resolver404, resolve, reverse
from django.utils import translation


class InterfaceLanguageMiddleware:
    admin_views = {
        "core:feedback_list",
        "core:feedback_detail",
        "core:feedback_reply",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = "ja"
        try:
            match = resolve(request.path_info)
        except Resolver404:
            match = None

        if request.path_info.startswith(reverse("admin:index")) or (
            match and match.view_name in self.admin_views
        ):
            language = "en-us"

        request.LANGUAGE_CODE = language
        with translation.override(language):
            response = self.get_response(request)
            if hasattr(response, "render") and not response.is_rendered:
                response.render()
            response.setdefault("Content-Language", language)
            return response
```

流程如下：

```text
request
  ├─ /admin/ 或管理員專用 feedback view → en-us
  └─ 其他頁面                         → ja
        ↓
translation.override(language)
        ↓
在相同語言 context 內建立及 render response
        ↓
加入 Content-Language header
        ↓
離開 context，自動還原先前語言
```

這個設計避免用 `request.user.is_staff` 判斷語言。管理員打開 quiz、單語帳等共用頁面時仍然看到日文；只有管理員專用頁面才使用英文。

### 10.2 將顯示標籤集中到 `core/ui.py`

修改前，顯示文字分散在 model choices、template 及 service 的 f-string 中，部分畫面直接顯示 `vocab_request_result`、`create` 等內部值。

修改後新增集中 mapping：

```python
VOCAB_TYPES = {
    "vocab": "一般語彙",
    "katakana": "カタカナ語",
}

VOCAB_LEVELS = {
    "0": "未設定",
    "1": "N1",
    "2": "N2",
    "3": "N3",
    "4": "N4",
    "5": "N5",
}

EVENT_TYPES = {
    "vocab_request_result": "単語申請の審査結果",
    "new_vocab_request": "New vocabulary request",
    "vocab": "単語",
    "weight_update_by_system": "出題優先度の自動更新",
    "feedback_reply": "フィードバックへの返信",
}

REQUEST_TYPES_JA = {
    "create": "追加",
    "update": "変更",
    "delete": "削除",
    "restore": "復元",
}

REQUEST_TYPES_EN = {
    "create": "Creation",
    "update": "Update",
    "delete": "Deletion",
    "restore": "Restoration",
}
```

關鍵點是 dictionary key 沒有改。`create`、`vocab`、`0` 仍是程式和資料庫使用的值，只有右邊顯示文字改變。

### 10.3 以 template filters 隔開內部值與畫面文字

新增檔案：`core/templatetags/ui_labels.py`

```python
@register.filter
def event_label(value):
    return EVENT_TYPES.get(value, "お知らせ")


@register.filter
def vocab_type_label(value):
    return VOCAB_TYPES.get(value, "その他")


@register.filter
def vocab_level_label(value):
    return VOCAB_LEVELS.get(str(value), "未設定")


@register.filter
def kana_key_label(value):
    return {'"': '゛', '。': '゜'}.get(value, value)
```

通知類型修改前：

```django
<td>{{ user_event.event.event_type }}</td>
```

會直接顯示：

```text
vocab_request_result
```

修改後：

```django
{% load ui_labels %}
<td>{{ user_event.event.event_type|event_label }}</td>
```

顯示：

```text
単語申請の審査結果
```

單語詳情修改前：

```django
<div>level : {{ user_vocab.vocab.level }}</div>
<div>type : {{ user_vocab.vocab.type }}</div>
```

修改後：

```django
{% load ui_labels %}
<div>JLPTレベル： {{ user_vocab.vocab.level|vocab_level_label }}</div>
<div>種類： {{ user_vocab.vocab.type|vocab_type_label }}</div>
```

這樣資料庫可以繼續保存 `1`、`vocab`，畫面顯示 `N1`、`一般語彙`。

### 10.4 假名鍵盤只改 label，不改事件值

檔案：`quiz/templates/quiz/partials/quiz_input_panel_partial.html`

修改前：

```django
<button type="button" class="kana-key" data-kana="{{ kana }}">
    {{ kana }}
</button>
```

特殊按鍵以 `"` 和 `。` 顯示，使用者不容易知道它們代表濁點和半濁點。

修改後：

```django
{% load ui_labels %}
<button type="button" class="kana-key" data-kana="{{ kana }}">
    {{ kana|kana_key_label }}
</button>
```

輸出例子：

```html
<button data-kana="&quot;">゛</button>
<button data-kana="。">゜</button>
```

畫面顯示 `゛`／`゜`，JavaScript 收到的值仍是 `"`／`。`，因此 `handleDakuten()` 和 `handleHandakuten()` 不需要改。

### 10.5 Forms：加入明確 label、選項和驗證訊息

檔案：`dictionary/forms.py`

修改前依賴 Django 從 field name 自動產生英文 label：

```python
level = forms.ChoiceField(choices=VocabLevel.choices)
categories = forms.ModelMultipleChoiceField(
    queryset=Category.objects.all(),
    required=False,
)
native_japanese = forms.CharField(max_length=255, required=False)
```

修改後明確指定日文：

```python
level = forms.ChoiceField(
    label="JLPTレベル",
    choices=VocabLevel.choices,
)
categories = forms.ModelMultipleChoiceField(
    label="カテゴリー",
    queryset=Category.objects.all(),
    required=False,
)
native_japanese = forms.CharField(
    label="対応する日本語表現",
    max_length=255,
    required=False,
)
```

搜尋表單修改前：

```python
choices=[("", "-----")] + list(VocabType.choices)
empty_label="-----"
```

修改後：

```python
choices=[("", "すべて")] + VocabType.choices
empty_label="すべて"
```

`UserVocabInUse` 修改前：

```python
choices = [
    (NO_MATTER, "No Matter"),
    (YES, "Yes"),
    (NO, "No"),
]
```

修改後：

```python
choices = [
    (NO_MATTER, "すべて"),
    (YES, "はい"),
    (NO, "いいえ"),
]
```

刪除確認修改前：

```python
confirm = forms.BooleanField(required=False)

if confirm == False:
    raise ValidationError("Please confirm the action")
```

修改後：

```python
confirm = forms.BooleanField(
    label="削除申請を確認しました",
    required=False,
)

if confirm == False:
    raise ValidationError(
        "この単語の削除を申請する場合は、確認欄にチェックを入れてください。"
    )
```

檔案：`accounts/forms.py`

使用者註冊表單由英文 labels 改成日文，並為 email unique error 加入自訂日文：

```python
class Meta:
    labels = {
        "username": "ユーザー名",
        "email": "メールアドレス",
        "password": "パスワード",
    }
    error_messages = {
        "email": {
            "unique": "このメールアドレスはすでに登録されています。",
        },
    }
```

同一檔案內的 `UserCreationAdminForm` 保留英文，修正文法：

```python
password2 = forms.CharField(
    label="Confirm password",
    widget=forms.PasswordInput(),
)

self.add_error("password2", "The passwords do not match.")
self.add_error(None, "Please fill in both password fields.")
```

檔案：`core/forms.py`

一般使用者回饋表單：

```python
feedback_type = forms.ChoiceField(
    label="種類",
    choices=FeedbackType.choices,
)
context = forms.CharField(
    label="内容",
    max_length=255,
    widget=forms.Textarea,
)
```

管理員回覆表單則維持英文：

```python
context = forms.CharField(
    label="Message",
    max_length=255,
    widget=forms.Textarea,
)
```

### 10.6 Models：只改 choices label 和 `verbose_name`

檔案：`dictionary/models.py`

修改前：

```python
class VocabType(models.TextChoices):
    VOCAB = "vocab", "Vocab"
    KATAKANA = "katakana", "Katakana"

class VocabLevel(models.TextChoices):
    JLPT_N0 = "0", "未定義"
```

修改後：

```python
class VocabType(models.TextChoices):
    VOCAB = "vocab", "一般語彙"
    KATAKANA = "katakana", "カタカナ語"

class VocabLevel(models.TextChoices):
    JLPT_N0 = "0", "未設定"
```

左邊第一個值完全不變，所以資料庫仍保存 `vocab`、`katakana` 和 `0`。

管理員欄位修改例子：

```python
in_use = models.BooleanField(
    verbose_name="Include in quizzes",
    default=True,
)
weight = models.IntegerField(
    verbose_name="Selection weight",
    default=50,
)
last_quiz_at = models.DateTimeField(
    verbose_name="Last practiced",
    blank=True,
    null=True,
)
```

檔案：`core/models.py`

修改前：

```python
class EventType(models.TextChoices):
    VOCAB_REQUEST_RESULT = "vocab_request_result", "Vocab Request Result"
    NEW_VOCAB_REQUEST = "new_vocab_request", "New Vocab Request Result"
```

修改後：

```python
class EventType(models.TextChoices):
    VOCAB_REQUEST_RESULT = "vocab_request_result", "単語申請の審査結果"
    NEW_VOCAB_REQUEST = "new_vocab_request", "New vocabulary request"
```

`NEW_VOCAB_REQUEST` 只供管理員查看，因此使用修正後英文。其他共用 event choices 使用日文。

### 10.7 Services：按通知接收者選擇語言

檔案：`dictionary/service/vocab_request.py`

管理員收到的新申請通知修改前：

```python
event_title = f"A new vocab {request_type} request has been submitted."
```

修改後：

```python
event_title = (
    "A new vocabulary request has been submitted: "
    f"{REQUEST_TYPES_EN[request_type]}."
)
```

例如 `request_type == "delete"` 時顯示：

```text
A new vocabulary request has been submitted: Deletion.
```

申請人收到審批結果，修改前直接插入內部值：

```python
event_title = (
    f"Your {locked_request.request_type} vocab request "
    f"has been approved by {reviewed_by}"
)
```

修改後先映射成日文：

```python
event_title = (
    f"単語の{REQUEST_TYPES_JA[locked_request.request_type]}申請が"
    f"{reviewed_by}さんに承認されました。"
)
```

因此 `delete` 不會直接出現在使用者通知，而會顯示 `削除申請`。

檔案：`core/service/event.py`

同步通知修改前用 `item(s)` 避免處理英文單複數：

```python
event_title = (
    f"There {'is' if count == 1 else 'are'} {count} "
    "new vocab item(s) since your last vocab sync."
)
```

修改後直接使用日文量詞：

```python
event_title = f"前回の単語同期以降に追加された単語：{count}件"
```

更新、復元和削除通知使用相同結構。

### 10.8 Views：將 flash messages 和 form errors 日文化

檔案：`dictionary/views.py`

修改前：

```python
messages.success(
    self.request,
    "A new word request has been sent to admin for confirmation.",
)
```

修改後：

```python
messages.success(
    self.request,
    "単語の追加申請を送信しました。管理者の審査をお待ちください。",
)
```

另一項邏輯修正了原句不可靠的描述：

```python
# 修改前：無法保證一定是另一位使用者提出
"Another user has already requested the same word."

# 修改後：只描述能確定的狀態
"この単語と読み方については、すでに申請があり、管理者の審査待ちです。"
```

檔案：`quiz/views.py`

修改前：

```python
messages.warning(request, "You have a unanswer yet question!")
```

修改後：

```python
messages.warning(request, "まだ回答していない問題があります。")
```

沒有可出題單語時，訊息亦補充實際操作位置：

```python
messages.warning(
    request,
    "出題できる単語がありません。"
    "マイ単語帳で単語を出題対象に設定してください。",
)
```

### 10.9 Templates：由內部式命名改為頁面語境

一般模板修改形式主要是直接替換可見文字，不改 URL、HTTP method、form action 或 template context。

例一，登入頁：

```django
<!-- 修改前 -->
<h1>user login</h1>
<button type="submit">Login</button>

<!-- 修改後 -->
<h1>ログイン</h1>
<button type="submit">ログイン</button>
```

例二，單語詳情操作：

```django
<!-- 修改前 -->
<a href="{% url 'dictionary:vocab_update' vocab_id=vocab.pk %}">更新</a>
<a href="{% url 'dictionary:vocab_delete' vocab_id=vocab.pk %}">del</a>

<!-- 修改後 -->
<a href="{% url 'dictionary:vocab_update' vocab_id=vocab.pk %}">変更申請</a>
<a href="{% url 'dictionary:vocab_delete' vocab_id=vocab.pk %}">削除申請</a>
```

URL name 和參數沒有改，只有 anchor 文字改變。

例三，個人單語詳情的空值：

```django
<!-- 修改前 -->
{{ user_vocab.last_quiz_at }}

<!-- 修改後 -->
{{ user_vocab.last_quiz_at|default_if_none:"未出題" }}
```

例四，分類：

```django
<!-- 修改前：顯示 daily_life 等內部 name -->
{{ category.name }}

<!-- 修改後：呼叫 Category.__str__()，優先顯示日文 display -->
{{ category }}
```

### 10.10 Quiz 結果及開發檢查 table

結果按鈕修改前：

```django
<button type="submit">Summary</button>
<button type="submit">Next</button>
```

曾經翻成較完整的 `クイズを終了して結果を見る`／`次の問題へ`，最後按 UI 長度要求改成：

```django
<button type="submit">結果へ</button>
<button type="submit">次へ</button>
```

開發檢查資料修改前：

```django
{% for item in compared_result %}
    <div>
        {{ item.type }}
        {{ item.correct }}
        {{ item.answer }}
        {{ item.sub_type }}
    </div>
{% endfor %}
```

修改後：

```django
<table class="table table-bordered table-sm">
    <thead>
        <tr>
            <th>type</th>
            <th>correct</th>
            <th>user</th>
            <th>sub_stype</th>
        </tr>
    </thead>
    <tbody>
        {% for item in compared_result %}
            <tr>
                <td>{{ item.type }}</td>
                <td>{{ item.correct }}</td>
                <td>{{ item.answer }}</td>
                <td>{{ item.sub_type }}</td>
            </tr>
        {% endfor %}
    </tbody>
</table>
```

曾經加入 `answer_result_label` 將 `WRONG` 翻成 `不一致`、`DAKUTEN` 翻成 `濁点`。確認這段是開發資料後，已刪除該 filter，恢復顯示原始值。

### 10.11 JavaScript 錯誤顯示

檔案：`static/js/quiz/quiz_play.js`

AJAX 失敗訊息修改前：

```javascript
errorContainer.textContent =
    "系統暫時發生問題，請重新整理頁面再試。";
```

修改後：

```javascript
errorContainer.textContent =
    "エラーが発生しました。ページを再読み込みして、もう一度お試しください。";
```

錯誤欄位名稱修改前：

```javascript
const labels = {
    answer: "答案",
    tips_count: "提示次數",
    user_vocab_id: "Quiz資料",
};
```

修改後：

```javascript
const labels = {
    answer: "回答",
    tips_count: "ヒント使用回数",
    user_vocab_id: "問題",
};
```

fetch、FormData、JSON parsing 和 error rendering 流程沒有改。

### 10.12 錯誤頁由狀態碼改成完整 template

修改前每個檔案只有一個數字：

```html
404
```

修改後的結構：

```django
{% load i18n %}
{% get_current_language as language %}
<!DOCTYPE html>
<html lang="{{ language }}">
<head>
    <meta charset="utf-8">
    <title>404</title>
</head>
<body>
    <p>
        404 —
        {% if language == "en-us" %}
            Page not found. Please check the address.
        {% else %}
            ページが見つかりません。URLを確認してください。
        {% endif %}
    </p>
</body>
</html>
```

400、403、500 使用相同結構及各自訊息。

### 10.13 Migration 實際記錄的 code state

例如 `dictionary.0030_shared_japanese_labels`：

```python
migrations.AlterField(
    model_name="vocab",
    name="type",
    field=models.CharField(
        choices=[
            ("vocab", "一般語彙"),
            ("katakana", "カタカナ語"),
        ],
        max_length=20,
        verbose_name="Type",
    ),
)
```

這類 `AlterField` 主要更新 migration state 和 Django 顯示 label。由於 choice value 和欄位型別不變，沒有重寫原有單語資料。

### 10.14 Tests 如何驗證 code 行為

模板編譯測試：

```python
for app in ("accounts", "core", "dictionary", "quiz", "errorHandler"):
    templates = root / app / "templates"
    for path in templates.rglob("*.html"):
        get_template(str(path.relative_to(templates)))
```

語言 request 隔離測試：

```python
with translation.override("fr"):
    public = self.client.get(reverse("accounts:user_login"))
    self.assertEqual(public["Content-Language"], "ja")

    admin = self.client.get(reverse("admin:login"))
    self.assertEqual(admin["Content-Language"], "en-us")

    self.assertEqual(translation.get_language(), "fr")
```

假名鍵盤測試同時驗證顯示和事件值：

```python
self.assertIn('data-kana="&quot;"', html)
self.assertIn('data-kana="。"', html)
self.assertIn("゛", html)
self.assertIn("゜", html)
```

通知接收者語言測試：

```python
VocabRequestService.create_event_for_admin(
    word="猫",
    kana="ねこ",
    request_type="create",
    request_by=self.user,
)
self.assertIn("Creation", admin_event.title)

VocabRequestService.reject_vocab_request(request, self.admin)
self.assertIn("追加申請", user_event.title)
self.assertIn("却下", user_event.title)
```

開發結果 table 測試保留原始代碼，同時驗證 escape：

```python
self.assertIn("WRONG", html)
self.assertIn("DAKUTEN", html)
self.assertIn("&lt;script&gt;", html)
self.assertNotIn("<script>", html)
```

這些測試驗證的不是單純「頁面包含一段文字」，而是語言分流、內部值穩定性、template 安全輸出和通知接收者等實際行為。

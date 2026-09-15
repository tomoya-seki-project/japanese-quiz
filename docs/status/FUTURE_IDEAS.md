# Future Ideas

呢份文件用嚟記低「將來可能做，但目前未承諾 / 未納入開發 scope」嘅想法。  
當某個 idea 真正開始進入近期開發，先搬返去 `TODO.md`，改成 `TODO` 或 `WORKING`。

## 目錄

- [Account](#account)
- [Event Notification](#event-notification)
- [User Message / Admin Inbox](#user-message--admin-inbox)
- [Quiz](#quiz)
- [Scheduled Maintenance](#scheduled-maintenance)
- [Post-v1.0.0 Multiple Choice Quiz](#post-v100-multiple-choice-quiz)
- [Vocab Data Model](#vocab-data-model)
- [Database Export / Restore](#database-export--restore)
- [CSV Import / Logging](#csv-import--logging)

## Account

- 加入 password reset flow，使用 Django內建 views、forms及 `default_token_generator`；如需要同 activation不同期限，再拆分 timeout策略。

## Event Notification

- Site announcement 可以之後加入 publish time、expire time、importance level、active status、target user group。
- Vocab request result event 之後可以加入 reviewer reason 或更詳細 result message。

## User Message / Admin Inbox

- 保留原本 user message 同最後 import batch 嘅關係，方便追蹤處理結果。
- 如果同一批 vocab 由多個 users 提出，要確保每個相關 user 都收到處理結果。

## Quiz

- 正式加入 katakana answer flow。
- 為 smartphone 實作日文假名 flick keyboard：以「あ・か・さ・た・な・は・ま・や・ら」等行首假名作主鍵，按住主鍵後向指定方向滑動手指選擇同一行嘅目標假名。
- 如之後需要更精準嘅 recent skip，可只保存最近 10 個 vocab ids；暫時唔建立完整 question history model。

## Scheduled Maintenance

- v1.0.0 後考慮定期調整逾期 `UserVocab.weight`：使用 `last_quiz_at` 判斷太耐冇出現嘅 vocab，決定各階段等待時間、每次 boost、high value上限，並以每個 user自己嘅 `UserVocab` 範圍計算 average weight。
- 如果 M-03 最終使用短期 `QuizAttempt` records防止 Answer／Skip重複處理，為 completed、expired及長期 pending attempts制定 retention policy，並加入獨立 cleanup management command，避免過時資料無限累積。
- Weight adjustment同 `QuizAttempt` cleanup維持為兩個獨立 management commands，方便使用唔同執行頻率、獨立記錄結果與處理失敗；command應考慮 logging、處理數量及 `--dry-run`。
- Deployment時再按環境選擇 cron或hosting platform scheduler定期呼叫 commands；除非將來需要大量 background jobs、retry或worker queue，暫不為呢兩項 maintenance單獨引入 Celery Beat。

## Post-v1.0.0 Multiple Choice Quiz

- v1.0.0 後重新啟用 `adverb`、`mimetic`、`conjunction` 同 `colloquial` choices；完成 multiple-choice panel、選項生成、submit、backend checking、result response 同 template 顯示後，先再次向 user 開放。
- 四種 type 係 project-specific quiz／learning 分類，唔係純語言學詞性。重疊時依序判斷固有擬聲／擬態、主要連接句子、主要修飾功能，再判斷係咪符合口語／辨認式學習用途；無法確定就進 ambiguity queue，展示最多三個有證據嘅常見義、建議 type 同來源，唔為湊數加入罕見意思。
- CSV contract 預計以 `word` 保存原字、`kana` 保存平假名讀音，並喺 `native_japanese` 後加入 `question1`、`question2`、`mc_answer1`、`mc_answer2`、`mc_answer3`；`vocab`／`katakana` 嘅 MC 欄位使用 `---`，而 `native_japanese` 只供 `katakana` 使用。
- 每個 sense 使用兩條簡短自然用例；可用單句或 `Q：...\nA：...` 對答，目標詞用 `____` 隱藏，活用提示緊接 ASCII 括號。每題目標不超過 50 Unicode characters，只有自然度或消除歧義需要先可放寬至最多 100，並計入字面 `\n`、blank、標點同提示。
- 正確選項與三個 distractors 全部保存基本形並互不重複：`mc_answer1` 為近義／易混淆但兩題皆不適用、`mc_answer2` 為同 project type 但明確錯、`mc_answer3` 可跨四種 MC type但仍須兩題皆明確錯。選項可以來自 DB 外，但必須係已查證嘅自然用語；如任何 distractor 能自然完成其中一題，就要換題或換選項。
- 實作 question blank、字面 `\n`、活用提示、長度、distractor 語義／句法／活用／type validation；四個選項喺 view context 階段 randomize，但 CSV 保留正確答案與三種 distractor 嘅固定角色。
- 沿用同一 `(word, kana)` 一個 `Vocab`、多個 `MCSense` 嘅設計；每個 sense 有獨立 meaning、questions 同 distractors，但共用 `UserVocab` weight、streak、答題統計、`last_quiz_at` 同 recent-question exclusion。
- 落實 `sense_no` 由 1 開始嘅 minimum validation，定義穩定 `sense_key` 規則與 CSV 欄位，令重跑同一份 CSV 可以辨認已有 sense；保留 `(word, kana)` 作 `Vocab` identity，並以 `sense_key` 作 stable sense identity、`(vocab, sense_no)` 作 vocab 內 duplicate validation。
- 決定同一 `Vocab` 各 senses 嘅 type、level、categories 必須一致並合併到 base `Vocab`，定係部分資料移入 `MCSense`；同時確立 `adverb`／`mimetic`／`conjunction` 對應同名 category、`colloquial` 按內容主題分類嘅最終政策。
- 擴充 CSV import、`VocabActionService`、admin／request、create／update／restore／delete、detail view 同 answer comparison，真正建立及使用 `MCSense`。相同 `(word, kana)` MC rows 要指向同一 `Vocab`；非 MC duplicate 或 MC type 衝突要 skip 並寫入 conflict report，唔可以當成功或靜默略過。
- 現有 `NewWord_YYYY_MM.csv` 只作測試，由 user 喺正式啟用前自行刪除；唔自動刪除、覆蓋或升級同名測試檔，亦暫不批量升級舊 `resource/kanji*.csv`。
- 四種 type 完成 end-to-end tests，並驗證 import、request、admin、quiz、answer result 全條 vertical flow 後，先恢復 choices及正式匯入資料。

## Vocab Data Model

- `Vocab.word_slug` 延至 v1.0.0 之後：決定以 `word`、`kana` 定其他資料產生 slug，處理 duplicate、word／kana 更新時同步政策，同為舊資料 backfill。

## Database Export / Restore

- Whole database CSV export 延至 v1.0.0 之後：如日後實作 `python manage.py export_whole <output_folder>`，將主要 models／tables 分開輸出，同時保留 primary key、foreign key、必要 relationships，決定 sensitive data export／mask 政策，並考慮加入 manifest。
- 配套 whole database restore／import 同樣延至 v1.0.0 之後：按 model dependency 決定 restore order，加入 schema／version preflight 同 dry-run，並以 export format 作唯一輸入 contract。

## CSV Import / Logging

- 之後可考慮 database import history model。
- User message / admin inbox 如觸發 CSV import，可以用 import report 回寫處理結果。
- `import_vocab` 目前遇到重複資料會 skip，並以 terminal message 同 log 提示；將來可考慮將所有被判定為重複嘅 rows 另外匯出成一份 CSV，方便 import 後集中檢查。

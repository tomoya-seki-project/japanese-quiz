# Future Ideas

呢份文件用嚟記低「將來可能做，但目前未承諾 / 未納入開發 scope」嘅想法。  
當某個 idea 真正開始進入近期開發，先搬返去 `TODO.md`，改成 `TODO` 或 `WORKING`。

## 目錄

- [Account](#account)
- [Event Notification](#event-notification)
- [User Message / Admin Inbox](#user-message--admin-inbox)
- [Quiz](#quiz)
- [Vocab Data Model](#vocab-data-model)
- [CSV Import / Logging](#csv-import--logging)

## Account

- 設計 account email activation flow。
- 實作 email activation 時，拆成 public registration form 同 `UserCreationAdminForm`。
- Public registration 建立 `is_active=False` 的 user，等待 email activation。
- Admin 建立 user 時可以直接設定 `is_active=True`。
- 設計 registration 後是否即時限制 login。
- 建立 activation link flow。
- 決定 activation link expiry。
- 設計 resend activation email flow。

## Event Notification

- Site announcement 可以之後加入 publish time、expire time、importance level、active status、target user group。
- Vocab request result event 之後可以加入 reviewer reason 或更詳細 result message。

## User Message / Admin Inbox

- 保留原本 user message 同最後 import batch 嘅關係，方便追蹤處理結果。
- 如果同一批 vocab 由多個 users 提出，要確保每個相關 user 都收到處理結果。

## Quiz

- 正式加入 katakana answer flow。
- 正式加入 multiple choice question / answer flow。
- Multiple choice panel 要產生實際選項，並接上 answer submit 同 backend checking。
- Multiple choice answer flow 要回傳答題結果，方便 view/template 顯示答啱或答錯。
- 如之後需要更精準嘅 recent skip，可只保存最近 10 個 vocab ids；暫時唔建立完整 question history model。

## Vocab Data Model

- 詳細研究一詞多義 identity 應採用 `sense_no`、`sense_key`，或兩者分工：比較穩定識別、顯示排序、重新編號、可讀性、migration 同 duplicate validation 嘅影響，再決定點樣取代目前只以 `(word, kana)` 判斷唯一嘅設計。

## CSV Import / Logging

- 之後可考慮 database import history model。
- User message / admin inbox 如觸發 CSV import，可以用 import report 回寫處理結果。

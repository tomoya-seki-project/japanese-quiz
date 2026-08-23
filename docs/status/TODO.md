# Project TODO

呢份 TODO 用嚟追蹤 project 本身嘅 bug、功能、flow 狀態同改良。
舊版 TODO 內容已整合入目前格式。
未承諾、未納入目前 scope 嘅未來擴展 idea 統一放喺 `FUTURE_IDEAS.md`。

Status badge：

-  <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span>（62）：核心功能已完成，或已有明確 decision
-  <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span>（3）：已開始處理，但仍有必要項目未完成
-  <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span>（9）：未開始或暫時只係計劃

## 目錄

- [已 Check 到嘅問題 / Fix Tracking](#已-check-到嘅問題--fix-tracking)
- [Vocab Planned Work](#vocab-planned-work)
- [VocabRequest Result / UserVocab Flow](#vocabrequest-result--uservocab-flow)
- [Account / User Management](#account--user-management)
- [Event Notification System](#event-notification-system)
- [Data Import / Export / Database Migration](#data-import--export--database-migration)
- [User Message to Admin](#user-message-to-admin)
- [Quiz Question Logic](#quiz-question-logic)
- [Logging / Audit Trail](#logging--audit-trail)
- [General Improvements](#general-improvements)
- [UI / UX](#ui--ux)

## 已 Check 到嘅問題 / Fix Tracking


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 1 點（VocabRequest / Admin Review）：真正實作 approve / reject request 嘅處理 flow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Approve 已按 CREATE / UPDATE / RESTORE / DELETE request type 呼叫對應 vocab action。
- Reject 會更新 request status 同 reviewer，但唔會改動 vocab。
- Admin 會根據 service 回傳結果顯示成功或已處理 warning。
- 已用 browser / admin 手動測試 create、restore、update、delete request，以及 approve / reject 正常 flow。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 2 點（VocabRequest / Admin Review）：Admin approve / reject action 由 GET link 改做 POST**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 避免誤 click、refresh page 時重複執行，或者連續 click 造成重複處理。
- 當 request 已經唔係 `PENDING` 狀態，就唔可以再處理多次。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 3 點（VocabRequest / Admin Review）：確認 approve / reject permission boundary**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Approve / reject 已改為喺 admin change form 入面經 `response_change()` 處理。
- 正常入到 admin change page 已經會受 Django admin permission 控制。
- Approve / reject branch 已額外 call `self.has_change_permission(request=request, obj=obj)` 作 defense-in-depth。
- 無 change permission 時會經 `handle_no_change_permission()` 顯示 error message 並 redirect 回 request change page。


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 目前 approve / reject permission boundary 已確認足夠。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 4 點（VocabRequest Form）：`VocabUpdateRequestForm.vocab_type` readonly**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已將 `VocabUpdateRequestForm` 入面嘅 `vocab_type` set 做 readonly。
- 避免 user 喺 update vocab request 期間改咗 vocab type，令 detail model 關係變亂。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 5 點（VocabRequest Transaction）：建立 `VocabRequest` 嘅操作要有 transaction atomic**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Create / update / restore / delete request creation 已經用咗 `transaction.atomic()`。
- 避免 create request 中途 exception、server stop，或者其中一部分 save 咗但另一部分冇 save。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 6 點（VocabRequest / Admin Review）：approve / reject review flow 要有 transaction atomic**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Approve / reject 已使用 `transaction.atomic()`、`select_for_update()` 同 `PENDING` status check。
- Review 時更新 `VocabRequest` 同執行 vocab action 會放喺同一個 transaction 入面。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 7 點（VocabRequest Duplicate Check）：防止 duplicate pending request**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Service 會先檢查有冇 pending request，提供較清楚嘅正常 flow feedback。
- Database 已加入 conditional unique constraints，防止 concurrent requests 同時通過 application check。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 8 點（VocabRequest View Error Handling）：處理 service 拋出嘅 `ValidationError`**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Create / update / restore / delete request 遇到 concurrent duplicate 時，service 會將 `IntegrityError` 轉成 `ValidationError`。
- `VocabCreateRequestView`、`VocabUpdateRequestView` 同 `VocabDeleteRequestView` 已喺 call service 時捕捉 `ValidationError`。
- View 會將錯誤加入 form non-field errors，並回到 `form_invalid()`，避免 exception 穿出 request flow。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 9 點（VocabRequest / Admin Review）：擴大 admin review concurrency protection**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `VocabRequestAdmin.get_queryset()` 會喺 approve / reject POST 時使用 `select_for_update()`，令 admin change form save 前先鎖住目標 request row。
- `VocabRequestService.approve_vocab_request()` / `reject_vocab_request()` 仍保留 service-level `select_for_update()`，避免日後其他 caller 繞過 admin protection。
- Reviewed request 會經 `get_readonly_fields()` 設為 readonly，並由 `save_model()` 擋住非 pending request 被再次保存。
- 已手動測試 approve / reject 正常操作。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可以再用 automated tests 驗證兩個 admin 同時 review 同舊頁面 submit 嘅情況。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 10 點（VocabRequest / Admin Review）：Admin workflow-controlled fields readonly**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `status`、`request_type`、`reviewed_by` 同適合 readonly 嘅 proposed data 已納入 readonly 設計。
- 普通 model fields 已透過 `get_readonly_fields()` 於 reviewed request 變成 readonly。
- `save_model()` 已擋住非 pending request 被再次保存。
- `proposed_categories` 係 ManyToMany field，已透過 `get_form()` / `form.base_fields["proposed_categories"].disabled = True` 額外 disable。
- 狀態變更應該經 approve / reject service 處理，唔應該喺 admin form 直接亂改。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可再手動測試 reviewed request 入面 M2M checkbox 是否真係無法修改。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 11 點（VocabRequest Form）：統一 request form required fields 同 submission 設計**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- User submit CREATE request 時可以將 `meaning`、`level`、`categories` 留空，由 admin review 時補返。
- `VocabCreateRequestForm` 已將 `meaning`、`level`、`categories` 設為 optional。
- Approve 前會再經 `validate_for_approval()` 檢查最終 proposed data 是否足夠。
- `VocabUpdateRequestForm` 仍保留較嚴格 required fields，因為 update form 會由原本 vocab data 提供 initial value。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 12 點（VocabRequest Validation）：決定唔同 vocab type 專屬 fields validation rule**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- CREATE / UPDATE Katakana request 喺 approve 時必須有 `proposed_native_japanese`。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 13 點（Vocab List）：公開 vocab list 只 show active vocab**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已喺適合位置加 `is_active=True` filter。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 14 點（Vocab Type）：決定改 vocab type 時 validation 同 related detail 處理**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 目前決定：喺 `VocabUpdateRequestForm` 將 vocab type set 做 readonly。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 15 點（VocabRequest Model）：保留 `VocabRequest.original_vocab` 目前 `CASCADE` 行為**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 正常 delete vocab 嘅方式係 soft delete / disable，而唔係 database 入面永久 delete。
- 如果 vocab 真係被永久 delete，目前接受相關 review record 一齊消失。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 16 點（Vocab Model Integrity）：確保 `Vocab.type` 同 detail model 保持一致**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `vocab` type 應該有 `VocabDetail`；`katakana` type 應該有 `KatakanaDetail`。
- 正式 create vocab path 交由 `VocabActionService` 處理，確保 create 主表時同時建立對應 detail model。
- `VocabAdmin.has_add_permission()` 已禁止 admin 直接新增 vocab，避免繞過 service create flow。
- `VocabAdmin.readonly_fields` 已將 `type` 設為 readonly，避免 admin 直接改 existing vocab type 造成 type/detail mismatch。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 舊資料或 future bypass service 嘅情況仍要靠之後 data audit / tests 留意。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 17 點（VocabRequest Form）：清理已移除嘅 `similar_word` form 設計**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `Vocab.similar_word` 已經移除。
- `BaseVocabRequestForm` 入面嘅 `similar_word` field 已停用。
- Vocab request creation / update flow 入面 related save code 亦已停用，避免 user 以為提交咗但實際被忽略。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 18 點（Account Admin）：檢查 custom User Admin 寫法**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `CustomizedUserAdmin` 已繼承 Django standard `UserAdmin`。
- Add form 會用 `set_password()`。
- Change form 會用 readonly password hash field。
- 目前 public registration 同 admin Add User 共用 `RegistForm`。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 19 點（Account Login）：移除 login flow 入面冇實際作用嘅 `user.save()`**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Django `LoginView` 已經會透過 authentication flow 更新 `last_login`。
- 已移除 login 成功後無欄位改動嘅額外 `user.save()`，避免多餘 database write。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 20 點（UserVocab Flow）：穩定 UserVocab 選擇頁 GET / POST 之間嘅候選範圍**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 原本嘅 `UserVocabSelectVocabView` 會每次 request 重新計算候選 vocab，GET / POST 之間可能出現候選範圍變動。
- 目前加字主流程已改成 login / register 後自動 sync 新 vocab，建立 `UserVocab(in_use=True)`。
- 舊 selection flow 暫時唔作為主要加字入口。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 25 點（VocabRequest Approval Guard）：Approve UPDATE / RESTORE / DELETE 前驗證 `original_vocab`**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- UPDATE / RESTORE / DELETE request flow 已依賴 `original_vocab` 作為目標 vocab。
- Approve 前已檢查 `original_vocab` 是否存在。
- UPDATE / DELETE approve 時要求 `original_vocab.is_active=True`。
- RESTORE approve 時要求 `original_vocab.is_active=False`。
- 如果資料異常，service 會 raise `ValidationError`，停止 approve 並回傳清楚 error result。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 21 點（UserVocab / Quiz Pool）：避免 inactive vocab 進入 quiz 出題範圍**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserVocabService.get_new_vocab()` 已只 sync `is_active=True` vocab。
- `QuizService.create_question_pool()` 已加入 `vocab__is_active=True`，避免 inactive vocab 進入 quiz pool。
- `QuizSettingView.get()` 入面檢查 active vocab 數量時，已同樣使用 `vocab__is_active=True`。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 22 點（Vocab URL Boundary）：inactive vocab detail / update / delete 直入 URL 處理**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `VocabDetailView.get_queryset()` 已限制 `is_active=True`。
- `VocabUpdateRequestView.target_vocab` 已用 `get_object_or_404(..., is_active=True)`。
- `VocabDeleteRequestView.target_vocab` 已用 `get_object_or_404(..., is_active=True)`。
- Inactive vocab 直入 detail / update / delete URL 會走 404，restore request flow 保持分開。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 23 點（UserVocab Detail Permission）：`UserVocabDetailView` object ownership guard**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserVocabDetailView.get_queryset()` 已限制 `user=self.request.user`。
- `UserVocabDetailView.get_queryset()` 已加入 `vocab__is_active=True`，避免 inactive vocab detail 被普通 user 查看。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **第 24 點（VocabRequest Delete Snapshot）：DELETE request 保存完整 proposed snapshot**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- DELETE request creation 時，同步保存當時 vocab 嘅 `proposed_vocab_type`、`proposed_meaning`、`proposed_level` 同 `proposed_categories`。
- 如 target vocab 係 katakana，保存 `proposed_native_japanese` snapshot。
- 避免 admin review DELETE request 時見到 default / 空 proposed data 而誤判。

## Vocab Planned Work


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Additional vocab types：adverb / mimetic / conjunction / colloquial**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `VocabType` 已加入 `adverb`、`mimetic`、`conjunction` 同 `colloquial` choices。
- 已產生 migration，更新 `Vocab.type` 同 `VocabRequest.proposed_vocab_type` choices。
- 已決定 `adverb`、`mimetic`、`conjunction` 同 `colloquial` 使用 multiple-choice 答題，而唔使用 50 音 keyboard。
- 新 type 係 project-specific quiz / learning 分類，唔係純語言學詞性；例如 `ズレ` 會歸入 `colloquial`，避免要求 user 用 kana keyboard 重複輸入同一寫法。
- 已決定四種 MC type 嘅 CSV mapping：`word` 保存原字，`kana` 保存平假名讀音。
- 已決定 monthly new-word CSV 喺 `native_japanese` 後加入 `question1`、`question2`、`mc_answer1`、`mc_answer2`、`mc_answer3`；`vocab`／`katakana` 呢五欄使用 `---`。
- 已定義 `question1`／`question2` 內容：各自生成一條簡短自然用例，可按需要使用單句或 `Q：...\nA：...` 對答；只有對答先保存字面 `\n` 分行標記。
- 題目以四個半形 underscore `____` 隱藏目標詞；需要活用時緊接 ASCII 括號提示，例如 `____(て)`、`____(ない)`、`____(され)`、`____(られ)`、`____(させ)`。
- 每個 question 以 Unicode characters 獨立計長度，生成目標為最多 50 字；只有為保持自然度或消除多答案歧義先可放寬至 100 字，任何情況都唔可以超過 100 字。字面 `\n`、`____`、標點同活用提示全部計入。
- MC 正確選項維持 `word` 保存嘅基本形；即使句子實際需要 `ググって`，選項仍使用 `ググる`，括號負責提示活用。
- 已定義三個 distractor：`mc_answer1` 用近義／易混淆但兩題皆不適用嘅字；`mc_answer2` 用同一 project type 但兩題皆明確錯嘅字；`mc_answer3` 可來自四種 MC type 其中之一，但兩題皆明確錯。
- `word` 同三個 distractor 全部保存基本形、互不重複；任何 distractor 如能自然完成其中一題，就要改題目或換選項，唔可以保留多個合理答案。
- `mc_answer1`～`mc_answer3` 唔需要已存在於目前 DB／resource CSV；可以由外部日文詞彙生成，但必須係已查證嘅真實自然用語，欄位設計亦唔應強制依賴 `Vocab` ForeignKey。
- `native_japanese` 只供 `katakana` 使用，其他 type 統一保存 `---`。
- `type=adverb`、`mimetic`、`conjunction` 時，`category1` 必須使用同名 category；`colloquial` 暫時按內容主題選現有 category。
- 已決定 MC type 重疊時嘅優先順序：固有擬聲／擬態先用 `mimetic`，主要連接句子用 `conjunction`，主要修飾功能用 `adverb`，其餘符合 project 口語／辨認式學習定義先用 `colloquial`；仍然不確定就進 ambiguity queue。
- 四個 MC 選項會喺 view `get_context_data()` 階段 randomize，CSV 繼續保存正確答案同三種 distractor 嘅固定角色。
- 多義／type 不確定嘅字會排入 ambiguity queue：先完成同批清楚嘅字，再為每個 unresolved word 顯示最多三個常見詞義、建議 type 同來源，等 user 選一個、多個或唔收錄。
- 常見詞義選項唔需要湊足三個；只有一至兩個常見義就只顯示一至兩個，唔可以加入罕見、過時、專門或證據薄弱嘅意思湊數。
- 已決定同一個 `(word, kana)` 只保存一個 `Vocab`，各個 MC 語意改用 `MCSense` one-to-many rows 保存；每個 sense 有獨立 meaning、questions 同 distractors，但共用同一個 `UserVocab` learning progress。
- 已接受任何一個 sense 出題後，同一個 `Vocab` 其他 senses 都要等該 `UserVocab` 離開 recent-question exclusion 後先再出；`weight`、`streak`、correct / incorrect count 同 `last_quiz_at` 亦按整個 `UserVocab` 共用。
- 保留 `VocabDetail` one-to-one relationship，繼續專門保存 `vocab` type 將來可能加入嘅額外資料；MC 題資料另外使用 `MCSense`。
- CSV import 判斷同一個 vocab 時使用 `(word, kana)`，唔可以只比較 `word`；第一個 MC row 建立 `Vocab` 同第一個 `MCSense`，之後相同 `(word, kana)` 嘅 MC rows 只新增指向同一 `Vocab` 嘅 `MCSense`。
- `MCSense` model foundation 已加入 `Vocab` ForeignKey、`sense_no`、`sense_key`、meaning、兩條 questions、三個 distractors、`__str__()` 同明確 `mc_sense` table name；`(vocab, sense_no)` database constraint 已定義，Django system check 通過，但 migration 尚未建立。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 完成四種新 type 嘅 multiple-choice input panel、選項生成同 submit flow。
- 確認 `sense_no` 是否由 1 開始並加入相應 minimum validation，決定 `sense_key` 生成規則後，建立及套用 migration。
- 實作 `question1`／`question2` 嘅 blank、字面 `\n` 同活用提示 validation。
- 實作三個 distractor 對兩條題目嘅語義、句法、活用同 type validation，以及 view `get_context_data()` 選項 randomization。
- 更新 CSV import、service、admin / request flow 同測試，真正建立及使用 `MCSense`；同一 CSV 或現有 DB 內重複 `(word, kana)` 嘅 MC rows 要指向同一個 `Vocab`，非 MC duplicate 或 MC type 衝突要 skip 並列入 conflict report，唔可以當成功或靜默略過。
- 保留 `Vocab` 目前 `(word, kana)` unique rule；用 `MCSense.sense_key` 做 stable identity，並用 `(vocab, sense_no)` 做同一 vocab 內嘅 duplicate validation。
- 決定 CSV 點樣提供或穩定生成 `sense_key`，令重跑同一份 CSV 時可以辨認已有 sense，唔會重複新增；現有 monthly CSV 尚未有 `sense_key` 欄。
- 決定同一 `Vocab` 各個 senses 嘅 `type`、level 同 categories 必須一致、合併到 base `Vocab`，定係部分資料要搬入 `MCSense`；目前測試 CSV 已有同字各 sense categories 不同嘅例子。
- 現有 `NewWord_YYYY_MM.csv` 只係測試品，由 user 喺正式啟用前自行刪除；skill 唔可以刪除、覆蓋或升級同名測試檔。舊 `resource/kanji*.csv` 暫時亦唔批量升級。
- 擴充 answer result comparison；目前只為 `vocab` 同 `katakana` 產生逐字比較結果。
- 驗證 create / update / restore / delete request、CSV import、detail view 同 admin flow 對四種新 type 嘅完整支援。
- 將四種 MC type 接上 `MCSense` creation / update flow；目前 `VocabActionService` 仍只處理 `vocab`／`katakana` detail row，未保存 MC-specific data。
- 加入各 type 嘅 end-to-end 測試後，先視為可正式匯入及出題。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Category multiple selection**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已新增 `Category` model。
- `Vocab` 同 `VocabRequest` 已使用 ManyToMany categories，request form、snapshot、admin review 同 approve flow 均支援最多三個 categories。
- CSV import 已支援 `category1`～`category3`，category 基礎資料由 `resource/categories.csv` 同 `setup_categories` command 管理。
- Vocab／UserVocab search 已配合 M2M categories，legacy single-category field 已移除。
- Categories admin、request 同 import 主要流程已手動驗證。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- `Category multiple selection` 目前主要由 request form 控制最多三個 categories；如果呢個係 project invariant，之後要喺 service / admin form 層面一併保護。
- 將來如 category 數量增加，可以再改善 admin/search UI。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Word slug generation**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 實作 `Vocab.word_slug` 產生規則。
- 決定 slug 由 `word`、`kana` 定其他資料產生。
- 處理 duplicate slug。
- 決定 word / kana 更新時 slug 是否同步更新。
- 為舊資料 backfill slug。

## VocabRequest Result / UserVocab Flow


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **VocabRequest core workflow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- CREATE / UPDATE / RESTORE / DELETE request creation flow 已完成。
- Request creation、approve 同 reject 均經 service transaction 處理；review action 使用 POST、row lock 同 `PENDING` guard 防止重複處理。
- Duplicate pending request 同 concurrency 由 application validation、conditional unique constraints，以及 `IntegrityError` → `ValidationError` handling 共同保護。
- Reviewed request 同 workflow-controlled fields 會變成 readonly；approve 前亦會驗證最終 proposed data。
- CREATE／UPDATE／RESTORE／DELETE request 及 approve／reject 主要流程已手動驗證，admin 會按 service result 顯示 feedback。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可以補 automated tests 驗證 duplicate request、approve / reject concurrency、reviewed request readonly behavior。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Vocab model integrity through service layer**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Vocab create / update / restore / delete 已集中交由 `VocabActionService` 處理。
- `VocabAdmin.has_add_permission()` 已禁止 admin 直接新增 vocab。
- `VocabAdmin.readonly_fields` 已將 `type` 設為 readonly。
- `Vocab.type` 同 detail model 關係由 service create flow 維持。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 舊資料或 future bypass service 嘅情況，可以之後用 data audit / tests 檢查。

## Account / User Management


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Custom User Admin foundation**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `CustomizedUserAdmin` 已繼承 Django standard `UserAdmin`。
- Add form 會用 `set_password()`。
- Change form 會用 readonly password hash field。
- Admin user detail page 已用 function readonly field 顯示 profile data。
- User admin 已用 summary field + filtered `UserVocabAdmin` link 取代 `UserVocabInline`。
- `date_joined` / `last_login` 已放入 user detail readonly area。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **UserProfile auto creation**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已加入 `accounts.signals`。
- User create 後會透過 `post_save` signal 自動建立 `UserProfile`。
- `INSTALLED_APPS` 已改用 explicit `AppConfig` path，確保 `AccountsConfig.ready()` 載入 signals。
- 目前 database 已重新 migrate，新 user 會自動有 profile。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **UserVocab sync and in-use flow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserVocab.in_use` 已改成 default `True`。
- Login／register 後會由 `UserVocabService.sync_new_vocab()` 補齊 user 尚未擁有嘅 vocab，並以 `bulk_create(ignore_conflicts=True)` 減少同步成本。
- UserVocab list 可按 `in_use` filter，亦支援以 `selectable_ids`／`selected_ids` 安全地 bulk update quiz 使用狀態。
- Select-all、checkbox 同 `in_use` 更新流程已用 browser 驗證。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 如將來 vocab 數量大幅增加，可以再實測 `bulk_create()` 後嘅 sync performance。
- 如將來 user 需要大量管理 `in_use`，可以再改善 filtering / bulk action UI。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **UserVocab detail single-item management**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserVocabDetailView` 已有 ownership guard，限制目前 user 只能查看自己嘅 active user vocab。
- Detail page 已接入 list／URL，並分開顯示 user-specific quiz 狀態同 vocab master data。
- User 可由 detail page進入既有 update／delete request flow，亦可單獨更新該 vocab 嘅 `in_use` 狀態。
- POST 更新後會 redirect，invalid POST 則保留 bound form，避免錯誤內容被 context 重建覆蓋。

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **UserVocab selection page scope decision**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 舊 `UserVocabSelectVocabView` 暫時唔再作為主要加字入口。
- 目前主流程係 login / register 自動建立 `UserVocab` relationship。
- 已避免 GET / POST 期間候選 vocab range 變動影響主流程。

## Event Notification System


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Event / UserEvent data model foundation**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已建立 `Event` model 保存 event type、title、message。
- 已建立 `UserEvent` through model 保存每個 user 對 event 嘅 read status。
- `UserEvent` 已加入 `(user, event)` unique constraint。
- `Event` 已註冊到 admin。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **EventService helpers**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `create_event()` 已負責建立 event record。
- `assign_event_to_user()` 已用 `get_or_create()` 避免 duplicate assignment。
- `assign_event_to_users()` 已可派 event 俾指定 user queryset；預設可派俾所有 users。
- `mark_as_read()` 已會設定 `is_read=True` 同 `read_at`。
- `get_unread_events()` 已回傳 user 未讀 events，並用 `select_related("event")`。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Vocab request events**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- User submit CREATE / UPDATE / RESTORE / DELETE vocab request 後會通知 staff。
- Staff notification 使用 `transaction.on_commit()`。
- Approve request 後會建立 `VOCAB_REQUEST_RESULT` event 通知 request owner。
- Reject request 後會建立 `VOCAB_REQUEST_RESULT` event 通知 request owner。
- User 已可喺 notification page 查看 request result event。
- User 已可將 result event mark as read。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Vocab sync summary event**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserProfile.last_vocab_sync_at` 已作為 user vocab sync / event summary 基準時間。
- `EventService.gen_vocab_sync_event()` 會按 sync window 找出 vocab 變化，並根據 approved request 分辨 CREATE／UPDATE／RESTORE／DELETE；無 request 記錄嘅變化會使用 admin／import fallback。
- Summary generation 已接入 login 同 profile refresh point；首次 sync 只建立基準時間，唔補發歷史事件。
- User 可經 event list／detail 查看 summary；create、update、restore、delete 同 import 情況已手動驗證。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- `gen_vocab_sync_event()` 目前會對每個 changed vocab 查 related approved request；當 changed vocab 數量大時會有 N+1 query 風險，之後可改成一次預取相關 request 再喺 Python group。
- 如資料量變大，可以再優化 query 數量同 summary generation performance。
- 如 login / profile 兩個 request 同時觸發 `gen_vocab_sync_event()`，可能讀到同一個 `last_vocab_sync_at` 並建立重複 summary event；之後可考慮 profile row lock 或 event window idempotency。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Notification read / history**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已建立 unread event list view。
- User 可查看 unread、read 或全部 event history，並透過安全嘅 `selectable_ids`／`selected_ids` bulk flow 標記已讀。
- Event detail 有 ownership guard；navbar 會經 context processor 顯示 unread count。
- Event list 已支援 status filter 同 Ajax partial pagination。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- Mark all as read。
- Login 後首頁如需要，可以顯示更完整 notification summary。

## Data Import / Export / Database Migration


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **CSV vocab import command**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `import_vocab` 已支援 CSV path argument。
- Command 只容許 superuser 執行，並驗證 CSV headers、最多三個 categories 同每行資料。
- 每筆 vocab 會經 `VocabActionService` transaction 建立；duplicate 或 invalid row 會保留行號／原因並繼續處理下一行。
- 完成後會輸出 imported／failed 統計及各 failed row 詳情。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 如之後需要更細分，可以再加 skipped rows count。
- 可以輸出 summary log file，方便大量 import 後 review。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Development clear vocab command**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已建立 `dev_clear_vocab` command。
- 用於 development/testing 時快速清理 vocab 相關資料。
- 已手動測試 command 正常運作。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Whole database export command**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 實作 `python manage.py export_whole <output_folder>`。
- 將主要 models / tables 分開 export 成 CSV。
- 保留 primary key、foreign key 同必要 relationship。
- 決定 sensitive data 是否 export / mask。
- Export folder 可附帶 manifest file。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Whole database restore / import command**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 配合 `export_whole` 產生嘅 CSV files restore 去新 database。
- 按 model dependency 決定 import order。
- Restore 前做 schema / version check。
- 提供 dry-run mode 預先檢查 errors。

## User Message to Admin


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **User-to-admin feedback flow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已將原本 FAQ 方向整理成 `Feedback` flow。
- 登入 user 可提交 `PENDING` feedback；superuser 會進入有固定 ordering 嘅管理 list／detail／reply flow。
- Admin reply 後會更新 `REPLIED` status、reviewer 同時間，並建立 `FEEDBACK_REPLY` event 通知提交者。
- 普通 user submission、superuser review／reply、status update 同 event creation 已手動驗證。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- Feedback form 內容長度之後可按實際用途調整；如果會用嚟提交大量 vocab suggestion，`context` 可能要放寬。
- 如 admin handling 變複雜，再考慮加入更多 status，例如 `PROCESSING` / `DONE`。
- 如日後需要 public contact form，再另外設計 anonymous feedback / contact email / anti-spam flow。
- Admin 整理 vocab suggestion 後，可建立 CSV，再用 `import_vocab` 加入 database。
- Feedback list / detail / reply UI wording 之後可再 polish。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Feedback duplicate submission handling**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 檢查 `FeedbackCreateView` 入面 `get_or_create()` lookup 同 `Feedback` unique constraint 是否一致。
- 如果同一 user 曾提交相同 type/context 並已被 reply，再次提交時目前可能撞到 `user + type + context` unique constraint。
- 決定移除目前永久限制 `user + type + context` 重複提交嘅 unique constraint。
- Create flow 改成先 check 是否已有同一 user / type / context 嘅 `PENDING` feedback。
- 如果已有 pending feedback，回到 form invalid 並顯示清楚 error。
- 如果舊 feedback 已 `REPLIED`，允許 user 用同一 type / context 再提交新 feedback。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後如要防 double submit / race condition，可加入 conditional unique constraint，只限制同一 user / type / context 同時存在一筆 `PENDING` feedback。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Feedback service extraction**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已建立 `core/service/feedback.py`，將 feedback domain logic 由 view 抽出。
- `create_feedback()` 可負責 pending duplicate check、建立 feedback、回傳 result / 拋出 validation error。
- `reply_feedback()` 可負責更新 feedback status、寫入 `reply_by` / `reply_at`、建立 reply event。
- View 保持負責 form handling、redirect、message / form error，service 負責 business rule。

## Quiz Question Logic


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz question filter**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `QuizSettingForm` 可用 checkbox 複選 vocab type、level 同 categories；空選項代表不限制該條件。
- Settings 會保存到 session，並由 play／next flow 傳入 `QuizService.create_question_pool()`。
- Question pool 只使用目前 user `in_use=True` 嘅 UserVocab，支援單一、複數或無條件 filter 組合。
- Filter 後無題會 fallback 到 full active vocab pool，並回傳 `fallback_used`；active vocab 數量不足則 redirect 到 user vocab list 並顯示 warning。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- Filter fallback / no active vocab warning message 之後可再配合 template 顯示得更清楚。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz setting use-last-setting guard**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 如果 user 第一次進入 quiz setting 就勾選 `use_last_setting`，但 session 入面未有 `quiz_settings`，會回到 invalid form。
- `QuizSettingView.form_valid()` 已檢查 previous settings 是否存在；不存在時會加 `use_last_setting` field error。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz view routing and result flow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Quiz 已完成 setting、隨機出題、answer submit、result、Next、Skip、resume 同 no-question 基本流程。
- Quiz 採用 full-page shell + Ajax partial 架構；answer、next 同 skip endpoints 會透過統一 JSON contract，分別更新 main content 同對應 input panel。
- `quiz_settings` 同 `quiz_session` 已分開管理，支援目前題目、題數、答題統計、fallback、tips、skip，以及有限題 quiz 中途離開後恢復。
- Answer submit 已驗證 `UserVocab` ownership 同 session question identity，避免修改 hidden `user_vocab_id` 操作其他 user 或污染非目前題目嘅 stats。
- Next、Skip、fallback、Summary button 同 quiz completion lifecycle 已處理；50 音 keyboard、answer result、partial replacement 同續題流程亦已手動驗證。
- 目前所有 answer submit 暫時使用 kana checking flow；其他 vocab type 會喺相應 multiple-choice flow 完成後再接入。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- `quiz/views.py` 入面嘅 `get_input_panel_rows()`、`render_quiz_question_payload_html()`、`build_next_question_payload()` 暫時可以接受；之後 flow 穩定後可移去 `quiz/view_helpers.py`，令 views 保持專注處理 request / response。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Weighted random question selection**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Question pool 以目前 user 嘅 `UserVocab.weight` 做 weighted random；`QuizService.pick_question()` 使用 cumulative weights + `bisect_left` 抽題。
- `weight` 有 database-compatible `MinValueValidator(1)` 同 service-level `min_weight` clamp，避免正常輸入或運算令數值跌穿下限。
- Correct／wrong、tips、streak 同 skip 會按 `quiz/config/quiz_config.json` 調整 weight，設定名稱已整理成清楚嘅 gameplay keys。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後實際玩一段時間後，再調整 `correct`、`wrong`、`skip`、`tips`、`streak_correct`、`streak_wrong` 等數值是否合理。
- 之後可再考慮是否需要 `max_weight`，避免長期錯題 weight 過高。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Recent question skip**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `create_question_pool()` 已改用 `last_quiz_at__isnull=False` 搵出最近 quiz 過嘅 10 個 `UserVocab` id，再由原本 `filtered_qs` 排除呢 10 個 id。
- Recent skip 目標係避開最近出現過嘅 vocab，而唔係追蹤完整 question history。
- 暫時以 `UserVocab.last_quiz_at` + ORM query 控制最近出現過嘅 vocab。
- User vocab 少過或等於 10 個時，`create_question_pool()` 會暫時不套用 recent skip，避免 question pool 直接變空。
- 如果 filter 後 question pool 變空，`create_question_pool()` 會 fallback 返 full active vocab pool。
- `last_quiz_at=None` 嘅新 vocab 會保留喺原本 question pool 入面，唔會因為 recent skip 被抽走。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **UserVocab quiz stats and streak update**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Kana／MC answer checking 會更新 `correct_count`、`incorrect_count`、streak、`last_quiz_at` 同 `last_answer`，供出題與 result UI 使用。
- Tips 使用量會納入 weight calculation；只要使用提示就會計數，反映 learner 需要確認答案。
- Skip punishment 有 ownership guard，並會更新 weight、streak 同 `last_quiz_at`。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 決定 kana answer 同其他 answer checking flow 是否抽共用 helper。
- 如之後 stats update 牽涉多個 model / history record，再考慮用 transaction 包住整個更新流程。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz tips_count server-side validation**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `tips_count` 由 hidden input submit，不能完全信任 browser 傳入嘅值。
- 在 form / service 層加入 server-side validation 或 clamp，避免 user 改 POST data 令 weight calculation 被污染。
- 已喺 `QuizForm` 加 `min_value=0` / `max_value=50`。
- 已喺 `check_kana_answer()` 用 `max(0, min(tips_count, 50))` 做 service-level guard。
- 暫時接受每題最多 50 次 tips penalty 作為 technical / gameplay cap。


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Quiz result answer difference display**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `QuizService.answer_compare()` 已建立初版，可產生 `MATCH`、`WRONG`、`MISSING`、`EXTRA` compare result。
- Compare logic 已處理 correct answer / user answer 長度唔同嘅情況，避免其中一邊無下一隻 kana 時 index error。
- Compare logic 已加入 `match_count` tie-break，優先保留更多對得返位置嘅 kana。
- `compare_answer_subtype.json` 已建立，用嚟判斷 `NORMAL`、`DAKUTEN`、`HANDAKUTEN`、`SMALL_KANA`。
- `kana_graphic_map.json` 已生成初版，用嚟由 kana + compare type / subtype 查對應 image path 同 `font_width`。
- `QuizService.gen_answer_image()` 已建立初版，將 compare result 轉成 answer graphic data。
- `QuizSubmitAnswerView` 已開始將 `compare_result` 傳入 `quiz_result_partial.html`。
- `QuizSubmitAnswerView` 已將 `gen_answer_image()` 產生嘅 graphic data 傳入 `quiz_result_partial.html`。
- `quiz_result_partial.html` 已可 render answer compare 圖片，初版能顯示錯位 kana 圖。
- Font image 已 copy 到 `static/rec/font/...`，`kana_graphic_map.json` 已改用 template static 可讀嘅 path。
- Compare logic 已加入 `non_normal_wrong_count` tie-break；當 cost 同 `match_count` 一樣時，會優先保留能產生 `DAKUTEN` / `HANDAKUTEN` / `SMALL_KANA` subtype 嘅 route。
- 已處理 correct `そうぞう`、answer `そそく` 呢類 case，讓結果偏向 `MISSING う`、`WRONG ぞ/そ DAKUTEN`、`WRONG う/く NORMAL`。
- 已補齊 `ぁ`、`ぃ`、`ぅ`、`ぇ`、`ぉ`、`ゎ`、`ヴ`、`ヵ`、`ヮ` 嘅 static kana images 同 `kana_graphic_map.json` mapping。
- `kana_graphic_map.json` 已加入 `sub_image_path`，支援主 kana 圖加共用 overlay mark 嘅設計。
- `MISSING` / `EXTRA` mapping 已改用正常黑字 kana 圖作主圖，再用 `missing_mark_big/small` 或 `extra_mark_big/small` 作 overlay。
- `QuizService.gen_answer_image()` 已將 `sub_image_path` 傳入 result graphic data。
- `quiz_result_partial.html` 已初步 render `sub_image_path`，missing / extra mark 圖已可由 template 讀到。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- `quiz_result_partial.html` 未正式將 `image_path` 同 `sub_image_path` 疊圖顯示；目前只係順序 render 兩張圖。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- `gen_answer_image()` 之後可以加入 fallback image / fallback text，避免 mapping 漏項時 render 出 broken image path。
- `answer_compare()` 目前用 recursive branch 搜尋；短 kana 答案可以接受，如果將來支援較長 answer，可考慮 memoization / DP。
- 之後 UI polish 時，將 missing / extra mark 改成 CSS overlay，令 mark 圖疊喺 kana 主圖上，而唔係另佔一個位置。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz session summary tracking**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `quiz_session` 會保存目標／已答題數、correct／wrong、skip、tips、目前題目同 fallback 狀態，answer、next 同 skip 後均會同步更新。
- Skipped question 唔計入 `quizzed_count`；quiz 可按固定題數或手動 Finish 完結。
- Summary flow 會顯示本局主要統計，render 後清除 `quiz_session`，避免完成後被誤判為 unfinished quiz。
- Summary page 已提供返回 Home 嘅明確離開路徑。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- Summary page wording / layout 之後可再整理；目前先以 logic flow 可測試為主。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Overdue weight boost**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 用 `last_quiz_at` 幫太耐冇出現嘅 vocab 做 weight boost。
- 決定各階段等待時間、每次加幾多、high value 幾多。
- 研究 management command + cron、Celery Beat 或其他 scheduler。
- 計算 average weight 時要以每個 user 自己嘅 `UserVocab` 為範圍。

## Logging / Audit Trail


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **CSV import log / import report**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `import_vocab` 已整理出 `success_count`、`failed_rows`、`row_number`、`error_message` 等 structured data。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 輸出正式 log，而唔只係 terminal message。
- Log 記低 import file、執行 admin、執行時間、成功筆數、失敗筆數、failed row 原因。
- 可以先做 terminal summary + log file。

## General Improvements


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 A：Model `__str__()`**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已為 `Vocab`、`VocabRequest` 等 model 加 `__str__()`，admin 同 debug 時更易睇。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 B：Service class naming style**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已將 `vocabRequestService` rename 做 `VocabRequestService`。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **改善 C：清理未用 import / commented code**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 清走未用 imports。
- 清走舊 commented query / obsolete code。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **改善 D：補 tests**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- Duplicate request tests。
- Create / update / delete request flow tests。
- Approve / reject flow tests。
- Admin concurrency / reviewed request readonly tests。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 E：Project dependencies file**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已加入 `requirements.txt`，記錄目前 project runtime dependencies。
- 已加入 `requirements-dev.txt`，記錄 development / asset generation 需要嘅 dependencies，例如 Pillow。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **改善 F：Production settings hardening**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 正式 deploy 前，將 `SECRET_KEY`、`DEBUG` 等 settings 搬去 environment variables。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 G：Whitespace cleanup**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已執行 `git diff --check` 檢查目前 diff。
- 檢查完成後沒有需要繼續追蹤嘅 whitespace cleanup item。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 H：Approve request final validation**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- User submit CREATE request 時允許部分 proposed fields 留空。
- Admin approve 時先驗證最終 proposed data 是否足夠。
- 資料不足時會留喺 review page 顯示錯誤，唔執行 vocab action。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 J：收窄 `UserVocab` bulk in-use update POST validation 範圍**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Update 時已有 `user=request.user` 保護，暫時唔會改到其他 user 資料。
- 正常 browser submit 只會提交當前 page 嘅 `selectable_ids`。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 如要更嚴謹，可以喺 POST 時重新 paginate queryset，將當前 page `object_list` 傳入 form 作 validation queryset。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 K：User admin summary field + filtered link**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- User admin detail page 已改用 readonly function field 顯示 user vocab count。
- Count field 會提供 link 去 filtered `UserVocabAdmin` list。
- `UserProfile.last_vocab_sync_at` 已用 readonly function field 顯示。
- 已放棄用 `UserVocabInline` 長期顯示大量 user vocab。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 L：Quiz question pool query performance review**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `QuizService.pick_random_vocab()` 已改用 `values_list("id", "weight")`，只拉抽題需要嘅欄位。
- 已移除抽題前額外 `.count()` 嘅需要，改用 Python list 判斷有冇候選題。
- Weighted random 仍然保留 total weight、cumulative weight 同 `bisect_left` 嘅做法。

<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 如果日後 quiz pool 大到現有 Python list 計算變慢，再研究 DB-level weighted random 或更完整嘅抽題 cache strategy。

## UI / UX


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **50 音假名 keyboard**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 50 音 keyboard 只用於 quiz answer UI；search 同 vocab request 等一般 forms 繼續使用系統 keyboard。
- Input panel 可按題目 type render 平假名或片假名 rows，並將按鍵輸入同步寫入 hidden answer 同畫面顯示。
- Kana controls 已支援 backspace、清音／濁音／半濁音雙向轉換、小假名／促音及片假名長音符號。
- Keyboard 可收起及重新顯示；Ajax submit、DOM replacement、tips 同 panel toggle 邏輯已集中到 quiz JavaScript modules。
- Multiple-choice panel 已預留 `mc_rows`／`mc-key` 結構，待相應答題 flow 接入。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可再將 `quiz_play.html` 入面剩低嘅 inline initializer 整理成更正式嘅 JS init pattern，令 template 更乾淨。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz kana background asset generator**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `generate_kana_bg.py` 可由 project root 產生 seamless hiragana、katakana 同 mixed background tiles／previews 到指定 export folder。
- Generator 可使用 WSL 可讀嘅 Windows Japanese font，避免 fallback font 缺少日文字形而輸出方格。
- 顏色、字體大小、密度、大小比例、字距同重複距離已集中到 `kana_bg_config.json`，並有 README 說明使用方法。
- 現有輸出採用配合 quiz 淺藍背景嘅灰藍色系。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可按 quiz page 實際畫面再微調 `kana_bg_config.json` 入面嘅顏色、密度同字體大小。
- 之後決定要用 800x600 tile 定 1600x1200 tile 作為實際 CSS background asset。
- 如之後正式接入 quiz UI，可將選定輸出 copy / export 到 `static/images/`。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Ajax partial pagination**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Vocab、UserVocab 同 UserEvent lists 已共用 Ajax partial pagination，同時保留普通 `<a href>` 作 non-JavaScript full-page fallback。
- Search、pagination、partial replacement 同 UserVocab select-all flow 已手動驗證。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可以考慮將 checkbox event binding 由 setup reload function refactor 成 event delegation。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Event notification page UI / wording polish**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Event list / detail 已可以顯示需要嘅資料，足夠支援整體 logic flow 測試。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可以整理 layout。
- 之後可以整理 read / unread visual state。
- 之後可以整理 wording 同 notification summary。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Japanese UI language and wording polish**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- Site UI language 之後統一改用日文。
- Button wording 之後集中整理，避免 logic phase 被 wording 細節卡住。
- Vocab request update / delete wording 要避免 user 誤會 request removal 係從自己 list 移除。
- Feedback / event / quiz result / user vocab detail wording 之後一併 polish。
- UserVocab detail page 之後整理 HTML 結構同 UI layout。

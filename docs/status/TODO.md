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
- User 選擇多個 sense 時，每個 sense 要有獨立 meaning、type、categories、questions 同 distractors，並保存成獨立 row；每個 row 嘅 `question1`／`question2` 只可以測試該 row 嘅 meaning，唔可以混合其他 sense。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 完成四種新 type 嘅 multiple-choice input panel、選項生成同 submit flow。
- 實作 `question1`／`question2` 嘅 blank、字面 `\n` 同活用提示 validation。
- 實作三個 distractor 對兩條題目嘅語義、句法、活用同 type validation，以及 view `get_context_data()` 選項 randomization。
- 更新 CSV import、model / related data structure 同測試，真正保存及使用新增五欄。
- 更新 `(word, kana)` unique rule，令同字同讀音可以按 sense 保存多個 rows，並同步定義新 identity／duplicate validation。
- 現有 `NewWord_YYYY_MM.csv` 只係測試品，由 user 喺正式啟用前自行刪除；skill 唔可以刪除、覆蓋或升級同名測試檔。舊 `resource/kanji*.csv` 暫時亦唔批量升級。
- 擴充 answer result comparison；目前只為 `vocab` 同 `katakana` 產生逐字比較結果。
- 驗證 create / update / restore / delete request、CSV import、detail view 同 admin flow 對四種新 type 嘅完整支援。
- 決定四種新 type 是否需要 `VocabDetail` 或其他 type-specific detail model；目前 `VocabActionService` 只為 `vocab`／`katakana` 建立 detail row。
- 加入各 type 嘅 end-to-end 測試後，先視為可正式匯入及出題。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Category multiple selection**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已新增 `Category` model。
- `Vocab.categories` 已改成 ManyToManyField。
- `VocabRequest.proposed_categories` 已改成 ManyToManyField。
- Vocab request form 已支援最多三個 categories。
- Create / update / restore request 已保存 proposed categories snapshot。
- Approve CREATE / UPDATE 時已同步寫入 `Vocab.categories.set(...)`。
- CSV import 已支援 `category1`、`category2`、`category3`。
- 已建立 `setup_categories` command 同 `resource/categories.csv`。
- Admin review form 已可查看 / 編輯 proposed categories。
- Vocab list / user vocab list search filter 已改用 M2M categories。
- Legacy single category field 已移除。
- 已手動測試 categories admin / request / import 主要 flow。


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
- Request creation 已使用 `transaction.atomic()`。
- Duplicate pending request 已有 application check + database conditional unique constraints。
- Service `IntegrityError` 已轉成 `ValidationError`，view 會回到 `form_invalid()`。
- Admin approve / reject 已改用 POST。
- Approve / reject 已使用 `transaction.atomic()`、`select_for_update()` 同 `PENDING` status check。
- Reviewed request 會變成 readonly，並由 `save_model()` 擋住再次保存。
- `VocabUpdateRequestForm.vocab_type` 已 readonly。
- Approve 前會 validate 最終 proposed data 是否足夠。
- Admin 會根據 service result 顯示成功 / warning feedback。
- 已手動測試 create / restore / update / delete request，以及 approve / reject flow。


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
- Login 成功後會呼叫 `UserVocabService.sync_new_vocab()`。
- Register 成功後亦會 sync 現有 vocab。
- `sync_new_vocab()` 已決定每次 sync 所有 user 未擁有嘅 vocab。
- `sync_new_vocab()` 已由逐個 `get_or_create()` 改成 `bulk_create(ignore_conflicts=True)`，減少大量 vocab sync 時嘅 query / insert round trip。
- UserVocab list 可以按 `in_use=True / False` filter。
- UserVocab list 已加入 bulk update flow，用 `selectable_ids` / `selected_ids` 更新 `in_use`。
- 已用 browser 測試 select all / checkbox 更新 `in_use` flow。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 如將來 vocab 數量大幅增加，可以再實測 `bulk_create()` 後嘅 sync performance。
- 如將來 user 需要大量管理 `in_use`，可以再改善 filtering / bulk action UI。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **UserVocab detail single-item management**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserVocabDetailView` 已有 ownership guard，限制目前 user 只能查看自己嘅 active user vocab。
- 已決定 `UserVocabDetail` 會分開顯示「My Vocab / quiz 狀態」同「Vocab master data」兩部分。
- `UserVocabDetailView` 已正式接入 URL。
- `UserVocabListView` item 已加入 detail link，可以由 user vocab list 進入單一 user vocab detail。
- Detail page 已開始顯示 user-specific data，例如 weight、streak、correct / incorrect count、last quiz、last answer。
- Detail page 已開始顯示 vocab master data，例如 word、kana、meaning、type 同 categories。
- Detail page 已加入 request update / request delete entry，連到既有 vocab request flow。
- Detail page 已加入單字 `in_use` update form，用嚟控制該 vocab 是否加入自己嘅 quiz pool。
- Detail page 已顯示 `in_use` checkbox。
- `UserVocabDetailView` 已可處理 POST，更新目前 object 嘅 `in_use` 後 redirect 返 detail page。
- `get_context_data()` 已避免覆蓋 POST invalid 時傳入嘅 bound form。

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
- `EventService.gen_vocab_sync_event()` 已根據 `Vocab.update_at > last_vocab_sync_at` 找出變化。
- CREATE request 會獨立計算。
- UPDATE / RESTORE / DELETE 會按 sync window 內最新 non-CREATE approved request 分類。
- 無對應 approved request 但 vocab 有變化時，暫時當成 admin / import created vocab fallback。
- `gen_vocab_sync_event()` 已接入 login flow。
- `gen_vocab_sync_event()` 已接入 user detail / profile page。
- 已手動測試 create / update / restore / delete / import 後 summary event 正常生成。
- 第一次 sync 已決定只設定 `last_vocab_sync_at`，唔產生歷史 vocab summary event。
- User 已可透過 event list / detail 查看 vocab sync summary event。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- `gen_vocab_sync_event()` 目前會對每個 changed vocab 查 related approved request；當 changed vocab 數量大時會有 N+1 query 風險，之後可改成一次預取相關 request 再喺 Python group。
- 如資料量變大，可以再優化 query 數量同 summary generation performance。
- 如 login / profile 兩個 request 同時觸發 `gen_vocab_sync_event()`，可能讀到同一個 `last_vocab_sync_at` 並建立重複 summary event；之後可考慮 profile row lock 或 event window idempotency。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Notification read / history**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已建立 unread event list view。
- User 可以喺 unread event list tick event 並 submit mark as read。
- Bulk mark read flow 已用 `selectable_ids` / `selected_ids` 限制提交範圍。
- Event list 已支援 Ajax partial pagination。
- `UserEventDetailView` 已限制只能查看目前 user 自己嘅 event。
- Navbar 已透過 context processor 顯示 unread event count。
- User 已可查看全部 event，包括 unread / read history。
- Event list 已可按 status 選擇 / filter，例如 all、unread、read。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- Mark all as read。
- Login 後首頁如需要，可以顯示更完整 notification summary。

## Data Import / Export / Database Migration


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **CSV vocab import command**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `import_vocab` 已支援 CSV path argument。
- 已加入 superuser authentication。
- 已加入 header validation。
- 已加入 row-level validation / error handling。
- 已經經 `VocabActionService` create flow 建立 vocab。
- Duplicate vocab 或 invalid row 會輸出錯誤並繼續下一行。
- 每筆 vocab creation 已由 service transaction 保護。
- 完成後會 show imported / failed rows count。
- 已保留每個 failed row 嘅行數及錯誤原因。
- 已支援最多三個 categories。


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
- 已建立 `Feedback` model / type / status 基礎。
- Feedback 暫時採用登入 user 才可提交，不開 anonymous public form。
- 普通 user 可以由前台提交 feedback。
- Feedback create 後會以 `PENDING` 作初始狀態。
- Superuser 進入 feedback 入口會 redirect 到 feedback list。
- 普通 user 進入 feedback 入口會 redirect 到 feedback create。
- Feedback list 已有固定 ordering，避免 pagination 使用 unordered queryset。
- Admin 可以進入 feedback list / detail 查看提交內容。
- Feedback list 已提供 detail link。
- Admin 可以 reply feedback。
- Reply 後 feedback status 會更新成 `REPLIED`，並寫入 `reply_by` / `reply_at`。
- Reply 後會建立 `FEEDBACK_REPLY` event 並 assign 俾提交 feedback 嘅 user。
- 已手動測試普通 user create、superuser list / detail / reply、feedback status update 同 user event creation。


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

- 已決定建立 quiz form，俾 user 選擇今次想考嘅 vocab type、level、category。
- `QuizSettingForm` 已建立 `vocab_type`、`level`、`categories` 三個 filter fields。
- 三個 filter fields 已暫時使用 checkbox UI，方便 user 複選出題範圍。
- `QuizService.create_question_pool()` 已建立初稿，會由目前 user 嘅 `UserVocab` 建立 question pool。
- Question pool 已支援 `in_use=True`、vocab type、level、categories filter。
- `QuizSettingView` 已將 `QuizSettingForm.cleaned_data` 保存到 session，並由 `QuizPlayView` / `QuizNextView` 傳入 `QuizService.create_question_pool()`。
- Empty filter 選項已喺 `create_question_pool()` 用 truthy check 處理，代表「不限制該條件」。
- `create_question_pool()` 已支援單一條件、複數條件、無條件 filter 組合。
- Filter 後無題時已加入 fallback strategy：改用目前 user 嘅 full active vocab pool，並回傳 `fallback_used` flag。
- `QuizSettingView` 已用 `QUIZ_MIN_IN_USE_VOCAB_COUNT` 檢查 user active vocab 數量；不足時會 redirect 去 user vocab list 並顯示 warning message。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- Filter fallback / no active vocab warning message 之後可再配合 template 顯示得更清楚。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz setting use-last-setting guard**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 如果 user 第一次進入 quiz setting 就勾選 `use_last_setting`，但 session 入面未有 `quiz_settings`，會回到 invalid form。
- `QuizSettingView.form_valid()` 已檢查 previous settings 是否存在；不存在時會加 `use_last_setting` field error。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz view routing and result flow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Quiz basic flow 已有初稿：setting page -> random `UserVocab` question -> answer form -> result page。
- `QuizSubmitAnswerView` 已用 `get_object_or_404(UserVocab, pk=..., user=request.user)` 防止 user 改 hidden id 操作其他 user 嘅 vocab。
- 已重新釐清 Ajax partial flow：View 應按 user action 分工，partial 只代表 UI state。
- 已決定 `quiz_result_partial.html` 不一定需要獨立 `QuizResultView`；答題 submit action 可以直接 render result partial。
- 已決定 result partial 入面嘅 Next button 應 call next-question endpoint，再由該 endpoint render question partial。
- Quiz flow 已開始重整成 full page shell + action endpoints：
  - `QuizPlayView` render quiz full page shell / 第一題 question partial。
  - `QuizSubmitAnswerView` 做 answer checking、stats update，然後 return `quiz_result_partial.html`。
  - `QuizNextView` 負責抽下一題，然後 return `quiz_question_partial.html`。
- 已移除獨立 `QuizResultView` 方向，改由 submit answer action 直接 render result partial。
- 已移除 answer data 放 URL path 嘅方向，改由 POST body / form data 傳入。
- `QuizForm` 已加入 hidden `user_vocab_id`，用嚟表示目前 answer form 對應邊個 `UserVocab`。
- `QuizNextForm` 已建立成空 form，`QuizNextView` 已改用 next-only form，避免要求 answer fields。
- `QuizSettingForm.quiz_num` 已改用 `TypedChoiceField(coerce=int)`，避免 quiz count 由 form / session 傳到 template 後變成 string 而影響大小比較。
- `QuizSettingRequiredMixin` 已建立，並用 `dispatch()` 喺 `QuizPlayView` / `QuizNextView` 進入前檢查 session 入面是否有 `quiz_settings`。
- `QuizSessionRequiredMixin` 已建立，並用喺 submit / next / skip 等需要現有 quiz session 嘅 endpoints。
- `QuizSubmitAnswerView` 已從 session 讀取目前題目嘅 `fallback_used` flag，並傳入 result partial context。
- `QuizSubmitAnswerView` 已檢查 POST 入嚟嘅 `user_vocab_id` 是否等於 `quiz_session["question_user_vocab_id"]`，避免 hidden id 指向非目前題目時污染 stats / weight。
- Hidden id mismatch 時，如 session 仍有目前題目，會重新 render session 入面真正題目；如 session 已無目前題目，會回 no-question partial。
- `QuizNextView` 已將新題目嘅 `fallback_used` flag 保存到 session，方便 submit answer 後 result partial 判斷是否顯示 Next。
- `tips_count` 已改成 hidden field，準備由 question form 以 hidden/default value submit。
- `UserVocab.last_answer` 已加入 model / migration / admin display，準備俾 result partial 顯示 user 最近一次答案。
- `quiz_session` 已同 `quiz_settings` 分開，開始追蹤目前題目、fallback 狀態、答題數、正確數、錯誤數、skip 數同 tips 總數。
- `quiz_play.html` 已建立 full page shell，並用 `quiz-area-container` 包住可被 Ajax replace 嘅 question / result partial。
- `quiz_question_partial.html` 已建立 answer POST form，包含 hidden `user_vocab_id` 同 hidden/default `tips_count`。
- `quiz_result_partial.html` 已建立 next POST form，會 call `QuizNextView` 再換入下一題 partial。
- 前端 Ajax submit / replace flow 已接上 `form.action`，可根據 answer form / next form 指向對應 view。
- Result partial 已用 `fallback_used` 控制是否顯示 Next button。
- Result partial 已按 `total_quiz_num` / `current_quiz_num` 控制 Summary button 同 Next button 顯示。
- Ajax quiz flow 已手動測試成功：50 音 keyboard 可將答案寫入 hidden input，submit answer 後可局部更新成 result partial，Next 可再局部更新成下一題。
- Quiz Ajax response 已改成 JSON contract，分開回傳 `main_html` 同 `input_panel_html`，讓 main question/result area 同 input panel area 可以分開 replace。
- `QuizNextView` 已根據下一題 `VocabType` 產生對應 input panel context，準備支援 hiragana keyboard / katakana keyboard / multiple choice panel。
- Quiz question form 已開始提供 tips button，並準備透過 `data-correct-answer` 俾前端讀取正確答案作提示處理。
- `quiz_result_partial.html` 已顯示基本答題結果，包括題目、正確答案、user submitted answer 同 correct / wrong 狀態。
- `quiz_no_question_partial.html` 已加入基本訊息同 back to settings link，避免 no-question case 顯示空白。
- Tips button 前端提示邏輯已完成初稿，會按正確答案修正 / 補完 hidden answer input，並同步更新 answer display。
- `tips_count` 已會隨 tips click 正確遞增，並會跟 answer form 一齊提交到 backend。
- `QuizSkipForm` / `QuizSkipView` / `quiz_skip` URL 已建立，question partial 已有獨立 skip form。
- Skip form 已沿用 Ajax JSON contract，skip 後會局部更新下一題或 no-question partial。
- `build_next_question_payload()` 已抽出共用 next-question payload 建立流程，供 `QuizNextView` 同 `QuizSkipView` 重用。
- Skip 後如 user filter pool 已無可用題目，會回傳 no-question partial，引導 user 返設定 / vocab list。
- Skip 後會先清空 `quiz_session["question_user_vocab_id"]`，再嘗試抽下一題，避免已 skip 題目被當成未完成題目。
- Skip flow 已傳入 `is_skip=True`，令 skip 後抽出嘅下一題不會增加 `quizzed_count`，避免有限題 quiz 因大量 skip 而超出目標題數。
- `QuizUnfinishedView` 已可按 session 入面未完成題目重新 render quiz page；如 session 無目前題目，會嘗試抽一題新題繼續。
- `QuizUnfinishedView` 已補返 `current_quiz_num` / `total_quiz_num` context，避免由 unfinished flow 入返 quiz page 時 quiz count 顯示唔到。
- `QuizSettingView` 已處理有限題 quiz 中途離開後返回嘅 lifecycle：未答題會 resume 同一題，result page 離開但未答晒會繼續下一題，有限題已完成則清走 `quiz_session`。
- 暫時所有 quiz answer submit 都走 kana answer checking flow，避免 katakana 題目未正式拆 type 前被直接當 wrong。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- `quiz/views.py` 入面嘅 `get_input_panel_rows()`、`render_quiz_question_payload_html()`、`build_next_question_payload()` 暫時可以接受；之後 flow 穩定後可移去 `quiz/view_helpers.py`，令 views 保持專注處理 request / response。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Weighted random question selection**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserVocab` 已有 `weight` field。
- 已決定 question pool 會來自目前 user 嘅 `UserVocab`。
- 已決定 weight 越高，被抽中機會越高。
- 已決定唔用 `random.choices()`。
- 已決定自行計算 total weight，再用 cumulative weight + `bisect_left` 搵中獎項目。
- `QuizService.pick_question()` 已建立初稿，會計算 total weight、cumulative weight，並用 `bisect_left` 抽題。
- `UserVocab.weight` 已加入 `MinValueValidator(1)`，避免正常 form / admin validation 接受 0 或負數。
- `UserVocab.weight` validator migration `0024_weight_add_min.py` 已建立。
- Weight adjustment 參數已抽到 `quiz/config/quiz_config.json`。
- `check_kana_answer()` 已根據 answer result、tips count 同 streak 更新 weight。
- `skip_question_punish()` 已根據 config 增加 skipped vocab weight。
- Service layer 已用 `min_weight` clamp，避免 weight 跌穿最低值。
- `streak_correct` / `streak_wrong` 已改成較清楚嘅 config key。


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

- `UserVocab` 已有 `streak`、`correct_count`、`incorrect_count`、`last_quiz_at`。
- 已決定 streak 基本規則。
- `check_kana_answer()` 已開始處理 correct / incorrect count、streak、`last_quiz_at`，並 save 回 `UserVocab`。
- `check_mc_answer()` 已開始處理 correct / incorrect count、streak、`last_quiz_at`，並 save 回 `UserVocab`。
- `check_kana_answer()` / `check_mc_answer()` 已保存 `last_answer`，方便 result partial 顯示 user 上一次提交嘅答案。
- 已決定 tips button 只要被按下就應增加 `tips_count`，即使 user 原本已經輸入完整正確答案，因為「需要確認」本身代表掌握度未夠穩。
- `skip_question_punish()` 已建立，skip 時會檢查 `UserVocab` 是否屬於目前 user，再更新 weight、streak 同 `last_quiz_at`。
- `check_kana_answer()` 已將 submitted `tips_count` 納入 weight calculation。


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

- `quiz_session` 已開始保存整局 quiz 嘅統計資料，包括 `aims_quiz_num`、`quizzed_count`、`correct_count`、`wrong_count`、`skipped_count`、`total_tips_count`。
- Answer submit 後已會更新 correct / wrong count、tips total，並將 nested session dict 寫返入 `request.session["quiz_session"]`。
- Skip 後已會更新 skipped count，並將 nested session dict 寫返入 `request.session["quiz_session"]`。
- Next / skip 抽到新題時已會更新 `question_user_vocab_id`、`fallback_used` 同 `quizzed_count`。
- Skip 抽下一題時已不增加 `quizzed_count`，所以 skipped question 不計入已答題數。
- `QuizSummaryForm` / `QuizSummaryView` / `quiz_summary_partial.html` 已有初稿。
- Summary partial 已可顯示本局答題數、目標題數、正確數、錯誤數、skip 數同 tips 使用量。
- Summary response render 完後已用 `session.pop("quiz_session", None)` 清走 quiz session，避免完成後再入 setting 被誤判成 unfinished quiz。
- Quiz 已支援固定題數完結。
- Quiz 已支援手動 finish button 完結。
- Summary page 已加入返回 Home 嘅 link，提供明確離開路徑。


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

- 只用喺 user 回答 quiz 嘅介面。
- Vocab search、create request、update request 等其他 forms 繼續使用普通 keyboard。
- 已建立平假名 / 片假名 keyboard rows constants，並由 quiz view 傳入 input panel partial。
- 已建立 `quiz_input_panel_partial.html`，用 button rows render 假名 keyboard。
- 已建立 `kana_input.js`，將 keyboard input 寫入 hidden answer input，並同步更新畫面顯示。
- 按下假名後，可將文字插入 quiz answer hidden input。
- 已初步支援 backspace、濁音、半濁音同小假名轉換。
- 已將 kana input 字串處理 function 拆到 `static/js/quiz/kana_input.js`。
- Input panel 已可按題目 type 使用平假名 rows 或片假名 rows。
- Multiple choice panel 已有 `mc_rows` / `mc-key` placeholder 結構。
- 濁音 / 半濁音 handler 已支援反向轉換，可由濁音 / 半濁音切回清音。
- 小假名 handler 已加入促音 `っ` 處理。
- 片假名 keyboard rows 已加入長音符號 `ー`。
- Hide keyboard button 已可收起 input panel，外層 show keyboard button 可再次顯示 input panel。
- Quiz Ajax submit / DOM replace / tips / keyboard toggle JS 已移到 `static/js/quiz/quiz_play.js`。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可再將 `quiz_play.html` 入面剩低嘅 inline initializer 整理成更正式嘅 JS init pattern，令 template 更乾淨。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz kana background asset generator**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已建立 `devtools/image_generator/generate_kana_bg.py`，用嚟生成 seamless kana background tiles。
- Generator 已固定可由 project root 執行，並輸出到 `assets/export/background/kana_bg_output_blue/`。
- 已加入 WSL 可讀嘅 Windows Japanese font path，避免 fallback 到無日文字形嘅 font 後輸出方格。
- 已將字色、底色、字體大小、大小出現比例、字數、字距同同字重複距離抽到 `kana_bg_config.json`。
- 已建立 `devtools/image_generator/README.md`，記錄 config 各項數值用途同 generator 執行方式。
- 已調整 kana background 字色為灰藍色系，配合目前淺藍底色。
- 已生成 hiragana、katakana 同 mixed 三組 tile / preview image。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可按 quiz page 實際畫面再微調 `kana_bg_config.json` 入面嘅顏色、密度同字體大小。
- 之後決定要用 800x600 tile 定 1600x1200 tile 作為實際 CSS background asset。
- 如之後正式接入 quiz UI，可將選定輸出 copy / export 到 `static/images/`。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Ajax partial pagination**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `VocabListView` 已支援 Ajax partial pagination。
- `UserVocabListView` 已支援 Ajax partial pagination。
- `UserEventListView` 已支援 Ajax partial pagination。
- Pagination link 保留普通 `<a href>`，non-JavaScript fallback 可完整 reload page。
- Search + pagination + Ajax partial update 已手動測試。
- UserVocab checkbox select-all flow 已手動測試。


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

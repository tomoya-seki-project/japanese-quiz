# Project TODO

呢份 TODO 用嚟追蹤 project 本身嘅 bug、功能、flow 狀態同改良。
舊版 TODO 內容已整合入目前格式。
未承諾、未納入目前 scope 嘅未來擴展 idea 統一放喺 `FUTURE_IDEAS.md`。

Status badge：

-  <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span>（81）：核心功能已完成，或已有明確 decision
-  <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span>（1）：已開始處理，但仍有必要項目未完成
-  <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span>（2）：未開始或暫時只係計劃

## 目錄

- [已 Check 到嘅問題 / Fix Tracking](#已-check-到嘅問題--fix-tracking)
- [Vocab Planned Work](#vocab-planned-work)
- [VocabRequest Result / UserVocab Flow](#vocabrequest-result--uservocab-flow)
- [Account / User Management](#account--user-management)
- [Event Notification System](#event-notification-system)
- [Data Import / Export / Database Migration](#data-import--export--database-migration)
- [User Message to Admin](#user-message-to-admin)
- [Quiz Question Logic](#quiz-question-logic)
- [Error Handling](#error-handling)
- [Logging / Audit Trail](#logging--audit-trail)
- [General Improvements](#general-improvements)
- [UI / UX](#ui--ux)

## 已 Check 到嘅問題 / Fix Tracking


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 1 點（VocabRequest / Admin Review）：真正實作 approve / reject request 嘅處理 flow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Approve 已按 CREATE / UPDATE / RESTORE / DELETE request type 呼叫對應 vocab action。
- Reject 會更新 request status 同 reviewer，但唔會改動 vocab；Reject submit 必須填寫 `review_note`。
- User 可在 CREATE／UPDATE／RESTORE／DELETE request 提供 optional `request_reason`；admin review page 會將 request reason 設為 readonly，並可另外填寫 review note。
- Approve／reject 結果 event 會使用 `review_note` 作訊息內容，將 reviewer 嘅補充說明傳回申請人。
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


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 24 點（VocabRequest Delete Snapshot）：DELETE request 保存完整 proposed snapshot**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- DELETE request 建立時會保存 word、kana、type、meaning、level 同 categories，令 admin review 見到提交當時嘅完整 vocab snapshot。
- Katakana vocab 會額外保存 `proposed_native_japanese`。
- Scalar fields、Many-to-Many categories 同 type-specific data 都在同一 transaction 內建立；Django system check 已通過。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 26 點（Quiz Answer Comparison）：限制 answer comparison 嘅最壞執行時間**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 新增 bottom-up `answer_compare_dp()`，以 `(m + 1) × (n + 1)` table 計算最佳路線，並由 `dp[0][0]` reconstruction 成原有 result format；`compare_kana_answer()` 已切換至新實作。
- 保留 minimum cost、最多 match、最多 non-normal wrong 同最終 `WRONG`／`MISSING`／`EXTRA` 次序；以舊 recursive implementation 作 oracle，比較 24,336 組 0 至 3 字元輸入，完整輸出無 mismatch。
- 25 對 25 全 mismatch targeted benchmark 約 0.0018 秒；Django system check 通過。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 27 點（Quiz Filter Fallback）：由 user 確認是否改用 full active pool**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已移除自動 fallback 同 `fallback_used` state；filtered pool 無題時唔再靜默提供設定範圍外嘅題目。
- 新增 no-pool confirmation page；user 可返回修改 quiz setting，或經 POST 明確確認使用 full active pool。
- Full-pool 選擇以 `use_full_pool` session flag 保存，原本 level、vocab type 同 categories 設定仍然保留；Next / Skip 會沿用同一 full pool。
- Setting 入口同 QuizPlay 無題分支會共用 `handle_insufficient_pool()` 檢查 full active/in-use pool；少過最低出題數量時返回 user vocab list 並顯示 warning，避免進入無法開始嘅 confirmation flow 或形成 redirect loop。
- Django system check、`git diff --check` 同現有 10 個 automated tests 已通過。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 28 點（Feedback Reply）：容許跟進回覆並以 CLOSED 作 terminal guard**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已確認產品規則：admin 可以先回覆 user 表示開始處理，其後再發送進度／完成通知；一般重複 reply 唔視為 bug。
- `FeedbackStatus` 已加入 `CLOSED`；reply form 可選擇回覆後結案，detail page 對 closed feedback 隱藏 Reply action。
- `reply_feedback()` 會喺 atomic transaction 內以 `select_for_update()` 重新取得 feedback；一旦狀態為 `CLOSED`，會喺建立 event 前拒絕後續回覆。
- View 會將 closed-state `ValidationError` 放回 reply form，避免直接 POST closed feedback 變成未處理 500；status migration 已建立。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 補一般多次 reply、reply-and-close、closed direct POST 同 concurrent close／reply 嘅 service / integration tests。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 29 點（Quiz Session）：失效題目與空 pool 嘅 terminal recovery**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Resume、正常／stale answer submit 同 skip 都會重新驗證目前題目屬於該 user、`in_use=True` 及 `vocab__is_active=True`。
- 目前畫面題目失效時會立即終止 quiz，唔會靜默換題；answer／skip learning state亦唔會被錯誤更新。
- Answer／skip 後 question pool 變空時會以 `quiz_ended` terminal state顯示提早結束 summary，並清除 `quiz_session`。
- 正常與提早完成共用 `build_quiz_summary_payload()`；`question_unavailable`／`no_question_pool` reason會提供相應 user feedback。
- Commit `89d3030` 已包含修正；Django system check、migration drift check同現有10個automated tests通過。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 補 M-01 integration tests，覆蓋 current question 被關閉／停用／刪除、pool 中途變空、resume、Next、Submit 同 Skip 嘅 response、database mutation及session cleanup。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- `build_next_question_payload()` 同 initial `QuizPlayView` 抽出 ID 後重新載入 object 仍有短暫 race window；之後可統一由原 eligible queryset 載入，並補 concurrency test。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 30 點（Account Email Identity）：統一 email canonicalization 與大小寫唯一性**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Custom `UserManager.normalize_email()` 會將完整 email `strip()` 後轉成 lowercase；registration、login、activation resend 同 admin create／change forms 共用同一規則。
- Registration 同 admin forms 以 `email__iexact` 提早攔截大小寫變體 duplicate，並保留清楚 validation message。
- `User` model 加入 `Lower("email")` database unique constraint 作最終 data-integrity guard；migration `accounts/0007_email_upper_lower_problem` 已套用。
- 現有 database 掃描結果為 0 組 case-insensitive collision、0 筆非 lowercase email；Django system check 同 migration drift check 通過。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 31 點（VocabRequest Notification）：`on_commit()` callback 失敗後 HTTP 結果不一致**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Staff notification 已採用 best-effort policy；CREATE／UPDATE／RESTORE／DELETE 四個 `transaction.on_commit()` callback 均設為 `robust=True`，通知失敗唔會再令已成功建立 request 嘅 HTTP flow 報錯。
- `create_event_for_admin()` 以獨立 atomic transaction 建立 event 及 staff assignments，避免 callback 中途失敗時留下部分通知資料。
- Django system check 已通過；如日後要求 guaranteed delivery，再評估 outbox + retry worker。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 補 callback-failure regression test，確認通知 exception 會被記錄，而 request row、service return value及 HTTP success response維持正確。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 32 點（Quiz Answer／Skip）：防止並行重複處理同一題**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 每次出題會建立帶唯一UUID token嘅`QuizAttempt(PENDING)`，session同Answer／Skip forms會保存同提交同一token；attempt同owner、`UserVocab`、status及`processed_at`均有持久化紀錄。
- Answer同Skip共用一次性狀態規則：service喺`transaction.atomic()`內先`select_for_update()`鎖attempt並重新檢查`PENDING`，再以固定`QuizAttempt → UserVocab`次序鎖learning row；`of=("self",)`收窄`UserVocab`鎖定範圍。
- Attempt決定真正`user_vocab_id`，server唔會直接信任browser指定更新目標；duplicate request排隊後會得到`already_processed`，唔會再次計分、改weight或執行skip punishment。
- View保留session token／question-ID consistency guard同結構化409 errors；stale request唔會清走較新題目嘅session。Frontend另有共用in-flight guard減少一般double click。
- PostgreSQL 16.15基準已確認migration套用、locking features及`FOR UPDATE OF self`可用；rollback smoke check覆蓋Answer／Skip首次成功及第二次`already_processed`，browser亦實際走過Answer path。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 補真正兩個database connections同時競爭同一attempt嘅`TransactionTestCase`或等效concurrency test，以及Answer／Skip完整integration tests；獨立test role及隔離database lifecycle已可運作，限制只剩測試案例尚未撰寫。
- Skip path已有service rollback smoke check，仍待補browser end-to-end regression coverage。

## Vocab Planned Work


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **MC schema foundation 與未完成功能隔離**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已確立 `adverb`、`mimetic`、`conjunction` 同 `colloquial` 採用 multiple-choice 答題，以及共用一個 `Vocab`／`UserVocab` progress、用多個 `MCSense` rows 保存各語意嘅基礎設計。
- `MCSense` schema foundation 已包含 `Vocab` ForeignKey、`sense_no`、`sense_key`、meaning、兩條 questions、三個 distractors、明確 table name，以及 `(vocab, sense_no)` database constraint；migration `0027_add_mc_sense` 已納入版本紀錄。
- `VocabDetail` 繼續保存一般 `vocab` type 嘅額外資料，MC-specific 題目資料由 `MCSense` 獨立承擔，避免兩種資料用途混合。
- 未完成嘅 MC flow 已從 v1.0.0 scope 隔離：migration `0028_vocabtype_cut_out_mc` 將正式 choices 限制為 `vocab`／`katakana`，request form、admin approve、CSV import 同 service亦會阻止未支援嘅 MC type 寫入。
- 隔離完成時，local database 已確認冇 MC type `Vocab`／`VocabRequest`；`manage.py check` 同 `makemigrations --check --dry-run` 均通過。完整 MC content contract、import／request／quiz flow 同測試已移到 `FUTURE_IDEAS.md`，留待 v1.0.0 後重新啟動。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Category multiple selection**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已新增 `Category` model；`Vocab` 同 `VocabRequest` 已改用 ManyToMany categories，legacy single-category field 已移除，相關 search亦已配合。
- 共用 `validate_category_count()` 集中定義最多三個嘅規則，並支援按 lifecycle 指定下限。
- User request 同 pending request admin form 容許 0～3 個 categories；approve、正式 Vocab admin form 同 `VocabActionService` create／update 強制 1～3 個。
- `VocabActionService` 會喺 transaction／database write 前執行最終 validation；CSV import 支援 `category1`～`category3` 並經同一 service 繼承規則，基礎資料由 `resource/categories.csv` 同 `setup_categories` 管理。
- Django system check、validator 0／3／4 邊界及 service 0／4 寫入前拒絕 probe 已通過。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 補 category count regression tests，覆蓋 request 0／3／4、正式資料 0／1／3／4、兩個 admin form wiring、approve validation 同 service create／update failure path。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 將來如 category 數量增加，可以再改善 admin/search UI。


## VocabRequest Result / UserVocab Flow


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **VocabRequest core workflow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- CREATE / UPDATE / RESTORE / DELETE request creation flow 已完成。
- Request creation、approve 同 reject 均經 service transaction 處理；review action 使用 POST、row lock 同 `PENDING` guard 防止重複處理。
- `VocabRequest` 分開保存 optional `request_reason` 同 `review_note`：前者由申請人提供並在 admin readonly 顯示，後者由 reviewer 填寫；Reject 時由 admin form 動態要求 review note 必填。
- Review 完成後，結果 event 會以 `review_note` 作訊息內容通知申請人。
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


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Account email activation**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Public registration會建立 `is_active=False` user；Admin add-user維持active預設，未認證帳戶唔會預先建立 `UserVocab`。
- 專用stateless token綁定user id、password、email、timestamp及 `is_active`，24小時後過期；GET只顯示確認，POST先啟用，成功後舊link失效並執行resilient vocab sync。
- Registration會建立完整activation URL、用日文template寄信並進入檢查email頁；email backend已改由environment variables配置，未提供設定時保留console backend作development fallback。
- Resend支援email驗證、inactive-only寄送、統一回應及每個user 60秒cache cooldown；registration首封信亦會啟動cooldown，寄信失敗會釋放key。
- 寄信回傳0或拋exception會記錄安全audit context；registration失敗會保留inactive account並引導resend，resend失敗則維持不洩漏account狀態嘅統一回應。
- Zoho SMTP已使用App Password、真正登入mailbox同已批准寄件alias接通Port 465 implicit SSL；connection test、真實寄送及mailbox收件確認成功，敏感設定只保存在Git忽略嘅 `.env`。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 將目前temporary diagnostics轉成正式accounts automated tests，覆蓋registration、email內容、valid／invalid／expired／reused token、inactive login、resend cooldown、寄信失敗及activation後vocab sync。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 正式部署仍要配置HTTPS site domain、共享cache、production secret management及environment validation；亦要補齊 `.env.example` email keys，並確認SPF／DKIM／DMARC同寄送監控。
- 如之後增加admin resend、background task或更多caller，可將activation email function由view module移到accounts service層。


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
- Login／account activation後會由 `UserVocabService.sync_new_vocab()`補齊 user尚未擁有嘅 vocab，並以 `bulk_create(ignore_conflicts=True)`減少同步成本；inactive registration唔會預先建立關係。
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


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **由 SQLite 轉用 PostgreSQL**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Django database backend已切換到PostgreSQL，加入Psycopg 3同`python-dotenv`；五項database connection values由未追蹤`.env`提供，`.env.example`保存無secret設定格式。
- 今次採用fresh-database策略：用既有migrations重建schema，再重新建立admin user及匯入category／vocab基礎資料；並非將舊SQLite records自動搬移到PostgreSQL。
- 2026-09-15 runtime驗證確認PostgreSQL 16.15、Django vendor為`postgresql`、24張tables、全部migrations已套用，users／categories／vocabs均已有資料，row-lock features可用。
- README已改為PostgreSQL local setup；完整轉換步驟、role權限、驗證同限制另有development report記錄。舊SQLite file唔再係目前Django runtime backend。
- 已建立獨立`japanese_quiz_test` role並授予`CREATEDB`；Django成功建立／刪除`test_japanese_quiz`、重播全部migrations並完成現有10個tests。正常application role繼續保持`NOCREATEDB`。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- Production secrets、backup／restore、service provisioning同deployment automation仍屬production hardening；唔將今次local development backend轉換誤當成production database rollout。


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
- Filter 後無題會先進入 confirmation page；user 可返回 setting，或經 POST 明確改用 full active／in-use pool。Full pool 數量不足則 redirect 到 user vocab list 並顯示 warning。


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


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz result answer difference display**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `QuizService.answer_compare_dp()` 以 bottom-up DP 產生 `MATCH`、`WRONG`、`MISSING`、`EXTRA`，並處理答案長度不同、位置對齊及 subtype tie-break。
- `compare_answer_subtype.json` 可分辨 `NORMAL`、`DAKUTEN`、`HANDAKUTEN`、`SMALL_KANA`，包括 `そうぞう`／`そそく` 等錯位情況。
- `kana_graphic_map.json`、static kana assets 同 `QuizService.gen_answer_image()` 已可將 compare result 轉成主圖及 `sub_image_path` graphic data。
- `QuizSubmitAnswerView` 已將 graphic data 傳入 result partial，畫面可顯示 answer difference 圖片及 missing／extra mark 資料。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- `gen_answer_image()` 之後可以加入 fallback image / fallback text，避免 mapping 漏項時 render 出 broken image path。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz session summary tracking**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `quiz_session` 會保存目標／已答題數、correct／wrong、skip、tips、目前題目同 fallback 狀態，answer、next 同 skip 後均會同步更新。
- Skipped question 唔計入 `quizzed_count`；quiz 可按固定題數或手動 Finish 完結。
- Summary flow 會顯示本局主要統計，render 後清除 `quiz_session`，避免完成後被誤判為 unfinished quiz。
- Summary page 已提供返回 Home 嘅明確離開路徑。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- Summary page wording / layout 之後可再整理；目前先以 logic flow 可測試為主。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **移除 Quiz action endpoints 嘅空 Django Forms**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Next、Skip 同 Summary 已改用普通 `View.post()`；full-pool confirmation 使用 `TemplateView` 處理 GET rendering，並以自訂 `post()` 執行確認 action。
- 四個無 fields／validation 嘅 Form classes、相關 imports、action views 嘅 form plumbing 同 confirm template 內無輸出嘅 `{{ form.as_p }}` 已移除。
- HTML forms、CSRF token、既有 endpoints、login／quiz setting／quiz session mixins、AJAX payload 同 domain guards均保留。
- Next、Skip、Summary同 full-pool confirmation 已手動驗證可運作；Django system check、migration drift check、現有 10 個 tests同 `git diff --check` 通過。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 補四個 action endpoints 嘅 integration tests，確認只接受預期 method、guard redirect、session mutation、CSRF 同 AJAX response無 regression。

## Error Handling


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **HTTP error response、error page 同 exception logging**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已建立獨立 `errorHandler` app，註冊 `400`、`403`、`404`、`500` 全域 handlers 及對應 templates；template loader 可正常找到錯誤頁，並已移除臨時 exception output。
- 以 `DEBUG=False`同臨時URLConf實際觸發400／403／404／500，四個全域handlers均回傳正確HTTP status及HTML response；測試exception內容、traceback同filesystem path冇洩漏到頁面。
- Quiz Submit AJAX 會以 `400` JSON 回傳 form validation errors；Next／Skip／Summary 已移除無實際 validation 嘅空 Form plumbing。前端亦會在 parsing 前檢查 `Content-Type`，將非 JSON HTTP errors、network failure 同 parsing failure 導向通用 fallback。
- Login、register 同 user detail 已共用 `UserVocabService.sync_vocab_safely()`：vocab sync 失敗會記錄 exception traceback 並留待下次重試；sync 成功後 event generation 失敗會保留 sync，而 event rows、user assignment 同 sync checkpoint 由 `gen_vocab_sync_event()` 自己嘅 atomic transaction 一組 rollback。Admin approve／reject 及結果 event 則維持同一 transaction、一併成功或 rollback。
- `500` handler 已改用獨立 template render path，不傳入 request context，避免再次執行全站 context processors；`error500.html` 亦不依賴 `base.html` 或 database data。
- Application logging 已設定 formatter、console 及每日 rotating file handlers、exact-DEBUG filter、app loggers 同 `django.request`；並以 `.gitkeep` 保留 log directory、`.gitignore` 排除 runtime `.log` files。已用 project `.venv` 嘅 Django 6.0.5 通過 system check，並實測 console、DEBUG、INFO+ 同 ERROR+ file routing 正確。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 驗證每日 rotation／retention，以及未處理 500 只保留一次完整 traceback。
- 模擬 context processor 失敗，驗證獨立 `500` fallback 仍可回應 status 500 及錯誤頁內容。
- 以browser integration實測 Quiz AJAX收到403／404／500 HTML時會進入通用fallback；目前環境冇Node／JavaScript parser，未有JavaScript runtime或browser自動驗證。
- 為四個全域handlers、Quiz invalid-form JSON contract同非JSON前端fallback補永久自動tests；目前project test discovery顯示 `0 tests`，現有證據來自system check、direct request、MRO同臨時URLConf驗證。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 日後可按需要加入 structured logging、request ID 同 error monitoring service；目前唔屬於基礎 error handling 必要範圍。

## Logging / Audit Trail


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Application logging coverage / placement**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已設定 formatter、console／daily rotating file handlers、7 日 retention、exact-DEBUG filter、`django.request` 同各 app loggers；實測 DEBUG／INFO+／ERROR+ routing 正確，runtime log files亦已排除於 Git。
- Vocab request／admin review、UserVocab `in_use` 變更同 sync 已覆蓋重要 outcomes；sync 會以 per-user row lock 串行化，只有 database 實際新增 rows 先記 `created_count` success，零新增保持安靜，sync／event failure各自保留 traceback。
- Quiz 已記錄 setting／resume／pool rejection、stale或 duplicate answer、會改 learning state嘅 answer／skip 同 summary；普通 question pick同 next唔記低價值 log。
- Account registration／login、event bulk mark-read、feedback create／duplicate／reply同 admin permission denial已記錄必要 audit context；零變更mark-read保持安靜，亦唔記 credentials、session、feedback body或完整POST data。
- `import_vocab`、`setup_categories`同`dev_clear_vocab`已記錄 started／completed、summary、預期 rejection同未預期 traceback；destructive command只有完整 transaction成功後先記 completed。
- Log wording、snake_case operation同`*_id` fields已統一；底層Vocab／Event helpers、logout、普通read views同未處理500唔重複記錄，避免噪音、敏感資料同雙重traceback。Python compile、Django system check同diff check已通過；project目前仍未有自動tests。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 為 Vocab request／admin review、UserVocab `in_use`／sync、Quiz同 Account／Event／Feedback flows補 log assertions，確認 level、IDs、counts、zero-change silence同敏感資料邊界。
- 為三個 management commands補成功、預期 rejection同未預期 failure assertions，確認summary、transaction完成點同traceback正確。
- 模擬同一 user concurrent sync，驗證只有實際新增 rows嘅執行記success count，零新增執行保持安靜。
- 確認真正 exception只出現一次完整 traceback，預期 validation／duplicate唔會變成500或`ERROR`，亦唔會被 Django同application logger重複記錄。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 如日後需要 security monitoring，再按實際異常量決定 403／404、permission denial 或可疑操作嘅額外策略；普通 404 唔當成 application error，亦唔阻止目前 logging coverage 完成。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **CSV import / category setup log and report**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `import_vocab` 保留 terminal row result 同 final summary，並以 `success_count`、`failed_rows`、`row_number` 同 `error_message` 組織執行結果。
- Import start／finish log 會記錄 operation、執行 user、CSV file、成功筆數同失敗筆數；formatter timestamp 提供執行時間。
- Missing file／headers、database integrity rejection 同 validation rejection 會以 `WARNING` 記錄；未預期 exception 會以 `ERROR` level 保存完整 traceback後重新拋出。
- Log 只記識別及診斷所需資料，唔會記錄 admin password。
- `setup_categories` 同樣保留 terminal row／summary output，並記錄 CSV file、成功／失敗筆數、invalid row、missing file／headers 及未預期 crash。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 為兩個 CSV commands 補 log assertions，覆蓋成功、部分 row 失敗、missing file／headers 同未預期 crash，並確認 level、summary count 同 traceback 正確。

## General Improvements


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 A：Model `__str__()`**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已為 `Vocab`、`VocabRequest` 等 model 加 `__str__()`，admin 同 debug 時更易睇。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 B：Service class naming style**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已將 `vocabRequestService` rename 做 `VocabRequestService`。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 C：清理 obsolete commented code**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 舊 `similar_word`、feedback constraint、UserVocab sync、Vocab update同舊 view flow等 obsolete commented code已清走。
- MC vocab types、MC request fields同對應 view branch係 v1.0.0後重新啟用功能嘅刻意 placeholders，因此保留；一般解釋 comments同 Django starter comments亦不屬於 obsolete code。
- Repository掃描確認冇殘留舊 `similar_word` references；Django system check同 `git diff --check`通過。


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **改善 D：補 tests**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已加入 10 個 UI／語系 regression tests，覆蓋全部 project templates compile、public/admin language boundary、Django built-in validation language、共用 choices、假名 keyboard event values、answer result escaping、notification recipient language同主要 detail labels。
- `manage.py test`、Django system check 同 migration dry-run 已通過。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- Duplicate request tests。
- Create / update / delete request flow tests。
- Approve / reject flow tests。
- Admin concurrency / reviewed request readonly tests。
- Quiz answer comparison correctness／performance tests，以及 filtered no-pool confirmation、full-pool initial／Next／Skip integration tests。
- Feedback repeated／concurrent reply idempotency tests。


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


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz Ajax accessibility announcement / focus management**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Quiz question、answer result 同 summary partial 已加入可由 JavaScript focus 嘅語意 heading；Ajax replacement 完成後會將 focus 移到新內容標題。
- Quiz 動態內容區使用 polite live region／atomic announcement，validation 同 request error 區使用 assertive alert，令輔助技術知道內容或錯誤已更新。
- Django system check、template compilation、`git diff --check` 同現有 10 個 automated tests 已通過。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Quiz answer comparison overlay display**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- `quiz_result_partial.html` 目前只係順序 render `image_path` 同 `sub_image_path`。
- 用 HTML / CSS 將 missing／extra mark 疊喺 kana 主圖上，避免 overlay 另佔一個位置。


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


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Japanese UI language and wording polish**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 一般 user-facing pages、forms、buttons、validation、feedback、event、quiz result 同 UserVocab detail wording 已統一使用日文；只供管理員使用嘅 admin／feedback review 介面維持英文。
- 新增 request-level language middleware，按頁面 responsibility 切換 `ja`／`en-us` 並於 response 後還原，避免 public 同 admin request 互相污染語系。
- 共用 choices、JLPT level、category、answer comparison type／subtype 同假名 keyboard 只修改顯示標籤，保留 database values及 JavaScript event values。
- 已加入對應 regression tests；10 個 tests、Django system check、migration dry-run 同 template compilation 全部通過。


<p style="margin-left:1.5em;"><strong>待測試</strong></p>

- 仍需 browser 逐頁 visual verification，確認長文案、mobile layout、Ajax partial replacement 同管理員／一般 user 實際操作畫面。

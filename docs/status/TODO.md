# Project TODO

呢份 TODO 用嚟追蹤 project 本身嘅 bug、功能、flow 狀態、改良同擴展預想。  
舊版 TODO 內容已整合入目前格式。

Status badge：

-  <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span>：核心功能已完成，或已有明確 decision
-  <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span>：已開始處理，但仍有必要項目未完成
-  <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span>：未開始或暫時只係計劃

## 目錄

- [已 Check 到嘅問題 / Fix Tracking](#已-check-到嘅問題--fix-tracking)
- [Vocab Future Work](#vocab-future-work)
- [VocabRequest Result / UserVocab Flow](#vocabrequest-result--uservocab-flow)
- [Account Email Activation](#account-email-activation)
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


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **第 3 點（VocabRequest / Admin Review）：確認 approve / reject permission boundary**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Approve / reject 已改為喺 admin change form 入面經 `response_change()` 處理。
- 正常入到 admin change page 已經會受 Django admin permission 控制。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 再確認目前 permission boundary 是否足夠。
- 決定 approve / reject branch 入面是否需要額外 call `has_change_permission()`。


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


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- 實作 email activation 時，拆成 public registration form 同 `UserCreationAdminForm`。
- Public registration 建立 `is_active=False` 的 user，等待 email activation。
- Admin 建立 user 時可以直接設定 `is_active=True`。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 19 點（Account Login）：移除 login flow 入面冇實際作用嘅 `user.save()`**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Django `LoginView` 已經會透過 authentication flow 更新 `last_login`。
- 已移除 login 成功後無欄位改動嘅額外 `user.save()`，避免多餘 database write。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **第 20 點（UserVocab Flow）：穩定 UserVocab 選擇頁 GET / POST 之間嘅候選範圍**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 原本嘅 `UserVocabSelectVocabView` 會每次 request 重新計算候選 vocab，GET / POST 之間可能出現候選範圍變動。
- 目前加字主流程已改成 login / register 後自動 sync 新 vocab，建立 `UserVocab(in_use=True)`。
- 舊 selection flow 暫時唔作為主要加字入口。


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **改善 I（VocabRequest）：Approve UPDATE / RESTORE / DELETE 前驗證 `original_vocab`**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- UPDATE / RESTORE / DELETE request flow 已依賴 `original_vocab` 作為目標 vocab。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- Approve 前檢查 `original_vocab` 是否存在。
- 檢查 `original_vocab` 狀態是否符合 request type。
- 如果資料異常，要停止 approve 並回傳清楚 error result。

## Vocab Future Work


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

## Account Email Activation


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Custom User Admin foundation**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `CustomizedUserAdmin` 已繼承 Django standard `UserAdmin`。
- Add form 會用 `set_password()`。
- Change form 會用 readonly password hash field。
- Admin user detail page 已用 function readonly field 顯示 profile data。
- User admin 已用 summary field + filtered `UserVocabAdmin` link 取代 `UserVocabInline`。
- `date_joined` / `last_login` 已放入 user detail readonly area。


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- 實作 email activation 時，拆開 public registration form 同 admin user creation form。


> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **UserProfile auto creation**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已加入 `accounts.signals`。
- User create 後會透過 `post_save` signal 自動建立 `UserProfile`。
- `INSTALLED_APPS` 已改用 explicit `AppConfig` path，確保 `AccountsConfig.ready()` 載入 signals。
- 目前 database 已重新 migrate，新 user 會自動有 profile。


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Account email activation**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 設計 registration 後是否即時限制 login。
- 建立 activation link flow。
- 決定 activation link expiry。
- 設計 resend activation email flow。

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **UserVocab sync and in-use flow**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserVocab.in_use` 已改成 default `True`。
- Login 成功後會呼叫 `UserVocabService.sync_new_vocab()`。
- Register 成功後亦會 sync 現有 vocab。
- `sync_new_vocab()` 已決定每次 sync 所有 user 未擁有嘅 vocab。
- UserVocab list 可以按 `in_use=True / False` filter。
- UserVocab list 已加入 bulk update flow，用 `selectable_ids` / `selected_ids` 更新 `in_use`。
- 已用 browser 測試 select all / checkbox 更新 `in_use` flow。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 如將來 vocab 數量大幅增加，可以再考慮 batch sync performance。
- 如將來 user 需要大量管理 `in_use`，可以再改善 filtering / bulk action UI。


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


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- Site announcement 可以之後加入 publish time、expire time、importance level、active status、target user group。


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


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- 之後可以加入 reviewer reason 或更詳細 result message。


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

- 如資料量變大，可以再優化 query 數量同 summary generation performance。


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Notification read / history**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已建立 unread event list view。
- User 可以喺 unread event list tick event 並 submit mark as read。
- Bulk mark read flow 已用 `selectable_ids` / `selected_ids` 限制提交範圍。
- Event list 已支援 Ajax partial pagination。
- `UserEventDetailView` 已限制只能查看目前 user 自己嘅 event。
- Navbar 已透過 context processor 顯示 unread event count。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- User 查看已讀 notification history。
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


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **User-to-admin message flow**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 俾一般 user 用普通 message 發一批想加入嘅 vocab 俾 admin。
- Message 唔需要 user 填 reading、meaning、type、category。
- Admin 可以喺後台睇 user message。
- Message 可以有 `UNREAD`、`READ`、`PROCESSING`、`DONE` 等狀態。
- Admin 整理資料後可建立 CSV，再用 `import_vocab` 加入 database。
- 處理完成後經 event system 通知 user。


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- 保留原本 user message 同最後 import batch 嘅關係，方便追蹤處理結果。
- 如果同一批 vocab 由多個 users 提出，要確保每個相關 user 都收到處理結果。

## Quiz Question Logic


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Quiz question filter**


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


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- Filter fallback / no active vocab warning message 之後可再配合 template 顯示得更清楚。


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Quiz view routing and result flow**


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


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 之後要將臨時 kana-only checking 拆返做正式 type-specific answer flow。
- `VocabType.VOCAB` / `VocabType.KATAKANA` 應走 kana checking，multiple choice type 應走 MC checking。


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


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- 如之後需要更精準嘅 recent skip，可只保存最近 10 個 vocab ids；暫時唔建立完整 question history model。


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **UserVocab quiz stats and streak update**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `UserVocab` 已有 `streak`、`correct_count`、`incorrect_count`、`last_quiz_at`。
- 已決定 streak 基本規則。
- `check_kana_answer()` 已開始處理 correct / incorrect count、streak、`last_quiz_at`，並 save 回 `UserVocab`。
- `check_mc_answer()` 已開始處理 correct / incorrect count、streak、`last_quiz_at`，並 save 回 `UserVocab`。
- `check_kana_answer()` / `check_mc_answer()` 已保存 `last_answer`，方便 result partial 顯示 user 上一次提交嘅答案。
- 已決定 tips button 只要被按下就應增加 `tips_count`，即使 user 原本已經輸入完整正確答案，因為「需要確認」本身代表掌握度未夠穩。
- `skip_question_punish()` 已建立，skip 時會檢查 `UserVocab` 是否屬於目前 user，再更新 weight、streak 同 `last_quiz_at`。
- `check_kana_answer()` 已將 submitted `tips_count` 納入 weight calculation。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 決定 kana answer 同 multiple choice answer 是否抽共用 helper。
- Multiple choice answer flow 要回傳答題結果，方便 view/template 顯示答啱或答錯。
- 如之後 stats update 牽涉多個 model / history record，再考慮用 transaction 包住整個更新流程。


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Quiz session summary tracking**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- `quiz_session` 已開始保存整局 quiz 嘅統計資料，包括 `aims_quiz_num`、`quizzed_count`、`correct_count`、`wrong_count`、`skipped_count`、`total_tips_count`。
- Answer submit 後已會更新 correct / wrong count、tips total，並將 nested session dict 寫返入 `request.session["quiz_session"]`。
- Skip 後已會更新 skipped count，並將 nested session dict 寫返入 `request.session["quiz_session"]`。
- Next / skip 抽到新題時已會更新 `question_user_vocab_id`、`fallback_used` 同 `quizzed_count`。
- Skip 抽下一題時已不增加 `quizzed_count`，所以 skipped question 不計入已答題數。
- `QuizSummaryForm` / `QuizSummaryView` / `quiz_summary_partial.html` 已有初稿。
- Summary partial 已可顯示本局答題數、目標題數、正確數、錯誤數、skip 數同 tips 使用量。
- Summary response render 完後已用 `session.pop("quiz_session", None)` 清走 quiz session，避免完成後再入 setting 被誤判成 unfinished quiz。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 決定一局 quiz 點樣完結：固定題數、手動 finish button，定係兩者都支援。
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


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- 之後可考慮 database import history model。
- User message / admin inbox 如觸發 CSV import，可以用 import report 回寫處理結果。

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


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **改善 G：Whitespace cleanup**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 清理 `git diff --check` 報告嘅 trailing whitespace。


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


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **改善 L：Quiz question pool query performance review**


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- Review `QuizService.create_question_pool()` 入面 `qs.count()` + `pick_random_vocab()` 入面 `list(queryset)` 造成兩次 SQL 嘅 trade-off。
- 目前寫法清楚易明，暫時可接受；之後如 quiz pool 變大，再評估是否需要改成更適合大量資料嘅抽題策略。

## UI / UX


> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **50 音假名 keyboard**


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


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 完成 multiple choice panel 嘅實際選項產生、answer submit 同 backend checking。


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

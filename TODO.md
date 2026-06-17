# Project TODO

呢份 TODO 主要記低之後要補嘅位，同埋已經處理咗嘅 decision。  
寫法會盡量用廣東話 + English technical terms，方便自己返嚟睇嗰陣快啲入腦。

## VocabRequest / Admin Review Flow

- [ ] **第 1 點：真正實作 approve / reject request 嘅處理 flow。**
  - 目前狀態：刻意留返未完成。
  - 要等 approve / reject 真係成功處理完，先可以 show success message。

- [x] **第 2 點：Admin 入面嘅 approve / reject action 由 GET link 改做 POST。**
  - 避免誤 click、refresh page 時重複執行，或者連續 click 造成重複處理。
  - 當 request 已經唔係 `PENDING` 狀態，就唔可以再處理多次。

- [ ] **第 3 點：幫 admin custom approve / reject view 加 permission check。**
  - 等學清楚 Django admin permission flow 之後再補。
  - 要 check reviewer 係咪有 permission 去 change `VocabRequest`。

- [x] **第 4 點：將 `VocabUpdateRequestForm` 入面嘅 `vocab_type` set 做 readonly。**
  - 避免 user 喺 update vocab request 期間改咗 vocab type，令 detail model 關係變亂。

- [x] **第 9 點：Admin 入面由 workflow 控制嘅 fields 要 set 做 readonly。**
  - 例如：`status`、`request_type`、`reviewed_by`，同埋適合 readonly 嘅 proposed data。
  - 狀態變更應該經 approve / reject service 處理，唔應該喺 admin form 直接亂改。

- [x] **第 5A 點：建立 `VocabRequest` 嘅操作要有 transaction atomic。**
  - 避免 create request 中途 exception、server stop，或者其中一部分 save 咗但另一部分冇 save。
  - 目前 create / update / restore / delete request creation 已經用咗 `transaction.atomic()`。

- [ ] **第 5B 點：approve / reject review flow 都要有 transaction atomic。**
  - 之後做第 1 點 approve / reject workflow 嗰陣一齊處理。
  - 如果 review 時要同時 update `VocabRequest`、`Vocab`、`VocabDetail`、`KatakanaDetail` 等資料，應該包喺同一個 transaction 入面。

- [x] **第 7 點：防止同時建立多筆 duplicate pending request。**
  - 目前方向：喺 `Vocab` 加 field，當有 pending request 時 mark / lock 住嗰個 vocab。
  - 亦要考慮 database constraint 或 row lock，因為淨係 check Boolean field，遇到 concurrent request 時仍然可能有 race condition。

- [ ] **第 11 點：決定唔同 vocab type 專屬 fields 嘅 validation rule。**
  - 例如：Katakana type 係咪一定要填 `native_japanese`。

## Vocab

- [x] **第 8 點：公開 vocab list 只 show active vocab。**
  - 喺適合位置加 `is_active=True` filter。

- [x] **第 4 點補充：決定改 vocab type 時，validation 同 related detail 要點處理。**
  - 目前決定：喺 `VocabUpdateRequestForm` 將 vocab type set 做 readonly。

- [x] **第 10 點：保留 `VocabRequest.original_vocab` 目前嘅 `CASCADE` 行為。**
  - 正常 delete vocab 嘅方式係 soft delete / disable，而唔係 database 入面永久 delete。
  - 如果 vocab 真係被永久 delete，目前接受相關 review record 一齊消失。

## Account Admin

- [ ] **第 6 點：檢查 custom User Admin 寫法。**
  - `CustomizedUserAdmin` 目前繼承 `admin.ModelAdmin`，唔係 Django standard `UserAdmin`。
  - 普通 admin form 可能會直接 save password field，冇 call `set_password()`，咁 password hash 會出事。
  - 用返 `UserAdmin` 可以攞到 standard password hash form、password change flow、groups、permissions、staff fields 等功能。

## General Improvements

- [ ] **改善 A：** 幫 `Vocab`、`VocabRequest` 等 model 加 `__str__()`，admin 同 debug 時會易睇好多。
- [ ] **改善 B：** 考慮將 `vocabRequestService` rename 做 `VocabRequestService`，跟返 class naming style。
- [ ] **改善 C：** 清走未用嘅 import 同舊嘅 commented query code。
- [ ] **改善 D：** 幫 duplicate request、create / update / delete flow、approve / reject flow 加 tests。
- [ ] **改善 E：** 加 `requirements.txt` 或 `pyproject.toml`，正式記低 project dependencies。
- [ ] **改善 F：** 正式 deploy 前，將 `SECRET_KEY`、`DEBUG` 等 settings 搬去 environment variables。
- [ ] **改善 G：** 清理 `git diff --check` 報告嘅 trailing whitespace。

## Later Features

- [ ] 實作 vocab request approve / reject email notification。
- [ ] 實作 account email activation。

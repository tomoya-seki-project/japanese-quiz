# 專案待辦事項

## 詞彙申請／後台管理

- [ ] **第 1 點：實作核准及拒絕申請的實際處理流程。**
  - 目前狀態：刻意保留為未完成。
  - 只有操作真正完成後，才顯示成功訊息。

- [x] **第 2 點：將後台的核准／拒絕操作由 GET 連結改為 POST。**
  - 避免誤觸、重新整理時重複執行，以及連續點擊。
  - 當申請不再是 `PENDING` 狀態後，禁止再次處理。

- [ ] **第 3 點：為後台自訂的核准／拒絕 View 加入權限檢查。**
  - 學習 Django 後台權限處理後再實作。
  - 檢查審核者是否擁有修改 `VocabRequest` 的權限。

- [x] **第 4 點：將 `VocabUpdateRequestForm` 的 `vocab_type` 設為唯讀。**
  - 避免使用者在更新詞彙申請期間改變詞彙類型。

- [x] **第 9 點：將由工作流程控制的後台欄位設為唯讀。**
  - 例如：`status`、`request_type`、`reviewed_by`，以及適當的 proposed data。
  - 狀態變更應經由核准／拒絕 service 處理。

- [x] **第 5A 點：確保建立 `VocabRequest` 的操作具備交易原子性。**
  - 避免建立 request 時發生例外、程序中斷或伺服器故障，留下只儲存了一部分的資料。
  - 目前 create/update/restore/delete request creation 已使用 `transaction.atomic()`。

- [ ] **第 5B 點：確保審核 approve/reject 的操作具備交易原子性。**
  - 之後實作第 1 點 approve/reject workflow 時處理。
  - 若審核時需要同時更新 `VocabRequest`、`Vocab`、`VocabDetail`、`KatakanaDetail` 等資料，應包在同一個 transaction 內。

- [x] **第 7 點：防止同時建立多筆重複的 pending 申請。**
  - 目前構想：在 `Vocab` 加入欄位，當有 pending 申請時將該詞彙標記／鎖定。
  - 同時考慮資料庫約束或資料列鎖定，因為單純檢查 Boolean 欄位，在並行請求下仍可能發生競爭狀況。

- [ ] **第 11 點：決定不同詞彙類型專屬欄位的驗證規則。**
  - 例如：Katakana 類型是否必須填寫 `native_japanese`。

## 詞彙

- [x] **第 8 點：公開詞彙列表只顯示已啟用的詞彙。**
  - 在適當位置加入 `is_active=True` 篩選。

- [x] **第 4 點補充：決定變更詞彙類型時的驗證及關聯 detail 處理方式。**
  - 目前決定：在 `VocabUpdateRequestForm` 將詞彙類型設為唯讀。

- [x] **第 10 點：保留 `VocabRequest.original_vocab` 目前的 `CASCADE` 行為。**
  - 正常刪除方式是停用，而不是從資料庫永久刪除。
  - 如果詞彙被永久刪除，目前可以接受其審核紀錄一併消失。

## 帳戶後台

- [ ] **第 6 點：檢視自訂 User Admin 的實作。**
  - `CustomizedUserAdmin` 目前繼承 `admin.ModelAdmin`，而不是 Django 的 `UserAdmin`。
  - 一般後台表單可能直接儲存密碼欄位內容，而沒有呼叫 `set_password()`。
  - 使用及設定 `UserAdmin` 可以取得標準的密碼雜湊表單、密碼修改流程、群組、權限及 staff 欄位。

## 一般改善

- [ ] **改善 A：**為 `Vocab`、`VocabRequest` 等 model 加入 `__str__()`。
- [ ] **改善 B：**考慮將 `vocabRequestService` 重新命名為 `VocabRequestService`。
- [ ] **改善 C：**移除未使用的 import 及舊有的註解查詢程式碼。
- [ ] **改善 D：**為重複申請、建立／更新／刪除流程，以及核准／拒絕流程加入測試。
- [ ] **改善 E：**加入 `requirements.txt` 或 `pyproject.toml` 等依賴套件設定。
- [ ] **改善 F：**正式部署前，將 `SECRET_KEY`、`DEBUG` 等設定移至環境變數。
- [ ] **改善 G：**清理 `git diff --check` 報告的行尾空白。

## 之後要做的功能

- [ ] 實作 vocab request approve / reject email notification。
- [ ] 實作 account email activation。

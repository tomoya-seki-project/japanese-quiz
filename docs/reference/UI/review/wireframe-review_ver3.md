# Wireframe Review — Version 3

## Status tags

- <span style="color: #16803c; font-weight: 700;">[OK]</span>：本輪確認可接受
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span>：已確認需要修改
- <span style="color: #b26a00; font-weight: 700;">[PENDING]</span>：需要再決定規格
- <span style="color: #1565c0; font-weight: 700;">[TO-CHECK]</span>：本輪未有明確確認結果

## 本輪原則

- 本文件記錄第三輪 wireframe review。
- Review 記錄階段只記錄問題；使用者其後已授權同步 design docs 並實作本輪修正。
- 本輪 TO-FIX 已完成實作並通過使用者視覺確認；原始問題描述保留作設計決策記錄。
- <span style="color: #16803c; font-weight: 700;">[FINAL UI ACCEPTANCE]</span> 使用者已完成第三輪檢查，確認本輪全部修正的視覺效果均可接受。
- 本版 UI 已由 wireframe 驗證階段進入 release candidate 狀態；後續如沒有新需求，不再以 wireframe 名義反覆調整已確認項目。
- 驗證：Tailwind build、Django system check、git diff --check 通過；14 項 Playwright 測試通過，包含 ver3 各項尺寸與排列的實測。
- Word／kana input 以原兩欄 input 寬度 × 125% 計算，兩者等寬；label 與增闊 input 同行放不下時換成上下排列。
- Feedback dropdown 目標 15em（原 10em × 150%），窄屏按 label 外的剩餘寬度限制，保持同行。

## Buttons

- <span style="color: #16803c; font-weight: 700;">[OK]</span> 除本文件已指出的 Tips／Skip 顏色及 selection group 排列外，其餘本輪修改的 buttons 已確認可接受。

## User Vocab Detail

- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 以下 data rows 與上下虛線的距離不一致：
    - Correct count
    - Wrong count
    - Streak
    - Last quiz time
    - Last answer
- `Last quiz time` row 的垂直空間明顯較闊。
- 上述同類 data rows 應使用一致的上下距離。

## Quiz

- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Question state 的 Tips／Skip button 仍未改成已確認的顏色；目前顏色仍不正確。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Result state 的 word 與 kana 距離可以再縮短。

## Homepage

- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Logo 與 username／Guest frame 可以再拉近。

## Selection buttons

- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 上一輪將所有 selection group 統一成每行最多三粒的規則不正確，需要改回按每個 field 自己的選項數目排版。
- Categories：只有 category selection buttons 保持每行最多三粒。
- Level：六粒 level buttons 必須同一行顯示。
- Type 與 `in_use`：各自按本身的選項數目排成一行，不受下方 Categories 每行三粒的規則影響。
- 此修正適用於 User Vocab List Filter、Quiz Setting，以及其他使用相同 selection component 的頁面。

## Selection field frame padding

- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Quiz Setting、User Vocab List Filter、Vocab List Filter、Create Request 與 Update Request 的 selection field 大 frame，上下 padding 不一致。
- 受影響 fields：
    - 問題數
    - Type
    - Level
    - Categories
- 目前上方 padding 過大；修正時以現有下方 padding 為準，將上方 padding 調成相同數值。

## Create／Update Request

- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Kana field name 在 Create Request 與 Update Request 都要保持單行顯示，不可分成兩行。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 兩頁的 Word 與 kana input box 仍未按之前確認的規格增闊。
- 兩個 input box 要保持等闊，並增加至原本實作闊度約 `125%`。

## 本輪補充確認

### Account／Request

- <span style="color: #16803c; font-weight: 700;">[OK]</span> User Profile 的 username、email、last login 單行 frame 高度已足夠降低。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Create／Update Request 的「意味」及「理由」已使用 field name 在上、textarea 在下的排列。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> User Vocab Filter 已使用 `出題してる／出題してない` 文案。

### User Vocab／Event List

- <span style="color: #16803c; font-weight: 700;">[OK]</span> User Vocab List header checkbox 下方的「すべて」已刪除。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> User Vocab List 的 checkbox 與 word 之間已有垂直線，header 與各 row checkbox 亦已對位。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Event List header checkbox 下方的「選択」已刪除。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Event List 的 checkbox 與內容之間已有垂直線，header 與各 row checkbox 亦已對位。

### Tag／Feedback

- <span style="color: #16803c; font-weight: 700;">[OK]</span> Category tags 的新背景色 `#D2E5ED` 可接受。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Feedback List 的 user／type frame 新背景色可接受。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Feedback List 的「状態」與 dropdown 已正確放在同一行。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Feedback List dropdown 收得太窄；以目前實際闊度為基準，增闊至目前的 `150%`。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Feedback item 上下兩行之間的虛線可接受。

### Event Detail／Quiz／Global

- <span style="color: #16803c; font-weight: 700;">[OK]</span> Event Detail 已加回「内容」field name，內容亦由下一行開始。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Quiz Question／Result 的 word 字級按字數由 `76px` 降至 `42px` 的效果可接受。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 其他尚未另行指出的非 button element，包括 modal、list row、tag 等，上下 padding 暫時可接受。

## 已確認的實作值

- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 按 `quiz-question-state.png`，Tips／Skip 兩粒 button 統一使用 Primary `#8BC9E6` 背景及 Ink `#26343D` 文字。現有設計文件所寫的 `#EAF2F6` 需要同步更正。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Quiz Result 的 word 與 kana 距離先改為 `6px`。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Homepage logo 與 username／Guest frame 的目標視覺距離先改為 `16px`。

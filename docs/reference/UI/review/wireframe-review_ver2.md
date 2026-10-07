# Wireframe Review — Version 2

## Status tags

- <span style="color: #16803c; font-weight: 700;">[OK]</span>：本輪確認可接受
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span>：已確認需要修改
- <span style="color: #b26a00; font-weight: 700;">[PENDING]</span>：需要再決定規格
- <span style="color: #1565c0; font-weight: 700;">[TO-CHECK]</span>：本輪未有明確確認結果

## 本輪結論

- `ui-confirm` 內可檢查的頁面全部確認為 <span style="color: #16803c; font-weight: 700;">[OK]</span>。
- 本文件只記錄第二輪 review 結果；未定案項目不會當成正式 UI 規格。
- 已按使用者授權實作下列修正；本文件的 TO-FIX 保留為第二輪 review 原始記錄，實際視覺效果待下一輪使用者確認。
- 本次驗證：Tailwind build、Django system check、JavaScript 語法檢查通過；12 項既有 UI 測試及新增尺寸測試通過。
- Pagination 在空間不足時減少可見頁碼，保留 44px 按鈕，避免 360px 畫面內部溢出。

## 全站共用

- <span style="color: #16803c; font-weight: 700;">[OK]</span> 大量壓成一行的 HTML／Django template markup 已拆行，並改回 4 spaces 縮排。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Page header 已改成有左右留白、圓角及陰影的 frame。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 全站非 button element 的 vertical padding 需要統一：
    - 每個 element 自身的 top／bottom padding 必須相等。
    - 同一 component type 在不同頁面必須使用相同 vertical padding。
    - 不同 component type 可以使用不同數值；至少分開 page header、field／card、單行 data row、list header／toolbar、list row、badge／tag、modal section、footer。
    - Mobile safe area 額外加在 footer bottom，不計入視覺 top／bottom padding。
    - Button padding 已另行記錄於 `button-design.md`，不在這條規則重複定義。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> List header／filter toolbar 已改成有左右留白的圓角 frame。
    - <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 刪除 User vocab list 全選 checkbox 下方可見文字「すべて」。
    - <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 刪除 Event list 全選 checkbox 下方可見文字「選択」。
    - 保留兩個 checkbox 的 accessible `aria-label`；Event filter 的 `すべて／未読／既読` 不屬於今次刪除範圍。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 虛線已改成較接近 preview 的長線段效果。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Pagination 目前為 36px；新確認規格為 `44 × 44px`，需要修改。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 一般主要 button 文字確認為 18px Bold。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Footer／page shell 的水平 overflow 已修正。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Zen Maru Gothic、Hachi Maru Pop 已改成本地載入，不再依賴 Google Fonts。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 已加入本地字體檔及 OFL license。

## Homepage

- <span style="color: #16803c; font-weight: 700;">[OK]</span> 已登入狀態的「単語帳」已改為連往 User vocab filter。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Guest／username frame 已收窄。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 未登入 Guest frame 及已登入 username frame 都要再拉近上方 logo，減少兩者之間的垂直距離。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Homepage 主要 buttons 的 padding 確認保留現狀：上下 `.7em`、左右 `2em`。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 「学習データ」標題已置中。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Logout／Event buttons 已限制在現有 540px app shell 範圍內，不再無限跟隨 viewport 向兩邊移動。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Footer buttons 上下 padding 的目前觀感已確認。
    - <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 按新規格統一闊度：單粒為 active area 50% 並置中；多粒扣除 gap 後平均分配整行。

## Forms／Account

- <span style="color: #16803c; font-weight: 700;">[OK]</span> Login 未 activation 提示已正確置中。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 破棄確認 modal 句子已置中。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Username、email、last login 類型的單行資料 frame 高度已有改善，但仍需再降低／調整。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 一般主要 buttons 改用新確認規格：基本為 active area 50%，左右每邊最少 2em；單行所需寬度超過 app shell 80% 時分兩行，再按較長一行計算寬度。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Word／kana input box 已等寬，但希望兩者闊度增加至目前約 125%。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 「意味」／「理由」textarea 的 field name 在上方靠左、textbox 在下一行的排版沒有可見改變。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Update request 的固定種類已改成 field name 在左、data 在右。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> `出題対象` 顯示文字：
    - User vocab detail：`出題する／出題しない`，已確認 <span style="color: #16803c; font-weight: 700;">[OK]</span>。
    - User vocab filter：改成 `出題してる／出題してない`。

## Selection buttons

- <span style="color: #16803c; font-weight: 700;">[OK]</span> 未選狀態已由 disabled 灰改成 preview 使用的 `#91AAB7`。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Level buttons 維持正常 viewport 同一行及相同尺寸，並保留目前 compact padding。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Category／一般 selection buttons 的目前上下 padding 已確認保留。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 所有 selection group 統一排列：同 group 同尺寸、每行最多三粒；最後一行一粒置中、兩粒靠左，均不拉闊。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Event 狀態 `すべて／未読／既読` 納入 selection button 規格。

## Vocab／Event lists

- <span style="color: #16803c; font-weight: 700;">[OK]</span> 已確認自訂 `list-item` 與 Tailwind 內置 class 撞名。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 自訂 class 已改名為 `ui-list-item`。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> User vocab 與 Event list 的 checkbox／「V」位置：
    - 每行最左側的排列位置已確認 <span style="color: #16803c; font-weight: 700;">[OK]</span>。
    - Checkbox 與 word 之間加入垂直分隔線，視覺效果跟 word 與 kana 之間的分隔線一致。
    - List item checkbox／「V」與 header checkbox 的水平位置需要對齊。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Vocab list header 已改為圓角 frame，並保留左右空間。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Event filter container 已改成圓角 frame。
    - <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Event list item 的「V」與 header checkbox 仍未對位。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Event type badge 的圓角已加大。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Categories frame 底部多餘空位看來已收窄。
    - <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 每個 category frame 的背景色改為 Tag / Metadata BG `#D2E5ED`，文字使用 `#26343D`。

## Event detail

- <span style="color: #16803c; font-weight: 700;">[OK]</span> Page title／內容之間已恢復分隔效果。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 內容上下已加入虛線。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> 內容欄位排版：
    - 加回 field name「內容」，放在最高一行左側。
    - Data 由下一行開始顯示。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 日期已新增 `日時` field name。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 日期已使用 field name 在左、data 在右的排列。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 底部已讀／未讀 button 已收窄。

## Feedback

- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Feedback list 的「状態」控制：
    - 「状態」label 已恢復，這部分確認 <span style="color: #16803c; font-weight: 700;">[OK]</span>。
    - Label 與 dropdown 改為同一行。
    - Dropdown 闊度縮小。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Dropdown 文字已正確靠右。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Feedback item 的 user／type 小 frame 改為 Tag / Metadata BG `#D2E5ED`，文字使用 `#26343D`。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Feedback item 上下兩行中間加入虛線。

## Quiz

- <span style="color: #16803c; font-weight: 700;">[OK]</span> Question state 的 Tips／Skip button 現有尺寸及排列確認保留。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 無設定總題數時，結果頁「第幾問」frame 已按內容收窄。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 「第幾問」與正解／不正解 frame 暫時使用一致的 14px 圓角。
- <span style="color: #c62828; font-weight: 700;">[TO-FIX]</span> Quiz word 動態字級已確認為 1–2 字 76px，之後每增加一字減少 4px，10 字 44px，11 字或以上 42px；42px 仍放不下時才換行。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> 「次へ」與「結果へ」同時出現時已左右並排。
- <span style="color: #16803c; font-weight: 700;">[OK]</span> Judgement modal：
    - `正解　data`、`回答　data` 同行。
    - `種類　data`、`詳細種類　data` 同行。
    - MATCH／MISSING 等種類 data 已使用不同顏色。

## UI confirm

- <span style="color: #16803c; font-weight: 700;">[OK]</span> `ui-confirm` 內所有可檢查頁面均已確認。

## 下一輪已確認要處理

1. 再調低單行 account data frame 的高度。
2. Word／kana input box 闊度增加至目前約 125%。
3. 修正「意味」／「理由」textarea 的上下排版。
4. User vocab filter 的選項文字改成 `出題してる／出題してない`。
5. User vocab／Event list 加入 checkbox 後的垂直分隔線，並修正 header 對位。
6. Category 與 feedback 小 frame 改用 Tag / Metadata BG `#D2E5ED` 及 Ink `#26343D`。
7. Event detail 加回「內容」field name，data 由下一行開始。
8. Feedback 狀態 label 與 dropdown 同行，並縮小 dropdown。
9. Feedback item 上下行之間加入虛線。
10. Pagination 改為 `44 × 44px`。
11. 一般主要 button 套用 active area 50%、每邊最少 2em 及長文字換行規格。
12. Footer button 套用單粒 50% 置中、多粒平均分配整行的規格。
13. Selection group 套用每行最多三粒及最後一行固定單粒寬度的排列規格。
14. 刪除 User vocab list 全選 checkbox 下方「すべて」及 Event list 全選 checkbox 下方「選択」；保留 accessible labels。
15. Homepage 的 Guest／username frame 拉近 logo。
16. 盤點非 button element 並按 component type 統一 vertical padding；每個 element 的 top／bottom padding 相等。
17. Quiz Question／Answer Result word 套用 76px 至 42px 的字數分級，42px 放不下時才換行。

## 尚待決定／確認

目前沒有未定的本輪 wireframe 規格。


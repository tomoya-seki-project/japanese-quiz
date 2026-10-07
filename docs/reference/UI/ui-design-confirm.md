# Japanese Quiz UI — Confirmed Design Specification

## 1. 文件定位

本文件是目前 UI 的主要實作規格，內容由以下資料整合而成：

- UI-design.md 的完整頁面及互動要求
- button-design.md 已確認的按鈕尺寸規則
- wireframe-review.md 與 wireframe-review_ver2.md 的實作檢查結果

原 UI-design.md 保留設計過程、候選方案及 preview 歷史；本文件只保留目前有效的要求、已確認規格、版本範圍及仍待定項目。

### 1.1 規格優先次序

1. 本文件的已確認規格
2. 各頁面的明確例外
3. 現有 preview，只作視覺參考
4. 舊 review 與原 UI-design.md，只作歷史追溯

如 preview 與本文件衝突，以本文件為準。

### 1.2 版本範圍

v1.0.0 包括：

- Account、Vocab、User Vocab、Event、Feedback
- 非 Multiple Choice Quiz
- Quiz Summary、No-question、No-pool
- 400、403、404、500
- 開發環境 UI confirm page

v1.0.0 後處理：

- Multiple Choice Quiz
- Admin Event Create
- 只影響當前頁、可回復為未讀的 event reading 行為
- 未有 backend／model 支援的額外功能

---

## 2. 語言與文案

- Django /admin/ 以外的所有網站頁面使用日文 UI。
- Admin-only custom site pages 仍使用日文。
- Django /admin/ 維持現有語言，不加入額外轉換。
- 開發或診斷 UI 如「判定詳細」亦使用日文欄名。
- UI 文案必須以本文件指定文字為準；不得因 template 舊值而回復舊文案。

---

## 3. 全站版面系統

### 3.1 App shell 與 active area

- 所有主要 UI 集中在 viewport 中央。
- 中央範圍稱為 app shell。
- App shell 寬度為 100%，最大寬度 540px，並水平置中。
- Viewport 大於 app shell 時，外圍只顯示背景。
- App shell 不是可見大框；頁面不得用一張大 card 包住全部內容。
- App shell 扣除頁面左右留白後的可用範圍稱為 active area。
- 所有百分比 element 寬度以 active area 計算，不以整個 browser viewport 計算。
- 最低正式支援寬度為 320 CSS px。
- 320px 或以上不得產生頁面級水平捲動。

### 3.2 固定區與捲動區

一般頁面採用：

1. 固定 header
2. 獨立可捲動 content area
3. 如有操作，使用固定 footer action bar

List page 只讓正式 list area 捲動；header、filter／table header、footer action 與 pagination 保持固定。

手機 browser 地址列展開或收起時，版面以動態 viewport height 重算，固定區不可漂移或重疊。

### 3.3 Header

- Header 置於 app shell 內，保留左右空間。
- 使用近白實色背景、圓角及柔和陰影。
- 一般高度 72px；compact mode 為 60px。
- 中間 page title 使用 28px Zen Maru Gothic Bold。
- 左右各保留 icon control 區；沒有 control 時仍保留版面空位，確保標題真正置中。
- Header icon button 為 48 × 48px，icon 為 28 × 28px。

### 3.4 Footer action bar

- Footer 使用完整近白實色底欄，不讓 button 或 pagination 直接浮在 kana 背景上。
- 視覺 top／bottom padding 相等。
- Mobile safe area 只額外加在 bottom，不計入視覺 padding。
- 同時有 action 與 pagination 時，以兩行共用同一個 footer，兩行之間保留一組 14px gap，不重複累加內距。
- Footer 必須留在 app shell 範圍，不可跟 browser viewport 無限向外擴張。

### 3.5 Compact mode

Viewport height 低於 700px 時：

- Header 高度由 72px 改為 60px。
- 一般 button 高度可由 58px縮至 50px；不得低於 44px touch target。
- Footer 視覺上下 padding 由 14px 改為 10px。
- Section 垂直距離約縮短 20%。
- 字體大小、input 高度及可點擊寬度不縮小。

### 3.6 虛擬 keyboard 輸入模式

文字 input／textarea focus 且手機虛擬 keyboard 實際開啟時：

- 暫時收起 header 與固定 footer。
- 自動捲動，確保 focused field 完整位於 keyboard 上方。
- Keyboard 關閉後恢復原版面與原捲動位置。
- Select、switch、selection button 不觸發此模式。
- 此規則優先於 compact mode。

---

## 4. Spacing 與密度

### 4.1 Vertical padding

- 每個非 button element 自身的 top／bottom padding必須相等。
- 同一 component type 在不同頁面必須使用相同 vertical padding。
- 不同 component type 可使用不同數值。
- 必須至少分開以下類型：
  - Page header
  - Field／card
  - 單行 data row
  - List header／toolbar
  - List row
  - Badge／tag
  - Modal title／body／actions
  - Footer
- 不得以固定高度製造無用途的底部空白。
- 內容換行時才按內容增加高度。

### 4.2 Component gap

- 同級 card 之間使用一致 gap。
- 同一 card 內 field row 以分隔線與一致 padding 區分。
- Section 之間使用較明顯的實線與較大間距。
- 不以逐頁 margin override 修正視覺位置。

---

## 5. Typography

### 5.1 Fonts

- 一般正文、form、table、data：Zen Maru Gothic。
- Page title、modal title、狀態主標題、主要 button：Zen Maru Gothic Bold。
- Hachi Maru Pop 只用於短裝飾文字；Homepage 已改用 logo image，不再用文字 wordmark。
- Quiz kana keyboard、輸入答案及答案比較可使用現有 HGS 創英角ポップ体風格 PNG。
- 字體由本地 static assets 載入，不依賴 Google Fonts。
- OFL license 必須與字體檔一同保留。

### 5.2 字級

- Page title：28px Bold。
- Field name：20px Bold。
- Data、input、正文：16px。
- 輔助文字／任意標記：13px。
- 一般主要 button：18px Bold。
- Homepage hero button：28px Bold。

過長 title 先換行，再逐級縮小；不得直接裁切。

---

## 6. Color system

| Token | 色值 | 用途 |
|---|---|---|
| Ink | #26343D | 正文、淺色 button 文字 |
| Muted | #607783 | 日期、說明、placeholder |
| Paper | #F8FCFF | Card、header、footer |
| Primary | #8BC9E6 | 主要操作 |
| Selected | #BFE8F7 | Selection active、keyboard panel |
| Control | #EAF2F6 | Input、次要操作 |
| Tag / Metadata BG | #D2E5ED | Category tag、Feedback item 的 user／type 小 frame |
| Line | #91ADBC | 虛線、柔和分隔 |
| Icon | #477A99 | Icon、較深線條 |
| Success | #39765B | 正解、成功、replied |
| Danger | #AD4B55 | 錯誤、不正解、危險操作 |
| Disabled BG | #D5DFE4 | Disabled control |
| Disabled text | #687B85 | Disabled 文字 |

- Card 使用 Paper 90% opacity。
- Header、footer、modal、toast 使用不透明背景。
- 一般 control 不使用 visible border。
- Focus-visible 使用 Icon 色 outline 與 Selected 色外圈。
- 狀態不得只依靠顏色；同時使用文字或 icon。
- Category tag 與 Feedback item 的 user／type 小 frame 統一使用 Tag / Metadata BG，不使用 Control 或 Selected 色。

---

## 7. Background 與 card

### 7.1 Background

- 一般頁面使用 mixed kana tile。
- 一般 vocab Quiz 使用 hiragana tile。
- Katakana Quiz 使用 katakana tile。
- 無 current question type 的 Quiz state 使用 mixed tile。
- Background 固定在 viewport，seamless repeat，不使用 cover 拉伸。
- 優先載入 1600 × 1200 asset，以 800 × 600 CSS size 顯示。
- 如個別 mobile browser fixed background 效能不佳，可降級成隨頁面捲動。

### 7.2 Card

- Paper 90% opacity、無 visible border。
- 圓角 card，陰影為 0 4px 12px、#26343D 16%。
- Card 間必須顯示背景。
- Field／data card 寬度一致並使用 active area。
- Card 高度由內容加標準 padding 決定。

### 7.3 分隔線

- 同一 table／field group：#91ADBC 單虛線。
- 虛線使用較長線段，不使用細密點狀效果。
- 不同 section／table：#477A99 較粗實線及較大上下間距。
- 分隔線只畫在內容 frame 內。

---

## 8. Button system

### 8.1 尺寸與顏色分離

Button 必須分別指定：

- 尺寸 type
- 語意 color variant

Color variant 包括 Primary、Secondary、Danger、Selected、Disabled；不得為 Danger 等顏色另建 page-specific padding。

### 8.2 Homepage hero button

- 28px Bold。
- Padding：上下 .7em、左右 2em。
- 寬度按內容。
- 全站最高視覺層級。

### 8.3 一般主要 button

- 18px Bold。
- 基本寬度：active area 50%。
- 左右每邊最少 2em。
- 短文案維持 50%。
- 較長文案可增加寬度。
- 單行所需寬度超過 app shell 80% 時，文字改為兩行。
- 換行後按較長一行的文字寬度加左右各 2em 重算。
- 最終寬度仍不得小於 active area 50%。
- 超過兩行的極端情況留待有真實文案時另定。

### 8.4 Footer button

- 上下 padding 保留 8px。
- 同行一粒：active area 50%，水平置中。
- 同行多粒：扣除 gap 後平均分配整行。
- 同行 button 等寬。
- 尺寸不得由 DOM nesting 決定。

### 8.5 Selection button

- 一般字級 16px Bold，最小高度 44px。
- 一般 padding 為四邊 8px。
- Level compact padding 為上下 6px、左右 2px。
- 同一 selection group 全部 button 相同尺寸。
- 各 field 獨立決定欄數；只有 Categories 每行最多三粒。
- Categories 完整行三粒排滿；尾行一粒置中、兩粒靠左，保持同組單粒尺寸，不拉闊。
- Level 六粒同一行；Type、in_use、問題數各按實際選項數量平均分配一行。
- Selection field 外框上下 padding 以現有下方 16px 為準；標題頂部不得再疊加 12px padding。
- Event 狀態「すべて／未読／既読」使用 selection 系列，不使用主要 action 尺寸。
- 未選狀態為 #91AAB7；已選狀態為 #BFE8F7。
- Disabled 與 unselected 必須保持不同語意。

### 8.6 Pagination

- 每粒固定 44 × 44px。
- 目前頁使用 Primary；不可用方向使用 Disabled。
- 同組 gap 為 6px。
- 左組：First、Previous。
- 中組：Page numbers，整組以 active area 真正中心置中。
- 右組：Next、Last。
- 方向 button disabled 時保留位置。
- 只有一頁時只顯示 page number 1。
- 顯示頁碼數上限如下；如 active area 放不下方向鍵、頁碼及 gap，減少可見頁碼數，優先維持 44 × 44px 及置中：
  - 480px 或以上：最多 5 個
  - 360–479px：最多 3 個
  - 320–359px：只顯示目前頁

### 8.7 Icon button

- Header icon：48 × 48px。
- Icon：28 × 28px。
- Password visibility：44 × 44px。
- Icon-only control 必須有 accessible label。

### 8.8 Quiz 特殊 button

- Tips／Skip：保留目前 18px、上下 8px、左右 16px、最小高度 58px，兩者等寬。
- 判定：保留 18px、上下 8px、左右 16px、最小高度 44px。
- Kana key：22px Bold；key 尺寸 44–62px responsive。
- Answer input surface 為 full-width interactive card，不套用一般 action button width。

---

## 9. Forms 與資料顯示

### 9.1 Field card

- Field name 與 control 放在同一張 card。
- 單行 field 一般使用 label 左、control 右。
- 空間不足時改為 label 上、control 下。
- Login／Registration 固定使用上下排列。
- Textarea field 固定使用 label 上方靠左、textarea 下一行。
- Optional field 在 label 旁顯示「任意」。
- 必填 field 不顯示「必須」。

### 9.2 Controls

- 單行 input、select 最少 44px 高。
- Input 文字靠右。
- Dropdown 文字靠右，右側保留獨立 vector arrow。
- Textarea 文字靠左。
- Create／Update Request 的 word／kana input 等寬，目標為增闊要求提出前的寬度約 125%；不是每次 review 再乘 125%。
- Kana field name 保持單行。若 label 與增闊 input 無法同行放下，使用 label 上、input 下，保留 input 目標寬度並限制在 frame 內。
- 寬 viewport 時 input 靠右；窄 viewport 時使用 active area 全闊。
- Password 預設隱藏，右側提供 visibility icon。

### 9.3 Data rows

- 一般情況 label 左、data 右。
- Data 太長時改為 label 上方靠左、data 下一行靠右。
- 單行 username、email、last login 等 row 使用 compact height。
- 同一 table 內 row 以虛線分隔。
- User Vocab Detail 的正解数、不正解数、連続記録、最後出題時間、前回回答使用一致上下內距；時間切換的 touch target 不得額外撐高該 row。
- Read-only 同一 model、同一語意 group 可共用 table card。

### 9.4 Validation modal

- 所有錯誤一次顯示在置中 modal。
- Backdrop 阻止後方操作與捲動。
- Modal title 與 action 固定；中間錯誤內容超出 max-height 才捲動。
- 關閉後：
  - 錯誤 field 使用 Danger outline 與 label
  - 自動 focus 第一個錯誤 field
- 點擊 backdrop 或關閉 button 可關閉。

### 9.5 未保存資料

以下頁面在 header Back、Home 或指定內部導航離開時顯示確認 modal：

- User Vocab Detail
- Vocab Create／Update／Delete Request
- Feedback Create／Reply

文案及操作：

- 主要危險操作：破棄して移動
- 次要操作：キャンセル
- 提示句置中

重新整理、關閉 tab 或直接離站不使用 browser native warning。

---

## 10. Shared states

### 10.1 Toast

- 顯示在 viewport 頂部，不阻擋操作。
- 約 3 秒後自動消失。
- 用於 Login、保存、各 request、Feedback、Event read status 等成功操作。

### 10.2 純通知／狀態頁

- 使用一張置中狀態 card，包含 icon／插圖、標題、說明及操作。
- No-question 與 No-pool 的 action 放在固定 footer。
- 適用 Activation、Logout、Quiz empty states 與 Error pages。

### 10.3 Construction placeholder

- 未完成資料功能：使用高不透明近白遮罩及幼黃黑斜紋。
- 未完成插圖：只佔未來插圖位置，不遮住真實 control。
- 正式功能／asset 完成後直接移除 placeholder，不重做 layout。

---

## 11. Homepage

### 11.1 共通

- Background 使用 mixed tile。
- Logo 使用 static/rec/logo/wordloop_logo.png。
- Logo 寬度為 viewport 80%，並受 active area 上限限制；保持原比例。
- Logo 與 identity card 之間不得加入舊有額外 48px spacer。
- Logo 圖片元素與 Username／Guest card 的 layout 間距先試 16px；兩種登入狀態一致。圖片本身透明邊緣不當作 CSS padding。
- Logout 與 Event icon 限制在 app shell，不隨大型 viewport 無限外移。

### 11.2 已登入

- Identity card 顯示 username。
- 左上 Logout；右上 Event。
- Learning Data title 置中。
- Learning Data 保留三項位置並以 construction overlay 覆蓋未完成資料。
- 中央 hero buttons：クイズ、単語の追加。
- Footer navigation：プロフィール、単語帳、フィードバック。
- 「単語帳」連往 User vocab filter。
- Footer 三粒正常一行；空間不足時 2 + 1，最後一粒置中。

### 11.3 未登入

- Identity card 顯示 ゲスト。
- Hero buttons：登録、ログイン、単語帳。
- 「単語帳」連往一般 Vocab filter。

---

## 12. Vocab pages

### 12.1 Vocab／User Vocab Filter

- Header：Back、頁名、Home。
- Selection fields：種類、JLPT、カテゴリー。
- User Vocab Filter 另有出題対象：
  - 出題してる → in_use=True
  - 出題してない → in_use=False
  - 兩者都未選或都選 → 全部
- Category 每行最多三粒，按全站 selection 排列規則。
- Footer 固定顯示「検索」。

### 12.2 Vocab List

- Header、list header、pagination 固定；只有 list rows 捲動。
- Columns：単語、読み方。
- Word column 較窄、kana column 較闊。
- Header 與 row 使用相同 column 起點。
- Columns 之間使用垂直分隔線。
- Row 全行可點擊。
- 單行 row 使用 compact padding；文字換行時才增高。

### 12.3 User Vocab List

- 在 Vocab List 基礎上增加最左 checkbox column。
- Header 全選 checkbox 只作用於當前頁。
- Checkbox 下方不顯示「すべて」；保留 aria-label。
- Checkbox 與 word column 之間使用垂直分隔線。
- Header checkbox 與 row checkbox 必須水平對齊。
- Checkbox 不屬於 detail link 點擊區。
- 未保存勾選在轉頁時直接放棄。
- Footer：保存 action 加 pagination。

### 12.4 Vocab Detail

- Header：Back、単語の詳細、Home。
- 基本 table：単語、意味、読み方、JLPT、種類、カテゴリー。
- Category 位於 label 下方，以虛線分隔，tag 最多三個。
- 額外資料：
  - Katakana：対応する日本語表現
  - MCSense：按 sense_no 顯示意味與例文；不顯示 distractors
- MCSense 例文將底線換成基本形答案，保留活用提示。
- Guest 不顯示修改／刪除操作。
- 已登入 footer：変更申請、削除申請，兩者等寬。
- Delete 使用 Danger。

### 12.5 User Vocab Detail

- 上方 table：user-specific data；下方 table：基本 vocab data。
- 出題対象文案：出題する／出題しない，互斥選擇。
- Weight bar：
  - 1–49 #BFE8F7
  - 50–99 #8BC9E6
  - 100–149 #E6B85C
  - 150–199 #D9854B
  - 200–299 #AD4B55
  - 300–499 #73528D
  - 500+ #3F344A
- 顯示正解數、不正解數、連續紀錄、最後出題時間、前回回答。
- 最後出題時間可切換相對／實際時間。
- Footer：保存、単語の詳細。
- 未改動時保存 disabled；改動後 enabled；成功保存後回復 disabled。
- 未保存離開使用確認 modal。

### 12.6 Vocab Create Request

- Header：Back、単語の追加、Home。
- Fields：
  1. 種類
  2. 単語
  3. 読み方
  4. JLPT
  5. カテゴリー
  6. 意味
  7. 理由
  8. 対応する日本語表現（Katakana）
- Word／kana input 等寬並使用增闊後規格。
- 意味／理由：label 上、textarea 下；初始約三行。
- 種類與 JLPT 為單選 button；Category 最多選三個。
- Katakana field 按種類顯示，切換隱藏時保留未提交值。
- Footer 兩粒等寬：
  - 申請／ホームへ
  - 続けて／次の単語
- 第二行文字較細。
- 成功使用 toast；未保存離開使用 modal。

### 12.7 Vocab Update Request

- Header：Back、変更申請、Home。
- 預填現有資料。
- 種類不可修改，以 label 左、data 右顯示。
- Word／kana input 等寬並使用增闊後規格。
- 意味／理由固定使用 label 上、textarea 下。
- Footer 單一「変更申請」。
- 成功返回 Vocab Detail 並顯示 toast。

### 12.8 Vocab Delete Request

- 顯示基本資料及 optional 理由 textarea。
- Footer 單一 Danger「削除申請」。
- 提交前顯示確認 modal：「この単語の削除を申請しますか？」
- 成功返回 Vocab Detail 並顯示 toast。

---

## 13. Account pages

### 13.1 Login

- Header：ログイン、Home；左側留空。
- Form 與 resend area 同屬可捲動 content。
- Fields 固定 label 上、input 下。
- Login state 使用 switch。
- Login button 使用一般主要 button 規格。
- 未 activation 提示置中。
- Resend 說明與次要 button 放在獨立 card。
- Validation 使用共用 modal。

### 13.2 Registration

- 跟 Login form layout。
- Header：登録、Home。
- Password fields 提供 visibility icon。
- 登録 button 跟內容捲動。

### 13.3 Activation Email Sent

- 使用共用狀態 card。
- 顯示 email icon／未來 tent 插圖、標題、說明。
- Actions：ログイン画面に戻る、認証メールを再送する。

### 13.4 Account Activation

狀態：

- 等待：アカウントを有効にする
- 成功：ログイン
- 已認證：ログイン
- Link 無效／過期：認証メールを再送する

UI confirm preview 不得執行真實 activation。

### 13.5 Resend Activation

- 跟 Login form layout。
- 只顯示 email field。
- Action：認証メールを再送する。

### 13.6 Logout Result

- 使用共用狀態 card。
- 顯示「ログアウトしました。」
- Action：ログイン。

### 13.7 User Profile

- Compact rows：username、email、last login。
- Learning Data title 置中；未完成功能以 overlay 顯示。
- 顯示「マイ単語帳」button。
- Recent answers 使用預留 table layout及 overlay。

---

## 14. Event pages

### 14.1 Event List

- Header：お知らせ、Home；無 Back。
- Filter：すべて／未読／既読，使用 selection button 規格。
- Table header：全選 checkbox、項目。
- Checkbox 下方不顯示「選択」；保留 aria-label。
- Checkbox 與項目之間使用垂直分隔線。
- Header 與 row checkbox 必須對齊。
- 每頁五筆。
- Row：checkbox 左；type badge 與 title 右。
- Checkbox 跨兩行垂直置中。
- Type 與 title 之間使用虛線。
- 未讀只將 title 加粗。
- Title 最多兩行，超出使用 ellipsis。
- Footer：既読にする 加 pagination。
- 沒有資料時顯示 no-event state，不顯示 action。

Short type labels：

- 単語申請の審査結果 → 申請結果
- 単語 → 単語
- 出題優先度の自動更新 → 優先度更新
- フィードバックへの返信 → フィードバック返信
- New vocabulary request → 新規申請

### 14.2 Event Detail

- Header：Back、お知らせ、Home。
- 顯示完整 type badge、title、內容、日時。
- Title 與內容、內容與日期之間使用虛線。
- 「内容」label 位於內容區首行左側；message 由下一行開始。
- 「日時」label 左、data 右。
- 日期格式：YYYY年MM月DD日 HH:mm。
- 開頁不自動設已讀。
- Footer action：
  - 未讀 → 既読にする
  - 已讀 → 未読に戻す
- 以 POST、CSRF 及固定 action 值修改；成功 redirect 同頁並顯示 toast。

---

## 15. Feedback pages

### 15.1 Feedback Create

- Header：Back、フィードバック、Home。
- 種類使用 dropdown；文字靠右。
- 内容 textarea 初始約六行。
- Footer：送信。
- 成功返回 Homepage 並顯示 toast。
- 未保存離開使用 modal。

### 15.2 Feedback Admin List

- Header：フィードバック一覧、Home。
- Status filter：
  - 「状態」label 與 dropdown 同一行
  - Dropdown 由 ver3 review 時的 10em 增至 15em（150%）；窄屏以扣除 label 與 gap 後的剩餘寬度為上限，保持同行
  - 文字靠右
  - 選項：すべて、未対応、返信済み、終了
  - 預設未対応
- 每頁五筆。
- Item 上行：status icon、user frame、type frame。
- Item 下行：一行內容 preview。
- 上下行以虛線分隔。
- Item 全行可點擊。
- Status：
  - Pending：紅色、實心圓
  - Replied：綠色、剔號
  - Closed：一般深色、橫線
- Pagination 固定；沒有資料時隱藏 pagination。
- User／type 小 frame 使用 Tag / Metadata BG `#D2E5ED`，文字使用 Ink `#26343D`。

### 15.3 Feedback Admin Detail

- Header：Back、フィードバック詳細、Home。
- 基本 table：status、user、種類、送信日時。
- 「内容」獨立 section，label 在上方左側，data 下一行。
- 已回覆時顯示 reply admin 與 reply time。
- Table 內虛線；section 間實線。
- Footer：
  - 未対応／返信済み → 返信
  - 終了 → disabled 終了

### 15.4 Feedback Admin Reply

- Header：Back、フィードバックに返信、Home。
- 先顯示原 feedback，再顯示 reply textarea 與 switch。
- Switch label：返信後に終了；預設 off。
- Footer：返信。
- 成功返回 detail 並顯示 toast。
- 未保存離開使用 modal。

---

## 16. Quiz

### 16.1 Quiz Setting

- Header：Back、クイズ設定、Home。
- 前回の設定を読み込む：
  - 有資料時載入目前 form，不自動開始
  - 無資料時顯示 unavailable，點擊提示「前回のクイズ設定がありません」
- 問題数：10／20／30 單選；全未選代表無制限 -1；再次點擊已選項可取消。
- 種類、JLPT、Category 為 multi-select；全未選代表不限。
- Selection 各 field 獨立排版：Level 六粒同一行，Type、問題數按選項數排一行；只有 Categories 每行最多三粒。同 group 同尺寸。
- Footer：開始。
- 離開未開始設定不顯示未保存 modal。

### 16.2 Quiz 共通進度

- 已回答數 = 正解數 + 不正解數。
- Skip 不算已回答，不消耗固定題數，下一題沿用同一題號。
- Skip 次數獨立統計。
- 使用 Hint 後 Skip，Hint 仍計入 Summary。
- 無制限直至題庫耗盡或既有結束條件。
- Server endpoint 必須自行驗證進度，不能只信任前端狀態。

### 16.3 Question State

- Header title：クイズ。
- 題號 frame 靠左，按內容收窄。
- 題目 card：
  - Word 置中，預留最多兩行
  - Word 字級按字數固定分級；Question 與 Non-MC Answer Result 共用：
  
    | 字數 | Font size |
    |---:|---:|
    | 1–2 | 76px |
    | 3 | 72px |
    | 4 | 68px |
    | 5 | 64px |
    | 6 | 60px |
    | 7 | 56px |
    | 8 | 52px |
    | 9 | 48px |
    | 10 | 44px |
    | 11+ | 42px |
  
  - 42px 為最小值；到達最小值後仍放不下一行才換行
  - 長英文優先在 space 換行
  - Word 與 meaning 以虛線分隔
  - Meaning 置中，按內容收緊高度
- Answer input surface 全行可點擊。
- Empty hint：「ここを押して回答を入力」。
- Tips／Skip 左右等寬，按 quiz-question-state.png 使用 Primary #8BC9E6 背景及 Ink #26343D 文字；保留已確認尺寸。
- Skip 不顯示 Answer Result，直接下一題／Summary。
- Footer 回答：
  - 無答案時顯示 unavailable 但保留 click
  - 點擊提示「何も答えないと進めないよ」
  - 有答案時可提交

### 16.4 Kana Input Mode

- 白色半透明 backdrop 覆蓋原頁。
- 前景答案位於 keyboard panel 上方並置中。
- Bottom sheet 只承載 keyboard。
- 10 × 6 grid。
- 第六欄：濁點、半濁點、小書き、Backspace。
- 完了位於最底第 4–5 欄，只收起 keyboard，不提交。
- Panel：#BFE8F7。
- Kana key：#F8FCFF。
- Function key：#EAF2F6。
- 完了：#8BC9E6。
- Key responsive 44–62px。
- 320px 不得水平捲動。
- 矮 viewport 只捲動 keyboard 內容。
- 點擊 backdrop 或完了均保留答案並關閉輸入 mode。

### 16.5 Non-MC Answer Result

- 頂行三欄：
  - 左：第幾問，按內容收窄
  - 中：正解／不正解
  - 右：superuser 判定；一般 user 保留空位
- 三個 frame 圓角一致，使用 14px。
- Word card 顯示 word 與 (kana)；word 使用 Question State 相同的 76px 至 42px 字數分級。
- Word 與 kana 的 layout 間距先試 6px；card 外圍上下留白相等。
- Answer comparison card：
  - 上：あなたの回答 label／data
  - 虛線
  - 下：圖片字逐字比較
- MATCH：Ink。
- WRONG／MISSING／EXTRA：Danger。
- Overlay 必須與 kana 保持疊合。
- 圖片字同步縮放；放不下才換兩行。
- Footer：
  - 尚有下一題 → 次へ
  - 最後一題 → 結果へ
  - 無制限模式同時可顯示次へ與結果へ時，左右並排

### 16.6 Judgement Modal

- 只供 superuser。
- Title：判定詳細。
- 每個比較單位：
  - 第一行：正解 data、回答 data
  - 第二行：種類 data、詳細種類 data
- MATCH／MISSING 等 type data 使用對應顏色。
- Units 之間用虛線。
- Modal 最大 80dvh；只捲動中間資料。
- Header title 與 footer 完了固定。
- 完了、backdrop、Esc 均可關閉。

### 16.7 Summary

- Header：結果、Home；無 Back。
- 可愛圖片位置較 Answer Result 細。
- ended_early 時顯示原因 card。
- 五項統計：
  - 回答した問題
  - 正解
  - 不正解
  - スキップ
  - ヒント
- 第一項 full-width；其餘兩行各兩欄。
- 320px 仍保持兩欄，按規格縮小 gap、padding、字級。
- Data 全部用 Ink；label 使用各自功能色。
- Footer：クイズ設定へ。

### 16.8 No-question

- Header：クイズ、Home。
- 狀態 card：
  - 問題が見つからないよ。
  - 設定を確認してみてね。
- 不顯示題號、題目、答案、Tips、Skip。
- Footer：クイズ設定へ。

### 16.9 No-pool Confirmation

- Header：クイズ設定、Home。
- 狀態說明：
  - この条件で出せる問題がないよ。
  - 条件を変えるか、すべての出題対象から始めますか？
- Footer 兩粒等寬：
  - 設定へ戻る（Secondary）
  - すべてから出題（Primary）

---

## 17. Error pages

### 17.1 共通

- 400、403、404、500 共用 layout。
- 不顯示一般 header。
- 內容在 viewport 中央。
- 顯示 error code、插圖、日文 title、說明、ホームへ。
- 500 使用 self-contained template，不依賴 base context。
- 正式插圖未提供前使用 placeholder。

### 17.2 文案

400：

- Title：そのリクエスト、通ると思いました？
- Body：入力内容かURL、ちゃんと確認してくださいね。

403：

- Title：誰でも入れると思わないでください。
- Body：権限がないので、おとなしく戻ってください。

404：

- Title：
  - どこどこ？
  - ページはどこ？
  - ……ないよ。
- Body：いくら探してもありませんよ。URLを確認して、ホームへ戻ってください。

500：

- Title：
  - 僕のせいだけど、
  - 謝るつもりはない
  - www
- Body：しばらくしてから、もう一度試してください。

---

## 18. UI confirm page

- Route：/ui-confirm/。
- 只在 DEBUG=True 註冊。
- 不加入一般 navigation。
- 提供：
  - Activation 等待、成功、已認證、無效／過期
  - Quiz No-question
  - Error 400、403、404、500
- Activation preview 不得執行真實 activation 或修改資料。

---

## 19. 插圖與 icon 方向

- 網站角色與 Home icon 使用單柱 pyramid tent 主題。
- Tent 不擬人化，不加入眼、嘴、手、腳。
- 狀態以入口、燈光、角度、天氣、小道具表達。
- Home icon 使用簡化 vector tent，保留「ホーム」accessible label。
- 正式 asset 由 owner 設計；UI 只保留位置、尺寸、安全邊界與 accessibility。
- Quiz 狀態圖片未定前使用 construction placeholder。

---

## 20. Future scope

### 20.1 Multiple Choice Quiz

MC 不屬於 v1.0.0 阻塞項目，但保留以下方向：

- Question card 顯示 question／meaning；答案位置底線及活用提示使用提示色。
- 四個答案 button 垂直排列、同尺寸、無 A／B／C／D。
- 點選只改 selected state，按回答才提交。
- Hint 每次排除一個錯誤答案並顯示 ----；不自動選正確答案。
- Tips／Skip 沿用 non-MC。
- MC Result 顯示完成句、あなたの回答與正確答案。
- MC 不顯示判定 modal。
- Footer 流程跟 non-MC 一致。
- 提示紅色仍待確認，須與 Danger error red 清楚區分。

### 20.2 Admin Event Create

- Admin-only custom site page，仍使用日文。
- Fields：種類、タイトル、内容；全部必填。
- 對象第一版固定全體 user。
- Footer：公開。
- 提交前確認：「全ユーザーに公開します。よろしいですか？」
- Publish／expire、importance、active status 不納入第一版。
- 返回目的地仍待 admin event management flow 確定。

---

## 21. 尚待確認

以下未成為 final token，不得在實作時自行猜測：

1. Quiz input mode 的 panel 高度與前景答案區最小高度。
2. Quiz answer input focus、cursor、delete 與圖片字細節。
3. Future MC 的提示紅色。
4. Admin Event Create 的返回目的地。
5. 正式 tent／Quiz illustration assets。

---

## 22. 實作與驗收原則

### 22.1 結構

- 共用尺寸由 component class 或 design token 定義。
- 不依賴 parent DOM nesting 改變 button padding。
- 不逐頁複製相同 CSS。
- Django template 使用四格縮排，長 attribute 拆行。
- 所有 interactive control 有 keyboard focus 與 accessible name。

### 22.2 Responsive

至少檢查：

- 320px
- 390px
- 540px
- 大型 desktop viewport
- 高度低於 700px
- Mobile virtual keyboard 開啟狀態

### 22.3 視覺一致性

- 同 type element top／bottom padding 相等。
- 同 type 在不同頁面使用相同 padding。
- Header、content、footer 不產生水平 overflow。
- 固定 footer 不被 scrollbar 遮擋。
- Selection、checkbox、column header 正確對齊。
- 長文字只按已定規則換行，不任意縮小或截斷。

### 22.4 行為

- Skip 不算已回答。
- 未保存確認只在規格指定的 site navigation 觸發。
- State-changing action 使用 POST 與 CSRF。
- Disabled／unavailable 行為按頁面規格處理，不只依賴外觀。
- UI confirm 永不修改真實資料。

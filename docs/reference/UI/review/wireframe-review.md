# Wireframe Review

呢份文件用嚟集中記錄現有 wireframe 對照 `UI-design.md` 後發現嘅問題、需要確認嘅項目同修改決定。

> 記錄原則：先記錄 review 意見，唔會因為新增項目而即時修改 UI。

## Review 第一輪修改（2026-10-05，待使用者覆核）

- 已按本次 review 修改現有 Django templates、共用 CSS 及 Quiz JS；下方原始 review 意見保留作逐項覆核依據，未將實作完成視為使用者已驗收。
- 共用：恢復 4 spaces 縮排並展開巢狀 markup；page header、list header／filter toolbar 改為有左右留白的圓角 frame；虛線使用 8px 線段／6px 間距；pagination 改為 36px 正方形；主要 button 文字採用 18px Bold。
- 字體：沿用已定 Zen Maru Gothic／Hachi Maru Pop，改用現有 preview 的本地字體與 OFL 授權檔，避免依賴 Google Fonts 網絡載入。暫用 TTF，三款總計約 12 MB，壓縮及分包尚未處理。
- Homepage：已登入單詞簿改連 User vocab filter；主要 buttons 放大、身份 frame 收窄；學習資料標題置中；角落按鈕限制在現有 540px shell 內。
- Form／profile：word 與 kana 等寬、textarea label 上左及輸入區下一行、固定種類 label 左／data 右、單行資料 frame 收窄高度；Login 提示與破棄確認句置中。
- Selection：未選取底色使用 preview 的 `#91AAB7`；Level 按實際選項數等分為單行；category button 尺寸暫時保留，等之後確認。
- Vocab／Event list：自訂 `list-item` 與 Tailwind 同名 display utility 撞名，已統一改為 `ui-list-item`，checkbox 恢復每行最左；出題対象改為「出題する／出題しない」；categories 底部多餘 padding 收窄。
- Event／Feedback：event type 圓角加大；Event detail 加分隔線及日期 label（暫用「日時」）；Feedback 恢復狀態 label、dropdown 靠右、item 小 frame 底色改回 preview 的 control 色。
- Quiz：兩個結果操作 buttons 同時出現時並排；題號 frame 按內容收窄，與結果狀態採相同圓角；判定 modal 每組 label／data 同行，種類按 type 顯色。
- 暫用而未定案：主要 button 使用內容寬度加 padding／現有容器上限，未採用全站 80% viewport 規則；結果狀態圓角暫用 14px；Word 按字數縮放並保留原有 28–42px 範圍；Login switch 顏色維持現況；高度方向的首頁角落定位上限仍待確認。
- Account activation 各狀態、No-question 及 400／403／404／500 的人工確認，延後至 `UI-design.md` 所記錄的下一版 `/ui-checking/` 入口完成後；今版未實作該入口。
- 驗證：11 個 Django tests、11 個 Playwright checks 通過；包含 320／390／540／1280px 的主要頁面與 checkbox 排列、表單、Quiz AJAX、Level 等寬單行及無限題數結果操作。資料使用獨立測試 SQLite，未用正式資料庫。

## 目錄

- [Review 第一輪修改](#review-第一輪修改2026-10-05待使用者覆核)
- [全站共用](#全站共用)
  - [Template coding style](#template-coding-style)
  - [UI 言語](#ui-言語)
  - [畫面配置](#畫面配置)
  - [Font](#font)
  - [Color setting](#color-setting)
  - [Background](#background)
  - [純通知與狀態資訊頁共用 frame](#純通知與狀態資訊頁共用-frame)
  - [Success toast](#success-toast)
  - [可愛圖片與狀態插圖](#可愛圖片與狀態插圖)
- [Homepage](#homepage)
- [Vocab](#vocab)
  - [Vocab list filter](#vocab-list-filter)
  - [User vocab list filter](#user-vocab-list-filter)
  - [Vocab list](#vocab-list)
  - [User vocab list](#user-vocab-list)
  - [Vocab detail](#vocab-detail)
  - [User vocab detail](#user-vocab-detail)
  - [Vocab create／update／delete request](#vocab-createupdatedelete-request)
- [Account](#account)
  - [Login](#login)
  - [Registration](#registration)
  - [Account activation email sent](#account-activation-email-sent)
  - [Account activation](#account-activation)
  - [Resend activation email](#resend-activation-email)
  - [Logout result](#logout-result)
  - [User profile](#user-profile)
- [Event](#event)
  - [Event list](#event-list)
  - [Event detail](#event-detail)
  - [Admin event create（future）](#admin-event-createfuture)
- [Feedback](#feedback)
  - [Feedback create](#feedback-create)
  - [Admin feedback list](#admin-feedback-list)
  - [Admin feedback detail](#admin-feedback-detail)
  - [Admin feedback reply](#admin-feedback-reply)
- [Quiz](#quiz)
  - [Quiz setting](#quiz-setting)
  - [Question](#question)
  - [Input mode](#input-mode)
  - [Non-MC answer result](#non-mc-answer-result)
  - [Judgement modal](#judgement-modal)
  - [MC question（future）](#mc-questionfuture)
  - [MC result（future）](#mc-resultfuture)
  - [Summary](#summary)
  - [No-question](#no-question)
  - [No-pool](#no-pool)
- [Error pages](#error-pages)
  - [400](#400)
  - [403](#403)
  - [404](#404)
  - [500](#500)

## 全站共用

### Template coding style

- 狀態：待確認規格。
- 現有 wireframe templates 將原本 4 spaces 縮排改成 2 spaces，亦有多層 HTML elements、Django template tags 同完整 blocks 壓成同一行，令 hierarchy 難以閱讀。
- 原有 coding style：
    - 每層 HTML element 及 Django template block 使用 4 spaces 縮排。
    - 巢狀 elements、`{% if %}`、`{% for %}`、`{% include %}` 等按 hierarchy 分行及縮排。
    - 包含子元素或較長內容嘅 element，opening tag、內容同 closing tag 分行。
- 待確認：opening tag 嘅 attributes 應該喺咩情況拆行，以及拆行後 attributes 同 closing `>` 嘅對齊方式。
- 暫時只記錄問題，未修改 templates；確認後將正式規則加入 `UI-design.md`。

### UI 言語

### 畫面配置

- Footer bar 喺頁面出現水平捲動軸時會有部分被 scrollbar／slider 遮住，繼而令畫面額外產生垂直捲動。
- 左上 Event button 同右上 Logout button 目前會持續隨 viewport 加闊而向外移，固定貼近 viewport 左右上角。
- 期望行為：viewport 變窄時兩個 buttons 可跟住向內移及縮短；當 viewport width／height 大過指定上限後，位置停止再向外擴張。上限數值待完成 review 後確認。
- 所有 element frame 嘅高度未有按用途清楚分類，之後需要按 frame type 詳細定義高度、padding 及內容密度。
- 至少要區分單行 field／data frame、主要 action、次要 action、資訊卡及列表 row，避免所有 frame 套用近似高度。
- Category／分類選擇 buttons 可能全站整體偏大；暫未確定係 button 尺寸、padding，定 surrounding frame 比例造成，先記錄並留待完成 review 後比較。

### Font

- 多個頁面嘅 button、單字、讀音及 pagination 文字明顯比 preview 幼，懷疑全站實際使用咗錯誤 font 或錯誤 font weight。
- 待全部 review 完成後，統一核對實際載入字款、各類文字嘅 font family、weight 同 size。

### Color setting

- 全站虛線變成非常細粒嘅點狀效果，同 preview 已確認嘅虛線風格不一致。

### Background

- Background 顯示符合預期。

### 純通知與狀態資訊頁共用 frame

### Success toast

- Viewport 頂部短訊通知嘅顯示符合預期。

### 可愛圖片與狀態插圖

- 正式可愛圖片／狀態插圖尚未使用，今次未能 review；目前只保留 placeholder／預留位置。

## Homepage

- 「ゲスト」frame 相對 preview 大咗好多，由次要 element 變成接近主要 element，視覺層級失衡。
- 三個主要 action buttons 比 preview 明顯縮細，主要操作感減弱。
- 登入狀態下兩個主要 buttons 同樣比 preview 細。
- Preview 中主要 button 相對文字有明顯 padding：左右各約 2–2.5 個字位，整體高度約為文字高度嘅 2.3–2.5 倍；目前 buttons 只係略大過文字，主要操作感不足。
- 「学習データ」未有置中。
- 登入狀態頁面亦受全站 footer 水平／垂直 overflow 問題影響。
- 左上 Event button 及右上 Logout button 嘅 responsive 定位需要跟從「畫面配置」所記錄嘅 viewport 上限行為。
- 已登入狀態下「単語帳」button 目前錯誤連到一般 Vocab filter；應連到 User vocab filter。
- 只有未登入狀態下嘅「単語帳」button 先連到一般 Vocab filter。

## Vocab

### Vocab list filter

- 全部 buttons 嘅文字比 preview 幼，需要連同全站 font 問題核對係咪使用咗錯誤 font 或 font weight。
- Selection button 喺未選取狀態時嘅顏色，同之前確認嘅設計不一致。

### User vocab list filter

- 整體問題大致同 Vocab list filter 相同：buttons 字體過幼，未選取 selection button 顏色亦同已確認設計不一致。
- 修正時需要保持兩個 filter pages 使用同一套 component 規格。

### Vocab list

- 「単語／読み方」table header 嘅背景同 frame 應與 table body 保持同一套圓角容器風格；目前變成長方形。
- Table header width 覆蓋成個 viewport，左右完全無留白，同 preview 比例不一致。
- Word 同 kana 嘅字體比 preview 幼，需要納入全站 font 問題一併核對。
- Footer 嘅 first／previous／page number／next／last buttons 原本偏向正方形，目前變成高身長方形。
- Pagination 文字同樣比 preview 幼。

### User vocab list

- 每行 user vocab 嘅「V」indicator 應放喺最左側；目前顯示喺 row 上方中央，位置錯誤。

### Vocab detail

- Categories 內容下方同 frame bottom 之間有過多 empty space，需要收窄底部留白。

### User vocab detail

- 「出題対象」目前顯示為「はい／いいえ」；preview 已定為「出題する／出題しない」。

### Vocab create／update／delete request

- Update request 嘅 type 欄目前 field name 同 data 一齊黐喺左側；需要 field name 靠左、data 靠右。
- Create request 同 Update request 嘅 word／kana input boxes width 應保持一致。
- Create request 同 Update request 嘅意味／理由等較長文字欄，需要 field name 放喺上方左側，textbox 放喺下一行。
- Create request 嘅 level buttons 需要縮細，並同 Quiz setting 嘅 level buttons 使用一致尺寸規格。
- 表單未提交就返回上一頁時顯示嘅破棄確認 modal，其確認句需要置中。
- Delete request page 嘅個別 layout 大致符合預期；主要只受全站 font、header／`page_title` frame 等共通問題影響。

## Account

### Login

- 「狀態保持」switch 開啟時嘅顏色同 preview 不同；目前顏色觀感可接受，但 `UI-design.md` 似乎未有記錄 switch on-state 顏色，需要完成 review 後確認係保留現況定跟 preview。
- Login button font size 比 preview 細。
- Login button width 目前接近 viewport width，比例同 preview 不一致。
- 印象中原規格可能係 viewport width 嘅 80%，但尚未確認，需對照設計記錄後再定。
- 未 activation 提示文字失去置中。

### Registration

- 「登録」主要 button 目前闊度接近成個 viewport，與 preview 嘅主要 button 比例不一致。
- Button font size 明顯細咗約 2–3 級，失去主要 action button 嘅視覺層級。
- 推測相關位置屬於 `page_title` block：preview 原本係圓角 frame，目前變成橫跨頁面嘅大型長方形，風格完全不同。
- `UI-design.md` 似乎未有明確記錄 `page_title` frame 嘅形狀及尺寸規格，完成 review 後需要確認並補充。

### Account activation email sent

- 個別 layout 符合預期；其餘只需跟隨全站共通問題修正。

### Account activation

### Resend activation email

- 主要 button width 過大，需要同其他接近 viewport width 嘅 buttons 一併定義寬度上限；實際比例待完成 review 後確認。

### Logout result

- 個別 layout 符合預期；其餘只需跟隨全站共通問題修正。

### User profile

- 「学習データ」未有置中。
- Username、email、last login 若以 field name 與 data 同一行顯示，frame 高度應降低，避免單行資料使用過高容器。
- 前往 User vocab 嘅 button width 過大，情況同其他接近 viewport width 嘅主要 buttons 相似。
- 該 button 可能應採用約 viewport width 80% 嘅限制，但數值尚未確認，需連同全站 button width 規格一併定義。

## Event

### Event list

- 包住「すべて／未読／既読」三個 filter buttons 嘅 container，目前變成覆蓋整個 viewport width 嘅長方形；應恢復為有左右留白嘅圓角 frame。
- Event list item 排位出現同 User vocab list 一樣嘅問題：「V」indicator 目前喺 row 上方置中，應放喺每行最左側。
- List item 內 event type frame 嘅圓角比 preview 細。
- 「已讀」button width 過大，比例明顯失衡。

### Event detail

- Page title 同內容之間缺少虛線分隔。
- 內容同日期之間需要加入虛線分隔。
- 日期目前無 field name；呢點之前未有明確規格，完成 review 後需要補定。
- 日期欄應跟其他 pages 嘅一般 field 排列：field name 靠左、data 靠右。
- Event type frame 同 Event list 一樣，圓角比 preview 細。

### Admin event create（future）

## Feedback

### Feedback create

- 個別 layout 符合預期；其餘只需跟隨全站共通問題修正。

### Admin feedback list

- 狀態 label 消失，需要恢復顯示。
- Dropdown 內文字需要靠右對齊。
- Feedback item 嘅 title frame 同 type frame，其 background color 同 preview 不一致。

### Admin feedback detail

- 個別 layout 大致無額外問題；主要受全站 font、header／frame 等共通問題影響。

### Admin feedback reply

- 個別 layout 大致符合預期；其餘只需跟隨全站共通問題修正。

## Quiz

### Quiz setting

- Level buttons 目前太大太闊；正常 viewport 下希望全部保持同一行排列，而且每個 button 尺寸一致。
- Last setting button 同樣過闊；可考慮限制為 viewport width 約 80%，但呢個比例尚未定案，完成 review 後再討論。

### Question

- Question state 嘅個別 layout 大致符合預期。
- Tips button 同 Skip button 嘅顏色同已確認設計不一致。

### Input mode

- Input mode 個別 layout 符合預期；其餘只需跟隨全站共通問題修正。

### Non-MC answer result

- 「次」同「結果」兩個 buttons 同時出現時，需要左右並排。
- 無設定回答題數時，「第幾問」frame 目前仍然過闊，似乎預留咗顯示總題數文字嘅空間；無總題數時應收窄。
- 「第幾問」frame 同「正解／不正解」frame 嘅圓角需要一致。
- 圓角基準可約為目前「正解／不正解」frame 再圓少少，實際數值完成 review 後確認。
- Word 似乎未跟從「字數較少時字體較大」原則；之前未定最大 font size，需完成 review 後再討論。

### Judgement modal

- 目前 field name 同 data 分成上下兩行；需要改為每組 field name 與 data 同行。
- 第一行排列：「正解　X」同「回答　X」左右並排。
- 第二行排列：「種類　XXXXX」同「詳細種類　XXXXXX」左右並排。
- 兩行均維持左右兩組資料嘅清晰間距及對齊。
- 「種類」data 目前全部顯示黑色，缺少應有嘅類型顏色區分。

### MC question（future）

### MC result（future）

### Summary

- 個別 layout 符合預期；其餘只需跟隨全站共通問題修正。

### No-question

### No-pool

- No-pool confirm 個別 layout 符合預期；其餘只需跟隨全站共通問題修正。

## Error pages

### 400

### 403

### 404

### 500


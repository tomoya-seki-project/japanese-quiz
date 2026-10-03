# User Interface Design Idea

呢份文件用嚟記低我對japanese-quiz UI嘅想法。

## 目錄

- [UI言語](#ui言語)
- [畫面配置](#畫面配置)
- [Font](#font)
- [Color setting](#color-setting)
- [Background](#background)
- [純通知與狀態資訊頁共用frame](#純通知與狀態資訊頁共用frame)
- [Success toast](#success-toast)
- [Page previews](#page-previews)
- [UI sample](#ui-sample-0104jpeg)
- [可愛圖片與狀態插圖建議](#可愛圖片與狀態插圖建議)
- [Homepage](#homepage)
- [Vocab lists與filters](#vocab-list-filter-and-user-vocab-list-filter)
- [Account pages](#login-page)
- [Vocab detail與request pages](#vocab-detail-page)
- [Event pages](#event-list-page)
- [Feedback pages](#feedback-create-page)
- [Quiz](#quiz-setting-page)
- [Error pages](#error-pages)

## UI言語

- Django `/admin/`以外的所有site page一律使用日文UI，不因登入user是一般user或admin而改變語言
- 只限admin使用的custom site page，例如Feedback admin pages同Admin event create page，亦使用日文UI
- Site內只向admin顯示的開發／診斷UI亦使用日文；例如Quiz Answer Result的`判定詳細`modal欄名不可因只限admin查看而保留英文
- Django `/admin/`維持現有顯示語言；不為強制全英文或全日文加入額外converter code

## 畫面配置
- 以方便mobile睇為標準，將全部items集中係畫面中間；中央frame只代表內容寬度範圍，不是一個實際可見的大框
- 不使用一個大frame包住整頁所有內容
- 參考UI-sample-01的「今月／收入／支出」：每組`field name + data`各自使用一個獨立小frame／card包住
- 不同資料組使用不同小frame／card，card之間保留間距並讓page background顯示出來
- Field container統一使用近白色圓角frame／card，底色為`#F8FCFF`，固定使用90%不透明度
  - Read-only資料：`field name + data`放在同一個frame內
    - Vocab Detail與User Vocab Detail的同一model唯讀屬性屬於資料table例外：同一語意群組內的多個field可以共用一個table frame，並以分隔線區分row；不需要將每個field拆成獨立card
    - 這個例外只適用於同一model、唯讀而且屬於同一資料群組的detail資料，不適用於form input、不同model／section或一般互不相關的read-only資料
  - Text input同textarea：`field name + input area`放在同一個frame內，例如Create Request的`単語`、`意味`同`理由`
  - Button selection field：`field name + selection buttons`放在同一個frame內，例如`種類`、`JLPTレベル`同`カテゴリー`
  - 各field frame寬度一致，佔滿viewport可用寬度（扣除左右padding）
  - Frame本身90%不透明；input area、selection button、weight bar等實際control保持完全不透明
  - Header、固定底部操作區、modal同toast不跟field frame透明，保持完全不透明
  - Selection field統一使用`field name → 單虛線 → selection buttons`結構；包括Filter、Quiz Setting、Vocab Request及其他同級selection control
  - 單行input同dropdown縮短高度並保留至少44px可點擊／輸入高度；textarea按內容需要保留多行高度
  - 單行input內的輸入文字靠右；textarea同dropdown文字靠左，dropdown右側固定保留獨立下箭嘴
  - Field frame高度按內容加固定上下padding，不保留無用途的大面積底部空白
- `工事進行中`分成兩種用途；兩者可以沿用黃黑施工警示視覺，但行為、尺寸同取代方式不同
  - **未完成功能遮罩**
    - 用於已經準備好真實data／list架構、但功能尚未開放的section
    - 用高不透明度的大型近白遮罩覆蓋尚未可用的data／list部分，遮罩顯示`工事進行中`
    - Section title仍留在原本frame內可見；遮罩只蓋住title下面的未完成內容
    - 遮罩圓角極低但不為0，亦不可操作下面被覆蓋的control
    - 遮罩外圍使用幼身黃黑斜紋施工警示border；近白高不透明內容層放在border內，保留文字可讀性
    - 這個暫時遮罩不視為一般page的大型中央frame，不改變全站以獨立小card分組的原則
  - **未完成插圖placeholder**
    - 用於正式可愛插圖或狀態圖片尚未完成的預留位置，不覆蓋任何真實data或可操作control
    - Placeholder按該頁未來插圖區的最大尺寸顯示，通常比未完成功能遮罩細
    - 可以使用同一套幼身黃黑斜紋施工警示border及近白內容層，中央顯示`工事進行中`
    - 正式圖片完成後在同一位置直接取代placeholder，不改變周圍layout
- 所有固定viewport底部操作區統一使用Quiz Setting式完整近白底欄
  - Button、pagination或兩者一同放在同一個固定底欄內，不直接浮在kana背景上
  - 底欄內所有element按視覺高度垂直置中，上下留白相等；mobile safe area另行加在底部，不計入視覺留白
  - 同一底欄同時包含操作button同pagination時，兩行共用版面計算；只保留一組14px行間距，不疊加兩行各自的內側padding
  - Pagination三組按鈕維持左組靠左、頁碼組置中、右組靠右；各組內按鈕統一保留6px間距
  - 可見頁碼數按viewport width調整，方向button保留原本三組位置
    - 480px或以上：中央最多顯示5個page number
    - 360px至479px：中央最多顯示3個page number
    - 320px至359px：中央只顯示目前page number
    - 各breakpoint都以目前頁為中心選取相鄰頁碼；接近第一頁或最後一頁時向仍有頁碼的一側補足
  - 底欄統一左右padding與垂直間距；button下面只保留必要padding及mobile safe area，不留無用途的大面積空白
  - 同時有action button同pagination的list page使用同一個連續底欄分成上下兩行
- 手機內容佔滿viewport，只留左右 padding
- 最低正式支援viewport width為320 CSS px
  - 320px或以上不顯示橫向捲動；frame按可用寬度收窄，並按各page規則換行、轉列或增加高度
  - 文字與button保留最低可讀字級及最低可點擊尺寸，不為極窄畫面無限縮小
  - 低於320px視為正式支援範圍外；保持最低內容寬度，必要時容許少量橫向overflow
- desktop mode中央frame最大闊度約手機畫面寛度，唔會跟screen size無限擴闊
- 矮身手機viewport使用compact mode
  - viewport高度低於700px時啟用
  - Header高度由72px縮至60px
  - 一般button高度由58px縮至50px
  - 固定底欄上下padding由14px縮至10px
  - Section之間的垂直距離縮短約20%
  - 字體大小、input高度同可點擊寬度保持不變，避免因短畫面降低可讀性或操作性
  - Header同固定底欄繼續固定，中間內容區維持獨立捲動
- 手機虛擬keyboard顯示時使用輸入專注模式
  - 只在文字input／textarea取得focus而且虛擬keyboard實際打開時啟用；desktop實體keyboard focus不觸發
  - Header同固定底部操作欄一同暫時收起，將可用畫面集中畀目前輸入欄位
  - Form area自動捲動，確保focused field完整顯示在keyboard上方
  - Keyboard關閉後恢復Header同固定底欄，保留已輸入內容及原本form捲動位置
  - Dropdown、switch同selection button不會彈出文字keyboard，因此不套用輸入專注模式
  - 虛擬keyboard規則優先於compact mode；keyboard關閉後再按目前viewport高度恢復一般或compact layout


## font

### 採用方向

- 全站一般正文、form、table同資料內容使用`Zen Maru Gothic`
  - 保持圓潤、輕鬆、唔太正經的感覺
  - 相對適合較長內容同mobile UI閱讀
- 所有page header中央頁名、狀態頁主標題、Error page主標題同modal title使用`Zen Maru Gothic Bold`
  - 基準字級跟Activation Already preview的28px；過長時先換行，再按需要逐級縮小
  - 內容區section heading維持較細字級，不套用page title的28px規則
- 所有主要button使用`Zen Maru Gothic Bold`，避免只有Regular字重的`Hachi Maru Pop`在button上顯得太幼
  - Button文字按實際文字高度在button內水平及垂直置中，不使用固定baseline偏移作視覺補位
- `Hachi Maru Pop`只保留作短裝飾文字或Homepage的暫定`言葉の輪`wordmark；wordmark將來會換成正式logo
- Field name正式使用20px粗體；data同input文字使用16px，`任意`等輔助標記使用13px
- Quiz輸入答案及答案比較繼續使用現有HGS創英角ポップ体風格PNG
  - 只限Quiz kana keyboard、輸入答案同答案比較的視覺字形
  - 這批PNG不作一般UI字體使用

### 曾考慮的字體記錄

- `Zen Maru Gothic`
  - 圓潤、柔和，適合作為全站一般UI字體
  - 目前採用為正文、form、table同資料內容的主要方向
- `Hachi Maru Pop`
  - 以可愛丸文字同不規則手寫感為特色
  - 只保留作短裝飾文字及暫定Homepage wordmark；不再用於page title、modal title或主要button
- `Zen Kurenaido`
  - 有原子筆手寫感，筆畫粗幼、字形大小同水平位置帶輕微不規則感
  - 字體較幼，暫不作主要button或全站正文；保留為角色對白或特殊裝飾文字候選
- `Yomogi`
  - 手寫感更強，字形親切而有個性
  - 整體非常幼，暫不作全站主要字體；保留為少量說明或角色對白候選
- `Mochiy Pop One`
  - 粗身、活潑，適合遊戲感或雜誌感的大標題
  - 正文使用會太搶眼；保留為大型活動標題或特別狀態文字候選
- `M PLUS Rounded 1c`
  - 圓角清楚，UI可讀性穩定，但整齊感較強，少咗所需的不規則手寫味
  - 暫不採用，保留為`Zen Maru Gothic`無法使用時的替代方向
- `Noto Sans JP`
  - 表格、長文同細字的可讀性高，但氣氛較正式
  - 暫不作主要視覺字體；可作系統fallback候選
- `HGS創英角ポップ体`（PSD metadata：`HGSSoeiKakupopta`）
  - 現有Quiz kana PNG的主要字體風格
  - 不直接作網站一般webfont使用
- `小塚ゴシック Pr6N Regular`（PSD metadata：`KozGoPr6N-Regular`）
  - 在現有Quiz kana原始PSD metadata中同時出現
  - 不作目前UI字體候選，只保留來源記錄

### 實作時驗證

- Font family、font weight同各類文字的基準字級依照本文件已確認規格，不在實作時重新決定
- 實作時只按實際render結果微調行距、fallback stack，以及過長文字的逐級縮小門檻
- 要驗證日文、英文、數字同符號混排效果，特別是table、時間、weight數值同form validation message

## Color setting

- 配色實際色板預覽：[`color-palette-preview.png`](./preview/png/color-palette-preview.png)（[`SVG原稿`](./preview/svg/color-palette-preview.svg)）
  - 色板目前列出的顏色已全部確認；`CONFIRMED`代表已納入正式UI規格
- 綜合視覺草稿：[`ui-style-preview.png`](./preview/png/ui-style-preview.png)（[`SVG原稿`](./preview/svg/ui-style-preview.svg)）
  - 用於一併預覽背景、獨立card、文字、form、狀態同button；圖內列出的未定項目仍需逐項確認
- Vocab Create Request page目前草稿：[`vocab-create-request-preview-selection-light-dark.png`](./preview/png/vocab-create-request-preview-selection-light-dark.png)（[`SVG原稿`](./preview/svg/vocab-create-request-preview-selection-light-dark.svg)）
  - 所有field frame固定使用90%不透明度
  - Selection button參考UI-sample-02頂部`支出／収入`：同一藍色系內，已選項較亮、未選項較暗；不加check icon；選項正式使用4px小圓角，藉輪廓同大圓角主要操作button區分
- User Vocab Detail page目前草稿：[`user-vocab-detail-preview-all-frame-90.png`](./preview/png/user-vocab-detail-preview-all-frame-90.png)（[`SVG原稿`](./preview/svg/user-vocab-detail-preview-all-frame-90.svg)）
  - 所有data frame固定使用90%不透明度
  - 兩張page草稿用來檢查已定layout同整體配色；圖內`PROPOSAL`項目仍需逐項確認
  - PNG版本已將`Zen Maru Gothic`同`Hachi Maru Pop`直接渲染入圖片；部分IDE的SVG viewer可能忽略本地font並顯示fallback字體
- 主要button藍色比較結果選用候選B；原本`#477A99`只保留作細小功能icon／線條色
- 成個project ge UI button同圖案用藍色為主調
  - 主要button底色由偏暗的`#72ACCA`調亮為`#8BC9E6`，文字使用深藍黑`#26343D`
  - `#8BC9E6`同`#26343D`的對比度約為`7.07:1`
  - 主button保持比selected selection button更飽和；selection使用較淡的`#BFE8F7`，避免兩種control混淆
  - 原先`#477A99`大面積使用時太深、令粗圓文字視覺上太沉，因此不再用作button底色
  - `#477A99`保留作homepage、返回、通知等細小功能icon或幼線顏色，避免淺藍幼線辨識度不足
  - 所有有顏色的button使用實心底色，不使用近白底加彩色外框的outline button樣式
  - 一般／主要操作使用實心藍色；成功／正面操作使用實心綠色；危險／錯誤操作使用實心紅色
  - Button本身不顯示額外外框border；文字色按實心底色確保對比，較淺藍色使用深藍黑字，綠色同紅色使用`#F8FCFF`字
- 各獨立field／data frame使用`#F8FCFF`底色，固定使用90%不透明度
  - Kana背景會在frame之間清楚顯示，亦會在frame內淡淡透出
- 一般text使用帶少量藍調的深灰`#26343D`
  - 一般標題沿用同一色，透過字體、字重同字級建立層次，不另外增加近似深色
- 日期、時間、輔助說明、input placeholder同非主要metadata等次要文字使用`#607783`
  - `#607783`在`#F8FCFF`上的對比度約為`4.56:1`
- Card不使用可見border；以90%不透明底色、間距，以及淡藍灰柔和陰影同背景分層
  - 陰影正式沿用目前預覽效果：水平偏移0、向下偏移4px、約12px模糊範圍，使用深藍灰`#26343D`的16%透明度
  - 陰影只用作將card同kana背景分層，不形成明顯黑邊
- Input同dropdown預設狀態不使用border
  - 無border時使用淡霧藍灰`#EAF2F6`實色底，同`#F8FCFF` card區分輸入範圍
  - Keyboard focus使用`focus-visible`狀態顯示：內層使用深藍灰`#477A99`清晰輪廓，外層使用淡藍`#BFE8F7`光暈
  - Focus indicator只在keyboard navigation時顯示；mouse click不強制長期保留，亦不使用紅色以免同validation error混淆
- 同一table／field group內使用柔和藍灰`#91ADBC`幼單虛線；不同table／section之間使用更深的藍灰色較粗單實線並增加上下間距
  - Section實線第一版使用深藍灰`#477A99`，加強與背景kana及內部單虛線的區別
  - 分隔線只畫在近白內容frame內，避免直接與背景kana混在一起
  - 第一輪preview先檢查較粗單實線；如仍不清楚，再考慮加入淺色分隔帶
- Disabled control使用淡灰藍`#D5DFE4`底色及深灰藍`#687B85`文字
- 原本建議作control border的`#718F9F`取消既定用途，暫不列入已確認palette
- 成功／正解狀態使用柔和深綠`#39765B`
  - 用於Quiz正解、Feedback返信済み、success toast圖示或強調位置，以及其他成功狀態
  - 狀態同時配合icon或文字，不只依靠顏色表達
- 錯誤／不正解狀態使用柔和深紅`#AD4B55`
  - 用於Quiz不正解、form error邊框與field name、Feedback未対応、危險操作，以及error提示的圖示或強調位置
  - 狀態同時配合icon或文字，不只依靠顏色表達

## Background

- 全站背景使用`assets/export/background/kana_bg_output_blue/`內的kana tile系列
- 一般site page預設使用`mixed_tile`
  - 之後可以再考慮生成另一張專供一般page使用的mixed background
- Quiz背景按題目類型切換
  - 一般語彙／vocab題目使用`hiragana_tile`
  - Katakana題目使用`katakana_tile`
  - 將來Multiple Choice Quiz使用`mixed_tile`
  - Summary、No-question state及Quiz no-pool confirmation等沒有current question type的Quiz畫面使用`mixed_tile`
- 實作時按viewport同顯示密度，在現有`800x600`及`1600x1200`版本之間選擇合適asset
- Kana背景保持為page底層，會在各獨立小frame／card之間顯示
- 不使用覆蓋整個中央內容範圍的大型可見frame
- 各獨立field／data frame使用90%不透明底色，背景kana會淡淡透出；實作時需要檢查密集資料頁的可讀性
- 各小frame／card不顯示外框border
- 各小frame／card底色沿用Color Setting指定的`#F8FCFF`，opacity為`0.90`
- 背景圖片固定在viewport；頁面內容捲動時背景不跟隨移動
- 正式mobile實作需要檢查fixed background的捲動效能；如個別browser／裝置出現明顯卡頓，該環境可以降級成一般隨頁面捲動的背景，但唔改變圖片、尺寸或其他視覺規格
- 背景使用seamless repeat方式向四邊重複鋪排，不使用`cover`拉伸單張圖片
- 優先使用`1600x1200`高清tile，CSS顯示尺寸以`800x600`處理，保持kana大小一致並避免高DPI畫面模糊

## 純通知與狀態資訊頁共用frame

- 只顯示通知或狀態資訊的page，主要內容需要使用一個frame包住
- Frame內預設包括狀態icon／可愛插圖、標題、說明文字同該頁操作button
- Quiz No-question state及Quiz no-pool confirmation page屬於操作區例外：主要frame只包住狀態圖片及說明文字，操作button放在全站統一的viewport固定底欄
- Frame沿用全站field／data card樣式：`#F8FCFF`近白底、90%不透明度、無border，以及目前採用的淡藍灰柔和陰影
- 目前適用頁面
  - Account activation email sent page
  - Account activation page的等待、成功、已認證、link無效／過期狀態
  - Logout result page
  - Quiz No-question state
  - Quiz no-pool confirmation page
  - 400、403、404、500 Error pages
- Login、Registration、Resend activation email等有輸入form的page不套用這個純狀態frame規則
- 相關preview圖已更新

## Success toast

- form成功完成後，可以在viewport上方顯示一行簡短的成功提示
- 這個提示使用不阻擋操作的toast，不是modal
- toast在大約3秒後自動消失
- 以下操作使用success toast
  - Login成功
  - User vocab detail保存成功
  - Vocab新增申請成功
  - Vocab修改申請成功
  - Vocab刪除申請成功
  - Feedback送出成功
  - User vocab list批量保存成功
  - Event list的"既読にする"成功
  - Admin Feedback回覆成功
- 以下操作不使用success toast
  - Registration
  - Resend activation email
    - 以上兩項會轉到專用的結果／狀態page
  - Quiz相關form
  - Vocab list filter同User vocab list filter

## Page previews

- 已按本文件目前已定規格生成46張page／主要state預覽
- 全部預覽總覽：[`all-page-previews-contact-sheet.png`](./preview/png/all-page-previews-contact-sheet.png)
- 個別PNG同SVG索引：[`preview/README.md`](./preview/README.md)
- 預覽圖只用作layout、元件、字級同配色樣版；圖中使用的背景不代表所有正式頁面固定使用同一款tile
- 正式UI的背景選擇一律以本文件`Background`章節為準；其餘共通視覺沿用90%近白card、淡藍灰柔和陰影、20px粗體field name、16px data／input、13px輔助文字、4px selection button圓角、selection label下單虛線，以及縮短後的單行control高度
- 明確尚未完成規格的畫面暫不生成
  - Quiz Play已生成非MC Question state、50音keyboard input mode、非MC Answer result、判定modal、MC Question三種狀態、MC Answer Result、Summary兩種狀態、No-question state同No-pool confirmation preview
  - Admin Event Create page：主要form fields同公開確認流程已定；返回目的地仍要等admin event管理入口確定
- 預覽只記錄視覺方向，不代表已修改project template、CSS、JavaScript或Django code

## UI-sample-01~04.jpeg

- 這些圖片是我從其他apps中screen capture過黎的
- 佢地會係作為UIge 參考圖片
- 無需理會圖片中出現的卡通公仔圖案

## 可愛圖片與狀態插圖建議

- 本section集中記錄裝飾性角色圖片、狀態插圖同未來logo方向；由於Home icon共用pyramid tent主題，會在此記錄其造型方向，其他返回箭嘴、password眼睛等一般功能icon不放在這裏
- 所有建議以同一套可愛、簡潔、mobile畫面容易辨認的角色／插圖風格為方向
- 網站角色同Home功能icon統一使用露營帳篷主題，呼應網站owner喜歡camp的個人特色
- 主體造型使用真正單柱pyramid tent，不使用頂部伸出多支交叉長桿的tipi輪廓
- Error page同Account activation相關狀態頁共用同一個pyramid tent主體，按狀態改變入口、燈光、角度、環境效果或小道具
- 全站header內返回Homepage的icon亦由一般房屋改成簡化pyramid tent vector icon
  - 小尺寸功能icon保留清楚三角／金字塔帳篷外形同入口線，避免加入縮小後無法辨認的裝飾
  - Icon需要保留可理解的`ホーム`accessible label，唔可以只靠帳篷外形傳達功能
- Pyramid tent保持非擬人化：不加入眼、嘴、手或腳
- 不同狀態使用帳篷入口開合、內部燈光、傾斜角度、天氣效果及小道具表達，不依賴角色面部表情
- Home功能使用更簡化的純帳篷輪廓版本，不加入狀態裝飾
- Pyramid tent相關asset，包括Home icon同狀態頁帳篷圖的具體外形、線條、配色及美術細節，由網站owner自行設計，不在本UI規格流程逐項決定
- UI實作只預留已定位置、尺寸、安全邊界、可點擊範圍同accessible label；正式asset未提供前可以使用簡單placeholder
- 如網站owner之後主動要求，可以再協助整理、輸出、縮圖測試或接入asset，但不主動追問美術方向
- UI sample圖片內原有的卡通角色只作layout參考，不直接照搬
- Quiz相關圖片等待user之後提供Quiz sample再決定，本section暫時不為Quiz作圖像定案

### Homepage

- 以UI-sample-01.jpeg為主要參考，background使用一般page的`mixed_tile`
- Product name暫時顯示`言葉の輪`
  - 暫定文字比上一版放大50%，使用`Hachi Maru Pop`
  - 預留將來替換正式logo的空間
  - Logo area額外增加相當於username frame高度的48px垂直空間
  - Username／`ゲスト`frame以及其後所有非固定主要內容整體向下移48px；viewport底部固定footer及其button位置保持不變
- 已登入狀態
  - Product name下面的username使用獨立近白frame，避免與背景kana混在一起
  - 左上角使用門口加向外箭嘴vector icon執行logout；右上角使用鐘形vector icon進入Event List
  - 兩個icon各自放在較大的圓形近白底上；圓形中心放在viewport左右頂角之外，只讓朝畫面內側的下方圓角部分進入viewport，icon本身及可點擊範圍完整留在viewport內
  - 學習數據section第一版已建立`現在の連続数`、`最大連続正解数`、`最大連続不正解数`三個位置
    - `学習データ` title留在同一個section frame內可見
    - 未完成功能的三筆data由低圓角、高不透明度`工事進行中`遮罩覆蓋
    - 將來功能完成時移除遮罩即可，不重做layout
  - 中間兩個主button為`クイズ`同`単語の追加`
    - 相對上一版button尺寸放大約50%，各自按文字長度設定寬度並水平置中
    - Button文字亦跟隨整體尺寸放大約50%，使用`Zen Maru Gothic Bold`；唔只放大button背景
  - `プロフィール`、`単語帳`、`フィードバック`固定在viewport底部
    - 三個button等寬、字級一致
    - viewport足夠時三個一行
    - viewport不足時改成第一行兩個、第二行一個置中的`2 + 1`排列
    - 最多只轉成`2 + 1`，再窄時三個button一同逐級縮小字級，不轉成三個直排
    - 固定操作區要為可捲動內容保留相應bottom padding，避免遮住內容
- 未登入狀態
  - Product name下面的`ゲスト`亦使用獨立近白frame
  - 顯示`登録`、`ログイン`、`単語帳`三個垂直排列入口button，主button為`ログイン`
  - 三個button相對上一版一同放大約50%，不受已登入狀態底部三個導航button規則影響
  - 三個button文字亦跟隨button尺寸放大，使用`Zen Maru Gothic Bold`

## vocab list filter and user vocab list filter

- 以UI-sample-02.jpeg為參考
- 最高個行
  - "入力"改成對應ge"単語帳"、"マイ単語帳"
    - font size可以大少少
  - "完了" 改成homepage ge icon
  - 左邊左箭咀 都係做成上一頁ge功能
- "支出收入"改成"一般語彙"、"カタカナ"button，
  - 並以click左落去就係select左，無click落去就係無select為狀態
  - "副詞"、"擬音・擬態語"、"接続詞"、"口語表現" 為之後會加ge野，但v1.0.0唔會有住
    - 將來加了以上4種後，畫面闊度會唔夠，到時改成兩行
  - button為multi selection
- マイ単語帳的話
  - 下面加入`出題対象`的`はい`、`いいえ`兩個selection button
    - button為multi selection，每個button可以獨立切換選取／未選取狀態
    - 只選`はい`時顯示`in_use=True`的單語
    - 只選`いいえ`時顯示`in_use=False`的單語
    - 兩個button都未選或兩個button都選中時顯示全部單語
- 下面分別再係 JLPT lv selection
  - "未設定"、"N1"、"N2"、"N3"、"N4"、"N5"
  - 並以click左落去就係select左，無click落去就係無select為狀態
  - button為multi selection
- 再下面就係catagories,以三個一列 6行方式
  - 並以click左落去就係select左，無click落去就係無select為狀態
  - 如果畫面寛度過窄，不足是三個一列時
    - 自動改成2個一列
    - 如果連2個一列都太窄，再改成1個一列
  - 每個button的width and height一致
    - 如果字數太多就自動係space位/.位換行
  - button為multi selection
- viewport最下面固定顯示`検索`button
  - Button在固定底欄內水平置中

## vocab list and user vocab list

- 以UI-sample-04.jpeg為
- 最高個行(A行)
  - "履歷"改成對應ge"単語帳"、"マイ単語帳"
  - 右邊只顯示一個homepage icon
  - 左邊"もどる"保留功能變成返去 vocablistfilter / uservocablistfilter
  - stick on screen 唔會跟畫面滑動，固定係viewport最高
- 下面正式list部份(B行)
  - 最高位為table header部份左至右
    - マイ単語帳時
      - すべて(checkbox)
        - 只有效於當前頁面顯示中的items
      - 単語(word)
      - 読み方(kana)
    - 単語帳時
      - 単語(word)
      - 読み方(kana)
    - stick on screen 唔會跟畫面滑動，固定係viewport第二高位置，位於"単語帳"、"マイ単語帳"個行下面
    - 各column header之間顯示垂直分隔線；實作用固定線條而非文字`|`
    - 每個header文字與下面對應column data使用同一個水平起點／對齊方式
    - `単語`／word column使用較窄比例，`読み方`／kana column使用較闊比例；Vocab List同User Vocab List一致
  - 下面就係正式list
    - 左至右ge排法跟返table header
    - 如果単語(word)/読み方(kana)太長就自動分成兩行
      - 點為之長係實作後再定字數
    - 一般單行item使用較緊湊的frame高度並減少上下padding；只有文字實際換成兩行時，該item才按內容增加高度
    - 在list data不足以cover全list area時空白剩餘位置
    - list中每row的全行均為可以點擊進入該vocab detail page
      - マイ単語帳時，for in_use的checkbox不包含在進入user vocab detail page的點擊範圍內
- マイ単語帳時(C行)
  - 係list下面畫面中間位置加入"保存"button
  - stick on screen 唔會跟畫面滑動，固定係viewport第二低位置，位置page number個行上面
    - 在list data不足以cover全list area時，仍然固定係viewport第二低位置，位置page number個行上面
- 畫面最底部係 first、previous、page number、next、last button(D行)
  - Pagination放在完整近白固定底欄；如頁面另有保存／既読等action button，兩行共用同一個連續底欄
  - 最左邊係first page button
    - 用兩個向左箭咀代表
  - Pagination固定分成三個互不影響的區域
    - 左區：first、previous依此次序靠最左
    - 中區：目前顯示的page number整組以viewport水平中心置中
    - 右區：next、last依此次序靠最右
    - 方向button disable時仍保留原位，避免三個區域跳動
  - 左邊係previous page button
    - 用向左箭咀代表
  - 中間係page number list
    - 可見page number數量按全站pagination breakpoint調整；480px或以上最多顯示5個
      - 例:
        - page 1 and total page more than 5
          - 1 2 3 4 5
        - page 1 and total page is 3
          - 1 2 3
        - page 50 and total page more than 52
          - 48 49 50 51 52
        - page 32 and total page is 33
          - 29 30 31 32 33
        - page 23 and total page is 23
          - 19 20 21 22 23
  - 右邊係next page button
    - 用向右箭咀代表
  - 最右邊係last page button
    - 用兩個向右箭咀代表
  - previous, next, first, last button
    - 如果係page 1, first previous button 會灰左佢 disable左佢，但唔隱藏
    - 如果係已經係last page, last next button 會灰左佢 disable左佢，但唔隱藏
  - 如果係只得一頁ge情況
    - previous, next, first, last button 全部hide
    - 只留 page number 姐係"1"係下面
  - stick on screen 唔會跟畫面滑動，固定係viewport最底位
    - 在list data不足以cover全list area時，仍然固定係viewport最底位
- 除了正式list的部份外，其他部份我想佢地係hold住係畫面，唔會因為畫面上下滑動而離開畫面，只有正式list的部份才會因為畫面上下滑動而動
- 當手機瀏覽器地址列收起／展開時
  - 自動調整A行的Y值(應該係掛)，以保持位於viewport最高
  - C行and D行繼續保持位於viewport最低
  - B行，即正式list部份就條調節height黎應對viewport total height ge 變化
- マイ単語帳的勾選項目，在轉頁時未有保存的話直接放棄不用保留

## event list page
- 以UI-sample-04.jpeg為
- 最高個行(A行)
  - "履歷"改成"お知らせ"
  - 右邊只顯示一個homepage icon
  - 左邊"もどる"唔使留
  - stick on screen 唔會跟畫面滑動，固定係viewport最高
- 下面加入"すべて"同"未読"同"既読"ge switch button(B行)
  - 以UI-sample-02.jpeg中的"支出""收入"為參考
  - stick on screen 唔會跟畫面滑動，固定係viewport第二高位置，位於"お知らせ"個行下面
- 下面正式list部份(C行)
  - 最高位為table header部份左至右
    - 選択(checkbox)
      - 只有效於當前頁面顯示中的items
      - 每次進入或重新載入event list時，全部checkbox預設為未勾選
      - checkbox只代表今次批量設為已讀的選擇，不代表event本身的已讀狀態
    - 項目
    - `選択`同`項目`之間顯示固定垂直分隔線，視覺效果如`|`
    - `項目`與下面每筆item的type／title使用相同左邊起點
  - stick on screen 唔會跟畫面滑動，固定係viewport第三高位置，位於"すべて"同"未読"同"既読"個行下面
  - 下面就係正式list
    - 每頁顯示5筆event
    - 左邊係checkbox，右邊係項目內容
    - checkbox垂直跨過右邊的type同title，並置中顯示
    - 右邊項目內容分成上下兩行
      - 上面顯示type，使用較細的badge樣式
        - Badge底色改用較明顯的明亮淡水藍`#BFE8F7`
        - Type文字由目前preview約12px放大兩級至16px；badge高度同內距同步增加，避免文字逼近邊緣
        - 這項調整只適用於Event list的短版type badge，Event detail的完整type badge暫時不跟隨調整
        - 相關preview圖已更新
      - 下面顯示title，作為主要內容
      - type badge同title之間加入一條橫向分隔線
        - 分隔線使用柔和藍灰`#91ADBC`、2px單虛線，沿用detail table內的分隔語言
        - 相關preview圖已更新
    - list顯示用的type使用以下短版名稱
      - "単語申請の審査結果"顯示為"申請結果"
      - "単語"顯示為"単語"
      - "出題優先度の自動更新"顯示為"優先度更新"
      - "フィードバックへの返信"顯示為"フィードバック返信"
      - admin only的"New vocabulary request"顯示為"新規申請"
    - 完整type名稱保留在event detail page或admin顯示
    - title最多顯示兩行，超出的部份以"…"截斷
      - event detail page顯示完整title
    - 在list data不足以cover全list area時空白剩餘位置
    - list中每row除了最左邊的checkbox cell外，均為可以點擊進入該event detail page
    - list中的"未読"data，只將title以粗體字表示
      - type badge的字體粗幼不受已讀狀態影響
  - 係list下面畫面中間位置加入"既読にする"button(D行)
    - stick on screen 唔會跟畫面滑動，固定係viewport第二低位置，位置page number個行上面
      - 在list data不足以cover全list area時，仍然固定係viewport第二低位置，位置page number個行上面
    - 在當前選擇的"すべて"同"未読"同"既読"狀態下，如果list中間沒有data可以顯示就直接轉成no event ge畫面
      - "既読にする"button 唔需要show
- 畫面最底部係 first、previous、page number、next、last button(E行)
  - Pagination放在完整近白固定底欄；如頁面另有保存／既読等action button，兩行共用同一個連續底欄
  - 最左邊係first page button
    - 用兩個向左箭咀代表
  - Pagination固定分成三個互不影響的區域
    - 左區：first、previous依此次序靠最左
    - 中區：目前顯示的page number整組以viewport水平中心置中
    - 右區：next、last依此次序靠最右
    - 方向button disable時仍保留原位，避免三個區域跳動
  - 左邊係previous page button
    - 用向左箭咀代表
  - 中間係page number list
    - 可見page number數量按全站pagination breakpoint調整；480px或以上最多顯示5個
      - 例:
        - page 1 and total page more than 5
          - 1 2 3 4 5
        - page 1 and total page is 3
          - 1 2 3
        - page 50 and total page more than 52
          - 48 49 50 51 52
        - page 32 and total page is 33
          - 29 30 31 32 33
        - page 23 and total page is 23
          - 19 20 21 22 23
  - 右邊係next page button
    - 用向右箭咀代表
  - 最右邊係last page button
    - 用兩個向右箭咀代表
  - previous, next, first, last button
    - 如果係page 1, first previous button 會灰左佢 disable左佢，但唔隱藏
    - 如果係已經係last page, last next button 會灰左佢 disable左佢，但唔隱藏
  - 如果係只得一頁ge情況
    - previous, next, first, last button 全部hide
    - 只留 page number 姐係"1"係下面
  - stick on screen 唔會跟畫面滑動，固定係viewport最底位
    - 在list data不足以cover全list area時，仍然固定係viewport最底位
- 除了正式list的部份外，其他部份我想佢地係hold住係畫面，唔會因為畫面上下滑動而離開畫面，只有正式list的部份才會因為畫面上下滑動而動
- 當手機瀏覽器地址列收起／展開時
  - 自動調整A行同B行的Y值(應該係掛)，以保持位於viewport最高
  - D行and E行繼續保持位於viewport最低
  - C行，即正式list部份就條調節height黎應對viewport total height ge 變化

- 除了正式Homepage外，各app在`urls.py`內使用`path("", ...)`連接的開發初期temp page不列入UI設計範圍

## Login page

- 以UI-sample-02.jpeg為主要參考
- 最高一行
  - 中間顯示"ログイン"
  - 右邊顯示homepage icon
  - 左邊不需要返回按鈕，因為返回按鈕的用途會與homepage icon接近
- form置中顯示
- 只有最高一行header固定，不會跟畫面捲動
- header以下全部內容屬於同一個可捲動area，包括form、button同重發認證郵件area
- 每個field name單獨顯示一行，input area顯示在field name下一行，避免橫向排列令input area太短
- 單行input control縮短高度，輸入文字靠右；password亦靠右並為右側眼睛icon預留空間
- Textarea內容保持靠左；dropdown文字保持靠左並在右側顯示獨立vector下箭嘴
- input area設有最大闊度
  - viewport比input area最大闊度寬時，input area向右對齊內容範圍
  - viewport比input area最大闊度窄時，input area佔滿扣除左右padding後的可用內容闊度
- password input預設隱藏輸入內容
  - input右邊加入眼睛icon，用於切換顯示／隱藏密碼
  - Login page同Registration page共用這個設計
- "ログイン状態を保持"使用switch button
- form輸入有錯誤時
  - 在viewport正中位置顯示一個modal dialog
  - 原本form page保留在modal後面，並加上半透明深色遮罩
  - modal開啟期間，後面的form不能操作或捲動
  - modal一次過顯示全部輸入錯誤
  - modal設有最大height
    - 錯誤內容超過最大height時，只有modal內的錯誤內容area可以上下捲動
  - "閉じる"button長期固定在modal底部，不會跟錯誤內容捲動
  - 點擊modal外面的半透明深色遮罩亦可以關閉modal
  - 關閉modal後返回原本form
    - 所有輸入有錯誤的input加上紅色邊框
    - 對應的field name轉成紅色文字
    - Input邊框同field name沿用已確認錯誤紅色`#AD4B55`
    - 自動捲動並focus第一個有錯誤的input
- form下面的操作內容由上至下顯示，並與form一同捲動
  - "ログイン"button
  - "メールアドレス認証が完了していない場合は、認証メールを再送してください。"
  - "認証メールを再送する"button
- "ログイン"button位於重發認證郵件area上面
- 重發認證郵件說明同`認証メールを再送する`button放入同一個獨立近白frame

## Registration page

- form layout跟Login page相同
- 最高一行中間顯示"登録"，右邊顯示homepage icon，左邊不需要返回按鈕
- "登録"button放在form下面，並與form一同捲動

## Account activation email sent page

- Account activation相關狀態頁使用統一layout
  - 最高一行header固定，中間顯示對應頁面名稱，右邊顯示homepage icon
  - header左邊不需要返回按鈕
  - header以下的主要內容依次顯示狀態icon、標題、說明文字同操作button
  - Header頁名同主要狀態標題使用`Zen Maru Gothic Bold`，不使用`Hachi Maru Pop`；相對上一版預覽各提高兩級字級（24px→28px、27px→31px）
  - 狀態icon、標題、說明文字同操作button集中在主要內容範圍中間
  - 畫面太矮時，header以下整個主要內容area可以捲動
  - 狀態icon、標題、說明文字同操作button由共用90%不透明近白frame包住
  - 狀態icon位置將來換成網站共用的非擬人化金字塔帳篷；不同activation狀態使用入口開合、內部燈光、傾斜角度、天氣效果或小道具表達，不加入角色表情
- 此頁的狀態icon暫時使用信封圖案
- 顯示認證郵件已送出的標題同相關說明
- 操作button包括"ログイン画面に戻る"同"認証メールを再送する"
  - 兩個button垂直排列
  - "ログイン画面に戻る"使用主要藍色button樣式
  - "認証メールを再送する"使用較低調的次要button樣式

## Account activation page

- layout跟Account activation email sent page的共用狀態頁layout相同
- 根據狀態顯示不同內容
  - 等待確認啟用account時顯示對應icon、說明同"アカウントを有効にする"button
  - 認證成功時暫時使用剔號icon，並顯示"ログイン"button
  - account已經認證時使用對應狀態icon，並顯示"ログイン"button
  - 認證link無效或過期時暫時使用感嘆號icon，並顯示"認証メールを再送する"button

## Resend activation email page

- form layout跟Login page相同
- 最高一行中間顯示"認証メールの再送"，右邊顯示homepage icon，左邊不需要返回按鈕
- form只顯示メールアドレスfield
- "認証メールを再送する"button放在form下面，並與form一同捲動

## Logout result page

- 保留獨立的logout完成頁
- layout跟Account activation email sent page的共用狀態頁layout相同
- 中間保留狀態icon的位置，之後可以換成較可愛的圖片
- 顯示"ログアウトしました。"
- 加入"ログイン"button，讓user可以再次登入

## User profile page

- username、email同最後登入時間只作read-only顯示，不提供修改功能
- 最高一行header固定，中間顯示`プロフィール`，右邊顯示homepage icon，左邊留空
- username、email同最後登入時間各自使用較緊湊的field frame
- 學習數據section第一版已建立以下真實layout位置
  - `現在の連続数`
  - `最大連続正解数`
  - `最大連続不正解数`
  - `学習データ` title留在section frame內可見；title下面的未完成data由低圓角、高不透明度`工事進行中`遮罩覆蓋
- 學習數據下面顯示`マイ単語帳`button
- 最近回答section第一版已建立最近十題list所需的row／column結構
  - `最近の回答` title同list放入同一個近白frame，不再放在frame外，以免與背景kana混在一起
  - Title保持可見；title下面的未完成list由低圓角、高不透明度`工事進行中`遮罩覆蓋
  - 被遮罩覆蓋的內容不可操作；將來功能完成時移除遮罩即可

## Vocab detail page

- Vocab detail page同User vocab detail page共用同一套單語基本資料layout
- 最高一行header固定
  - 左邊顯示返回按鈕，返回進入detail page前的原本列表並保留當時的list／filter context
  - 中間顯示"単語の詳細"
  - 右邊顯示homepage icon
- 共用的單語基本資料包括
  - 単語
  - 意味
  - 読み方（かな）
  - JLPTレベル
  - 種類
  - カテゴリー
- 以上單語基本資料在UI上放在同一個table顯示
  - `カテゴリー`field name下面先顯示單虛線，再顯示Category tags；frame高度按tag實際內容收窄，唔保留多餘底部空白
  - 每個Category顯示成細小圓角tag
  - 所有tag的width同height一致
  - 最多三個Category的responsive排列
    - 預設一行並排三個
    - viewport闊度不足時，第一行顯示兩個，第三個在第二行置中
    - viewport再窄、連兩個都不能並排時，三個各佔一行並垂直排列，每個tag置中
    - 實際切換breakpoint在實作時根據tag尺寸決定
  - Category名稱太長時，tag內文字可以在空格或"・"位置換行，最多顯示兩行
- 單語基本資料table下面，根據vocab type顯示對應detail model的額外資料table
  - 額外資料table與Vocab基本資料table之間使用較粗單實線加較大上下間距分隔
  - `vocab` type顯示VocabDetail的資料
    - VocabDetail目前未有需要顯示的額外field
  - `katakana` type顯示KatakanaDetail的資料
    - 顯示"対応する日本語表現"
  - 有MCSense的vocab顯示MCSense資料
    - MCSense資料只在Vocab detail page顯示，不在User vocab detail page重複顯示
    - Vocab detail page遇到有MCSense的vocab時，頂部單語基本資料table隱藏`Vocab.meaning`，只使用下面各個`意味 1`、`意味 2`區塊顯示個別語意
    - User vocab detail page即使遇到有MCSense的vocab，亦只顯示頂部單語基本資料table的`Vocab.meaning`；不合併或另外顯示`MCSense.meaning`
    - 每個sense各自顯示成一個獨立資料區塊
    - 多個sense按`sense_no`順序排列
    - 每個sense區塊頂部以`意味 1`、`意味 2`格式顯示標題，數字使用該筆`sense_no`
    - 各sense區塊之間沿用table之間的較粗單實線分隔；實線置中，與上下兩個sense frame各保留24px
    - 每個sense區塊在標題下面直接顯示該sense的meaning，不再重複顯示另一個`意味` field label
    - 每個sense frame內以單虛線分隔`意味 n`標題、meaning內容及各個例文row
    - Frame高度按實際row數量收緊；最後一個row下面只保留正常padding，不留下大面積empty space
    - `question_1`同`question_2`顯示成已揭示答案的例句題目
      - `question_1`前顯示`例文 1`標籤，`question_2`前顯示`例文 2`標籤
      - 將原本的`____`換成正確答案基本形，正式UI不顯示底線
      - 保留原本的活用提示，不另外保存或生成活用後答案
      - 例如`____(て)`配合正確答案`ググる`，顯示成`ググる(て)`，不轉換成`ググって`
      - 正確答案部分`ググる`使用深藍灰`#477A99`粗體；活用提示`(て)`同句子其餘部分維持一般深色`#26343D`
    - 不顯示三個distractor答案
- Vocab detail page同User vocab detail page的資料顯示共用以下規則
  - 一般情況每行左邊顯示field name，右邊顯示資料
  - 資料太長或可用闊度不足時，自動轉成兩行
    - 第一行顯示field name
    - 第二行顯示資料，排列方式跟Login／Registration form的field相同
- 同一個table內的field之間使用單虛線分隔
  - table同table之間使用較粗單實線加較大上下間距分隔
- viewport底部固定顯示操作button
  - "変更申請"
  - "削除申請"
  - 兩個button左右並排，width同height一致
  - "変更申請"使用主要藍色button樣式
  - "削除申請"使用紅色警告button樣式
  - 顏色沿用已確認palette：`変更申請`使用`#8BC9E6`，`削除申請`使用`#AD4B55`
  - 操作button不會跟資料內容捲動
- Guest查看Vocab detail page時
  - 不顯示"変更申請"同"削除申請"button
  - 只保留header的返回按鈕同homepage icon作導航
- 已登入user查看時，header同viewport底部操作button固定，只有中間資料table可以捲動
- Guest查看時沒有底部操作button，header固定，header以下整個資料area可以捲動

## User vocab detail page

- 單語基本資料layout跟Vocab detail page相同
- 最高一行header固定
  - 左邊顯示返回按鈕，返回進入detail page前的原本列表並保留當時的list／filter context
  - 中間顯示"マイ単語帳の詳細"
  - 右邊顯示homepage icon
- 沿用Vocab detail page的左右排列、過長時轉兩行、單虛線同較粗單實線section分隔規則
- 額外顯示user個人的資料
  - 出題対象設定
    - 視覺沿用User Vocab List Filter的`はい`／`いいえ`兩個selection button，不使用左右滑動switch
    - Detail page的值是單一Boolean設定，兩個button互斥並預先選中目前已保存值；Filter page仍按篩選規則容許兩者獨立選取，兩者只共用視覺樣式
    - 切換後先enable"保存"button
  - 出題優先度
    - 這個field固定使用兩行layout，不使用一般field的左右排列
      - 第一行顯示"出題優先度"
      - 第二行顯示bar，bar佔主要可用闊度
    - 使用橫向bar顯示
    - bar的顯示範圍暫定為1至200，最少數值為1
    - 200只是bar長度的顯示上限，不代表weight的實際最大值
    - weight達到或超過200時，bar保持全滿
    - Weight為10以上時，數字跟隨填色長度，固定顯示在彩色fill內部右側並與fill末端保留12px內距
    - Weight為1至9時，彩色fill太短，數字改放在整條track最右側
    - weight超過200時仍顯示完整實際數值，不顯示成"200+"
    - bar根據weight數值區間改變顏色
      - 200時已進入紅色區間
      - 200以上可以再轉成紫色、接近黑色等更高區間
      - 已確認區間及色值
        - 1至49：淡天藍`#BFE8F7`
        - 50至99：主藍`#8BC9E6`
        - 100至149：琥珀`#E6B85C`
        - 150至199：橙`#D9854B`
        - 200至299：深紅`#AD4B55`
        - 300至499：紫`#73528D`
        - 500以上：近黑紫`#3F344A`
    - 數字位於淡天藍、主藍、琥珀或橙色fill時使用深色`#26343D`；位於深紅、紫或近黑紫fill時使用近白`#F8FCFF`
    - 個位數移到未填色track最右側時使用深色`#26343D`
    - bar左右兩端不額外顯示1或200的尺度標記
  - 正解數
    - 數字使用綠色，沿用連續正解記錄的顏色
  - 不正解數
    - 數字使用紅色，沿用連續不正解記錄的顏色
  - 連續正解／不正解數
    - 不直接顯示正數或負數的raw value
    - 正數顯示為"n問連続正解"，並使用綠色文字
    - 負數取absolute value後顯示為"n問連続不正解"，並使用紅色文字
    - 0顯示為"連続記録なし"，並使用一般深色文字
    - 綠色沿用`#39765B`，紅色沿用`#AD4B55`
  - 最後出題時間
    - 點擊時間顯示位置，可以在相對時間同實際時間之間切換，不需要重新載入page
    - 進入page時預設顯示相對時間
    - 每次點擊會在相對時間同實際時間之間來回切換
    - 時間旁邊不顯示切換icon
    - 從未出題時
      - 預設顯示"いつですかね？"
      - 點擊後切換成"早くクイズしろ"
      - 再次點擊會切換回"いつですかね？"
    - 相對時間的顯示規則
      - 距離現在少於1小時：顯示相差幾多分鐘
      - 距離現在1小時以上但少於1日：只顯示相差幾多小時，不顯示剩餘分鐘
      - 距離現在1日以上：只顯示相差幾多日
    - 實際時間的顯示規則
      - 距離現在少於1日：顯示完整年月日、時同分
      - 距離現在1日以上：顯示年月日，加上時間帶名稱，不顯示實際時分
        - 06:01至12:00："朝"
        - 12:01至18:00："昼"
        - 18:01至翌日02:00："夜"
        - 02:01至06:00："明け方"
  - 前回回答
    - 沒有回答記錄時顯示"まだありませんよ"
    - 沒有回答記錄時不提供文字切換
    - 有回答記錄時只顯示user上次實際輸入的答案文字
    - 不顯示逐字kana圖片或正誤比對結果
- page內分成上下兩個table
  - 上面的table顯示user個人的出題設定、答題資料同前回回答
  - 下面的table顯示單語基本資料
  - 兩個table之間使用較粗單實線加較大上下間距分隔
- User vocab detail page不顯示"変更申請"同"削除申請"button
- viewport底部固定顯示操作button
  - "保存"
  - 前往一般Vocab detail page的button
    - 正式字眼使用"単語の詳細"
  - 兩個button左右並排，width同height一致
  - "保存"使用主要藍色button樣式
    - 未修改"出題対象"時變灰並disable
    - "出題対象"與已保存狀態不同時才enable
    - 保存成功後留在同一個User vocab detail page
      - 將目前的"出題対象"狀態視為已保存
      - "保存"button重新變灰並disable
      - viewport上方顯示一行細小的保存成功提示
      - 成功提示不阻擋user操作，並在大約3秒後自動消失
    - 修改"出題対象"但未保存時，如果user按返回、homepage icon或"単語の詳細"
      - 顯示置中確認modal，提醒有未保存的修改
      - modal提供"破棄して移動"同"キャンセル"button
      - 重新整理、關閉browser tab或直接離開網站時，不需要browser原生的未保存警告
  - "単語の詳細"使用較低調的次要button樣式，底色沿用input淡霧藍灰`#EAF2F6`、文字使用`#26343D`
  - `保存`disabled時使用`#D5DFE4`底色及`#687B85`文字；修改後enable並改用主要藍色`#8BC9E6`
  - 操作button不會跟資料內容捲動
- header同viewport底部操作button固定，只有中間兩個資料table可以捲動

## Vocab create request page

- 整體page骨架沿用Login／Registration page的固定header、中間可捲動form area同field frame視覺
- 最高一行header固定
  - 左邊顯示返回按鈕
  - 中間顯示"単語の追加"
  - 右邊顯示homepage icon
- 中間form area可以捲動
- Form field沿用全站responsive label／control規則，但不照搬Login／Registration固定上下兩行的排列
  - 一般情況左邊顯示field name，右邊顯示input area
  - input太長或viewport可用闊度不足時，自動轉成上下兩行
    - 第一行顯示field name
    - 第二行顯示input area
  - 可選欄位的field name旁邊顯示細小的`任意`標記
    - `意味`
    - `JLPTレベル`
    - `カテゴリー`
    - `理由`
    - `対応する日本語表現`（顯示時）
  - 必填欄位不額外顯示`必須`標記
- form field按以下順序排列
  1. `種類`
  2. `単語`
  3. `読み方（かな）`
  4. `JLPTレベル`
  5. `カテゴリー`
  6. `意味`
  7. `理由`
  8. `対応する日本語表現`（選中`カタカナ`時顯示，固定在form最後）
- `理由`使用多行textarea
  - 初始高度約三行
  - 內容超過可見高度時在textarea內捲動，不繼續自動增加欄位高度
- `意味`使用多行textarea，避免長內容只能在單行input內左右捲動
  - 初始高度約三行
  - 內容超過可見高度時在textarea內捲動，不繼續自動增加欄位高度
- `種類`、`JLPTレベル`同`カテゴリー`等selection field全部在field name下面加入單虛線，再留足間距顯示button，避免button貼住或蓋住field name
- `カテゴリー`欄位沿用Vocab list filter page的多選button設計，不使用傳統checkbox或Detail page的純展示tag
  - 點擊整個button切換選取／未選取狀態
  - 預設全部未選取
  - 預設三個button一行，viewport闊度不足時自動改成兩個一行；如果兩個一行仍然太窄，再改成一個一行
  - 每個button的width同height一致，文字太長時可以在空格或"・"位置換行
  - 最多可以選擇三個Category
  - 不顯示`2 / 3`等已選數量提示
  - 選滿三個後，其他未選button變灰並disable
  - 取消其中一個已選Category後，其他button立即恢復可選
- `種類`欄位使用與Filter page一致的selection button，不使用下拉選單
  - 顯示`一般語彙`同`カタカナ`兩個button
  - 只可以選擇一個種類
  - 進入page時兩個button都保持未選，不預設選擇`一般語彙`
  - 已選button使用active狀態顏色；另一個未選button變灰，但仍然可以點擊
  - 點擊另一個button後，新button變成已選狀態，原本已選button變灰
- `JLPTレベル`欄位使用與`種類`相同的單選button設計，不使用下拉選單
  - 顯示`未設定`、`N1`、`N2`、`N3`、`N4`、`N5`
  - 進入page時全部保持未選
  - 已選button使用active狀態顏色；其他button變灰但仍然可以點擊
  - 點擊另一個button後，新button變成已選狀態，原本已選button變灰
- `対応する日本語表現`是`カタカナ`專用的條件式欄位
  - 選中`カタカナ`時顯示
  - 選中`一般語彙`或尚未選擇種類時隱藏
  - 已輸入內容後切換到`一般語彙`時，保留目前page內的輸入值，但隱藏並停用該欄位，不隨`一般語彙`申請提交
  - 在提交前切換回`カタカナ`時，重新顯示之前保留的輸入值
- viewport底部固定顯示兩個提交button，button不會跟form內容捲動
  - 兩個button左右並排，width同height一致
  - 左邊button使用兩行文字：第一行`申請`，第二行`ホームへ`
    - 第二行字體比第一行細一級，兩行都在button內置中
    - 成功建立申請後返回Homepage
  - 右邊button使用兩行文字：第一行`続けて`，第二行`次の単語`
    - 第二行字體比第一行細一級，兩行都在button內置中
    - 先成功建立目前申請，再留在Vocab create request page，清空整張form並準備輸入下一個create request
  - 兩種成功結果都使用全站統一的成功toast提示
- form有任何輸入或選擇變更但尚未成功提交時，按header返回按鈕或homepage icon會顯示置中確認modal
  - modal沿用User vocab detail page的`破棄して移動`同`キャンセル`button
  - `破棄して移動`會放棄目前form內容並前往原本選擇的目的地
  - `キャンセル`會關閉modal並保留目前form內容
  - 重新整理page、關閉browser tab或直接離開網站時，不使用browser原生的未保存資料警告

## Vocab update request page

- 整體沿用Vocab create request page的固定header、responsive field排列、中間form捲動同視覺樣式
- header左邊顯示返回按鈕，中間顯示「変更申請」，右邊顯示homepage icon
- form載入時預先填入目標Vocab的現有資料
- `種類`不提供修改，只以「種類：一般語彙」或「種類：カタカナ」格式顯示目前值；不使用selection button
- `単語`、`読み方（かな）`、`意味`同`JLPTレベル`為必填欄位，不顯示`任意`標記
- `カテゴリー`、`理由`同`対応する日本語表現`為可選欄位，field name旁邊顯示細小的`任意`標記
- viewport底部只固定顯示一個「変更申請」button，button不會跟form內容捲動
- 成功建立變更申請後返回原本的Vocab detail page，並顯示全站統一的成功toast
- form資料有任何修改但尚未成功提交時，沿用Vocab create request page的未保存確認規則
  - 按header返回按鈕或homepage icon時顯示`破棄して移動`／`キャンセル`確認modal
  - 重新整理page、關閉browser tab或直接離開網站時，不使用browser原生的未保存資料警告

## Vocab delete request page

- 最高一行header固定
  - 左邊顯示返回按鈕
  - 中間顯示「削除申請」
  - 右邊顯示homepage icon
- 中間內容area先顯示準備申請刪除的單語基本資料，再顯示`理由`textarea
  - 單語基本資料顯示`単語`、`意味`、`読み方（かな）`、`JLPTレベル`、`種類`同`カテゴリー`
  - 不顯示MCSense、KatakanaDetail或其他type專用額外資料
- `理由`field name旁邊顯示細小的`任意`標記
  - 使用初始約三行高的textarea
  - 內容超過可見高度時在textarea內捲動，不繼續自動增加欄位高度
- 中間內容area可以捲動
- viewport底部固定顯示紅色「削除申請」button，button不會跟中間內容捲動
- 按「削除申請」後先顯示置中確認modal，不立即提交
  - 顯示「この単語の削除を申請しますか？」
  - modal提供「申請する」同「キャンセル」button
  - 「申請する」會正式提交delete request
  - 「キャンセル」會關閉modal，返回原頁並保留目前的理由內容
- 成功建立刪除申請後返回原本的Vocab detail page，並顯示全站統一的成功toast
- `理由`有輸入但尚未成功提交時，沿用其他Vocab request page的未保存確認規則
  - 按header返回按鈕或homepage icon時顯示`破棄して移動`／`キャンセル`確認modal
  - 重新整理page、關閉browser tab或直接離開網站時，不使用browser原生的未保存資料警告

## Event detail page

- 最高一行header固定
  - 左邊顯示返回按鈕，返回Event list page並保留原本的filter／page context
  - 中間顯示「お知らせ」
  - 右邊顯示homepage icon
- 只有header下面的event內容area可以捲動
- event內容由上至下按以下順序顯示
  1. 完整event type，使用badge樣式，不使用Event list的短版名稱
  2. 完整title
  3. message
  4. event建立時間`create_at`
- 建立時間固定顯示完整日本格式：`YYYY年MM月DD日 HH:mm`
  - 使用24小時制
  - 不提供相對時間切換
- title使用較大粗體，作為event內容的主要標題
  - title固定使用`Zen Maru Gothic Bold`，不使用裝飾用的`Hachi Maru Pop`
- event type badge提高文字字級、badge高度同左右padding，確保完整type清晰可讀
- message使用一般字體並保留原本換行；長內容按可用闊度自然換行
- 建立時間使用較細、較淡的文字
- 打開Event detail page不會自動將通知設為已讀，單純查看內容不改變`is_read`
- Event detail page提供`既読にする`button，由user手動將目前通知設為已讀
  - button固定在viewport底部，不會跟event內容捲動
  - header同底部button固定，只有中間event內容area獨立捲動
  - 通知已讀時仍保留底部操作列；button文字改為`既読`，顯示灰色並disable
  - 成功設為已讀後顯示全站統一的短暫成功toast：`既読にしました`
  - 這是database狀態修改，使用包含CSRF protection的HTML POST form，不使用GET link
  - POST以URL中的UserEvent `pk`識別目標，backend必須再限制為目前登入user擁有的UserEvent
  - 不需要為沒有輸入欄位的固定action強制建立獨立Django `forms.Form` class
  - 成功後redirect回同一Event detail page；重複提交保持安全，不因通知已讀而報錯

## Admin event create page (future)

- 這是將來加入的admin-only custom site page，不是Django `/admin/` page
- 用於由admin手動建立並發佈system announcement，例如系統更新內容、新功能通知或其他需要通知user的事項
- 雖然event create backend flow尚未建立，但這個page納入第一次整體UI實作的準備範圍；共用layout、form元件同互動pattern應預留給這個page使用
- 雖然只有admin可以進入，但這是site內的一般page，不是Django `/admin/`；所有user-facing UI文字使用日文
- 整體UI結構大致沿用Feedback create page
  - 最高一行header固定
  - 中間form area可以捲動
  - viewport底部固定提交button
  - 成功後使用全站統一的短暫success toast
  - 有未提交內容時，頁面內返回／homepage導航使用`破棄して移動`／`キャンセル`確認modal
  - 重新整理page、關閉browser tab或直接離開網站時，不使用browser原生的未保存資料警告
- header中間顯示`お知らせの作成`，右邊顯示homepage icon；左邊返回目的地要等admin event管理入口確定後再定
- Form欄位順序固定為`種類`→`タイトル`→`内容`，三個欄位全部必填
- `種類`使用dropdown select
  - 預設顯示`選択してください`，不預先選擇種類
  - Control高度、近白frame結構同右側vector下箭嘴沿用Feedback create page
  - 實際種類選項由Event model／產品規則決定，不在UI style guide定義
- `タイトル`使用單行input，沿用全站單行input frame與文字對齊規則
- `内容`使用初始約八行高的textarea，不顯示`任意`標記
  - 內容超過可見高度時在textarea內部捲動，不繼續自動增加欄位高度
  - UI規格將`内容`視為必填；正式實作時由這個page的Django form執行required validation，不應只依賴HTML前端限制
  - 現有`Event.message`可以保留`blank=True`，因為這個必填規則只屬於admin手動發佈form；其他system flow仍可按各自規則建立空白message
- 第一版通知對象固定為全體user，不提供個別user、多選user或群組target control，因此form內不顯示收件人選擇欄位
- 個別user通知繼續由單語申請、Feedback等相應system flow自動建立，不經Admin event create page手動發佈
- viewport底部固定顯示`公開`button
- 按下`公開`後先顯示置中確認modal，不會立即發佈
  - 訊息：`全ユーザーに公開します。よろしいですか？`
  - 主要button：`公開する`
  - 次要button：`キャンセル`
  - `公開する`成功後返回Homepage並顯示全站統一的短暫success toast
- Publish／expire時間、importance同active status暫不加入第一版form；如日後需要，再另行定義產品規則同UI

## Feedback create page

- 最高一行header固定
  - 左邊顯示返回按鈕
  - 中間顯示「フィードバック」
  - 右邊顯示homepage icon
- 中間form area可以捲動
- `種類`欄位使用dropdown select，不使用Filter page風格的selection button
  - 預設顯示`選択してください`，不預先選擇任何種類
  - 使用縮短後的單行control高度；右側顯示獨立、清楚可見的vector下箭嘴，唔將`▾`混入文字
- `内容`使用多行textarea
  - 初始高度約六行
  - 內容超過可見高度時在textarea內捲動，不繼續自動增加欄位高度
- viewport底部固定顯示「送信」button，button不會跟form內容捲動
- 成功送出後返回Homepage，並顯示全站統一的短暫成功toast
- form有任何輸入或選擇但尚未成功送出時，按header返回按鈕或homepage icon會顯示置中確認modal
  - modal沿用Vocab request page的「破棄して移動」同「キャンセル」button
  - 「破棄して移動」會放棄目前form內容並前往原本選擇的目的地
  - 「キャンセル」會關閉modal並保留目前form內容
  - 重新整理page、關閉browser tab或直接離開網站時，不使用browser原生的未保存資料警告

## Feedback admin list page

- 最高一行header固定
  - 左邊留空，不顯示返回按鈕
  - 中間顯示`フィードバック一覧`
  - 右邊顯示homepage icon
- 每筆feedback顯示成上下兩行的list item
  - 上行顯示user同種類
    - user name同種類各自使用一個獨立細frame包住，不合併成同一個frame
    - status icon保持在第一行最左；user name frame使用中間剩餘空間，種類frame放在右邊
    - user name過長時仍保持單行並以`…`截斷
    - 相關preview圖已更新
  - 下行顯示內容預覽，只顯示一行，超出可用闊度的部分以`…`截斷
  - 整個list item全行均可點擊，進入對應Feedback detail page
  - 不顯示獨立的`詳細を見る`button
- 不直接顯示status文字；第一行由左至右顯示status icon、user同種類
  - pending：顯示實心圓vector icon，user同種類使用紅色粗字
  - replied：顯示剔號vector icon，user同種類使用綠色文字
  - closed：顯示橫線vector icon，user同種類使用黑色文字
  - 狀態icon使用真正SVG／CSS vector，不依賴可能缺字的font glyph
  - status icon跟隨對應狀態文字顏色
  - 顏色沿用已確認palette：pending紅色`#AD4B55`、replied綠色`#39765B`、closed一般深色`#26343D`
- 第一行排列時，status icon固定在最左，種類完整顯示在右邊，user使用中間剩餘空間
  - user過長時保持單行並以`…`截斷；Feedback detail page顯示完整user
- 每頁顯示5筆feedback
- header下面固定顯示status filter dropdown
  - 選項為`すべて`、`未対応`（pending）、`返信済み`（replied）、`終了`（closed）
  - 進入page時預設選擇`未対応`
  - Dropdown右側顯示獨立vector下箭嘴
  - 預設`未対応`畫面只顯示pending資料；另設選中`すべて`的preview展示pending、replied、closed三種狀態
  - 不使用Event list的橫排filter button
  - 切換選項後更新中間feedback list，並返回篩選結果第1頁
- pagination完全沿用Event list page
  - 固定在viewport最底部
  - 由左至右顯示first、previous、按全站breakpoint調整數量的page number、next、last
  - 第一頁disable first同previous，最後一頁disable next同last，但不隱藏
  - 只有一頁時隱藏四個方向button，只保留page number `1`
- header同pagination固定，只有中間feedback list area可以捲動
- 目前filter沒有資料時，中間顯示`該当するフィードバックはありません。`
  - 空狀態下隱藏pagination

## Feedback admin detail page

- 最高一行header固定
  - 左邊顯示返回按鈕，返回Feedback admin list page並保留原本的status filter／page context
  - 中間顯示`フィードバック詳細`
  - 右邊顯示homepage icon

- header下面的detail內容area可以捲動
- 由上至下按以下順序顯示
  1. status
    - 顯示vector status icon同日文文字：`未対応`、`返信済み`、`終了`
    - vector icon形狀、文字顏色同pending粗體規則沿用Feedback admin list page；不依賴font glyph
  2. 完整user
  3. feedback種類
  4. 送信日時
  5. feedback內容全文
  6. 已回覆時顯示目前保存的reply admin同reply時間
- Detail內容分成以下區塊
  - 上方基本資料table顯示status、user、feedback種類同送信日時
  - 中間`内容`使用獨立的全闊度區塊，保留原本換行並按可用闊度自然換行
  - 已回覆時，內容下面再顯示reply admin同reply時間資料table
- label-value資料一般情況左邊顯示field name，右邊顯示data
  - data太長或viewport可用闊度不足時自動轉成兩行
  - field name在第一行靠左，data在第二行靠右
- 同一個table內各field之間使用單虛線分隔
- 基本資料、內容同回覆資料區塊之間使用較粗單實線加較大上下間距分隔
- viewport底部固定顯示操作button，不會跟detail內容捲動
  - status為`未対応`或`返信済み`時顯示可點擊的`返信`button，進入Feedback admin reply page
  - status為`終了`時顯示灰色disabled的`終了`button
- header同底部操作列固定，只有中間detail內容area可以捲動
- 目前Feedback同回覆時建立的Event沒有關聯，因此暫時不能在detail page可靠顯示reply內容；相關data model改善記錄在Future Ideas

## Feedback admin reply page

- 最高一行header固定
  - 左邊顯示返回按鈕，返回原本的Feedback admin detail page
  - 中間顯示`フィードバックに返信`
  - 右邊顯示homepage icon
- 中間內容area可以捲動
  - 先顯示原本Feedback內容
    - 顯示完整user、feedback種類、送信日時同feedback內容全文
    - 不重複顯示status
  - 再顯示reply textarea同結束狀態switch
    - `返信内容`textarea初始高度約六行
    - 內容超過可見高度時在textarea內捲動，不繼續自動增加欄位高度
    - switch label正式使用`返信後に終了`，避免同離開page混淆
    - switch預設關閉
    - 開啟後，成功送出今次reply時將Feedback status設為closed
- viewport底部固定顯示`返信`button，button不會跟中間內容捲動
- 成功送出reply後返回原本的Feedback admin detail page，並顯示全站統一的短暫成功toast
  - 沒有開啟`返信後に終了`時，Detail顯示`✓ 返信済み`並保留可點擊的`返信`button
  - 開啟`返信後に終了`時，Detail顯示`— 終了`同灰色disabled的`終了`button
- reply form有輸入或switch狀態有改動但尚未成功送出時，按header返回按鈕或homepage icon會顯示置中確認modal
  - modal使用`破棄して移動`同`キャンセル`button
  - 重新整理page、關閉browser tab或直接離開網站時，不使用browser原生的未保存資料警告

## Quiz setting page

- 最高一行header固定
  - 左邊顯示返回按鈕
  - 中間顯示`クイズ設定`
  - 右邊顯示homepage icon
- 中間設定area可以捲動
- `問題数`使用三個單選button，不使用dropdown
  - 只顯示`10`、`20`、`30`
  - 三個button都未選時代表`無制限`，backend值使用現有的`-1`
  - 三個button的width同height一致
  - 已選button使用active狀態顏色；其他button變灰但仍然可以點擊
  - 點擊另一個button後，新button變成已選狀態，原本已選button變灰
  - 再次點擊目前已選button會取消選擇，回復三個button都未選的無制限狀態
  - 這個可取消單選行為只適用於問題數
- `種類`、`JLPTレベル`同`カテゴリー`全部使用與Vocab Filter一致的multi-select button
  - 進入page時全部預設未選
  - 每個button可以獨立切換選取／未選狀態
  - 沒有選擇任何項目時代表不限，包含該欄位的全部選項
  - 已選button使用active狀態顏色；未選button變灰但仍然可以點擊
  - `種類`目前顯示`一般語彙`同`カタカナ`
  - `JLPTレベル`顯示`未設定`、`N1`、`N2`、`N3`、`N4`、`N5`
  - `カテゴリー`沿用Vocab Filter的3個一行、太窄時2個一行、再窄時1個一行排列
  - Quiz Setting的Category沒有三個選項上限，可以任意多選
- 將現有`前回の設定を使用` checkbox改成`前回の設定を読み込む`button
  - button放在中間設定area最上方、`問題数`之前，並佔一整行
  - 設定欄位由上至下排列為`問題数`、`種類`、`JLPTレベル`、`カテゴリー`
  - 點擊後將上一次保存的問題數、種類、JLPTレベル同Category填入目前各個selection button
  - 載入本身不會提交form或開始Quiz
  - 載入後user仍然可以修改任何設定，再按底部`開始`
  - 不再使用backend提交時忽略目前欄位並直接覆蓋成上次設定的舊行為
  - 有上一次設定時，button使用正常可用樣式
  - 沒有上一次設定時，button顯示灰色unavailable樣式，但不使用真正的HTML `disabled` attribute，保留click事件
  - user點擊灰色button時，在viewport上方顯示短暫提示`前回のクイズ設定がありません`
- viewport底部固定顯示`開始`button，button不會跟設定內容捲動
- 設定有效並成功開始後直接進入Quiz play page，不顯示success toast
- 修改Quiz Setting後未按`開始`就返回或前往Homepage時，直接離開，不顯示未保存確認modal

## Quiz play page

- 目前初稿preview
  - 非MC Question state：[`quiz-question-state.png`](./preview/png/quiz-question-state.png)（[`SVG`](./preview/svg/quiz-question-state.svg)）
  - 50音keyboard input mode：[`quiz-input-mode.png`](./preview/png/quiz-input-mode.png)（[`SVG`](./preview/svg/quiz-input-mode.svg)）
  - Answer result state：[`quiz-answer-result.png`](./preview/png/quiz-answer-result.png)（[`SVG`](./preview/svg/quiz-answer-result.svg)）
  - Answer result判定modal：[`quiz-answer-result-judgement-modal.png`](./preview/png/quiz-answer-result-judgement-modal.png)（[`SVG`](./preview/svg/quiz-answer-result-judgement-modal.svg)）
  - MC Question未選：[`quiz-mc-question-unselected.png`](./preview/png/quiz-mc-question-unselected.png)（[`SVG`](./preview/svg/quiz-mc-question-unselected.svg)）
  - MC Question已選：[`quiz-mc-question-selected.png`](./preview/png/quiz-mc-question-selected.png)（[`SVG`](./preview/svg/quiz-mc-question-selected.svg)）
  - MC Question使用Hint：[`quiz-mc-question-hint.png`](./preview/png/quiz-mc-question-hint.png)（[`SVG`](./preview/svg/quiz-mc-question-hint.svg)）
  - MC Answer Result：[`quiz-mc-answer-result.png`](./preview/png/quiz-mc-answer-result.png)（[`SVG`](./preview/svg/quiz-mc-answer-result.svg)）
  - Summary正常完成：[`quiz-summary.png`](./preview/png/quiz-summary.png)（[`SVG`](./preview/svg/quiz-summary.svg)）
  - Summary題庫用盡：[`quiz-summary-no-question-pool.png`](./preview/png/quiz-summary-no-question-pool.png)（[`SVG`](./preview/svg/quiz-summary-no-question-pool.svg)）
  - No-question state：[`quiz-no-question-state.png`](./preview/png/quiz-no-question-state.png)（[`SVG`](./preview/svg/quiz-no-question-state.svg)）
  - No-pool confirmation：[`quiz-no-pool-confirmation.png`](./preview/png/quiz-no-pool-confirmation.png)（[`SVG`](./preview/svg/quiz-no-pool-confirmation.svg)）
  - Preview中的panel與keyboard button配色及`クイズ`page title已確認保留；Backspace vector icon的具體外形仍待正式asset確認
- 共通page骨架沿用其他site page
  - Header固定在viewport頂部；Question、Input及Answer Result state的中央page title固定為`クイズ`
  - Header右邊顯示Homepage icon
  - Question state的viewport底部固定顯示`回答`；Answer Result按進度顯示`次へ`或`結果へ`
  - 中間Quiz內容區獨立捲動
- Quiz進度以實際提交並完成判定的回答數計算，等於`正解數＋不正解數`
  - 固定`10／20／30`題代表需要完成的回答數；達到指定回答數後由server結束Quiz並顯示Summary
  - `スキップ`不當作已回答，不增加回答進度，亦不消耗固定題數名額；Skip後載入的題目沿用同一題號
  - `スキップ`次數仍獨立累計；如果該題使用Hint後再Skip，已使用的Hint次數仍計入Summary
  - 無制限模式不設回答數上限，直到題庫耗盡或其他既有結束條件出現
  - `次へ`、Summary及未完成Quiz的server endpoint都必須自行驗證目前回答進度，不依賴前端按鈕文字或顯示狀態作為唯一限制
- Quiz內容區最上方靠左顯示細frame，標示目前是第幾問
- 以下大型word／meaning題目frame同圖片字輸入規格只適用於非Multiple Choice題目；Multiple Choice Question state使用下方獨立規格
- 非Multiple Choice題目的題目資料放在同一個大型frame內
  - 上半部顯示word，使用大字並水平置中
  - Word區預留兩行高度；只有一行時在預留區內垂直置中
  - Word字級按字數調節，太長時換行；包含空格的長英文優先在space位置斷行，避免任意切開單字
  - Word同meaning之間使用虛線分隔
  - 下半部顯示meaning，文字水平置中並使用固定字級；不在預留區域內垂直置中
  - Meaning第一行由虛線下方的全站標準間距開始，距離沿用其他page虛線與下方內容的間距
  - Meaning區只保留實際文字行數所需高度及正常上下padding，明顯比兩行大字的Word區矮；一行內容時，最後一行至frame底部不得保留額外空白
  - 內容放得下一行時維持一行；太長時自動換到第二行；超過兩行時增加題目frame高度並完整顯示，不使用省略號截斷
- Summary、No-question、No-pool confirmation、Multiple Choice Question同Multiple Choice Answer Result的layout及主要互動規格已記錄；MC不列入`v1.0.0`發布範圍

### Question state

- 非Multiple Choice題目的答案輸入區使用一個獨立frame包住整個答案顯示範圍；沿用一般近白card、圓角同陰影，不額外加border
- 未有任何input時，在frame內使用一般font及灰色文字顯示提示`ここを押して回答を入力`
  - 目前正式採用`ここを押して回答を入力`，因為手機同desktop都適用而且長度較短
  - 保留較親切語氣的候選記錄：`ここを押して、答えを入力してね`、`ここから答えを入力してね`
- 整個答案frame全行都可以點擊，不限於提示文字位置；點擊後進入答案輸入mode
- 正式答案顯示不使用一般webfont；每個輸入字元以現有Quiz kana圖片字逐字拼合顯示
- 圖片字沿用現有HGS創英角ポップ体風格PNG，使用範圍只限Quiz輸入答案及之後的答案比較
- Quiz答案圖片字配色採用A方案
  - `NORMAL`輸入中同`MATCH`一致均使用深藍黑`#26343D`；兩者不靠字色區分
  - `WRONG`、`MISSING`同`EXTRA`統一使用柔和深紅`#AD4B55`；不為`EXTRA`另設橙色
  - `MISSING`的底線同`EXTRA`的交叉線必須以overlay方式覆蓋在對應kana圖片上，不可作為另一個字元並排顯示
  - 濁点、半濁点及小書き等局部差異須保留字身深藍黑，只將出錯的局部標記轉成柔和深紅；例如正解`ぼ`、回答`ぽ`使用`HANDAKUTEN`結果，顯示深色字身及紅色濁點
  - 生成指定顏色版本時可以現有PNG的alpha channel保留透明邊緣；但`*_mark_red.png`含有字身與局部紅色標記，不可整張單色化，須分開處理字身與差異標記
- 答案圖片字設有最大顯示尺寸同最小顯示尺寸
  - 答案較短時使用最大尺寸
  - 隨輸入字數增加，答案內全部圖片字同步使用同一尺寸逐步縮細；不會逐字獨立縮放或出現大小混合
  - 縮到最小尺寸後不再繼續縮小；實際最大／最小尺寸同縮放門檻之後再定
  - 到達最小尺寸後仍然超出一行時，自動換到第二行，答案frame隨內容增加高度
  - 換行後全部圖片字繼續使用同一尺寸；答案區不使用橫向捲動
- 答案frame下面顯示左右並排的兩個輔助button
  - 左邊button文字固定為`ヒント`，右邊button文字固定為`スキップ`
  - 兩個button的width同height一致
  - 兩者都屬於同級次要操作，Question page使用相同的淡藍灰`#EAF2F6`實色底同深藍黑`#26343D`文字；不以Summary統計label的不同功能色區分兩個button，亦不使用與主要提交操作相同的`#8BC9E6`
  - 這兩個button屬於可捲動Quiz內容區，不取代viewport底部固定的主要`回答`button
  - 點擊`スキップ`成功後不顯示Answer Result，直接載入下一題；如果已無下一題，則直接進入Summary
  - Skip流程不顯示`正解`／`不正解`、正確答案或`未回答`結果卡
- 未輸入任何答案時，viewport底部固定的`回答`button顯示灰色unavailable樣式
  - 不使用真正的HTML `disabled` attribute，保留click事件
  - user點擊後不提交空白答案；在viewport頂部顯示短暫提示，要求先輸入答案
  - 頂部短暫提示文字固定為`何も答えないと進めないよ`
- 輸入至少一個字元後，`回答`button回復正常可提交樣式
- 點擊答案frame進入輸入mode後，使用參考UI-sample-02／03關係的bottom-sheet輸入層
  - 原本Quiz Question page保留在背景，整頁由半透明白色backdrop覆蓋並停止操作
    - 白色backdrop是目前暫定的可讀性方案；深色backdrop會令前景答案圖片字同背景原有文字混在一起
    - 在找到能清楚分隔前景答案與背景文字的更好方案之前，Input Mode維持白色；一般modal仍沿用深色backdrop
  - 原本Question page的答案frame跟其他page內容一樣留在backdrop下面並被淡化，不作輸入中的主要顯示區
  - 在半透明backdrop上方、bottom sheet之外、keyboard panel上方另外新增一個前景答案顯示區
  - 前景答案顯示區在輸入期間即時顯示已輸入的答案圖片字；它不是透過backdrop觀看原本答案frame，亦不放在bottom sheet內
  - 前景答案顯示區不使用近白card或其他frame；答案圖片字直接顯示在半透明backdrop上方
  - 前景答案顯示區佔用keyboard panel上方剩餘的backdrop區域，答案圖片字在該區域內水平及垂直置中
  - Bottom sheet只承載50音keyboard及相關操作鍵
  - 50音keyboard改用10行×6欄的視覺grid，不再沿用現有11行×5欄加獨立Backspace的排位；第6欄由跨行直向功能button組成
  - Hiragana鍵盤排列如下；Katakana使用相同位置規則換成對應片假名

    ```text
    あ  い  う  え  お  ┐
    か  き  く  け  こ  ┘ "
    さ  し  す  せ  そ  ┐
    た  ち  つ  て  と  ┘ 。
    な  に  ぬ  ね  の  ┐
    は  ひ  ふ  へ  ほ  ┘ 小
    ま  み  む  め  も  ┐
    や      ゆ      よ  │ Backspace
    ら  り  る  れ  ろ  │
    わ  を  ん  [ 完了 ] ┘
    ```

  - 第6欄第1–2行由一個標示`"`的直向button跨兩行；第3–4行由一個`。`button跨兩行；第5–6行由一個`小`button跨兩行
  - Backspace放在第6欄最後4行，形成一個跨4行的直向大型button，位於`も`、`よ`、`ろ`同最下方`完了`button的右邊
  - 現有`隠す`button改名為`完了`，放在最底第4–5欄並橫跨兩欄
  - `完了`只會收起keyboard並保留已輸入答案，不會提交答案；正式提交仍使用viewport底部固定的`回答`button
  - 一般kana key參考UI-sample-03使用圓形button；所有圓形大小一致
  - 跨行的`"`、`。`、`小`同Backspace使用同一套視覺語言的直向膠囊形；`完了`使用橫向膠囊形
  - Keyboard配色正式固定如下
    - Bottom sheet panel底色保留目前淡藍`#BFE8F7`，不使用白色
      - 雖然同selection button的active色相同，但keyboard panel不是可選項目，視覺上不會被理解為selected control；這是keyboard專用的明確例外
    - 一般kana圓形button：完全不透明近白`#F8FCFF`
    - `"`、`。`、`小`同Backspace功能button：淡藍灰`#EAF2F6`
    - `完了`button：主要button藍`#8BC9E6`
    - 所有button文字使用深藍黑`#26343D`
  - 因50音keyboard需要較多空間，panel高度可以比UI-sample-03更高，但由10行keyboard實際內容高度、正常上下padding同mobile safe area計算，不使用固定高度製造多餘空白
  - Keyboard grid在panel內完整顯示時，第一行button頂部至panel頂邊的留白固定等於最左／最右button至panel左右邊的留白；底部在相同視覺留白之外另加mobile safe area
  - 6欄keyboard需要配合viewport寬度responsive縮放
    - 寬度足夠時使用preview目前約62px的圓形kana key、約20px欄距同24px左右／頂部padding
    - viewport收窄時，key直徑、欄距同panel padding一同逐步縮小；所有同級kana key保持相同尺寸
    - 320px最低支援寬度時，key直徑不得小於44px；可使用約6px欄距同13px左右／頂部padding，確保6欄無橫向捲動
    - 跨行功能button使用同一欄寬同步縮放；`完了`繼續橫跨第4–5欄
  - `完了`完整位於第10行，不能被viewport或panel裁切
  - 矮身viewport無法完整顯示10行keyboard時，只讓bottom sheet內的keyboard內容垂直捲動
  - 上方前景答案顯示區、backdrop同bottom sheet邊界保持固定，不跟keyboard內容捲動
  - Panel實際高度與上方答案區最低保留高度仍待preview確認
  - user點擊bottom sheet panel以外的backdrop區域時，收起keyboard panel並返回一般Question state
  - 收起panel只結束輸入mode，不會清除已輸入答案；原本Question page的答案frame顯示目前答案
  - 點擊`完了`或panel外backdrop都可以收起keyboard；兩種操作都保留目前答案
- 答案區進入輸入mode後的frame focus樣式、游標、刪除及圖片字排列細節仍待後續確認

### Multiple Choice Question state

- Version scope：`v1.0.0`尚未提供Multiple Choice題目；以下MC規格與preview保留作後續版本實作參考，不列為`v1.0.0`發布阻塞項目
- 整體page骨架沿用非Multiple Choice Question state：Header固定、內容區最上方顯示「第幾問」、中間內容區獨立捲動、主要提交button固定在viewport底部
- 題目大型frame不顯示`word`／`meaning`，改為上下顯示`question`／`meaning`
  - `question`放在上半部；單行時水平置中，兩行時第一行靠左、第二行靠右，三行時第一行靠左、第二行置中、第三行靠右
  - `meaning`放在下半部並水平置中
  - `question`同`meaning`之間沿用題目frame的虛線分隔
  - `question`內的`_`代表答案位置；畫面保留`_`並轉為紅色
  - 如果`_`後面有`(して)`一類活用提示，`_`與該括號提示視為同一組並一同轉紅色
  - 提示紅的詳細色值之後再定；需要避免與`不正解`錯誤紅完全相同而令題目提示被誤解為錯誤狀態
- 移除非Multiple Choice使用的答案輸入frame，改為四個垂直排列的答案選項button
  - 四個button的width、height及字級一致，整組水平置中
  - Button尺寸接近Homepage主button，不佔滿viewport可用闊度；四個選項使用相同固定寬度，圓角沿用普通button的`17px`
  - 正常情況保持單行；如果意外出現過長選項，四個button一同逐級縮小至相同字級，不會只縮小其中一個
  - 暫不為低機率的過長選項設定換行及增高layout；實作時仍須避免文字溢出button邊界
  - 四個選項保持單一直列，不改成兩欄
  - 選項只顯示答案文字，不加`A／B／C／D`或其他編號，亦不預留編號欄位；文字在button內水平及垂直置中
- `ヒント`同`スキップ`繼續保留在四個選項button下面
  - `ヒント`在左、`スキップ`在右，兩個button左右並排並保持相同width及height
  - 樣式沿用非Multiple Choice的次要操作button
  - MC的`ヒント`每次點擊會從尚未排除的錯誤答案中排除一個；正確答案不會被排除
  - 被排除的選項button保持原本位置、width及height，轉為灰色disabled外觀並禁止再次點擊，原本答案文字改為`----`
  - 三個錯誤答案全部排除後再點擊`ヒント`，選項不再改變，只在viewport頂部顯示短暫提示`まだ答えられないの？`
  - 如果隨機排除的是user目前已選的錯誤答案，立即清除該選項的selected狀態，再將button變成灰色`----`
  - 清除已選錯誤答案後，viewport底部`回答`回復灰色unavailable樣式；user須從剩餘可用選項重新選擇，先可再次提交
  - 三個錯誤答案全部排除後，不會自動選取唯一剩下的正確答案；正確答案保持未選，底部`回答`維持灰色，直至user親自點擊正確答案
  - 錯誤答案全部排除後，`ヒント`仍保留click事件，以便再次點擊時顯示`まだ答えられないの？`
- 四個選項加上`ヒント`／`スキップ`超出可用高度時，只捲動中間Quiz內容區；Header及viewport底部主要操作區保持固定
- 點擊選項只更新選取狀態，不會即時提交答案
  - 同一時間只可選擇一個答案；user可在提交前點擊其他選項改選，原本選項回復未選狀態
  - 選好答案後，按viewport底部固定的`回答`button先正式提交及進入判定
  - 尚未選擇答案時，底部`回答`沿用非Multiple Choice的灰色unavailable樣式但保留click；點擊不提交，並顯示`何も答えないと進めないよ`
  - MC選項不顯示`✓`；Selected使用深藍`#477A99`配近白字`#F8FCFF`，不加border
  - Unselected使用近白`#F8FCFF`配深藍黑字`#26343D`；MC未選button仍可點擊
  - 深藍過往不適合大面積主要button，但MC同時只有一個較小Selected選項，因此用作局部焦點
  - Hint排除後使用較深灰藍`#91AAB7`並顯示`----`，同近白Unselected清楚區分
  - 點擊另一個選項時，主藍Selected狀態轉移至新選項，原本選項回復淺灰未選樣式
- MC Question preview已生成三種主要狀態
  - 未選狀態：四個選項全部使用近白Unselected樣式，底部`回答`為灰色unavailable樣式
  - 已選狀態：示例選擇`スルー`；該選項改用深藍Selected樣式，其餘維持近白Unselected樣式，底部`回答`回復正常可提交樣式
  - Hint狀態：示例排除`チェック`，該選項變成灰藍並顯示`----`

### Non-Multiple Choice Answer result state

- Header同Question state保持一致，固定在viewport頂部，右邊繼續顯示Homepage icon
- Quiz內容區最上方保留「第幾問」一行
  - 左邊繼續顯示目前是第幾問的細frame
  - 同一行中間新增結果狀態frame，不顯示固定的`答え合わせ`
  - 答啱時顯示`正解`，狀態frame使用柔和深綠實色底`#39765B`
  - 答錯時顯示`不正解`，狀態frame使用柔和深紅實色底`#AD4B55`
  - 兩種狀態文字都使用近白`#F8FCFF`及`Zen Maru Gothic Bold`
  - 狀態frame使用圓角並不顯示border
  - 這一行使用三欄視覺結構：左邊「第幾問」、中央結果狀態、右邊管理用判定button位置
  - 中央結果狀態以整個內容區真正中心為準，不受左右內容闊度影響
  - 右邊判定button只向`user.is_superuser`顯示；一般user及非superuser staff保留空位，因此中央狀態位置不變
  - 右邊button文字固定為`判定`
  - `判定`使用淡藍灰實色底`#EAF2F6`同深藍黑文字`#26343D`，屬於低強調管理輔助操作
  - `判定`button高度與同一行的「第幾問」frame一致，不搶過中央`正解`／`不正解`狀態
  - admin點擊`判定`後，在同一頁開啟modal，不進行導頁或改變Quiz結果
  - modal標題固定為`判定詳細`
  - modal顯示目前`quiz_result_partial.html`的答案比較詳細資料，欄名使用日文
  - 每個比較字獨立顯示成`2×2`資料區塊，上行為`正解`／`回答`，下行為`種類`／`詳細種類`
  - 每個cell同時顯示欄名及該比較字的對應值，不將四項資料橫排成同一行
  - 相鄰比較字的資料區塊之間使用虛線分隔；每組最後一行至虛線、虛線至下一組第一行使用相近而緊湊的正常間距，不保留大片空白
  - modal高度按實際內容自動計算：內容較少時縮短並保持viewport中央；內容增加時才向上下擴展
  - modal最大高度為viewport的`80%`；比較資料超出最大高度的可用範圍時只捲動中間table區域
  - 內容未超出可用範圍時不顯示捲軸；只有modal已達`80%`高度上限而中間資料仍放不下時才顯示
  - modal標題固定在頂部不捲動，底部固定顯示`完了`button並且不捲動
  - `完了`只關閉modal，不進行其他操作
  - 點擊modal外的backdrop亦會關閉modal
  - Desktop按`Esc`亦會關閉modal
  - 三種關閉方式都保留目前Quiz Result畫面及所有資料不變
- 保留Question state的題目大型frame及word位置
  - word繼續顯示原本題目文字
  - 原本meaning位置不再顯示meaning，改為顯示該題的正確答案
  - 正確答案使用一般`Zen Maru Gothic`文字，不使用Quiz kana圖片字
  - Quiz kana圖片字繼續只用於使用者輸入答案及逐字答案比較
  - 題目frame內直接以上下兩行顯示`word`及括號包住的`(kana)`；兩行之間不使用虛線，垂直空白約為先前preview的一半
  - `(kana)`區不預留額外高度；題目frame頂部至word與`(kana)`至frame底部使用相同的視覺留白，內容較長需要換行時才按內容增加高度
- 原本答案輸入frame改為兩段式答案比較結果frame
  - 整體結構參考題目frame，但上下空間比例反轉
  - 題目frame的word／下方資料比例約為`2:1`；答案比較frame的原始回答／比較結果比例約為`1:2`
  - 上半部改用全站field name／data資料列格式：左邊顯示`あなたの回答`，右邊顯示使用者原本輸入的完整答案
  - 原始回答使用一般`Zen Maru Gothic`字體render，不使用kana圖片字；彩色逐字比較區才使用kana圖片字
  - 一般長度時field name與data同一行並分別靠左／靠右；資料太長時跟全站規則改成兩行，field name在上方靠左，data在下方靠右
  - 資料列至中間虛線只保留正常間距，不用額外留白；兩行layout出現時才按內容增加上半部及整張回答卡高度
  - `1:2`只作一般長度答案的視覺參考，不以固定高度硬撐比例；上下區域優先按實際內容及正常padding收緊，長答案換行時再增加高度
  - 中間使用虛線分隔
  - 下半部使用較大空間顯示彩色逐字比較結果，表達`MATCH`、`WRONG`、`MISSING`同`EXTRA`
  - 比較區高度由一行比較字、overlay及正常上下padding決定，不為維持比例加入大片空白
  - 彩色比較字連同overlay作為一個整體，在虛線以下至回答frame底部的可用區域內垂直置中
  - 下半部不顯示`答え合わせ`、`比較結果`或其他caption；由上半部`あなたの回答`、中間虛線及彩色錯誤標記表達兩部分的關係
  - 彩色比較結果較短時使用下半部的較大基準圖片字尺寸
  - 隨比較結果字數增加，全部kana圖片字及overlay同步縮小至最低尺寸
  - 到達最低尺寸仍然超出可用闊度時先換成兩行，並增加下半部及整張回答卡高度；不使用橫向捲動或省略號
  - 每個kana連同其`MISSING`底線或`EXTRA`交叉線視為同一個不可拆分單位，縮放及換行時保持疊合
  - 原始回答與比較結果各自排列及置中，不按DP欄位作上下逐格對齊
  - 題目frame的正確答案、原始回答同逐字比較結果分別負責標準答案、實際輸入及錯誤位置，三者都保留
- 可愛狀態圖片放在題目frame與答案比較frame之間，圖片內容尚未決定
  - 使用透明背景圖片，不另外增加card、frame或border
  - 圖片水平置中，設定最大闊度及最大高度，保持原比例完整縮放並且不裁切
  - 可愛圖片未完成前，在同一預留位置使用全站`工事進行中`未完成插圖placeholder，不再重複顯示大字`正解`／`不正解`
  - 頂部結果狀態frame無論可愛圖片是否完成都保留，作為必要文字資訊
- viewport底部固定操作button
  - 尚有下一題時顯示`次へ`
  - 最後一題時顯示`結果へ`

### Multiple Choice Answer result state

- 整體結果骨架沿用Non-Multiple Choice Answer result：頂部保留「第幾問」同中央`正解`／`不正解`狀態frame
  - 頂部同樣使用三欄骨架；MC沒有逐字DP比較資料，因此右邊不顯示admin專用`判定`button，只保留同等寬空位
  - 中央`正解`／`不正解`以整個內容區真正中心為準，不因右欄留空而偏移；MC亦不提供`判定詳細`modal
- 題目大型frame繼續顯示原本完整`question`
  - 將`question`中代表答案位置的整段連續`_`刪除，並在同一位置插入正確答案，顯示完成後的完整句子
  - 例如`失礼なコメントには反応せず____(して)ください。`會以`スルー`取代整段`____`
  - 插入的正確答案與其後`(して)`等活用提示視為同一組，整組使用提示紅；句子其餘部分使用深藍黑
  - Result完整question的多行對齊沿用MC Question state：單行置中；兩行左／右；三行左／中／右；整組文字在題目frame內垂直置中
  - 提示紅實際色值與MC Question state相同，詳細色值之後再定
  - MC Result題目卡不再另外顯示`meaning`
- 題目frame與回答frame之間保留可愛狀態圖片位置；圖片未完成前使用全站`工事進行中`未完成插圖placeholder
- 回答卡沿用上下兩段結構
  - 上半部使用全站field name／data格式：左邊顯示`あなたの回答`，右邊以一般`Zen Maru Gothic`字體顯示user選擇
  - user答錯時，上半部答案data使用錯誤紅；答啱時保持深藍黑
  - 中間使用虛線分隔
  - 下半部不顯示`正解`或其他caption，直接以一般`Zen Maru Gothic`字體render正確答案
  - 下半部正確答案固定使用深藍黑，不隨正誤狀態改色
  - 答啱時上下兩段雖然顯示相同答案，仍然完整保留`あなたの回答`資料列、虛線及下半部正確答案，不合併或隱藏重複內容
  - 答啱與答錯使用完全相同的回答卡高度及結構，避免判定後layout跳動
  - MC正確答案可能包含漢字、英文字母或其他符號，因此不使用Quiz kana圖片字
  - 正確答案文字使用明顯大過上半部`あなたの回答`data的基準字級，視覺層級與Non-Multiple Choice比較答案區一致
  - 正確答案在下半部水平及垂直置中；內容增長時統一縮小字級，仍放不下時換行並按內容增加回答卡高度
  - 下半部按實際答案高度及正常padding收緊，不因使用大字而預留大片空白
- MC Answer Result只會在user提交答案後顯示；點擊`スキップ`會直接載入下一題，無下一題時直接進Summary，不會進入MC Result
- Result畫面不帶入MC Question state的四個選項、Hint排除狀態或`ヒント`／`スキップ`
- viewport底部固定操作button：尚有下一題時顯示`次へ`，最後一題時顯示`結果へ`

### Summary state

- Header固定在viewport頂部；中央標題使用`結果`，右邊顯示Homepage icon
- Header左邊不顯示返回按鈕，避免返回已完成的Quiz state
- Header下方、統計區上方預留較細的Quiz完成可愛圖片位置
  - 使用透明背景圖片，水平置中，設定最大闊度及最大高度，保持原比例完整縮放並且不裁切
  - 圖片未完成前使用全站既有的較細`工事進行中`未完成插圖placeholder
  - 預留高度明顯小於Answer Result狀態圖片，避免將五張統計frame推得太低或留下過多空白
- 提早結束原因提示只在`ended_early=True`時顯示，位置在可愛圖片下方、統計區上方
  - 使用full-width近白提示frame；文字置中，過長時自動換行並按內容增加frame高度
  - `question_unavailable`顯示`現在の問題が出題対象から外れたため、クイズを終了しました。`
  - `no_question_pool`顯示`出題できる問題がなくなったため、クイズを終了しました。`
  - 正常完成時不顯示提示frame，亦不保留其空位
- Summary保留五項統計：回答した問題、正解數、不正解數、Skip數、Hint使用次數
  - `回答した問題`只計實際提交並完成判定的回答，等於正解數＋不正解數；Skip不計入此數值
  - `スキップ`獨立顯示被略過的題目次數，不會加進`回答した問題`
  - `ヒント`顯示整次Quiz實際使用次數；在最後Skip的題目上已使用的Hint亦照常計入
- 統計區使用五個獨立frame
  - 第一行為總題數，使用一個full-width較大frame
  - 第二行為正解／不正解，兩個同尺寸frame左右並排
  - 第三行為Skip／Hint，兩個同尺寸frame左右並排
  - 每個frame上方顯示label，下方顯示較大數字
  - 統計label與同一張frame的data使用相同字級：一般viewport的總題數label／data約44px，四張雙欄frame的label／data約38px
  - Summary統計label屬於卡片主標題，不使用一般form field較細label的層級
  - 窄viewport仍保持兩欄，按以下規則縮小欄距、內距同整組字級，避免文字溢出或增加成過多直列row
    - 320px至359px：總題數label／data約34至36px；四張雙欄frame的label／data約30至32px
    - 同一張frame內label同data必須同步使用相同字級
    - 360px以上逐步回復一般viewport基準字級；所有同級雙欄frame保持一致
- 統計frame全部使用同一近白底；每張frame內label在上、data在下並各自水平置中
  - Label使用對應功能色：`回答した問題`深藍黑`#26343D`、`正解`柔和深綠`#39765B`、`不正解`柔和深紅`#AD4B55`、`スキップ`功能深藍`#477A99`、`ヒント`琥珀橙`#E6B85C`
  - `スキップ`同`ヒント`只在Summary統計label使用不同功能色；Question page內兩個同級輔助button保持相同配色
  - 所有data統一使用深藍黑`#26343D`，不跟label改色，方便直接比較五個數值
  - 以上label配色已按Summary preview確認
- 五張統計frame的正式label與數值格式
  - `回答した問題`：數值使用`10問`格式
  - `正解`：數值使用`7問`格式
  - `不正解`：數值使用`2問`格式
  - `スキップ`：數值使用`1問`格式
  - `ヒント`：數值使用`3回`格式
  - 單位跟數字顯示在同一行，label不重複加入`数`、`問題数`或`使用回数`
- viewport底部固定顯示主要button`クイズ設定へ`，返回Quiz Setting；返回Homepage使用Header右邊Homepage icon
### No-question state

- Header固定在viewport頂部；中央標題維持`クイズ`，右邊顯示Homepage icon
- 中央內容區顯示狀態圖片及以下兩行日文說明，不顯示「第幾問」、題目卡、答案區、`ヒント`或`スキップ`
  - `問題が見つからないよ。`
  - `設定を確認してみてね。`
- 正式狀態圖片完成前，圖片位置使用`工事進行中`未完成插圖placeholder
- 呢個畫面主要用作無current question時的防呆狀態；正常題庫耗盡時直接進入Quiz Summary
- viewport底部固定顯示主要button`クイズ設定へ`
### Quiz no-pool confirmation page

- 呢個畫面在目前Quiz篩選條件找不到題目時顯示，讓user選擇返回修改設定，或者忽略篩選條件並從全部出題対象開始
- Header固定在viewport頂部；中央標題顯示`クイズ設定`，右邊顯示Homepage icon
- 中央內容區由上至下顯示
  - 狀態圖片；正式圖片完成前使用`工事進行中`未完成插圖placeholder
  - `この条件で出せる問題がないよ。`
  - `条件を変えるか、すべての出題対象から始めますか？`
- viewport底部固定顯示兩個相同width及height的操作button
  - 左邊`設定へ戻る`使用較淡的次要button色
  - 右邊`すべてから出題`使用主要亮藍色，作為直接繼續Quiz的主要操作

## Error pages

- 400、403、404、500共用同一套視覺layout
- 不顯示一般site header
- 主要內容在viewport水平及垂直置中
- 由上至下顯示
  1. 大字error code
  2. 對應狀態icon或可愛插圖
  3. 日文標題
     - 使用`Zen Maru Gothic Bold`，不使用`Hachi Maru Pop`
     - 標題基準使用28px；400、403、404、500換行後均維持相同字級，只有實際超出可用闊度時先逐級縮小
     - 400同403標題置中分成兩行
     - 404固定三行並使用相同字級：`どこどこ？`／`ページはどこ？`／`……ないよ。`
     - 500固定三行：`僕のせいだけど、`／`謝るつもりはない`／`www`
  4. 簡短日文說明
  5. `ホームへ`button
- Error page維持低依賴設計；特別是500 page繼續使用獨立self-contained template，不extend `base.html`，避免error handler依賴一般全站context或database navigation
- 視覺上跟全站font、顏色、button風格一致，但實作時要為關鍵樣式提供不依賴一般page runtime的fallback
- 四個Error page同Account activation相關狀態頁共用同一個單柱pyramid tent主體，按error／account狀態改變入口、燈光、角度、環境效果或小道具
  - 正式角色圖片未定前，第一輪UI使用簡單placeholder icon
- Site route顯示日文；如error發生在Django `/admin/`，可以沿用admin介面的現有語言，不為強制轉換加入額外converter code


### 400 page

- 標題：`そのリクエスト、通ると思いました？`
- 說明：`入力内容かURL、ちゃんと確認してくださいね。`

### 403 page
- 標題：`誰でも入れると思わないでください。`
- 說明：`権限がないので、おとなしく戻ってください。`

### 404 page
- 標題分三行顯示：
  - `どこどこ？`
  - `ページはどこ？`
  - `……ないよ。`

- 說明：`いくら探してもありませんよ。URLを確認して、ホームへ戻ってください。`

### 500 page
- 標題分三行顯示：
  - `僕のせいだけど、`
  - `謝るつもりはない`
  - `www`
- 說明：`しばらくしてから、もう一度試してください。`

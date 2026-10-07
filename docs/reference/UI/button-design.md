# Button Design

## 點睇呢份文件

全站按鈕先分 7 組。以下全部係 **目前數值**，未必係最終規格。

Padding 即係文字同按鈕邊框之間嘅距離：

- 上下 padding：影響按鈕高度
- 左右 padding：影響按鈕闊度

本文所講嘅「active area」係中央 app shell 扣除頁面左右留白後，真正放置內容嘅範圍：

- App shell 寬度最多 `540px`，viewport 再闊都保持置中。
- App shell 外只顯示背景。
- Button 百分比寬度以 active area 計算，唔係以整個 browser viewport 計算。

## 總表

| 組別 | 用途 | 字體 | 上下 padding | 左右 padding |
|---|---|---:|---:|---:|
| A. Homepage 主按鈕 | Homepage 中央入口 | `28px` | 約 `20px` | `56px` |
| B. 一般主要按鈕 | Login、Register、普通頁面操作 | `18px` | `8px` | `16px／24px` |
| C. Footer 按鈕 | 頁底提交、保存、下一步 | `18px` | `8px` | `16px／24px` |
| D. Selection 按鈕 | Level、category、題數等選項 | `16px` | 一般 `8px` | 一般 `8px` |
| E. Pagination | First、Previous、頁碼、Next、Last | `16px` | 無 | 無 |
| F. Icon 按鈕 | Back、Home、Logout、Event、密碼眼睛 | 不適用 | 無 | 無 |
| G. Quiz 特殊按鈕 | Tips、Skip、判定、假名鍵盤 | 視種類 | 視種類 | 視種類 |

目前最大問題：B、C 兩組會因 HTML 排法不同，自動變成左右 `16px` 或 `24px`。同類按鈕未真正統一。

---

## A. Homepage 主按鈕

### 邊度見到

- 未登入：`登録`、`ログイン`、`単語帳`
- 已登入：`クイズ`、`単語の追加`

### 目前尺寸

| 字體 | 上下 padding | 左右 padding | 最小高度 | 寬度 |
|---:|---:|---:|---:|---|
| `28px` Bold | 約 `20px` | `56px` | 約 `67px` | 跟文字 |

### 已確認規格

- 保留目前尺寸及視覺效果。
- CSS 比例保留為上下 `.7em`、左右 `2em`。
- 呢組係全站最大、視覺層級最高嘅主要按鈕。

---

## B. 一般主要按鈕

### 邊度見到

- Login：`ログイン`
- Register：`登録`
- Resend activation：`認証メールを再送する`
- Account activation：`アカウントを有効にする`
- Activation result：`ログイン`、`認証メールを再送する`
- Activation email sent：`ログイン画面に戻る`
- Logout：`ログイン`
- User profile：`マイ単語帳`
- Quiz home：`開始`
- Quiz setting：`前回の設定を読み込む`
- UI confirm：所有 preview links

### 目前尺寸

| 字體 | 上下 padding | 左右 padding | 最小高度 | 圓角 |
|---:|---:|---:|---:|---:|
| `18px` Bold | `8px` | `16px` 或 `24px` | `58px` | `17px` |

### 已確認規格

- 基本寬度為 active area 嘅 `50%`。
- 左右每邊最少保留兩個中文字寬度；以 `18px` 字計，即每邊約 `2em／36px`。
- 短文字（例如「開始」）仍維持 active area 嘅 `50%`。
- 如果文字較長，button 可以按內容增加寬度。
- 如果單行所需 button 寬度超過 app shell 嘅 `80%`，文字改為兩行。
- 換行後，以兩行之中較長嗰行重新計算內容寬度，再加左右各兩個中文字嘅空位。
- Button 最少仍為 active area 嘅 `50%`。

計算概念：

```text
button width = max(active area 50%, 最長一行文字寬度 + 左右各 2em)
```

目前未有長到需要處理極端 overflow 嘅 button；日後出現先再定超過兩行嘅處理。

---

## C. Footer 按鈕

### C1. 單一按鈕

#### 邊度見到

- Vocab／User vocab filter：`検索`
- User vocab list：`保存`
- Vocab update／delete：`変更申請／削除申請`
- Event list／detail：`既読にする／未読に戻す`
- Feedback：`送信／返信／終了`
- Quiz setting／question：`開始／回答`
- Quiz summary／no-question：`クイズ設定へ`

#### 目前尺寸

| 字體 | 上下 padding | 左右 padding | 最小高度 | 寬度 |
|---:|---:|---:|---:|---|
| `18px` Bold | `8px` | 通常 `24px` | `58px` | 跟文字，但最少約 `14em` |

### C2. 左右並排按鈕

#### 邊度見到

- User vocab detail：`保存`、`単語の詳細`
- Vocab detail：`変更申請`、`削除申請`
- Vocab create：兩個申請後去向
- Quiz no-pool：`設定へ戻る`、`すべてから出題`
- Quiz result：`次へ`、`結果へ`

#### 目前尺寸

| 字體 | 上下 padding | 左右 padding | 最小高度 | 寬度 |
|---:|---:|---:|---:|---|
| `18px` Bold | `8px` | `16px` 或 `24px` | `58px` | 通常左右等分 |

### 已確認規格

- 上下 padding 保留目前 `8px`。
- 同行只有一粒 button：寬度為 active area 嘅 `50%`，並置中。
- 同行多過一粒 button：扣除中間 gap 後，平均分配整行寬度。
- 同行所有 button 等寬。
- 單一及並排 Footer button 唔再因 HTML nesting 使用不同 padding 規則。

---

## D. Selection 按鈕

用嚟揀選項，唔係提交。

### 邊度見到

- Vocab／User vocab filters
- Vocab create／update
- User vocab detail：`出題する／出題しない`
- Quiz setting：題數、類型、level、categories
- Event list：`すべて／未読／既読`

### D1. 一般 Selection

| 字體 | Padding | 最小高度 | 寬度 |
|---:|---:|---:|---|
| `16px` Bold | 四邊 `8px` | `44px` | 同行平均分配 |

### D2. Level Selection

| 字體 | 上下 padding | 左右 padding | 最小高度 |
|---:|---:|---:|---:|
| `16px` Bold | `6px` | `2px` | `44px` |

Level 特別窄，係為咗正常 viewport 可以一行顯示晒。

### D3. Event 狀態

| 字體 | 上下 padding | 左右 padding | 最小高度 |
|---:|---:|---:|---:|
| `18px` Bold | `8px` | `16px` | `58px` |

Event 狀態其實係 selection，但目前使用一般主要按鈕尺寸，所以比其他 selection 大。

### 已確認規格

- 一般 Selection 上下 padding 保留目前數值。
- 同一個 selection group 內所有 button 必須相同尺寸。
- 每個 field 獨立按選項數排版；只有 Categories 每行最多三粒。
- 以下尾行規則只適用於 Categories。
- 三粒：剛好排滿一行。
- 兩粒：保持同 group 其他 button 相同嘅單粒寬度，靠左排列。
- 一粒：保持相同單粒寬度，置中排列。
- 換行後嘅 button 唔會因為該行數量較少而拉闊。
- Level 保留 compact padding，六粒同一行；Type、in_use、問題數各按本身選項數平均分配一行。

Categories 排列例子：

```text
4 粒：[ 1 ][ 2 ][ 3 ]
            [ 4 ]           ← 同上面每粒一樣闊，整粒置中

5 粒：[ 1 ][ 2 ][ 3 ]
      [ 4 ][ 5 ]         ← 同上面每粒一樣闊，整組靠左
```

---

## E. Pagination

### 邊度見到

Vocab list、User vocab list、Event list、Feedback list。

| 字體 | Padding | 尺寸 | 圓角 |
|---:|---:|---:|---:|
| `16px` Bold | 無 | `36 × 36px` | `8px` |

### 已確認規格

- Pagination 由 `36 × 36px` 改為 `44 × 44px`。

---

## F. Icon 按鈕

### F1. Header Icon

Back、Home、Homepage Logout、Homepage Event。

| Button 尺寸 | Icon 尺寸 | Padding | 形狀 |
|---:|---:|---:|---|
| `48 × 48px` | `28 × 28px` | 無 | 圓形 |

### F2. Password 顯示／隱藏

Login、Register password fields。

| Button 尺寸 | Padding |
|---:|---:|
| `44 × 44px` | 無 |

### 已確認規格

- 保留現狀：Header icon `48px`，password icon `44px`。

---

## G. Quiz 特殊按鈕

### G1. Tips／Skip

| 字體 | 上下 padding | 左右 padding | 最小高度 | 寬度 |
|---:|---:|---:|---:|---|
| `18px` Bold | `8px` | `16px` | `58px` | 左右各一半 |

Review 已記錄樣式仍未達到預期。

### G2. 判定

| 字體 | 上下 padding | 左右 padding | 最小高度 |
|---:|---:|---:|---:|
| `18px` Bold | `8px` | `16px` | `44px` |

### G3. 回答輸入區

成張 frame 可以按，用嚟打開假名 keyboard。

| Padding | 寬度 | 高度 |
|---:|---:|---|
| 四邊 `16px` | `100%` | 跟內容 |

### G4. 假名 Keyboard

| 字體 | Padding | Key 尺寸 |
|---:|---:|---:|
| `22px` Bold | 無 | 最小 `44px`、最大 `62px` |

包括 kana、濁點、半濁點、小書き、Backspace、`完了`。

### 已確認規格

- Tips／Skip 保留現時尺寸；配色按 quiz-question-state.png，背景 #8BC9E6、文字 #26343D。
- 判定保留現時尺寸。
- 假名 keyboard 保留現時尺寸。
- 回答輸入區今次未提出尺寸改動。

---

## 顏色同尺寸分開

| 顏色用途 | 意思 |
|---|---|
| Primary | 最主要操作 |
| Secondary | 次要、返回或替代操作 |
| Danger | 刪除等危險操作 |
| Selected | 已選中 |
| Disabled | 暫時不可操作 |

例：`削除申請` 應使用 Footer 尺寸加 Danger 顏色，唔需要另設 padding。

## 建議統一方法

每粒按鈕只需要指定：

1. 尺寸組別：Homepage／一般／Footer／Selection／Pagination／Icon／Quiz
2. 顏色用途：Primary／Secondary／Danger／Selected／Disabled

每組 padding、font size、height、width 只喺共用 CSS 定義一次，唔再逐頁設定。

## 已確認總結

- Homepage 主按鈕：保留現狀。
- 一般主要按鈕：基本為 active area 50%，每邊最少 2em；過長時分兩行再計寬度。
- Footer：單一為 active area 50% 並置中；多粒平均分配整行。
- Selection：各 field 獨立排版、同 group 同尺寸；Level 六粒同一行，Type／in_use／問題數各自一行。只有 Categories 每行最多三粒，尾行一粒置中、兩粒靠左。
- Pagination：改為 `44 × 44px`。
- Icon：保留現狀。
- Quiz Tips／Skip：保留尺寸，背景改為 #8BC9E6、文字 #26343D。判定、keyboard 保留現狀。

## 技術備註

目前一般 button 共用 `.ui-button`：

- Base：`18px`、上下 `8px`、左右 `16px`、最小高度 `58px`
- 部分父層規則會將左右 padding 改成 `24px`
- Homepage 主按鈕同 Homepage footer 再各自 override

所以目前問題係同一 class 會受父層 HTML 結構影響。

Django admin 嘅 `Approve／Reject` 使用 admin theme，唔納入前台設計。

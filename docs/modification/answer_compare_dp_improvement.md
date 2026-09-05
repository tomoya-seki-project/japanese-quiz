# Answer Compare Bottom-up DP Improvement Report

## 目的

今次改動係將 quiz app 原本使用 recursive branch search 嘅逐字答案比較，改成 bottom-up dynamic programming（DP）。

舊設計：

- `QuizService.answer_compare()` 由目前兩個字串位置開始遞迴。
- 字元相同時直接進入下一對字元。
- 字元唔同時同時展開 `WRONG`、`MISSING`、`EXTRA` 三條路。
- 每條路都會保存及組合完整 result list。
- 大量 mismatch 時會重複計算相同 `(i, j)` state，最壞執行時間呈指數級增長。

新設計：

- `QuizService.answer_compare_dp()` 建立 `(m + 1) × (n + 1)` DP table。
- 每個 `(i, j)` state 只計算一次。
- 每格只保存由該位置開始嘅最佳 score、operation 同 wrong subtype。
- 填表完成後，由 `dp[0][0]` 沿 operation 重建 result。
- 時間複雜度變成 `O(m × n)`，空間複雜度係 `O(m × n)`。
- Public return format、score ranking 同原本 tie-breaking 行為保持一致。

## 原本問題

### Recursive branch search

舊版 `answer_compare()` 以兩個 cursor 表示目前比較位置：

```text
i = correct answer 目前位置
j = user answer 目前位置
```

當兩個字唔同，會展開三條路：

```text
WRONG   -> compare(i + 1, j + 1)
MISSING -> compare(i + 1, j)
EXTRA   -> compare(i, j + 1)
```

唔同遞迴路徑會多次到達同一個 `(i, j)`，但舊版無 cache，所以同一個 suffix comparison 會被重複計算。

例如：

```text
compare(0, 0)
├─ WRONG   -> compare(1, 1)
├─ MISSING -> compare(1, 0)
│             └─ EXTRA -> compare(1, 1)
└─ EXTRA   -> compare(0, 1)
              └─ MISSING -> compare(1, 1)
```

`compare(1, 1)` 已經重複出現；答案愈長、mismatch 愈多，重複分支會迅速增加。

### 實際影響

Project review 嘅 targeted benchmark 顯示，舊 recursive implementation 處理 11 字元大量 mismatch 時已超過 5 秒 timeout。

Answer form 最多接受 25 字，因此唔可以再依賴「一般 kana 答案比較短」避免最壞情況。即使正常答案多數短，惡意或極端輸入仍然會佔用 request worker。

## 點解選擇 Bottom-up DP

曾考慮兩個方向：

### 方案 A：Recursive + memoization

為每個 `(i, j)` 保存第一次計算結果，下次到達相同 state 時直接重用。

優點：

- 改動較少。
- 同舊 recursive mental model 接近。
- 同樣可以將時間複雜度降到 `O(m × n)`。

代價：

- 仍然保留 recursive call stack。
- 如果每個 cache entry 保存完整 result list，仍會產生大量 list copy。
- 填表順序、state 同 reconstruction 較隱含。

### 方案 B：Bottom-up DP

預先建立所有 state，由已知邊界開始逐格計算，最後先重建一次 result。

優點：

- 每格只計算一次。
- 無 recursive call stack。
- Score calculation 同 result reconstruction 清楚分開。
- 容易檢查填表 dependency、tie-breaking 同 performance。
- 每格唔需要保存完整 result list。

今次採用方案 B，因為呢段係 quiz 核心比較邏輯，清晰嘅 state table 比保留 recursive shape 更容易長期維護。

## DP State 定義

定義：

```text
dp[i][j]
= correct_answer[i:] 同 user_answer[j:] 嘅最佳比較結果
```

其中 `answer[index:]` 代表由 `index` 開始到字串結尾嘅 suffix。

例如：

```text
correct_answer = がっこう
user_answer    = かこう

dp[1][1]
= っこう 對 こう 嘅最佳結果
```

DP cell 唔係只比較 `correct_answer[i]` 同 `user_answer[j]` 一對字；佢代表「由目前位置開始，所有剩餘字元」嘅最佳總結果。

## Data Structure

### `Score`

每個 state 使用三項數值比較候選路線：

```python
@dataclass
class Score:
    cost: int
    match_count: int
    non_normal_wrong_count: int
```

欄位用途：

- `cost`：總 edit cost；`WRONG`、`MISSING`、`EXTRA` 各加 1。
- `match_count`：完整相同字元數量。
- `non_normal_wrong_count`：`DAKUTEN`、`HANDAKUTEN`、`SMALL_KANA` 等具教學意義 wrong subtype 數量。

### `DPCell`

```python
@dataclass
class DPCell:
    score: Score
    operation: Optional[str]
    sub_operation: str | None = None
```

每格保存：

- 由該 state 開始嘅最佳 aggregate score。
- 最佳路線第一步應執行嘅 operation。
- 如果 operation 係 `WRONG`，保存 wrong subtype。

無保存 `next_i`、`next_j`，因為下一格可以由 operation 唯一推算：

```text
MATCH / WRONG -> (i + 1, j + 1)
MISSING       -> (i + 1, j)
EXTRA         -> (i, j + 1)
END           -> 停止
```

### 建立 2D table

```python
m = len(correct_answer)
n = len(user_answer)

dp_table: list[list[Optional[DPCell]]] = [
    [None for _ in range(n + 1)]
    for _ in range(m + 1)
]
```

額外一行同一列用嚟表示其中一邊已經去到字串結尾。

如果 correct 有 4 字、user 有 3 字：

```text
(4 + 1) × (3 + 1) = 5 × 4 = 20 cells
```

## 填表方向

目前 state 使用 suffix 定義，每格可能依賴：

```text
dp[i + 1][j]      # 下面
dp[i][j + 1]      # 右邊
dp[i + 1][j + 1]  # 右下
```

因此 child cells 必須先計算，再計 parent cell。Loop 由右下向左上：

```python
for i in range(m, -1, -1):
    for j in range(n, -1, -1):
        ...
```

實際係由最底一行開始，每行由右至左：

```text
dp[m][n] -> dp[m][n-1] -> ... -> dp[m][0]
dp[m-1][n] -> ...
...
dp[0][0]
```

由右下開始唔係所有 DP 嘅固定規則。今次由右下開始，係因為 suffix state 依賴右、下、右下；原則永遠係先計 dependency。

## Boundary Conditions

### 兩邊都用完：`END`

```text
i == m and j == n
```

兩邊 suffix 都係空，唔需要任何 edit：

```text
score = (0, 0, 0)
operation = END
```

### Correct 用完：`EXTRA`

```text
i == m and j < n
```

Correct 已經無字，user 剩低嘅每個字只可能係 `EXTRA`：

```text
dp[m][j] = EXTRA + dp[m][j + 1]
```

Score：

```text
cost                   = next.cost + 1
match_count            = next.match_count
non_normal_wrong_count = next.non_normal_wrong_count
```

### User 用完：`MISSING`

```text
j == n and i < m
```

User 已經無字，correct 剩低嘅每個字只可能係 `MISSING`：

```text
dp[i][n] = MISSING + dp[i + 1][n]
```

呢兩條邊界唔係不良 hard code，而係演算法嘅通用 base cases。佢哋由輸入長度 `m`、`n` 推導，唔係針對某個固定答案或固定座標寫死。

## 內部 Cell 計算

### 字元相同：`MATCH`

如果：

```python
correct_answer[i] == user_answer[j]
```

目前 scoring rule 下可以直接選 `MATCH`：

```text
next state              = dp[i + 1][j + 1]
cost                    = next.cost
match_count             = next.match_count + 1
non_normal_wrong_count  = next.non_normal_wrong_count
```

`MATCH` 同時消耗 correct 同 user 一個字元。

### 字元不同：建立三個 candidates

唔可以直接比較三個 child cells；必須先加入目前 operation 嘅 cost／score adjustment，再比較形成嘅 candidates。

#### `WRONG`

```text
child     = dp[i + 1][j + 1]
cost      = child.cost + 1
match     = child.match_count
special   = child.non_normal_wrong_count + current subtype contribution
```

Current correct/user 字元會傳入 `define_wrong_sub_type()`：

```python
sub_operation = QuizService.define_wrong_sub_type(
    correct_letter=correct_answer[i],
    user_letter=user_answer[j],
)
```

Subtype 唔係 `NORMAL` 時，`non_normal_wrong_count` 加 1。

#### `MISSING`

```text
child   = dp[i + 1][j]
cost    = child.cost + 1
match   = child.match_count
special = child.non_normal_wrong_count
```

只消耗 correct 字元。

#### `EXTRA`

```text
child   = dp[i][j + 1]
cost    = child.cost + 1
match   = child.match_count
special = child.non_normal_wrong_count
```

只消耗 user 字元。

## Ranking 與 Tie-breaking

三個 candidates 使用：

```python
min(
    wrong_result,
    missing_result,
    extra_result,
    key=lambda result: (
        result.score.cost,
        -result.score.match_count,
        -result.score.non_normal_wrong_count,
    ),
)
```

排序規則依次係：

1. 最少 `cost`。
2. Cost 相同時，最多 `match_count`。
3. Cost、match 都相同時，最多 `non_normal_wrong_count`。
4. 三項完全相同時，保留傳入 `min()` 最先出現嘅 candidate。

因為 candidate order 係：

```text
WRONG -> MISSING -> EXTRA
```

所以完整同分時仍然保留舊 implementation 嘅 deterministic tie-breaking。

負數只係用嚟將「愈大愈好」轉成 `min()` 可以處理嘅排序：

```text
match_count 3 -> -3
match_count 2 -> -2

min(-3, -2) 會揀 -3，即原本較大嘅 match_count 3
```

## 例子：`がっこう` 對 `かこう`

```text
correct = が っ こ う
user    = か   こ う
```

最佳 reconstruction path：

```text
dp[0][0] WRONG   が -> か  subtype=DAKUTEN
dp[1][1] MISSING っ
dp[2][1] MATCH   こ -> こ
dp[3][2] MATCH   う -> う
dp[4][3] END
```

最終 score：

```text
cost                   = 2
match_count            = 2
non_normal_wrong_count = 1
```

`dp[1][1]` 揀 `MISSING` 唔係預先寫死，而係三個 candidate 加入目前 operation cost 後，`MISSING` 得到最佳總 score。

## Reconstruction

填表完成時，`dp[0][0].score` 已經係完整答案嘅最佳總分，但 public output 仲需要逐字 result list。

Reconstruction 由左上角開始：

```python
result = []
i = 0
j = 0

while dp_table[i][j].operation != "END":
    cell = dp_table[i][j]
    ...
```

每一步做兩件事：

1. 按 operation 將一筆資料加入 `result`。
2. 按 operation 更新 cursor。

Result mapping：

```text
MATCH:
    correct = correct_answer[i]
    answer  = user_answer[j]
    move    = i + 1, j + 1

WRONG:
    correct = correct_answer[i]
    answer  = user_answer[j]
    subtype = cell.sub_operation
    move    = i + 1, j + 1

MISSING:
    correct = correct_answer[i]
    answer  = None
    move    = i + 1, j

EXTRA:
    correct = None
    answer  = user_answer[j]
    move    = i, j + 1
```

Reconstruction 階段唔會再次比較 score。最佳 decision 已經喺填表階段寫入每個 cell；呢一步只係沿住保存嘅 operation 行到 `END`。

未知 operation 會明確 raise error，避免 cursor 無移動而形成無限 loop：

```python
case _:
    raise ValueError(f"Unknown operation: {cell.operation}")
```

## Public Interface 保持不變

`compare_kana_answer()` 已由舊 recursive implementation 切換到 DP：

```python
return QuizService.answer_compare_dp(
    correct_answer=correct_answer or "",
    user_answer=user_answer or "",
)
```

DP 最後仍回傳原本 dictionary contract：

```python
{
    "cost": ...,
    "match_count": ...,
    "non_normal_wrong_count": ...,
    "result": [...],
}
```

因此 `gen_answer_image()`、quiz submit view 同 result partial 唔需要因演算法改動而更改資料格式。

## 複雜度改善

假設：

```text
m = len(correct_answer)
n = len(user_answer)
```

### 舊版

Mismatch 時最多展開三條 recursive branches，同一 state 反覆計算，最壞情況呈指數級增長。

### 新版

DP table 有：

```text
(m + 1) × (n + 1)
```

每格只做固定數量工作：

```text
Time  = O(m × n)
Space = O(m × n)
```

25 對 25 最多只有：

```text
26 × 26 = 676 cells
```

呢個規模對目前 synchronous quiz request 足夠細。

## 測試 / 驗證

### Django checks

已執行：

```text
manage.py check
```

結果：

```text
System check identified no issues (0 silenced).
```

### 新舊 implementation equivalence

保留舊 recursive `answer_compare()` 作短輸入 oracle，將相同 correct/user input 分別傳入新舊 implementation，再比較完整 return dictionary。

測試範圍：

- Alphabet：`あ`、`い`、`が`、`か`、`っ`
- 字串長度：0 至 3
- Correct/user 所有配對：24,336 組
- 比較內容：cost、match count、non-normal wrong count、operation result sequence 及 subtype

結果：

```text
24,336 pairs
0 mismatches
```

### Worst-case targeted benchmark

測試：

```text
correct = 25 個「あ」
user    = 25 個「い」
```

結果：

```text
cost = 25
執行時間約 0.0018 秒
```

Benchmark 數字會因硬件、OS 負載同 Python runtime 有變化；重要結果係新版完成固定數量 DP cells，無舊版 branch explosion。

## 最終狀態

目前 kana answer comparison 已完成由 recursive branch search 遷移至 bottom-up DP：

- Quiz public入口已使用 `answer_compare_dp()`。
- Output contract 保持不變。
- 原有 ranking、subtype preference 同 deterministic tie-breaking 保持不變。
- 長 mismatch 輸入唔再呈指數級增長。
- 舊 recursive function 暫時保留，可作 characterization／regression comparison reference。

## 之後注意事項

### 1. Automated regression tests

目前已完成 targeted equivalence verification，但正式 automated test suite 仍應加入：

- 空字串／單邊空字串。
- 全部 `MATCH`。
- 全部 `WRONG`。
- 中間 `MISSING`／`EXTRA`。
- `DAKUTEN`、`HANDAKUTEN`、`SMALL_KANA`。
- 完整 score 相同時嘅 candidate-order tie-break。
- 25 字 worst-case performance guard。

Tests 統一由 TODO「改善 D：補 tests」追蹤。

### 2. 舊 recursive implementation

正式 regression tests 穩定後，可以考慮移除舊 `answer_compare()`，避免日後兩套 implementation 同時存在而產生維護混亂。

### 3. Type hints

DP table 初始化時包含 `None`，但填表順序保證讀取 child cell 前已經完成計算。Static type checker 未必能從 nested loop 證明呢項 invariant，因此可能將 `next_cell` 判斷為 `DPCell | None`。

如果日後加入嚴格 type checking，可以使用清楚嘅 assertion 或 helper 封裝「取得已完成 cell」，唔應該為消除 warning 而靜默忽略真正可能嘅 `None`。

### 4. Ranking rule 改動

目前「字元相同直接 MATCH」係基於現有規則：MATCH 無 cost，而且增加 match count，所以一定唔會差過刻意將相同字拆成 edit operations。

如果將來改變 operation cost、加入 position-dependent score，或者引入跨字元規則，就要重新確認：

- MATCH 仲可唔可以直接決定。
- `Score` 是否需要加入新欄位。
- Candidate ranking key 是否仍代表完整產品規則。
- State 是否仍只需要 `(i, j)`。

### 5. 命名一致性

`DPCell.sub_operation` 實際保存嘅係 wrong `sub_type`。目前功能無問題；將來整理 code 時可以考慮統一命名，減少 domain terminology 差異。

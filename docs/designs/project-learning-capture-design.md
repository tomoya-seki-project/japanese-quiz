# project-learning-capture 詳細設計

文件性質：供使用者及 ChatGPT 審閱嘅設計提案，唔係已安裝嘅 skill。此版已納入外部 feedback，仍待使用者補充與最終確認。

配套文件：[project-learning-guide 詳細設計](project-learning-guide-design.md)。本文件包含獨立閱讀所需背景。

共用格式唯一規格：[LIBRARY.md 草案](LIBRARY.md)。交俾其他 AI 審閱時，請連同呢份格式草案一齊提供。

## 1. 使用者需求與本次範圍

使用者希望建立跨 project 共用嘅 learning library（學習知識庫），保存自己學過、做過及值得再參考嘅 programming 知識。日後由 `project-learning-guide` 先用過往例子提醒，再按需要結合目前 project 解釋。

已確認需求：

- `project-learning-capture` 同 `project-learning-guide` 都係 global skills。
- Library 最終承接現有 `docs/status/CODING_REFERENCE.md` 嘅全部內容及角色；日後新知識直接收錄入 library。
- 首次轉移後必須保留原本 `CODING_REFERENCE.md`，由使用者自行刪除。唔截斷、清空、覆寫成指向 library 嘅 stub，亦唔搬走原檔。
- Library 成立後，capture 唔再寫 project coding reference，guide 唔再依賴佢。原檔暫時仍存在，唔代表繼續同步。
- Modification report 係使用者大修改後留作 review／學習嘅完整紀錄；capture 整理相關知識時應參考對應 report。
- Report 係資料來源，唔係對 `modification-learning-report` skill 嘅依賴。唔自動呼叫、修改或改變該 skill 嘅輸出位置。
- 使用者已使用 VS Code multi-root workspace；guide 提供 HTML 連結，唔主動開 browser。
- 今次只產生設計文件，未執行資料轉移、安裝 skill 或修改其他 workflow。

本文件其餘結構、路徑及 metadata 係建議實作，唔冒充使用者已逐項指定。

## 2. 職責與分工

Capture 負責將使用者指定嘅內容變成可檢索、可追溯、可跨 project 重用嘅學習紀錄，包括選擇來源、整理、查重、關聯例子、登記索引及檢查連結。

| 元件 | 負責 | 不承擔 |
|---|---|---|
| Capture | 寫入及更新 library；處理指定資料嘅首次匯入 | 日常自動收集每段對話；修改應用程式；創作未提供證據嘅歷史 |
| Guide | 搜尋 library；判斷適用性；提醒、解釋及提供連結 | 自動修改 topic、catalog 或來源 report |
| Modification report 文件 | 提供原本問題、前後 code、取捨、驗證與限制 | 自動成為目前 project 現況或跨技術規則 |

Capture 可以獨立運作，唔要求 guide 或 report-generation skill 已被呼叫。

Guide 按需要搜尋，唔係每個 coding 問題都讀 library；呢個觸發政策唔改變 capture 嘅明確收錄條件。使用者叫收錄時，capture 仍需搜尋既有條目以查重，唔因該知識點簡單而跳過。

## 3. 觸發與收錄範圍

建議 description 草案：

> Capture user-selected programming knowledge into a shared global learning library. Use when the user clearly asks to save, collect, import, organize, or update learning notes or examples. Consult relevant existing modification reports as source material. Do not treat ordinary explanations, implementation requests, or design discussion as collection intent.

正常自然語言可觸發，毋須每次輸入 `$project-learning-capture`。唔需要設定成只有明確 skill 名稱先可啟用；真正寫入嘅條件係使用者有清楚收錄意圖。

| 使用者請求 | 行為 |
|---|---|
| 「將今次 bottom-up DP 收錄入 library」 | 收錄已識別嘅 DP 知識與直接相關案例 |
| 「保存頭先講嘅 exception ownership」 | 根據對話及可用證據整理指定主題 |
| 「將呢份 report 有關 transaction 嘅部分整理入 library」 | 整理 transaction；唔擴展至 report 全部主題 |
| 「將 coding reference 全部轉移入 library」 | 執行完整匯入及覆蓋核對；保留來源原檔 |
| 「DP 係點做？」 | 交由一般解釋／guide，唔寫入 |
| 「呢個值得保存嗎？」 | 評估；唔當成收錄命令 |
| 「之後應該點設計 capture？」 | 討論設計；唔入庫討論中嘅全部內容 |

「收錄呢個」若從緊接對話可以唯一識別，直接處理。只有多個合理主題會令實際保存範圍明顯唔同，先問一條具體問題。唔為每個 metadata 或分類選擇要求批准。

## 4. 共用 library 與路徑

建議將資料獨立於兩個 skill 嘅程式／指令目錄，避免 library 被誤認為 guide 嘅可替換附帶資源。

建議預設位置：`/home/seki/.codex/learning-library/`。此路徑係提案，正式實作時遵從使用者指定位置；兩個 skill 必須使用同一個已配置嘅 root，唔各自建立副本。

```text
/home/seki/.codex/
├── skills/
│   ├── project-learning-capture/
│   │   └── SKILL.md
│   └── project-learning-guide/
│       └── SKILL.md
└── learning-library/
    ├── LIBRARY.md
    ├── catalog.md
    ├── topics/
    │   ├── algorithms/
    │   │   └── bottom-up-dp.md
    │   └── django/
    │       └── admin-action-flow.md
    ├── sources/
    │   └── japanese-quiz/
    │       └── answer-compare-dp/<snapshot-id>/
    │           ├── SOURCE.md
    │           ├── answer_compare_dp_improvement.md
    │           ├── answer_compare_dp_improvement.html
    │           ├── assets/report.css
    │           └── example/...
    └── imports/
        └── japanese-quiz-coding-reference/<import-id>/
            ├── original.md
            └── mapping.md
```

圖中目錄係有內容先建立，唔預建空語言分類。`<snapshot-id>`、`<import-id>` 係實作時產生嘅穩定識別，唔係 literal 檔名。

- `LIBRARY.md`：共用格式版本、路徑解讀、欄位定義及來源規則。兩個 skill 都讀同一份契約。
- `catalog.md`：輕量搜尋入口；列 topic ID、標題、問題別名、技術條件及 topic 路徑，唔重複完整知識。
- `topics/`：整理後嘅主要教學文件。Topic 內容及 metadata 係索引嘅依據。
- `sources/`：已收錄嘅原始 report／HTML 圖解／必要 assets 嘅歷史快照。多個 topic 可以引用同一份來源。
- `imports/`：首次大型轉移嘅原始內容及對照紀錄，唔係日常 guide 嘅主要搜尋範圍。

Library 內部用相對路徑，外部來源按共用規格明確標記；對使用者輸出時先定位實際檔案，chat 連結格式按 guide G18 實作驗收結果決定。唔把 cwd 或目前選中嘅 VS Code root 當成 library root。多個 project 開住而來源不明時，先確認相關檔案屬於邊個 repository。

Library 尚未建立時，capture 可以喺已獲授權嘅首次收錄中初始化指定位置；位置有歧義先詢問。若環境唔允許寫 global 路徑，依實際權限流程處理，唔默默改寫入 project repo。

獨立 library 需要喺 multi-root workspace 加入該 folder；如果使用者更想資料位於現有 skills root 之內，可以選另一個 root，資料契約唔因此改變。呢個係安裝位置選擇，唔係收錄時反覆決定嘅事。

## 5. 文件粒度與共用資料契約（提案 v1）

以「能回答一個完整問題」作為拆分單位。短主題一份 MD；大型流程可以保留完整流程文件，再連結細題目。唔按每個 heading 機械拆分，亦唔強制每題都有 `concept.md`、implementation MD 同 HTML。

Topic 使用 YAML frontmatter；其唯一 schema、欄位型別、必填／可選規則、ID、versions、`source_refs`、來源 manifest、SHA-256、snapshot／import ID 同 catalog 格式，全部由 [LIBRARY.md](LIBRARY.md) 定義。Capture 寫入前讀取並遵從，唔喺自身 skill 另存一份格式定義。

格式嚴格唔等於資料必須齊全。未知版本／基準依共用規格表示，唔猜測亦唔因此阻止保存有用知識。段落證據與適用條件仍用人類可讀正文，唔強制將每句教學結構化。

`record_state` 表示整篇 topic 嘅可用性；局部未驗證想法只需段落限制，唔自動令整篇變 `needs-review`。只有未解問題影響主要結論或安全重用時先標該狀態。另一 framework 新案例唔自動令原本有效案例過時；具體 enum／條件以共用規格為準。

概念式 topic 範本：

```markdown
# Bottom-up DP：由相依狀態逐步建立答案

## 幾時可以諗起呢個做法

使用者會遇到嘅症狀、問題及適用前提。

## 核心理解

足以獨立重溫嘅解釋及必要小例子。

## 我以前點用過

來源 project、具體問題、當時做法與理由；未做過就清楚寫明。

## 可以沿用與需要改動嘅部分

概念、語言／framework 細節、domain 規則分別說明。

## 驗證、限制與未確認事項

區分來源 report 記載、今次檢查與未實作推論。

## 相關案例

完整 report、HTML 圖解、其他 topic 嘅連結及各自用途。
```

Topic 要足以重溫，唔可以只剩幾句摘要加一條指向已刪 project 文件嘅連結。

## 6. 正常 capture 流程

### 6.1 識別收錄目標

從請求及目前對話辨認目標問題、指定內容、技術棧及已知來源。使用者只叫保存一個細知識點，就唔順手收錄同一 project 所有修改。

### 6.2 搜尋已存在知識

先讀 catalog，按問題、術語、別名及技術條件搜尋；未命中就再搜 topics 標題及內文。唔因為 catalog 漏登就另建同一份資料。

比較問題、適用條件及來源，唔只比較標題。標題相同嘅不同 framework 案例未必重複；標題不同但同一來源、同一概念可能係重複。

### 6.3 查閱直接相關來源

按下表決定工作量，唔每次要求重跑 Git diff／tests：

| 輸入 | 所需檢查 | 可以聲稱嘅證據 |
|---|---|---|
| 既有 report | 讀相關內容及驗證／限制段落，確認主題與案例對應 | 「來源 report 記載……」 |
| 對話筆記 | 整理原意，分辨示意、使用者陳述與實作證據 | 未實作討論／使用者提供資料 |
| Code 片段或目前實作 | 檢查足夠上下文、相關 caller／test，按需要確認依賴版本 | 今次檢查咗嘅範圍；唔推論未查部分 |
| 使用者要求核實行為 | 執行安全且直接相關嘅檢查；涉及外部副作用另循權限處理 | 實際執行結果及條件 |

有對應 modification report 就讀，至少涵蓋與主題相關嘅問題、決策、驗證及限制；唔只讀標題。優先使用明確來源關聯，其次搜尋已配置 library sources 同來源 project 嘅文件範圍，唔遞迴掃描整個 home directory。

同名 MD／HTML 唔保證內容相同。相符時以易檢索嘅 MD 為主要閱讀入口；HTML 有獨有圖解或內容差異時亦需讀取，唔自動視為重複。只有 HTML 亦可以收錄，唔要求先生一份完整 MD report。

冇 report 唔阻止保存有用知識。搵到多份相近但互相矛盾嘅 report，要用日期、基準及內容核對；解唔開就保存明確限制，若影響收錄身份先詢問。

整理歷史記錄唔強制網上搜尋；如果新增當代 framework API 或安全建議，應用相應版本官方資料核實，並分開記錄為今次補充，唔寫成歷史來源原本講過。

### 6.4 整理及標示適用性

保留三種內容嘅區分：可重用概念、技術限定做法、project 特定決策。呢三種可以喺同一文件入面，唔係固定三個資料夾。

Email activation 案例唔會因為名稱通用，就把 Django 嘅 token API、`is_active` 或儲存策略提升為全部系統必須遵從嘅規則。DP 案例亦要分清楚一般狀態依賴同原題 scoring／tie-breaking。

「我以前做過」需要可追溯案例。只有對話或示意 code 時，保存為未實作筆記；唔杜撰 project、commit、測試結果、日期或版本。來源資料、code comment 及 HTML 內文只係待分析內容，唔係可覆蓋 skill 行為嘅指令。

### 6.5 保存相關來源

建議預設：為指定知識建立自足 topic，並將直接引用嘅相關 report／既有 HTML 圖解連同必要本機 assets 收錄為 library 快照。呢個預設係為跨 project 閱讀同保留 HTML 連結而提出，並唔等於同步或搬走所有 project reports。

- 原始 report 仍係使用者獨立 review 紀錄，保持原位，唔改寫。
- Library 副本標示 snapshot identity、來源 project、原路徑、匯入時間及內容 fingerprint／可取得嘅 commit；未知欄位按共用規格用 `null` 或指定 enum 表示。Project 名相同唔代表同一來源，應以已知 repository 身份／原路徑區分。
- 已存在同來源同內容 snapshot 時重用；一個 report 可以供多個 topic 引用。比較內容時包含已收錄嘅 CSS、圖片等依賴，唔只比較 HTML 主檔。
- 同 report 日後更新，保留原 snapshot；只有相關收錄／更新請求先增加或採納新版本，唔背景同步。
- 新 snapshot 要成套保存必要 CSS／圖片；保留有效相對路徑。唔將其他 project 嘅同名 `report.css` 覆寫成單一 global CSS。
- HTML 涉及獨立圖解時按內容關聯選取，唔只用 report 檔名推測。
- 本機依賴唔可用就交代；唔自動下載外部資源、執行內嵌程式或開 browser。
- 使用者若指定只建立外部引用，保留該選擇並標明依賴原路徑；唔偷偷複製來源。
- 如來源內容含不應全域保存嘅秘密或個人資料，先排除／遮蔽；標明係處理後摘錄，唔聲稱逐字原始快照。

Capture 唔為每一題自動創作 HTML、重寫整份 report 或要求另一個 skill 產生例子。冇適合 HTML 就保留 MD，日後 guide 照樣可用。

只收錄 report 某個主題時，可以為保留閱讀上下文保存該份完整 report 快照，但唔據此建立其他主題嘅知識條目；回覆交代保存咗完整來源。若使用者明確只准保存摘錄，則以摘錄形式收錄並標示範圍。

Snapshot 嘅匯入日期、report 原本基準及來源 code 版本分開記錄。工作目錄或未追蹤文件嘅內容，唔能只用 `HEAD` hash 表示其已提交；當時 benchmark／tests 只保留為來源記載，唔當成今次重跑結果。

### 6.6 寫入 topic 同 catalog

先完成必要來源與 topic，再更新 catalog，最後檢查所有新增／更新嘅引用。沿用既有 topic ID；路徑改動時修正 library 內已知反向引用。

新知識嘅細節以 topic／source 為準；catalog 只負責發現。分類、版本、來源欄位唔喺三份檔案各自獨立維護。

### 6.7 回覆

交代新增、更新、重用或未能完成嘅項目，附實際可用嘅 topic／HTML 連結。指出來源是否只讀、是否建立 library snapshot，以及重要證據限制。唔把「已寫入檔案」當成「全部連結與內容核對完成」。

## 7. 查重、更新及衝突規則

| 情況 | 做法 |
|---|---|
| 同一來源、同一內容、已有相同 topic | 重用；無新內容就回報已收錄，唔改日期製造更新 |
| 同一 topic 新增清楚解釋 | 合併相關段落，保留來源身份及原有有效內容 |
| 同一功能、另一 framework | 增加案例；有足夠內容再拆 implementation 文件 |
| 同一 project 另一輪修改 | 新歷史來源；唔覆蓋舊 report |
| 新舊資料互相矛盾 | 記錄版本／條件差異；局部問題用段落限制，影響主結論或安全重用而無法解決時先標 `needs-review` |
| 使用者自行修改 library | 保留其修改；重讀目標再寫，唔用舊副本覆寫 |

V1 預設一次只有一個 capture writer。Guide 可以讀取已完成內容。寫入時若目標同已讀基準不一致，要重新比較；未能安全合併嘅重疊改動先詢問。唔為第一版建多程序同步系統，但亦唔聲稱支援同時入庫。

中途失敗時保留已知完成／未完成清單，修復斷鏈後先宣告完成。再次執行先檢查現有 topic 與 snapshot，唔靠換檔名重複匯入。

## 8. 首次完整轉移 CODING_REFERENCE.md

呢個係 capture 嘅指定匯入模式，唔係正常收錄必經步驟。

1. 完整讀取來源，包括所有 substantive sections、code、例子、限制、來源同相互引用；唔只讀目錄。
2. 記錄來源檔案路徑及本次內容 fingerprint；保存一份 library 內原始 `original.md`。原 repository 檔案保持原樣。
3. 建立 section inventory，優先沿用現有 anchor／entry ID；冇 ID 時給予穩定匯入識別。
4. 按完整問題整理 topic；可以合併或拆分，但必須保留語義、重要 code、例子及限制。唔只提煉「通用」部分而丟棄 project 案例。
5. 參考已明確對應嘅 modification report／HTML 圖解；冇 report 嘅 entry 照樣轉移。
6. `mapping.md` 逐項列「原 ID／章節 → 新 topic 與章節 → 重組說明 → 覆蓋核對」。合併、拆分、無實質內容嘅 placeholder 都要交代。
7. 逐段核對重要內容有落點；原始備份只係保底，唔可當作全部 topic 已整理嘅證明。
8. 檢查新 topic／HTML／CSS 連結；更新 catalog。
9. 再比較原 repository 檔案 fingerprint，確認來源內容是否一致。若使用者同時有修改，交代本次匯入基準及差異，唔覆寫原檔或假稱最新內容已全部涵蓋。
10. 提供匯入對照、完成範圍及待處理事項。明確告知原檔仍在，由使用者自行決定刪除時間。

「全部轉移完成」需要 inventory 所有實質內容均有解釋清楚嘅落點。未處理項目必須列出，唔可以因為完成常見主題就宣告完成。

日後 guide 以 topics／sources 運作；`imports/original.md` 只供核對來源，唔成為另一份持續更新嘅 coding reference。

## 9. 舊 workflow 整合注意事項

本次唯讀檢查發現 Japanese Quiz 嘅 `.agents/skills/project-status-sync/SKILL.md` 仍然列出 `docs/status/CODING_REFERENCE.md` 為文件來源，並包含確認後寫入該檔案嘅流程。

將來切換時要另外協調該既有規則，避免其他 workflow 重新建立或更新 project coding reference。Capture／guide 唔應暗中改其他 skill；亦唔能夠靠自身設計保證另一個 skill 永遠唔寫舊檔。

目前階段只記錄整合點，唔執行 project status sync、唔改歷史紀錄、唔更新既有 skill。原有歷史紀錄提及舊路徑可以保留歷史身份，唔一律全域取代文字。

## 10. 技術範圍與維護成本

- 第一版用 Markdown、既有 HTML、本機檔案搜尋；唔引入資料庫、embedding 或向量檢索服務。
- 唔預先產生所有語言分類，唔要求每個 entry 擁有 HTML。
- Library 格式規則放 `LIBRARY.md` 一處；兩個 skill 只保存各自流程與如何定位同一份 library。
- 若首次轉移需要機械拆分／連結檢查腳本，只為實際重複工作寫最小工具；屬於實作範圍，今次設計冇建立腳本。
- 建議 library 使用獨立版本控制或備份，原因係佢將承接原本受 project Git 保護嘅資料；唔默默初始化或推送 remote。
- Library 係使用者可手動編輯嘅普通檔案。索引漏登唔等於 topic 不存在；capture 更新時只核對相關範圍。

## 11. 驗收情境

以下係實作後應執行嘅行為驗收，唔表示今次已運行 skill 測試。

| ID | 輸入／前提 | 預期可觀察結果 |
|---|---|---|
| C01 | 對話只有 DP 解釋，未叫保存 | Library 無變動 |
| C02 | 叫保存討論中概念，未有實作 | 產生可重溫 reference，標明未實作，無虛構 report／測試 |
| C03 | 收錄 DP，有相關 report 同獨立 HTML 圖解 | Topic 連到兩者，說明各自用途；原檔不變 |
| C04 | 同一份資料收錄兩次 | 重用既有 entry／source，冇 duplicate |
| C05 | 收錄相同功能嘅另一 framework | 同一主題下保留不同案例及條件，唔互相覆蓋 |
| C06 | Report 記載測試通過，但今次未執行 | 明確係原 report 嘅驗證紀錄，唔聲稱今次測試通過 |
| C07 | 完整匯入 coding reference | 每個實質 section 有 mapping；原檔 fingerprint 不變 |
| C08 | 同名 MD／HTML 內容不同 | 保留差異同來源關係，唔默認任一份涵蓋另一份 |
| C09 | HTML 使用相對 CSS／圖解路徑 | 收錄後所有必要本機依賴可解析，無覆寫別個案例 stylesheet |
| C10 | 使用者手動改過目標文件 | 合併前重讀，保留其內容或回報具體衝突 |
| C11 | 有相關資料但 catalog 漏登 | 內文搜尋找到並修復相關索引，唔重複新增 |
| C12 | Global root 不可寫或來源有歧義 | 說明確切限制，唔偷偷落入 repo／捏造來源 |
| C13 | Snapshot 保存到一半中斷 | 可識別完成範圍；重試重用已有內容，修復後先宣布完成 |
| C14 | HTML 無變但 CSS／圖片變咗 | 識別來源 bundle 有差異，舊 snapshot 保持不變 |
| C15 | 初次匯入期間使用者更新原檔 | 保留原檔，指出未涵蓋差異，唔聲稱最新版本已全部轉移 |
| C16 | 不同次 capture 寫入同類資料 | 遵從同一份 `LIBRARY.md`；schema、source refs、catalog 及 IDs 格式一致 |
| C17 | 主結論已可用，只新增未驗證跨框架延伸 | 保持適當 topic 狀態，該段獨立標明未驗證 |
| C18 | 相同 payload，只有匯入時間或外部原路徑改變 | 經確認同一來源身份後重用 snapshot，唔因管理 metadata 製造新內容版本 |

## 12. 三輪自我 review 紀錄

本節記錄同一位設計者嘅三輪設計檢查，唔係獨立第三方審查或已安裝 skill 嘅測試結果。

### 第一輪：使用者需求及責任邊界

發現：早期設計長期依賴 project coding reference，亦曾把 report-generation skill 拉入必要流程。

修正：Library 承接全部知識；舊檔只作首次來源且保留不動。既有 report 作資料證據，capture 不依賴 report-generation skill。

發現：正常「收錄」同首次「轉移全部」容易混淆。

修正：分開正常收錄與完整匯入模式；完整匯入需要逐項 mapping，正常收錄只處理指定主題。

### 第二輪：用實際情境逐步推演

發現：每次收錄都跑 Git／tests 過重；只有討論亦值得保存；一份 HTML 唔一定係 report。

修正：按輸入來源決定查證深度，證據標示到段落；report 與獨立圖解分別登記，一個 topic 可連多份來源。

發現：靠同名去重會合併錯案例；同名 MD／HTML 亦未必一致。

修正：以問題、技術條件、來源身份與內容判斷；分開 report 更新、其他 framework 案例及純解釋補充。

### 第三輪：資料壽命、失敗恢復及配套一致性

發現：只連 project 原路徑，日後搬 project 就可能斷；共用同名 CSS 可能改變舊 report 外觀。

修正：提出 scoped source snapshot 預設，保留原檔與來源資訊；相對依賴成套保存，唔跨案例覆寫 CSS。

發現：舊 status-sync workflow 仍可能寫 coding reference；catalog 可漏登；中途中斷可製造假完成。

修正：列明外部整合點、topics fallback、完成核對與重試規則。Library root、相對路徑基準及證據語義與 guide 設計一致。

再核對後補充：Snapshot 去重包含 assets；匯入日期同歷史 code／測試基準分開。原檔於匯入期間由使用者更新時，需要回報差異而唔回復原檔；record state 要有實際理由及替代位置。

## 13. 交俾 ChatGPT 嘅審閱重點

1. Scoped source snapshot 係咪比外部連結更符合跨 project 自足閱讀？額外儲存／版本維護成本是否值得？
2. Topic 粒度係咪保留足夠原始理解，又避免重複整份 report？
3. 初次轉移 mapping 是否足以發現遺漏，尤其 code 例子、限制及 project 特定背景？
4. Capture 同 guide 嘅路徑、來源、證據狀態與更新責任有冇矛盾？
5. 明確收錄意圖嘅觸發規則，有冇錯把普通討論或 review 當成寫入命令？

本設計未證明搜尋品質、實際路徑權限或 runtime skill 選擇效果。正式實作後應用上述情境驗收，而唔只依賴 frontmatter 格式檢查。

## 14. 本輪 feedback 修訂與待確認事項

- 共用格式移至 `LIBRARY.md` 草案，補齊可被解析嘅 topic frontmatter、來源、索引及識別規則。
- 澄清 topic 狀態同段落證據，局部不確定唔自動影響整篇。
- 保留 scoped source snapshots；fingerprint 依實際 payload／assets 計算，唔混入匯入時間。
- Capture 輸出連結同樣跟隨 guide G18 嘅實際 click 驗收，唔自行定義另一格式。
- Library 寫入、catalog 維護、原始 coding reference 保留及 report skill 無耦合嘅邊界不變。

原三輪 review 紀錄係先前設計歷程；本節記錄後續修訂。呢次只更新設計，schema 同 library 位置等仍待使用者最終確認，未初始化 global library 或執行匯入。

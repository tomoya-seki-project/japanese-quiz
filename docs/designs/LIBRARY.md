# Learning Library 共用格式草案

狀態：設計階段、待使用者最終確認。此檔位於 `docs/designs/` 供審閱，唔代表 global library 已建立，亦唔係技能指令。

配套：[Capture 設計](project-learning-capture-design.md)、[Guide 設計](project-learning-guide-design.md)。本檔係兩份設計共用嘅唯一格式規格；修改格式時改本檔，兩個 skill 只引用，唔各自複製一套 schema。

## 1. V1 範圍與位置

資料由 Markdown、既有 HTML、必要 assets 同普通檔案索引構成。無 database、embedding、背景同步、locking system 或必須生成 HTML 嘅要求。

建議 global root 為 `/home/seki/.codex/learning-library/`，仍待確認；正式位置在安裝時一次配置，兩個 skill 共用，唔以 cwd 推斷。將來本檔部署到選定 root，該份先係運作中規格；目前只係提案。

`schema_version: 1` 係文件格式版本，唔係程式語言版本或知識正確性版本。Capture 遇到不支援嘅 schema 唔自行轉換／覆寫；guide 可以讀明確可理解嘅正文並交代格式限制，唔猜測未知欄位。

## 2. 基本格式與路徑

- Topic、source manifest 同 import mapping 使用 UTF-8 Markdown；metadata 只放檔案開頭 `---` 圍住嘅 YAML frontmatter。
- YAML 只使用 mappings、arrays、strings、integers、null；唔用自訂 tags、anchors／aliases 或 duplicate keys。日期／時間與版本字串加引號，避免被 parser 自動轉型。
- 每類 metadata 都用下文指定欄位；未列出嘅欄位唔自行新增。有擴充需要時先明確更新共用契約。
- 必填 array 可以係 `[]`；未知 version／commit 等用指定 `null`，唔用空字串、`latest` 或杜撰值代替。
- Generated IDs 使用 lowercase ASCII kebab-case，符合 `^[a-z0-9]+(?:-[a-z0-9]+)*$`，長度 1–96；topic ID 全庫唯一且建立後穩定，分類搬位唔改 ID。
- 新 ID 先查相同身份；slug 已被不同項目用咗，加入有意義限定詞，仍撞名先用 `-2`、`-3` 等最小未用後綴。唔把舊 anchor ID 強制改寫成新身份；原 ID 留喺 migration mapping。
- Library 內 metadata 路徑一律以 library root 為基準，使用 `/`，不得有前置 `/`、空 segment、`.`、`..`、反斜線、NUL、CR 或 LF。唔把 fragment 混入 path。
- 正文 Markdown links 遵從檔案所在目錄嘅相對路徑語義；呢個同 metadata 嘅 root-relative path 分開處理。
- `external-file` 明確使用絕對本機路徑；`url` 使用明確 HTTP(S) URL。兩者都唔當成 library 內可攜來源。
- 使用本機檔案前解析並確認實際目標；唔依賴同名檔案或 VS Code 選中嘅 root。

## 3. Topic YAML frontmatter

以下 JSON Schema 係 topic frontmatter 解析成資料後嘅機器可讀規格。只驗證 frontmatter；跨檔案存在性、ID 唯一性、語義條件及正文證據另依後文驗收。

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Learning Library Topic v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "id", "title", "aliases", "technologies", "record_state", "updated_at", "source_refs"],
  "properties": {
    "schema_version": {"const": 1},
    "id": {"$ref": "#/$defs/id"},
    "title": {"$ref": "#/$defs/text"},
    "aliases": {"type": "array", "uniqueItems": true, "items": {"$ref": "#/$defs/text"}},
    "technologies": {"type": "array", "uniqueItems": true, "items": {"$ref": "#/$defs/technology"}},
    "record_state": {"enum": ["active", "needs-review", "superseded"]},
    "updated_at": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"},
    "state_reason": {"$ref": "#/$defs/text"},
    "superseded_by": {"type": "array", "minItems": 1, "uniqueItems": true, "items": {"$ref": "#/$defs/id"}},
    "source_refs": {"type": "array", "uniqueItems": true, "items": {"$ref": "#/$defs/sourceRef"}}
  },
  "allOf": [
    {
      "if": {"properties": {"record_state": {"enum": ["needs-review", "superseded"]}}},
      "then": {"required": ["state_reason"]}
    },
    {
      "if": {"required": ["superseded_by"]},
      "then": {"properties": {"record_state": {"const": "superseded"}}}
    }
  ],
  "$defs": {
    "id": {"type": "string", "minLength": 1, "maxLength": 96, "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"},
    "text": {"type": "string", "minLength": 1},
    "technology": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "kind", "scope", "version"],
      "properties": {
        "name": {"$ref": "#/$defs/id"},
        "kind": {"enum": ["language", "framework", "library", "database", "tool"]},
        "scope": {"enum": ["required", "example"]},
        "version": {
          "oneOf": [
            {"type": "null"},
            {
              "type": "object",
              "additionalProperties": false,
              "required": ["value", "basis", "evidence"],
              "properties": {
                "value": {"$ref": "#/$defs/text"},
                "basis": {"enum": ["observed", "declared", "reported"]},
                "evidence": {"$ref": "#/$defs/text"}
              }
            }
          ]
        }
      }
    },
    "sourceRef": {
      "type": "object",
      "additionalProperties": false,
      "required": ["location", "kind", "path"],
      "properties": {
        "location": {"enum": ["library", "external-file", "url"]},
        "kind": {"enum": ["report", "illustration", "note", "code", "documentation"]},
        "path": {"$ref": "#/$defs/text"},
        "section": {"$ref": "#/$defs/text"},
        "fragment": {"$ref": "#/$defs/text"},
        "snapshot_manifest": {"$ref": "#/$defs/text"}
      },
      "allOf": [
        {
          "if": {"required": ["snapshot_manifest"]},
          "then": {"properties": {"location": {"const": "library"}}}
        }
      ]
    }
  }
}
```

補充語義約束：

- 所有 text 必須去除首尾空白後仍非空；時間係真實有效 UTC 日期／時間。
- `aliases` 係字串 list，保存中英文術語、使用者講法及症狀；唔強制固定數量。
- `technologies.name` 使用統一 slug，例如 `python`、`django`、`cpp`、`csharp`、`aspnet-core`；唔按目錄名推斷。
- `scope: example` 表示來源例子使用，唔代表其他語言不適用；`required` 表示該 entry 嘅核心做法依賴該技術。混合條件在正文解釋。
- `version: null` 表示未確認；唔代表跨所有版本。非 null 嘅 `value` 保存實際觀察／宣告／來源記載字串，可係 exact version 或原始 constraint；`basis` 分別表示已觀察安裝版本、依賴宣告、歷史來源記載。`evidence` 指明取得版本嘅文件／位置，唔把 declared range 當實際安裝版本。
- `source_refs.path` 指向實際資源，唔只指目錄。`section` 係人類可讀章節名稱；`fragment` 係已存在嘅 anchor ID，不含 `#`。
- 指向 `sources/` 快照 payload 嘅引用必須帶 `snapshot_manifest`，值為該快照 `SOURCE.md` 嘅 root-relative path；目標檔案必須列喺該 manifest。其他來源省略該欄位。
- `superseded_by` 只列存在且不同於自身嘅 topic ID，唔得形成替代循環。無一對一替代時可以省略，但 `state_reason` 要交代。
- Source list 可以空，尤其係對話筆記；正文仍需說明來自本次討論、未實作等身份，唔捏造外部文件連結。

完整合法嘅 frontmatter 示例（純示意筆記，唔聲稱係已匯入案例）：

```yaml
---
schema_version: 1
id: bottom-up-dp
title: "Bottom-up DP：先計算依賴狀態"
aliases: ["動態規劃", "填表順序", "重複子問題"]
technologies:
  - name: python
    kind: language
    scope: example
    version: null
record_state: active
updated_at: "2026-09-12T00:00:00Z"
source_refs: []
---
```

正文要記錄呢份係概念筆記，唔係已完成實作；日期喺實際收錄時使用真實值。

## 4. Record state 同段落證據

| 值 | 意義 |
|---|---|
| `active` | 整篇主結論可作目前參考；仍須依正文條件判斷，唔表示全部內容經測試 |
| `needs-review` | 未解問題影響主結論或安全重用；`state_reason` 必填，正文指出受影響範圍 |
| `superseded` | 該 entry 已被替代或唔再作目前主要入口；保留歷史用途及替代理由 |

局部不確定唔自動令整篇 `needs-review`。例如 Django 主案例有依據，最後一段其他 framework 延伸未驗證，就喺該段標明「未實作／未驗證」，唔貶低整份 reference。

段落證據保留為正文，說明來源 report 記載、今次 code inspection、實際測試、使用者陳述或未實作討論；需要時指向 `source_refs` 對應資源與章節。唔建立單一 `verified` boolean。

`updated_at` 只係知識文件內容修改時間。完全重複收錄唔改時間；來源測試日期、匯入時間同 code 基準分開保存。

## 5. Scoped source snapshots

目錄固定為 `sources/<project-id>/<source-id>/<snapshot-id>/`。Project 同 source ID 遵從基本 ID 規則並保持穩定；來源改名或搬位唔自動改身份。`project-id` 係 library 內來源身份，唔只用 repository basename 推斷；已有身份優先沿用，有歧義先核對。

Snapshot 內保存 payload（例如 MD、HTML、CSS、圖片）同一份管理文件 `SOURCE.md`。原資料樹嘅必要相對關係保持可用；管理文件名保留，遇原檔同名衝突要明確重排及記錄，唔覆寫內容。

`SOURCE.md` YAML metadata 欄位如下；表內以外欄位唔自行添加：

| 欄位 | 必填 | 型別／規則 |
|---|---|---|
| `schema_version` | 是 | Integer，固定 `1` |
| `project_id` | 是 | 已分配 project ID，等於目錄身份 |
| `source_id` | 是 | 已分配 source ID，等於目錄身份 |
| `snapshot_id` | 是 | 依下一節計算 |
| `imported_at` | 是 | UTC string，與 topic `updated_at` 相同時間格式 |
| `original_path` | 是 | 匯入來源根目錄嘅絕對路徑，或未知時 `null` |
| `repository_identity` | 是 | 已知來源識別說明 string 或 `null`；唔收錄含 credential 嘅 URL |
| `commit` | 是 | 已核實 Git commit ID string 或 `null` |
| `worktree_state` | 是 | `clean`、`dirty`、`untracked`、`not-applicable` 或 `unknown` |
| `content_fingerprint` | 是 | `sha256:` 加完整 64 位 lowercase hex |
| `files` | 是 | 非空 object array，元素見下表 |

每個 `files` 元素只使用：

| 欄位 | 必填 | 型別／規則 |
|---|---|---|
| `path` | 是 | Snapshot-root-relative payload 路徑，符合內部相對路徑規則，唯一 |
| `sha256` | 是 | 該檔原始 bytes 嘅 64 位 lowercase SHA-256 hex |
| `kind` | 是 | `report`、`illustration`、`note`、`code` 或 `asset` |

Manifest 正文保存原 report 基準／限制、路徑重排或遮蔽說明，以及必要嘅來源背景。唔假定 manifest 嘅 `commit` 已包含工作目錄或未追蹤內容；來源報告基準與今次匯入 code 狀態不同時在正文分開講清楚。

Scope 只包括已選相關來源與必要本機依賴，唔跟隨每條外部 hyperlink 匯入整個網站。以 snapshot 保存嘅來源保持歷史身份；多個 topic 可引用同一 snapshot。無背景同步、唔覆寫舊 snapshot。

## 6. Fingerprint 與 snapshot ID

演算法固定為 SHA-256，使用完整 digest，唔以截短值判斷身份。

1. `files` 只列實際收錄嘅 payload，包含 HTML、MD 及必要 CSS／圖片等；唔包括管理文件 `SOURCE.md`、catalog、topic、匯入時間或原始絕對路徑。
2. 每個 payload 檔案以原始 bytes 計 SHA-256。唔轉換 newline、編碼、Unicode 或空白。
3. 以 snapshot-relative path 嘅 UTF-8 bytes 升序排列；路徑區分大小寫，不做 Unicode normalization。讀寫環境有名稱衝突時先解決，唔靜默合併。
4. 每個檔案形成一行：`<64位lowercase檔案hash><兩個ASCII空格><相對path><LF>`。因 path 不含 CR／LF、hash 固定長度，行格式可明確解析。
5. 將排序後各行串接成 UTF-8 bytes，對串接結果計 SHA-256，得到 bundle digest。
6. `content_fingerprint` 為 `sha256:<bundle-digest>`；`snapshot_id` 為 `s-<bundle-digest>`。

同來源身份下，payload 及內部路徑完全相同就得到相同 snapshot ID；只有 imported time／外部原路徑改變唔影響 digest。CSS／圖片改變即產生新 digest。Metadata 不參與內容 digest，來源身份由上層 project/source namespace 保留，唔因兩個 project 有同一 CSS 就合併來源。

已存在同 ID 時核對完整 manifest／payload，再重用；若同 ID 卻內容不一致，視為資料完整性問題，停止該項寫入，唔覆蓋。管理 metadata 如需修正，以明確維護請求記錄更正，唔假扮成新內容快照。

## 7. 首次 import ID 與 mapping

完整匯入 coding reference 嘅目錄為 `imports/<project-id>-coding-reference/<import-id>/`。

- `original.md` 保留該次來源原始 bytes；project 原檔保持原樣，由使用者自行刪除。
- `import-id` 固定為 `i-<SHA-256(original.md原始bytes)>`，使用完整 lowercase hex。
- 同一 project 同一來源版本重試重用同 ID，唔因重試時間不同建立新副本。
- 來源內容改變產生另一 import ID，需根據 mapping 與現有 topics 合併，唔重複創建所有 entry。

`mapping.md` frontmatter 只使用以下必填欄位：`schema_version`（固定 integer 1）、`project_id`（ID）、`import_id`（以上規則）、`imported_at`（UTC string）、`original_path`（來源絕對路徑）、`original_sha256`（完整 lowercase hex）。

正文包含固定 Markdown table，欄名與順序係 `source_entry | targets | disposition | coverage | notes`：

- `source_entry`：原 anchor／entry ID；無 ID 時用 `section-0001` 順序身份配合原標題。
- `targets`：JSON string array，每個值為新 topic 嘅 library-relative path；唔用手工逗號分隔。
- `disposition`：`copied`、`split`、`merged` 或 `placeholder`。
- `coverage`：`pending` 或 `checked`；notes 說明重要內容落點與拆合理由。
- Table cell 避免 literal `|` 及換行，必要時用 HTML entity／文字描述。原始內容仍可由 `original.md` 查閱。

檔案保存成功唔等於 coverage checked；全部實質章節有實際核對及落點後，先可宣告完整轉移。原檔在匯入期間有改動就報告基準差異，唔回復或刪除原檔。

## 8. catalog.md 唯一 entry 格式

Catalog 使用 Markdown 標題，下面只有一個 `yaml` fenced block 作機器資料區；唔同時維護另一份 Markdown table 或 JSON 索引。

```yaml
schema_version: 1
entries:
  - id: bottom-up-dp
    title: "Bottom-up DP：先計算依賴狀態"
    aliases: ["動態規劃", "填表順序", "重複子問題"]
    technologies:
      - name: python
        kind: language
        scope: example
        version: null
    record_state: active
    path: topics/algorithms/bottom-up-dp.md
```

根 mapping 只容許 `schema_version`（固定 1）同 `entries`（array，可空）。每個 entry 恰好包含示例六個欄位，唔另加摘要、測試結果或 source list。

除 `path` 外各欄位必須直接等於對應 topic frontmatter 同名值，型別亦沿用 topic schema。`path` 係實際 topic 檔案嘅 library-root-relative path。Entries 按 ID ASCII 升序，ID 同 path 各自唯一；alias list 保留 topic 中原順序。Catalog 係搜尋投影，topic 先係內容依據。

Capture 維護相關 entry；guide 只查閱，唔修復。Catalog 缺失、格式壞掉或有已知漏項時，guide 可按具體線索搜尋 topics，唔每次無命中都全庫掃描。

索引可用唔代表每題都要讀。Guide 先按其設計中嘅觸發條件、使用者請求同目前對話決定需唔需要查閱；呢個判斷唔預先讀 catalog 或本格式文件。同主題已讀內容可沿用。Capture 嘅收錄查重仍按明確寫入任務需要執行，唔受 guide 跳過簡單問題嘅規則影響。

## 9. 本機 HTML 連結契約：待 G18 驗收

內部 source path 嘅機器格式已在本草案定義；對話 UI 點擊用嘅連結表示法仍未確認，兩者唔混為一談。

實作時喺目標 VS Code Codex chat 測試當前規則允許嘅格式，先試絕對檔案路徑 Markdown link。唔使用目前回覆規則禁止嘅 `file:///`。Workspace-relative 格式只在環境容許而且可證明跨 root 正確時先考慮。

G18 要記錄：實際環境版本、採用表示法、library 外置於 project 嘅目標檔案、multi-root 同名檔案測試、點擊後係 editor 原始碼或預覽、是否正確定位。唔由 skill 自動開 browser／server。

實際點擊通過後先在運作中 `LIBRARY.md` 登記選定格式。未能操作 UI 時標 pending；`exists()`／路徑檢查唔等於點擊驗收通過。本文未登記任何已通過格式。

## 10. 一致性與實作後驗收

1. Topic frontmatter 能被 YAML parser 解析，符合內嵌 JSON Schema 同語義規則；未知欄位、重複 key 及錯誤型別可識別。
2. 每份 catalog entry 等於對應 topic 投影；guide 對故意漏項保持唯讀。
3. 相同 payload 更換匯入時間得到同一 fingerprint；單改 CSS／圖片得到不同 fingerprint。
4. 同來源重複 capture 重用 snapshot；不同來源身份不因同內容而失去 provenance。
5. `source_refs` 正確解析 library／external／URL，source payload 在所指 manifest 內，沒有跨 root 誤解。
6. 一篇主結論可用但有未驗證小段落仍可 `active`；影響主要安全重用時才 `needs-review`。
7. Import 每個原 entry 有可核對 mapping；original bytes 與使用者原檔保留規則成立。
8. G18 實際點擊後才確定 UI 連結契約。

目前只完成格式設計，未建立 parser、validator、capture／guide skill 或 global library。實作時驗證以上行為；唔為 V1 加入 database、排程或複雜多 agent 工作流。

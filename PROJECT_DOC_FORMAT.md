# Project Documentation Format

呢份文件記錄本 project 目前採用嘅 documentation / TODO 格式規則。  
之後其他 project 可以直接參考呢套格式，避免 TODO、history、learning notes 混埋一齊。

## 三份主要文件角色

Project 主要使用三份 markdown 文件，各自負責唔同層面。

| 文件 | 角色 | 應該記錄 | 唔應該記錄 |
| --- | --- | --- | --- |
| `TODO.md` | Project status / task tracking | Bug、未完成 feature、已完成 decision、改良、擴展預想 | 純 learning note、已更新某份 doc 呢類 meta 操作 |
| `LEARNING_POINTS.md` | 個人學習 / review 筆記 | 未理解清楚嘅概念、Django/Python pattern、之後想複習嘅解釋 | Project 完成度、task status、每日進度 |
| `PROJECT_HISTORY.md` | Project 里程碑 / 技術決策紀錄 | 重要功能完成、架構改動、database schema 改動、主要取捨、commit | 細碎 wording cleanup、普通 TODO update、單純 learning note 更新 |

簡單分工：

```text
TODO.md             = 而家仲有咩要做 / 咩已完成
LEARNING_POINTS.md  = 我學過咩 / 仲有咩概念想之後複習
PROJECT_HISTORY.md  = project 重要階段發生過咩事
```

## TODO.md 格式

`TODO.md` 主要負責記錄 project 本身嘅待辦、bug、flow 狀態、已完成 decision 同將來可做嘅功能。  
唔需要記錄「已寫入 learning notes」呢類 meta-doc 操作。

## 目錄

`TODO.md` 頂部要有目錄，並用 markdown link 直接跳去各大 tag。

例子：

```md
## 目錄

- [待 Fix Bug](#待-fix-bug)
- [Vocab Future Work](#vocab-future-work)
- [VocabRequest Result / UserVocab Flow](#vocabrequest-result--uservocab-flow)
- [Account Email Activation](#account-email-activation)
- [Event Notification System](#event-notification-system)
- [Data Import / Export / Database Migration](#data-import--export--database-migration)
- [User Message to Admin](#user-message-to-admin)
- [Quiz Question Logic](#quiz-question-logic)
- [Logging / Audit Trail](#logging--audit-trail)
- [UI / UX](#ui--ux)
```

## 大 Tag

大 tag 用嚟分 project area，例如：

- 待 Fix Bug
- Vocab Future Work
- VocabRequest Result / UserVocab Flow
- Account Email Activation
- Event Notification System
- Data Import / Export
- User Message to Admin
- Quiz Question Logic
- Logging / Audit Trail
- General Improvements
- UI / UX

大 tag 底下再放 sub tag。

## Sub Tag 狀態

Sub tag 用嚟記錄大題目下面某一個具體 flow、feature、bug、改善項目。

狀態固定使用三種：

```text
DONE
WORKING
TODO
```

建議寫法：

```md
> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Category multiple selection**

> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Event notification read / history**

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Word slug generation**
```

### 狀態顏色

| Status | Color | Background | 用途 |
| --- | --- | --- | --- |
| DONE | `#ffffff` | `#1b5e20` | 核心功能已完成，或已有明確 decision |
| WORKING | `#ffffff` | `#e65100` | 已開始處理，但仍有必要項目未完成 |
| TODO | `#ffffff` | `#0d47a1` | 未開始或暫時只係計劃 |

用深色背景 + 白字，避免淡色 badge 要望清楚先分到狀態。  
不用紅色做 TODO，避免 TODO 看起來像 error / urgent。

### Status 判斷規則

- 有 `已完成`，而且無 `未完成`，只剩 `改良` / `擴展預想`：用 `DONE`。
- 有 `已完成`，同時仲有 `未完成`：用 `WORKING`。
- 只有 `未完成`，未有實質完成內容：用 `TODO`。

例子：

```text
DONE    = 已 work / 已決定 / 核心完成，可以有改良
WORKING = 已開始，有部分完成，但核心目標未完成
TODO    = 未開始，或暫時只係計劃
```

## Sub Tag 內容結構

每個 sub tag 可以按需要包含以下 section：

```md

<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- 已經完成 / 已測試 / 已有明確 decision 嘅內容。


<p style="margin-left:1.5em;"><strong>未完成</strong></p>

- 呢個 sub tag 要真正完成前仍然必須處理嘅事項。


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- 將來可行、適合目前學習程度或 project 方向嘅擴展功能。
- 不影響目前核心完成度。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 核心已完成，但之後可以寫得更好、更穩、更清楚或更好維護嘅地方。
```

如果某個 section 無內容，可以省略。  
例如一個完成度高嘅 sub tag 可以只有 `已完成` 同 `改良`。

## 未完成 vs 改良 vs 擴展預想

三者要分清楚：

- `未完成`：會影響該 feature / flow 是否真正完成。
- `改良`：已經 work，但之後可以優化。
- `擴展預想`：唔係目前 scope，只係將來可能加。

例子：

```md
> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Vocab sync summary event**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Login 後會 sync vocab changes。
- User detail page 會作為 refresh point。
- 已測試 create / update / restore / delete / import 後 event summary 正常生成。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 將來如資料量變大，可以再優化 query performance。


<p style="margin-left:1.5em;"><strong>擴展預想</strong></p>

- 之後可以加入 event importance level 或 target user group。
```

## Bug Fix 編號

「待 Fix Bug」或已 check 到嘅重要 bug / logic risk 使用數字排序。

例子：

```md
> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **第 1 點（VocabRequest / Admin Review）：Permission boundary**
```

規則：

- Bug / 必要 fix 用 `第 X 點`。
- 數字按發現或整理順序排列。
- 如果已完成，狀態改為 `DONE`，但保留原本編號，方便回溯。

## General Improvements 編號

`General Improvements` 使用英文字母排序。

例子：

```md
> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **改善 A：Model `__str__()`**

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **改善 B：Add tests**
```

規則：

- 改善項目用 `改善 A`、`改善 B`、`改善 C`。
- 去到 `改善 Z` 後，用 `改善 AA`、`改善 AB`。
- 如果某改善項目已完成，狀態改為 `DONE`，但保留原本字母。

## UI / UX 分類

UI polish、wording、layout、顏色、版面整理等內容應集中放喺 `UI / UX`。

除非 UI 問題會直接影響 logic flow，否則唔應散落喺其他 feature / event / vocab tracking 入面。

例子：

```md
> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Event notification page UI / wording polish**


<p style="margin-left:1.5em;"><strong>已完成</strong></p>

- Event list / detail 已可以顯示需要嘅資料，足夠支援整體 logic flow 測試。


<p style="margin-left:1.5em;"><strong>改良</strong></p>

- 之後可以整理 layout、read/unread visual state、wording 同 notification summary。
```

## Learning Notes 分工

`LEARNING_POINTS.md` 只係個人學習 / review 筆記，唔係 project status tracking。

因此：

- `TODO.md` 唔需要寫「已加入 LEARNING_POINTS」。
- `PROJECT_HISTORY.md` 唔需要記錄普通 learning note 更新。
- 如果某個 learning point 牽涉 project decision，TODO 只記 decision 本身，唔記「文件已更新」。

## LEARNING_POINTS.md 格式

`LEARNING_POINTS.md` 用嚟保存自己學習過程中覺得需要回頭複習嘅概念。  
內容可以比 TODO 更解釋性，重點係之後自己睇得明，而唔係 tracking project progress。

## LEARNING_POINTS.md 目錄

文件頂部要有目錄，並用 markdown link 跳去每個 learning tag。

例子：

```md
## 目錄

- [DJANGO-CBV-OBJECT-ID](#DJANGO-CBV-OBJECT-ID)
- [DJANGO-POST-SAVE-SIGNAL-CREATED-GET-OR-CREATE](#DJANGO-POST-SAVE-SIGNAL-CREATED-GET-OR-CREATE)
- [DJANGO-DATETIME-LOCALTIME-ADMIN-FORMAT](#DJANGO-DATETIME-LOCALTIME-ADMIN-FORMAT)
```

## Learning Tag 命名

Learning tag 使用大寫英文 + hyphen，並用 topic prefix 分類。

例子：

```text
DJANGO-CBV-OBJECT-ID
DJANGO-ADMIN-GET-FORM-BASE-FIELDS
DJANGO-QUERYSET-SUBSET-ORDERING
PYTHON-SET-DIFFERENCE-CSV-HEADERS
HTML-JS-CHECKBOX-SELECT-ALL
DOMAIN-VOCAB-USERVOCAB-IN-USE
```

常用 prefix：

- `DJANGO-`
- `PYTHON-`
- `HTML-JS-`
- `DOMAIN-`
- `SQL-`

## Learning Tag 結構

每個 learning tag 使用 checkbox heading，方便之後自己 mark 已理解。

例子：

```md
<a id="DJANGO-CBV-OBJECT-ID"></a>

## [ ] `[DJANGO-CBV-OBJECT-ID]` Detail / Update / Delete View 點樣取得目標 Object

### 問題背景

- 當時點解會有呢個疑問。
- 喺 project 邊個 flow / file 遇到呢個問題。

### 研究方向

- 之後想查咩 keyword。
- 概念上要理解邊幾件事。

### 你的解答

- 用自己聽得明嘅方式寫清楚答案。
- 可以放簡短 code example。

### 理解內容

- 自己最後吸收咗咩。
- 日後遇到類似問題時要點諗。
```

Section 定義：

- `問題背景`：點解會問呢個問題。
- `研究方向`：之後想深入查 / 要理解嘅方向。
- `你的解答`：目前整理出嚟嘅答案。
- `理解內容`：用自己語言濃縮重點，方便之後複習。

## LEARNING_POINTS.md 使用規則

- 可以寫得比 TODO 詳細，因為目標係幫自己重新理解。
- 可以記 project 入面真實遇到嘅例子，但唔需要追蹤 task 完成度。
- 如果一個概念未完全明，可以保留 `[ ]`；理解後再手動剔。
- 唔需要每次更新 learning note 都寫入 `PROJECT_HISTORY.md`。
- 唔需要喺 `TODO.md` 寫「已加入 learning point」。

## Project History 分工

`PROJECT_HISTORY.md` 用嚟記錄 project 重要階段、架構決策、data model 改動、主要 flow 完成、重要取捨。

不應記錄太細碎嘅操作，例如：

- 普通 wording cleanup
- 小型 comment grammar cleanup
- 單純更新 TODO / Learning Points
- 無影響 project flow 嘅 formatting 改動

除非係大規模 documentation pass 或建立正式 documentation system，先需要寫入 project history。

## PROJECT_HISTORY.md 格式

`PROJECT_HISTORY.md` 應該按日期由舊到新記錄 project 重要進展。  
每一筆記錄應該偏向「project 層面發生咗咩」，而唔係流水帳。

建議格式：

```md
## YYYY-MM-DD - Short Title

Commit: `abc1234`

Status: 一句講清楚呢個階段完成咗咩，或者目前狀態係咩。

### 主要改動

- 重要功能 / flow / service / admin / command 改動。

### Database 改動

- 新增 / 修改 / 移除 model field。
- Migration 名稱。
- 無 schema 變更時可以寫「無新增 schema 變更」。

### 技術重點

- 今次實作上最重要嘅技術點。
- 架構分工、transaction、query、admin flow、service layer 等。

### 理由

- 點解要咁設計。
- 做咗咩取捨。

### 學到咩

- 今次真正學到 / 之後值得記住嘅 project-level lesson。
```

## PROJECT_HISTORY.md 記錄準則

應該記錄：

- 新 app / major feature foundation。
- 主要 workflow 完成，例如 vocab request approve/reject、event sync flow。
- Database schema 改動，例如新增 model、M2M、重要 field。
- Service layer 或 admin flow 嘅重要設計決策。
- 大型 refactor 或 migration。
- 一次完整 testing / review 後確認某個主要系統已穩定。

唔應該記錄：

- 單純更新 `TODO.md`、`LEARNING_POINTS.md`。
- 普通 typo / grammar / wording cleanup。
- 小型 comment cleanup。
- 單行 import 清理。
- 未影響 project 行為嘅 formatting。

如果一件事只係「幫自己理解」，放 `LEARNING_POINTS.md`。  
如果一件事係「project 仲要做 / 已做」，放 `TODO.md`。  
如果一件事係「project 重要階段 / 技術決策」，放 `PROJECT_HISTORY.md`。

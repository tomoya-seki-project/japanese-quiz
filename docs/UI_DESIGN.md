# Japanese Quiz UI — Confirmed Design Specification

## 1. Document Purpose

This document is the primary implementation specification for the current UI. It consolidates:

- The complete page and interaction requirements from `UI-design.md`
- The confirmed button sizing rules from `button-design.md`
- Implementation review results from `wireframe-review.md` through `wireframe-review_ver4.md`

The original `UI-design.md` retains the design process, alternative proposals, and preview history. This document contains only the currently valid requirements, confirmed specifications, version scope, and unresolved items.

### 1.1 Specification Priority

1. Confirmed specifications in this document
2. Explicit page-specific exceptions
3. Existing previews, as visual references only
4. Older reviews and the original `UI-design.md`, for historical traceability only

If a preview conflicts with this document, this document takes precedence.

### 1.2 Version Scope

v1.0.0 includes:

- Account, Vocab, User Vocab, Event, and Feedback
- Non-Multiple-Choice Quiz
- Quiz Summary, No-question, and No-pool states
- 400, 403, 404, and 500 pages
- The development-only UI confirmation page

Post-v1.0.0 scope:

- Multiple Choice Quiz
- Admin Event Create
- Event-reading behavior that affects only the current page and allows reverting an event to unread
- Additional features without current backend or model support

---

## 2. Language and Copy

- Every site page outside Django `/admin/` uses Japanese UI copy.
- Admin-only custom site pages also use Japanese.
- Django `/admin/` retains its current language; do not add extra conversion logic.
- Development and diagnostic UI, such as `判定詳細`, also uses Japanese field labels.
- UI copy must follow the text specified in this document and must not revert to old template text.

---

## 3. Global Layout System

### 3.1 App Shell and Active Area

- Center all primary UI within the viewport.
- The centered region is the app shell.
- The app shell is 100% wide, has a maximum width of 540px, and is horizontally centered.
- When the viewport is wider than the app shell, only the background appears outside it.
- The app shell is not a visible outer frame; pages must not wrap all content in one large card.
- The usable region after subtracting the page's horizontal spacing is the active area.
- Percentage-based element widths are calculated from the active area, not the browser viewport.
- The minimum officially supported width is 320 CSS px.
- At 320px and above, the page must not produce horizontal scrolling.

### 3.2 Fixed and Scrollable Regions

A standard page uses:

1. A fixed header
2. An independently scrollable content area
3. A fixed footer action bar when actions are present

On list pages, only the actual list area scrolls. The header, filter or table header, footer actions, and pagination remain fixed.

When the mobile browser address bar expands or collapses, recalculate the layout using dynamic viewport height. Fixed regions must not drift or overlap.

### 3.3 Header

- Keep the header inside the app shell with horizontal space on both sides.
- Use a solid near-white background, rounded corners, and a soft shadow.
- Standard height: 72px. Compact mode height: 60px.
- The centered page title uses 28px Zen Maru Gothic Bold.
- Reserve icon-control regions on both sides. Preserve empty space when a control is absent so the title remains truly centered.
- Header icon button: 48 × 48px. Icon: 28 × 28px.

### 3.4 Footer Action Bar

- Use a complete, solid near-white footer bar; buttons and pagination must not float directly on the kana background.
- Visual top and bottom padding must be equal.
- Add the mobile safe area only at the bottom; it does not count as visual padding.
- When actions and pagination share the footer, use two rows with one 14px gap and do not duplicate inner spacing.
- Keep the footer within the app shell; it must not expand indefinitely with the browser viewport.

### 3.5 Compact Mode

When viewport height is below 700px:

- Reduce header height from 72px to 60px.
- General button height may shrink from 58px to 50px, but never below a 44px touch target.
- Reduce footer visual vertical padding from 14px to 10px.
- Reduce vertical spacing between sections by about 20%.
- Do not reduce font sizes, input heights, or tappable widths.

### 3.6 Virtual Keyboard Input Mode

When a text input or textarea has focus and the mobile virtual keyboard is actually open:

- Temporarily hide the header and fixed footer.
- Scroll automatically so the focused field is fully visible above the keyboard.
- Restore the original layout and scroll position when the keyboard closes.
- Selects, switches, and selection buttons do not trigger this mode.
- This rule takes precedence over compact mode.

---

## 4. Spacing and Density

### 4.1 Vertical Padding

- Every non-button element must have equal top and bottom padding.
- The same component type must use the same vertical padding across pages.
- Different component types may use different values.
- At minimum, define separate values for:
  - Page header
  - Field or card
  - Single-line data row
  - List header or toolbar
  - List row
  - Badge or tag
  - Modal title, body, and actions
  - Footer
- Do not use fixed heights to create unused bottom space.
- Increase height only when content wraps.

### 4.2 Component Gaps

- Use consistent gaps between peer cards.
- Separate field rows within one card using dividers and consistent padding.
- Use a more prominent solid line and larger spacing between sections.
- Do not correct positioning with page-specific margin overrides.

---

## 5. Typography

### 5.1 Fonts

- General body copy, forms, tables, and data: Zen Maru Gothic.
- Page titles, modal titles, primary state titles, and primary buttons: Zen Maru Gothic Bold.
- Use Hachi Maru Pop only for short decorative text. The Homepage uses a logo image rather than a text wordmark.
- The Quiz kana keyboard, entered answers, and answer comparison may use the existing HGS Soei Kaku Pop-style PNG assets.
- Load fonts from local static assets rather than Google Fonts.
- Keep the OFL license with the font files.

### 5.2 Font Sizes

- Page title: 28px Bold.
- Field name: 20px Bold.
- Data, inputs, and body copy: 16px.
- Supporting text and `任意` markers: 13px.
- General primary button: 18px Bold.
- Homepage hero button: 28px Bold.

Wrap long titles first, then reduce their size incrementally. Do not clip them directly.

---

## 6. Color System

| Token | Value | Use |
|---|---|---|
| Ink | #26343D | Body copy and text on light buttons |
| Muted | #607783 | Dates, explanations, and placeholders |
| Paper | #F8FCFF | Cards, headers, and footers |
| Primary | #8BC9E6 | Primary actions |
| Selected | #BFE8F7 | Active selections and keyboard panel |
| Control | #EAF2F6 | Inputs and secondary actions |
| Tag / Metadata BG | #D2E5ED | Category tags and Feedback user/type frames |
| Line | #91ADBC | Dashed and soft dividers |
| Icon | #477A99 | Icons and darker lines |
| Success | #39765B | Correct, success, and replied states |
| Danger | #AD4B55 | Errors, incorrect states, and dangerous actions |
| Disabled BG | #D5DFE4 | Disabled controls |
| Disabled text | #687B85 | Disabled text |

- Cards use Paper at 90% opacity.
- Headers, footers, modals, and toasts use opaque backgrounds.
- Standard controls do not use a visible border.
- `focus-visible` uses an Icon-colored outline and a Selected-colored outer ring.
- Never communicate state by color alone; include text or an icon.
- Category tags and Feedback user/type frames use Tag / Metadata BG, not Control or Selected.

---

## 7. Background and Cards

### 7.1 Background

- General pages use the mixed kana tile.
- General-vocabulary Quiz questions use the hiragana tile.
- Katakana Quiz questions use the katakana tile.
- Quiz states without a current question type use the mixed tile.
- Fix the background to the viewport and repeat it seamlessly. Do not stretch it with `cover`.
- Prefer the 1600 × 1200 asset displayed at an 800 × 600 CSS size.
- If fixed backgrounds perform poorly in a particular mobile browser, allow a fallback that scrolls with the page.

### 7.2 Cards

- Paper at 90% opacity, with no visible border.
- Rounded cards with a `0 4px 12px` shadow using #26343D at 16% opacity.
- Background must remain visible between cards.
- Field and data cards use a consistent width based on the active area.
- Card height is determined by content plus standard padding.

### 7.3 Dividers

- Within one table or field group: a single #91ADBC dashed line.
- Use longer dashes rather than a dense dotted effect.
- Between sections or tables: a thicker #477A99 solid line with larger vertical spacing.
- Draw dividers only inside content frames.

---

## 8. Button System

### 8.1 Separate Size and Color

Every button must define both:

- A size type
- A semantic color variant

Color variants include Primary, Secondary, Danger, Selected, and Disabled. Do not create page-specific padding solely for colors such as Danger.

### 8.2 Homepage Hero Button

- 28px Bold.
- Padding: `.7em` vertically and `2em` horizontally.
- Content-based width.
- Highest visual hierarchy on the site.

### 8.3 General Primary Button

- 18px Bold.
- Base width: 50% of the active area.
- At least `2em` horizontal padding on each side.
- Short copy remains at 50% width.
- Longer copy may increase the width.
- If a single line would exceed 80% of the app shell, wrap the copy to two lines.
- After wrapping, recalculate from the longer line plus `2em` on each side.
- Final width must still be at least 50% of the active area.
- Handle exceptional copy exceeding two lines only when real copy exists.

### 8.4 Footer Button

- Preserve 8px vertical padding.
- One button in a row: 50% of the active area, centered.
- Multiple buttons in a row: divide the row evenly after subtracting the gap.
- Buttons in one row have equal width.
- DOM nesting must not determine button dimensions.

### 8.5 Selection Button

- Standard: 16px Bold, minimum height 44px.
- Standard padding: 8px on every side.
- Compact Level padding: 6px vertically and 2px horizontally.
- Every button in one selection group has the same size.
- Each field determines its own column count. Only Categories use at most three buttons per row.
- Full Category rows contain three buttons. A final row with one button is centered; a final row with two is left-aligned. Buttons retain the same width and do not stretch.
- Level uses six buttons in one row. Type, `in_use`, and question count each fill one row according to their option count.
- Selection-field frames use the existing 16px bottom padding for both top and bottom; do not add another 12px above the title.
- Event states `すべて／未読／既読` use the selection series, not primary-action sizing.
- Unselected: #91AAB7. Selected: #BFE8F7.
- Disabled and unselected must remain semantically distinct.

### 8.6 Pagination

- Every button is 44 × 44px.
- Current page uses Primary; unavailable directions use Disabled.
- Gap within each group: 6px.
- Left group: First, Previous.
- Center group: page numbers, centered on the true center of the active area.
- Right group: Next, Last.
- Disabled direction buttons retain their positions.
- With only one page, show only page number 1.
- Maximum visible page numbers follow these breakpoints. If the active area cannot fit direction controls, page numbers, and gaps, reduce the visible number count while preserving 44 × 44px controls and centering:
  - 480px and above: at most 5
  - 360–479px: at most 3
  - 320–359px: current page only

### 8.7 Icon Buttons

- Header icon control: 48 × 48px.
- Icon: 28 × 28px.
- Password visibility control: 44 × 44px.
- Icon-only controls require an accessible label.

### 8.8 Quiz-Specific Buttons

- Tips and Skip: preserve 18px text, 8px vertical padding, 16px horizontal padding, and a minimum height of 58px; both have equal width.
- `判定`: preserve 18px text, 8px vertical padding, 16px horizontal padding, and a minimum height of 44px.
- Kana key: 22px Bold; responsive size from 44px to 62px.
- The answer input surface is a full-width interactive card and does not use general action-button width.

---

## 9. Forms and Data Display

### 9.1 Field Card

- Place the field name and control in the same card.
- A standard single-line field places the label on the left and control on the right.
- When space is insufficient, move the label above the control.
- Login and Registration always use the vertical arrangement.
- Textareas always place the left-aligned label above the textarea.
- Show `任意` beside optional field labels.
- Do not show `必須` for required fields.

### 9.2 Controls

- Single-line inputs and selects are at least 44px high.
- Input text is right-aligned.
- Dropdown text is right-aligned with a separate vector arrow on the right.
- Textarea text is left-aligned.
- Word and kana inputs on Create and Update Request pages are equal width, targeting about 125% of their width before the enlargement request. Do not multiply by 125% again in every review.
- Keep the kana field name on one line. If the label and enlarged input do not fit side by side, move the label above while preserving the target input width within the frame.
- On wide viewports, align inputs to the right. On narrow viewports, use the full active-area width.
- Passwords are hidden by default and provide a visibility icon on the right.

### 9.3 Data Rows

- Normally place the label on the left and data on the right.
- For long data, place the label above on the left and data below on the right.
- Single-line username, email, and last-login rows use compact height.
- Separate rows within one table using dashed lines.
- On User Vocab Detail, `正解数`, `不正解数`, `連続記録`, `最後出題時間`, and `前回回答` use consistent vertical padding. The time toggle touch target must not increase that row's height.
- Read-only fields from the same model and semantic group may share a table card.

### 9.4 Validation Modal

- Show all errors at once in a centered modal.
- The backdrop blocks background interaction and scrolling.
- Keep the modal title and actions fixed; scroll the central error content only when it exceeds the maximum height.
- After closing:
  - Apply a Danger outline and label style to invalid fields.
  - Focus the first invalid field automatically.
- The backdrop and close button both close the modal.

### 9.5 Unsaved Data

Show a confirmation modal when leaving through Header Back, Home, or specified internal navigation on:

- User Vocab Detail
- Vocab Create, Update, and Delete Request
- Feedback Create and Reply

Copy and actions:

- Primary dangerous action: `破棄して移動`
- Secondary action: `キャンセル`
- Center the prompt

Do not use a browser-native unsaved-changes warning for refresh, closing the tab, or leaving the site directly.

---

## 10. Shared States

### 10.1 Toast

- Display at the top of the viewport without blocking interaction.
- Dismiss automatically after about three seconds.
- Use for successful Login, save, request, Feedback, and Event read-status operations.

### 10.2 Notification and Status Pages

- Use one centered status card containing an icon or illustration, title, explanation, and actions.
- Put No-question and No-pool actions in the fixed footer.
- Apply to Activation, Logout, Quiz empty states, and Error pages.

### 10.3 Construction Placeholder

- Incomplete data features: use a highly opaque near-white overlay with a thin yellow-and-black striped warning edge.
- Incomplete illustrations: occupy only the future illustration area and do not cover real controls.
- Remove the placeholder directly when the real feature or asset is ready; do not redesign the layout.

---

## 11. Homepage

### 11.1 Shared

- Use the mixed tile background.
- Use `static/rec/logo/wordloop_logo.png` for the logo.
- Logo width is 80% of the viewport, limited by the active area; preserve its aspect ratio.
- Do not add the old extra 48px spacer between the logo and identity card.
- Initially use a 16px layout gap between the logo element and the Username or Guest card in both authentication states. Transparent pixels inside the image do not count as CSS padding.
- Keep Logout and Event icons within the app shell; do not move them outward indefinitely on large viewports.

### 11.2 Authenticated

- Identity card displays the username.
- Logout at top-left; Event at top-right.
- Center the Learning Data title.
- Reserve three Learning Data positions and cover unfinished data with a construction overlay.
- Center hero buttons: `クイズ`, `単語の追加`.
- Footer navigation: `プロフィール`, `単語帳`, `フィードバック`.
- `単語帳` opens the User Vocab filter.
- Normally show all three footer buttons in one row. When space is insufficient, use a 2 + 1 layout with the final button centered.

### 11.3 Guest

- Identity card displays `ゲスト`.
- Hero buttons: `登録`, `ログイン`, `単語帳`.
- `単語帳` opens the general Vocab filter.

---

## 12. Vocab Pages

### 12.1 Vocab and User Vocab Filters

- Header: Back, page title, Home.
- Selection fields: `種類`, JLPT, `カテゴリー`.
- User Vocab Filter also includes `出題対象`:
  - `出題してる` → `in_use=True`
  - `出題してない` → `in_use=False`
  - Neither or both selected → all items
- Categories use at most three buttons per row according to the global selection layout.
- Fixed footer action: `検索`.

### 12.2 Vocab List

- Keep the header, list header, and pagination fixed; only list rows scroll.
- Columns: `単語`, `読み方`.
- The word column is narrower and the kana column wider.
- Headers and row data use the same starting positions.
- Use vertical dividers between columns.
- The whole row is clickable.
- A single-line row uses compact padding; increase height only when text wraps.

### 12.3 User Vocab List

- Add a leftmost checkbox column to the Vocab List structure.
- The header select-all checkbox affects only the current page.
- Do not show visible `すべて` copy below it; retain an `aria-label`.
- Use a vertical divider between the checkbox and word columns.
- Header and row checkboxes must align horizontally.
- The checkbox is outside the detail-link click target.
- Discard unsaved checkbox selections when changing pages.
- Footer contains the `保存` action and pagination.

### 12.4 Vocab Detail

- Header: Back, `単語の詳細`, Home.
- Basic table: `単語`, `意味`, `読み方`, JLPT, `種類`, `カテゴリー`.
- Place Categories below their label, separated by a dashed line, with at most three tags per row.
- Additional data:
  - Katakana: `対応する日本語表現`
  - MCSense: show `意味` and example sentence ordered by `sense_no`; do not show distractors
- Replace the underline in an MCSense example with the base-form answer while preserving the conjugation hint.
- Guests do not see Update or Delete actions.
- Authenticated footer: equal-width `変更申請` and `削除申請`.
- Delete uses Danger.

### 12.5 User Vocab Detail

- Upper table: user-specific data. Lower table: basic vocab data.
- `出題対象` copy: mutually exclusive `出題する／出題しない`.
- Weight bar:
  - 1–49: #BFE8F7
  - 50–99: #8BC9E6
  - 100–149: #E6B85C
  - 150–199: #D9854B
  - 200–299: #AD4B55
  - 300–499: #73528D
  - 500+: #3F344A
- Show `正解数`, `不正解数`, streak, `最後出題時間`, and `前回回答`.
- `最後出題時間` can toggle between relative and absolute time.
- Footer: `保存`, `単語の詳細`.
- `保存` is disabled when unchanged, enabled after a change, and disabled again after a successful save.
- Use the confirmation modal when leaving with unsaved changes.

### 12.6 Vocab Create Request

- Header: Back, `単語の追加`, Home.
- Fields:
  1. `種類`
  2. `単語`
  3. `読み方`
  4. JLPT
  5. `カテゴリー`
  6. `意味`
  7. `理由`
  8. `対応する日本語表現` for Katakana
- Word and kana inputs are equal width and use the enlarged specification.
- `意味` and `理由`: label above, textarea below, initially about three lines tall.
- `種類` and JLPT are single-select buttons; select at most three Categories.
- Show the Katakana field according to type; preserve an unsubmitted value when hidden after switching type.
- Two equal-width footer buttons:
  - `申請` / `ホームへ`
  - `続けて` / `次の単語`
- The second line uses smaller text.
- Use a toast on success and a modal when leaving with unsaved data.

### 12.7 Vocab Update Request

- Header: Back, `変更申請`, Home.
- Prefill existing data.
- `種類` is read-only and shown with label left, data right.
- Word and kana inputs are equal width and use the enlarged specification.
- `意味` and `理由` always use label above, textarea below.
- Footer has one `変更申請` action.
- Return to Vocab Detail with a toast on success.

### 12.8 Vocab Delete Request

- Show basic data and an optional `理由` textarea.
- Footer has one Danger action: `削除申請`.
- Before submission, show the confirmation modal: `この単語の削除を申請しますか？`
- Return to Vocab Detail with a toast on success.

---

## 13. Account Pages

### 13.1 Login

- Header: `ログイン`, Home; leave the left side empty.
- Form and resend area belong to the same scrollable content area.
- Fields always place the label above the input.
- Login state uses a switch.
- Login button follows the general primary-button specification.
- Center the not-activated notice.
- Put the resend explanation and secondary button in a separate card.
- Use the shared validation modal.

### 13.2 Registration

- Follow the Login form layout.
- Header: `登録`, Home.
- Password fields provide visibility icons.
- The `登録` button scrolls with the content.

### 13.3 Activation Email Sent

- Use the shared status card.
- Show an email icon or future tent illustration, title, and explanation.
- Actions: `ログイン画面に戻る`, `認証メールを再送する`.

### 13.4 Account Activation

States:

- Waiting: `アカウントを有効にする`
- Success: `ログイン`
- Already activated: `ログイン`
- Invalid or expired link: `認証メールを再送する`

The UI confirmation preview must not perform a real activation.

### 13.5 Resend Activation

- Follow the Login form layout.
- Show only the email field.
- Action: `認証メールを再送する`.

### 13.6 Logout Result

- Use the shared status card.
- Show `ログアウトしました。`
- Action: `ログイン`.

### 13.7 User Profile

- Compact rows: username, email, last login.
- Center the Learning Data title and cover unfinished functionality with an overlay.
- Show the `マイ単語帳` button.
- Reserve the Recent Answers table layout and cover it with an overlay.

---

## 14. Event Pages

### 14.1 Event List

- Header: `お知らせ`, Home; no Back control.
- Filter: `すべて／未読／既読`, using selection-button styling.
- Table header: select-all checkbox, `項目`.
- Do not show visible `選択` text below the checkbox; retain an `aria-label`.
- Use a vertical divider between checkbox and item.
- Header and row checkboxes must align.
- Five items per page.
- Row: checkbox on the left; type badge and title on the right.
- Vertically center the checkbox across both content lines.
- Use a dashed divider between type and title.
- Only unread titles are bold.
- Limit titles to two lines and use an ellipsis for overflow.
- Footer: `既読にする` plus pagination.
- When there is no data, show the no-event state and hide the action.

Short type labels:

- `単語申請の審査結果` → `申請結果`
- `単語` → `単語`
- `出題優先度の自動更新` → `優先度更新`
- `フィードバックへの返信` → `フィードバック返信`
- `New vocabulary request` → `新規申請`

### 14.2 Event Detail

- Header: Back, `お知らせ`, Home.
- Show the full type badge, title, content, and date/time.
- Use dashed dividers between title and content, and between content and date.
- Put the `内容` label at the upper-left of the content region and start the message on the following line.
- Put `日時` on the left and its data on the right.
- Date format: `YYYY年MM月DD日 HH:mm`.
- Opening the page does not automatically mark the event as read.
- Footer action:
  - Unread → `既読にする`
  - Read → `未読に戻す`
- Change state using POST, CSRF protection, and a fixed action value. Redirect back to the same page and show a toast on success.

---

## 15. Feedback Pages

### 15.1 Feedback Create

- Header: Back, `フィードバック`, Home.
- `種類` uses a dropdown with right-aligned text.
- `内容` textarea is initially about six lines tall.
- Footer: `送信`.
- Return to Homepage and show a toast on success.
- Show a modal when leaving with unsaved data.

### 15.2 Feedback Admin List

- Header: `フィードバック一覧`, Home.
- Status filter:
  - Place the `状態` label and dropdown on the same line.
  - Increase the dropdown from the 10em value in the Version 3 review to 15em (150%). On narrow screens, cap it at the remaining width after the label and gap while keeping both on one line.
  - Right-align the text.
  - Options: `すべて`, `未対応`, `返信済み`, `終了`.
  - Default: `未対応`.
- Five items per page.
- Item first row: status icon, user frame, type frame.
- Item second row: one-line content preview.
- Separate the rows with a dashed line.
- The whole item is clickable.
- Status:
  - Pending: red, filled circle
  - Replied: green, check mark
  - Closed: Ink, horizontal line
- Keep pagination fixed and hide it when there is no data.
- User and type frames use Tag / Metadata BG `#D2E5ED` with Ink `#26343D` text.

### 15.3 Feedback Admin Detail

- Header: Back, `フィードバック詳細`, Home.
- Basic table: status, user, `種類`, `送信日時`.
- `内容` is a separate section with its label above-left and data on the next line.
- When replied, show the reply administrator and reply time.
- Use dashed lines within tables and solid lines between sections.
- Footer:
  - `未対応／返信済み` → `返信`
  - `終了` → disabled `終了`

### 15.4 Feedback Admin Reply

- Header: Back, `フィードバックに返信`, Home.
- Show the original feedback first, then the reply textarea and switch.
- Switch label: `返信後に終了`; default off.
- Footer: `返信`.
- Return to the detail page and show a toast on success.
- Show a modal when leaving with unsaved data.

---

## 16. Quiz

### 16.1 Quiz Setting

- Header: Back, `クイズ設定`, Home.
- `前回の設定を読み込む`:
  - When data exists, load it into the current form without starting the Quiz.
  - When absent, show the unavailable state; clicking it displays `前回のクイズ設定がありません`.
- `問題数`: single-select 10, 20, or 30. No selection means unlimited (`-1`). Clicking the selected option again clears it.
- `種類`, JLPT, and Category are multi-select; no selection means no restriction.
- Lay out each Selection field independently: six Level controls in one row; Type and question count each use one row according to option count; only Categories use at most three per row. Controls in one group have equal size.
- Footer: `開始`.
- Leaving settings before starting does not show an unsaved-data modal.

### 16.2 Shared Quiz Progress

- Answered count = correct count + incorrect count.
- Skip does not count as answered, does not consume a fixed question slot, and the replacement question uses the same question number.
- Track Skip count separately.
- A Hint used before Skip still counts in Summary.
- Unlimited mode continues until the pool is exhausted or another existing ending condition occurs.
- Server endpoints must validate progress themselves rather than trust frontend state alone.

### 16.3 Question State

- Header title: `クイズ`.
- Left-align the question-number frame and size it to its content.
- Question card:
  - Center the word and reserve up to two lines.
  - Question and Non-MC Answer Result share this fixed word-size scale:

    | Character count | Font size |
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

  - 42px is the minimum. Wrap only when the text still cannot fit at that size.
  - Prefer breaking long English text at spaces.
  - Separate word and meaning with a dashed line.
  - Center the meaning and keep its height content-driven.
- The entire answer input surface is clickable.
- Empty hint: `ここを押して回答を入力`.
- Tips and Skip are equal width and use Primary #8BC9E6 with Ink #26343D according to `quiz-question-state.png`; preserve their confirmed dimensions.
- Skip bypasses Answer Result and loads the next question or Summary directly.
- Footer `回答`:
  - Without an answer, show the unavailable style but retain click handling.
  - Clicking displays `何も答えないと進めないよ`.
  - With an answer, submission is enabled.

### 16.4 Kana Input Mode

- Cover the original page with a translucent white backdrop.
- Center the foreground answer above the keyboard panel.
- The bottom sheet contains only the keyboard.
- Add a folder-tab label showing the current question at the upper-left of the keyboard panel:
  - Format: `問題：{word}`
  - Align the tab flush left and project it above the panel. Use the same #BFE8F7 background as the panel.
  - Size width to content, up to 80% of the keyboard panel.
  - Keep text on one line. Reduce the entire line when too long; do not wrap or scroll horizontally.
  - Use 24px Bold text; padding is 8px top, 16px left/right, and 4px bottom, with the text shifted down 4px.
  - Use 14px top corner radii and connect the bottom directly to the panel.
  - The panel's upper-left corner becomes square at the connection; retain the 24px upper-right radius.
  - Reserve normal layout height for the tab so it cannot cover the foreground answer or other content.
- Use a 10 × 6 grid.
- Sixth column: dakuten, handakuten, small-kana control, Backspace.
- Place `完了` across columns 4–5 on the final row. It closes the keyboard without submitting.
- Panel: #BFE8F7.
- Kana keys: #F8FCFF.
- Function keys: #EAF2F6.
- `完了`: #8BC9E6.
- Responsive key size: 44–62px.
- No horizontal scrolling at 320px.
- On short viewports, scroll only the keyboard content.
- Clicking the backdrop or `完了` preserves the answer and closes input mode.

### 16.5 Non-MC Answer Result

- Three-column top row:
  - Left: question number, content-sized
  - Center: `正解／不正解`
  - Right: superuser-only `判定`; reserve blank space for standard users
- All three frames use consistent 14px corner radii.
- The word card shows word and `(kana)`; word sizing uses the same 76px-to-42px scale as Question State.
- Initially use a 6px layout gap between word and kana. Keep equal outer top and bottom spacing in the card.
- Answer comparison card:
  - Upper: `あなたの回答` label and data
  - Dashed divider
  - Lower: per-character image comparison
- MATCH: Ink.
- WRONG, MISSING, and EXTRA: Danger.
- Overlays must stay aligned with their kana glyphs.
- Scale all image glyphs together and wrap to two lines only when necessary.
- Footer:
  - More questions → `次へ`
  - Final question → `結果へ`
  - In unlimited mode, if both Next and Results are available, show them side by side.

### 16.6 Judgement Modal

- Superuser only.
- Title: `判定詳細`.
- Each comparison unit:
  - First row: `正解` data, `回答` data
  - Second row: `種類` data, `詳細種類` data
- Type data such as MATCH or MISSING uses the corresponding color.
- Separate units with dashed lines.
- Maximum modal height: 80dvh. Scroll only the central data area.
- Keep the header title and footer `完了` fixed.
- `完了`, backdrop click, and Escape all close the modal.

### 16.7 Summary

- Header: `結果`, Home; no Back control.
- The illustration area is smaller than the Answer Result illustration area.
- Show a reason card when `ended_early` is true.
- Five statistics:
  - `回答した問題`
  - `正解`
  - `不正解`
  - `スキップ`
  - `ヒント`
- The first item is full width; the remaining four use two rows of two columns.
- Preserve two columns at 320px by reducing gaps, padding, and font sizes according to the specification.
- All data uses Ink; labels use their functional colors.
- Footer: `クイズ設定へ`.

### 16.8 No-question

- Header: `クイズ`, Home.
- Status card:
  - `問題が見つからないよ。`
  - `設定を確認してみてね。`
- Do not show question number, question card, answer area, Tips, or Skip.
- Footer: `クイズ設定へ`.

### 16.9 No-pool Confirmation

- Header: `クイズ設定`, Home.
- Status explanation:
  - `この条件で出せる問題がないよ。`
  - `条件を変えるか、すべての出題対象から始めますか？`
- Two equal-width footer actions:
  - `設定へ戻る` (Secondary)
  - `すべてから出題` (Primary)

---

## 17. Error Pages

### 17.1 Shared

- 400, 403, 404, and 500 share one layout.
- Do not show the standard header.
- Center content within the viewport.
- Show error code, illustration, Japanese title, explanation, and `ホームへ`.
- The 500 page uses a self-contained template without base context dependencies.
- Use a placeholder until the final illustration is available.

### 17.2 Copy

400:

- Title: `そのリクエスト、通ると思いました？`
- Body: `入力内容かURL、ちゃんと確認してくださいね。`

403:

- Title: `誰でも入れると思わないでください。`
- Body: `権限がないので、おとなしく戻ってください。`

404:

- Title:
  - `どこどこ？`
  - `ページはどこ？`
  - `……ないよ。`
- Body: `いくら探してもありませんよ。URLを確認して、ホームへ戻ってください。`

500:

- Title:
  - `僕のせいだけど、`
  - `謝るつもりはない`
  - `www`
- Body: `しばらくしてから、もう一度試してください。`

---

## 18. UI Confirmation Page

- Route: `/ui-confirm/`.
- Register only when `DEBUG=True`.
- Do not include it in general navigation.
- Provide previews for:
  - Activation waiting, success, already activated, and invalid or expired
  - Quiz No-question
  - Error 400, 403, 404, and 500
- Activation previews must not perform real activation or modify data.

---

## 19. Illustration and Icon Direction

- Use a single-pole pyramid-tent theme for the site character and Home icon.
- Do not anthropomorphize the tent with eyes, mouth, arms, or legs.
- Express states through the entrance, lighting, angle, weather, and props.
- Use a simplified vector tent for Home and retain the accessible label `ホーム`.
- The owner designs the final assets; the UI reserves only position, dimensions, safe boundaries, and accessibility behavior.
- Use construction placeholders until Quiz-state illustrations are finalized.

---

## 20. Future Scope

### 20.1 Multiple Choice Quiz

MC is not a v1.0.0 blocker, but retain these directions:

- The question card shows question and meaning; the answer underline and conjugation hint use a hint color.
- Four equal-sized answer buttons in a vertical list, without A/B/C/D labels.
- Selection changes only the selected state; `回答` performs submission.
- Each Hint removes one incorrect answer and displays `----`; never select the correct answer automatically.
- Tips and Skip follow non-MC behavior.
- MC Result shows the completed sentence, `あなたの回答`, and the correct answer.
- MC does not show the Judgement modal.
- Footer flow follows non-MC.
- The hint-red color remains unresolved and must remain distinct from the Danger error red.

### 20.2 Admin Event Create

- Admin-only custom site page, still using Japanese UI.
- Fields: `種類`, `タイトル`, `内容`; all required.
- The first version targets all users.
- Footer: `公開`.
- Confirmation before submission: `全ユーザーに公開します。よろしいですか？`
- Publish/expiry time, importance, and active status are outside the first version.
- Return destination remains pending until the admin event-management flow is defined.

---

## 21. Pending Decisions

The following are not final tokens and must not be guessed during implementation:

1. Quiz input-mode panel height and minimum foreground-answer-area height.
2. Quiz answer-input focus, cursor, deletion, and image-glyph details.
3. Hint-red color for future MC.
4. Return destination for Admin Event Create.
5. Final tent and Quiz illustration assets.

---

## 22. Implementation and Acceptance Principles

### 22.1 Structure

- Define shared dimensions through component classes or design tokens.
- Do not let parent DOM nesting change button padding.
- Do not duplicate the same CSS page by page.
- Django templates use four-space indentation and split long attributes across lines.
- Every interactive control has keyboard focus behavior and an accessible name.

### 22.2 Responsive Verification

At minimum, test:

- 320px
- 390px
- 540px
- Large desktop viewport
- Height below 700px
- Mobile virtual keyboard open

### 22.3 Visual Consistency

- The same element type has equal top and bottom padding.
- The same type uses the same padding across pages.
- Header, content, and footer produce no horizontal overflow.
- A fixed footer is not obscured by the scrollbar.
- Selection controls, checkboxes, and column headers align correctly.
- Long text wraps only according to the defined rules; do not shrink or truncate it arbitrarily.

### 22.4 Behavior

- Skip does not count as answered.
- Unsaved-data confirmation triggers only for the site navigation specified by the design.
- State-changing actions use POST and CSRF protection.
- Disabled and unavailable behavior follows page specifications rather than relying on appearance alone.
- UI confirmation previews never modify real data.

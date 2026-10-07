const { test, expect } = require("@playwright/test");
test.use({ baseURL: "http://127.0.0.1:8765", viewport: {width:390,height:844} });
async function login(page) {
  await page.goto("/accounts/user_login/");
  await page.locator('[name="username"]').fill("ui@example.test");
  await page.locator('[name="password"]').fill("ui-preview-password");
  await page.getByRole("button", {name:"ログイン",exact:true}).click();
  await expect(page).toHaveURL(/127\.0\.0\.1:8765\/(accounts\/)?$/);
}
test("all primary routes render without horizontal overflow at supported widths", async ({page}) => {
  const errors = []; page.on("pageerror", e => errors.push(e.message));
  await login(page);
  const routes = ["/", "/accounts/user_detail/", "/dictionary/vocab/list_filter",
    "/dictionary/user_vocab/list_filter", "/dictionary/vocab/list", "/dictionary/user_vocab/list",
    "/dictionary/vocab/1", "/dictionary/vocab/66", "/dictionary/user_vocab/1",
    "/dictionary/user_vocab/66", "/dictionary/vocab/create", "/dictionary/vocab/1/update/",
    "/dictionary/vocab/1/delete/", "/core/user_event_list", "/core/user_event_detail/1",
    "/core/feedback/create/", "/core/feedback/list/?status=all", "/core/feedback/detail/1",
    "/core/feedback/reply/1", "/quiz/setting", "/quiz/no_pool_confirm/"];
  for (const width of [320,390,540,1280]) {
    await page.setViewportSize({width,height:width===320?568:844});
    for (const route of routes) {
      const response = await page.goto(route);
      expect(response.status(), route).toBeLessThan(400);
      expect(await page.locator("body").evaluate(el => el.scrollWidth <= innerWidth + 1), route+" width="+width).toBeTruthy();
      if (width === 390 && ["/","/dictionary/vocab/create","/dictionary/user_vocab/66","/core/feedback/list/?status=all"].includes(route)) {
        await page.screenshot({path:"/tmp/kotoba-ui-"+route.replace(/[^a-z0-9]/gi,"_")+".png"});
      }
    }
  }
  expect(errors).toEqual([]);
});
test("password visibility and server-side error modal", async ({page}) => {
  await page.goto("/accounts/user_login/");
  await page.getByRole("button",{name:"パスワードを表示",exact:true}).click();
  await expect(page.locator('[name="password"]')).toHaveAttribute("type","text");
  await page.getByRole("button",{name:"ログイン",exact:true}).click();
  await expect(page.locator("#form-errors")).toBeVisible();
  await page.getByRole("button",{name:"閉じる"}).click();
  await expect(page.locator('[name="username"]')).toBeFocused();
});
test("request selection limits, conditional field and discard confirmation", async ({page}) => {
  await login(page);
  await page.goto("/dictionary/vocab/create");
  await expect(page.locator('[data-field="native_japanese"]')).toBeHidden();
  await page.locator('[name="vocab_type"][value="katakana"]').check({force:true});
  await expect(page.locator('[data-field="native_japanese"]')).toBeVisible();
  const categories = page.locator('[name="categories"]');
  for (let i=0;i<3;i++) await categories.nth(i).check({force:true});
  await expect(categories.nth(3)).toBeDisabled();
  await categories.nth(0).uncheck({force:true});
  await expect(categories.nth(3)).toBeEnabled();
  await page.getByRole("link",{name:"ホーム",exact:true}).click();
  await expect(page.locator("#ui-dialog")).toBeVisible();
  await page.getByRole("button",{name:"キャンセル",exact:true}).click();
  await expect(page.locator('[name="vocab_type"][value="katakana"]')).toBeChecked();
});
test("user vocabulary save toggles only when changed", async ({page}) => {
  await login(page); await page.goto("/dictionary/user_vocab/1");
  const save = page.getByRole("button",{name:"保存",exact:true});
  await expect(save).toBeDisabled();
  const initial = await page.locator('[name="in_use"]:checked').inputValue();
  await page.locator('[name="in_use"][value="'+(initial==="True"?"False":"True")+'"]').check({force:true});
  await expect(save).toBeEnabled(); await save.click();
  await expect(save).toBeDisabled();
});
test("create request submit actions and feedback reply use real server workflows", async ({page}) => {
  await login(page);
  for (const action of ["continue","home"]) {
    await page.goto("/dictionary/vocab/create");
    await page.locator('[name="vocab_type"][value="vocab"]').check({force:true});
    await page.locator('[name="word"]').fill("UI確認" + Date.now());
    await page.locator('[name="kana"]').fill("かくにん");
    await page.locator('[name="submit_action"][value="'+action+'"]').click();
    if (action === "continue") {
      await expect(page).toHaveURL(/dictionary\/vocab\/create$/);
      await expect(page.locator('[name="word"]')).toHaveValue("");
      await expect(page.locator('[name="vocab_type"]:checked')).toHaveCount(0);
    } else await expect(page).toHaveURL("http://127.0.0.1:8765/");
    await expect(page.locator("#toast-region")).toContainText("申請");
  }
  await page.goto("/core/feedback/create/");
  await expect(page.locator('[name="feedback_type"]')).toHaveValue("");
  await page.locator('[name="feedback_type"]').selectOption("bug_report");
  const message = "UI送信確認" + Date.now();
  await page.locator('[name="context"]').fill(message);
  await page.getByRole("button",{name:"送信",exact:true}).click();
  await expect(page).toHaveURL("http://127.0.0.1:8765/");
  await page.goto("/core/feedback/list/");
  await page.locator(".ui-list-item").filter({hasText:message}).getByRole("link").click();
  await page.getByRole("link",{name:"返信",exact:true}).click();
  await page.locator('[name="context"]').fill("UI確認用の返信です。");
  await page.locator('[name="is_close"]').check();
  await page.getByRole("button",{name:"返信",exact:true}).click();
  await expect(page).toHaveURL(/core\/feedback\/detail\/\d+/);
  await expect(page.getByRole("button",{name:"終了",exact:true})).toBeDisabled();
});
test("quiz question count selection can be cleared and previous settings are unavailable initially", async ({page}) => {
  await login(page); await page.goto("/quiz/setting");
  await page.getByRole("button",{name:"前回の設定を読み込む"}).click({force:true});
  await expect(page.locator("#toast-region")).toContainText("前回のクイズ設定がありません");
  const option = page.locator('[name="quiz_num"][value="10"]').locator("..");
  await option.click();
  await expect(page.locator('[name="quiz_num"][value="10"]')).toBeChecked();
  await option.click();
  await expect(page.locator('[name="quiz_num"]:checked')).toHaveCount(0);
});
test("notifications default unchecked and support read and unread", async ({page}) => {
  await login(page); await page.goto("/core/user_event_list");
  await expect(page.locator('[name="selected_ids"]:checked')).toHaveCount(0);
  await page.goto("/core/user_event_detail/1");
  const markRead = page.getByRole("button",{name:"既読にする",exact:true});
  if (await markRead.count()) await markRead.click();
  await page.getByRole("button",{name:"未読に戻す",exact:true}).click();
  await expect(markRead).toBeVisible();
});
test("quiz skip does not advance answer number; keyboard and AJAX result work", async ({page}) => {
  test.setTimeout(60000);
  const errors=[]; page.on("pageerror",e=>errors.push(e.message));
  await login(page); await page.goto("/quiz/setting");
  await page.locator('[name="quiz_num"][value="10"]').check({force:true});
  await page.getByRole("button",{name:"開始",exact:true}).click();
  await expect(page.locator("#quiz-count")).toContainText("第1問");
  await page.getByRole("button",{name:"スキップ",exact:true}).click();
  await expect(page.locator("#quiz-area-container")).not.toHaveAttribute("aria-busy", "true");
  await expect(page.locator("#quiz-count")).toContainText("第1問");
  await page.getByRole("button",{name:"回答",exact:true}).click({force:true});
  await expect(page.locator("#toast-region")).toContainText("何も答えないと進めないよ");
  await page.locator("[data-show-keyboard]").click();
  await expect(page.locator("#quiz-keyboard")).toBeVisible();
  await page.locator('[data-kana="あ"],[data-kana="ア"]').first().click();
  await page.locator('[data-kana="hide"]').click();
  await expect(page.locator("#answer-input")).not.toHaveValue("");
  await page.getByRole("button",{name:"回答",exact:true}).click();
  await expect(page.locator('[data-quiz-state="result"]')).toBeVisible();
  await page.getByRole("button",{name:"判定",exact:true}).click();
  await expect(page.locator("#judgement-dialog")).toBeVisible();
  await page.keyboard.press("Escape");
  await page.getByRole("button",{name:"次へ",exact:true}).click();
  await expect(page.locator("#quiz-count")).toContainText("第2問");
  await expect(page.locator("#answer-input")).toHaveValue("");
  await page.locator("[data-show-keyboard]").click();
  await page.screenshot({path:"/tmp/kotoba-ui-keyboard.png"});
  for (const width of [320,540]) {
    await page.setViewportSize({width,height:568});
    const key = await page.locator('[data-kana="あ"],[data-kana="ア"]').first().boundingBox();
    expect(key.width).toBeGreaterThanOrEqual(44);
    expect(Math.abs(key.width-key.height)).toBeLessThan(1);
    expect(await page.locator("#quiz-input-panel-container").evaluate(el => el.scrollWidth <= el.clientWidth+1)).toBeTruthy();
    await page.locator('[data-kana="hide"]').scrollIntoViewIfNeeded();
    await expect(page.locator('[data-kana="hide"]')).toBeInViewport();
  }
  await page.locator('[data-kana="hide"]').click();
  for (let question=2; question<=10; question++) {
    for (let hint=0; hint<25; hint++) {
      const correct = await page.locator("#answer-form").getAttribute("data-correct-answer");
      if (await page.locator("#answer-input").inputValue() === correct) break;
      await page.locator("[data-hint]").click();
    }
    await page.getByRole("button",{name:"回答",exact:true}).click();
    await expect(page.locator('[data-quiz-state="result"]')).toBeVisible();
    await page.getByRole("button",{name:question===10?"結果へ":"次へ",exact:true}).click();
    await expect(page.locator('[data-quiz-state="'+(question===10?"summary":"question")+'"]')).toBeVisible();
  }
  await expect(page.locator(".summary-total")).toContainText("10問");
  await expect(page.locator(".summary-card").filter({hasText:"スキップ"})).toContainText("1問");
  await page.screenshot({path:"/tmp/kotoba-ui-summary.png"});
  expect(errors).toEqual([]);
});

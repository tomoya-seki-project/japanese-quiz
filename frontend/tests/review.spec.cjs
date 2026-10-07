const { test, expect } = require("@playwright/test");

test("ver3: independent selection layouts, spacing and wider request fields", async ({ page }) => {
    await login(page);
    for (const width of [320, 390, 540, 1280]) {
        await page.setViewportSize({ width, height: 844 });
        for (const route of ["/quiz/setting", "/dictionary/user_vocab/list_filter", "/dictionary/vocab/list_filter", "/dictionary/vocab/create", "/dictionary/vocab/1/update/"]) {
            await page.goto(route);
            await page.evaluate(() => document.fonts.ready);
            const groups = await page.locator("[data-selection]").evaluateAll(fields => fields.map(field => {
                const grid = field.querySelector(".selection-grid");
                const boxes = [...grid.children].map(option => option.getBoundingClientRect());
                const label = field.querySelector(".field-label").getBoundingClientRect();
                const frame = field.getBoundingClientRect();
                return {
                    category: grid.classList.contains("categories"),
                    level: grid.classList.contains("level-options"),
                    count: boxes.length,
                    rows: new Set(boxes.map(box => Math.round(box.y))).size,
                    firstRow: boxes.filter(box => Math.abs(box.y - boxes[0].y) < 1).length,
                    top: label.top - frame.top,
                    bottom: frame.bottom - Math.max(...boxes.map(box => box.bottom)),
                    overflow: grid.scrollWidth > grid.clientWidth + 1
                };
            }));
            for (const group of groups) {
                if (group.category) expect(group.firstRow).toBeLessThanOrEqual(3);
                else expect(group.rows, route).toBe(1);
                if (group.level) expect(group.count).toBe(6);
                expect(Math.abs(group.top - group.bottom), route).toBeLessThan(1);
                expect(group.overflow, route).toBeFalsy();
            }
            if (route.includes("/create") || route.includes("/update")) {
                const widths = [];
                for (const name of ["word", "kana"]) {
                    const dimensions = await page.locator('[data-field="' + name + '"]').evaluate(field => {
                        const style = getComputedStyle(field);
                        const inner = field.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
                        const input = field.querySelector("input").getBoundingClientRect();
                        const label = field.querySelector("label");
                        return { width: input.width, target: (inner - 12) * 2 / 3 * 1.25,
                            labelHeight: label.offsetHeight, lineHeight: parseFloat(getComputedStyle(label).lineHeight),
                            inside: input.right <= field.getBoundingClientRect().right };
                    });
                    expect(Math.abs(dimensions.width - dimensions.target)).toBeLessThan(1);
                    expect(dimensions.labelHeight).toBeLessThanOrEqual(dimensions.lineHeight + 1);
                    expect(dimensions.inside).toBeTruthy();
                    widths.push(dimensions.width);
                }
                expect(Math.abs(widths[0] - widths[1])).toBeLessThan(1);
            }
        }
        await page.goto("/");
        const gap = await page.evaluate(() =>
            document.querySelector(".home-identity").getBoundingClientRect().top -
            document.querySelector(".home-logo").getBoundingClientRect().bottom);
        expect(Math.abs(gap - 16)).toBeLessThan(1);
        await page.goto("/core/feedback/list/?status=all");
        const filter = await page.locator(".feedback-filter").evaluate(field => {
            const label = field.querySelector("label").getBoundingClientRect();
            const select = field.querySelector("select").getBoundingClientRect();
            return { width: select.width, aligned: Math.abs(label.y + label.height / 2 - select.y - select.height / 2) < 1 };
        });
        expect(filter.aligned).toBeTruthy();
        if (width >= 390) expect(filter.width).toBe(240);
    }
    await page.setViewportSize({ width: 540, height: 844 });
    await page.goto("/dictionary/user_vocab/1");
    const heights = await page.locator(".user-vocab-stats > .data-row").evaluateAll(rows =>
        rows.slice(1).map(row => row.getBoundingClientRect().height));
    expect(Math.max(...heights) - Math.min(...heights)).toBeLessThan(2);
    const toggle = page.locator("[data-time-toggle]");
    const alternate = await toggle.getAttribute("data-time-toggle");
    await toggle.click();
    await expect(toggle).toHaveText(alternate);
    await page.goto("/quiz/setting");
    await page.getByRole("button", { name: "開始", exact: true }).click();
    for (const button of [page.locator("[data-hint]"), page.getByRole("button", { name: "スキップ", exact: true })]) {
        await expect(button).toHaveCSS("background-color", "rgb(139, 201, 230)");
    }
    await page.locator("[data-hint]").click();
    await page.getByRole("button", { name: "回答", exact: true }).click();
    await expect(page.locator(".quiz-result-word-card")).toBeVisible();
    const resultGap = await page.locator(".quiz-result-word-card").evaluate(card =>
        card.querySelector("p").getBoundingClientRect().top - card.querySelector(".quiz-word").getBoundingClientRect().bottom);
    expect(Math.abs(resultGap - 6)).toBeLessThan(1);
});

test("confirmed sizing, field layout and checkbox alignment", async ({ page }) => {
    await login(page);
    for (const width of [320, 360, 390, 540]) {
        await page.setViewportSize({ width, height: 844 });
        await page.goto("/dictionary/vocab/create");
        for (const name of ["meaning", "request_reason"]) {
            const field = page.locator('[data-field="' + name + '"]');
            const label = await field.locator("label").boundingBox();
            const input = await field.locator("textarea").boundingBox();
            expect(input.y).toBeGreaterThanOrEqual(label.y + label.height);
        }
        const options = await page.locator(".categories .selection-option").evaluateAll(nodes =>
            nodes.map(node => ({ width: node.offsetWidth, height: node.offsetHeight })));
        expect(options.every(option => Math.abs(option.width - options[0].width) <= 1 && option.height === options[0].height)).toBeTruthy();
        await page.goto("/dictionary/user_vocab/list");
        const header = await page.locator("[data-select-all]").boundingBox();
        const checkbox = await page.locator(".ui-list-item .checkbox-cell input[type=checkbox]").first().boundingBox();
        expect(header.x).toBe(checkbox.x);
        const pagination = page.locator("[data-pagination]");
        expect(await pagination.evaluate(node => node.scrollWidth <= node.clientWidth)).toBeTruthy();
        expect((await page.locator(".page-link:visible").first().boundingBox()).width).toBe(44);
        await page.goto("/accounts/resend-activation-email/");
        await page.evaluate(() => document.fonts.ready);
        const button = page.locator(".ui-button-action");
        const dimensions = await button.evaluate(node => ({
            width: node.offsetWidth,
            parent: document.querySelector(".app-main").clientWidth - 32,
            padding: parseFloat(getComputedStyle(node).paddingLeft),
            text: node.textContent
        }));
        expect(dimensions.width).toBeGreaterThanOrEqual(dimensions.parent / 2 - 1);
        expect(dimensions.padding).toBe(36);
        await button.evaluate(node => {
            delete node.dataset.actionText;
            node.textContent = "アカウントを有効にするための確認";
            window.dispatchEvent(new Event("resize"));
        });
        if (width <= 390) expect(await button.textContent()).toContain("\n");
    }
});

test.use({ baseURL: "http://127.0.0.1:8765", viewport: { width: 390, height: 844 } });

async function login(page) {
    await page.goto("/accounts/user_login/");
    await page.locator('[name="username"]').fill("ui@example.test");
    await page.locator('[name="password"]').fill("ui-preview-password");
    await page.getByRole("button", { name: "ログイン", exact: true }).click();
    await expect(page.locator(".home-navigation")).toBeVisible();
}

test("review: navigation, local fonts, equal inputs and single-row levels", async ({ page }) => {
    await login(page);
    await expect(page.locator(".home-navigation").getByRole("link", { name: "単語帳", exact: true }))
        .toHaveAttribute("href", /user_vocab/);
    await page.evaluate(() => document.fonts.ready);
    expect(await page.evaluate(() => document.fonts.check('700 20px "Zen Maru Gothic"'))).toBeTruthy();
    for (const route of ["/dictionary/vocab/create", "/quiz/setting"]) {
        await page.goto(route);
        const boxes = await page.locator(".level-options .selection-option").evaluateAll(elements =>
            elements.map(element => {
                const box = element.getBoundingClientRect();
                return { y: box.y, width: box.width };
            }));
        expect(boxes.length).toBeGreaterThan(0);
        expect(boxes).toHaveLength(6);
        expect(boxes.every(box => Math.abs(box.y - boxes[0].y) < 1)).toBeTruthy();
        expect(boxes.every(box => Math.abs(box.width - boxes[0].width) < 1)).toBeTruthy();
    }
    await page.goto("/dictionary/vocab/create");
    const word = await page.locator('[name="word"]').boundingBox();
    const kana = await page.locator('[name="kana"]').boundingBox();
    expect(Math.abs(word.width - kana.width)).toBeLessThan(1);
});

test("review: selectable rows keep checkbox beside content", async ({ page }) => {
    await login(page);
    for (const width of [320, 390, 540, 1280]) {
        await page.setViewportSize({ width, height: 844 });
        for (const route of ["/dictionary/user_vocab/list", "/core/user_event_list"]) {
            await page.goto(route);
            const row = page.locator(".ui-list-item.selectable-row").first();
            const checkbox = await row.locator(".checkbox-cell").boundingBox();
            const content = await row.locator("a").boundingBox();
            expect(checkbox.x).toBeLessThan(content.x);
            expect(Math.abs(checkbox.y + checkbox.height / 2 - content.y - content.height / 2)).toBeLessThan(2);
        }
    }
});

test("review: unlimited quiz result actions and judgement fields stay side by side", async ({ page }) => {
    await login(page);
    await page.goto("/quiz/setting");
    await page.getByRole("button", { name: "開始", exact: true }).click();
    await page.locator("[data-hint]").click();
    await page.getByRole("button", { name: "回答", exact: true }).click();
    await expect(page.locator('[data-quiz-state="result"]')).toBeVisible();
    const forms = page.locator(".quiz-result-actions form");
    await expect(forms).toHaveCount(2);
    const first = await forms.nth(0).boundingBox();
    const second = await forms.nth(1).boundingBox();
    expect(Math.abs(first.y - second.y)).toBeLessThan(1);
    expect(first.x).toBeLessThan(second.x);
    await page.getByRole("button", { name: "判定", exact: true }).click();
    const cell = page.locator(".judgement-cell").first();
    const label = await cell.locator("dt").boundingBox();
    const value = await cell.locator("dd").boundingBox();
    expect(Math.abs(label.y - value.y)).toBeLessThan(2);
    await page.screenshot({ path: "/tmp/ui-review-judgement.png" });
    await page.keyboard.press("Escape");
    await page.screenshot({ path: "/tmp/ui-review-result.png" });
});

test("review: UI confirm links render safely and Homepage logo uses 80vw", async ({ page }) => {
    await page.goto("/ui-confirm/");
    const links = page.locator("main a.ui-button");
    await expect(links).toHaveCount(9);
    const hrefs = await links.evaluateAll(elements => elements.map(element => element.getAttribute("href")));
    for (const href of hrefs) {
        const response = await page.goto(href);
        expect(response.status(), href).toBe(200);
    }
    await page.goto("/ui-confirm/account-activation/confirm/");
    await expect(page.getByRole("button", { name: "アカウントを有効にする" }))
        .toHaveAttribute("type", "button");
    await page.goto("/");
    const logo = page.locator(".home-logo");
    await expect(logo).toHaveAttribute("src", /wordloop_logo\.png$/);
    await expect.poll(() => logo.evaluate(element => element.complete && element.naturalWidth))
        .toBe(1538);
    const width = await logo.evaluate(element => element.getBoundingClientRect().width);
    expect(Math.abs(width - 312)).toBeLessThan(1);
});

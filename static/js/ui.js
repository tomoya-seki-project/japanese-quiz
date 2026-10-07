/* Shared interactions; styling classes are never used as action selectors. */
(() => {
    function sizeActions() {
        const shell = document.querySelector(".app-shell");
        const main = document.querySelector(".app-main");
        if (!shell || !main) return;
        const mainStyle = getComputedStyle(main);
        const activeWidth = main.clientWidth - parseFloat(mainStyle.paddingLeft) - parseFloat(mainStyle.paddingRight);
        document.querySelectorAll(".ui-button-action").forEach(button => {
            const text = button.dataset.actionText || button.textContent.trim();
            button.dataset.actionText = text;
            const style = getComputedStyle(button);
            const context = document.createElement("canvas").getContext("2d");
            context.font = style.fontWeight + " " + style.fontSize + " " + style.fontFamily;
            const padding = parseFloat(style.fontSize) * 4;
            let lines = [text];
            if (context.measureText(text).width + padding > shell.clientWidth * .8) {
                const characters = Array.from(text);
                let best = Infinity;
                for (let index = 1; index < characters.length; index++) {
                    const pair = [characters.slice(0, index).join(""), characters.slice(index).join("")];
                    const width = Math.max(...pair.map(line => context.measureText(line).width));
                    if (width < best) {
                        best = width;
                        lines = pair;
                    }
                }
            }
            button.textContent = lines.join("\n");
            button.style.whiteSpace = "pre-line";
            button.style.width = Math.max(activeWidth / 2, Math.max(...lines.map(line => context.measureText(line).width)) + padding + 1) + "px";
        });
    }
    document.fonts.ready.then(sizeActions);
    window.addEventListener("resize", sizeActions);
    const dialog = document.getElementById("ui-dialog");
    let confirmAction = null;
    window.uiToast = (message, kind = "") => {
        const toast = document.createElement("div");
        toast.className = "toast " + kind;
        toast.textContent = message;
        document.getElementById("toast-region").append(toast);
        setTimeout(() => toast.remove(), 3000);
    };
    window.uiConfirm = (title, text, label, action) => {
        document.getElementById("dialog-title").textContent = title;
        document.getElementById("dialog-body").textContent = text;
        dialog.querySelector("[data-dialog-confirm]").textContent = label;
        confirmAction = action;
        dialog.showModal();
    };
    document.querySelectorAll(".toast").forEach(t => setTimeout(() => t.remove(), 3000));
    document.addEventListener("click", e => {
        const close = e.target.closest("[data-close-dialog], [data-dialog-cancel]");
        if (close) close.closest("dialog").close();
        if (e.target.closest("[data-dialog-confirm]")) {
            dialog.close();
            confirmAction?.();
        }
        const password = e.target.closest("[data-password]");
        if (password) {
            const input = document.getElementById(password.dataset.password);
            const show = input.type === "password";
            input.type = show ? "text" : "password";
            password.setAttribute("aria-pressed", String(show));
            password.setAttribute("aria-label", show ? "パスワードを隠す" : "パスワードを表示");
        }
        const time = e.target.closest("[data-time-toggle]");
        if (time) {
            const previous = time.textContent;
            time.textContent = time.dataset.timeToggle;
            time.dataset.timeToggle = previous;
        }
        const unavailable = e.target.closest("[data-unavailable]");
        if (unavailable) {
            e.preventDefault();
            window.uiToast(unavailable.dataset.unavailable);
        }
        const link = e.target.closest("a[href]");
        if (link && !e.ctrlKey && !e.metaKey && !e.shiftKey) {
            const dirty = [...document.querySelectorAll("form[data-dirty]")].some(f => snapshot(f) !== f.dataset.initial);
            const navigate = () => {
                if (link.hasAttribute("data-back") && document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) history.back();
                else location.assign(link.href);
            };
            if (dirty) {
                e.preventDefault();
                window.uiConfirm("未保存の変更", "変更を破棄して移動しますか？", "破棄して移動", navigate);
            } else if (link.hasAttribute("data-back")) {
                e.preventDefault();
                navigate();
            }
        }
        const open = e.target.closest("[data-open-dialog]");
        if (open) document.getElementById(open.dataset.openDialog)?.showModal();
    });
    document.querySelectorAll("dialog").forEach(d => {
        d.addEventListener("click", e => {
            if (e.target !== d) return;
            const r = d.getBoundingClientRect();
            if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) d.close();
        });
    });
    const snapshot = form => JSON.stringify([...new FormData(form)].filter(([k]) => k !== "csrfmiddlewaretoken"));

    function updateSelections() {
        document.querySelectorAll("[data-selection][data-limit]").forEach(group => {
            const count = group.querySelectorAll("input:checked").length;
            group.querySelectorAll("input").forEach(i => i.disabled = !i.checked && count >= Number(group.dataset.limit));
        });
        const type = document.querySelector('[name="vocab_type"]:checked')?.value;
        const native = document.querySelector('[data-field="native_japanese"]');
        if (native && document.querySelector('[data-vocab-request]')) {
            const fixedType = document.querySelector("[data-fixed-type]")?.dataset.fixedType;
            native.hidden = (fixedType || type) !== "katakana";
            native.querySelectorAll("input").forEach(i => i.disabled = native.hidden);
        }
        document.querySelectorAll("form[data-save-on-change]").forEach(f => {
            const button = document.querySelector('[form="' + f.id + '"][type="submit"]');
            if (button) button.disabled = snapshot(f) === f.dataset.initial;
        });
    }
    document.querySelectorAll("[data-deselect] input").forEach(input => {
        let selected = false;
        input.closest("label").addEventListener("pointerdown", () => selected = input.checked);
        input.addEventListener("keydown", e => {
            if (e.key === " ") selected = input.checked;
        });
        input.addEventListener("click", () => {
            if (selected) input.checked = false;
            selected = false;
            input.dispatchEvent(new Event("change", {
                bubbles: true
            }));
        });
    });
    updateSelections();
    document.querySelectorAll("form[data-dirty], form[data-save-on-change]").forEach(f => f.dataset.initial = snapshot(f));
    updateSelections();
    const initialBoxes = [...document.querySelectorAll('input[name="selected_ids"]')];
    const initialAll = document.querySelector("[data-select-all]");
    if (initialAll && initialBoxes.length) {
        initialAll.checked = initialBoxes.every(i => i.checked);
        initialAll.indeterminate = initialBoxes.some(i => i.checked) && !initialAll.checked;
    }
    document.addEventListener("change", e => {
        updateSelections();
        if (e.target.matches("[data-select-all]")) {
            document.querySelectorAll('input[name="selected_ids"]').forEach(i => i.checked = e.target.checked);
        }
        const boxes = [...document.querySelectorAll('input[name="selected_ids"]')];
        const all = document.querySelector("[data-select-all]");
        if (all && boxes.length) {
            all.checked = boxes.every(i => i.checked);
            all.indeterminate = boxes.some(i => i.checked) && !all.checked;
        }
        if (e.target.matches("[data-auto-submit]")) e.target.form.requestSubmit();
    });
    document.addEventListener("input", updateSelections);
    document.querySelectorAll("form[data-confirm-delete]").forEach(f => {
        f.addEventListener("submit", e => {
            if (f.dataset.confirmed) return;
            e.preventDefault();
            window.uiConfirm("削除申請", "この単語の削除を申請しますか？", "申請する", () => {
                f.dataset.confirmed = "1";
                f.requestSubmit();
            });
        });
    });
    const errorDialog = document.querySelector("[data-auto-open]");
    if (errorDialog) {
        errorDialog.addEventListener("close", () => document.querySelector(".field-invalid input, .field-invalid textarea, .field-invalid select")?.focus());
        errorDialog.showModal();
    }

    function pagination() {
        document.querySelectorAll("[data-pagination]").forEach(nav => {
            const width = document.querySelector(".app-shell").clientWidth;
            const desired = width < 360 ? 1 : width < 480 ? 3 : 5;
            const available = Math.max(1, Math.floor((nav.clientWidth - 194) / 50));
            const max = Math.min(desired, available % 2 ? available : available - 1);
            const total = Number(nav.dataset.total),
                current = Number(nav.dataset.current);
            const start = Math.max(1, Math.min(current - Math.floor(max / 2), total - max + 1));
            nav.querySelectorAll("[data-page]").forEach(a => a.hidden = Number(a.dataset.page) < start || Number(a.dataset.page) >= start + max);
        });
    }
    pagination();
    window.addEventListener("resize", pagination);
    let baseline = window.visualViewport?.height || innerHeight;
    let savedScroll = 0;

    function inputViewport() {
        if (!window.visualViewport) return;
        const field = document.activeElement;
        const typing = field?.matches('textarea, input:not([type=checkbox],[type=radio],[type=hidden],[type=submit],[type=button])');
        const keyboard = typing && matchMedia("(pointer: coarse)").matches && baseline - visualViewport.height > 140;
        const main = document.getElementById("main-content");
        if (keyboard && !document.body.classList.contains("input-focus")) savedScroll = main.scrollTop;
        const wasOpen = document.body.classList.contains("input-focus");
        document.body.classList.toggle("input-focus", Boolean(keyboard));
        document.querySelector(".app-shell").style.height = keyboard ? visualViewport.height + "px" : "";
        if (keyboard) field.scrollIntoView({
            block: "nearest"
        });
        else if (wasOpen) main.scrollTop = savedScroll;
        if (!typing) baseline = Math.max(baseline, visualViewport.height);
    }
    window.visualViewport?.addEventListener("resize", inputViewport);
    document.addEventListener("focusin", inputViewport);
    document.addEventListener("focusout", () => setTimeout(inputViewport, 50));
})();

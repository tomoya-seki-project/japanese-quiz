(() => {
    const area = document.getElementById("quiz-area-container");
    if (!area) return;
    const keyboard = document.getElementById("quiz-keyboard");
    const panel = document.getElementById("quiz-input-panel-container");
    const assetBase = area.dataset.staticBase;
    let graphics = {},
        busy = false;
    const loadGraphics = fetch(assetBase + "rec/kana_graphic_map.json")
        .then(r => {
            if (!r.ok) throw new Error("Kana assets unavailable");
            return r.json();
        })
        .then(data => {
            graphics = data;
            renderAnswer();
            decorateKeys();
        })
        .catch(() => window.uiToast("文字画像を読み込めませんでした。文字で表示します。"));

    function drawAnswer(target, value) {
        target.replaceChildren();
        target.setAttribute("aria-label", value || "ここを押して回答を入力");
        if (!value) {
            const hint = document.createElement("span");
            hint.className = "text-muted";
            hint.textContent = "ここを押して回答を入力";
            target.append(hint);
            return;
        }
        for (const char of value) {
            const unit = document.createElement("span");
            unit.className = "kana-unit";
            const path = graphics[char]?.MATCH?.image_path;
            if (path) {
                const img = document.createElement("img");
                img.src = assetBase + path;
                img.alt = char;
                unit.append(img);
            } else {
                unit.textContent = char;
                unit.style.fontSize = "32px";
            }
            target.append(unit);
        }
        resizeKana(target);
    }

    function resizeKana(target) {
        const count = target.querySelectorAll(".kana-unit").length;
        if (count) target.style.setProperty("--kana-size", Math.max(28, Math.min(64, target.clientWidth / count)) + "px");
    }

    function renderAnswer() {
        const answer = document.getElementById("answer-input");
        if (!answer) return;
        drawAnswer(document.getElementById("answer-display"), answer.value);
        drawAnswer(document.getElementById("keyboard-answer-display"), answer.value);
        document.getElementById("answer-submit")?.setAttribute("aria-disabled", String(!answer.value));
    }

    function decorateKeys() {
        panel.querySelectorAll("[data-kana]").forEach(key => {
            const kana = key.dataset.kana,
                path = graphics[kana]?.MATCH?.image_path;
            if (!path) return;
            const img = document.createElement("img");
            img.src = assetBase + path;
            img.alt = "";
            key.setAttribute("aria-label", kana);
            key.replaceChildren(img);
        });
    }

    function resizeWords() {
        area.querySelectorAll(".quiz-word").forEach(word => {
            const length = Array.from(word.textContent.trim()).length || 1;
            const preferred = Math.max(42, 76 - Math.max(0, length - 2) * 4);
            word.style.whiteSpace = "nowrap";
            let size = preferred;
            word.style.fontSize = size + "px";
            while (size > 42 && word.scrollWidth > word.clientWidth) {
                size = Math.max(42, size - 1);
                word.style.fontSize = size + "px";
            }
            word.style.whiteSpace = "normal";
        });
    }

    function resizeKeyboardWord() {
        if (!keyboard.open) return;
        const word = document.getElementById("keyboard-word");
        word.style.fontSize = "24px";
        const available = word.clientWidth;
        if (available > 0 && word.scrollWidth > available) {
            word.style.fontSize = (24 * available / word.scrollWidth) + "px";
            while (word.scrollWidth > word.clientWidth && parseFloat(word.style.fontSize) > 1) {
                word.style.fontSize = (parseFloat(word.style.fontSize) - 0.1) + "px";
            }
        }
    }

    function syncState() {
        const questionWord = area.querySelector('[data-quiz-state="question"] .quiz-word')?.textContent.trim();
        document.getElementById("keyboard-word").textContent = questionWord ? "問題：" + questionWord : "";
        const state = area.querySelector("[data-quiz-state]");
        document.body.dataset.background = state?.dataset.vocabType || "mixed";
        document.getElementById("page-title").textContent = state?.dataset.quizState === "summary" ? "結果" : "クイズ";
        area.querySelectorAll(".kana-display").forEach(resizeKana);
        renderAnswer();
        decorateKeys();
        resizeWords();
        area.querySelectorAll("dialog").forEach(d => d.addEventListener("click", e => {
            if (e.target !== d) return;
            const r = d.getBoundingClientRect();
            if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) d.close();
        }));
    }
    area.addEventListener("submit", async e => {
        const form = e.target.closest(".quiz-ajax-form");
        if (!form) return;
        e.preventDefault();
        if (busy) return;
        if (form.id === "answer-form" && !document.getElementById("answer-input").value) {
            window.uiToast("何も答えないと進めないよ");
            return;
        }
        busy = true;
        area.setAttribute("aria-busy", "true");
        const data = new FormData(form);
        const tips = document.getElementById("tips-count");
        if (tips && !data.has("tips_count")) data.set("tips_count", tips.value);
        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: data,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });
            if (response.redirected) {
                location.assign(response.url);
                return;
            }
            const payload = await response.json();
            if (!payload.success) {
                const errors = Object.values(payload.errors || {}).flat().map(error => error.message).join(" ");
                window.uiToast(errors || "送信できませんでした。もう一度お試しください。", "error");
                return;
            }
            if (typeof payload.main_html !== "string") throw new Error("Missing quiz markup");
            keyboard.close();
            area.innerHTML = payload.main_html;
            panel.innerHTML = payload.input_panel_html || "";
            syncState();
            area.querySelector(".quiz-content-heading")?.focus({
                preventScroll: true
            });
        } catch (error) {
            window.uiToast("通信に失敗しました。回答を保持しています。もう一度お試しください。", "error");
        } finally {
            busy = false;
            area.removeAttribute("aria-busy");
        }
    });
    document.addEventListener("click", e => {
        if (e.target.closest("[data-show-keyboard]")) {
            keyboard.showModal();
            resizeKeyboardWord();
            renderAnswer();
            return;
        }
        if (e.target.closest("[data-keyboard-backdrop]")) {
            keyboard.close();
            return;
        }
        const key = e.target.closest("[data-kana]");
        if (key) {
            if (key.dataset.kana === "hide") {
                keyboard.close();
                return;
            }
            const answer = document.getElementById("answer-input");
            if (!answer) return;
            const value = handleAnswerInput(answer.value, key.dataset.kana);
            if (value.length <= 25) {
                answer.value = value;
                renderAnswer();
            } else window.uiToast("回答は25文字以内で入力してください。");
        }
        if (e.target.closest("[data-hint]")) {
            const answer = document.getElementById("answer-input");
            const correct = document.getElementById("answer-form").dataset.correctAnswer;
            const tips = document.getElementById("tips-count");
            if (answer.value === correct) {
                window.uiToast("まだ答えられないの？");
                return;
            }
            if (Number(tips.value) >= 50) {
                window.uiToast("ヒントはこれ以上使えません。");
                return;
            }
            answer.value = applyAnswerTips(correct, answer.value);
            tips.value = Number(tips.value) + 1;
            renderAnswer();
        }
    });
    window.addEventListener("resize", () => {
        resizeKeyboardWord();
        renderAnswer();
        resizeWords();
        area.querySelectorAll(".kana-display").forEach(resizeKana);
    });
    syncState();
    document.fonts.ready.then(() => {
        resizeWords();
        resizeKeyboardWord();
    });
})();

function applyAnswerTips(correctAnswer, currentInput) {
    if (currentInput === correctAnswer) return currentInput;
    if (currentInput.length > correctAnswer.length) return currentInput.slice(0, correctAnswer.length);
    for (let index = 0; index < currentInput.length; index++) {
        if (currentInput[index] !== correctAnswer[index]) {
            return currentInput.slice(0, index) + correctAnswer[index] + currentInput.slice(index + 1);
        }
    }
    return currentInput + correctAnswer[currentInput.length];
}

function quizAreaHandler(){
    const quizAreaContainer = document.getElementById('quiz-area-container')
    const quizInputPanelContainer = document.getElementById('quiz-input-panel-container')
    if(!quizAreaContainer || !quizInputPanelContainer){
        return;
    }
    let on_handling = false;
    quizAreaContainer.addEventListener('submit', function(e){
        if(!e.target.classList.contains('quiz-ajax-form')){
            return;
        }
        e.preventDefault();
        if(on_handling === true){
            return;
        }
        on_handling = true
        const form = e.target;
        const formData = new FormData(form);
        const tipsCounter = document.getElementById("tips-count");
        if(tipsCounter && !formData.has("tips_count")){
            formData.set("tips_count", tipsCounter.value);
        }
        fetch(form.action, {
            method: form.method,
            body: formData,
            headers:{
                'X-Requested-With': "XMLHttpRequest"
            }
        })
        .then(async res => {
            const contentType = res.headers.get("content-type") || "";

            if(!contentType.includes("application/json")){
                throw new Error(
                    `Expected JSON, received ${contentType}`
                );
            }

            return res.json();
        })
        .then(data => {
            const errorContainer = document.getElementById("quiz-error-message");

            if(data.success === false){
                renderFormErrorMessages(data.errors, errorContainer);
                return;
            }

            if (data.success !== true) {
                throw new Error(
                    "Invalid quiz response: missing valid success state"
                );
            }

            errorContainer.replaceChildren();

            quizAreaContainer.innerHTML = data.main_html;
            quizInputPanelContainer.innerHTML = data.input_panel_html;
            quizAreaContainer.querySelector(".quiz-content-heading")?.focus();
        })
        .catch(error => {
            console.error(error);

            const errorContainer =
                document.getElementById("quiz-error-message");

            errorContainer.textContent =
                "エラーが発生しました。ページを再読み込みして、もう一度お試しください。";
        })
        .finally(() => {
            on_handling = false;
        });
    })
}

function getErrorLabel(fieldName){
    const labels = {
        answer: "回答",
        tips_count: "ヒント使用回数",
        user_vocab_id: "問題",
    };
    return labels[fieldName] ?? fieldName;
}

function renderFormErrorMessages(errors, container){
    container.replaceChildren();

    Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
        fieldErrors.forEach(error => {
            const errorMsg = document.createElement("p");

            if (fieldName === "__all__"){
                errorMsg.textContent = error.message;
            } else {
                const label = getErrorLabel(fieldName);
                errorMsg.textContent = `${label}: ${error.message}`;
            }

            container.appendChild(errorMsg);
        });
    });
}

function answerAreaReactionHandler(){
    document.addEventListener('click', function(e){
        if(!e.target.classList.contains('kana-key')){
            return;
        }

        const answerInput = document.getElementById("answer-input");
        const answerDisplay = document.getElementById("answer-display");

        if(!answerInput || !answerDisplay){
            return;
        }
        if(e.target.dataset.kana === "hide"){
            const showInputPanelButton = document.getElementById("show-input-panel-button");
            const inputPanelContainer = document.getElementById("quiz-input-panel-container");

            inputPanelContainer.hidden = true;
            showInputPanelButton.hidden = false;
        }else{
            let newAnswer = handleAnswerInput(answerInput.value, e.target.dataset.kana);
            answerInput.value = newAnswer;
            answerDisplay.textContent = newAnswer;
        }

    });
}

function inputPanelToggleHandler(){
    const showInputPanelButton = document.getElementById("show-input-panel-button");
    const inputPanelContainer = document.getElementById("quiz-input-panel-container");
    if(!showInputPanelButton || !inputPanelContainer){
        return;
    }
    showInputPanelButton.addEventListener('click', function(){
        inputPanelContainer.hidden = false;
        showInputPanelButton.hidden = true;
    });
}

function tipsHandler(){
    document.addEventListener('click', function(e){
        if(!e.target.classList.contains('tips-button')){
            return;
        }
        const form = e.target.closest(".quiz-ajax-form");
        if(!form){
            return;
        }
        const correctAnswer = form.dataset.correctAnswer;
        if(!correctAnswer){
            return;
        }
        const tipsCounter = document.getElementById('tips-count');
        const answerInput = document.getElementById("answer-input");
        const answerDisplay = document.getElementById("answer-display");
        if(!tipsCounter || !answerInput || !answerDisplay){
            return;
        }
        let afterTipAnswer = applyAnswerTips(correctAnswer, answerInput.value);
        tipsCounter.value = Number(tipsCounter.value) + 1;
        answerInput.value = afterTipAnswer;
        answerDisplay.textContent = afterTipAnswer;
    });
}

function applyAnswerTips(correctAnswer, currentInput){
    let afterTipAnswer = "";
    // The user has already entered the correct answer.
    if(currentInput === correctAnswer){
        afterTipAnswer = currentInput;
        return afterTipAnswer;
    }
    // The current input is longer than the correct answer.
    if(currentInput.length > correctAnswer.length){
        afterTipAnswer = currentInput.slice(0, correctAnswer.length);
        return afterTipAnswer
    }

    // The current input is empty.
    if(currentInput === ""){
        afterTipAnswer = correctAnswer.slice(0,1);
        return afterTipAnswer;
    }

    // The current input has the same length as the correct answer, but is not correct.
    // Or the current input is shorter than the correct answer, but is not a correct prefix.
    if(((currentInput != correctAnswer) && (currentInput.length == correctAnswer.length))
        || ((currentInput.length < correctAnswer.length) && (currentInput != correctAnswer.slice(0,currentInput.length)))){
        let firstDiffPos = 0;
        for(let idx = 0; idx < currentInput.length; idx++){
            if(currentInput[idx] != correctAnswer[idx]){
                firstDiffPos = idx;
                break;
            }
        }

        if(firstDiffPos == 0){
            afterTipAnswer = correctAnswer.slice(0,1) + currentInput.slice(1,currentInput.length);
        }else{
            afterTipAnswer = currentInput.slice(0, firstDiffPos)
                                + correctAnswer.slice(firstDiffPos, firstDiffPos+1)
                                + currentInput.slice(firstDiffPos+1, currentInput.length);
        }
        return afterTipAnswer;
    }
    // The current input is a correct prefix, so reveal the next kana.
    if(currentInput.length < correctAnswer.length){
        afterTipAnswer = currentInput + correctAnswer.slice(currentInput.length, currentInput.length+1);
        return afterTipAnswer;
    }
}

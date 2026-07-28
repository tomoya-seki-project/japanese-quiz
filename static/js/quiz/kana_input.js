function handleAnswerInput(currentAnswer, userInput){
    let outputAnswer = currentAnswer;
    switch(userInput){
        case "\"": outputAnswer = handleDakuten(currentAnswer); break;
        case "。": outputAnswer = handleHandakuten(currentAnswer); break;
        case "小": outputAnswer = handleSmallKana(currentAnswer); break;
        // case "hide":  break;
        case "backspace": outputAnswer = handleBackspace(currentAnswer); break;
        default: outputAnswer += userInput;
    }
    return outputAnswer;
}

function handleDakuten(currentAnswer){
    const dakutenTargets = ["か", "き", "く", "け", "こ",
                            "さ", "し", "す", "せ", "そ",
                            "た", "ち", "つ", "て", "と",
                            "は", "ひ", "ふ", "へ", "ほ",
                            "カ", "キ", "ク", "ケ", "コ",
                            "サ", "シ", "ス", "セ", "ソ",
                            "タ", "チ", "ツ", "テ", "ト",
                            "ハ", "ヒ", "フ", "ヘ", "ホ"];
    const dakutenResult = ["が", "ぎ", "ぐ", "げ", "ご",
                           "ざ", "じ", "ず", "ぜ", "ぞ",
                           "だ", "ぢ", "づ", "で", "ど",
                           "ば", "び", "ぶ", "べ", "ぼ",
                           "ガ", "ギ", "グ", "ゲ", "ゴ",
                           "ザ", "ジ", "ズ", "ゼ", "ゾ",
                           "ダ", "ヂ", "ヅ", "デ", "ド",
                           "バ", "ビ", "ブ", "ベ", "ボ"];
    let lastChar = currentAnswer.slice(-1);
    return currentAnswer.slice(0, -1) + checkAndChangeChar(lastChar, dakutenTargets, dakutenResult);
}
function handleHandakuten(currentAnswer){
    const handakutenTargets = ["は", "ひ", "ふ", "へ", "ほ",
                               "ハ", "ヒ", "フ", "ヘ", "ホ"];
    const handakutenResult = ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ",
                               "パ", "ピ", "プ", "ペ", "ポ"];
    let lastChar = currentAnswer.slice(-1);
    return currentAnswer.slice(0, -1) + checkAndChangeChar(lastChar, handakutenTargets, handakutenResult);
}
function handleSmallKana(currentAnswer){
    const smallKanaTargets = ["や", "ゆ", "よ", "つ",
                              "ヤ", "ユ", "ヨ",
                              "ア", "イ", "ウ", "エ", "オ",
                              "ケ",];
    const smallKanaResult = ["ゃ", "ゅ", "ょ", "っ",
                              "ャ", "ュ", "ョ",
                              "ァ", "ィ", "ゥ", "ェ", "ォ",
                              "ヶ",];
    let lastChar = currentAnswer.slice(-1);
    return currentAnswer.slice(0, -1) + checkAndChangeChar(lastChar, smallKanaTargets, smallKanaResult);
}
function checkAndChangeChar(lastChar, targetList, resultList){
    for(var idx = 0; idx < targetList.length; idx++){
        if(lastChar === targetList[idx]){
            return resultList[idx];
        }
    }
    for(var idx = 0; idx < resultList.length; idx++){
        if(lastChar === resultList[idx]){
            return targetList[idx];
        }
    }
    return lastChar;
}
function handleBackspace(currentAnswer){
    if(currentAnswer.length > 0){
        return currentAnswer.slice(0,-1);
    }else{
        return currentAnswer
    }
}
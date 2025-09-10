document.addEventListener("DOMContentLoaded", function() {

    //1. 암호별 박스 밝기 조절
    const currentId = document.body.getAttribute("data-current");
    const boxes = document.querySelectorAll(".cipherBox");
    const keyBox = document.querySelector('#keyBox');

    boxes.forEach(box => {
        if (currentId === "index") { // 인덱스 페이지면 전부 밝게
            box.classList.add("active");
        } else if (box.getAttribute("data-id") === currentId) { // 현재 선택된 암호만 밝게
            box.classList.add("active");
        } else { // 나머지는 어둡게
            box.classList.add("inactive");
        }
    });

    //polybius 암호일 경우 keyBox 제거
        if (currentId === "polybius") {
            keyBox.style.display = "none";
        } else {
            keyBox.style.display = "block";
        }

    //2. 페이지 정보에 따라 ENC/DEC 버튼 밝기 조절
    const encDecButtons = document.querySelectorAll(".encORdec");
    encDecButtons.forEach(btn => {
        if (currentId === "index") { // index 페이지: 어둡게
            btn.classList.add("inactive");
            btn.classList.remove("active");
            btn.setAttribute("disabled", "");
        } 
        else { // 암호별  페이지: 밝게
            btn.classList.add("active");
            btn.classList.remove("inactive");
            btn.removeAttribute("disabled");
        }
    });

     //3. ENC/DEC 클릭 이후 이벤트 - ENc/DEC 버튼 밝기 조절 & inputBox, keyBox 밝기 조절
    const encBtn = document.querySelector('input.encORdec[value="ENC"]');
    const decBtn = document.querySelector('input.encORdec[value="DEC"]');
    const inputBox = document.querySelector('textarea[name="inputBox"]');
    const outputBox = document.querySelector('textarea[name="outputBox"]');
    const goBtn = document.querySelector('input[type="submit"]');

    function activateBoxes(mode) {
        inputBox.removeAttribute("readonly");       //readonly 해제
        keyBox.removeAttribute("readonly");

        inputBox.classList.add("active");       //클래스 추가
        keyBox.classList.add("active");

        ['#inputBox', '#keyBox'].forEach(selector => {
            document.querySelector(selector).style.color = "rgb(78, 214, 255)";
        });

        if (mode === "ENC") {       //ENC 버튼을 선택할 경우 - ENC, DEC 버튼 각각 모드 바꾸기
            encBtn.classList.add("active");
            encBtn.classList.remove("inactive");
            decBtn.classList.remove("active");
            decBtn.classList.add("inactive");

            //placeholder - inputBox 변경
            inputBox.placeholder = "Enter plaintext here. (alphabets only)";
            //placeholder - key 변경
            if ( currentId === "caesar" || currentId === "railfence") { 
                keyBox.placeholder = "Enter key here. (numbers only)";
            } 
            else {
                keyBox.placeholder = "Enter key here. (alphabets only)";
            } 

        }
        else {           //DEC 버튼을 선택할 경우 - ENC, DEC 버튼 각각 모드 바꾸기
            decBtn.classList.add("active");
            decBtn.classList.remove("inactive");
            encBtn.classList.remove("active");
            encBtn.classList.add("inactive");
            
            //placeholder - inputBox 변경
            if (currentId === "polybius") {
                inputBox.placeholder = "Enter ciphertext here. (numbers only)";
            } 
            else {
                inputBox.placeholder = "Enter ciphertext here. (alphabets only)";
            } 
            //placeholder - key 변경
            if (currentId === "caesar" || currentId === "railfence") {
                keyBox.placeholder = "Enter key here. (numbers only)";
            } 
            else {
                keyBox.placeholder = "Enter key here. (alphabets only)";
            } 
        }


        goBtn.style.borderColor = "rgb(78, 214, 255)";
        goBtn.style.color = "rgb(78, 214, 255)";
        goBtn.removeAttribute("disabled");

        //outputBox 초기화
        outputBox.setAttribute("readonly", "");        // 다시 읽기 전용으로
        outputBox.classList.remove("active");          // 클래스 제거
        outputBox.style.color = "";                    // 글자색 초기화 (CSS 기본값)
        outputBox.style.borderColor = "";             // 테두리 초기화
        outputBox.value = "";
    }

    encBtn.addEventListener("click", () => activateBoxes("ENC"));
    decBtn.addEventListener("click", () => activateBoxes("DEC"));


    //4. Go 버튼 클릭에 대한 이벤트 - outputBox 밝기 조절
    goBtn.addEventListener("click", function(event) {
        event.preventDefault(); // form 전송 방지

        const text = inputBox.value;
        const key = keyBox.value;
        const mode = encBtn.classList.contains("active") ? "ENC" : "DEC";

        let url = "";
        if (currentId === "caesar") url = "/caesar/";
        else if (currentId === "vigenere") url = "/vigenere/";
        else if (currentId === "polybius") url = "/polybius/";
        else if (currentId === "railfence") url = "/railfence/";


        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text, key: key, mode: mode })
        })
        .then(response => response.json())
        .then(data => {
            outputBox.removeAttribute("readonly");
            outputBox.classList.add("active");
            outputBox.style.color = "rgb(78, 214, 255)";
            outputBox.style.borderColor = "rgb(78, 214, 255)";
            outputBox.value = data.result;
        })
        .catch(err => {
            outputBox.value = "Error: " + err;
        });
    });
});


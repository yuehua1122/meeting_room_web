const idInput = document.getElementById("id"); 
const checkButton = document.getElementById("check"); // 獲取禁用按鈕

idInput.addEventListener("input", validateID);

function validateID() {
    const idPattern = /^[A-Z][0-9]{7}$/; // 英文字母+7位數字
    if (!idPattern.test(idInput.value) || idInput.value === "") {
        idInput.style.color = "red"; // 設置文字顏色為紅色
        checkButton.disabled = true; // 禁用確認按鈕
        checkButton.style.backgroundColor = "#bac4c3";
    } else {
        idInput.style.color = "black"; // 恢復文字顏色為黑色
        checkButton.disabled = false; // 啟用確認按鈕
        checkButton.style.backgroundColor = "#8af4e9";
    }
}

// 在頁面加載時執行一次以處理初始狀態
validateID();
// 獲取需要動態更新的選擇框
function checkReservation() {
    const startYear = parseInt(document.getElementById("StartYear").value);
    const startMonth = parseInt(document.getElementById("StartMonth").value);
    const startDate = parseInt(document.getElementById("StartDate").value);
    const startHour = parseInt(document.getElementById("StartHour").value);
    const startMinute = parseInt(document.getElementById("StartMinute").value);

    const endYear = parseInt(document.getElementById("EndYear").value);
    const endMonth = parseInt(document.getElementById("EndMonth").value);
    const endDate = parseInt(document.getElementById("EndDate").value);
    const endHour = parseInt(document.getElementById("EndHour").value);
    const endMinute = parseInt(document.getElementById("EndMinute").value);

    document.getElementById("reservation").textContent = "";
    document.getElementById("idDisplay").textContent = "";
    document.getElementById("roomDisplay").textContent = "";
    document.getElementById("startDisplay").textContent = "";
    document.getElementById("endDisplay").textContent = "";

    //檢查是否"結束"時間大於"開始"時間
    if (
        startYear > endYear ||
        (startYear === endYear &&
            (startMonth > endMonth ||
                (startMonth === endMonth &&
                    (startDate > endDate ||
                        (startDate === endDate &&
                            (startHour > endHour ||
                                (startHour === endHour && startMinute >= endMinute)
                            )
                        )
                    )
                )
            )
        )
    ) {
        document.getElementById("reservation").textContent = "錯誤：結束時間必須大於開始時間。";
        document.getElementById("reservation").style.color = "red";
        checkButton.disabled = true;  // 禁用送出按鈕
        document.getElementById("rForm").reset();
    }
    
    
}
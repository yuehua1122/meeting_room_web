const StartYear = document.getElementById("StartYear");
const StartMonth = document.getElementById("StartMonth");
const StartDate = document.getElementById("StartDate");
const StartHour = document.getElementById("StartHour");
const StartMinute = document.getElementById("StartMinute");
const EndYear = document.getElementById("EndYear");
const EndMonth = document.getElementById("EndMonth");
const EndDate = document.getElementById("EndDate");
const EndHour = document.getElementById("EndHour");
const EndMinute = document.getElementById("EndMinute");
const checkButton = document.getElementById("check"); // 獲取禁用按鈕

// 為所有日期和時間選擇框添加事件監聽器
StartYear.addEventListener("change", checkDates);
StartMonth.addEventListener("change", checkDates);
StartDate.addEventListener("change", checkDates);
StartHour.addEventListener("change", checkDates);
StartMinute.addEventListener("change", checkDates);
EndYear.addEventListener("change", checkDates);
EndMonth.addEventListener("change", checkDates);
EndDate.addEventListener("change", checkDates);
EndHour.addEventListener("change", checkDates);
EndMinute.addEventListener("change", checkDates);

// 在頁面加載時執行一次以設置初始狀態
checkDates();


// 獲取需要動態更新的選擇框
function checkDates() {
    // 獲取開始和結束日期的各個部分的值
    const startYear = parseInt(StartYear.value);
    const startMonth = parseInt(StartMonth.value);
    const startDate = parseInt(StartDate.value);
    const startHour = parseInt(StartHour.value);
    const startMinute = parseInt(StartMinute.value);

    const endYear = parseInt(EndYear.value);
    const endMonth = parseInt(EndMonth.value);
    const endDate = parseInt(EndDate.value);
    const endHour = parseInt(EndHour.value);
    const endMinute = parseInt(EndMinute.value);

    // 創建開始和結束的 Date 對象
    const startTime = new Date(startYear, startMonth - 1, startDate, startHour, startMinute);
    const endTime = new Date(endYear, endMonth - 1, endDate, endHour, endMinute);

    // 獲取當前時間
    var currentTime = new Date();

    // 比較日期和時間
    if (startTime >= endTime || startTime < currentTime) {
        // 如果開始時間大於或等於結束時間，或者開始時間大於當前時間，禁用按鈕
        checkButton.disabled = true;
        checkButton.style.backgroundColor = "#bac4c3";
    } else {
        // 否則，啟用按鈕
        checkButton.disabled = false;
        checkButton.style.backgroundColor = "#8af4e9";
    }
}

// 獲取需要動態更新的選擇框
const startYearSelect = document.getElementById("StartYear");
const startMonthSelect = document.getElementById("StartMonth");
const startDateSelect = document.getElementById("StartDate");
const startHourSelect = document.getElementById("StartHour");
const startMinuteSelect = document.getElementById("StartMinute");

const endYearSelect = document.getElementById("EndYear");
const endMonthSelect = document.getElementById("EndMonth");
const endDateSelect = document.getElementById("EndDate");
const endHourSelect = document.getElementById("EndHour");
const endMinuteSelect = document.getElementById("EndMinute");

// 獲取當前日期和時間
const currentDateTime = new Date();
const currentYear = currentDateTime.getFullYear();
const currentMonth = currentDateTime.getMonth() + 1; // 月份是從0開始的，所以要加1
const currentDay = currentDateTime.getDate();
const currentHour = currentDateTime.getHours();
const currentMinute = currentDateTime.getMinutes();

// 在年份選擇框上添加事件監聽器
startYearSelect.addEventListener("change", updateStartDateOptions);
endYearSelect.addEventListener("change", updateEndDateOptions);

// 頁面加載時初始化
updateYearOptions();
updateStartDateOptions();
updateEndDateOptions();

// 動態生成年份選項
function updateYearOptions() {
    // 定義年份範圍
    const startYear = currentYear;
    const endYear = startYear + 5;

    // 清空年份選項
    clearOptions(startYearSelect);
    clearOptions(endYearSelect);

    // 生成年份選項
    for (let year = startYear; year <= endYear; year++) {
        addOption(startYearSelect, year);
        addOption(endYearSelect, year);
    }
}

// 在月份選擇框上添加事件監聽器
startMonthSelect.addEventListener("change", updateStartDateOptions);
endMonthSelect.addEventListener("change", updateEndDateOptions);

// 初始化頁面時觸發一次更新
updateStartDateOptions();
updateEndDateOptions();

// 定義更新日期選項的函數
function updateDateOptions(yearSelect, monthSelect, dateSelect, selectedDate) {
    const selectedYear = parseInt(yearSelect.value);
    const selectedMonth = parseInt(monthSelect.value);

    // 計算選定月份的天數
    const daysInMonth = getDaysInMonth(selectedYear, selectedMonth);

    // 清空日期選項
    clearOptions(dateSelect);

    // 生成日期選項
    for (let i = 1; i <= daysInMonth; i++) {
        addOption(dateSelect, i);
    }

    // 設定預設選擇日期
    if (selectedDate) {
        dateSelect.value = selectedDate;
    }
}

// 定義更新小時和分鐘選項的函數
function updateTimeOptions(hourSelect, minuteSelect, selectedHour, selectedMinute) {
    // 清空小時和分鐘選項
    clearOptions(hourSelect);
    clearOptions(minuteSelect);

    // 生成小時選項（00 到 23）
    for (let i = 0; i < 24; i++) {
        addOption(hourSelect, i);
    }

    // 生成分鐘選項（00 到 50，每隔 10 分鐘）
    for (let i = 0; i < 60; i += 10) {
        addOption(minuteSelect, i);
    }

    // 設定預設選擇時間
    if (selectedHour) {
        hourSelect.value = selectedHour;
    }
    if (selectedMinute) {
        minuteSelect.value = selectedMinute;
    }
}

// 定義更新起始日期選項的函數
function updateStartDateOptions() {
    const selectedStartYear = parseInt(startYearSelect.value);
    const selectedStartMonth = parseInt(startMonthSelect.value);

    // 清空日期、小時和分鐘選項
    clearOptions(startDateSelect);
    clearOptions(startHourSelect);
    clearOptions(startMinuteSelect);

    // 動態生成日期選項
    updateDateOptions(startYearSelect, startMonthSelect, startDateSelect, currentDay);

    // 動態生成小時和分鐘選項
    updateTimeOptions(startHourSelect, startMinuteSelect, currentHour, getNearestMinute(currentMinute));
}

// 定義更新結束日期選項的函數
function updateEndDateOptions() {
    const selectedEndYear = parseInt(endYearSelect.value);
    const selectedEndMonth = parseInt(endMonthSelect.value);

    // 清空日期、小時和分鐘選項
    clearOptions(endDateSelect);
    clearOptions(endHourSelect);
    clearOptions(endMinuteSelect);

    // 動態生成日期選項
    updateDateOptions(endYearSelect, endMonthSelect, endDateSelect, currentDay);

    // 動態生成小時和分鐘選項
    updateTimeOptions(endHourSelect, endMinuteSelect, currentHour + 1, getNearestMinute(currentMinute));
}

// 取得離自己最近的10分鐘
function getNearestMinute(currentMinute) {
    if(currentMinute<50){
        const remainder = currentMinute % 10;
        return remainder === 0 ? currentMinute : currentMinute + (10 - remainder);
    }
    else{
        const remainder  = 0;
        return remainder ;
    }
}

// 判斷是否為閏年的函數
function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
}

// 獲取指定年份和月份的天數
function getDaysInMonth(year, month) {
    if ([4, 6, 9, 11].includes(month)) {
        return 30;
    } else if (month === 2) {
        return isLeapYear(year) ? 29 : 28;
    } else {
        return 31;
    }
}

// 清空選擇框的選項
function clearOptions(select) {
    select.innerHTML = '';
}

// 添加選項到選擇框
function addOption(select, value) {
    const option = document.createElement("option");
    option.value = value;
    option.text = value < 10 ? `0${value}` : `${value}`; // 若數字小於10，在前面補0
    select.appendChild(option);
}

// 設定預設選擇日期
startYearSelect.value = currentYear;
startMonthSelect.value = currentMonth;
endYearSelect.value = currentYear;
endMonthSelect.value = currentMonth;
updateStartDateOptions();
updateEndDateOptions();
endDateSelect.value = currentDay;
startDateSelect.value = currentDay;
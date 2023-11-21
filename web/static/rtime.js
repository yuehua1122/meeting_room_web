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

// 獲取當前時間
const currentDateTime = new Date();
const currentYear = currentDateTime.getFullYear();
const currentMonth = currentDateTime.getMonth() + 1; // 月份是從0開始的，所以要加1
const currentDay = currentDateTime.getDate();

// 在年份選擇框上添加事件監聽器
startYearSelect.addEventListener("change", updateStartDateOptions);
endYearSelect.addEventListener("change", updateEndDateOptions);

// 動態生成年份選項
function updateYearOptions() {
    // 先清空年份年分
    startYearSelect.innerHTML = '';
    endYearSelect.innerHTML = '';

    // 再生成年份選項
    for (let year = currentYear; year <= currentYear+5; year++) {
        const option = document.createElement("option");
        option.value = year;
        option.text = year;
        option.setAttribute("name", "start_hour"); // 設置 name 屬性
        startYearSelect.appendChild(option);
        endYearSelect.appendChild(option.cloneNode(true)); // 複製年份選項至結束年份的選項
    }
}

// 頁面加載時先更新一次
updateYearOptions();

// 在月份選擇框上添加事件監聽器
startMonthSelect.addEventListener("change", updateStartDateOptions);
endMonthSelect.addEventListener("change", updateEndDateOptions);

// 初始化頁面時觸發一次更新
updateStartDateOptions();
updateEndDateOptions();

// 判斷是否為閏年的函數
function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
}

// 定義更新日期選項的函數
function updateStartDateOptions() {
    // 清空日期、小時和分鐘選項
    startDateSelect.innerHTML = '';
    startHourSelect.innerHTML = '';
    startMinuteSelect.innerHTML = '';

    const selectedStartYear = parseInt(startYearSelect.value);
    // 獲取所選月份的值
    const selectedStartMonth = parseInt(startMonthSelect.value);

    // 起始月份動態生成日期選項
    let startDays = 31; // 默認為31天
    if (selectedStartMonth === 2) {
        // 如果所選的是二月
        if (isLeapYear(selectedStartYear)) {
            startDays = 29; // 閏年二月有29天
        } else {
            startDays = 28; // 平年二月有28天
        }
    } else if ([4, 6, 9, 11].includes(selectedStartMonth)) {
        // 4、6、9、11月每月30天
        startDays = 30;
    }

    for (let i = 1; i <= startDays; i++) {
        const option = document.createElement("option");
        option.text = i;
        option.setAttribute("name", "start_date"); // 設置 name 屬性
        startDateSelect.appendChild(option);
    }

    // 生成小時選項（00 到 23）
    for (let i = 0; i < 24; i++) {
        const option = document.createElement("option");
        const hourValue = i < 10 ? `0${i}` : `${i}`;
        option.value = hourValue;
        option.text = hourValue;
        option.setAttribute("name", "start_hour"); // 設置 name 屬性
        startHourSelect.appendChild(option);
    }

    // 生成分鐘選項（00 到 59，每隔 1 分鐘）
    for (let i = 0; i < 60; i ++) {
        const option = document.createElement("option");
        const minuteValue = i < 10 ? `0${i}` : `${i}`;//若分鐘小於10則在十位數字補0
        option.value = minuteValue;
        option.text = minuteValue;
        option.setAttribute("name", "start_minute"); // 設置 name 屬性
        startMinuteSelect.appendChild(option);
    }
    
}

function updateEndDateOptions() {
    endDateSelect.innerHTML = '';
    endHourSelect.innerHTML = '';
    endMinuteSelect.innerHTML = '';

    const selectedEndYear = parseInt(endYearSelect.value);
    const selectedEndMonth = parseInt(endMonthSelect.value);

    // 結束月份動態生成日期選項
    let endDays = 31; // 默認為31天
    if (selectedEndMonth == 2) {
        // 如果所選的是二月
        if (isLeapYear(selectedEndYear)) {
            endDays = 29; // 閏年二月有29天
        } else {
            endDays = 28; // 平年二月有28天
        }
    } else if ([4, 6, 9, 11].includes(selectedEndMonth)) {
        // 4、6、9、11月每月30天
        endDays = 30;
    }

    for (let i = 1; i <= endDays; i++) {
        const option = document.createElement("option");
        option.text = i;
        endDateSelect.appendChild(option);
    }

    // 生成小時選項（00 到 23）
    for (let i = 0; i < 24; i++) {
        const option = document.createElement("option");
        const hourValue = i < 10 ? `0${i}` : `${i}`;
        option.value = hourValue;
        option.text = hourValue;
        option.setAttribute("name", "end_hour"); // 設置 name 屬性
        endHourSelect.appendChild(option);
    }

    // 生成分鐘選項（00 到 59，每隔 1 分钟）
    for (let i = 0; i < 60; i ++) {
        const option = document.createElement("option");
        const minuteValue = i < 10 ? `0${i}` : `${i}`;//若分鐘小於10則在十位數字補0
        option.value = minuteValue;
        option.text = minuteValue;
        option.setAttribute("name", "end_minutem"); // 設置 name 屬性
        endMinuteSelect.appendChild(option);
    }
    
}

startYearSelect.value = currentYear;
endYearSelect.value = currentYear;
startMonthSelect.value = currentMonth;
endMonthSelect.value = currentMonth;
startDateSelect.value = currentDay;
endDateSelect.value = currentDay;

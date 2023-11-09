// 獲取需要動態更新的選擇框
const viewYearSelect = document.getElementById("viewYear");
const viewMonthSelect = document.getElementById("viewMonth");
const viewDateSelect = document.getElementById("viewDate");

const currentYear = new Date().getFullYear();

viewYearSelect.addEventListener("change", updateViewDateOptions);

// 動態生成年份選項
function updateYearOptions() {
    // 清空年份選項
    viewYearSelect.innerHTML = '';

    // 生成年份選項
    for (let year = currentYear; year <= currentYear+5; year++) {
        const option = document.createElement("option");
        option.value = year;
        option.text = year;
        viewYearSelect.appendChild(option);
    }
}

// 在頁面加載時更新一次
updateYearOptions();

// 在月份選擇框上添加事件監聽器
viewMonthSelect.addEventListener("change", updateViewDateOptions);

// 初始化頁面時觸發一次更新
updateViewDateOptions();

// 判斷是否為閏年的函數
function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
}

// 定義更新日期選項的函數
function updateViewDateOptions() {
    // 清空日期、小時和分鐘選項
    viewDateSelect.innerHTML = '';
    
    const selectedViewYear = parseInt(viewYearSelect.value);

    // 獲取所選月份的值
    const selectedViewMonth = parseInt(viewMonthSelect.value);

    // 起始月份動態生成日期選項
    let viewDays = 31; // 默認為31天
    if (selectedViewMonth === 2) {
        // 如果所選的是二月
        const currentYear = new Date().getFullYear(); // 獲取當前年份
        if (isLeapYear(selectedViewYear)) {
            viewDays = 29; // 閏年二月有29天
        } else {
            viewDays = 28; // 平年二月有28天
        }
    } else if ([4, 6, 9, 11].includes(selectedViewMonth)) {
        // 4、6、9、11月每月30天
        viewDays = 30;
    }

    for (let i = 1; i <= viewDays; i++) {
        const option = document.createElement("option");
        option.text = i;
        viewDateSelect.appendChild(option);
    }
}
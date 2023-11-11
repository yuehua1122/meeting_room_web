document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#mForm").addEventListener("submit", function (e) {
        e.preventDefault();  //阻止默認的表單提交行為
        const form = e.target;
        const formData = new FormData(form);
        fetch("/mdata", {
          method: "POST",
          body: formData,
        })
        .then(response => response.text())
        .then(data => {
          // 在此處理回應資料，可以顯示成功消息或執行其他操作
          const MessageLabel = document.getElementById("message3");
          const newMessage1 = data.replace( /&/g , "<br>");
          MessageLabel.innerHTML = newMessage1;   
        })
        .catch(error => {
          console.error("Error:", error);
        });
    });
});
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#dForm").addEventListener("submit", function (e) {
      e.preventDefault();  //阻止默認的表單提交行為
      const form = e.target;
      const formData = new FormData(form);
      fetch("/delete", {
        method: "POST",
        body: formData,
      })
      .then(response => response.text())
      .then(data => {
        // 在此處理回應資料，可以顯示成功消息或執行其他操作
        const MessageLabe2 = document.getElementById("message4");
        const newMessage2 = data.replace( /&/g , "<br>");
        MessageLabe2.innerHTML = newMessage2;   
      })
      .catch(error => {
        console.error("Error:", error);
      });
  });
});
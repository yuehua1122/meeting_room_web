document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#mForm").addEventListener("submit", function (e) {
        e.preventDefault();  //阻止默認的表單提交行為
        const form = e.target;
        const formData = new FormData(form);
        fetch("/mdata", {
          method: "POST",
          body: formData,
        })
        .then(response => response.json())
        .then(data => {
          // 在此處理回應資料，可以顯示成功消息或執行其他操作
          const MessageLabel = document.getElementById("message3");
          const newMessage1 = DOMPurify.sanitize(data.replace( /&/g , "<br>"));
          MessageLabel.innerHTML = newMessage1;   
        })
        .catch(error => {
          console.error("Error:", error);
        });
    });
});

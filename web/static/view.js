document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#vForm").addEventListener("submit", function (e) {
        e.preventDefault();  // 阻止默認的表單提交行為
        const form = e.target;
        const formData = new FormData(form);
        fetch("/vdata", {
          method: "POST",
          body: formData,
        })
        .then(response => response.text())
        .then(data => {
          // 在此處理回應資料，可以顯示成功消息或執行其他操作
          const MessageLabel = document.getElementById("message2");
          const newMessage = data.replace( /&/g , "<br>");
          MessageLabel.innerHTML = newMessage;          
        })
        .catch(error => {
          console.error("Error:", error);
        });
    });
});
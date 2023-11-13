document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#rForm").addEventListener("submit", function (e) {
        e.preventDefault();  //阻止默認的表單提交行為
        const form = e.target;
        const formData = new FormData(form);
        fetch("/rdata", {
          method: "POST",
          body: formData,
        })
        .then(response => response.json())
        .then(data => {
          // 在此處理回應資料，可以顯示成功消息或執行其他操作
          const MessageLabel = document.getElementById("message1");
          const newMessage = DOMPurify.sanitize(data.replace(/&amp;/g, "<br>"));
          MessageLabel.innerHTML = newMessage;    
        })
        .catch(error => {
          console.error("Error:", error);
        });
    });
});
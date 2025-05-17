document.addEventListener("DOMContentLoaded", function () {
  // Check if URL contains ?registered=1
  if (window.location.search.includes("registered=1")) {
    let popup = document.getElementById("registeration-success");
    popup.style.display = "block";
    setTimeout(function () {
      popup.style.display = "none";
    }, 2000);
  }
});

// Shows a registration success popup for 2 seconds if URL contains "registered=1"
// which means that the user has registered successfully.

document.addEventListener("DOMContentLoaded", function () {
  if (window.location.search.includes("registered=1")) {
    let popup = document.getElementById("registeration-success");
    popup.style.display = "block";
    setTimeout(function () {
      popup.style.display = "none";
    }, 2000);
  }
});

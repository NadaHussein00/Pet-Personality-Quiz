document.addEventListener("DOMContentLoaded", function () {
  // Check if URL contains ?registered=1
  if (window.location.search.includes("registered=1")) {
    let popup = document.getElementById("registeration-success");
    popup.style.display = "block";
    setTimeout(function () {
      popup.style.display = "none";
      // Optionally remove the query param from URL (for aesthetics)
      /*         if (window.history.replaceState) {
          const url = window.location.origin + window.location.pathname;
          window.history.replaceState({}, document.title, url);
        } */
    }, 2000);
  }
});

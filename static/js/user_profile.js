(function () {
  const profileEl = document.getElementById("profile-page-content");
  const username = profileEl.getAttribute("data-username");
  const firstName = profileEl.getAttribute("data-firstname");
  const quizHistoryJson = profileEl.getAttribute("data-quiz-history");
  const greetingEl = document.getElementById("greeting");

  // Helper to safely add event listener if element exists
  function addListener(id, event, handler) {
    const el = document.getElementById(id);
    if (el) {
      el.style.display = "inline-block"; // Show button when attaching listener
      el.addEventListener(event, handler);
    }
  }

  // Parse quiz history JSON safely
  let quizHistory = [];
  try {
    quizHistory = JSON.parse(quizHistoryJson);
  } catch (e) {
    console.error("Invalid quiz history JSON", e);
  }

  const localStorageKey = username + " hasLoggedInBefore";
  const sessionStorageKey = username + " sessionActive";

  const hasLoggedInBefore = localStorage.getItem(localStorageKey);
  const sessionActive = sessionStorage.getItem(sessionStorageKey);

  if (sessionActive) {
    // Same tab/session: show normal welcome
    greetingEl.textContent = `Welcome, ${firstName}!`;
  } else {
    // New tab/session
    if (hasLoggedInBefore) {
      greetingEl.textContent = `Welcome back, ${firstName}!`;
    } else {
      greetingEl.textContent = `Welcome, ${firstName}!`;
      localStorage.setItem(localStorageKey, "true");
    }
    // Mark session as active
    sessionStorage.setItem(sessionStorageKey, "true");
  }

  addListener("logout-btn", "click", function () {
    localStorage.removeItem(localStorageKey);
    sessionStorage.removeItem(sessionStorageKey);
    window.location.href = "/login";
  });

  addListener("edit-profile-btn", "click", function () {
    window.location.href =
      "/edit_profile?username=" + encodeURIComponent(username);
  });

  if (quizHistory.length === 0) {
    addListener("first-quiz-btn", "click", () => {
      window.location.href = "/quiz?username=" + encodeURIComponent(username);
    });
  } else {
    addListener("another-quiz-btn", "click", () => {
      window.location.href = "/quiz?username=" + encodeURIComponent(username);
    });
    addListener("view-quizzes-btn", "click", () => {
      window.location.href =
        "/quiz_history?username=" + encodeURIComponent(username);
    });
  }
})();

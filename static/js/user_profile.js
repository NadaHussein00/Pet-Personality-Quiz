document.addEventListener("DOMContentLoaded", function () {
  const profileEl = document.getElementById("profile-page-content");
  const username = profileEl.getAttribute("data-username");
  const firstName = profileEl.getAttribute("data-firstname");
  const quizHistoryJson = profileEl.getAttribute("data-quiz-history");
  const greetingEl = document.getElementById("greeting");
  const messageDiv = document.getElementById("message");


  const logoutBtn = document.getElementById("logout-btn");
  const editProfileBtn = document.getElementById("edit-profile-btn");
  const firstQuizBtn = document.getElementById("first-quiz-btn");
  const anotherQuizBtn = document.getElementById("another-quiz-btn");
  const viewQuizzesBtn = document.getElementById("view-quizzes-btn");


  let quizHistory = [];
  try {
    quizHistory = JSON.parse(quizHistoryJson);
  } catch (e) {
    messageDiv.className = "";
    messageDiv.classList.add("error");
    messageDiv.textContent = "Failed to load quiz history data.";
    messageDiv.style.display = "block";
  }

  const localStorageKey = username + " hasLoggedInBefore";
  const sessionStorageKey = username + " sessionActive";

  const hasLoggedInBefore = localStorage.getItem(localStorageKey);
  const sessionActive = sessionStorage.getItem(sessionStorageKey);

  if (sessionActive) {
    greetingEl.textContent = `Welcome, ${firstName}!`;
  } else {
    if (hasLoggedInBefore) {
      greetingEl.textContent = `Welcome back, ${firstName}!`;
    } else {
      greetingEl.textContent = `Welcome, ${firstName}!`;
      localStorage.setItem(localStorageKey, "true");
    }
    sessionStorage.setItem(sessionStorageKey, "true");
  }

  
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem(localStorageKey);
    sessionStorage.removeItem(sessionStorageKey);
    window.location.href = "/petsona/login";
  });

  editProfileBtn.addEventListener("click", () => {
    window.location.href =
      "/petsona/edit_profile?username=" + encodeURIComponent(username);
  });

  firstQuizBtn.addEventListener("click", () => {
    window.location.href = "/petsona/quiz?username=" + encodeURIComponent(username);
  });

  anotherQuizBtn.addEventListener("click", () => {
    window.location.href = "/petsona/quiz?username=" + encodeURIComponent(username);
  });

  viewQuizzesBtn.addEventListener("click", () => {
    window.location.href =
      "/petsona/quiz_history?username=" + encodeURIComponent(username);
  });  
  
  
  // Show/hide quiz buttons based on quiz history length
  if (quizHistory.length === 0) {
    firstQuizBtn.style.display = "inline-block";
    anotherQuizBtn.style.display = "none";
    viewQuizzesBtn.style.display = "none";
  } else {
    firstQuizBtn.style.display = "none";
    anotherQuizBtn.style.display = "inline-block";
    viewQuizzesBtn.style.display = "inline-block";
  }
});

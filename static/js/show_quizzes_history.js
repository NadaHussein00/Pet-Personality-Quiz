document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("quiz-history-container");
  const quizHistoryJson = container.getAttribute("data-quiz-history");
  const username = container.getAttribute("data-username");

  const delteQuizModal = document.getElementById("delete-quiz-modal");
  const cancelDeleteBtn = document.getElementById("cancel-delete-btn");
  const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
  const closeDeleteModalBtn = document.getElementById("close-delete-modal-btn");

  let quizHistory = [];
  let quizCardToDelete = null;
  let deleteUrl = "";

  try {
    quizHistory = JSON.parse(quizHistoryJson);
  } catch (e) {
    console.error("Failed to parse quiz history JSON", e);
  }
  confirmDeleteBtn.addEventListener("click", () => {
    if (!quizCardToDelete || !deleteUrl) return;

    fetch(deleteUrl, { method: "DELETE" })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          quizCardToDelete.remove();
          console.log("Quiz deleted successfully");
        } else {
          console.error("Failed to delete quiz");
          alert("Failed to delete quiz history.");
        }
      })
      .finally(() => {
        delteQuizModal.style.display = "none";
        quizCardToDelete = null;
        deleteUrl = "";
      });
  });
  quizHistory.forEach((quiz) => {
    // Assuming quiz object has properties: date, dominant_trait, pet_type, description
    const deleteQuizHistoryBtn = document.createElement("button");
    const viewFullResultBtn = document.createElement("button");
    const modifyAnswersBtn = document.createElement("button");
    const card = document.createElement("div");

    card.className = "quiz-card";
    deleteQuizHistoryBtn.className = "manage-history-btns";
    viewFullResultBtn.className = "manage-history-btns";
    modifyAnswersBtn.className = "manage-history-btns";

    deleteQuizHistoryBtn.innerText = "Delete History";
    viewFullResultBtn.innerText = "View Full Result";
    modifyAnswersBtn.innerText = "Modify your answers";

    deleteQuizHistoryBtn.style.backgroundColor = "red";

    // Format date nicely (optional)
    const date = new Date(quiz.submitted_at);
    const formattedDate = date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
    });

    card.innerHTML = `
      <div class="quiz-date"><strong>Date:</strong> ${formattedDate}</div>
      <div class="quiz-pet-type"><strong>Pet Type:</strong> <span class="highlight">${quiz.pet_type}</span></div>
      <div class="quiz-dominant-trait"><strong>Dominant Trait:</strong> <span class="highlight">${quiz.dominant_trait}</span></div>
    `;

    card.appendChild(viewFullResultBtn);
    viewFullResultBtn.addEventListener("click", () => {
      /* const username = quizHistory.username; */
      const quizId = encodeURIComponent(quiz.submitted_at);
      window.location.href = `/quiz_result?username=${encodeURIComponent(
        username
      )}&quiz_id=${quizId}`;
    });

    card.appendChild(modifyAnswersBtn);
    modifyAnswersBtn.addEventListener("click", () => {
      const url = `/quiz?username=${encodeURIComponent(
        username
      )}&submitted_at=${encodeURIComponent(quiz.submitted_at)}`;
      window.location.href = url;
    });

    card.appendChild(deleteQuizHistoryBtn);
    deleteQuizHistoryBtn.addEventListener("click", () => {
      quizCardToDelete = card;
      deleteUrl = `/delete_quiz?username=${encodeURIComponent(
        username
      )}&quiz_id=${encodeURIComponent(quiz.submitted_at)}`;
      delteQuizModal.style.display = "flex";

      cancelDeleteBtn.addEventListener("click", () => {
        delteQuizModal.style.display = "none";
        quizCardToDelete = null;
        deleteUrl = "";
      });

      closeDeleteModalBtn.addEventListener("click", () => {
        delteQuizModal.style.display = "none";
      });
    });

    delteQuizModal.addEventListener("click", (event) => {
      // If the clicked element is the overlay itself (not the modal content)
      if (event.target === delteQuizModal) {
        delteQuizModal.style.display = "none"; // Close the modal
      }
    });

    if (quiz.is_modified) {
      const modifiedAtTag = document.createElement("span");
      modifiedAtTag.className = "modified-tag";

      // Format modified_at date nicely
      const modifiedOn = new Date(quiz.modified_at);
      const formattedDate = modifiedOn.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
      });

      modifiedAtTag.textContent = `Last modified on: ${formattedDate}`;
      modifiedAtTag.title = `Last modified on ${modifiedOn.toLocaleString()}`; // Tooltip with full datetime

      card.appendChild(modifiedAtTag);
    }

    container.appendChild(card);
  });
});

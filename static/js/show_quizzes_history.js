document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("quiz-history-container");
    const quizHistoryJson = container.getAttribute("data-quiz-history");
    const username = container.getAttribute("data-username");
  
    const deleteQuizModal = document.getElementById("delete-quiz-modal");
    const cancelDeleteBtn = document.getElementById("cancel-delete-btn");
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
    const closeDeleteModalBtn = document.getElementById("close-delete-modal-btn");
  
    const messageDiv = document.getElementById("message");
    
    let quizHistory = [];
    let quizCardToDelete = null;
    let deleteUrl = "";
  

    // Parse quiz history JSON safely and show error message if invalid
    try {
      quizHistory = JSON.parse(quizHistoryJson);
    } catch (e) {
        messageDiv.className = "";
        messageDiv.classList.add("error");
        messageDiv.textContent = "Failed to load quiz history data.";
        messageDiv.style.display = "block";
    }


     // Handle confirm delete button click to delete quiz history entry
    confirmDeleteBtn.addEventListener("click", () => {
      if (!quizCardToDelete || !deleteUrl) return;
  
      fetch(deleteUrl, { method: "DELETE" })
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            quizCardToDelete.remove();
          messageDiv.className = "";
          messageDiv.classList.add("success");
          messageDiv.textContent = "Quiz deleted successfully.";
          messageDiv.style.display = "block";
          } else {
            messageDiv.className = "";
          messageDiv.classList.add("error");
          messageDiv.textContent = "Failed to delete quiz history.";
          messageDiv.style.display = "block";
          }
        }).catch(() => {
            messageDiv.className = "";
            messageDiv.classList.add("error");
            messageDiv.textContent = "Network error while deleting quiz history.";
            messageDiv.style.display = "block";
          })
        .finally(() => {
            deleteQuizModal.style.display = "none";
          quizCardToDelete = null;
          deleteUrl = "";
        });
    });


    // Generate quiz history cards and attach event listeners for actions
    quizHistory.forEach((quiz) => {
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
      modifyAnswersBtn.innerText = "Modify Your Answers";
  
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


      // Navigate to quiz result page when clicking on card (excluding buttons)
      card.addEventListener("click", (event) => {
        if (event.target.tagName.toLowerCase() === "button") return;
    
        const quizId = encodeURIComponent(quiz.submitted_at);
        window.location.href = `/petsona/quiz_result?username=${encodeURIComponent(
          username
        )}&quiz_id=${quizId}`;
      });
  

      // Navigate to full result page on button click
      card.appendChild(viewFullResultBtn);
      viewFullResultBtn.addEventListener("click", () => {
        const quizId = encodeURIComponent(quiz.submitted_at);
        window.location.href = `/petsona/quiz_result?username=${encodeURIComponent(
          username
        )}&quiz_id=${quizId}`;
      });
  

      // Navigate to edit quiz page on button click
      card.appendChild(modifyAnswersBtn);
      modifyAnswersBtn.addEventListener("click", () => {
        const url = `/petsona/edit_quiz?username=${encodeURIComponent(
          username
        )}&submitted_at=${encodeURIComponent(quiz.submitted_at)}`;
        window.location.href = url;
      });
  

      // Show delete confirmation modal on delete button click
      card.appendChild(deleteQuizHistoryBtn);
      deleteQuizHistoryBtn.addEventListener("click", () => {
        quizCardToDelete = card;
        deleteUrl = `/petsona/delete_quiz?username=${encodeURIComponent(
          username
        )}&quiz_id=${encodeURIComponent(quiz.submitted_at)}`;
        deleteQuizModal.style.display = "flex";
  

        // Cancel delete hides modal and resets state
        cancelDeleteBtn.addEventListener("click", () => {
            deleteQuizModal.style.display = "none";
          quizCardToDelete = null;
          deleteUrl = "";
        });
  

        // Close modal button hides modal
        closeDeleteModalBtn.addEventListener("click", () => {
            deleteQuizModal.style.display = "none";
        });
      });


      // Close modal when clicking outside modal content 
      deleteQuizModal.addEventListener("click", (event) => {
        if (event.target === deleteQuizModal) {
            deleteQuizModal.style.display = "none"; 
        }
      });

      
      // Show last modified date if quiz was modified
      if (quiz.is_modified) {
        const modifiedAtTag = document.createElement("span");
        modifiedAtTag.className = "modified-tag";

        const modifiedOn = new Date(quiz.modified_at);
        const formattedDate = modifiedOn.toLocaleDateString(undefined, {
          year: "numeric",
          month: "short",
          day: "numeric",
        });
  
        modifiedAtTag.textContent = `Last modified on: ${formattedDate}`;
        modifiedAtTag.title = `Last modified on ${modifiedOn.toLocaleString()}`; 
  
        card.appendChild(modifiedAtTag);
      }
  
      container.appendChild(card);
    });
  });

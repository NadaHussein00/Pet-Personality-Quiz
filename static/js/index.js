document.addEventListener("click", () => {
    const trialQuiz = document.getElementById("trial-quiz-btn");
    const trialQuizNoteModal = document.getElementById("trial-quiz-note-modal");
    const closeTrialQuiznoteBtn = document.getElementById(
      "close-trial-quiz-note-modal-btn"
    );
  
    // Show the trial quiz note modal when the trial quiz button is clicked
    trialQuiz.addEventListener("click", () => {
      trialQuizNoteModal.style.display = "block";
    });
  
    // Hide the trial quiz note modal when the close button is clicked
    closeTrialQuiznoteBtn.addEventListener("click", () => {
      trialQuizNoteModal.style.display = "none";
    });
  
     // Close the modal if clicking outside the modal content (on the overlay)
    trialQuizNoteModal.addEventListener("click", (event) => {
      if (event.target === trialQuizNoteModal) {
        trialQuizNoteModal.style.display = "none"; 
      }
    });
  });

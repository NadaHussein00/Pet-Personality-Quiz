document.addEventListener("click", () => {
  const trialQuiz = document.getElementById("trial-quiz-btn");
  const trialQuizNoteModal = document.getElementById("trial-quiz-note-modal");
  const closeTrialQuiznoteBtn = document.getElementById(
    "close-trial-quiz-note-modal-btn"
  );

  trialQuiz.addEventListener("click", () => {
    trialQuizNoteModal.style.display = "block";
  });

  closeTrialQuiznoteBtn.addEventListener("click", () => {
    trialQuizNoteModal.style.display = "none";
  });

  trialQuizNoteModal.addEventListener("click", (event) => {
    // If the clicked element is the overlay itself (not the modal content)
    if (event.target === trialQuizNoteModal) {
      trialQuizNoteModal.style.display = "none"; // Close the modal
    }
  });
});

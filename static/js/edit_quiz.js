document.addEventListener("DOMContentLoaded", async () => {
    const messageDiv = document.getElementById("message");
  
    const urlParams = new URLSearchParams(window.location.search);
    const username = urlParams.get("username");
    const submittedAt = urlParams.get("submitted_at");
  
    if (!username || !submittedAt) {
      return;
    }
  
    try {
      const response = await fetch(
        `/petsona/edit_quiz?username=${encodeURIComponent(username)}&submitted_at=${encodeURIComponent(submittedAt)}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        }
      );
  
      if (!response.ok) {
        messageDiv.className = "";
        messageDiv.classList.add("error");
        messageDiv.textContent = "Failed to load saved answers. Please try again later.";
        messageDiv.style.display = "block";
        return;
      }
  
      const data = await response.json();
      const savedAnswers = data.answers || {};
  
      for (const [questionName, answerValue] of Object.entries(savedAnswers)) {
        const inputs = document.querySelectorAll(`input[name="${questionName}"]`);
        inputs.forEach((input) => {
          if (input.value === answerValue) {
            input.checked = true;
          }
        });
      }
    } catch {
      // Handle network or unexpected errors 
      messageDiv.className = "";
      messageDiv.classList.add("error");
      messageDiv.textContent = "An error occurred while loading saved answers. Please check your connection.";
      messageDiv.style.display = "block";
    }
  
    const form = document.querySelector("#edit-quiz-form");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const formData = new FormData(form);
      const updatedAnswers = {};
      for (const [key, value] of formData.entries()) {
        updatedAnswers[key] = value;
      }
  
      try {
        const response = await fetch(
          `/petsona/edit_quiz?username=${encodeURIComponent(username)}&submitted_at=${encodeURIComponent(submittedAt)}`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify(updatedAnswers),
          }
        );
  
        const result = await response.json();
  
        if (result.redirect_url) {
          window.location.href = result.redirect_url;
        } 

      } catch {
        // Show error message 
        messageDiv.className = "";
        messageDiv.classList.add("error");
        messageDiv.textContent = "Failed to update quiz. Please check your connection and try again.";
        messageDiv.style.display = "block";
      }
    });
  });
  

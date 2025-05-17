document.addEventListener("DOMContentLoaded", async () => {
  // Extract username and submitted_at from URL query params
  const urlParams = new URLSearchParams(window.location.search);
  const username = urlParams.get("username");
  const submittedAt = urlParams.get("submitted_at");

  if (!username || !submittedAt) {
    // Not on quiz edit page, do nothing!
    return;
  }

  try {
    // Fetch saved answers from backend GET endpoint
    const response = await fetch(
      `/edit_quiz?username=${encodeURIComponent(
        username
      )}&submitted_at=${encodeURIComponent(submittedAt)}`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error("Failed to load saved answers");
    }

    const data = await response.json();
    const savedAnswers = data.answers || {};

    // Pre-fill the form inputs with saved answers
    for (const [questionName, answerValue] of Object.entries(savedAnswers)) {
      const inputs = document.querySelectorAll(`input[name="${questionName}"]`);
      console.log(savedAnswers);
      inputs.forEach((input) => {
        if (input.value === answerValue) {
          input.checked = true;
        }
      });
    }
  } catch (error) {
    console.error("Error loading saved answers:", error);
  }

  // Handle form submission with PATCH request
  const form = document.querySelector("form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const updatedAnswers = {};
    for (const [key, value] of formData.entries()) {
      updatedAnswers[key] = value;
    }

    try {
      const response = await fetch(
        `/edit_quiz?username=${encodeURIComponent(
          username
        )}&submitted_at=${encodeURIComponent(submittedAt)}`,
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
        // Redirect to the result card page
        window.location.href = result.redirect_url;
      }
    } catch (err) {
      alert("Failed to update quiz.");
      console.error(err);
    }
  });
});

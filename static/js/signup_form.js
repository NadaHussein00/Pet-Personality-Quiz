import { validateForm, clearErrors, showError } from "./validate_form.js";


// Validates the signup form fields and displays errors if any
function validateSignupForm() {

  const formValues = {
    "first-name": document.getElementById("first-name-reg").value.trim(),
    "last-name": document.getElementById("last-name-reg").value.trim(),
    email: document.getElementById("email-reg").value.trim(),
    username: document.getElementById("username-reg").value.trim(),
    password: document.getElementById("password-reg").value.trim(),
    "password-confirm": document
      .getElementById("password-confirm-reg")
      .value.trim(),
    bio: document.getElementById("bio-reg")
      ? document.getElementById("bio-reg").value.trim()
      : "",
  };


  const errorIds = {
    "first-name": "error-firstname-reg",
    "last-name": "error-lastname-reg",
    email: "error-email-reg",
    username: "error-username-reg",
    password: "error-password-reg",
    "password-confirm": "error-confirm-pass-reg",
    bio: "error-bio-reg", 
  };

  // Use generic validation runner imported from formValidation.js
  // For signup, password is required, bio max words 100
  return validateForm(formValues, null, errorIds, {
    passwordRequired: true,
    bioMaxWords: 100,
    showError,
  });
}

// Attach validation to form submit event
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signup-form");
  form.addEventListener("submit", (event) => {
    clearErrors();
    const isValid = validateSignupForm();
    console.log("Form validation result:", isValid);
    if (!isValid) {
      event.preventDefault(); 
    }
  });
});

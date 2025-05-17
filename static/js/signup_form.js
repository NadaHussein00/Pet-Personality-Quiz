// Assuming formValidation.js exposes:
// - validateForm (generic runner)
// - clearErrors, showError (can be shared or kept here if page-specific)
import { validateForm, clearErrors, showError } from "./validate_form.js";

// Main validation function called on form submit
function validateSignupForm() {
  // clearErrors(); // called in submit handler

  // Get trimmed values from inputs
  const formValues = {
    "first-name": document.getElementById("first-name-reg").value.trim(),
    "last-name": document.getElementById("last-name-reg").value.trim(),
    email: document.getElementById("email-reg").value.trim(),
    username: document.getElementById("username-reg").value.trim(),
    password: document.getElementById("password-reg").value.trim(),
    "confirm-password": document
      .getElementById("password-confirm-reg")
      .value.trim(),
    bio: document.getElementById("bio-reg")
      ? document.getElementById("bio-reg").value.trim()
      : "",
  };

  // Map input fields to their corresponding error span IDs
  const errorIds = {
    "first-name": "error-firstname-reg",
    "last-name": "error-lastname-reg",
    email: "error-email-reg",
    username: "error-username-reg",
    password: "error-password-reg",
    "confirm-password": "error-confirm-pass-reg",
    bio: "error-bio-reg", // if bio field exists
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
    console.log("Form validation result:", validateSignupForm());
    if (!validateSignupForm()) {
      event.preventDefault(); // Prevent form submission if invalid
    }
  });
});

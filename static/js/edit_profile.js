import { validateForm, clearErrors, showError } from "./validate_form.js";

// Retrieves the username from the URL query parameters
function getUsernameFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("username");
}

// Gets the current values from the form fields, trimmed of whitespace
function getCurrentFormValues() {
  return {
    "first-name": document.getElementById("first-name").value.trim(),
    "last-name": document.getElementById("last-name").value.trim(),
    password: document.getElementById("password").value.trim(),
    "confirm-password": document
      .getElementById("confirm-password")
      .value.trim(),
    "bio-edit": document.getElementById("bio-edit").value.trim(),
  };
}


// Checks if any form field values have changed compared to original values
function hasChanges(currentValues, originalValues) {
  for (const key in currentValues) {
    const current = currentValues[key];
    const original =
      originalValues[key] === undefined ? "" : originalValues[key];
    if (current !== original) {
      return true;
    }
  }
  return false;
}

const username = getUsernameFromUrl();
let originalValues = {};

document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Fetches the user's profile data and populates the form fields
    const response = await fetch(
      `/petsona/edit_profile?username=${encodeURIComponent(username)}`,
      { headers: { Accept: "application/json" } }
    );
    if (!response.ok) throw new Error("Failed to load profile data");
    const data = await response.json();

    originalValues = {
      "first-name": data.first_name || "",
      "last-name": data.last_name || "",
      "bio-edit": data.bio || "",
    };

    document.getElementById("first-name").value = originalValues["first-name"];
    document.getElementById("last-name").value = originalValues["last-name"];
    document.getElementById("bio-edit").value = originalValues["bio-edit"];
  } catch (err) {
    // Displays an error message if profile data fails to load
    const messageDiv = document.getElementById("message");
  messageDiv.className = "";
  messageDiv.classList.add("error");
  messageDiv.textContent = "An error occurred while loading profile data. Please try again.";
  messageDiv.style.display = "block";

  }

  // Handles form submission, validates input, and updates profile via PATCH request
  document
    .getElementById("edit-profile-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      clearErrors(); 

      const updatedData = getCurrentFormValues();

      if (!hasChanges(updatedData, originalValues)) {
        const messageDiv = document.getElementById("message");
  messageDiv.className = ""; 
  messageDiv.style.display = "none"; 

  messageDiv.classList.add("info");
  messageDiv.textContent = "No changes detected. Please update at least one field before saving.";
  messageDiv.style.display = "block";
  return;
      }

      const errorIds = {
        "first-name": "error-firstname",
        "last-name": "error-lastname",
        "bio-edit": "error-bio-edit",
        password: "error-password-edit",
        "confirm-password": "error-confirm-password-edit",
      };

      const isValid = validateForm(
        updatedData,
        originalValues,
        errorIds,
        { passwordRequired: false, bioMaxWords: 100 },
        showError 
      );

      if (!isValid) {
        return;
      }

      Object.keys(updatedData).forEach((key) => {
        if (!updatedData[key]) delete updatedData[key];
      });

      Object.keys(updatedData).forEach((key) => {
        if (!updatedData[key]) delete updatedData[key];
      });

      try {
        // Sends the updated profile data to the server
        const response = await fetch(
          `/petsona/edit_profile?username=${encodeURIComponent(username)}`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify(updatedData),
          }
        );

        const result = await response.json();

        const messageDiv = document.getElementById("message");
        if (response.ok) {
          messageDiv.className = "";
          messageDiv.classList.add("success");
          messageDiv.textContent = result.message || "Profile updated successfully";
          messageDiv.style.display = "block";
          originalValues = { ...originalValues, ...updatedData };
        } else {
          messageDiv.style.color = "red";
          messageDiv.textContent = result.error || "Failed to update profile";
        }
      } catch (err) {
        // Displays a network error message if the PATCH request fails
        const messageDiv = document.getElementById("message");
        messageDiv.className = "";
        messageDiv.classList.add("error");
        messageDiv.textContent = "Network error. Please check your connection and try again.";
        messageDiv.style.display = "block";
      }
    });
});

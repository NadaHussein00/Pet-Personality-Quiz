import { validateForm, clearErrors, showError } from "./validate_form.js";

function getUsernameFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("username");
}

// Helper function to get current form values
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

// Simple function to check if any field changed

function hasChanges(currentValues, originalValues) {
  for (const key in currentValues) {
    const current = currentValues[key];
    const original =
      originalValues[key] === undefined ? "" : originalValues[key];
    if (current !== original) {
      return true; // Found a difference
    }
  }
  return false; // No differences found
}

const username = getUsernameFromUrl(); // dynamically set this as needed

// Store original user data globally for comparison
let originalValues = {};

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch(
      `/edit_profile?username=${encodeURIComponent(username)}`,
      { headers: { Accept: "application/json" } }
    );
    if (!response.ok) throw new Error("Failed to load profile data");
    const data = await response.json();

    // Save original values for later comparison
    originalValues = {
      "first-name": data.first_name || "",
      "last-name": data.last_name || "",
      "bio-edit": data.bio || "",
    };

    // Fill form fields with fetched data
    document.getElementById("first-name").value = originalValues["first-name"];
    document.getElementById("last-name").value = originalValues["last-name"];
    document.getElementById("bio-edit").value = originalValues["bio-edit"];
  } catch (err) {
    console.error(err);
    // Optionally show an error message to user
  }
  console.log(document.getElementById("edit-profile-form"));
  // Handle form submission to PATCH update profile
  document
    .getElementById("edit-profile-form")
    .addEventListener("submit", async (e) => {
      console.log("Form submit event fired");
      e.preventDefault();
      console.log("Form submit handler triggered");

      clearErrors(); // Clear previous validation errors (implement or import this)

      const updatedData = getCurrentFormValues();

      // Check if there are any changes
      if (!hasChanges(updatedData, originalValues)) {
        const messageDiv = document.getElementById("message");
        messageDiv.style.color = "blue";
        messageDiv.textContent =
          "No changes detected. Please update at least one field before saving.";
        return; // Do not submit if no changes
      }

      // Define error span IDs for your form fields
      const errorIds = {
        "first-name": "error-firstname",
        "last-name": "error-lastname",
        bio: "error-bio-edit",
        password: "error-password-edit",
        "confirm-password": "error-confirm-password-edit",
      };

      console.log("Running validation...");
      // Call generic validation runner
      const isValid = validateForm(
        updatedData,
        originalValues,
        errorIds,
        { passwordRequired: false, bioMaxWords: 100 },
        showError // pass your showError function to display errors
      );

      console.log("Validation result:", isValid);
      if (!isValid) {
        // Validation failed, do not submit
        return;
      }

      // Remove empty fields to avoid overwriting with empty strings
      Object.keys(updatedData).forEach((key) => {
        if (!updatedData[key]) delete updatedData[key];
      });

      // Check if there are any changes
      if (!hasChanges(updatedData, originalValues)) {
        const messageDiv = document.getElementById("message");
        messageDiv.style.color = "orange";
        messageDiv.textContent =
          "No changes detected. Please update at least one field before saving.";
        return; // Do not submit if no changes
      }

      // Optional: Add your validation here before submitting
      // e.g. if (!validateEditProfileForm(updatedData)) return;

      // Remove empty fields to avoid overwriting with empty strings
      Object.keys(updatedData).forEach((key) => {
        if (!updatedData[key]) delete updatedData[key];
      });

      try {
        const response = await fetch(
          `/edit_profile?username=${encodeURIComponent(username)}`,
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
          messageDiv.style.color = "green";
          messageDiv.textContent = result.message;
          // Update originalValues to current values after successful save
          originalValues = { ...originalValues, ...updatedData };
        } else {
          messageDiv.style.color = "red";
          messageDiv.textContent = result.error || "Failed to update profile";
        }
      } catch (err) {
        console.error(err);
        const messageDiv = document.getElementById("message");
        messageDiv.style.color = "red";
        messageDiv.textContent = "Network error";
      }
    });
});

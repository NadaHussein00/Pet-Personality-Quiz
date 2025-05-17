// Clear all error messages and hide error spans
export function clearErrors() {
  const errorSpans = document.querySelectorAll(".error-message");
  errorSpans.forEach((span) => {
    span.textContent = "";
    span.style.display = "none";
  });
}

// Show error message for a specific field's error span
export function showError(fieldErrorId, message) {
  const errorSpan = document.getElementById(fieldErrorId);
  if (errorSpan) {
    errorSpan.textContent = message;
    errorSpan.style.display = "block";
    errorSpan.style.color = "red";
  } else {
    console.warn("Error span not found for ID:", fieldErrorId);
  }
}

function validateName(nameValue, label) {
  if (!nameValue) return `${label} is required.`;
  if (nameValue.length < 2) return `${label} must be at least 2 characters.`;
  if (nameValue.length > 20) return `${label} must be less than 20 characters.`;
  return "";
}

function validateEmail(email) {
  if (!email) return "Email is required.";
  if (email.length < 8) return "Email must be at least 8 characters.";
  if (email.length > 35) return "Email must be less than 35 characters.";
  if (email.includes(" ")) return "Email cannot contain spaces.";
  if (!email.includes("@")) return "Email must contain '@'.";
  if (email.startsWith("@")) return "'@' cannot be the first character.";
  if (email.endsWith("@")) return "'@' cannot be the last character.";
  if (email.indexOf("@") !== email.lastIndexOf("@"))
    return "Email can contain only one '@'.";
  if (!email.includes(".")) return "Email must contain a dot ('.').";
  const atIndex = email.indexOf("@");
  if (email.indexOf(".", atIndex) === -1)
    return "Email must contain a dot ('.') after '@'.";
  if (!email.endsWith(".com")) return "Email must end with '.com'.";
  return "";
}

function validateUsername(username) {
  if (!username) return "Username is required.";
  if (username.length < 8) return "Username must be at least 8 characters.";
  if (username.length > 35) return "Username must be less than 35 characters.";
  if (username.includes(" ")) return "Username cannot contain spaces.";
  return "";
}

function validatePassword(password, username, firstName) {
  if (!password) return "Password is required.";
  if (password.length < 8) return "Password must be at least 8 characters.";
  if (password.length > 34) return "Password must be less than 35 characters.";
  if (password.includes(" ")) return "Password cannot contain spaces.";

  const specialChars = "!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~";
  let hasSpecial = false;
  let hasNumber = false;
  let hasUpper = false;

  for (let ch of password) {
    if (specialChars.includes(ch)) hasSpecial = true;
    else if (ch >= "0" && ch <= "9") hasNumber = true;
    else if (ch >= "A" && ch <= "Z") hasUpper = true;
  }

  const conditionsMet = [hasSpecial, hasNumber, hasUpper].filter(
    Boolean
  ).length;
  if (conditionsMet < 3) {
    return "Password must contain at least 3 of the following: uppercase letters, numbers, special characters.";
  }

  const passworddLower = password.toLowerCase();
  if (username && passworddLower.includes(username.toLowerCase())) {
    return "Password must not contain your username.";
  }
  if (firstName && passworddLower.includes(firstName.toLowerCase())) {
    return "Password must not contain your first name.";
  }

  return "";
}

function validateConfirmPassword(password, confirmPassword) {
  if (password !== confirmPassword) return "Passwords do not match.";
  return "";
}

function validateBio(bio, maxWords = 100) {
  if (!bio) return ""; // bio can be empty
  const wordCount = bio.trim().split(/\s+/).length;
  if (wordCount > maxWords) return `Bio must be less than ${maxWords} words.`;
  return "";
}

/**
 *
 * @param {Object} newValues - The current form values keyed by field name
 * @param {Object} originalValues - The original values (for edit profile), or null for signup
 * @param {Object} errorIds - Map of field names to error span IDs
 * @param {Object} options - { passwordRequired: bool }
 * @returns {boolean} isValid
 */
export function validateForm(
  newValues,
  originalValues,
  errorIds,
  options = {}
) {
  let isValid = true;

  // Helper to show error if any
  function checkField(fieldName, errorMessage) {
    if (errorMessage) {
      showError(errorIds[fieldName], errorMessage);
      isValid = false;
    }
  }

  // Validate first name if changed or signup (originalValues null means signup)
  if (
    !originalValues ||
    newValues["first-name"] !== originalValues["first-name"]
  ) {
    checkField(
      "first-name",
      validateName(newValues["first-name"], "First name")
    );
  }

  // Validate last name if changed or signup
  if (
    !originalValues ||
    newValues["last-name"] !== originalValues["last-name"]
  ) {
    checkField("last-name", validateName(newValues["last-name"], "Last name"));
  }

  // Validate email if changed or signup
  if (!originalValues || newValues.email !== originalValues.email) {
    checkField("email", validateEmail(newValues.email));
  }

  // Validate username if present and changed or signup
  if (
    "username" in newValues &&
    (!originalValues || newValues.username !== originalValues.username)
  ) {
    checkField("username", validateUsername(newValues.username));
  }

  // Password validation
  // For signup, passwordRequired is true
  // For edit profile, passwordRequired is false, but if user entered password, validate it
  if (
    options.passwordRequired ||
    (newValues.password && newValues.password.length > 0)
  ) {
    const username =
      newValues.username || (originalValues && originalValues.username);
    const firstName =
      newValues["first-name"] ||
      (originalValues && originalValues["first-name"]);
    checkField(
      "password",
      validatePassword(newValues.password, username, firstName)
    );
    checkField(
      "confirm-password",
      validateConfirmPassword(newValues.password, newValues["confirm-password"])
    );
  }

  // Bio validation (always validate max words)
  checkField(
    "bio-edit",
    validateBio(newValues["bio-edit"], options.bioMaxWords || 100)
  );

  return isValid;
}

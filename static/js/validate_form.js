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
      errorSpan.textContent = message;
      errorSpan.style.display = "block";
      errorSpan.style.color = "red";

  }
  
  // Validates a name field with length constraints
  function validateName(nameValue, label) {
    if (!nameValue) return `${label} is required.`;
    if (nameValue.length < 2) return `${label} must be at least 2 characters.`;
    if (nameValue.length > 20) return `${label} must be less than 20 characters.`;
    return "";
  }
  
  // Validates an email address with format and character rules
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
  

  // Validates a username with length and character restrictions
  function validateUsername(username) {
    if (!username) return "Username is required.";
    if (username.length < 8) return "Username must be at least 8 characters.";
    if (username.length > 35) return "Username must be less than 35 characters.";
    if (username.includes(" ")) return "Username cannot contain spaces.";
    return "";
  }
  

  // Validates a password with complexity requirements and checks against username and first name
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
  


  // Validates that password and confirm password fields match
  function validateConfirmPassword(password, confirmPassword) {
    if (password !== confirmPassword) return "Passwords do not match.";
    return "";
  }
  
  // Validates bio length by word count with maximum number of words
  function validateBio(bio, maxWords = 100) {
    if (!bio) return ""; 
    const wordCount = bio.trim().split(/\s+/).length;
    if (wordCount > maxWords) return `Bio must be less than ${maxWords} words.`;
    return "";
  }
  

  // Validates the entire form's fields and shows errors for invalid inputs
  export function validateForm(
    newValues,
    originalValues,
    errorIds,
    options = {}
  ) {
    
    let isValid = true;
  
    // Helper to show error if any for a given field
    function checkField(fieldName, errorMessage) {
      if (errorMessage) {
        showError(errorIds[fieldName], errorMessage);
        isValid = false;
      }
    }
  

    if (
      !originalValues ||
      newValues["first-name"] !== originalValues["first-name"]
    ) {
      checkField(
        "first-name",
        validateName(newValues["first-name"], "First name")
      );
    }
  

    if (
      !originalValues ||
      newValues["last-name"] !== originalValues["last-name"]
    ) {
      checkField("last-name", validateName(newValues["last-name"], "Last name"));
    }
  

    if (!originalValues || newValues.email !== originalValues.email) {
      checkField("email", validateEmail(newValues.email));
    }

    if (
      "username" in newValues &&
      (!originalValues || newValues.username !== originalValues.username)
    ) {
      checkField("username", validateUsername(newValues.username));
    }
  

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
        "password-confirm",
        validateConfirmPassword(newValues.password, newValues["password-confirm"])
      );
    }
  

if ("bio" in newValues) {
    checkField(
      "bio",
      validateBio(newValues["bio"], options.bioMaxWords || 100)
    );

  }
  
  if ("bio-edit" in newValues) {
    checkField(
      "bio-edit",
      validateBio(newValues["bio-edit"], options.bioMaxWords || 100)
    );
  }
  
  
    return isValid;
  }

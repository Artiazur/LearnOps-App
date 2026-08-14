export function validateFirstName(firstName) {
  const value = firstName.trim();

  if (!value) {
    return "First name is required.";
  }

  if (/\d/.test(value)) {
    return "First name cannot contain numbers.";
  }

  return "";
}


export function validateLastName(lastName) {
  const value = lastName.trim();

  if (!value) {
    return "Last name is required.";
  }

  if (/\d/.test(value)) {
    return "Last name cannot contain numbers.";
  }

  return "";
}


export function validateEmail(email) {
  const value = email.trim();

  if (!value) {
    return "Email is required.";
  }

  const emailRegex =
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailRegex.test(value)) {
    return "Please enter a valid email address.";
  }

  return "";
}


export function validatePassword(password) {
  if (!password) {
    return "Password is required.";
  }

  if (/\s/.test(password)) {
    return "Password cannot contain spaces.";
  }

  if (password.length < 8) {
    return "Password must be at least 8 characters.";
  }

  if (!/[A-Z]/.test(password)) {
    return "Password must contain an uppercase letter.";
  }

  if (!/[a-z]/.test(password)) {
    return "Password must contain a lowercase letter.";
  }

  if (!/\d/.test(password)) {
    return "Password must contain a number.";
  }

  if (!/[!@#$%^&*]/.test(password)) {
    return "Password must contain a special character.";
  }

  return "";
}

export function validateLoginPassword(password) {
  if (!password) {
    return "Password is required.";
  }

  if (/\s/.test(password)) {
    return "Password cannot contain spaces.";
  }

  return "";
}

export function validateConfirmPassword(
  password,
  confirmPassword
) {
  if (!confirmPassword) {
    return "Please confirm your password.";
  }

  if (password !== confirmPassword) {
    return "Passwords do not match.";
  }

  return "";
}
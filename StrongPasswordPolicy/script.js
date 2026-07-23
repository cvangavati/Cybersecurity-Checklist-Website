function validatePassword() {

    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    const strongPassword =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#^()_\-+=])[A-Za-z\d@$!%*?&#^()_\-+=]{12,}$/;

    const commonPasswords = [
        "password",
        "password123",
        "12345678",
        "123456789",
        "qwerty",
        "admin"
    ];

    if (password.includes(" ")) {
        message.style.color = "red";
        message.textContent = "Password cannot contain spaces.";
        return;
    }

    if (commonPasswords.includes(password.toLowerCase())) {
        message.style.color = "red";
        message.textContent = "Choose a stronger password.";
        return;
    }

    if (!strongPassword.test(password)) {
        message.style.color = "red";
        message.textContent =
            "Password must be at least 12 characters and include uppercase, lowercase, a number, and a special character.";
    } else {
        message.style.color = "green";
        message.textContent = "Strong password accepted!";
    }
}
const btn = document.getElementById("toggle-password");
    const input = document.getElementById("password");

    btn.addEventListener("click", function () {
        if (input.type === "password") {
            input.type = "text";
            btn.textContent = "🙈";
        } else {
            input.type = "password";
            btn.textContent = "👁";
        }
    });
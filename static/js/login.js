document.addEventListener("DOMContentLoaded", function () {

    const username = document.getElementById("username");
    const password = document.getElementById("password");

    const loginBtn = document.getElementById("loginBtn");
    const message = document.getElementById("message");

    loginBtn.onclick = async function () {

        if (!username.value || !password.value) {
            message.innerText = "Please fill all fields";
            return;
        }

        try {

            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username.value,
                    password: password.value
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                window.location.href = "/app";
            } else {
                message.innerText = data.detail || "Login failed";
            }

        } catch (err) {
            message.innerText = "Unable to connect to server.";
            console.error(err);
        }
    };

});
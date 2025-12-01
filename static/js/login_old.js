// login.js — управление логином и регистрацией

// Открытие окна логина
function openLogin() {
    document.getElementById("loginPanel").style.display = "block";
}

// Закрытие окна логина
function closeLogin() {
    document.getElementById("loginPanel").style.display = "none";
}

// Открытие регистрации (можно потом расширить)
function openRegister() {
    alert("Registration form will be implemented here.");
}

// Логин пользователя
function login() {
    let username = document.getElementById("usernameInput").value;
    let password = document.getElementById("passwordInput").value;

    fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: username, password: password})
    })
    .then(r => r.json())
    .then(data => {
        if(data.status ==="ok"){
            closeLogin();
            updateUIAfterLogin(data.user);
        } else {
            alert("Invalid username or password1");
        }
    });
}

// Логаут пользователя
function logout() {
    fetch("/logout")
        .then(() => {
            document.getElementById("currentUser").textContent = "";
            const loginBtn = document.getElementById("loginBtn");
            loginBtn.textContent = "Log In";
            loginBtn.onclick = openLogin;
            document.getElementById("selectTrackersBtn").disabled = true;
        });
}

// Обновление интерфейса после логина
function updateUIAfterLogin(user) {
    document.getElementById("currentUser").textContent = "Logged in as: " + user.username;

    const loginBtn = document.getElementById("loginBtn");
    loginBtn.textContent = "Log Out";
    loginBtn.onclick = logout;

    document.getElementById("selectTrackersBtn").disabled = false;
}

// Показ/скрытие панели фильтра
function toggleFilterPanel() {
    const panel = document.getElementById("filter-panel");
    panel.style.display = panel.style.display === "block" ? "none" : "block";
}



function loadUserPoints(userId) {
    fetch("/api/points_new?user_id=" + userId)
        .then(r => r.json())
        .then(points => {
            points.forEach(p => {
                L.marker([p.lat, p.lon]).addTo(map);
            });
        });
}


// Проверка, если пользователь уже в сессии
fetch("/whoami")
    .then(r => r.json())
    .then(info => {
        if (info.user) {
            updateUIAfterLogin(info.user);
            loadUserPoints(info.user.id);
        }
    });
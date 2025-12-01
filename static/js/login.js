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



            // === Загрузка точек пользователя и отображение на карте ===
            function loadUserPoints(userId) {
                fetch("/api/points_new?user_id=" + userId)
                    .then(r => r.json())
                    .then(points => {
                        markersLayer.clearLayers();
                        if (!points || points.length === 0) {
                            showDefaultPoint();
                        } else {
                            points.forEach(pt => {
                                if(pt.lat == null || pt.lon == null) return;
                                const icon = pt.is_active === 1 ? activeIcon : passiveIcon;
                                const marker = L.marker([pt.lat, pt.lon], {icon});
                                marker.bindPopup(`
                                    <b>${pt.tracker_name}</b><br>
                                    ${pt.date} ${pt.time}<br>
                                    Status: ${pt.is_active===1 ? "Active" : "Passive"}
                                `);
                                markersLayer.addLayer(marker);
                            });
                            map.fitBounds(markersLayer.getBounds(), {padding:[50,50]});
                        }
                    });}



// === Получаем текущего пользователя ===
async function getCurrentUserId() {
    const res = await fetch('/whoami');
    const data = await res.json();
    return data.user ? data.user.id : null;
}

// === Загрузка точек для текущего пользователя ===
async function initUserPoints() {
    const userId = await getCurrentUserId();
    if (!userId) {
        showDefaultPoint();
        return;
    }
    const res = await fetch(`/api/points_new?user_id=${userId}`);
    const points = await res.json();
    showPoints(points);
    loadUserPoints(userId);
}

// === Обновление интерфейса после логина ===
function updateUIAfterLogin(user) {
    document.getElementById("currentUser").textContent = "Logged in as: " + user.username;
    const loginBtn = document.getElementById("loginBtn");
    loginBtn.textContent = "Log Out";
    loginBtn.onclick = logout;
    document.getElementById("selectTrackersBtn").disabled = false;

    loadUserPoints(user.id);

    // вызываем карту
    window.MapAPI.loadUserPoints(user.id);
}

// === Регистрация пользователя ===
function register() {
    const username = document.getElementById("regUsername").value;
    const password = document.getElementById("regPassword").value;

    fetch("/api/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === "ok") {
            closeLogin();
            updateUIAfterLogin(data.user);
        } else {
            alert(data.message);
        }
    });
}

// === Логин пользователя ===
function login() {
    const username = document.getElementById("usernameInput").value;
    const password = document.getElementById("passwordInput").value;

    fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(r => r.json())
    .then(data => {
        if(data.status ==="ok"){
            closeLogin();
            updateUIAfterLogin(data.user);
        } else {
            alert("Invalid username or password");
        }
    });
}

// === Логаут пользователя ===
function logout() {
    fetch("/logout")
        .then(() => {
            document.getElementById("currentUser").textContent = "";
            const loginBtn = document.getElementById("loginBtn");
            loginBtn.textContent = "Log In";
            loginBtn.onclick = openLogin;
            document.getElementById("selectTrackersBtn").disabled = true;

            showDefaultPoint();
        });
}

// === Открытие/закрытие панели логина ===
function openLogin() { document.getElementById("loginPanel").style.display = "block"; }
function closeLogin() { document.getElementById("loginPanel").style.display = "none"; }

// === Инициализация страницы ===
initUserPoints();





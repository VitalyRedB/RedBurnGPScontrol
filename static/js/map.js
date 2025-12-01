// =====================
// ИНИЦИАЛИЗАЦИЯ КАРТЫ
// =====================
const map = L.map('map').setView([50.45, 30.52], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

// =====================
// СЛОЙ МАРКЕРОВ (кластер)
// =====================
const markersLayer = L.markerClusterGroup();
map.addLayer(markersLayer);

// =====================
// ИКОНКИ
// =====================
const activeIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]});

const passiveIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]});

// =====================
// ДЕФОЛТНАЯ ТОЧКА (КИЕВ)
// =====================
function showDefaultPoint() {
    markersLayer.clearLayers();
    const m = L.marker([50.4501, 30.5234]).addTo(markersLayer);
    m.bindPopup("Киев");
    map.setView([50.4501, 30.5234], 10);}

// =====================
// ВЫВОД СПИСКА ТОЧЕК
// =====================
function showPointsList(points) {
    const box = document.getElementById("pointsList");
    box.innerHTML = "";

    points.forEach(p => {
        const div = document.createElement("div");
        div.textContent =
            `ID:${p.id}, ${p.tracker_name}, Lat:${p.lat}, Lon:${p.lon}, ${p.date} ${p.time}, Active:${p.is_active}`;
        box.appendChild(div);
    });
}

// =====================
// ОТРИСОВКА ТОЧЕК НА КАРТЕ
// =====================
function renderPoints(points) {
    markersLayer.clearLayers();

    points.forEach(p => {
        if (p.lat == null || p.lon == null) return;

        const icon = p.is_active === 1 ? activeIcon : passiveIcon;

        const marker = L.marker([p.lat, p.lon], { icon });
        marker.bindPopup(`
            <b>${p.tracker_name}</b><br>
            ${p.date} ${p.time}<br>
            Status: ${p.is_active === 1 ? "Active" : "Passive"}
        `);

        markersLayer.addLayer(marker);
    });

    if (markersLayer.getLayers().length > 0) {
        map.fitBounds(markersLayer.getBounds(), { padding: [50, 50] });
    }
}

// =====================
// ЗАГРУЗКА ТОЧЕК ПОЛЬЗОВАТЕЛЯ
// =====================
async function loadUserPoints(userId) {
    if (!userId) {
        showDefaultPoint();
        return;
    }

    const res = await fetch(`/api/points_new?user_id=${userId}`);
    const points = await res.json();

    showPointsList(points);
    renderPoints(points);
}

// =====================
// АВТОЗАПУСК ПРИ ЗАГРУЗКЕ СТРАНИЦЫ
// =====================
(async () => {
    const res = await fetch("/whoami");
    const info = await res.json();

    if (info.user) {
        // пользователь залогинен → подгружаем его точки
        await loadUserPoints(info.user.id);
    } else {
        showDefaultPoint();
    }
})();

// =====================
// API ДЛЯ login.js
// =====================
window.MapAPI = {
    loadUserPoints
};

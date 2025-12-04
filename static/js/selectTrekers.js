let trackerData = [];      // список трекеров из API
let selectedTrackers = []; // выбранные ID

function openTrackerPanel() {
    document.getElementById("tracker-popup").classList.remove("hidden");
}

function closeTrackerPanel() {
    document.getElementById("tracker-popup").classList.add("hidden");
}

function loadTrackers(data) {
    trackerData = data;

    const list = document.getElementById("trackerList");
    list.innerHTML = "";

    data.forEach(t => {
        const div = document.createElement("div");
        div.className = "tracker-item";
        div.innerHTML = `
            <label>
                <input type="checkbox" value="${t.id}" class="tracker-checkbox">
                ${t.name}
            </label>
        `;
        list.appendChild(div);
    });

    // Отметить уже выбранные трекеры
    selectedTrackers.forEach(id => {
        const cb = list.querySelector(`.tracker-checkbox[value="${id}"]`);
        if (cb) cb.checked = true;
    });
}

function selectAllTrackers() {
    document.querySelectorAll(".tracker-checkbox").forEach(cb => cb.checked = true);
}

function clearAllTrackers() {
    document.querySelectorAll(".tracker-checkbox").forEach(cb => cb.checked = false);
}

function applyTrackerSelection() {
    const checkboxes = document.querySelectorAll(".tracker-checkbox");
    selectedTrackers = [];

    checkboxes.forEach(cb => {
        if (cb.checked) selectedTrackers.push(cb.value);
    });

    const display = document.getElementById("trekersDisplay");
    if (selectedTrackers.length === 0 || selectedTrackers.length === trackerData.length) {
        display.textContent = "All trackers";
        selectedTrackers = [];
    } else {
        const names = trackerData
            .filter(t => selectedTrackers.includes(String(t.id)))
            .map(t => t.name);
        display.textContent = names.join(", ");
    }

    // Синхронизируем select
    const select = document.getElementById("trekersFilter");
    Array.from(select.options).forEach(opt => opt.selected = false);
    if (selectedTrackers.length === 0) {
        select.options[0].selected = true; // All
    } else {
        selectedTrackers.forEach(id => {
            const opt = select.querySelector(`option[value="${id}"]`);
            if (opt) opt.selected = true;
        });
    }

    closeTrackerPanel();
}

// Загрузка трекеров с сервера
async function loadTrekersPopup(userId) {
    if (!userId) return;

    const res = await fetch(`/api/trackers?user_id=${userId}`);
    const data = await res.json();
    const popupData = data.map(t => ({id: t.id, name: t.tracker_name}));
    loadTrackers(popupData);

    // Заполняем select (для совместимости)
    const select = document.getElementById("trekersFilter");
    select.innerHTML = "";

    const optAll = document.createElement("option");
    optAll.value = "";
    optAll.textContent = "All trackers";
    select.appendChild(optAll);

    data.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.textContent = t.tracker_name;
        select.appendChild(opt);
    });
}





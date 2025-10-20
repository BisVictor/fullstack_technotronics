const API = "http://127.0.0.1:8000"; // адрес твоего FastAPI

// --- СТАТИСТИКА ---
async function getStats() {
    const res = await fetch(`${API}/stats`);
    if (!res.ok) {
        alert("Ошибка при получении статистики");
        return;
    }
    const stats = await res.json();
    document.getElementById("device-count").textContent = stats.devices_total;
    document.getElementById("battery-count").textContent = stats.batteries_total;
}

// --- УСТРОЙСТВА ---
async function getAllDevices() {
    const res = await fetch(`${API}/get_all_device`);
    const list = document.getElementById("devices-list");
    list.innerHTML = "";

    if (!res.ok) {
        list.innerHTML = "<p>Нет устройств</p>";
        return;
    }

    const devices = await res.json();
    devices.forEach(d => {
        const el = document.createElement("div");
        el.className = "card";
        el.innerHTML = `
            <strong>${d.name}</strong><br>
            Версия: ${d.firmware_version}<br>
            Активен: ${d.is_active ? "✅" : "❌"}<br>
            Подключено АКБ: ${d.batteries_len}
        `;
        list.appendChild(el);
    });
}

async function getDeviceById() {
    const id = prompt("Введите ID устройства:");
    if (!id) return;
    const res = await fetch(`${API}/get_device_by_id/${id}`);
    const data = await res.json();
    alert(JSON.stringify(data, null, 2));
}

async function addDevice() {
    const name = prompt("Название устройства:");
    const firmware = prompt("Версия прошивки:");
    const active = confirm("Активировать устройство?");
    const res = await fetch(`${API}/add_new_device`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name,
            firmware_version: firmware,
            is_active: active
        })
    });
    alert(JSON.stringify(await res.json()));
    getAllDevices();
    getStats();
}

async function updateDevice() {
    const id = prompt("ID устройства для обновления:");
    const name = prompt("Новое имя (пусто — без изменений):");
    const firmware = prompt("Новая прошивка:");
    const active = confirm("Активировать?");
    const res = await fetch(`${API}/update_device_by_id/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name,
            firmware_version: firmware,
            is_active: active
        })
    });
    alert(JSON.stringify(await res.json()));
    getAllDevices();
}

async function deleteDevice() {
    const id = prompt("ID устройства для удаления:");
    const res = await fetch(`${API}/delete_device_by_id${id}`, { method: "DELETE" });
    alert(JSON.stringify(await res.json()));
    getAllDevices();
    getStats();
}

// --- БАТАРЕИ ---
async function getAllBatteries() {
    const res = await fetch(`${API}/get_all_batteries`);
    const list = document.getElementById("batteries-list");
    list.innerHTML = "";

    if (!res.ok) {
        list.innerHTML = "<p>Нет батарей</p>";
        return;
    }

    const batteries = await res.json();
    batteries.forEach(b => {
        const el = document.createElement("div");
        el.className = "card";
        el.innerHTML = `
            <strong>${b.name}</strong><br>
            Напряжение: ${b.voltage} В<br>
            Ёмкость: ${b.capacity} мАч<br>
            Срок службы: ${b.lifetime} мес<br>
            Привязано к устройству: ${b.device_id || "❌"}
        `;
        list.appendChild(el);
    });
}

async function getBatteryById() {
    const id = prompt("Введите ID батареи:");
    const res = await fetch(`${API}/get_battery_by_id/${id}`);
    const data = await res.json();
    alert(JSON.stringify(data, null, 2));
}

async function addBattery() {
    const name = prompt("Название батареи:");
    const voltage = parseFloat(prompt("Напряжение:"));
    const capacity = parseInt(prompt("Ёмкость (мАч):"));
    const lifetime = parseInt(prompt("Срок службы (мес):"));
    const device_id = parseInt(prompt("ID устройства (0 — без привязки):")) || 0;

    const res = await fetch(`${API}/add_new_battery`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, voltage, capacity, lifetime, device_id })
    });

    alert(JSON.stringify(await res.json()));
    getAllBatteries();
    getStats();
}

async function updateBattery() {
    const id = prompt("ID батареи для обновления:");
    const name = prompt("Новое имя:");
    const voltage = prompt("Новое напряжение:");
    const capacity = prompt("Новая ёмкость:");
    const lifetime = prompt("Новый срок службы:");
    const device_id = prompt("Новый ID устройства (0 — отвязать):");

    const res = await fetch(`${API}/update_battery_by_id/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, voltage, capacity, lifetime, device_id })
    });
    alert(JSON.stringify(await res.json()));
    getAllBatteries();
}

async function deleteBattery() {
    const id = prompt("ID батареи для удаления:");
    const res = await fetch(`${API}/delete_battery_by_id/${id}`, { method: "DELETE" });
    alert(JSON.stringify(await res.json()));
    getAllBatteries();
    getStats();
}

async function linkBattery() {
    const battery_id = prompt("ID батареи:");
    const device_id = prompt("ID устройства:");
    const res = await fetch(`${API}/link_battery/${battery_id}/${device_id}`, { method: "PUT" });
    alert(JSON.stringify(await res.json()));
    getAllBatteries();
}

async function unlinkBattery() {
    const battery_id = prompt("ID батареи:");
    const res = await fetch(`${API}/unlink_battery/${battery_id}`, { method: "PUT" });
    alert(JSON.stringify(await res.json()));
    getAllBatteries();
}

function resetAll() {
    document.getElementById("devices-list").innerHTML = "";
    document.getElementById("batteries-list").innerHTML = "";
    document.getElementById("device-count").textContent = "0";
    document.getElementById("battery-count").textContent = "0";
}
window.onload = () => {
    getStats();
    getAllDevices();
    getAllBatteries();
};

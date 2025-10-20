const API = "http://127.0.0.1:8000";

// --- СТАТИСТИКА ---
async function getStats() {
    const res = await fetch(`${API}/stats`);
    if (!res.ok) return;
    const stats = await res.json();
    document.getElementById("device-count").textContent = stats.devices_total;
    document.getElementById("battery-count").textContent = stats.batteries_total;
}

// --- УСТРОЙСТВА ---
async function getAllDevices() {
    const res = await fetch(`${API}/get_all_device`);
    const list = document.getElementById("devices-list");
    list.innerHTML = "";
    if (!res.ok) return;

    const devices = await res.json();
    devices.forEach(d => {
        const el = document.createElement("div");
        el.className = "card";
        el.innerHTML = `
            <strong>ID: ${d.id}</strong><br>
            Название: ${d.name}<br>
            Версия: ${d.firmware_version}<br>
            Активен: ${d.is_active ? "✅" : "❌"}<br>
            АКБ подключено: ${d.batteries_len}
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
        body: JSON.stringify({ name, firmware_version: firmware, is_active: active })
    });
    getAllDevices();
    getStats();
}

async function updateDevice() {
    const id = prompt("ID устройства для обновления:");
    const name = prompt("Новое имя (оставьте пустым, чтобы не менять):");
    const firmware = prompt("Новая версия прошивки:");
    const active = confirm("Активировать?");
    const res = await fetch(`${API}/update_device_by_id/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, firmware_version: firmware, is_active: active })
    });
    getAllDevices();
}

async function deleteDevice() {
    const id = prompt("ID устройства для удаления:");
    const res = await fetch(`${API}/delete_device_by_id/${id}`, { method: "DELETE" });
    getAllDevices();
    getStats();
}

// --- БАТАРЕИ ---
async function getAllBatteries() {
    const res = await fetch(`${API}/get_all_batteries`);
    const list = document.getElementById("batteries-list");
    list.innerHTML = "";
    if (!res.ok) return;

    const batteries = await res.json();
    batteries.forEach(b => {
        const el = document.createElement("div");
        el.className = "card";
        el.innerHTML = `
            <strong>ID: ${b.id}</strong><br>
            Название: ${b.name}<br>
            Напряжение: ${b.voltage} В<br>
            Ёмкость: ${b.capacity} мАч<br>
            Срок службы: ${b.lifetime} мес<br>
            Устройство: ${b.device_id || "❌"}
        `;
        list.appendChild(el);
    });
}

async function getBatteryById() {
    const id = prompt("Введите ID батареи:");
    if (!id) return;
    const res = await fetch(`${API}/get_battery_by_id/${id}`);
    const data = await res.json();
    alert(JSON.stringify(data, null, 2));
}

async function addBattery() {
    const name = prompt("Название батареи:");
    const voltage = parseFloat(prompt("Напряжение:"));
    const capacity = parseInt(prompt("Ёмкость:"));
    const lifetime = parseInt(prompt("Срок службы:"));
    const device_id = parseInt(prompt("ID устройства (0 — без привязки):")) || 0;
    await fetch(`${API}/add_new_battery`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, voltage, capacity, lifetime, device_id })
    });
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
    await fetch(`${API}/update_battery_by_id/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, voltage, capacity, lifetime, device_id })
    });
    getAllBatteries();
}

async function deleteBattery() {
    const id = prompt("ID батареи для удаления:");
    await fetch(`${API}/delete_battery_by_id/${id}`, { method: "DELETE" });
    getAllBatteries();
    getStats();
}

async function linkBattery() {
    const battery_id = prompt("ID батареи:");
    const device_id = prompt("ID устройства:");
    await fetch(`${API}/link_battery/${battery_id}/${device_id}`, { method: "PUT" });
    getAllBatteries();
}

async function unlinkBattery() {
    const battery_id = prompt("ID батареи:");
    await fetch(`${API}/unlink_battery/${battery_id}`, { method: "PUT" });
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

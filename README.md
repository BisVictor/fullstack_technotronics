# 🔋 Technotronics Battery Monitor

## 📘 Описание проекта

**Technotronics Battery Monitor** — это небольшой сервис для мониторинга аккумуляторных батарей и подключённых устройств.  
Реализован с использованием **FastAPI**, **SQLite** и простого **frontend (HTML/CSS/JS)**.

Сервис поддерживает:

- Добавление, изменение и удаление устройств и АКБ;
- Привязку АКБ к устройствам (до 5 штук на одно устройство);
- Просмотр статистики (количество устройств и батарей);
- Удобный интерфейс для работы через браузер.

---

## 🚀 Запуск проекта

### 🐳 Вариант 1 — через Docker (рекомендуется)

> Требуется установленный **Docker** и **docker-compose**.

```bash
# Клонирование репозитория
git clone https://github.com/BisVictor/fullstack_technotronics.git
cd fullstack_technotronics

# Сборка и запуск контейнера
docker-compose up --build
```

🚀 Основные эндпоинты

## 🚀 Основные эндпоинты

| Категория                | Метод    | Endpoint                                 | Описание                       |
| ------------------------ | -------- | ---------------------------------------- | ------------------------------ |
| **Устройства (Devices)** | `GET`    | `/get_all_device`                        | Получить список всех устройств |
|                          | `GET`    | `/get_device_by_id/{device_id}`          | Получить устройство по ID      |
|                          | `POST`   | `/add_new_device`                        | Добавить новое устройство      |
|                          | `PUT`    | `/update_device_by_id/{device_id}`       | Обновить устройство            |
|                          | `DELETE` | `/delete_device_by_id/{device_id}`       | Удалить устройство             |
| **Батареи (Batteries)**  | `GET`    | `/get_all_batteries`                     | Получить список всех батарей   |
|                          | `GET`    | `/get_battery_by_id/{battery_id}`        | Получить батарею по ID         |
|                          | `POST`   | `/add_new_battery`                       | Добавить новую батарею         |
|                          | `PUT`    | `/update_battery_by_id/{battery_id}`     | Обновить батарею               |
|                          | `DELETE` | `/delete_battery_by_id/{battery_id}`     | Удалить батарею                |
| **Связи (Linking)**      | `PUT`    | `/link_battery/{battery_id}/{device_id}` | Привязать батарею к устройству |
|                          | `PUT`    | `/unlink_battery/{battery_id}`           | Отвязать батарею от устройства |
| **Статистика**           | `GET`    | `/stats`                                 | Получить общую статистику      |

⚙️ Устройства (Devices)

🔹 `GET /get_all_device`

Возвращает список всех устройств с количеством подключённых батарей.

```
[
{
"id": 1,
"name": "Device A",
"firmware_version": "1.0.2",
"is_active": true,
"batteries_len": 3
}
]
```

🔹 `GET /get_device_by_id/{device_id}`

Возвращает одно устройство по ID.
Если не найдено — 404 Device not found.

🔹 `POST /add_new_device`

Добавляет новое устройство.

Пример запроса:

```
{
"name": "Device X",
"firmware_version": "2.0",
"is_active": true
}
```

🔹 `PUT /update_device_by_id/{device_id}`

Обновляет данные устройства.

Пример запроса:

```
{
"firmware_version": "2.3.1"
}
```

🔹 `DELETE /delete_device_by_id/{device_id}`

Удаляет устройство по ID.
Возвращает удалённый объект.

🔋 Батареи (Batteries)

🔹` GET /get_all_batteries`

Возвращает список всех батарей.

```
[
{
"id": 2,
"name": "Li-ion 2200mAh",
"voltage": 3.7,
"capacity": 2200,
"lifetime": 24,
"device_id": 1
}
]
```

🔹` GET /get_battery_by_id/{battery_id}`

Возвращает батарею по ID.

🔹 `POST /add_new_battery`

Добавляет новую батарею, с возможной привязкой к устройству.

Пример запроса:

```
{
"name": "Li-ion 3000mAh",
"voltage": 3.7,
"capacity": 3000,
"lifetime": 36,
"device_id": 1
}
```

🔹 `PUT /update_battery_by_id/{battery_id}`

Обновляет параметры батареи.

Особенности:

Проверяется существование батареи и устройства.

Проверяется лимит батарей на устройстве (≤ 5 шт).

🔹 `DELETE /delete_battery_by_id/{battery_id}`

Удаляет батарею по ID.

🔗 Связи (Linking)

🔹 `PUT /link_battery/{battery_id}/{device_id}`

Привязывает батарею к устройству.

Пример ответа:

```
{ "message": "Battery 3 linked to Device 1" }
```

🔹` PUT /unlink_battery/{battery_id}`

Отвязывает батарею от устройства.

Пример ответа:

`{ "message": "Battery 3 unlinked from device" }`

📊 Статистика

🔹 `GET /stats`

Возвращает количество устройств и батарей в системе.

```
{
"devices_total": 5,
"batteries_total": 17
}
```

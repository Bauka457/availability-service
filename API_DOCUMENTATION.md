# API Documentation - Booking Service

## Base URL
```
http://localhost:8000/api/bookings/
```

---

## Endpoints

### 1. Health Check
Проверка работоспособности сервиса.

**Request:**
```http
GET /api/bookings/health/
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "service": "Booking Service"
}
```

---

### 2. Check Service B Status
Проверка доступности сервиса проверки доступности.

**Request:**
```http
GET /api/bookings/check-service-b/
```

**Response (200 OK) - Service Available:**
```json
{
  "available": true
}
```

**Response (200 OK) - Service Unavailable:**
```json
{
  "available": false
}
```

---

### 3. Create Booking
Создание нового бронирования с проверкой доступности.

**Request:**
```http
POST /api/bookings/create/
Content-Type: application/json

{
  "email": "student@example.com",
  "room": "101",
  "date": "2026-03-15",
  "time_start": "10:00",
  "time_end": "12:00",
  "type": "lesson"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Email пользователя |
| room | string | Yes | Номер аудитории |
| date | string | Yes | Дата в формате YYYY-MM-DD |
| time_start | string | Yes | Время начала в формате HH:MM |
| time_end | string | Yes | Время окончания в формате HH:MM |
| type | string | Yes | Тип: lesson, exam, meeting |

**Response (201 Created) - Success:**
```json
{
  "success": true,
  "message": "Бронирование успешно создано",
  "booking": {
    "id": 1,
    "room": "101",
    "date": "2026-03-15",
    "time_start": "10:00",
    "time_end": "12:00",
    "type": "lesson",
    "email": "student@example.com"
  }
}
```

**Response (400 Bad Request) - Room Unavailable:**
```json
{
  "success": false,
  "reason": "Аудитория занята в это время"
}
```

**Response (503 Service Unavailable) - Service B Down:**
```json
{
  "success": false,
  "error": "Не удалось подключиться к сервису проверки. Убедитесь, что он запущен на порту 8001."
}
```

---

### 4. List Bookings
Получение списка всех бронирований.

**Request:**
```http
GET /api/bookings/list/
```

**Response (200 OK):**
```json
{
  "count": 2,
  "bookings": [
    {
      "id": 2,
      "room": "102",
      "date": "2026-03-16",
      "time_start": "14:00",
      "time_end": "16:00",
      "type": "exam",
      "email": "student2@example.com",
      "created_at": "2026-01-28T10:30:00Z"
    },
    {
      "id": 1,
      "room": "101",
      "date": "2026-03-15",
      "time_start": "10:00",
      "time_end": "12:00",
      "type": "lesson",
      "email": "student@example.com",
      "created_at": "2026-01-28T10:00:00Z"
    }
  ]
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid data |
| 503 | Service Unavailable - Service B is down |
| 500 | Internal Server Error |

---

## Example Usage (Python)
```python
import requests

# Create booking
response = requests.post(
    'http://localhost:8000/api/bookings/create/',
    json={
        "email": "student@example.com",
        "room": "101",
        "date": "2026-03-15",
        "time_start": "10:00",
        "time_end": "12:00",
        "type": "lesson"
    }
)

result = response.json()
print(result)
```

## Example Usage (cURL)
```bash
curl -X POST http://localhost:8000/api/bookings/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "room": "101",
    "date": "2026-03-15",
    "time_start": "10:00",
    "time_end": "12:00",
    "type": "lesson"
  }'
```
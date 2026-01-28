# API Documentation - Availability Service

## Base URL
```
http://localhost:8001/api/
```

---

## Endpoints

### 1. Health Check
Проверка работоспособности сервиса.

**Request:**
```http
GET /api/health/
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "service": "Availability Service"
}
```

---

### 2. Check Availability
Проверка доступности аудитории для бронирования.

**Request:**
```http
POST /api/check/
Content-Type: application/json

{
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
| room | string | Yes | Номер аудитории |
| date | string | Yes | Дата в формате YYYY-MM-DD |
| time_start | string | Yes | Время начала в формате HH:MM |
| time_end | string | Yes | Время окончания в формате HH:MM |
| type | string | Yes | Тип: lesson, exam, meeting |

**Response (200 OK) - Available:**
```json
{
  "available": true,
  "message": "Аудитория доступна для бронирования"
}
```

**Response (200 OK) - Unavailable (Conflict):**
```json
{
  "available": false,
  "reason": "Аудитория занята в это время. Конфликтов: 1"
}
```

**Response (200 OK) - Unavailable (Working Hours):**
```json
{
  "available": false,
  "reason": "Аудитория работает только с 08:00 до 20:00"
}
```

**Response (200 OK) - Unavailable (Invalid Type):**
```json
{
  "available": false,
  "reason": "Неизвестный тип бронирования. Допустимые: lesson, exam, meeting"
}
```

---

### 3. Get All Checks
Получение всех проверок доступности.

**Request:**
```http
GET /api/checks/
```

**Response (200 OK):**
```json
{
  "count": 3,
  "checks": [
    {
      "id": 3,
      "room": "101",
      "date": "2026-03-15",
      "time_start": "10:00",
      "time_end": "12:00",
      "type": "lesson",
      "result": true,
      "reason": "Аудитория доступна",
      "checked_at": "2026-01-28 10:30:45"
    },
    {
      "id": 2,
      "room": "101",
      "date": "2026-03-15",
      "time_start": "22:00",
      "time_end": "23:00",
      "type": "meeting",
      "result": false,
      "reason": "Аудитория работает только с 08:00 до 20:00",
      "checked_at": "2026-01-28 10:25:30"
    }
  ]
}
```

---

### 4. Get All Bookings
Получение всех успешных бронирований.

**Request:**
```http
GET /api/bookings-list/
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
      "created_at": "2026-01-28 11:00:00"
    },
    {
      "id": 1,
      "room": "101",
      "date": "2026-03-15",
      "time_start": "10:00",
      "time_end": "12:00",
      "type": "lesson",
      "created_at": "2026-01-28 10:30:00"
    }
  ]
}
```

---

## Validation Rules

### Time Constraints
- Working hours: **08:00 - 20:00**
- Bookings outside this range will be rejected

### Booking Types
Only these types are allowed:
- `lesson` - Урок
- `exam` - Экзамен
- `meeting` - Встреча

### Conflict Detection
The service checks for overlapping bookings:
- Same room
- Same date
- Overlapping time ranges

**Example of conflict:**
- Existing: Room 101, 10:00-12:00
- New request: Room 101, 11:00-13:00
- Result: ❌ Rejected (overlap detected)

---

## Example Usage (Python)
```python
import requests

# Check availability
response = requests.post(
    'http://localhost:8001/api/check/',
    json={
        "room": "101",
        "date": "2026-03-15",
        "time_start": "10:00",
        "time_end": "12:00",
        "type": "lesson"
    }
)

result = response.json()
if result['available']:
    print("✅ Room is available!")
else:
    print(f"❌ Not available: {result['reason']}")
```

## Example Usage (cURL)
```bash
curl -X POST http://localhost:8001/api/check/ \
  -H "Content-Type: application/json" \
  -d '{
    "room": "101",
    "date": "2026-03-15",
    "time_start": "10:00",
    "time_end": "12:00",
    "type": "lesson"
  }'
```
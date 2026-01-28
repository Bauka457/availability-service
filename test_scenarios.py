import requests
import json

BASE_URL = "http://localhost:8000/api/bookings/create/"


def test_scenario(name, data):
    print(f"\n{'=' * 60}")
    print(f"🧪 Тест: {name}")
    print(f"{'=' * 60}")
    print(f"📤 Отправляем: {json.dumps(data, indent=2, ensure_ascii=False)}")

    try:
        response = requests.post(BASE_URL, json=data, timeout=10)
        result = response.json()
        print(f"📥 Ответ ({response.status_code}):")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get('success'):
            print("✅ УСПЕХ")
        else:
            print(f"❌ ОТКЛОНЕНО: {result.get('reason', result.get('error'))}")
    except Exception as e:
        print(f"❌ ОШИБКА: {str(e)}")


# Тест 1: Успешное бронирование
test_scenario(
    "Успешное бронирование",
    {
        "email": "student1@example.com",
        "room": "101",
        "date": "2026-03-01",
        "time_start": "10:00",
        "time_end": "12:00",
        "type": "lesson"
    }
)

# Тест 2: Конфликт - та же аудитория, то же время
test_scenario(
    "Конфликт времени",
    {
        "email": "student2@example.com",
        "room": "101",
        "date": "2026-03-01",
        "time_start": "10:00",
        "time_end": "12:00",
        "type": "exam"
    }
)

# Тест 3: Нерабочее время
test_scenario(
    "Бронирование вне рабочего времени",
    {
        "email": "student3@example.com",
        "room": "102",
        "date": "2026-03-02",
        "time_start": "22:00",
        "time_end": "23:00",
        "type": "meeting"
    }
)

# Тест 4: Неверный тип
test_scenario(
    "Неверный тип бронирования",
    {
        "email": "student4@example.com",
        "room": "103",
        "date": "2026-03-03",
        "time_start": "14:00",
        "time_end": "16:00",
        "type": "party"
    }
)

# Тест 5: Успешное бронирование другой аудитории
test_scenario(
    "Успешное бронирование другой аудитории",
    {
        "email": "student5@example.com",
        "room": "104",
        "date": "2026-03-01",
        "time_start": "10:00",
        "time_end": "12:00",
        "type": "exam"
    }
)

print("\n" + "=" * 60)
print("✅ Все тесты завершены!")
print("=" * 60)
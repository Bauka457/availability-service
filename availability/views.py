from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, time
from django.shortcuts import render
from .models import Booking, AvailabilityCheck


# Веб-интерфейс
def dashboard(request):
    """Админ-панель сервиса проверки доступности"""
    return render(request, 'availability/dashboard.html')


# API
@api_view(['POST'])
def check_availability(request):
    """Проверяет доступность аудитории"""
    room = request.data.get('room')
    date = request.data.get('date')
    time_start = request.data.get('time_start')
    time_end = request.data.get('time_end')
    booking_type = request.data.get('type')

    print(f"\n{'=' * 50}")
    print(f"🔍 НОВЫЙ ЗАПРОС ПРОВЕРКИ")
    print(f"📍 Аудитория: {room}")
    print(f"📅 Дата: {date}")
    print(f"⏰ Время: {time_start} - {time_end}")
    print(f"📝 Тип: {booking_type}")
    print(f"{'=' * 50}\n")

    # Проверка наличия всех данных
    if not all([room, date, time_start, time_end, booking_type]):
        reason = "Не все данные заполнены"
        AvailabilityCheck.objects.create(
            room=room or "N/A",
            date=date or datetime.now().date(),
            time_start=time_start or "00:00",
            time_end=time_end or "00:00",
            booking_type=booking_type or "unknown",
            result=False,
            reason=reason
        )
        return Response({
            "available": False,
            "reason": reason
        }, status=400)

    # Сценарий 1: Проверка конфликтов
    conflicts = Booking.objects.filter(
        room=room,
        date=date,
        time_start__lt=time_end,
        time_end__gt=time_start
    )

    if conflicts.exists():
        reason = f"Аудитория занята в это время. Конфликтов: {conflicts.count()}"
        print(f"❌ {reason}")

        AvailabilityCheck.objects.create(
            room=room,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            time_start=datetime.strptime(time_start, "%H:%M").time(),
            time_end=datetime.strptime(time_end, "%H:%M").time(),
            booking_type=booking_type,
            result=False,
            reason=reason
        )

        return Response({
            "available": False,
            "reason": reason
        }, status=200)

    # Сценарий 2: Проверка рабочего времени (08:00-20:00)
    try:
        start = datetime.strptime(time_start, "%H:%M").time()
        end = datetime.strptime(time_end, "%H:%M").time()

        if start < time(8, 0) or end > time(20, 0):
            reason = "Аудитория работает только с 08:00 до 20:00"
            print(f"❌ {reason}")

            AvailabilityCheck.objects.create(
                room=room,
                date=datetime.strptime(date, "%Y-%m-%d").date(),
                time_start=start,
                time_end=end,
                booking_type=booking_type,
                result=False,
                reason=reason
            )

            return Response({
                "available": False,
                "reason": reason
            }, status=200)
    except ValueError:
        reason = "Неверный формат времени. Используйте HH:MM"

        AvailabilityCheck.objects.create(
            room=room,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            time_start="00:00",
            time_end="00:00",
            booking_type=booking_type,
            result=False,
            reason=reason
        )

        return Response({
            "available": False,
            "reason": reason
        }, status=400)

    # Сценарий 3: Проверка типа бронирования
    valid_types = ['lesson', 'exam', 'meeting']
    if booking_type not in valid_types:
        reason = f"Неизвестный тип бронирования. Допустимые: {', '.join(valid_types)}"
        print(f"❌ {reason}")

        AvailabilityCheck.objects.create(
            room=room,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            time_start=datetime.strptime(time_start, "%H:%M").time(),
            time_end=datetime.strptime(time_end, "%H:%M").time(),
            booking_type=booking_type,
            result=False,
            reason=reason
        )

        return Response({
            "available": False,
            "reason": reason
        }, status=200)

    # Всё ок! Создаём бронирование в БД Сервиса B
    Booking.objects.create(
        room=room,
        date=datetime.strptime(date, "%Y-%m-%d").date(),
        time_start=datetime.strptime(time_start, "%H:%M").time(),
        time_end=datetime.strptime(time_end, "%H:%M").time(),
        booking_type=booking_type
    )

    print(f"✅ Аудитория доступна!")

    AvailabilityCheck.objects.create(
        room=room,
        date=datetime.strptime(date, "%Y-%m-%d").date(),
        time_start=datetime.strptime(time_start, "%H:%M").time(),
        time_end=datetime.strptime(time_end, "%H:%M").time(),
        booking_type=booking_type,
        result=True,
        reason="Аудитория доступна"
    )

    return Response({
        "available": True,
        "message": "Аудитория доступна для бронирования"
    }, status=200)


@api_view(['GET'])
def get_all_checks(request):
    """Возвращает все проверки"""
    checks = AvailabilityCheck.objects.all()[:50]

    data = [{
        "id": c.id,
        "room": c.room,
        "date": str(c.date),
        "time_start": str(c.time_start)[:5],
        "time_end": str(c.time_end)[:5],
        "type": c.booking_type,
        "result": c.result,
        "reason": c.reason,
        "checked_at": c.checked_at.strftime("%Y-%m-%d %H:%M:%S")
    } for c in checks]

    return Response({
        "count": len(data),
        "checks": data
    })


@api_view(['GET'])
def get_all_bookings(request):
    """Возвращает все бронирования"""
    bookings = Booking.objects.all()[:50]

    data = [{
        "id": b.id,
        "room": b.room,
        "date": str(b.date),
        "time_start": str(b.time_start)[:5],
        "time_end": str(b.time_end)[:5],
        "type": b.booking_type,
        "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for b in bookings]

    return Response({
        "count": len(data),
        "bookings": data
    })


@api_view(['GET'])
def health_check(request):
    """Проверка работы сервиса"""
    return Response({
        "status": "ok",
        "service": "Availability Service"
    })
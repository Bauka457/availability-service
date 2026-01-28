import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Booking
from datetime import datetime


# Веб-страницы
def index(request):
    """Главная страница с формой бронирования"""
    return render(request, 'bookings/index.html')


def bookings_list_page(request):
    """Страница со списком бронирований"""
    return render(request, 'bookings/bookings_list.html')


def admin_panel(request):
    """Админ-панель для управления бронированиями"""
    return render(request, 'bookings/admin_panel.html')


# API endpoints
@api_view(['GET'])
def check_service_b_status(request):
    """Проверяет доступность сервиса B"""
    try:
        response = requests.get(
            'http://localhost:8001/api/health/',
            timeout=3
        )
        if response.status_code == 200:
            return Response({"available": True})
    except:
        pass
    return Response({"available": False})


@api_view(['POST'])
def create_booking(request):
    """Создаёт бронирование через проверку в сервисе доступности"""

    room = request.data.get('room')
    date = request.data.get('date')
    time_start = request.data.get('time_start')
    time_end = request.data.get('time_end')
    booking_type = request.data.get('type')
    user_email = request.data.get('email')

    if not all([room, date, time_start, time_end, booking_type, user_email]):
        return Response({
            "success": False,
            "error": "Не все поля заполнены"
        }, status=400)

    availability_data = {
        "room": room,
        "date": date,
        "time_start": time_start,
        "time_end": time_end,
        "type": booking_type,
    }

    try:
        print(f"🔄 Отправляем запрос в Сервис B: {settings.AVAILABILITY_SERVICE_URL}")
        print(f"📦 Данные: {availability_data}")

        response = requests.post(
            settings.AVAILABILITY_SERVICE_URL,
            json=availability_data,
            timeout=10
        )

        print(f"✅ Получен ответ от Сервиса B: {response.status_code}")

        if response.status_code != 200:
            return Response({
                "success": False,
                "error": "Сервис проверки доступности вернул ошибку",
                "details": response.text
            }, status=503)

        availability = response.json()

        if availability.get('available'):
            booking = Booking.objects.create(
                room=room,
                date=datetime.strptime(date, "%Y-%m-%d").date(),
                time_start=datetime.strptime(time_start, "%H:%M").time(),
                time_end=datetime.strptime(time_end, "%H:%M").time(),
                booking_type=booking_type,
                user_email=user_email
            )

            print(f"✅ Бронирование создано: ID {booking.id}")

            return Response({
                "success": True,
                "message": "Бронирование успешно создано",
                "booking": {
                    "id": booking.id,
                    "room": booking.room,
                    "date": str(booking.date),
                    "time_start": str(booking.time_start),
                    "time_end": str(booking.time_end),
                    "type": booking.booking_type,
                    "email": booking.user_email
                }
            }, status=201)
        else:
            print(f"❌ Аудитория недоступна: {availability.get('reason')}")
            return Response({
                "success": False,
                "reason": availability.get('reason')
            }, status=400)

    except requests.exceptions.Timeout:
        print("⏰ Timeout при обращении к Сервису B")
        return Response({
            "success": False,
            "error": "Сервис проверки не отвечает (timeout)"
        }, status=503)
    except requests.exceptions.ConnectionError:
        print("🔌 Ошибка подключения к Сервису B")
        return Response({
            "success": False,
            "error": "Не удалось подключиться к сервису проверки. Убедитесь, что он запущен на порту 8001."
        }, status=503)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {str(e)}")
        return Response({
            "success": False,
            "error": f"Неожиданная ошибка: {str(e)}"
        }, status=500)


@api_view(['GET'])
def list_bookings(request):
    """Список всех бронирований"""
    bookings = Booking.objects.all().order_by('-created_at')[:50]

    data = [{
        "id": b.id,
        "room": b.room,
        "date": str(b.date),
        "time_start": str(b.time_start)[:5],
        "time_end": str(b.time_end)[:5],
        "type": b.booking_type,
        "email": b.user_email,
        "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for b in bookings]

    return Response({
        "count": len(data),
        "bookings": data
    })


@api_view(['GET'])
def get_booking_detail(request, booking_id):
    """Получить детали конкретного бронирования"""
    try:
        booking = Booking.objects.get(id=booking_id)
        return Response({
            "id": booking.id,
            "room": booking.room,
            "date": str(booking.date),
            "time_start": str(booking.time_start)[:5],
            "time_end": str(booking.time_end)[:5],
            "type": booking.booking_type,
            "email": booking.user_email,
            "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    except Booking.DoesNotExist:
        return Response({
            "error": "Бронирование не найдено"
        }, status=404)


@api_view(['PUT'])
def update_booking(request, booking_id):
    """Обновить бронирование"""
    try:
        booking = Booking.objects.get(id=booking_id)

        # Получаем новые данные
        room = request.data.get('room', booking.room)
        date = request.data.get('date', str(booking.date))
        time_start = request.data.get('time_start', str(booking.time_start)[:5])
        time_end = request.data.get('time_end', str(booking.time_end)[:5])
        booking_type = request.data.get('type', booking.booking_type)
        user_email = request.data.get('email', booking.user_email)

        # Проверяем доступность в Сервисе B (если изменилось время/дата/аудитория)
        if (room != booking.room or date != str(booking.date) or
                time_start != str(booking.time_start)[:5] or
                time_end != str(booking.time_end)[:5]):

            availability_data = {
                "room": room,
                "date": date,
                "time_start": time_start,
                "time_end": time_end,
                "type": booking_type,
            }

            try:
                response = requests.post(
                    settings.AVAILABILITY_SERVICE_URL,
                    json=availability_data,
                    timeout=10
                )

                if response.status_code == 200:
                    availability = response.json()
                    if not availability.get('available'):
                        return Response({
                            "success": False,
                            "reason": availability.get('reason')
                        }, status=400)
            except:
                return Response({
                    "success": False,
                    "error": "Не удалось проверить доступность"
                }, status=503)

        # Обновляем бронирование
        booking.room = room
        booking.date = datetime.strptime(date, "%Y-%m-%d").date()
        booking.time_start = datetime.strptime(time_start, "%H:%M").time()
        booking.time_end = datetime.strptime(time_end, "%H:%M").time()
        booking.booking_type = booking_type
        booking.user_email = user_email
        booking.save()

        print(f"✏️ Бронирование {booking_id} обновлено")

        return Response({
            "success": True,
            "message": "Бронирование успешно обновлено",
            "booking": {
                "id": booking.id,
                "room": booking.room,
                "date": str(booking.date),
                "time_start": str(booking.time_start)[:5],
                "time_end": str(booking.time_end)[:5],
                "type": booking.booking_type,
                "email": booking.user_email
            }
        })

    except Booking.DoesNotExist:
        return Response({
            "success": False,
            "error": "Бронирование не найдено"
        }, status=404)


@api_view(['DELETE'])
def delete_booking(request, booking_id):
    """Удалить бронирование"""
    try:
        booking = Booking.objects.get(id=booking_id)
        booking_info = f"ID {booking.id} - {booking.room} - {booking.date}"
        booking.delete()

        print(f"🗑️ Бронирование удалено: {booking_info}")

        return Response({
            "success": True,
            "message": f"Бронирование {booking_id} успешно удалено"
        })
    except Booking.DoesNotExist:
        return Response({
            "success": False,
            "error": "Бронирование не найдено"
        }, status=404)


@api_view(['GET'])
def health_check(request):
    """Проверка работы сервиса"""
    return Response({
        "status": "ok",
        "service": "Booking Service"
    })
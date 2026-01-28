from django.db import models


class Booking(models.Model):
    BOOKING_TYPES = [
        ('lesson', 'Урок'),
        ('exam', 'Экзамен'),
        ('meeting', 'Встреча'),
    ]

    room = models.CharField(max_length=10)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Аудитория {self.room} - {self.date} {self.time_start}"


class AvailabilityCheck(models.Model):
    """Логирование всех проверок доступности"""
    room = models.CharField(max_length=10)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    booking_type = models.CharField(max_length=20)
    result = models.BooleanField()  # True = доступна, False = занята
    reason = models.TextField(blank=True, null=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-checked_at']

    def __str__(self):
        status = "✅ Доступна" if self.result else "❌ Недоступна"
        return f"{self.room} - {self.date} - {status}"
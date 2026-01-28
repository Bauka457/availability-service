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
    user_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_email} - {self.room} - {self.date}"
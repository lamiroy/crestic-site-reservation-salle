from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rooms.models import RoomCategory
from django.db import models
from django.urls import reverse
from datetime import date, datetime, time


class BookedRoom(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('canceled', 'Annulé'),
        ('validated', 'Validé'),
    ]

    LABORATORY_CHOICES = [
        ('CReSTIC', 'CReSTIC'),
        ('Labi*', 'Labi*'),
        ('Liciis', 'Liciis'),
    ]

    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    groups = models.CharField(max_length=100, choices=LABORATORY_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    motif = models.CharField(max_length=100)
    peopleAmount = models.IntegerField(default=1)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    room_category = models.ForeignKey(
        RoomCategory,
        on_delete=models.CASCADE,
    )

    def clean(self):
        # Your existing validation logic from form_valid() method
        selected_date = self.date
        if selected_date < date.today():
            raise ValidationError('Vous ne pouvez pas changer la date pour une date antérieure à aujourd\'hui.')

        start_time = self.startTime
        if start_time:
            if start_time < time(6, 0) or start_time > time(19, 30):
                raise ValidationError('L\'heure de début doit être entre 6h00 et 19h30.')

            if selected_date == date.today():
                current_time = datetime.now().time()
                new_hour = current_time.hour + 1
                new_minute = current_time.minute + 30
                if new_minute >= 60:
                    new_hour += 1
                    new_minute -= 60
                min_start_time = time(new_hour, new_minute)
                if start_time <= min_start_time:
                    raise ValidationError('L\'heure de début doit être supérieure à 1h30 de l\'heure actuelle.')

        end_time = self.endTime
        if end_time:
            if end_time < time(6, 0) or end_time > time(22, 0):
                raise ValidationError('L\'heure de fin doit être entre 6h00 et 22h00.')

            if end_time <= start_time:
                raise ValidationError('L\'heure de fin doit être supérieure à l\'heure de début.')

        # For new bookings, the start date should not be less than today's date

        # For old bookings, you can't update the details 4 days before the start date

        # Loop through the start and end dates
        '''
        day = timedelta(days=1)
        start = self.start_date
        end = self.end_date
        current = start
        while current < end:
            print(current)
            # Retrieve booked rooms that fall into this date
            rooms = BookedRoom.objects.filter(
                start_date__lte=current,
                end_date__gt=current,
                room_category__libRoom=self.room_category.libRoom)
            print("\tNbr of results: {}".format(rooms.count()))

            # Sum the totals
            total_booked_rooms = 0
            for room in rooms:
                total_booked_rooms = total_booked_rooms + room.peopleAmount

            total_available_rooms = RoomCategory.objects.filter(
                libRoom=self.room_category.libRoom)[0].maxCapacity
            # Check if there is an instance of this room so as to
            # not add the current peopleAmount
            current_room = BookedRoom.objects.filter(id=self.id)
            if current_room.count() == 1:
                remaining = total_available_rooms - total_booked_rooms + current_room[0].peopleAmount
            else:
                remaining = total_available_rooms - total_booked_rooms

            print("\t\tRemaining Rooms: {}".format(remaining))
            print("\t\tNbr of rooms:{}".format(self.peopleAmount))

            if self.peopleAmount > remaining:
                raise ValidationError(
                    "On {} there are less rooms than you desire. ({} > {})".format(
                        current, self.peopleAmount, remaining))
            current += day
            '''

    def get_absolute_url(self):
        return reverse('bookedrooms_detail', args=[str(self.id)])

    def __str__(self):
        return self.room_category.libRoom + " |  " + self.user.username

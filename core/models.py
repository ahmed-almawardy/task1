import time

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Days(models.TextChoices):
    """Days of week prepared to DB"""

    SATURDAY = 'saturday', 'Saturday'
    SUNDAY = 'sunday', 'Sunday'
    MONDAY = 'monday', 'Monday'
    TUESDAY = 'tuesday', 'Tuesday'
    WEDNESDAY = 'wednesday', 'Wednesday'
    THURSDAY = 'thursday', 'Thursday'
    FRIDAY = 'friday', 'Friday'


class WorkShift(models.Model):
    """Describes a shift related with day in a restaurant"""

    opening_time = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(settings.MAX_TOTAL_SECONDS)], null=True)
    closing_time = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(settings.MAX_TOTAL_SECONDS)], null=True)
    is_closed = models.BooleanField(default=False)
    day = models.CharField(max_length=9, choices=Days.choices)

    def __to_time_struct(self, total_seconds):
        return time.gmtime(total_seconds)

    def __convert_to_str_readable(self, total_seconds):
        struct_time = self.__to_time_struct(total_seconds)
        return time.strftime(settings.TIME_FORMAT, struct_time)

    def readable(self, with_day=True):
        if self.is_closed:
            return f'{self.day.title()}: Closed'
        opens_at = self.__convert_to_str_readable(self.opening_time)
        closes_at = self.__convert_to_str_readable(self.closing_time)
        if with_day:
            return f'{self.day.title()}: {opens_at} - {closes_at}'
        return f'{opens_at} - {closes_at}'

    def save(self, *args, **kwargs):
        """Making is closed and same day attrs dynamically assigned due to the open and close time """

        self.is_closed = self.closing_time is self.opening_time is None
        return super().save(*args, **kwargs)

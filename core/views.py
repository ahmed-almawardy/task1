from rest_framework.generics import CreateAPIView
from django.http import HttpResponse


from core.models import WorkShift, Days


class WorkShiftAPI(CreateAPIView):
    queryset = WorkShift.objects.all()

    def create(self, request, *args, **kwargs):
        work_shifts = []
        cur_day = None
        row = dict()
        for day, time_table in request.data.items():
            if not time_table:
                work_shifts.append(WorkShift(day=Days[day.upper()], opening_time=None,
                                             closing_time=None, is_closed=True))
                cur_day = day

            for working_hours in time_table:
                if working_hours['type'] == 'open':
                    row['opening_time'] = working_hours['value']
                elif working_hours['type'] == 'close':
                    row['closing_time'] = working_hours['value']

                if len(row) % 2 == 0:
                    work_shifts.append(WorkShift(day=Days[cur_day.upper()], opening_time=row['opening_time'],
                                                 closing_time=row['closing_time']))
                    row = dict()
                    cur_day = None
                else:
                    cur_day = day

        created = WorkShift.objects.bulk_create(work_shifts)
        response = self.__to_plain_text(created)
        return HttpResponse(response)

    def __to_plain_text(self, objects):
        """generating a str response"""
        days = dict()
        for o in objects:
            if o.day in days:
                days[o.day] = days[o.day] + ', ' + o.readable(with_day=False)
            else:
                days[o.day] = o.readable()

        return '\n'.join(days.values())

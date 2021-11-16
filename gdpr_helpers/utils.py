from django.utils.timezone import datetime, localdate, localtime, make_aware, timedelta


def aware_timedelta_days(to_move: datetime, timedelta_days: timedelta) -> datetime:
    # This is to check for correct timezone/DST setting, see why we separate date and time here:
    # https://gist.github.com/codeinthehole/1ac10da7874033406f25f86df07b88ff
    to_move_date = localdate(to_move) + timedelta_days
    to_move_time = localtime(to_move).time()

    return make_aware(datetime.combine(to_move_date, to_move_time))

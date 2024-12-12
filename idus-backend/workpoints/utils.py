from datetime import datetime, timedelta


def calculate_worked_hours(points, start_date, end_date, scale):
    """
    Calcula as horas trabalhadas para cada dia entre start_date e end_date,
    levando em consideração a escala de trabalho.

    :param points: Lista de pontos no formato especificado
    :param start_date: Data inicial (datetime.date)
    :param end_date: Data final (datetime.date)
    :param scale: Escala de trabalho ("5x1", "6x1", "12x36", "4h", "6h")
    :return: Total de horas trabalhadas (float)
    """
    points_by_date = {
        datetime.strptime(point["date_point"], "%d/%m/%Y").date(): point
        for point in points
    }

    if not any(
        start_date <= date <= end_date and point.get("timestamp")
        for date, point in points_by_date.items()
    ):
        return 0.0

    total_hours = timedelta()
    current_date = start_date

    while current_date <= end_date:
        daily_hours = timedelta()
        point = points_by_date.get(current_date, None)
        weekday = current_date.weekday()

        if scale == "5x1":
            expected_hours = 8 if weekday < 6 else 8
        elif scale == "6x1":
            expected_hours = 7 + 20 / 60
        elif scale == "12x36":
            expected_hours = 12 if weekday % 2 == 0 else 0
        elif scale == "4h":
            expected_hours = 4
        elif scale == "6h":
            expected_hours = 6
        else:
            raise ValueError("Escala inválida!")

        if point:
            timestamps = point.get("timestamp", [])
            if not timestamps:
                if scale == "5x1" and weekday == 6:
                    daily_hours += timedelta(hours=8)
                elif scale == "6x1" and weekday == 6:
                    daily_hours += timedelta(hours=7, minutes=20)
                elif scale == "4h" and weekday == 6:
                    daily_hours += timedelta(hours=4)
            else:
                timestamps.sort(key=lambda t: datetime.strptime(t["time"], "%H:%M:%S"))
                i = 0
                while i < len(timestamps) - 1:
                    start = timestamps[i]
                    end = timestamps[i + 1]
                    if start["type"] == "in" and end["type"] == "out":
                        start_time = datetime.strptime(start["time"], "%H:%M:%S")
                        end_time = datetime.strptime(end["time"], "%H:%M:%S")
                        daily_hours += end_time - start_time
                    i += 2
        else:
            if scale == "5x1" and weekday == 6:
                daily_hours += timedelta(hours=8)
            elif scale == "6x1" and weekday == 6:
                daily_hours += timedelta(hours=7, minutes=20)
            elif scale == "4h" and weekday == 6:
                daily_hours += timedelta(hours=4)
            elif scale in ["5x1", "6x1"] and weekday != 6:
                daily_hours += timedelta(hours=expected_hours)

        total_hours += daily_hours
        current_date += timedelta(days=1)

    total_hours_decimal = round(total_hours.total_seconds() / 3600, 4)
    return round(total_hours_decimal, 2)


def calculate_remaining_hours(total_worked, work_schedule, period_days):
    required_hours = int(work_schedule.replace("h", ""))
    missing_hours_total = 0

    for day in period_days:
        weekday = day["weekday"]
        timestamps = day.get("timestamp", [])

        total_hours = timedelta()
        in_time = None

        if weekday == "domingo":
            if work_schedule == "8h":
                worked_hours = 8
            elif work_schedule == "6h":
                worked_hours = 7 + 20 / 60
            elif work_schedule == "4h":
                worked_hours = 4
        elif weekday == "sábado":
            if work_schedule == "8h":
                worked_hours = 4
            elif work_schedule == "6h":
                worked_hours = 7 + 20 / 60
            elif work_schedule == "4h":
                worked_hours = 0
        else:
            for entry in timestamps:
                if entry["type"] == "in":
                    in_time = datetime.strptime(entry["time"], "%H:%M:%S")
                elif entry["type"] == "out" and in_time:
                    out_time = datetime.strptime(entry["time"], "%H:%M:%S")
                    total_hours += out_time - in_time
                    in_time = None

            worked_hours = total_hours.total_seconds() / 3600

        if worked_hours < required_hours:
            missing_hours_total += required_hours - worked_hours

    return round(missing_hours_total, 2)


def calculate_extra_hours(total_worked, work_schedule, period_days):
    """
    Calcula as horas extras realizadas no período selecionado.
    Retorna as horas excedentes como timedelta, ou 00:00 se não houver horas extras.
    """
    if isinstance(total_worked, (int, float)):
        total_worked = timedelta(hours=total_worked)

    daily_hours = timedelta(hours=6 if work_schedule == "6h" else 8)
    total_target = timedelta()

    for day in period_days:
        if isinstance(day, dict):
            day = datetime.strptime(day["date_point"], "%d/%m/%Y").date()

        if day.weekday() < 5:
            total_target += daily_hours
        else:
            total_target += timedelta(hours=6)

    extra = total_worked - total_target

    return extra if extra > timedelta() else timedelta()

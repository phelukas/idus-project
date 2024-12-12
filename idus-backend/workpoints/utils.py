from datetime import datetime, timedelta


def calculate_worked_hours(points):
    """
    Calcula o total de horas trabalhadas no período selecionado.
    Retorna o total de horas como um número (inteiro ou decimal).
    """
    if not points:
        return 0

    grouped_by_day = {}
    for point in points:
        if isinstance(point, dict):
            day = datetime.strptime(point["date_point"], "%d/%m/%Y").date()
            entries = point["timestamp"]
        else:
            day = point.timestamp.date()
            entries = grouped_by_day.get(day, [])
            entries.append(
                {"time": point.timestamp.strftime("%H:%M:%S"), "type": point.type}
            )
        grouped_by_day[day] = entries

    total_hours = timedelta()

    for day, day_points in grouped_by_day.items():
        sorted_points = sorted(
            day_points, key=lambda x: datetime.strptime(x["time"], "%H:%M:%S")
        )

        daily_worked = timedelta()
        i = 0
        while i < len(sorted_points) - 1:
            start = sorted_points[i]
            end = sorted_points[i + 1]

            if start["type"] == "in" and end["type"] == "out":
                start_time = datetime.strptime(start["time"], "%H:%M:%S")
                end_time = datetime.strptime(end["time"], "%H:%M:%S")
                daily_worked += end_time - start_time
                i += 2
            else:
                i += 1

        total_hours += daily_worked

    total_seconds = total_hours.total_seconds()
    total_hours_decimal = total_seconds / 3600
    return round(total_hours_decimal, 2)


def calculate_remaining_hours(total_worked, work_schedule, period_days):
    """
    Calcula o total de horas faltantes ou excedentes para o período selecionado.
    Retorna um número decimal indicando a diferença em horas (positivo para faltas, negativo para horas excedentes).
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

    remaining = total_target - total_worked

    remaining_hours_decimal = remaining.total_seconds() / 3600

    return round(remaining_hours_decimal, 2)


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

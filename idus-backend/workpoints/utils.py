from datetime import timedelta


def calculate_worked_hours(points):
    """
    Calcula o total de horas trabalhadas no período selecionado.
    Retorna o total de horas como um número (inteiro ou decimal).
    """
    if not points:
        return 0

    grouped_by_day = {}
    for point in points:
        day = point.timestamp.date()
        if day not in grouped_by_day:
            grouped_by_day[day] = []
        grouped_by_day[day].append(point)

    total_hours = timedelta()

    for day, day_points in grouped_by_day.items():
        day_points = sorted(day_points, key=lambda x: x.timestamp)

        daily_worked = timedelta()
        for i in range(0, len(day_points) - 1, 2):
            start = day_points[i]
            end = day_points[i + 1]

            if start.type == "in" and end.type == "out":
                daily_worked += end.timestamp - start.timestamp

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
        if day.weekday() < 5:
            total_target += daily_hours
        else:

            pass

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
        if day.weekday() < 5:
            total_target += daily_hours
        else:
            total_target += timedelta(hours=6)

    extra = total_worked - total_target

    return extra if extra > timedelta() else timedelta()

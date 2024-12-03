from datetime import timedelta


def calculate_worked_hours(points):
    """
    Calcula o total de horas trabalhadas baseado nos registros de pontos.
    """
    total_hours = timedelta()
    for i in range(0, len(points), 2):
        if i + 1 < len(points):
            start = points[i].timestamp
            end = points[i + 1].timestamp
            total_hours += end - start
    return total_hours


def calculate_remaining_hours(total_worked, work_schedule):
    """
    Calcula as horas restantes para completar a jornada.
    """
    if work_schedule == "6h":
        target = timedelta(hours=6)
    elif work_schedule == "8h":
        target = timedelta(hours=8)
    else:
        raise ValueError("Regime de jornada inválido.")
    remaining = target - total_worked
    return remaining if remaining > timedelta() else timedelta()


def calculate_extra_hours(total_worked, work_schedule):
    """
    Calcula as horas excedentes na jornada.
    """
    if work_schedule == "6h":
        target = timedelta(hours=6)
    elif work_schedule == "8h":
        target = timedelta(hours=8)
    else:
        raise ValueError("Regime de jornada inválido.")
    extra = total_worked - target
    return extra if extra > timedelta() else timedelta()


def calculate_completion_time(points, work_schedule):
    total_worked = calculate_worked_hours(points)
    remaining = calculate_remaining_hours(total_worked, work_schedule)

    if remaining > timedelta():
        last_point = points.last()
        if last_point:
            return last_point.timestamp + remaining
    return None

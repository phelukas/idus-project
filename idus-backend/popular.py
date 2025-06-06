import os
import django
from datetime import datetime, timedelta, time

# Debug para verificar o caminho do módulo de configurações
try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "idus_backend.settings")
    django.setup()
except Exception as e:
    print(f"Erro ao configurar Django: {e}")
    raise

from django.db import transaction
from django.utils.timezone import make_aware
import pytz
from users.models import User
from workpoints.models import WorkPoint

# Configurações iniciais
timezone = pytz.timezone("America/Sao_Paulo")
date_format = "%Y-%m-%d"

# Definir o período e horários de batida de ponto
start_date = datetime.strptime("2024-11-01", date_format).date()
end_date = datetime.strptime("2024-11-30", date_format).date()
weekdays_hours = [
    time(5, 54),
    time(9, 54),
    # time(10, 54),
    # time(14, 54),
]
saturdays_hours = [
    time(5, 54),
    time(9, 54),
]

# Criar usuário (se não existir)
cpf = "05158578079"
email = "estagiario@example.com"
first_name = "estagiario"
last_name = "estagiario"
password = "password123"

try:
    user = User.objects.get(cpf=cpf)
    created = False
except User.DoesNotExist:
    user = User.objects.create_user(
        cpf=cpf,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )
    created = True

if created:
    print(f"Usuário {first_name} {last_name} criado com sucesso.")
else:
    print(f"Usuário {first_name} {last_name} já existe.")


# Função para criar batidas de ponto com rollback em caso de falha
def create_work_points(user, start_date, end_date, weekdays_hours, saturdays_hours):
    current_date = start_date

    try:
        with transaction.atomic():
            while current_date <= end_date:
                if current_date.weekday() < 5:  # Segunda a sexta
                    hours = weekdays_hours
                # elif current_date.weekday() == 5:  # Sábado
                #     hours = saturdays_hours
                else:  # Domingo
                    current_date += timedelta(days=1)
                    continue

                # Verificar a última batida do dia anterior
                last_point = (
                    WorkPoint.objects.filter(user=user, timestamp__date=current_date)
                    .order_by("-timestamp")
                    .first()
                )
                is_in_next = not last_point or last_point.type == "out"

                for hour in hours:
                    timestamp = datetime.combine(current_date, hour)
                    aware_timestamp = make_aware(timestamp, timezone)

                    WorkPoint.objects.create(
                        user=user,
                        timestamp=aware_timestamp,
                        type="in" if is_in_next else "out",
                    )
                    is_in_next = not is_in_next

                current_date += timedelta(days=1)
    except Exception as e:
        print(f"Erro ao criar batidas de ponto: {e}")
        raise


# Criar as batidas de ponto
create_work_points(user, start_date, end_date, weekdays_hours, saturdays_hours)

print("Batidas de ponto criadas com sucesso.")

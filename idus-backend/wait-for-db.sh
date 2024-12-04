#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "Aguardando o banco de dados no host $host..."

until pg_isready -h "$host" -p 5432 -q; do
  >&2 echo "Postgres está indisponível - aguardando..."
  sleep 1
done

>&2 echo "Postgres está pronto - aplicando migrações"
python manage.py migrate

>&2 echo "Iniciando o servidor"
exec $cmd

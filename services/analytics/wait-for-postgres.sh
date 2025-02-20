#!/bin/bash
set -e

host="db"
port="5432"

echo "En attente de PostgreSQL à $host:$port..."

until pg_isready -h $host -p $port -U user; do
  sleep 1
done

echo "PostgreSQL est prêt, lancement de l'application !"
exec "$@"

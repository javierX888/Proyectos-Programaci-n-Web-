#!/bin/bash

ORACLE_HOST=$1
ORACLE_PORT=$2
ORACLE_SID=$3
ORACLE_USER=$4
ORACLE_PASSWORD=$5

echo "Esperando a que la base de datos Oracle esté lista..."

until echo "exit" | sqlplus -s "${ORACLE_USER}/${ORACLE_PASSWORD}@//${ORACLE_HOST}:${ORACLE_PORT}/${ORACLE_SID}" > /dev/null 2>&1
do
  echo -n "."
  sleep 5
done

echo
echo "La base de datos Oracle está lista para aceptar conexiones."
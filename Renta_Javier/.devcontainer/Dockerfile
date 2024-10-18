FROM python:3.10

WORKDIR /app

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y libaio1 wget unzip

# Descargar e instalar Oracle Instant Client
RUN mkdir -p /opt/oracle && \
    wget https://download.oracle.com/otn_software/linux/instantclient/219000/instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip && \
    wget https://download.oracle.com/otn_software/linux/instantclient/219000/instantclient-sqlplus-linux.x64-21.9.0.0.0dbru.zip && \
    unzip instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip -d /opt/oracle && \
    unzip instantclient-sqlplus-linux.x64-21.9.0.0.0dbru.zip -d /opt/oracle && \
    rm -f instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip instantclient-sqlplus-linux.x64-21.9.0.0.0dbru.zip && \
    sh -c "echo /opt/oracle/instantclient_21_9 > /etc/ld.so.conf.d/oracle-instantclient.conf" && \
    ldconfig

# Configurar variables de entorno para Oracle
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_9
ENV PATH=$PATH:/opt/oracle/instantclient_21_9

# Copiar requirements.txt y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los scripts de espera
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY wait-for-oracle.sh /wait-for-oracle.sh
RUN chmod +x /wait-for-oracle.sh

# Copiar el resto del código
COPY . .

# Comando por defecto
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
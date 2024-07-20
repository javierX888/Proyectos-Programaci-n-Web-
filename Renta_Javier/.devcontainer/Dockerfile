# Usa la imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos requirements.txt y .env al contenedor
COPY requirements.txt ./
COPY .env ./

# Copia todo el contenido del proyecto en el directorio de trabajo del contenedor
COPY ../ ./

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libaio1 \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip
RUN pip install --upgrade pip

# Descarga e instala Oracle Instant Client y SQL*Plus
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2340000/instantclient-basic-linux.x64-23.4.0.24.05.zip \
    && wget https://download.oracle.com/otn_software/linux/instantclient/2340000/instantclient-sqlplus-linux.x64-23.4.0.24.05.zip \
    && mkdir -p /opt/oracle \
    && unzip -o instantclient-basic-linux.x64-23.4.0.24.05.zip -d /opt/oracle \
    && unzip -o instantclient-sqlplus-linux.x64-23.4.0.24.05.zip -d /opt/oracle \
    && rm instantclient-basic-linux.x64-23.4.0.24.05.zip instantclient-sqlplus-linux.x64-23.4.0.24.05.zip \
    && ln -sf /opt/oracle/instantclient_23_4/libclntsh.so.23.1 /opt/oracle/instantclient_23_4/libclntsh.so \
    && ln -sf /opt/oracle/instantclient_23_4/sqlplus /usr/bin/sqlplus

# Establece las variables de entorno para Oracle Instant Client
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_23_4 
ENV PATH=/opt/oracle/instantclient_23_4:$PATH

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Crea el usuario vscode y establece los permisos adecuados
RUN useradd -ms /bin/bash vscode && chown -R vscode:vscode /app

# Establece el usuario vscode para ejecutar comandos
USER vscode

# Expone el puerto 8000 para el servicio (puerto estándar de desarrollo de Django)
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación (en el servidor de desarrollo de Django)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

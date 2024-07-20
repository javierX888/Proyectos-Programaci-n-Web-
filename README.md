# Rentas Chile

## Acerca del Proyecto

Rentas Chile es una plataforma de alquiler de alojamientos inspirada en Airbnb, adaptada específicamente para el mercado chileno. Este proyecto utiliza Django como framework backend y Oracle como base de datos, ofreciendo una solución robusta para la gestión de alquileres en Chile.

### Construido Con

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
- ![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white)
- ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
- ![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
- ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Comenzando

Siga estas instrucciones para configurar el proyecto en su máquina local.

### Prerrequisitos

Asegúrese de tener instalado:
- Docker(en caso de que no quiera instalar Oracle y Django localmente)
- Python 3.10+
- Oracle Database 19c (puede ser en un contenedor Docker)

### Instalación

1. Clone el repositorio
   ```sh
   git clone https://github.com/javierX888/ProyectosWeb.git
   ```

2. Navegue al directorio del proyecto
   ```sh
   cd RentaStay-Chile
   ```

3. Cree un archivo .env en la raíz del proyecto y configure las variables de entorno necesarias
   ```
   SECRET_KEY=insecure-i0wv*o49r)huc_*ebh$!o&ps0kych_9dp&h43#kno(ey^1oz_b
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0(direcciones aceptadas)
   ORACLE_USER=nombre_usuario
   ORACLE_PASSWORD=contraseña_usuario
   ORACLE_HOST=nombre_host
   ORACLE_PORT=puerto_oracle(por lo general es 1521)
   ORACLE_SID=nombre_sid
  
  Ruta al Oracle Instant Client
  lib_dir=(ejemplo:/opt/oracle/instantclient_23_4/)
   ```
   
4. Construya y ejecute los contenedores Docker
   ```sh
   docker-compose up --build
   ```

5. Ejecute las migraciones
   ```sh
   python manage.py migrate
   ```

6. Acceda a la aplicación en su navegador
   ```
   http://localhost:8000
   ```

## Uso

El sistema permite a los usuarios:
- Registrarse y iniciar sesión
- Buscar alojamientos disponibles en Chile
- Publicar sus propiedades para alquilar
- Realizar reservas
- Gestionar sus reservas y propiedades

## Estructura del Proyecto

- `accounts/`: Aplicación Django para la gestión de usuarios
- `pages/`: Aplicación Django para las páginas estáticas
- `rentastay/`: Proyecto Django principal
- `static/`: Archivos estáticos (CSS, JS, imágenes)
- `templates/`: Plantillas HTML de Django
- `media/`: Archivos subidos por los usuarios

## Desarrollo

Para trabajar en el desarrollo:

1. Cree un entorno virtual
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows use `venv\Scripts\activate`
   ```

2. Instale las dependencias
   ```sh
   pip install -r requirements.txt
   ```

3. Ejecute el servidor de desarrollo
   ```sh
   python manage.py runserver localhost:8000
   ```

## Contacto

[Javier Gacitúa] - [ja.gacitua@duocuc.cl]

Enlace del Proyecto: https://github.com/javierX888/ProyectosWeb.git
import os
import sys
import django
from django.conf import settings
from django.db import connection
from django.db.backends.oracle.base import DatabaseWrapper as OracleDatabaseWrapper



# Añadir el directorio del proyecto al Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)



# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rentastay.settings")
django.setup()





tabla = "CITIES"

try:
    print(f"Proveedor de base de datos: {connection.vendor}")
    
    # Intentar obtener la versión de manera segura
    if hasattr(connection, 'version'):
        print(f"Versión de la base de datos: {connection.version}")
    elif isinstance(connection, OracleDatabaseWrapper):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM v$version")
            version = cursor.fetchone()
            print(f"Versión de Oracle: {version[0] if version else 'Desconocida'}")
    else:
        print("No se pudo determinar la versión de la base de datos.")
    
    # Imprimir información de diagnóstico
    print(f"Nombre de la base de datos: {connection.settings_dict['NAME']}")
    print(f"Usuario: {connection.settings_dict['USER']}")
    print(f"Host: {connection.settings_dict['HOST']}")
    print(f"Puerto: {connection.settings_dict['PORT']}")
    
    # Intentar obtener información del listener
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM v$session_connect_info WHERE sid = SYS_CONTEXT('USERENV', 'SID')")
            listener_info = cursor.fetchall()
            if listener_info:
                print("\nInformación del Listener:")
                for info in listener_info:
                    print(f"{info[1]}: {info[2]}")
            else:
                print("\nNo se pudo obtener información del Listener.")
            
            # Intentar obtener la ubicación del listener
            cursor.execute("SELECT value FROM v$parameter WHERE name = 'listener_networks'")
            listener_location = cursor.fetchone()
            if listener_location:
                print(f"\nUbicación del Listener: {listener_location[0]}")
            else:
                print("\nNo se pudo obtener la ubicación específica del Listener.")
                
            # Obtener información adicional del listener
            cursor.execute("SELECT * FROM v$listener")
            listener_details = cursor.fetchone()
            if listener_details:
                print(f"Detalles adicionales del Listener:")
                print(f"Nombre: {listener_details[0]}")
                print(f"Estado: {listener_details[2]}")
            else:
                print("No se pudieron obtener detalles adicionales del Listener.")
        
        except Exception as listener_error:
            print(f"\nError al obtener información del Listener: {listener_error}")
        
        try:
            cursor.execute(f"SELECT * FROM {tabla}")
            rows = cursor.fetchall()
            
            if rows:
                print(f"\nRegistros en la tabla {tabla}:")
                for row in rows:
                    print(row)
            else:
                print("\nNo se encontraron registros en la tabla {tabla}.")
        except Exception as table_error:
            print(f"\nError al consultar la tabla {tabla}: {table_error}")
            print("Intentando listar las tablas disponibles...")
            cursor.execute("SELECT table_name FROM user_tables")
            tables = cursor.fetchall()
            print("Tablas disponibles:")
            for table in tables:
                print(table[0])

except Exception as ex:
    print(f"Error durante la conexión: {ex}")

finally:
    connection.close()
    print("\nLa conexión ha finalizado.")



import cx_Oracle

try:
    connection = cx_Oracle.connect(
        user="rentastay",
        password="rentastay_password",
        dsn="oracledb19c_new:1521/ORCLCDB"
    )
    print("Conexión exitosa!")
    connection.close()
except cx_Oracle.Error as error:
    print(f"Error de conexión: {error}")
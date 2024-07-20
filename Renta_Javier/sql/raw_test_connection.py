import oracledb
import sys

try:
    connection = oracledb.connect(
        user='system',
        password='12345',
        dsn='(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracledatabase19c)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=ORCLCDB)))'
    )
    print(f"Conexión exitosa. Versión de Oracle: {connection.version}")
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM COUNTRIES")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except oracledb.DatabaseError as e:
    error, = e.args
    print(f"Error de Oracle: {error.code} - {error.message}")
    if error.code == 12543:
        print("Verifica que el servidor de la base de datos esté en ejecución y accesible.")
    elif error.code == 12541:
        print("Verifica el número de puerto y el nombre del servicio.")
    elif error.code == 12170:
        print("Tiempo de espera de conexión agotado. Verifica la red y la configuración del firewall.")
    sys.exit(1)

except Exception as ex:
    print(f"Error durante la conexión: {ex}")
    print(f"Tipo de excepción: {type(ex).__name__}")
    sys.exit(1)

finally:
    if 'connection' in locals():
        connection.close()
        print("La conexión ha finalizado.")
    else:
        print("La conexión no se estableció.")




# import oracledb

# # Configuración de la conexión
# username = 'system'
# password = '12345'
# dsn = 'localhost:1522/ORCLCDB'  # Ajusta esto según tu configuración






# try:
#     # Intenta establecer la conexión
#     connection = oracledb.connect(
#         user=username,
#         password=password,
#         dsn=dsn,
#         encoding='UTF-8'
#     )
#     print(f"Conexión exitosa. Versión de Oracle: {connection.version}")

#     # Ejecuta una consulta de prueba
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM USERS") 
#     rows = cursor.fetchall()
    
#     print("\nUsuarios en la base de datos:")
#     for row in rows:
#         print(row)

# except oracledb.Error as error:
#     print(f"Error durante la conexión: {error}")
# except Exception as ex:
#     print(f"Error inesperado: {ex}")
# finally:
#     # Cierra la conexión si se estableció
#     if 'connection' in locals():
#         connection.close()
#         print("\nLa conexión ha finalizado.")
import cx_Oracle

try:
    connection = cx_Oracle.connect(
        user="rentastay",
        password="123456",
        dsn="oracledb19c_new:1521/ORCLCDB"
    )
    print("Conexión exitosa!")
    connection.close()
except cx_Oracle.Error as error:
    print(f"Error de conexión: {error}")
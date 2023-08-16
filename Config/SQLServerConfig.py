from SQLServerConnection import sqlserver

# SQL Server Connection
def sql_connection_config():
    sql_connection_string_dict = {
        'driver':   '{ODBC Driver 17 For SQL Server}',
        'server':   'DESKTOP-N2E4KLH',
        'database': 'RequestRegistrationF',
        'username': 'sa',
        'password': '2224616'
    }
    sql_server_connection = sqlserver.database_connection_build(sql_connection_string_dict)
    return sql_server_connection
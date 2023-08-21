import pyodbc


def connection_string_build(connection_dict: dict):
    return f"DRIVER={connection_dict['driver']}; SERVER={connection_dict['server']}; DATABASE={connection_dict['database']}; UID={connection_dict['username']}; PWD={connection_dict['password']};"


def database_connection_build(connection_dict):
    try:
        connection = pyodbc.connect(connection_string_build(connection_dict))
    except Exception as e:
        print(f"connection is unsucceful! \n Your error type: {str(e)}")
    return connection

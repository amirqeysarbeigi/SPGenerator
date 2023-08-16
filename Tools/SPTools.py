from Config import SQLServerConfig


def connection_string_func():
    connection = SQLServerConfig.sql_connection_config()
    return connection


def cursor_func():
    cursor = connection_string_func().cursor()
    return cursor


# TODO: Fix the COL_LENGTH problem for this function
def sp_table_columns_info_raw(sp_config: dict):
    cursor = cursor_func()
    cursor.execute(
        f"""
            SELECT 
                c.name  'Column Name', 
                t.Name  'Data Type',
                COL_LENGTH('{sp_config['schema_name']}.{sp_config['table_name']}', 'c.name'),
                c.is_nullable
            FROM 
                sys.columns as c
            INNER JOIN 
                sys.types as t ON c.user_type_id = t.user_type_id
            WHERE 
                object_id = OBJECT_ID('{sp_config['schema_name']}.{sp_config['table_name']}')
        """)
    table_columns = cursor.fetchall()
    return table_columns


def sp_table_columns_info_fixed(table_columns_raw):
    for record in table_columns_raw:
        if record[3] == True:
            record[3] = "= NULL"
        elif record[3] == False:
            record[3] == ""
        else:
            raise("Incorrect value for boolean type is_nullable")
    return table_columns_raw



# ! Not complete yet, do not use it.
def table_primary_key(sp_config: dict):
    cursor = cursor_func()

    cursor.execute(
        f"""
            SELECT 
                C.COLUMN_NAME
            FROM  
                INFORMATION_SCHEMA.TABLE_CONSTRAINTS T  
                JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE C ON C.CONSTRAINT_NAME=T.CONSTRAINT_NAME  
            WHERE  
                C.TABLE_NAME=[{sp_config['schema_name']}].[{sp_config['table_name']}] and T.CONSTRAINT_TYPE='PRIMARY KEY';
                    """)

    primary_key_table = cursor.fetchall()

    return primary_key_table


def sp_input_declaration_string(table_columns):
    print(table_columns)
    input_declaration_string = ""
    for record in table_columns[:-1]:
        input_declaration_string = input_declaration_string + "@" + \
            str(record[0]) + " " + str(record[1]) + " " + \
            str(record[2]) + " " + str(record[3]) + ", \n"
    input_declaration_string = input_declaration_string + "@" + \
        str(table_columns[-1][0]) + " " + str(table_columns[-1][1]) + " " + \
        str(table_columns[-1][2]) + " " + str(table_columns[-1][3]) + "\n"
    return input_declaration_string


def sp_key_input_declaration_string(sp_config):
    primary_key_table = table_primary_key(sp_config=sp_config)

            

def sp_insert_declaration_string(table_columns):
    insert_declaration_string = "("
    for record in table_columns[:-1]:
        insert_declaration_string = insert_declaration_string + \
            str(record[0]) + ", "
    insert_declaration_string = insert_declaration_string + \
        str(table_columns[-1][0]) + ")"
    return insert_declaration_string


def sp_insert_values_string(table_columns):
    insert_values_string = "("
    for record in table_columns[:-1]:
        insert_values_string = insert_values_string + "@" + str(record[0]) + ", "
    insert_values_string = insert_values_string + \
        "@" + str(table_columns[-1][0]) + ")"
    return insert_values_string


def sp_update_values_string(table_columns_raw):
    update_values_string = ""
    for record in table_columns_raw[:-1]:
        update_values_string = update_values_string + record[0] + " = "
        if (record[3] == True):
            update_values_string = update_values_string + \
                f"ISNULL(@{record[0]}, [{record[0]}])" + ",\n"
        else:
            update_values_string = update_values_string + \
                f"@{record[0]}" + ", \n"
    update_values_string = update_values_string + \
        table_columns_raw[-1][0] + " = "
    if (record[3] == True):
        update_values_string = update_values_string + \
            f"ISNULL(@{table_columns_raw[-1][0]}, [{table_columns_raw[-1][0]}])" + "\n"
    else:
        update_values_string = update_values_string + \
            f"@{table_columns_raw[-1][0]}" + "\n"
    return update_values_string


def sp_conditional_selection_string(sp_info_config):
    primary_key_table = table_primary_key(sp_config=sp_info_config)
    primary_key_string = ""
    i = 0
    for key in primary_key_table[:-1]:
        primary_key_string = primary_key_string + f"AND ([{key}] = @{key}), \n"
    primary_key_string = primary_key_string + \
        f"AND ([{primary_key_table[-1]}] = @{primary_key_table[-1]})"
    return primary_key_string

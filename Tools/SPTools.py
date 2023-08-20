from Config import SQLServerConfig


def connection_string_func():
    connection = SQLServerConfig.sql_connection_config()
    return connection


def cursor_func():
    cursor = connection_string_func().cursor()
    return cursor


def sp_table_columns_info_raw(sp_config: dict):
    cursor = cursor_func()
    cursor.execute(
        f"""
            SELECT 
                c.name  'Column Name', 
                t.Name  'Data Type',
                COL_LENGTH('{sp_config['schema_name']}.{sp_config['table_name']}', c.name),
                c.is_nullable
            FROM 
                sys.columns as c
            INNER JOIN 
                sys.types as t ON c.user_type_id = t.user_type_id
            WHERE 
                object_id = OBJECT_ID('{sp_config['schema_name']}.{sp_config['table_name']}')
        """
    )
    table_columns = cursor.fetchall()
    cursor.close()

    return table_columns


def sp_table_columns_info_fixed(table_columns_raw):
    for record in table_columns_raw:
        if (record[1] == "nvarchar") | (record[1] == "ncahr"):
            record[2] = str(int(record[2]) // 2)

        if str(record[3]) == "True":
            record[3] = "= NULL"
        elif str(record[3]) == "False":
            record[3] = ""
        else:
            raise ("Incorrect value for boolean type is_nullable")
        if (record[1] == "nvarchar") | (record[1] == "ncahr"):
            record[2] = str(int(record[2]) // 2)

        if (
            (record[1] == "char")
            | (record[1] == "nchar")
            | (record[1] == "varchar")
            | (record[1] == "nvarchar")
        ):
            record[2] = "(" + str(record[2]) + ")"
        else:
            record[2] = ""

    return table_columns_raw


def primary_key_table(sp_config: dict):
    cursor = cursor_func()

    cursor.execute(
        f"""
            SELECT	COLUMN_NAME
            FROM	INFORMATION_SCHEMA.KEY_COLUMN_USAGE as C
                    INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS as T ON (C.CONSTRAINT_NAME = T.CONSTRAINT_NAME)
            WHERE	C.TABLE_SCHEMA = '{sp_config['schema_name']}'
                    AND	C.TABLE_NAME = '{sp_config['schema_name']}'
                    AND T.CONSTRAINT_TYPE = 'PRIMARY KEY';
        """
    )

    # #TODO Can be implemented as an alternative faster way to  get the primary key table
    # cursor.execute(
    #     f"""
    #         SELECT	COLUMN_NAME
    #         FROM	INFORMATION_SCHEMA.KEY_COLUMN_USAGE as C
    #         WHERE	C.TABLE_SCHEMA = '{sp_config['schema_name']}'
    #                 AND	C.TABLE_NAME = '{sp_config['table_name']}'
    #                 AND	OBJECTPROPERTY(OBJECT_ID('[{sp_config['schema_name']}].[C.CONSTRAINT_NAME]'), 'IsPrimaryKey') = 1;
    #     """
    # )

    primary_key_table = cursor.fetchall()
    cursor.close()

    return primary_key_table


def sp_input_declaration_string(table_columns):
    print(table_columns)
    input_declaration_string = ""
    for record in table_columns[:-1]:
        input_declaration_string = (
            input_declaration_string
            + "@"
            + str(record[0])
            + " "
            + str(record[1])
            + " "
            + str(record[2])
            + " "
            + str(record[3])
            + ",\n"
        )
    # ?added this part instead to see if it works:
    input_declaration_string = input_declaration_string[:-2]

    # #TODO if it worked correctly without the tree lines below, then erase them.
    # input_declaration_string = input_declaration_string + "@" + \
    #     str(table_columns[-1][0]) + " " + str(table_columns[-1][1]) + " " + \
    #     str(table_columns[-1][2]) + " " + str(table_columns[-1][3]) + "\n"
    return input_declaration_string


def sp_key_input_declaration_string(sp_config):
    table_column_raw = sp_table_columns_info_raw(sp_config=sp_config)
    table_column_fixed = sp_table_columns_info_fixed(table_column_raw)
    key_table = primary_key_table(sp_config=sp_config)

    input_declaration_string = ""

    for record in table_column_fixed:
        for primary_key in key_table:
            if record[0] == primary_key[0]:
                input_declaration_string += (
                    "@" + record[0] + " " + record[1] + record[2] + ",\n"
                )
    input_declaration_string = input_declaration_string[:-2]
    return input_declaration_string


def sp_insert_declaration_string(table_columns):
    insert_declaration_string = "("
    for record in table_columns[:-1]:
        insert_declaration_string = insert_declaration_string + str(record[0]) + ", "
    insert_declaration_string = (
        insert_declaration_string + str(table_columns[-1][0]) + ")"
    )
    return insert_declaration_string


def sp_insert_values_string(table_columns):
    insert_values_string = "("
    for record in table_columns[:-1]:
        insert_values_string = insert_values_string + "@" + str(record[0]) + ", "
    insert_values_string = insert_values_string + "@" + str(table_columns[-1][0]) + ")"
    return insert_values_string


def sp_update_values_string(table_columns_raw):
    update_values_string = ""
    for record in table_columns_raw[:-1]:
        update_values_string = update_values_string + record[0] + " = "
        if record[3] == True:
            update_values_string = (
                update_values_string + f"ISNULL(@{record[0]}, [{record[0]}])" + ",\n"
            )
        else:
            update_values_string = update_values_string + f"@{record[0]}" + ", \n"
    update_values_string = update_values_string + table_columns_raw[-1][0] + " = "
    if record[3] == True:
        update_values_string = (
            update_values_string
            + f"ISNULL(@{table_columns_raw[-1][0]}, [{table_columns_raw[-1][0]}])"
            + "\n"
        )
    else:
        update_values_string = (
            update_values_string + f"@{table_columns_raw[-1][0]}" + "\n"
        )
    return update_values_string


def sp_conditional_selection_string(condition_columns_table: tuple):
    condition = ""
    for key in condition_columns_table[:][0]:
        condition = condition + f"([{str(key)}] = @{str(key)}),\nAND "
    condition = condition[:-6]
    return condition

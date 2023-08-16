from Tools import SPTools

def sp_insert(sp_info_config: dict, sp_name_config: str):
    table_columns_raw = SPTools.sp_table_columns_info_raw(sp_info_config)
    table_columns = SPTools.sp_table_columns_info_fixed(table_columns_raw)
    
    input_declaration_string = SPTools.sp_input_declaration_string(table_columns)


    insert_declaration_string = SPTools.sp_insert_declaration_string(table_columns)



    insert_values_string = SPTools.sp_insert_values_string(table_columns)

    cursor = SPTools.cursor_func()
    cursor.execute(
        f"""  
            CREATE PROCEDURE [{sp_info_config['schema_name']}].[{sp_name_config}_{sp_info_config['table_name']}] (
                {input_declaration_string}
            )
            AS
            BEGIN
                -- SET NOCOUNT ON added to prevent extra result sets from
                -- interfering with SELECT statements.
                SET NOCOUNT ON;

                -- Insert statements for procedure here
                INSERT INTO [{sp_info_config['schema_name']}].[{sp_info_config['table_name']}]
                    {insert_declaration_string}
                VALUES
                    {insert_values_string}
            END
            GO
        """
    )
    
    cursor.close()

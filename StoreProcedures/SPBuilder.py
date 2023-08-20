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


def sp_update(sp_info_config: dict, sp_name_config: str):
    table_columns_raw = SPTools.sp_table_columns_raw(sp_config=sp_info_config)

    table_columns = SPTools.sp_table_columns_info_fixed(
        table_columns_raw=table_columns_raw
    )

    input_declaration_string = SPTools.sp_input_declaration_string(
        table_columns=table_columns
    )

    update_values_string = SPTools.sp_update_values_string(table_columns_raw)

    # ? check to see if the primary key funciton todo is solved
    primary_keys_string = SPTools.sp_conditional_selection_string(
        sp_config=sp_info_config
    )

    cursor = SPTools.cursor_func()

    cursor.execute(
        f"""
            CREATE PROCEDURE [{sp_info_config['schema_name']}].[{sp_name_config}_{sp_info_config['table_name']}](
                {input_declaration_string}
            )
            AS
            BEGIN
                -- SET NOCOUNT ON added to prevent extra result sets from
                -- interfering with SELECT statements.
                SET NOCOUNT ON;
                
                -- insert statements for procedure here
                UPDATE
                    [{sp_info_config['schema_name']}].[{sp_info_config['table_name']}
                SET (
                    {update_values_string}
                )
                    
                WHERE
                    {primary_keys_string};
            END

        """
    )
    cursor.close()


def sp_delete(sp_info_config: dict, sp_name_config: str):
    input_declaration_string = SPTools.sp_key_input_declaration_string(
        sp_config=sp_info_config
    )
    primary_keys = SPTools.primary_key_table(sp_config=sp_info_config)

    condition = SPTools.sp_conditional_selection_string(primary_keys)

    cursor = SPTools.cursor_func()

    cursor.execute(
        f"""
            CREATE PROCEDURE [{sp_info_config['schema_name']}].[{sp_name_config['Delete']}_{sp_info_config['table_name']}](
                {input_declaration_string}
            )
            AS
            BEGIN
                -- SET NOCOUNT ON added to prevent extra result sets from
                -- interfering with SELECT statements.
                SET NOCOUNT ON;
                
                -- insert statements for procedure here
                DELETE FROM [{sp_info_config['schema_name']}].[{sp_info_config['table_name']}]
                WHERE  {condition}
            END
        """
    )

    cursor.close()


def sp_virtual_delete(sp_info_config: dict, sp_name_config: str):
    input_declaration_string = SPTools.sp_key_input_declaration_string(sp_config=sp_info_config)
    primary_keys = SPTools.primary_key_table(sp_config=sp_info_config)
    condition = SPTools.sp_conditional_selection_string(primary_keys)

    cursor = SPTools.cursor_func()

    cursor.execute(
        f"""
            CREATE PROCEDURE [{sp_info_config['schema_name']}].[{sp_name_config['VirtualDelete']}_{sp_info_config['table_name']}](
                {input_declaration_string}
            )
            AS
            BEGIN
                -- SET NOCOUNT ON added to prevent extra result sets from
                -- interfering with SELECT statements.
                SET NOCOUNT ON;
                
                -- insert statements for procedure here
                UPDATE 
                    [{sp_info_config['schema_name']}].[{sp_info_config['table_name']}]
                SET 
                    [status] = 0 
                WHERE 
                    {condition}
            END
        """
    )

    cursor.close()
    
    # * Second way to do it is to call the sp_update for this table
    # input_for_sp_update = None
    # cursor.execute(
    #     f"""
    #         CREATE PROCEDURE [{sp_info_config['schema_name']}].[{sp_name_config['VirtualDelete']}_{sp_info_config['table_name']}](
    #             {input_declaration_string}
    #         )
    #         AS
    #         BEGIN
    #             -- SET NOCOUNT ON added to prevent extra result sets from
    #             -- interfering with SELECT statements.
    #             SET NOCOUNT ON;
                
    #             -- insert statements for procedure here
    #             [{sp_info_config['schema_name']}].[{sp_name_config['Update']}_{sp_info_config['table_name']}] {input_for_sp_update}
    #         END
    #     """
    # )

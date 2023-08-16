from Tools import SPTools
from Config import SPConfig

# SPInsert.test()


# * checking input for the set clause of the update operation
# sp_config = {
#     'database_name': 'RequestRejectionF',
#     'schema_name': 'merchant',
#     'table_name': 'Merchant'
# }

# table_columns_raw = SPTools.sp_table_columns_info_raw(sp_config=sp_config)
# output = SPTools.sp_update_values_string(table_columns_raw=table_columns_raw)

# print(output)


# * checking to see why does my qeury has problem retrieving the primary keys of a table
# cursor = SPTools.cursor_func()

# cursor.execute(
#     f"""
#         SELECT
#             COLUMN_NAME
#         FROM
#             INFORMATION_SCHEMA.COLUMNS
#         WHERE
#             TABLE_NAME = 'Merchant'
#             AND COLUMN_NAME IN (
#                 SELECT
#                     COLUMN_NAME
#                 FROM
#                     INFORMATION_SCHEMA.KEY_COLUMN_USAGE
#                 WHERE
#                     OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_NAME), 'IsPrimaryKey') = 1
#                     AND TABLE_NAME = 'Merchant')
#     """)
# primaryKey = cursor.fetchall()

# print(primaryKey)

# cursor.close()


# * my problem with the sql built-in functions
#
# SELECT	OBJECT_ID(C.CONSTRAINT_NAME)
# FROM	INFORMATION_SCHEMA.KEY_COLUMN_USAGE as C
# WHERE	C.TABLE_SCHEMA = 'merchant'
# 		AND	C.TABLE_NAME = 'Merchant'
# 		AND	C.CONSTRAINT_NAME = 'PK_Merchant';

# SELECT	CONSTRAINT_NAME
# FROM	INFORMATION_SCHEMA.KEY_COLUMN_USAGE

# SELECT	C.COLUMN_NAME
# FROM	INFORMATION_SCHEMA.KEY_COLUMN_USAGE as C
# WHERE	C.TABLE_SCHEMA = 'merchant'
# 		AND	C.TABLE_NAME = 'Merchant'
# 		AND	C.CONSTRAINT_NAME = 'PK_Merchant';

# # * Examining the whole update Sp input to the sql language by cursor.execute()
# # * It worked perfectly fine.
# sp_info_config = SPConfig.sp_info_config
# sp_name_config = SPConfig.sp_name_config

# table_columns_raw = SPTools.sp_table_columns_info_raw(sp_info_config)

# input_declaration_string = SPTools.sp_input_declaration_string(
#     table_columns_raw)

# update_values_string = SPTools.sp_update_values_string(table_columns_raw)
# primary_key_string = 'salam'
# print(
#     f"""
#             CREATE PROCEDURE [{sp_info_config['schema_name']}].[{sp_name_config['Update']}_{sp_info_config['table_name']}](
#                 {input_declaration_string}
#             )
#             AS
#             BEGIN
#                 -- SET NOCOUNT ON added to prevent extra result sets from
#                 -- interfering with SELECT statements.
#                 SET NOCOUNT ON;
                
#                 -- insert statements for procedure here
#                 UPDATE
#                     [{sp_info_config['schema_name']}].[{sp_info_config['table_name']}]
#                 SET (
#                     {update_values_string}
#                 )
#                 WHERE
#                     {primary_key_string};
#             END

#         """)

print("hello love")
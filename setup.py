from StoreProcedures import SPBuilder as sp
from Config import SPConfig

sp.sp_insert(sp_info_config=SPConfig.sp_info_config, sp_name_config=SPConfig.sp_name_config['Insert'])

sp.sp_update(sp_info_config=SPConfig.sp_info_config, sp_name_config=SPConfig.sp_name_config['Update'])

sp.sp_delete(sp_info_config=SPConfig.sp_info_config, sp_name_config=SPConfig.sp_name_config['Delete'])

sp.sp_virtual_delete(sp_info_config=SPConfig.sp_info_config, sp_name_config=SPConfig.sp_name_config['VirtualDelete'])

sp.sp_loadList(sp_info_config=SPConfig.sp_info_config, sp_name_config=SPConfig.sp_name_config['LoadList'])

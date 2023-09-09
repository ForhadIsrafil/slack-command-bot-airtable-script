import json
import os, sys
from pyairtable import Table, Api, Base

# MAKE CONNECT WITH AIRTABLE BASE AND TABLE START
# Table ID: tblL234oK0HIl3Z04
api_key = ''
base_id = 'ap'
table_name = 'Test Dev'
token = 'patl83a2AzFDoiIal.83b5e4ee6dfbd4ba92e74c8e56b09752'

table = Table(api_key=api_key, base_id=base_id, table_name=table_name)
print(table.all())
# MAKE CONNECT WITH AIRTABLE BASE AND TABLE END

# try:
#
#     data_list = []
#     for data in json_data:
#         # print(data)
#         dict_data = {
#             "noticeId": data["noticeId"],
#         }
#
#         data_list.append(dict_data)
#     # table.batch_create(data_list)
#
#     print(".......Done.......")
# except Exception as e:
#     print(e.__str__())

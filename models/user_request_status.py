from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


STATUS_MAPPING = {"Схвалено": 1, "Відхилено": 2, "Розглядається": 3, "Скасовано": 4}


user_request_status = Table('user_request_status', metadata_obj,
          Column('user_request_status_id', Integer, primary_key=True),
          Column('user_request_status_name', VARCHAR(50)))

from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


STATUS_MAPPING = {"Схвалено": 1, "Відхилено": 2, "Розглядається": 3, "Скасовано": 4}


status = Table('status', metadata_obj,
          Column('status_id', Integer, primary_key=True),
          Column('status_name', VARCHAR(50)))

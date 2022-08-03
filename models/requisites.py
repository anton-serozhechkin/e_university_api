from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey)


metadata_obj = MetaData()

requisites = Table('requisites', metadata_obj,
          Column('iban', VARCHAR(100)),
          Column('university_id', Integer, ForeignKey("university.university_id")),
          Column('organisation_code', VARCHAR(50)),
          Column('service_id', Integer, ForeignKey("service.service_id")),
          Column('payment_recognation', VARCHAR(255)))

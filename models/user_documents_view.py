from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, DateTime)


metadata_obj = MetaData()


user_documents_view = Table('user_documents_view', metadata_obj,
          Column('user_document_id', Integer),
          Column('university_id', Integer),
          Column('user_id', Integer),
          Column('name', VARCHAR(255)),
          Column('content', VARCHAR(255)),
          Column('date_created', DateTime))
      
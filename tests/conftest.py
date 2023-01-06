import pytest
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv(".quartenv")


from application import create_app
from db import tags_metadata

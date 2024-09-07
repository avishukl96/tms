from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError

try:
    #engine = create_engine("mysql+mysqlconnector://mhmloacal:mfduLqe7ApS5LwXw@164.52.203.32:3306/tms")
    #engine = create_engine("mysql+pymysql://admin:OpenMhm@2024@216.48.182.31:3306/tms")
    engine = create_engine("mysql+pymysql://root:@localhost:3306/tms")
    meta = MetaData()
    conn = engine.connect()
    print("Connection successful!")
except SQLAlchemyError as e:
    print(f"An error occurred: {e}")    
    
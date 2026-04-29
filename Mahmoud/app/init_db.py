from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

print("Tables created successfully")

print("Tables:")
for table in Base.metadata.tables.keys():
    print(table)
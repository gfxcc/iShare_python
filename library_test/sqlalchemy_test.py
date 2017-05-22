import sqlalchemy

# This engine just used to query for list of databases
engine = sqlalchemy.create_engine('mysql://root:19920406Cy@localhost:3306')
ret = engine.execute('show databases;')
for row in ret:
    print row

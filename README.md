# Data Modeling with Postgres
Project from Udacity's Data Engineer Nano Degree. ETL pipeline to ingest songs and user activity data.

# Setup
Project is using python 3. Install dependencies:
```
pip install -r requirements.txt
```

Postgres database is assumed to connect with these configs:
```
host=127.0.0.1
dbname=studentdb
user=student
password=student
```

# Run Project
```
python3 create_tables.py
python3 etl.py
```

# Project Structure

| Folder / File    | Description                                                       |
|------------------|-------------------------------------------------------------------|
| data folder      | Contains songs and user activity data.                            |
| sql_queries.py   | Sql commands.                                                     |
| create_tables.py | Creates songplay, app_user, song, artist and time tables.         |
| etl.py           | Process the files in data folder and stores the data in database. |
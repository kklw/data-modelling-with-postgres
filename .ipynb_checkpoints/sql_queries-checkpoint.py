# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS app_user"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay(
                            songplay_id SERIAL PRIMARY KEY,
                            start_time timestamp,
                            user_id int NOT NULL,
                            level varchar,
                            artist_id varchar,
                            song_id varchar,
                            session_id int,
                            location text,
                            user_agent text)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS app_user(
                        user_id int NOT NULL,
                        first_name varchar NOT NULL,
                        last_name varchar NOT NULL,
                        gender char,
                        level varchar,
                        PRIMARY KEY (user_id))
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song(
                        song_id varchar NOT NULL,
                        title varchar,
                        artist_id varchar,
                        year int,
                        duration float,
                        PRIMARY KEY (song_id))
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artist(
                        artist_id varchar NOT NULL,
                        name varchar,
                        location varchar,
                        lattitude numeric,
                        longitude numeric,
                        PRIMARY KEY (artist_id))
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
                        start_time timestamp NOT NULL,
                        hour int,
                        day int,
                        week int,
                        month int,
                        year int,
                        weekday varchar,
                        PRIMARY KEY (start_time))
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplay(start_time, user_id,level,artist_id,song_id, session_id, location, user_agent)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO app_user(user_id, first_name, last_name, gender, level)
                        VALUES(%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) 
                        DO UPDATE SET level = excluded.level
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id,year,duration)
                        VALUES(%s, %s, %s, %s, %s)
                        ON CONFLICT (song_id) 
                        DO NOTHING"
""")

artist_table_insert = ("""
INSERT INTO  artist(artist_id, name, location, lattitude, longitude)
                          VALUES(%s, %s, %s, %s, %s)
                          ON CONFLICT (artist_id) 
                          DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year,weekday)
                        VALUES(%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (start_time) 
                        DO NOTHING
""")

# FIND SONGS

song_select = ("""
SELECT songs.song_id, artists.artist_id FROM songs 
                  JOIN artists ON  songs.artist_id=artists.artist_id
                  WHERE songs.title=%s AND artists.name=%s AND songs.duration=%s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
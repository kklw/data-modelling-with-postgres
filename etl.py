import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import datetime


def process_song_file(cur, filepath):
    """
    Processes song data and maps it to song and artist.

    Parameters:
    - cur: cursor variable
    - filepath: file path to the song file
    """
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[
        0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Processes log data and maps it to user, time and songplay.

    Parameters:
    - cur: cursor variable
    - filepath: file path to the song file
    """
    df = pd.read_json(filepath, lines=True)
    df = df[df['page'] == "NextSong"].reset_index()

    # convert timestamp column to datetime
    start_time = pd.to_datetime(df.ts, unit='ms')

    # insert time data records
    df['start_time'] = start_time
    df['week'] = start_time.apply(lambda x: datetime.date(x.year, x.month, x.day).isocalendar()[1])
    df['week_day'] = start_time.apply(lambda x: datetime.date(x.year, x.month, x.day).strftime("%A"))
    time_data = (
    start_time, start_time.dt.hour, start_time.dt.day, df.week, start_time.dt.month, start_time.dt.year, df.week_day)
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for _, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for _, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for _, row in df.iterrows():
        # get song id and artist id from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = (
            str(row.start_time), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Retrieves files and run processing.

    Parameters:
    - cur: database cursor
    - conn: database connection
    - filepath: file path for files to be processed
    - func: processing function
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    ETL pipeline to process songs and logs.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()

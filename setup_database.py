import sqlite3

conn=sqlite3.connect('better_spotify.db')
cursor=conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL   
            )
               ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
            ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
               
            )''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_songs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_id INTEGER NOT NULL,
                song_id INTEGER NOT NULL,
                FOREIGN KEY(playlist_id) REFERENCES playlists(id),
                FOREIGN KEY(song_id) REFERENCES songs(id)
               
            )''')

cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS favourite_songs(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    song_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(song_id) REFERENCES songs(id)
                )''')

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
if tables:
    print("Utworzone tabele:", tables)
else:
    print("Brak tabel w bazie danych")



print("Database setup done")
try:
    cursor.execute('''
        ALTER TABLE songs ADD COLUMN last_played DATETIME
    ''')
except sqlite3.OperationalError as e:
    print("Kolumna 'last_played' już istnieje lub wystąpił błąd:", e)

conn.commit()
conn.close()
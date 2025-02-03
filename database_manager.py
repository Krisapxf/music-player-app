import sqlite3
import os

class DatabaseManager:
    def __init__(self, database_filename="better_spotify.db"):
        self.db_path = database_filename
    
    def _connect(self):
        return sqlite3.connect(self.db_path)
    

    def add_user(self, username,email, password):
        conn=self._connect()
        cursor=conn.cursor()
        try:
            cursor.execute("INSERT INTO users(username, email, password) VALUES(?,?,?)",( username, email, password))
            conn.commit()
            print("User added")
        except sqlite3.IntegrityError:
            print("User already exists")
        finally:
            conn.close()

    def get_user(self, email, password):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user=cursor.fetchone()
        conn.close()
        return user
    def get_user_by_email(self, email): 
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user=cursor.fetchone()
        conn.close()
        return user
    
    def add_song(self, title, artist, file_path):
        if not os.path.exists(file_path):
            raise Exception("File does not exist")
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO songs(title, artist, file_path) VALUES(?,?,?)",(title, artist, file_path))
        conn.commit()
        conn.close()

    def get_all_songs(self):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM songs")
        songs=cursor.fetchall()
        conn.close()
        return songs
    
    def get_song(self, song_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM songs WHERE id=?", (song_id,))
        song=cursor.fetchone()
        conn.close()
        if song:
            return song[0]
        else:
            raise Exception("Song not found")

    
    def get_song_by_title_artist(self, title, artist):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM songs WHERE title=? AND artist=?", (title, artist))
        song=cursor.fetchone()
        conn.close()
        return song
    
    def add_favourite_song(self, user_id, song_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO favourite_songs(user_id, song_id) VALUES(?,?)",(user_id, song_id))
        conn.commit()
        conn.close()

    def remove_favourite_song(self, user_id, song_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM favourite_songs WHERE user_id=? AND song_id=?",(user_id, song_id))
        conn.commit()
        conn.close()

    def get_favourite_songs(self, user_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM favourite_songs WHERE user_id=?", (user_id,))
        favourite_songs=cursor.fetchall()
        conn.close()
        return favourite_songs
    
    def create_playlist(self, title, user_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO playlists(title, user_id) VALUES(?,?)",(title, user_id))
        conn.commit()
        conn.close()

    def add_song_to_playlist(self, playlist_id, song_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO playlist_songs(playlist_id, song_id) VALUES(?,?)",(playlist_id, song_id))
        conn.commit()
        conn.close()

    def remove_song_from_playlist(self, playlist_id, song_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM playlist_songs WHERE playlist_id=? AND song_id=?",(playlist_id, song_id))
        conn.commit()
        conn.close()

    def get_playlist(self, user_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM playlists WHERE user_id=?", (user_id,))
        playlists=cursor.fetchall()
        conn.close()
        return playlists
    
    def get_playlist_info_by_id(self, playlist_id):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM playlists WHERE id=?", (playlist_id,))
        playlist=cursor.fetchone()
        conn.close()
        return playlist
    
    def get_playlist_songs(self, playlist_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ps.id, ps.playlist_id, s.title
            FROM playlist_songs ps
            JOIN songs s ON ps.song_id = s.id
            WHERE ps.playlist_id = ?
        """, (playlist_id,))
        songs = cursor.fetchall()
        conn.close()
        return songs
    
    
    def update_playback_history(self, song_id):
        from datetime import datetime
        conn=self._connect()
        cursor=conn.cursor()
        last_played=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE songs SET last_played=? WHERE id=?", (last_played, song_id))
        conn.commit()
        conn.close()

    def search_songs(self, text):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM songs WHERE title LIKE ? OR artist LIKE ?", (f"%{text}%", f"%{text}%"))
        songs=cursor.fetchall()
        conn.close()
        return songs
    
    def update_user(self, username, email, password):
        conn=self._connect()
        cursor=conn.cursor()
        cursor.execute("UPDATE users SET username=?, password=? WHERE email=?", (username,password ,email))
        conn.commit()
        conn.close()
    



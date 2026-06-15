# Loretta Liu - Music Charts Database Application
import sqlite3
import os

# Constants and Variables
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, "music_charts.db")


def check_table_exists():
    """Check if the Songs table exists"""
    try:
        conn = sqlite3.connect(DATABASE)  
        
        cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name='Songs';
        """)
        
        table = cursor.fetchone()
        conn.close()
        return table is not None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def display_all_music():
    """Display all music records with artist and album info"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT Artists.ArtistName, Songs.SongName, 
               IFNULL(Albums.AlbumName, 'No Album') as AlbumName,
               Songs.StreamsMillions, Songs.SongLength, Songs.ChartRanking
        FROM Songs
        JOIN Artists ON Songs.ArtistID = Artists.ArtistID
        LEFT JOIN Albums ON Songs.AlbumID = Albums.AlbumID
        ORDER BY Songs.ChartRanking
        """)
        
        results = cursor.fetchall()
        
        print("\n" + "=" * 100)
        print("ALL MUSIC RECORDS")
        print("=" * 100)
        print(f"{'Artist':<25} {'Song':<30} {'Album':<20} {'Streams':<10} {'Length':<10} {'Rank':<5}")
        print("-" * 100)
        
        for song in results:
            artist = song[0][:24] if song[0] else "N/A"
            song_name = song[1][:29] if song[1] else "N/A"
            album = song[2][:19] if song[2] else "N/A"
            streams = f"{song[3]}M" if song[3] else "N/A"
            length = song[4] if song[4] else "N/A"
            rank = song[5] if song[5] else "N/A"
            
            print(f"{artist:<25} {song_name:<30} {album:<20} {streams:<10} {length:<10} {rank:<5}")
        
        print("=" * 100)
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def display_top_rankings():
    """Display top 5 ranked songs"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT Artists.ArtistName, Songs.SongName, Songs.ChartRanking
        FROM Songs
        JOIN Artists ON Songs.ArtistID = Artists.ArtistID
        WHERE Songs.ChartRanking IS NOT NULL
        ORDER BY Songs.ChartRanking ASC
        LIMIT 5
        """)
        
        results = cursor.fetchall()
        
        print("\n" + "=" * 50)
        print("TOP 5 CHART RANKINGS")
        print("=" * 50)
        
        for i, row in enumerate(results, 1):
            print(f"{i}. {row[0]} - \"{row[1]}\" (Rank #{row[2]})")
        
        print("=" * 50)
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def display_most_streamed():
    """Display top 3 most streamed songs"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT Artists.ArtistName, Songs.SongName, Songs.StreamsMillions
        FROM Songs
        JOIN Artists ON Songs.ArtistID = Artists.ArtistID
        WHERE Songs.StreamsMillions IS NOT NULL
        ORDER BY Songs.StreamsMillions DESC
        LIMIT 3
        """)
        
        results = cursor.fetchall()
        
        print("\n" + "=" * 50)
        print("MOST STREAMED SONGS")
        print("=" * 50)
        
        for i, row in enumerate(results, 1):
            print(f"{i}. {row[0]} - \"{row[1]}\" ({row[2]} million streams)")
        
        print("=" * 50)
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def search_artist():
    """Search for an artist by name"""
    artist = input("\nEnter artist name: ").strip()
    
    if not artist:
        print("Please enter an artist name.")
        return
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT Artists.ArtistName, Songs.SongName, Songs.ChartRanking, 
               Songs.StreamsMillions, IFNULL(Albums.AlbumName, 'No Album')
        FROM Songs
        JOIN Artists ON Songs.ArtistID = Artists.ArtistID
        LEFT JOIN Albums ON Songs.AlbumID = Albums.AlbumID
        WHERE Artists.ArtistName LIKE ?
        ORDER BY Songs.ChartRanking
        """, (f'%{artist}%',))
        
        results = cursor.fetchall()
        
        if len(results) == 0:
            print(f"\nNo artist found matching '{artist}'")
        else:
            print(f"\n{'=' * 70}")
            print(f"Found {len(results)} song(s) by {results[0][0]}:")
            print(f"{'=' * 70}")
            
            for row in results:
                print(f"  - {row[1]}")
                print(f"    Rank: #{row[2]} | Streams: {row[3]}M | Album: {row[4]}")
                print()
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def add_sample_data():
    """Add sample data to the database if it's empty"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check if Songs table is empty
        cursor.execute("SELECT COUNT(*) FROM Songs")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("\nAdding sample data to database...")
            
            # Add sample artists
            cursor.execute("INSERT OR IGNORE INTO Artists (ArtistID, ArtistName) VALUES (1, 'Taylor Swift')")
            cursor.execute("INSERT OR IGNORE INTO Artists (ArtistID, ArtistName) VALUES (2, 'The Weeknd')")
            cursor.execute("INSERT OR IGNORE INTO Artists (ArtistID, ArtistName) VALUES (3, 'Olivia Rodrigo')")
            cursor.execute("INSERT OR IGNORE INTO Artists (ArtistID, ArtistName) VALUES (4, 'Drake')")
            cursor.execute("INSERT OR IGNORE INTO Artists (ArtistID, ArtistName) VALUES (5, 'Billie Eilish')")
            
            # Add sample albums
            cursor.execute("INSERT OR IGNORE INTO Albums (AlbumID, AlbumName, ArtistID) VALUES (1, 'Midnights', 1)")
            cursor.execute("INSERT OR IGNORE INTO Albums (AlbumID, AlbumName, ArtistID) VALUES (2, 'After Hours', 2)")
            cursor.execute("INSERT OR IGNORE INTO Albums (AlbumID, AlbumName, ArtistID) VALUES (3, 'Sour', 3)")
            cursor.execute("INSERT OR IGNORE INTO Albums (AlbumID, AlbumName, ArtistID) VALUES (4, 'Certified Lover Boy', 4)")
            cursor.execute("INSERT OR IGNORE INTO Albums (AlbumID, AlbumName, ArtistID) VALUES (5, 'Happier Than Ever', 5)")
            
            # Add sample songs
            cursor.execute("INSERT OR IGNORE INTO Songs (SongID, SongName, StreamsMillions, SongLength, ChartRanking, ArtistID, AlbumID) VALUES (1, 'Anti-Hero', 850, '3:20', 1, 1, 1)")
            cursor.execute("INSERT OR IGNORE INTO Songs (SongID, SongName, StreamsMillions, SongLength, ChartRanking, ArtistID, AlbumID) VALUES (2, 'Blinding Lights', 1200, '3:30', 2, 2, 2)")
            cursor.execute("INSERT OR IGNORE INTO Songs (SongID, SongName, StreamsMillions, SongLength, ChartRanking, ArtistID, AlbumID) VALUES (3, 'drivers license', 950, '4:02', 3, 3, 3)")
            cursor.execute("INSERT OR IGNORE INTO Songs (SongID, SongName, StreamsMillions, SongLength, ChartRanking, ArtistID, AlbumID) VALUES (4, 'Way 2 Sexy', 600, '4:17', 4, 4, 4)")
            cursor.execute("INSERT OR IGNORE INTO Songs (SongID, SongName, StreamsMillions, SongLength, ChartRanking, ArtistID, AlbumID) VALUES (5, 'Happier Than Ever', 700, '4:58', 5, 5, 5)")
            
            conn.commit()
            print("Sample data added successfully!")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Error adding sample data: {e}")


# Main Program
def main():
    """Main program loop"""
    print("\n" + "=" * 50)
    print("WELCOME TO MUSIC CHARTS DATABASE")
    print("=" * 50)
    
    # Check if database exists and has the Songs table
    if not check_table_exists():
        print(f"\nERROR: The database '{DATABASE}' does not exist or doesn't have the 'Songs' table.")
        print("\nPlease make sure:")
        print("1. music_charts.db is in the same folder as this script")
        print("2. The database has the Artists, Albums, and Songs tables")
        print("\nRun SQLiteStudio to check your database setup.")
        return
    
    # Add sample data if database is empty
    add_sample_data()
    
    # Main menu loop
    while True:
        print("\n" + "-" * 50)
        print("MUSIC CHARTS DATABASE MENU")
        print("-" * 50)
        print("1. Display all music")
        print("2. Display top 5 rankings")
        print("3. Display most streamed songs")
        print("4. Search for an artist")
        print("5. Exit")
        print("-" * 50)
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            display_all_music()
        elif choice == "2":
            display_top_rankings()
        elif choice == "3":
            display_most_streamed()
        elif choice == "4":
            search_artist()
        elif choice == "5":
            print("\n" + "=" * 50)
            print("Thank you for using Music Charts Database!")
            print("Goodbye!")
            print("=" * 50)
            break
        else:
            print("\nInvalid option. Please choose 1, 2, 3, 4, or 5.")


# Run the program
if __name__ == "__main__":
    main()
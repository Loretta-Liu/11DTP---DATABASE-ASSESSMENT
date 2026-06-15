# Loretta Liu - Music Charts Database Application
import sqlite3
import os

DATABASE = "music.db"

def setup_database():
    """Create database and add sample data if needed"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS music (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist_name TEXT NOT NULL,
        song_name TEXT NOT NULL,
        album TEXT,
        song_streams INTEGER,
        song_length TEXT,
        chart_ranking INTEGER
    )
    """)
    
    # Check if table is empty
    cursor.execute("SELECT COUNT(*) FROM music")
    count = cursor.fetchone()[0]
    
    # Add sample data if empty
    if count == 0:
        sample_data = [
            ('Taylor Swift', 'Anti-Hero', 'Midnights', 850, '3:20', 1),
            ('The Weeknd', 'Blinding Lights', 'After Hours', 1200, '3:30', 2),
            ('Olivia Rodrigo', 'drivers license', 'Sour', 950, '4:02', 3),
            ('Drake', 'Way 2 Sexy', 'Certified Lover Boy', 600, '4:17', 4),
            ('Billie Eilish', 'Happier Than Ever', 'Happier Than Ever', 700, '4:58', 5),
        ]
        cursor.executemany("""
        INSERT INTO music (artist_name, song_name, album, song_streams, song_length, chart_ranking)
        VALUES (?, ?, ?, ?, ?, ?)
        """, sample_data)
        conn.commit()
    
    conn.close()

def check_table_exists():
    """Check if the music table exists"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='music'")
    table = cursor.fetchone()
    conn.close()
    return table is not None

def display_all_music():
    """Display all music records"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    results = cursor.fetchall()
    
    print("\n" + "=" * 70)
    print("ALL MUSIC RECORDS")
    print("=" * 70)
    
    for music in results:
        print(f"ID: {music[0]}")
        print(f"Artist: {music[1]}")
        print(f"Song: {music[2]}")
        print(f"Album: {music[3]}")
        print(f"Streams: {music[4]} million")
        print(f"Length: {music[5]}")
        print(f"Rank: #{music[6]}")
        print("-" * 70)
    
    conn.close()

def display_top_rankings():
    """Display top 5 ranked songs"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT artist_name, song_name, chart_ranking
    FROM music
    ORDER BY chart_ranking ASC
    LIMIT 5
    """)
    
    results = cursor.fetchall()
    
    print("\n" + "=" * 40)
    print("TOP 5 CHART RANKINGS")
    print("=" * 40)
    
    for row in results:
        print(f"#{row[2]} - {row[0]} - {row[1]}")
    
    conn.close()

def display_most_streamed():
    """Display top 3 streamed songs"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT artist_name, song_name, song_streams
    FROM music
    ORDER BY song_streams DESC
    LIMIT 3
    """)
    
    results = cursor.fetchall()
    
    print("\n" + "=" * 40)
    print("MOST STREAMED SONGS")
    print("=" * 40)
    
    for row in results:
        print(f"{row[0]} - {row[1]} ({row[2]} million streams)")
    
    conn.close()

def search_artist():
    """Search for an artist"""
    artist = input("\nEnter artist name: ")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT artist_name, song_name, chart_ranking, song_streams
    FROM music
    WHERE artist_name LIKE ?
    """, (f'%{artist}%',))
    
    results = cursor.fetchall()
    
    if len(results) == 0:
        print(f"\nNo artist found matching '{artist}'")
    else:
        print(f"\nFound {len(results)} song(s):")
        for row in results:
            print(f"  • {row[0]} - {row[1]} (Rank #{row[2]}, {row[3]}M streams)")
    
    conn.close()

# ============ MAIN PROGRAM ============
print("\n" + "=" * 50)
print("WELCOME TO MUSIC CHARTS DATABASE")
print("=" * 50)

# Setup database first
setup_database()

# Check if table exists
if not check_table_exists():
    print("ERROR: Could not create or find the music table")
else:
    # Main menu loop
    while True:
        print("\n" + "-" * 30)
        print("MUSIC CHARTS MENU")
        print("-" * 30)
        print("1. Display all music")
        print("2. Display top 5 rankings")
        print("3. Display most streamed songs")
        print("4. Search for artist")
        print("5. Exit")
        print("-" * 30)
        
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            display_all_music()
        elif choice == "2":
            display_top_rankings()
        elif choice == "3":
            display_most_streamed()
        elif choice == "4":
            search_artist()
        elif choice == "5":
            print("\nThank you for using Music Charts Database!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid option. Please choose 1, 2, 3, 4, or 5.")

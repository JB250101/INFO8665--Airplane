import sqlite3
import pandas as pd

# Define correct database path for airfare data
DB_PATH = "data/airfare_data.db"  # Changed from animal_shelter.db
DATA_FILE = "data/Data_Train.xlsx"  # Correct dataset file

def load_data():
    """Load airfare data from the Excel file."""
    try:
        df = pd.read_excel(DATA_FILE)
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def create_airfare_table():
    """Create the airfare price table in SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create airfare data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Airfare_Prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Airline TEXT,
            Source TEXT,
            Destination TEXT,
            Date_of_Journey TEXT,
            Duration REAL,
            Price REAL
        )
    """)

    conn.commit()
    conn.close()

def insert_airfare_record(Airline, Source, Destination, Date_of_Journey, Duration, Price):
    """Insert an airfare record into the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Airfare_Prices (Airline, Source, Destination, Date_of_Journey, Duration, Price) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (Airline, Source, Destination, Date_of_Journey, Duration, Price))

    conn.commit()
    conn.close()

def fetch_all_airfare_records():
    """Retrieve all airfare records from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("✅ Querying Airfare_Prices table...")  # Debugging Log
    cursor.execute("SELECT * FROM Airfare_Prices")
    records = cursor.fetchall()
    conn.close()

    return records

# Run once to ensure the table exists
create_airfare_table()

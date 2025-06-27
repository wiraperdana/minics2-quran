import os
import json
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv(override=True)

# Get database connection string from environment variables
connection_string = os.getenv('SUPABASE_CONNECTION_STRING')

# Create Flask application
app = Flask(__name__)
CORS(app)

# Function to get all verses from Surah Maryam (Surah ID 19)
def get_surah_maryam_verses():
    try:
        # Connect to the database
        conn = psycopg2.connect(connection_string)
        
        # Create a cursor with dictionary-like results
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Execute query to get all verses from Surah Maryam
        cursor.execute("""
            SELECT * FROM quranidn 
            WHERE surah_id = 19 
            ORDER BY verse_id ASC
        """)
        
        # Fetch all results
        verses = cursor.fetchall()
        
        # Convert results to list of dictionaries
        result = [dict(verse) for verse in verses]
        
        # Close cursor and connection
        cursor.close()
        conn.close()
        
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

# API endpoint to get Surah Maryam verses
@app.route('/api/quran/maryam', methods=['POST'])
def surah_maryam():
    # Get all verses from Surah Maryam
    verses = get_surah_maryam_verses()
    
    # Return as JSON response
    return jsonify({
        "surah": "Maryam",
        "surah_id": 19,
        "verses": verses
    })

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
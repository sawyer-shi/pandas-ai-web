import os
import sqlite3
import uuid
from datetime import datetime

class DatabaseManager:
    """Manages database operations for chat history and session storage."""
    
    def __init__(self, db_path="chat_history.db"):
        """Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database schema if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create chat history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            session_file TEXT,
            timestamp TEXT,
            question_id TEXT,
            question TEXT,
            answer TEXT,
            model TEXT,
            model_name TEXT
        )
        ''')
        
        # Create sessions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            session_file TEXT,
            timestamp TEXT,
            client_id TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_chat(self, session_id, session_file, client_id, question, answer, model_type, model_name):
        """Save a chat entry to the database.
        
        Args:
            session_id: The session ID
            session_file: The session file name
            client_id: The client ID
            question: The user's question
            answer: The AI's answer
            model_type: The model type (e.g., "OpenAI", "Azure", "Ollama")
            model_name: The specific model name
            
        Returns:
            str: The ID of the created chat entry
        """
        if not question or not answer:
            return None
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        chat_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute(
            """INSERT INTO chat_history 
            (id, session_id, session_file, timestamp, question_id, question, answer, model, model_name) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (chat_id, session_id, session_file, timestamp, client_id, question, answer, model_type, model_name)
        )
        
        conn.commit()
        conn.close()
        
        return chat_id
    
    def create_session(self, client_id, file_name=None):
        """Create a new session.
        
        Args:
            client_id: The client ID
            file_name: Optional base file name for the session
            
        Returns:
            tuple: (session_id, session_file)
        """
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Generate a session file name if not provided
        if not file_name:
            session_file = f"session_{timestamp}"
        else:
            file_basename = os.path.basename(file_name)
            session_file = f"{file_basename}_{timestamp}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO sessions (session_id, session_file, timestamp, client_id) VALUES (?, ?, ?, ?)",
            (
                session_id, 
                session_file, 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                client_id
            )
        )
        
        conn.commit()
        conn.close()
        
        return session_id, session_file
    
    def get_sessions(self, client_id=None):
        """Get sessions for a client.
        
        Args:
            client_id: Optional client ID to filter sessions
            
        Returns:
            list: Session records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if client_id:
            cursor.execute(
                "SELECT session_id, session_file, timestamp FROM sessions WHERE client_id=? ORDER BY timestamp DESC",
                (client_id,)
            )
        else:
            cursor.execute(
                "SELECT session_id, session_file, timestamp FROM sessions ORDER BY timestamp DESC"
            )
            
        sessions = cursor.fetchall()
        conn.close()
        
        return [
            {
                "session_id": s[0], 
                "session_file": s[1], 
                "timestamp": s[2]
            } 
            for s in sessions
        ]
    
    def get_chat_history(self, session_id):
        """Get chat history for a session.
        
        Args:
            session_id: The session ID
            
        Returns:
            list: Chat history records
        """
        # Handle session_id as dict with "value" key (from Gradio)
        if isinstance(session_id, dict) and "value" in session_id:
            session_id = session_id["value"]
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, timestamp, question, answer, model, model_name FROM chat_history WHERE session_id=? ORDER BY timestamp ASC",
            (session_id,)
        )
        history = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": h[0],
                "timestamp": h[1],
                "question": h[2],
                "answer": h[3],
                "model": h[4],
                "model_name": h[5]
            } 
            for h in history
        ]
    
    def get_session_file(self, session_id):
        """Get the session file name for a session ID.
        
        Args:
            session_id: The session ID
            
        Returns:
            str: The session file name, or None if not found
        """
        if isinstance(session_id, dict) and "value" in session_id:
            session_id = session_id["value"]
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT session_file FROM sessions WHERE session_id=?", (session_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None

# Create a singleton instance
db_manager = DatabaseManager() 
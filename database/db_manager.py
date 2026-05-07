import sqlite3
import csv
import os
from datetime import datetime


class DatabaseManager:
    """
    Manages all SQLite3 database operations.
    Demonstrates: sqlite3, SQL SELECT, SQL JOIN
    """

    DB_PATH = "monty_hall.db"
    EXPORTS_DIR = "exports"

    def __init__(self):
        self._connection: sqlite3.Connection | None = None
        self._connect()
        self._create_tables()

    def __str__(self):
        return f"DatabaseManager(db='{self.DB_PATH}')"

    def __repr__(self):
        return f"DatabaseManager(path='{self.DB_PATH}', connected={self._connection is not None})"

    def __del__(self):
        self.close()

    # Connection management
    def _connect(self):
        self._connection = sqlite3.connect(self.DB_PATH)
        self._connection.row_factory = sqlite3.Row  # Dict-like rows
        self._connection.execute("PRAGMA foreign_keys = ON")

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def _create_tables(self):
        """Create all required tables if they don't exist."""
        cursor = self._connection.cursor()

        # Main game sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                door_count  INTEGER NOT NULL,
                mode        TEXT    NOT NULL,
                total_games INTEGER DEFAULT 0,
                wins        INTEGER DEFAULT 0,
                num_games   INTEGER DEFAULT 0,
                created_at  TEXT    DEFAULT (strftime('%d.%m.%Y %H:%M', 'now', 'localtime'))
            )
        """)

        # Individual rounds table (for detailed history)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_rounds (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id   INTEGER NOT NULL,
                round_number INTEGER NOT NULL,
                switched     INTEGER NOT NULL,
                won          INTEGER NOT NULL,
                created_at   TEXT DEFAULT (strftime('%d.%m.%Y %H:%M', 'now', 'localtime')),
                FOREIGN KEY (session_id) REFERENCES game_sessions(id) ON DELETE CASCADE
            )
        """)

        self._connection.commit()

    # Session CRUD
    def create_session(self, name: str, door_count: int, mode: str,
                       num_games: int = 0) -> int:
        """Create a new game session. Returns the new session ID."""
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO game_sessions (name, door_count, mode, num_games)
            VALUES (?, ?, ?, ?)
        """, (name, door_count, mode, num_games))
        self._connection.commit()
        return cursor.lastrowid

    def update_session_stats(self, session_id: int, total_games: int, wins: int):
        """Update win/loss stats for a session."""
        self._connection.execute("""
            UPDATE game_sessions
            SET total_games = ?, wins = ?
            WHERE id = ?
        """, (total_games, wins, session_id))
        self._connection.commit()

    def add_round(self, session_id: int, round_number: int,
                  switched: bool, won: bool):
        """Record an individual game round."""
        self._connection.execute("""
            INSERT INTO game_rounds (session_id, round_number, switched, won)
            VALUES (?, ?, ?, ?)
        """, (session_id, round_number, int(switched), int(won)))
        self._connection.commit()

    def get_all_sessions(self) -> list[dict]:
        """
        Fetch all sessions with aggregated stats.
        Demonstrates: SQL SELECT with LEFT JOIN and GROUP BY
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT
                gs.id,
                gs.name,
                gs.door_count,
                gs.mode,
                gs.total_games,
                gs.wins,
                gs.num_games,
                gs.created_at,
                ROUND(
                    CASE WHEN gs.total_games > 0
                         THEN CAST(gs.wins AS REAL) / gs.total_games * 100
                         ELSE 0
                    END, 1
                ) AS win_rate,
                COUNT(gr.id) AS round_count
            FROM game_sessions gs
            LEFT JOIN game_rounds gr ON gs.id = gr.session_id
            GROUP BY gs.id
            ORDER BY gs.created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_session_by_id(self, session_id: int) -> dict | None:
        """Get a single session with its rounds count."""
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT
                gs.*,
                COUNT(gr.id) AS round_count,
                ROUND(
                    CASE WHEN gs.total_games > 0
                         THEN CAST(gs.wins AS REAL) / gs.total_games * 100
                         ELSE 0
                    END, 1
                ) AS win_rate
            FROM game_sessions gs
            LEFT JOIN game_rounds gr ON gs.id = gr.session_id
            WHERE gs.id = ?
            GROUP BY gs.id
        """, (session_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_rounds_for_session(self, session_id: int) -> list[dict]:
        """Get all rounds for a specific session."""
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT * FROM game_rounds
            WHERE session_id = ?
            ORDER BY round_number ASC
        """, (session_id,))
        return [dict(row) for row in cursor.fetchall()]

    def delete_session(self, session_id: int):
        """Delete a session and all its rounds (cascade)."""
        self._connection.execute(
            "DELETE FROM game_sessions WHERE id = ?", (session_id,)
        )
        self._connection.commit()

    def get_global_stats(self) -> dict:
        """
        Return global statistics across all sessions.
        Uses subquery to avoid double-counting from JOIN.
        Demonstrates: SQL aggregate functions, subquery, JOIN
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT
                COUNT(gs.id)                                    AS total_sessions,
                COALESCE(SUM(gs.total_games), 0)                AS total_games,
                COALESCE(SUM(gs.wins), 0)                       AS total_wins,
                ROUND(
                    CASE WHEN SUM(gs.total_games) > 0
                         THEN CAST(SUM(gs.wins) AS REAL) / SUM(gs.total_games) * 100
                         ELSE 0
                    END, 1
                )                                               AS overall_win_rate,
                COALESCE(
                    (SELECT COUNT(*) FROM game_rounds), 0
                )                                               AS total_rounds
            FROM game_sessions gs
        """)
        row = cursor.fetchone()
        return dict(row) if row else {}

    # CSV Export (Week 13: Data Formats)
    def export_to_csv(self, session_id: int | None = None) -> str:
        """
        Export sessions (or a specific session) to CSV.
        Demonstrates: CSV data format handling
        """
        os.makedirs(self.EXPORTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if session_id:
            filename = os.path.join(self.EXPORTS_DIR, f"session_{session_id}_{timestamp}.csv")
            sessions = [self.get_session_by_id(session_id)]
            rounds = self.get_rounds_for_session(session_id)
        else:
            filename = os.path.join(self.EXPORTS_DIR, f"all_sessions_{timestamp}.csv")
            sessions = self.get_all_sessions()
            rounds = []

        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)

            # Sessions header
            writer.writerow(["=== GAME SESSIONS ==="])
            writer.writerow(["ID", "Name", "Doors", "Mode", "Total Games",
                             "Wins", "Win Rate %", "Created At"])
            for s in sessions:
                if s:
                    writer.writerow([
                        s["id"], s["name"], s["door_count"], s["mode"],
                        s["total_games"], s["wins"],
                        s.get("win_rate", 0), s["created_at"]
                    ])

            if rounds:
                writer.writerow([])
                writer.writerow(["=== ROUNDS ==="])
                writer.writerow(["Round #", "Switched", "Won"])
                for r in rounds:
                    writer.writerow([
                        r["round_number"],
                        "Yes" if r["switched"] else "No",
                        "Yes" if r["won"] else "No"
                    ])

        return filename

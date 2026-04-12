import sqlite3

DB_NAME = "sport.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def get_leagues_by_sport(sport: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT league
        FROM teams
        WHERE sport = ?
        ORDER BY league
    """, (sport,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def get_teams_by_league(league: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM teams
        WHERE league = ?
        ORDER BY name
    """, (league,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def get_team_details(team_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, sport, name, country, league, stadium, coach, founded_year, trophies, description
        FROM teams
        WHERE name = ?
    """, (team_name,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_team_stats(team_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT matches_played, wins, draws, losses, goals_scored, goals_conceded, points
        FROM team_stats
        WHERE team_id = ?
    """, (team_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_latest_matches(team_id: int, limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT opponent, match_date, tournament, home_away, scored, conceded, result
        FROM matches
        WHERE team_id = ?
        ORDER BY match_date DESC
        LIMIT ?
    """, (team_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_best_players(team_id: int, limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, position, number, age, nationality, goals_points, assists, rating
        FROM players
        WHERE team_id = ?
        ORDER BY rating DESC, goals_points DESC, assists DESC
        LIMIT ?
    """, (team_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows
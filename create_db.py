import sqlite3

DB_NAME = "sport.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sport TEXT NOT NULL,
        name TEXT NOT NULL UNIQUE,
        country TEXT,
        league TEXT,
        stadium TEXT,
        coach TEXT,
        founded_year INTEGER,
        trophies INTEGER DEFAULT 0,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        position TEXT,
        number INTEGER,
        age INTEGER,
        nationality TEXT,
        goals_points INTEGER DEFAULT 0,
        assists INTEGER DEFAULT 0,
        rating REAL DEFAULT 0,
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sport TEXT NOT NULL,
        team_id INTEGER NOT NULL,
        opponent TEXT NOT NULL,
        match_date TEXT,
        tournament TEXT,
        home_away TEXT,
        scored INTEGER,
        conceded INTEGER,
        result TEXT,
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER NOT NULL UNIQUE,
        matches_played INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        draws INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        goals_scored INTEGER DEFAULT 0,
        goals_conceded INTEGER DEFAULT 0,
        points INTEGER DEFAULT 0,
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    teams = [
        # EPL
        ("Football", "Manchester City", "England", "EPL", "Etihad Stadium", "Pep Guardiola", 1880, 35,
         "Manchester City is one of the strongest clubs in English and European football."),
        ("Football", "Arsenal", "England", "EPL", "Emirates Stadium", "Mikel Arteta", 1886, 48,
         "Arsenal is one of the most successful clubs in England with a long history."),
        ("Football", "Liverpool", "England", "EPL", "Anfield", "Arne Slot", 1892, 68,
         "Liverpool is a historic English club known for domestic and European success."),
        ("Football", "Chelsea", "England", "EPL", "Stamford Bridge", "Mauricio Pochettino", 1905, 34,
         "Chelsea is a major English club with strong recent success."),

        # LaLiga
        ("Football", "Real Madrid", "Spain", "LaLiga", "Santiago Bernabéu", "Carlo Ancelotti", 1902, 100,
         "Real Madrid is one of the most decorated clubs in world football."),
        ("Football", "Barcelona", "Spain", "LaLiga", "Olympic Stadium", "Xavi Hernández", 1899, 97,
         "Barcelona is one of the most successful and influential clubs in football history."),
        ("Football", "Atletico Madrid", "Spain", "LaLiga", "Cívitas Metropolitano", "Diego Simeone", 1903, 33,
         "Atletico Madrid is known for intensity, discipline, and strong league performances."),
        ("Football", "Sevilla", "Spain", "LaLiga", "Ramón Sánchez Pizjuán", "Quique Sánchez Flores", 1890, 20,
         "Sevilla is famous for strong performances, especially in European competitions."),

        # Serie A
        ("Football", "Inter", "Italy", "Serie A", "San Siro", "Simone Inzaghi", 1908, 45,
         "Inter is one of Italy’s biggest and most successful clubs."),
        ("Football", "Juventus", "Italy", "Serie A", "Allianz Stadium", "Massimiliano Allegri", 1897, 70,
         "Juventus is historically the most successful club in Italian football."),
        ("Football", "AC Milan", "Italy", "Serie A", "San Siro", "Stefano Pioli", 1899, 49,
         "AC Milan is a legendary club with rich domestic and European history."),
        ("Football", "Napoli", "Italy", "Serie A", "Stadio Diego Armando Maradona", "Francesco Calzona", 1926, 17,
         "Napoli is one of Italy’s top clubs, famous for passionate supporters."),

        # Bundesliga
        ("Football", "Bayern Munich", "Germany", "Bundesliga", "Allianz Arena", "Thomas Tuchel", 1900, 83,
         "Bayern Munich is Germany’s dominant football club."),
        ("Football", "Borussia Dortmund", "Germany", "Bundesliga", "Signal Iduna Park", "Edin Terzić", 1909, 25,
         "Borussia Dortmund is known for attacking football and elite fan support."),
        ("Football", "RB Leipzig", "Germany", "Bundesliga", "Red Bull Arena", "Marco Rose", 2009, 8,
         "RB Leipzig is a modern German club with rapid growth."),
        ("Football", "Bayer Leverkusen", "Germany", "Bundesliga", "BayArena", "Xabi Alonso", 1904, 7,
         "Bayer Leverkusen is a strong Bundesliga club with technical football."),

        # Ligue 1
        ("Football", "PSG", "France", "Ligue 1", "Parc des Princes", "Luis Enrique", 1970, 50,
         "Paris Saint-Germain is France’s most powerful modern football club."),
        ("Football", "Marseille", "France", "Ligue 1", "Stade Vélodrome", "Jean-Louis Gasset", 1899, 27,
         "Marseille is one of France’s most historic and passionate clubs."),
        ("Football", "Lyon", "France", "Ligue 1", "Groupama Stadium", "Pierre Sage", 1950, 20,
         "Lyon is known for developing talented players and strong domestic eras."),
        ("Football", "Monaco", "France", "Ligue 1", "Stade Louis II", "Adi Hütter", 1924, 17,
         "Monaco is known for youth development and competitive football.")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO teams
        (sport, name, country, league, stadium, coach, founded_year, trophies, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, teams)

    conn.commit()

    # Team IDs
    cursor.execute("SELECT id, name FROM teams")
    team_map = {name: team_id for team_id, name in cursor.fetchall()}

    players = [
        # Manchester City
        (team_map["Manchester City"], "Erling Haaland", "Forward", 9, 23, "Norway", 27, 5, 9.4),
        (team_map["Manchester City"], "Kevin De Bruyne", "Midfielder", 17, 32, "Belgium", 7, 18, 9.3),
        (team_map["Manchester City"], "Phil Foden", "Midfielder", 47, 23, "England", 16, 9, 8.9),

        # Arsenal
        (team_map["Arsenal"], "Bukayo Saka", "Winger", 7, 22, "England", 14, 10, 9.0),
        (team_map["Arsenal"], "Martin Ødegaard", "Midfielder", 8, 25, "Norway", 8, 11, 8.8),
        (team_map["Arsenal"], "Declan Rice", "Midfielder", 41, 25, "England", 6, 7, 8.7),

        # Liverpool
        (team_map["Liverpool"], "Mohamed Salah", "Winger", 11, 31, "Egypt", 22, 11, 9.2),
        (team_map["Liverpool"], "Virgil van Dijk", "Defender", 4, 32, "Netherlands", 3, 2, 8.6),
        (team_map["Liverpool"], "Darwin Núñez", "Forward", 9, 24, "Uruguay", 15, 8, 8.5),

        # Real Madrid
        (team_map["Real Madrid"], "Jude Bellingham", "Midfielder", 5, 20, "England", 19, 6, 9.3),
        (team_map["Real Madrid"], "Vinícius Júnior", "Winger", 7, 23, "Brazil", 18, 10, 9.1),
        (team_map["Real Madrid"], "Rodrygo", "Forward", 11, 23, "Brazil", 14, 7, 8.7),

        # Barcelona
        (team_map["Barcelona"], "Robert Lewandowski", "Forward", 9, 35, "Poland", 20, 5, 8.9),
        (team_map["Barcelona"], "Pedri", "Midfielder", 8, 21, "Spain", 6, 8, 8.7),
        (team_map["Barcelona"], "Lamine Yamal", "Winger", 27, 16, "Spain", 7, 9, 8.8),

        # Inter
        (team_map["Inter"], "Lautaro Martínez", "Forward", 10, 26, "Argentina", 24, 4, 9.3),
        (team_map["Inter"], "Nicolò Barella", "Midfielder", 23, 27, "Italy", 6, 9, 8.8),
        (team_map["Inter"], "Hakan Çalhanoğlu", "Midfielder", 20, 30, "Turkey", 10, 7, 8.9),

        # Juventus
        (team_map["Juventus"], "Dušan Vlahović", "Forward", 9, 24, "Serbia", 17, 4, 8.8),
        (team_map["Juventus"], "Federico Chiesa", "Winger", 7, 26, "Italy", 10, 6, 8.6),
        (team_map["Juventus"], "Adrien Rabiot", "Midfielder", 25, 29, "France", 5, 4, 8.3),

        # Bayern Munich
        (team_map["Bayern Munich"], "Harry Kane", "Forward", 9, 30, "England", 30, 8, 9.5),
        (team_map["Bayern Munich"], "Jamal Musiala", "Midfielder", 42, 21, "Germany", 12, 10, 9.0),
        (team_map["Bayern Munich"], "Leroy Sané", "Winger", 10, 28, "Germany", 11, 13, 8.8),

        # Borussia Dortmund
        (team_map["Borussia Dortmund"], "Julian Brandt", "Midfielder", 19, 27, "Germany", 8, 11, 8.6),
        (team_map["Borussia Dortmund"], "Niclas Füllkrug", "Forward", 14, 31, "Germany", 14, 6, 8.5),
        (team_map["Borussia Dortmund"], "Mats Hummels", "Defender", 15, 35, "Germany", 2, 1, 8.2),

        # PSG
        (team_map["PSG"], "Kylian Mbappé", "Forward", 7, 25, "France", 29, 7, 9.6),
        (team_map["PSG"], "Ousmane Dembélé", "Winger", 10, 26, "France", 6, 11, 8.5),
        (team_map["PSG"], "Vitinha", "Midfielder", 17, 24, "Portugal", 7, 5, 8.4),

        # Marseille
        (team_map["Marseille"], "Pierre-Emerick Aubameyang", "Forward", 10, 34, "Gabon", 18, 5, 8.7),
        (team_map["Marseille"], "Jordan Veretout", "Midfielder", 27, 31, "France", 5, 7, 8.2),
        (team_map["Marseille"], "Jonathan Clauss", "Defender", 7, 31, "France", 3, 8, 8.1),
    ]

    cursor.executemany("""
        INSERT INTO players
        (team_id, name, position, number, age, nationality, goals_points, assists, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, players)

    matches = [
        # Manchester City
        ( "Football", team_map["Manchester City"], "Arsenal", "2026-04-08", "Premier League", "Home", 2, 1, "Win"),
        ( "Football", team_map["Manchester City"], "Liverpool", "2026-04-02", "Premier League", "Away", 1, 1, "Draw"),
        ( "Football", team_map["Manchester City"], "Chelsea", "2026-03-28", "Premier League", "Home", 3, 0, "Win"),
        ( "Football", team_map["Manchester City"], "Tottenham", "2026-03-20", "Premier League", "Away", 0, 1, "Loss"),
        ( "Football", team_map["Manchester City"], "Newcastle", "2026-03-15", "Premier League", "Home", 4, 2, "Win"),

        # Arsenal
        ( "Football", team_map["Arsenal"], "Manchester City", "2026-04-08", "Premier League", "Away", 1, 2, "Loss"),
        ( "Football", team_map["Arsenal"], "Aston Villa", "2026-04-03", "Premier League", "Home", 2, 0, "Win"),
        ( "Football", team_map["Arsenal"], "Brighton", "2026-03-29", "Premier League", "Away", 1, 1, "Draw"),
        ( "Football", team_map["Arsenal"], "Chelsea", "2026-03-22", "Premier League", "Home", 3, 1, "Win"),
        ( "Football", team_map["Arsenal"], "Liverpool", "2026-03-16", "Premier League", "Away", 0, 2, "Loss"),

        # Liverpool
        ( "Football", team_map["Liverpool"], "Everton", "2026-04-07", "Premier League", "Home", 2, 0, "Win"),
        ( "Football", team_map["Liverpool"], "Manchester City", "2026-04-02", "Premier League", "Home", 1, 1, "Draw"),
        ( "Football", team_map["Liverpool"], "Arsenal", "2026-03-16", "Premier League", "Home", 2, 0, "Win"),
        ( "Football", team_map["Liverpool"], "Chelsea", "2026-03-30", "Premier League", "Away", 3, 2, "Win"),
        ( "Football", team_map["Liverpool"], "West Ham", "2026-03-24", "Premier League", "Home", 1, 0, "Win"),

        # Real Madrid
        ( "Football", team_map["Real Madrid"], "Barcelona", "2026-04-06", "LaLiga", "Home", 2, 1, "Win"),
        ( "Football", team_map["Real Madrid"], "Sevilla", "2026-04-01", "LaLiga", "Away", 1, 0, "Win"),
        ( "Football", team_map["Real Madrid"], "Atletico Madrid", "2026-03-27", "LaLiga", "Home", 1, 1, "Draw"),
        ( "Football", team_map["Real Madrid"], "Valencia", "2026-03-20", "LaLiga", "Away", 3, 0, "Win"),
        ( "Football", team_map["Real Madrid"], "Villarreal", "2026-03-14", "LaLiga", "Home", 2, 0, "Win"),

        # Barcelona
        ( "Football", team_map["Barcelona"], "Real Madrid", "2026-04-06", "LaLiga", "Away", 1, 2, "Loss"),
        ( "Football", team_map["Barcelona"], "Girona", "2026-04-01", "LaLiga", "Home", 3, 1, "Win"),
        ( "Football", team_map["Barcelona"], "Sevilla", "2026-03-26", "LaLiga", "Away", 2, 2, "Draw"),
        ( "Football", team_map["Barcelona"], "Atletico Madrid", "2026-03-18", "LaLiga", "Home", 2, 1, "Win"),
        ( "Football", team_map["Barcelona"], "Real Sociedad", "2026-03-11", "LaLiga", "Away", 1, 0, "Win"),

        # Inter
        ( "Football", team_map["Inter"], "Juventus", "2026-04-05", "Serie A", "Home", 2, 0, "Win"),
        ( "Football", team_map["Inter"], "Napoli", "2026-03-31", "Serie A", "Away", 1, 1, "Draw"),
        ( "Football", team_map["Inter"], "AC Milan", "2026-03-26", "Serie A", "Home", 3, 1, "Win"),
        ( "Football", team_map["Inter"], "Roma", "2026-03-19", "Serie A", "Away", 0, 1, "Loss"),
        ( "Football", team_map["Inter"], "Lazio", "2026-03-12", "Serie A", "Home", 2, 0, "Win"),

        # Juventus
        ( "Football", team_map["Juventus"], "Inter", "2026-04-05", "Serie A", "Away", 0, 2, "Loss"),
        ( "Football", team_map["Juventus"], "Milan", "2026-03-30", "Serie A", "Home", 1, 0, "Win"),
        ( "Football", team_map["Juventus"], "Napoli", "2026-03-25", "Serie A", "Away", 1, 1, "Draw"),
        ( "Football", team_map["Juventus"], "Torino", "2026-03-17", "Serie A", "Home", 2, 0, "Win"),
        ( "Football", team_map["Juventus"], "Atalanta", "2026-03-10", "Serie A", "Away", 1, 2, "Loss"),

        # Bayern Munich
        ( "Football", team_map["Bayern Munich"], "Borussia Dortmund", "2026-04-04", "Bundesliga", "Home", 3, 1, "Win"),
        ( "Football", team_map["Bayern Munich"], "RB Leipzig", "2026-03-29", "Bundesliga", "Away", 2, 2, "Draw"),
        ( "Football", team_map["Bayern Munich"], "Bayer Leverkusen", "2026-03-23", "Bundesliga", "Home", 1, 0, "Win"),
        ( "Football", team_map["Bayern Munich"], "Wolfsburg", "2026-03-16", "Bundesliga", "Away", 4, 1, "Win"),
        ( "Football", team_map["Bayern Munich"], "Frankfurt", "2026-03-09", "Bundesliga", "Home", 2, 1, "Win"),

        # Borussia Dortmund
        ( "Football", team_map["Borussia Dortmund"], "Bayern Munich", "2026-04-04", "Bundesliga", "Away", 1, 3, "Loss"),
        ( "Football", team_map["Borussia Dortmund"], "Stuttgart", "2026-03-30", "Bundesliga", "Home", 2, 1, "Win"),
        ( "Football", team_map["Borussia Dortmund"], "Leipzig", "2026-03-24", "Bundesliga", "Away", 1, 1, "Draw"),
        ( "Football", team_map["Borussia Dortmund"], "Gladbach", "2026-03-17", "Bundesliga", "Home", 3, 0, "Win"),
        ( "Football", team_map["Borussia Dortmund"], "Augsburg", "2026-03-10", "Bundesliga", "Away", 2, 0, "Win"),

        # PSG
        ( "Football", team_map["PSG"], "Marseille", "2026-04-05", "Ligue 1", "Home", 3, 1, "Win"),
        ( "Football", team_map["PSG"], "Monaco", "2026-03-31", "Ligue 1", "Away", 2, 2, "Draw"),
        ( "Football", team_map["PSG"], "Lyon", "2026-03-25", "Ligue 1", "Home", 4, 0, "Win"),
        ( "Football", team_map["PSG"], "Lille", "2026-03-18", "Ligue 1", "Away", 1, 0, "Win"),
        ( "Football", team_map["PSG"], "Nice", "2026-03-11", "Ligue 1", "Home", 2, 1, "Win"),

        # Marseille
        ( "Football", team_map["Marseille"], "PSG", "2026-04-05", "Ligue 1", "Away", 1, 3, "Loss"),
        ( "Football", team_map["Marseille"], "Lyon", "2026-03-30", "Ligue 1", "Home", 2, 0, "Win"),
        ( "Football", team_map["Marseille"], "Monaco", "2026-03-23", "Ligue 1", "Away", 1, 1, "Draw"),
        ( "Football", team_map["Marseille"], "Rennes", "2026-03-16", "Ligue 1", "Home", 3, 2, "Win"),
        ( "Football", team_map["Marseille"], "Lille", "2026-03-09", "Ligue 1", "Away", 0, 1, "Loss"),
    ]

    cursor.executemany("""
        INSERT INTO matches
        (sport, team_id, opponent, match_date, tournament, home_away, scored, conceded, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, matches)

    team_stats = [
        (team_map["Manchester City"], 32, 23, 5, 4, 78, 29, 74),
        (team_map["Arsenal"], 32, 22, 6, 4, 69, 31, 72),
        (team_map["Liverpool"], 32, 21, 8, 3, 71, 28, 71),
        (team_map["Real Madrid"], 31, 24, 5, 2, 70, 24, 77),
        (team_map["Barcelona"], 31, 21, 6, 4, 65, 33, 69),
        (team_map["Inter"], 31, 23, 5, 3, 68, 25, 74),
        (team_map["Juventus"], 31, 19, 7, 5, 52, 29, 64),
        (team_map["Bayern Munich"], 29, 22, 4, 3, 75, 27, 70),
        (team_map["Borussia Dortmund"], 29, 17, 6, 6, 58, 35, 57),
        (team_map["PSG"], 30, 24, 4, 2, 79, 26, 76),
        (team_map["Marseille"], 30, 16, 7, 7, 52, 36, 55),
    ]

    for stat in team_stats:
        cursor.execute("""
            INSERT OR REPLACE INTO team_stats
            (team_id, matches_played, wins, draws, losses, goals_scored, goals_conceded, points)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, stat)

    conn.commit()
    conn.close()
    print("Database created and sample data inserted successfully.")


if __name__ == "__main__":
    init_db()
    seed_data()
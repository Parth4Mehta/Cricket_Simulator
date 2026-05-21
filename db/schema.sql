-- CricSim SQLite schema
-- Mirrors the shape of the existing JSON storage so the cutover is mechanical.

-- Aggregated team standings (mirrors database/team_stats.json).
CREATE TABLE IF NOT EXISTS teams (
    team_code      TEXT PRIMARY KEY,
    played         INTEGER NOT NULL DEFAULT 0,
    won            INTEGER NOT NULL DEFAULT 0,
    lost           INTEGER NOT NULL DEFAULT 0,
    tied           INTEGER NOT NULL DEFAULT 0,
    points         INTEGER NOT NULL DEFAULT 0,
    runs_scored    INTEGER NOT NULL DEFAULT 0,
    runs_conceded  INTEGER NOT NULL DEFAULT 0,
    balls_faced    INTEGER NOT NULL DEFAULT 0,
    balls_bowled   INTEGER NOT NULL DEFAULT 0
);

-- Aggregated player career stats (mirrors database/player_stats.json).
CREATE TABLE IF NOT EXISTS players (
    name                  TEXT PRIMARY KEY,
    team                  TEXT,
    runs                  INTEGER NOT NULL DEFAULT 0,
    balls_faced           INTEGER NOT NULL DEFAULT 0,
    fours                 INTEGER NOT NULL DEFAULT 0,
    sixes                 INTEGER NOT NULL DEFAULT 0,
    matches               INTEGER NOT NULL DEFAULT 0,
    outs                  INTEGER NOT NULL DEFAULT 0,
    not_outs              INTEGER NOT NULL DEFAULT 0,
    highest_score         INTEGER NOT NULL DEFAULT 0,
    wickets               INTEGER NOT NULL DEFAULT 0,
    balls_bowled          INTEGER NOT NULL DEFAULT 0,
    best_bowling_wickets  INTEGER NOT NULL DEFAULT 0,
    best_bowling_runs     INTEGER NOT NULL DEFAULT 999
);

-- One row per played match (mirrors database/match_stats/*.json).
CREATE TABLE IF NOT EXISTS matches (
    match_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    team_a         TEXT NOT NULL,
    team_b         TEXT NOT NULL,
    timestamp_utc  TEXT NOT NULL,
    winner         TEXT,
    margin         TEXT,
    a_score        INTEGER,
    b_score        INTEGER
);

-- Per-match batting card (one row per batter per match).
CREATE TABLE IF NOT EXISTS match_batting (
    match_id     INTEGER NOT NULL,
    team         TEXT NOT NULL,
    position     INTEGER NOT NULL,
    player_name  TEXT,
    runs         INTEGER NOT NULL DEFAULT 0,
    balls        INTEGER NOT NULL DEFAULT 0,
    fours        INTEGER NOT NULL DEFAULT 0,
    sixes        INTEGER NOT NULL DEFAULT 0,
    dismissal    TEXT,
    PRIMARY KEY (match_id, team, position),
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE
);

-- Per-match bowling card (one row per bowler per match).
CREATE TABLE IF NOT EXISTS match_bowling (
    match_id     INTEGER NOT NULL,
    team         TEXT NOT NULL,
    player_name  TEXT NOT NULL,
    overs        INTEGER NOT NULL DEFAULT 0,
    balls        INTEGER NOT NULL DEFAULT 0,
    runs         INTEGER NOT NULL DEFAULT 0,
    wickets      INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (match_id, team, player_name),
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE
);

-- Cumulative team standings across seasons (mirrors database/cumulative_stats.json).
CREATE TABLE IF NOT EXISTS cumulative_teams (
    team_code  TEXT PRIMARY KEY,
    played     INTEGER NOT NULL DEFAULT 0,
    won        INTEGER NOT NULL DEFAULT 0,
    lost       INTEGER NOT NULL DEFAULT 0,
    tied       INTEGER NOT NULL DEFAULT 0,
    points     INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_players_runs    ON players(runs DESC);
CREATE INDEX IF NOT EXISTS idx_players_wickets ON players(wickets DESC);
CREATE INDEX IF NOT EXISTS idx_matches_ts      ON matches(timestamp_utc);

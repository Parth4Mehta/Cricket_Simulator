"""
db package - SQLite-backed persistence layer for CricSim.

This package adds a SQLite database alongside the legacy JSON files.
In Part 1 of the migration it runs purely in shadow mode: the database
is populated from existing JSON, but the game itself still reads and
writes JSON. Part 2 will switch the game over to use SQLite.
"""

class Player:
    def __init__(self, name, batting, bowling):
        self.name = name
        self.batting = batting
        self.bowling = bowling

def get_teams():
    return {
        "MI": [
            Player("De Kock", 7.3, 0.5),
            Player("S Rohit", 8.3, 0.8),
            Player("V Tilak", 8.8, 0.9),
            Player("Y Suryakumar", 9.4, 1.2),
            Player("W Jacks", 7.7, 2.8),
            Player("P Hardik", 8.0, 7.2),
            Player("AM Ghazanfar", 4.6, 7.3),
            Player("S Thakur", 4.2, 7.4),
            Player("D Chahar", 3.3, 7.8),
            Player("T Boult", 1.1, 9.0),
            Player("J Bumrah", 1.0, 9.8),
        ],

        "CSK": [
            Player("A Mhatre", 7.4, 0.7),
            Player("S Samson", 8.6, 1.0),
            Player("R Gaikwad", 8.6, 0.9),
            Player("D Brevis", 8.4, 2.1),
            Player("S Dube", 7.6, 5.2),
            Player("P Veer", 5.8, 5.4),
            Player("MS Dhoni", 7.4, 0.9),
            Player("N Ellis", 2.4, 7.8),
            Player("M Henry", 1.6, 7.4),
            Player("A Noor", 1.4, 9.4),
            Player("A Khaleel", 1.0, 7.6),
        ],

        "SRH": [
            Player("S Abhishek", 9.6, 3.2),
            Player("T Head", 9.0, 3.1),
            Player("I Kishan", 8.1, 1.0),
            Player("H Klaasen", 8.9, 1.0),
            Player("NK Reddy", 7.7, 5.2),
            Player("L Livingstone", 7.6, 1.0),
            Player("D Harsh", 5.2, 5.9),
            Player("P Cummins", 3.0, 8.1),
            Player("P Harshal", 2.5, 8.6),
            Player("Z Ansari", 1.6, 7.3),
            Player("J Unadkat", 1.3, 7.4),
        ],

        "RCB": [
            Player("P Salt", 8.9, 0.9),
            Player("V Kohli", 9.6, 2.1),
            Player("V Iyer", 7.6, 1.0),
            Player("R Patidar", 7.9, 1.0),
            Player("S Jitesh", 7.9, 1.0),
            Player("T David", 8.3, 3.9),
            Player("P Krunal", 5.1, 7.5),
            Player("K Bhuvneshwar", 3.6, 8.8),
            Player("J Hazlewood", 1.6, 9.1),
            Player("S Suyash", 1.2, 7.3),
            Player("Y Dayal", 1.0, 7.1),
        ],

        "RR": [
            Player("Y Jaiswal", 9.6, 1.0),
            Player("V Sooryavanshi", 8.0, 1.0),
            Player("S Hetmeyer", 7.4, 1.0),
            Player("R Parag", 7.8, 3.8),
            Player("D Jurel", 7.6, 1.0),
            Player("R Jadeja", 7.3, 7.6),
            Player("D Ferreira", 6.6, 5.1),
            Player("S Curran", 5.6, 7.1),
            Player("J Archer", 2.2, 8.6),
            Player("S Sandeep", 1.0, 7.5),
            Player("T Deshpande", 1.0, 7.2),
        ],

        "PBKS": [
            Player("S Prabhsimran", 8.2, 1.0),
            Player("P Arya", 7.5, 0.9),
            Player("S Iyer", 9.5, 2.0),
            Player("N Wadhera", 7.4, 2.0),
            Player("C Connolly", 7.2, 5.0),
            Player("S Shashank", 7.8, 1.0),
            Player("M Stoinis", 6.8, 5.4),
            Player("M Jansen", 5.5, 7.5),
            Player("H Brar", 3.6, 7.6),
            Player("S Arshdeep", 1.0, 9.4),
            Player("Y Chahal", 1.0, 8.8),
        ],

        "LSG": [
            Player("M Marsh", 8.3, 6.4),
            Player("A Markram", 8.1, 4.0),
            Player("N Pooran", 9.4, 1.0),
            Player("R Pant", 8.7, 1.0),
            Player("A Badoni", 7.4, 2.0),
            Player("A Samad", 7.1, 2.0),
            Player("W Hasaranga", 5.2, 7.4),
            Player("R Digvesh", 2.0, 7.6),
            Player("Y Mayank", 1.0, 8.1),
            Player("K Avesh", 1.0, 7.9),
            Player("M Shami", 1.0, 7.7),
        ],

        "KKR": [
            Player("S Narine", 7.5, 9.0),
            Player("F Allen", 7.3, 1.0),
            Player("A Rahane", 8.3, 1.0),
            Player("A Raghuvanshi", 8.0, 1.0),
            Player("C Green", 8.1, 3.9),
            Player("S Rinku", 7.8, 1.0),
            Player("S Ramandeep", 7.6, 4.0),
            Player("H Rana", 4.1, 8.1),
            Player("V Arora", 1.0, 7.5),
            Player("M Pathirana", 1.0, 8.5),
            Player("V Chakravarthy", 1.0, 9.2),
        ],

        "GT": [
            Player("S Sudarshan", 9.2, 1.0),
            Player("S Gill", 9.3, 1.0),
            Player("J Buttler", 9.3, 1.0),
            Player("W Sundar", 6.8, 7.6),
            Player("K Shahrukh", 7.1, 3.0),
            Player("G Phillips", 7.2, 4.0),
            Player("R Tewatia", 6.4, 6.0),
            Player("K Rashid", 5.1, 9.5),
            Player("K Rabada", 2.2, 8.7),
            Player("K Prasidh", 1.0, 8.0),
            Player("M Siraj", 1.0, 8.4),
        ],

        "DC": [
            Player("KL Rahul", 9.5, 1.0),
            Player("B Duckett", 7.2, 1.0),
            Player("N Rana", 7.8, 1.0),
            Player("T Stubbs", 8.5, 3.0),
            Player("S Ashutosh", 7.6, 2.0),
            Player("D Miller", 8.2, 5.0),
            Player("Axar Patel", 7.0, 8.2),
            Player("N Auqib", 4.1, 7.2),
            Player("M Starc", 3.3, 8.6),
            Player("Y Kuldeep", 2.8, 9.2),
            Player("T Natarajan", 1.0, 7.9),
        ],
    }

def calculate_team_strength(team):
    batting_strength = sum(sorted((player.batting for player in team), reverse=True)[:7])
    bowling_strength = sum(sorted((player.bowling for player in team), reverse=True)[:5])
    return batting_strength, bowling_strength


def get_all_batsmen_sorted(teams=None, as_names=True):
    """Return all players sorted by batting ability (best -> worst).

    If `as_names` is True return a list of `(name, batting)` tuples,
    otherwise return `Player` objects in sorted order.
    """
    if teams is None:
        teams = get_teams()
    players = []
    for roster in teams.values():
        players.extend(roster)
    sorted_players = sorted(players, key=lambda p: p.batting, reverse=True)
    if as_names:
        return [(p.name, p.batting) for p in sorted_players]
    return sorted_players


def get_all_bowlers_sorted(teams=None, as_names=True):
    """Return all players sorted by bowling ability (best -> worst).

    If `as_names` is True return a list of `(name, bowling)` tuples,
    otherwise return `Player` objects in sorted order.
    """
    if teams is None:
        teams = get_teams()
    players = []
    for roster in teams.values():
        players.extend(roster)
    sorted_players = sorted(players, key=lambda p: p.bowling, reverse=True)
    if as_names:
        return [(p.name, p.bowling) for p in sorted_players]
    return sorted_players


if __name__ == "__main__":
    teams = get_teams()
    for team_name, roster in teams.items():
        batting_strength, bowling_strength = calculate_team_strength(roster)
        print(f"Team: {team_name}, Batting Strength: {batting_strength:.1f}, Bowling Strength: {bowling_strength:.1f}")
        print(f"Total Strength: {batting_strength+bowling_strength:.1f}")
        
    print("\n Batsmen sorted by batting ability:")
    for name, batting in get_all_batsmen_sorted():
        print(f"{name:25} {batting}")
    
    print("\n Bowlers sorted by bowling ability:")
    for name, bowling in get_all_bowlers_sorted():
        print(f"{name:25} {bowling}")
    print("Teams data loaded successfully.")

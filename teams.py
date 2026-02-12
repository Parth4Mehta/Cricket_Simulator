class Player:
    def __init__(self, name, batting, bowling):
        self.name = name
        self.batting = batting
        self.bowling = bowling

def get_teams():
    return {
        "MI": [
            Player("D Kock", 7.3, 0.5),
            Player("S Rohit", 8.3, 0.8),
            Player("V Tilak", 8.8, 0.9),
            Player("Y Suryakumar", 9.4, 1.2),
            Player("W Jacks", 7.7, 2.8),
            Player("P Hardik", 8.0, 7.2),
            Player("A Ghazanfar", 4.6, 7.3),
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
            Player("M Dhoni", 7.4, 0.9),
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
            Player("N Reddy", 7.7, 5.2),
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
            Player("K Rahul", 9.5, 1.0),
            Player("B Duckett", 7.2, 1.0),
            Player("N Rana", 7.8, 1.0),
            Player("T Stubbs", 8.5, 3.0),
            Player("S Ashutosh", 7.6, 2.0),
            Player("D Miller", 8.2, 5.0),
            Player("P Axar", 7.0, 8.2),
            Player("N Auqib", 4.1, 7.2),
            Player("M Starc", 3.3, 8.6),
            Player("Y Kuldeep", 2.8, 9.2),
            Player("T Natarajan", 1.0, 7.9),
        ],
        # IPL 2016 Teams
        "MI16": [
            Player("PZ Parthiv", 7.1, 0.5),
            Player("LZ Simmons", 7.9, 0.6),
            Player("RZ Sharma", 8.8, 2.4),
            Player("AZ Rayudu", 7.6, 1.8),
            Player("KZ Pollard", 8.2, 6.2),
            Player("HZ Pandya", 7.8, 6.8),
            Player("KZ Pandya", 6.4, 6.9),
            Player("SZ Harbhajan", 4.2, 8.0),
            Player("MZ McClenaghan", 2.1, 8.2),
            Player("JJ Bumrah", 1.8, 9.0),
            Player("LZ Malinga", 1.2, 9.0),
        ],

        "RCB16": [
            Player("VZ Kohli", 9.8, 1.2),
            Player("CZ Gayle", 8.9, 0.8),
            Player("AB de Villiers", 9.6, 1.4),
            Player("SZ Watson", 7.8, 6.8),
            Player("SZ Mandeep", 7.4, 0.9),
            Player("SZ Khan", 6.9, 1.4),
            Player("SZ Binny", 6.0, 6.0),
            Player("IZ Abdulla", 5.8, 6.2),
            Player("SZ Aravind", 2.8, 7.6),
            Player("YZ Chahal", 2.4, 8.8),
            Player("CZ Jordan", 2.0, 7.1),
        ],

        "SRH16": [
            Player("DZ Warner", 9.4, 1.6),
            Player("SZ Dhawan", 8.2, 0.8),
            Player("KS Williamson", 8.6, 1.2),
            Player("SZ Yuvraj", 7.6, 5.6),
            Player("NZ Ojha", 7.1, 0.8),
            Player("DZ Hooda", 6.8, 3.2),
            Player("BZ Cutting", 6.1, 6.8),
            Player("BZ Kumar", 3.4, 9.2),
            Player("MZ Rahman", 2.2, 8.6),
            Player("AZ Nehra", 1.6, 8.2),
            Player("RZ Ashish", 6.3, 6.1),
        ],

        "KKR16": [
            Player("GZ Gambhir", 8.2, 1.4),
            Player("RZ Uthappa", 7.8, 0.9),
            Player("MZ Pandey", 7.4, 1.1),
            Player("YK Pathan", 7.6, 5.4),
            Player("SK Yadav", 7.0, 1.8),
            Player("AZ Russell", 7.7, 7.2),
            Player("SZ Narine", 6.8, 8.8),
            Player("PZ Chawla", 3.8, 8.2),
            Player("UZ Yadav", 2.2, 7.8),
            Player("MZ Morkel", 1.8, 8.6),
            Player("CZ Woakes", 3.4, 7.3),
        ],

        "DD16": [
            Player("QZ de Kock", 8.6, 0.7),
            Player("KZ Nair", 7.4, 1.2),
            Player("SZ Iyer", 7.6, 2.2),
            Player("JP Duminy", 7.7, 6.8),
            Player("RZ Pant", 7.2, 0.6),
            Player("AZ Mayank", 7.0, 0.8),
            Player("CZ Brathwaite", 7.1, 7.4),
            Player("CM Morris", 6.9, 7.6),
            Player("AZ Mishra", 3.2, 8.4),
            Player("ZZ Khan", 2.4, 8.4),
            Player("MZ Shami", 1.8, 8.3),
        ],

        "KXIP16": [
            Player("MZ Vijay", 7.6, 0.9),
            Player("MZ Vohra", 7.3, 0.7),
            Player("SZ Gurkareet", 6.9, 0.5),
            Player("MZ Marsh", 7.1, 7.1),
            Player("GJ Maxwell", 8.1, 6.2),
            Player("DA Miller", 8.4, 1.4),
            Player("AZ Patel", 5.8, 7.4),
            Player("MG Johnson", 4.7, 7.8),
            Player("SZ Sharma", 2.6, 8.2),
            Player("SZ Mohit", 2.2, 7.5),
            Player("KZ Abbott", 1.8, 7.7),
        ],

        "GL16": [
            Player("BB McCullum", 8.3, 0.8),
            Player("DR Smith", 8.0, 1.2),
            Player("SZ Raina", 8.4, 5.6),
            Player("AJ Finch", 7.1, 0.9),
            Player("DM Bravo", 7.2, 1.3),
            Player("RA Jadeja", 6.8, 8.0),
            Player("JZ Faulkner", 6.2, 7.1),
            Player("DJ Bravo", 6.4, 8.6),
            Player("PJ Sangwan", 2.4, 7.2),
            Player("SZ Tye", 1.8, 8.2),
            Player("DS Kulkarni", 2.2, 8.0),
        ],

        "RPS16": [
            Player("GZ Bailey", 7.2, 0.8),
            Player("FZ du Plessis", 8.1, 1.1),
            Player("AM Rahane", 8.4, 1.2),
            Player("SZ Smith", 8.6, 2.4),
            Player("MS Dhoni", 8.2, 0.9),
            Player("AL Menaria", 6.1, 5.2),
            Player("RZ Bhatia", 5.8, 6.8),
            Player("RZ Ashwin", 4.6, 8.6),
            Player("AZ Zampa", 3.2, 7.8),
            Player("AB Dinda", 2.4, 7.4),
            Player("IZ Sharma", 2.2, 7.8),
        ],    }

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

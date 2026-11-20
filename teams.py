from models import Player


def get_teams():
    return {
        "MI": [
            Player("D Kock", 7.5, 0.5, "bat", "spin"),
            Player("S Rohit", 8.4, 0.8, "bat", "spin"),
            Player("V Tilak", 8.5, 0.9, "bat", "spin"),
            Player("Y Suryakumar", 8.8, 1.2, "bat", "spin"),
            Player("W Jacks", 7.5, 2.8, "ar", "spin"),
            Player("P Hardik", 8.3, 7.4, "ar", "pace"), # F
            Player("A Ghazanfar", 3.6, 7.6, "bowl", "spin"), # D
            Player("S Thakur", 3.2, 7.5, "bowl", "pace"), # E
            Player("D Chahar", 2.3, 7.8, "bowl", "pace"), # C
            Player("T Boult", 1.1, 8.5, "bowl", "pace"), # B
            Player("J Bumrah", 1.0, 9.5, "bowl", "pace"), # A
        ],

        "CSK": [
            Player("A Mhatre", 7.6, 0.7, "bat", "spin"),
            Player("S Samson", 8.7, 1.0, "bat", "spin"),
            Player("R Gaikwad", 8.5, 0.9, "bat", "spin"),
            Player("D Brevis", 8.4, 2.1, "bat", "spin"),
            Player("S Dube", 8.1, 5.2, "ar", "pace"), # F
            Player("P Veer", 5.8, 5.5, "ar", "spin"), # E
            Player("M Dhoni", 7.4, 0.9, "bat", "pace"),
            Player("N Ellis", 2.4, 7.8, "bowl", "pace"), # B
            Player("M Henry", 1.6, 7.5, "bowl", "pace"), # D
            Player("A Noor", 1.4, 8.9, "bowl", "spin"), # A
            Player("A Khaleel", 1.0, 7.6, "bowl", "pace"), # C
        ],

        "SRH": [
            Player("S Abhishek", 9.3, 3.2, "bat", "spin"),
            Player("T Head", 8.5, 3.1, "bat", "spin"),
            Player("I Kishan", 8.6, 1.0, "bat", "spin"),
            Player("H Klaasen", 8.9, 1.0, "bat", "spin"),
            Player("N Reddy", 7.7, 5.2, "ar", "pace"), # F
            Player("L Livingstone", 6.9, 1.0, "bat", "spin"),
            Player("D Harsh", 5.2, 5.9, "ar", "spin"), # E
            Player("P Cummins", 3.0, 8.4, "bowl", "pace"), # A
            Player("P Harshal", 2.5, 7.7, "bowl", "pace"), # B
            Player("Z Ansari", 1.6, 7.3, "bowl", "spin"), # D
            Player("J Unadkat", 1.3, 7.4, "bowl", "pace"), # C
        ],

        "RCB": [
            Player("P Salt", 8.9, 0.9, "bat", "spin"),
            Player("V Kohli", 9.4, 2.1, "bat", "pace"),
            Player("V Iyer", 7.5, 1.0, "bat", "pace"),
            Player("R Patidar", 8.3, 1.0, "bat", "spin"),
            Player("S Jitesh", 7.7, 1.0, "bat", "spin"),
            Player("T David", 7.8, 3.9, "bat", "spin"),
            Player("P Krunal", 5.1, 8.2, "ar", "spin"), # C
            Player("K Bhuvneshwar", 3.2, 9.0, "bowl", "pace"), # B
            Player("J Hazlewood", 1.6, 9.0, "bowl", "pace"), # A
            Player("S Suyash", 1.2, 7.4, "bowl", "spin"), # D
            Player("Y Dayal", 1.0, 7.2, "bowl", "pace"), # E
        ],

        "RR": [
            Player("Y Jaiswal", 9.0, 1.0, "bat", "spin"),
            Player("V Sooryavanshi", 9.2, 1.0, "bat", "spin"),
            Player("S Hetmeyer", 7.5, 1.0, "bat", "spin"),
            Player("R Parag", 7.8, 3.8, "bat", "spin"),
            Player("D Jurel", 7.6, 1.0, "bat", "spin"),
            Player("R Jadeja", 7.0, 7.7, "ar", "spin"), # C
            Player("D Ferreira", 6.8, 5.1, "ar", "spin"), # F
            Player("S Curran", 4.6, 7.3, "ar", "pace"), # E
            Player("J Archer", 2.2, 9.2, "bowl", "pace"), # A
            Player("S Sandeep", 1.0, 7.8, "bowl", "pace"), # B
            Player("T Deshpande", 1.0, 7.6, "bowl", "pace"), # D
        ],

        "PBKS": [
            Player("S Prabhsimran", 8.0, 1.0, "bat", "spin"),
            Player("P Arya", 8.0, 0.9, "bat", "spin"),
            Player("S Iyer", 9.3, 2.0, "bat", "spin"),
            Player("N Wadhera", 7.7, 2.0, "bat", "spin"),
            Player("C Connolly", 7.6, 5.0, "ar", "spin"), # F
            Player("S Shashank", 7.8, 1.0, "bat", "spin"),
            Player("M Stoinis", 6.1, 5.6, "ar", "pace"), # E
            Player("M Jansen", 5.5, 7.5, "ar", "pace"), # D
            Player("H Brar", 2.6, 7.6, "bowl", "spin"), # C
            Player("S Arshdeep", 1.0, 9.0, "bowl", "pace"), # A
            Player("Y Chahal", 1.0, 8.7, "bowl", "spin"), # B
        ],

        "LSG": [
            Player("M Marsh", 8.2, 6.4, "ar", "pace"), # F
            Player("A Markram", 8.2, 4.0, "bat", "spin"),
            Player("N Pooran", 8.7, 1.0, "bat", "spin"),
            Player("R Pant", 7.9, 1.0, "bat", "spin"),
            Player("A Badoni", 7.5, 2.0, "bat", "spin"),
            Player("A Samad", 7.1, 2.0, "bat", "spin"),
            Player("W Hasaranga", 5.2, 7.5, "ar", "spin"), # E
            Player("R Digvesh", 2.0, 7.9, "bowl", "spin"), # B
            Player("Y Mayank", 1.0, 7.6, "bowl", "pace"), # D
            Player("K Avesh", 1.0, 7.7, "bowl", "pace"), # C
            Player("M Shami", 1.0, 7.9, "bowl", "pace"), # A
        ],

        "KKR": [
            Player("S Narine", 7.1, 9.2, "ar", "spin"), # A
            Player("F Allen", 7.5, 1.0, "bat", "spin"),
            Player("A Rahane", 7.7, 1.0, "bat", "spin"),
            Player("A Raghuvanshi", 8.2, 1.0, "bat", "spin"),
            Player("C Green", 7.8, 3.9, "ar", "pace"),
            Player("S Rinku", 8.2, 1.0, "bat", "spin"),
            Player("S Ramandeep", 7.6, 4.0, "ar", "pace"),
            Player("H Rana", 4.1, 8.0, "bowl", "pace"), # D
            Player("V Arora", 1.0, 7.7, "bowl", "pace"), # E
            Player("M Pathirana", 1.0, 8.4, "bowl", "pace"), # C
            Player("V Chakravarthy", 1.0, 9.1, "bowl", "spin"), # B
        ],

        "GT": [
            Player("S Sudarshan", 9.4, 1.0, "bat", "spin"),
            Player("S Gill", 9.3, 1.0, "bat", "spin"),
            Player("J Buttler", 9.1, 1.0, "bat", "spin"),
            Player("W Sundar", 6.8, 7.3, "ar", "spin"), # E
            Player("K Shahrukh", 7.1, 3.0, "bat", "spin"),
            Player("G Phillips", 7.2, 4.0, "bat", "spin"),
            Player("R Tewatia", 6.4, 6.0, "ar", "spin"), # F
            Player("K Rashid", 5.1, 9.4, "bowl", "spin"), # A
            Player("K Rabada", 2.2, 8.7, "bowl", "pace"), # B
            Player("K Prasidh", 1.0, 8.0, "bowl", "pace"), # D
            Player("M Siraj", 1.0, 8.3, "bowl", "pace"), # C
        ],

        "DC": [
            Player("K Rahul", 9.2, 1.0, "bat", "spin"),
            Player("B Duckett", 7.2, 1.0, "bat", "spin"),
            Player("N Rana", 7.5, 1.0, "bat", "spin"),
            Player("T Stubbs", 8.5, 3.0, "bat", "spin"),
            Player("S Ashutosh", 7.6, 2.0, "bat", "spin"),
            Player("D Miller", 8.2, 5.0, "bat", "spin"),
            Player("P Axar", 5.9, 7.9, "ar", "spin"), # C
            Player("N Auqib", 3.6, 7.0, "bowl", "pace"), # E
            Player("M Starc", 3.3, 8.5, "bowl", "pace"), # B
            Player("Y Kuldeep", 2.8, 8.9, "bowl", "spin"), # A
            Player("T Natarajan", 1.0, 7.8, "bowl", "pace"), # D
        ],
        # IPL 2016 Teams
        "MI16": [
            Player("PZ Parthiv", 7.2, 0.5, "bat", "spin"),
            Player("LZ Simmons", 7.9, 0.6, "bat", "spin"),
            Player("RZ Sharma", 8.7, 2.4, "bat", "spin"),
            Player("AZ Rayudu", 7.7, 1.8, "bat", "spin"),
            Player("KZ Pollard", 8.2, 5.2, "ar", "pace"),
            Player("HZ Pandya", 7.8, 6.9, "ar", "pace"),
            Player("KZ Pandya", 6.4, 7.1, "ar", "spin"),
            Player("SZ Harbhajan", 4.2, 8.1, "bowl", "spin"),
            Player("MZ McClenaghan", 2.1, 8.2, "bowl", "pace"),
            Player("JJ Bumrah", 1.8, 8.9, "bowl", "pace"),
            Player("LZ Malinga", 1.2, 8.9, "bowl", "pace"),
        ],

        "RCB16": [
            Player("VZ Kohli", 9.4, 1.2, "bat", "pace"),
            Player("CZ Gayle", 8.9, 0.8, "bat", "spin"),
            Player("AB de Villiers", 9.3, 1.4, "bat", "pace"),
            Player("SZ Watson", 7.8, 6.8, "ar", "pace"),
            Player("SZ Mandeep", 7.1, 0.9, "bat", "pace"),
            Player("SZ Khan", 6.9, 1.4, "bat", "spin"),
            Player("SZ Binny", 6.0, 6.2, "ar", "pace"),
            Player("IZ Abdulla", 4.8, 6.4, "bowl", "spin"),
            Player("SZ Aravind", 1.8, 7.6, "bowl", "pace"),
            Player("YZ Chahal", 1.4, 8.6, "bowl", "spin"),
            Player("CZ Jordan", 1.0, 7.2, "bowl", "pace"),
        ],

        "SRH16": [
            Player("DZ Warner", 9.3, 1.6, "bat", "spin"),
            Player("SZ Dhawan", 8.5, 0.8, "bat", "spin"),
            Player("KS Williamson", 8.7, 1.2, "bat", "spin"),
            Player("SZ Yuvraj", 7.9, 5.6, "ar", "spin"),
            Player("NZ Ojha", 7.0, 0.8, "bat", "spin"),
            Player("DZ Hooda", 6.8, 5.2, "ar", "spin"),
            Player("BZ Cutting", 6.1, 6.8, "ar", "pace"),
            Player("RZ Ashish", 5.3, 6.2, "ar", "pace"),
            Player("BZ Kumar", 2.4, 8.9, "bowl", "pace"),
            Player("MZ Rahman", 1.2, 8.4, "bowl", "pace"),
            Player("AZ Nehra", 1.6, 8.1, "bowl", "pace"),
        ],

        "KKR16": [
            Player("GZ Gambhir", 8.2, 1.4, "bat", "spin"),
            Player("RZ Uthappa", 7.8, 0.9, "bat", "pace"),
            Player("MZ Pandey", 7.5, 1.1, "bat", "spin"),
            Player("YK Pathan", 7.6, 5.4, "ar", "spin"),
            Player("SK Yadav", 7.4, 1.8, "bat", "spin"),
            Player("AZ Russell", 7.9, 7.0, "ar", "pace"),
            Player("SZ Narine", 6.5, 8.7, "bowl", "spin"),
            Player("CZ Woakes", 3.4, 7.2, "bowl", "pace"),
            Player("PZ Chawla", 2.8, 8.1, "bowl", "spin"),
            Player("UZ Yadav", 1.2, 7.9, "bowl", "pace"),
            Player("MZ Morkel", 1.8, 8.5, "bowl", "pace"),
        ],

        "DD16": [
            Player("QZ de Kock", 8.1, 0.7, "bat", "spin"),
            Player("KZ Nair", 7.0, 1.2, "bat", "spin"),
            Player("SZ Iyer", 8.1, 2.2, "bat", "spin"),
            Player("JP Duminy", 7.5, 5.8, "ar", "spin"),
            Player("RZ Pant", 7.8, 0.6, "bat", "spin"),
            Player("AZ Mayank", 6.9, 0.8, "bat", "spin"),
            Player("CZ Brathwaite", 7.1, 7.1, "ar", "pace"),
            Player("CM Morris", 5.9, 7.2, "ar", "pace"),
            Player("AZ Mishra", 2.2, 8.5, "bowl", "spin"),
            Player("MZ Shami", 1.8, 7.8, "bowl", "pace"),
            Player("ZZ Khan", 1.4, 8.4, "bowl", "pace"),
        ],

        "KXIP16": [
            Player("MZ Vijay", 7.5, 0.9, "bat", "spin"),
            Player("MZ Vohra", 7.3, 0.7, "bat", "spin"),
            Player("SZ Gurkareet", 7.0, 0.5, "bat", "spin"),
            Player("MZ Marsh", 7.2, 7.1, "ar", "pace"),
            Player("GJ Maxwell", 8.1, 6.2, "ar", "spin"),
            Player("DA Miller", 8.4, 1.4, "bat", "spin"),
            Player("AZ Patel", 4.8, 7.6, "ar", "spin"),
            Player("MG Johnson", 3.7, 7.9, "bowl", "pace"),
            Player("KZ Abbott", 1.8, 7.4, "bowl", "pace"),
            Player("SZ Sharma", 1.6, 8.0, "bowl", "pace"),
            Player("SZ Mohit", 1.2, 7.6, "bowl", "pace"),
        ],

        "GL16": [
            Player("BB McCullum", 8.3, 0.8, "bat", "spin"),
            Player("DR Smith", 8.0, 1.2, "bat", "pace"),
            Player("SZ Raina", 8.4, 5.6, "ar", "spin"),
            Player("AJ Finch", 7.1, 0.9, "bat", "spin"),
            Player("DM Bravo", 6.8, 1.3, "bat", "spin"),
            Player("DJ Bravo", 6.9, 8.4, "ar", "pace"),
            Player("RA Jadeja", 6.8, 7.8, "ar", "spin"),
            Player("JZ Faulkner", 6.2, 7.4, "ar", "pace"),
            Player("SZ Tye", 1.8, 8.2, "bowl", "pace"),
            Player("PJ Sangwan", 1.4, 7.2, "bowl", "pace"),
            Player("DS Kulkarni", 1.2, 8.0, "bowl", "pace"),
        ],

        "RPS16": [
            Player("GZ Bailey", 7.1, 0.8, "bat", "spin"),
            Player("FZ du Plessis", 8.0, 1.1, "bat", "spin"),
            Player("AM Rahane", 8.1, 1.2, "bat", "spin"),
            Player("SZ Smith", 8.2, 2.4, "bat", "spin"),
            Player("MS Dhoni", 8.2, 0.9, "bat", "pace"),
            Player("AL Menaria", 6.5, 5.2, "ar", "spin"),
            Player("RZ Bhatia", 5.8, 6.8, "ar", "pace"),
            Player("RZ Ashwin", 3.6, 8.3, "bowl", "spin"),
            Player("AZ Zampa", 1.2, 8.2, "bowl", "spin"),
            Player("AB Dinda", 1.4, 7.4, "bowl", "pace"),
            Player("IZ Sharma", 1.2, 7.8, "bowl", "pace"),
        ],

        # T20 World Cup 2024 Teams
        "AFG": [
            Player("R. Gurbaz", 8.2, 2.0, "bat", "spin"),
            Player("H. Zazai", 7.5, 2.0, "bat", "spin"),
            Player("I. Zadran", 7.8, 2.0, "bat", "spin"),
            Player("N. Zadran", 7.2, 2.0, "bat", "spin"),
            Player("K. Janat", 6.8, 6.5, "ar", "pace"), # G
            Player("A. Omarzai", 7.4, 7.5, "ar", "pace"), # F
            Player("M. Nabi", 7.0, 7.9, "ar", "spin"), # E
            Player("R. Khan", 5.3, 9.0, "bowl", "spin"), # A
            Player("F. Farooqi", 2.0, 8.0, "bowl", "pace"), # C
            Player("N. Haq", 1.5, 7.8, "bowl", "pace"),# D
            Player("N. Ahmad", 1.3, 8.4, "bowl", "spin"), # B
            # Player("F. Ahmad", 5.5, 7.5),
            # Player("N. Kharote", 5.0, 5.5),
            # Player("M. Ishaq", 6.5, 2.0),
            # Player("G. Naib", 6.5, 6.0),
        ],

        "AUS": [
            Player("T. Head", 9.0, 2.0, "bat", "spin"),
            Player("D. Warner", 8.8, 2.5, "bat", "spin"),
            Player("M. Marsh", 7.9, 5.0, "ar", "pace"), # G
            Player("M. Wade", 7.7, 2.0, "bat", "spin"),
            Player("G. Maxwell", 8.2, 5.8, "ar", "spin"), # F
            Player("T. David", 8.3, 2.0, "bat", "spin"),
            Player("M. Stoinis", 6.1, 5.9, "ar", "pace"), # E
            Player("P. Cummins", 3.9, 8.3, "bowl", "pace"), # D
            Player("M. Starc", 2.6, 8.8, "bowl", "pace"), # A
            Player("J. Hazlewood", 1.5, 8.7, "bowl", "pace"), # B
            Player("A. Zampa", 1.0, 8.5, "bowl", "spin"), # C
            # Player("N. Ellis", 4.0, 8.0),
            # Player("C. Green", 7.2, 4.5),
            # Player("A. Agar", 6.5, 7.5),
            # Player("J. Inglis", 7.5, 2.0),
        ],

        "BAN": [
            Player("N. Shanto", 7.6, 2.0, "bat", "spin"),
            Player("L. Das", 7.6, 2.0, "bat", "spin"),
            Player("T. Hridoy", 7.3, 2.0, "bat", "spin"),
            Player("S. Hasan", 7.2, 8.2, "ar", "spin"), # B
            Player("S. Sarkar", 7.1, 2.5, "bat", "pace"),
            Player("J. Ali", 6.9, 2.0, "bat", "spin"),
            Player("M. Hasan", 6.5, 7.1, "ar", "spin"), # F
            Player("T. Ahmed", 1.5, 7.8, "bowl", "pace"), # C
            Player("S. Islam", 1.5, 7.2, "bowl", "pace"), # E
            Player("T. Sakib", 1.4, 7.3, "bowl", "pace"), # D
            Player("M. Rahman", 1.0, 8.3, "bowl", "pace"), # A
            # Player("R. Hossain", 2.5, 7.8),
            # Player("T. Islam", 5.0, 7.5),
            # Player("M. Mahmudullah", 6.8, 3.0),
            # Player("T. Hasan", 6.5, 2.0),
        ],

        "CAN": [
            Player("A. Johnson", 6.0, 2.0, "bat", "spin"),
            Player("N. Dhaliwal", 6.5, 2.0, "bat", "spin"),
            Player("P. Singh", 5.5, 5.0, "ar", "spin"), # F
            Player("D. Bajwa", 6.0, 3.0, "bat", "spin"),
            Player("N. Kirton", 6.5, 2.0, "bat", "spin"),
            Player("S. Movva", 6.5, 2.0, "bat", "spin"),
            Player("J. Siddiqui", 5.5, 6.4, "ar", "spin"), # B
            Player("D. Heyliger", 1.5, 5.6, "bowl", "pace"), # E
            Player("S. Zafar", 1.7, 6.3, "bowl", "spin"), # C
            Player("K. Sana", 1.5, 6.2, "bowl", "pace"), # D
            Player("J. Gordon", 1.3, 6.5, "bowl", "pace"), # A
            # Player("R. Singh", 6.0, 2.0),
            # Player("R. Pathan", 6.0, 5.0),
            # Player("N. Dutta", 1.1, 6.1),
            # Player("R. Joshi", 1.0, 6.0),
        ],

        "ENG": [
            Player("P. Salt", 8.7, 2.0, "bat", "spin"),
            Player("J. Bairstow", 8.3, 2.0, "bat", "spin"),
            Player("J. Buttler", 9.2, 2.0, "bat", "spin"),
            Player("H. Brook", 8.3, 2.0, "bat", "spin"),
            Player("W. Jacks", 8.0, 6.0, "ar", "spin"), # G
            Player("L. Livingstone", 7.7, 6.8, "ar", "spin"), # F
            Player("M. Ali", 6.5, 7.8, "ar", "spin"), # D
            Player("S. Curran", 6.4, 7.7, "ar", "pace"), # E
            Player("J. Archer", 2.3, 8.8, "bowl", "pace"), # A
            Player("M. Wood", 1.5, 8.2, "bowl", "pace"), # B
            Player("A. Rashid", 1.5, 8.0, "bowl", "spin"), # C
            # Player("C. Jordan", 1.5, 8.1),
            # Player("R. Topley", 1.0, 8.0),
            # Player("T. Hartley", 1.0, 7.7),
            # Player("B. Duckett", 7.9, 2.0),
        ],

        "IND": [
            Player("R. Sharma", 8.3, 2.0, "bat", "spin"),
            Player("Y. Jaiswal", 8.4, 2.0, "bat", "spin"),
            Player("V. Kohli", 8.9, 2.0, "bat", "pace"),
            Player("S. Yadav", 8.7, 2.0, "bat", "spin"),
            Player("R. Pant", 8.0, 2.0, "bat", "spin"),
            Player("H. Pandya", 8.2, 7.8, "ar", "pace"), # E
            Player("S. Dube", 7.9, 6.0, "ar", "pace"), # F
            Player("A. Patel", 6.8, 8.0, "ar", "spin"), # D
            Player("K. Yadav", 2.5, 9.0, "bowl", "spin"), # B
            Player("J. Bumrah", 1.0, 9.4, "bowl", "pace"), # A
            Player("A. Singh", 1.0, 8.6, "bowl", "pace"), # C
            # Player("S. Samson", 8.4, 2.0),
            # Player("M. Siraj", 1.0, 8.2),
            # Player("Y. Chahal", 1.0, 8.2),
            # Player("R. Jadeja", 7.1, 7.9), # F
        ],

        "IRE": [
            Player("A. Balbirnie", 7.1, 2.0, "bat", "spin"),
            Player("P. Stirling", 7.2, 5.2, "ar", "spin"), # H
            Player("L. Tucker", 7.1, 2.0, "bat", "spin"),
            Player("H. Tector", 6.9, 5.6, "ar", "spin"), # G
            Player("C. Campher", 6.4, 5.9, "ar", "pace"), # F
            Player("G. Dockrell", 6.3, 7.0, "ar", "spin"), # C
            Player("G. Delany", 6.4, 6.3, "ar", "spin"), # E
            Player("R. Adair", 6.0, 2.0, "bat", "spin"),
            Player("M. Adair", 4.4, 7.6, "bowl", "pace"), # A
            Player("J. Little", 1.0, 7.3, "bowl", "pace"), # B
            Player("C. Young", 1.5, 6.8, "bowl", "pace"), # D
            # Player("B. McCarthy", 2.6, 6.0),
            # Player("B. White", 1.0, 6.4),
            # Player("G. Hume", 4.5, 5.5),
            # Player("N. Rock", 5.1, 2.0),
        ],

        "NAM": [
            Player("M. van Lingen", 6.5, 3.0, "bat", "pace"),
            Player("N. Davin", 6.1, 2.0, "bat", "spin"), # G
            Player("G. Erasmus", 7.8, 4.0, "ar", "spin"), # G (wait, need to check)
            Player("J. Smit", 7.1, 7.8, "ar", "pace"), # A
            Player("D. Wiese", 7.2, 6.6, "ar", "pace"), # D
            Player("J. Frylinck", 6.4, 7.0, "ar", "pace"), # B
            Player("Z. Green", 6.5, 2.0, "bat", "spin"),
            Player("M. Kruger", 6.0, 2.0, "bat", "spin"),
            Player("D. Leicher", 5.8, 5.0, "ar", "spin"), # F
            Player("R. Trumpelmann", 1.0, 6.9, "bowl", "pace"), # C
            Player("T. Lungameni", 1.0, 6.2, "bowl", "pace"), # E
            # Player("B. Scholtz", 1.0, 6.1),
            # Player("J. Kotze", 6.5, 1.0),
            # Player("P. Blignaut", 5.1, 1.0),
            # Player("B. Shikongo", 1.5, 7.0),
        ],

        "NEP": [
            Player("K. Bhurtel", 6.6, 2.0, "bat", "spin"),
            Player("A. Sheikh", 6.2, 2.0, "bat", "spin"),
            Player("R. Paudel", 6.5, 5.0, "ar", "spin"),
            Player("DS. Airee", 7.9, 7.7, "ar", "spin"), # B
            Player("K. Malla", 6.3, 4.0, "ar", "spin"),
            Player("G. Jha", 6.1, 6.5, "ar", "pace"), # D
            Player("K. KC", 5.5, 6.5, "ar", "pace"), # E
            Player("S. Kami", 5.0, 6.5, "ar", "pace"), # F
            Player("L. Rajbanshi", 1.5, 6.2, "bowl", "spin"), # G
            Player("A. Bohara", 1.0, 7.0, "bowl", "pace"), # C
            Player("S. Lamichhane", 1.0, 8.0, "bowl", "spin"), # A
            # Player("KS. Airee", 5.2, 5.7),
            # Player("S. Jora", 5.6, 2.0),
            # Player("S. Dhakal", 1.5, 5.2),
            # Player("A. Sah", 5.5, 2.0),
        ],

        "NED": [
            Player("M. Levitt", 6.8, 2.0, "bat", "spin"),
            Player("M. O'Dowd", 7.0, 2.0, "bat", "spin"),
            Player("V. Singh", 6.2, 2.0, "bat", "spin"),
            Player("S. Engelbrecht", 5.7, 4.0, "bat", "spin"), # F
            Player("B. de Leede", 6.9, 6.3, "ar", "pace"), # D
            Player("S. Edwards", 6.5, 2.0, "bat", "spin"),
            Player("T. Nidamanuru", 5.2, 2.0, "bat", "spin"), # G
            Player("L. van Beek", 2.6, 6.8, "bowl", "pace"), # B
            Player("T. Pringle", 3.0, 6.3, "bowl", "spin"), # E
            Player("P. van Meekeren", 2.1, 7.5, "bowl", "pace"), # A
            Player("V. Kingma", 1.0, 6.7, "bowl", "pace"), # C
            # Player("W. Barresi", 6.7, 2.0),
            # Player("S. Zulfiqar", 4.2, 5.5),
            # Player("A. Dutt", 1.4, 6.0),
            # Player("K. Klein", 1.0, 7.8),
        ],

        "NZL": [
            Player("F. Allen", 8.6, 2.0, "bat", "spin"),
            Player("D. Conway", 8.4, 2.0, "bat", "spin"),
            Player("R. Ravindra", 8.2, 5.5, "ar", "spin"), # G
            Player("K. Williamson", 8.4, 2.0, "bat", "spin"),
            Player("D. Mitchell", 8.2, 2.0, "bat", "pace"),
            Player("G. Phillips", 8.3, 6.3, "ar", "spin"), # F
            Player("M. Santner", 6.1, 7.8, "ar", "spin"), # E
            Player("L. Ferguson", 3.5, 8.1, "bowl", "pace"), # D
            Player("T. Boult", 2.0, 8.9, "bowl", "pace"), # A
            Player("I. Sodhi", 1.0, 8.0, "bowl", "spin"), # C
            Player("T. Southee", 1.0, 8.5, "bowl", "pace"), # B
            # Player("J. Neesham", 7.2, 6.8),
            # Player("M. Chapman", 7.8, 2.0),
            # Player("M. Bracewell", 7.7, 6.1),
            # Player("M. Henry", 1.0, 7.9),
        ],

        "OMN": [
            Player("N. Khushi", 5.8, 1.0, "bat", "spin"),
            Player("P. Athavale", 6.1, 1.0, "bat", "spin"),
            Player("A. Ilyas", 6.6, 6.9, "ar", "spin"), # B
            Player("Z. Maqsood", 6.7, 6.4, "ar", "spin"), # C
            Player("M. Nadeem", 6.0, 5.8, "ar", "pace"), # F
            Player("K. Kail", 5.8, 2.0, "bat", "spin"),
            Player("K. Prajapati", 5.7, 2.5, "bat", "spin"),
            Player("A. Khan", 5.6, 4.2, "ar", "spin"), # G
            Player("M. Khan", 5.2, 6.1, "ar", "spin"), # D
            Player("K. Kaleemullah", 4.0, 6.0, "bowl", "pace"), # E
            Player("B. Khan", 1.5, 7.8, "bowl", "pace"), # A
            # Player("S. Ahmed", 3.0, 6.0),
            # Player("S. Khan", 5.6, 3.0),
            # Player("R. Rafiullah", 5.1, 5.2),
            # Player("F. Butt", 2.2, 6.2),
        ],

        "PAK": [
            Player("B. Azam", 8.3, 2.0, "bat", "spin"),
            Player("I. Ahmed", 7.4, 2.0, "bat", "spin"),
            Player("F. Zaman", 8.3, 2.0, "bat", "spin"),
            Player("M. Rizwan", 8.4, 2.0, "bat", "spin"),
            Player("S. Ayub", 7.5, 2.0, "bat", "spin"),
            Player("I. Wasim", 6.3, 7.2, "ar", "spin"), # F
            Player("A. Ahmed", 4.0, 7.6, "bowl", "spin"), # E
            Player("H. Rauf", 1.0, 8.2, "bowl", "pace"), # D
            Player("M. Amir", 1.0, 8.5, "bowl", "pace"), # B
            Player("N. Shah", 1.0, 8.3, "bowl", "pace"), # C
            Player("S. Afridi", 1.2, 8.8, "bowl", "pace"), # A
            # Player("S. Khan", 6.5, 7.0),
            # Player("U. Khan", 7.0, 2.0),
            # Player("A. Afridi", 3.6, 6.5),
            # Player("A. Khan", 6.9, 2.0),
        ],

        "PNG": [
            Player("T. Ura", 7.4, 1.0, "bat", "spin"),
            Player("S. Bau", 6.5, 1.0, "bat", "spin"),
            Player("A. Vala", 7.2, 6.1, "ar", "spin"), # F
            Player("L. Siaka", 6.3, 2.0, "bat", "spin"),
            Player("H. Hiri", 5.5, 2.0, "bat", "pace"), # G
            Player("C. Amini", 6.8, 6.3, "ar", "spin"), # E
            Player("K. Doriga", 5.4, 2.0, "bat", "spin"),
            Player("A. Nao", 1.5, 6.6, "bowl", "pace"), # B
            Player("C. Soper", 1.0, 7.1, "bowl", "pace"), # A
            Player("K. Morea", 1.0, 6.5, "bowl", "pace"), # D
            Player("J. Kariko", 1.0, 6.5, "bowl", "pace"), # C
            # Player("H. Vare", 5.5, 6.0),
            # Player("J. Gardner", 5.0, 6.5),
            # Player("S. Kamea", 4.5, 6.0),
            # Player("N. Vanua", 5.5, 5.5),
        ],

        "SCO": [
            Player("G. Munsey", 7.6, 2.0, "bat", "spin"),
            Player("M. Jones", 6.6, 2.0, "bat", "spin"),
            Player("B. McMullen", 7.2, 5.1, "ar", "pace"), # G
            Player("R. Berrington", 7.3, 2.0, "bat", "pace"),
            Player("M. Leask", 6.6, 6.5, "ar", "spin"), # D
            Player("M. Cross", 6.6, 2.0, "bat", "spin"),
            Player("C. Greaves", 5.4, 6.4, "ar", "spin"), # E
            Player("M. Watt", 4.0, 7.5, "bowl", "spin"), # B
            Player("S. Sharif", 3.8, 6.9, "bowl", "pace"), # C
            Player("B. Wheal", 1.8, 6.2, "bowl", "pace"), # F
            Player("B. Currie", 1.0, 7.7, "bowl", "pace"), # A
            # Player("O. Hairs", 6.0, 1.0),
            # Player("C. Tear", 5.0, 1.0),
            # Player("J. Jarvis", 4.8, 5.7),
            # Player("C. Sole", 1.0, 6.1),
        ],

        "RSA": [
            Player("Q. de Kock", 8.4, 2.0, "bat", "spin"),
            Player("A. Markram", 8.7, 2.0, "bat", "spin"),
            Player("R. Rickelton", 8.1, 2.0, "bat", "spin"),
            Player("H. Klaasen", 9.0, 2.0, "bat", "spin"),
            Player("T. Stubbs", 8.6, 3.8, "bat", "spin"),
            Player("D. Miller", 8.5, 2.0, "bat", "spin"),
            Player("M. Jansen", 5.3, 8.2, "ar", "pace"), # D
            Player("A. Nortje", 1.2, 8.6, "bowl", "pace"), # B
            Player("K. Rabada", 1.2, 8.9, "bowl", "pace"), # A
            Player("K. Maharaj", 1.0, 8.3, "bowl", "spin"), # C
            Player("T. Shamsi", 1.0, 8.2, "bowl", "spin"), # E
            # Player("G. Coetzee", 1.0, 8.3),
            # Player("O. Baartman", 3.5, 7.5),
            # Player("B. Fortuin", 3.0, 7.6),
            # Player("R. Hendricks", 7.6, 2.0),
        ],

        "SRL": [
            Player("P. Nissanka", 8.4, 2.0, "bat", "spin"),
            Player("K. Mendis", 8.2, 2.0, "bat", "spin"),
            Player("KA. Mendis", 7.2, 5.0, "ar", "spin"),
            Player("C. Asalanka", 7.6, 4.8, "bat", "spin"),
            Player("A. Mathews", 7.7, 7.0, "ar", "pace"), # E
            Player("D. Shanaka", 7.6, 6.5, "ar", "pace"), # F
            Player("D. de Silva", 7.4, 5.4, "ar", "spin"),
            Player("W. Hasaranga", 6.0, 8.5, "ar", "spin"), # A
            Player("M. Theekshana", 1.0, 8.2, "bowl", "spin"), # B
            Player("N. Thushara", 1.0, 7.9, "bowl", "pace"), # D
            Player("M. Pathirana", 1.0, 8.1, "bowl", "pace"), # C
            # Player("D. Chameera", 1.5, 7.8),
            # Player("D. Madushanka", 1.5, 7.5),
            # Player("D. Wellalage", 1.5, 7.8),
            # Player("S. Samarawickrama", 7.0, 2.0),
        ],

        "UGA": [
            Player("S. Ssesazi", 6.4, 2.0, "bat", "spin"),
            Player("R. Mukasa", 6.3, 2.0, "bat", "spin"),
            Player("R. Obuya", 6.0, 3.5, "bat", "spin"),
            Player("D. Nakrani", 6.1, 4.5, "ar", "pace"), # G
            Player("R. Shah", 6.7, 2.0, "bat", "spin"),
            Player("A. Ramjani", 6.2, 7.4, "ar", "spin"), # A
            Player("K. Waiswa", 5.3, 6.2, "ar", "pace"), # F
            Player("B. Masaba", 1.0, 6.5, "bowl", "spin"), # C
            Player("F. Nsubuga", 1.0, 7.2, "bowl", "spin"), # B
            Player("J. Miyagi", 1.0, 6.4, "bowl", "pace"), # D
            Player("C. Kyewuta", 1.0, 6.3, "bowl", "pace"), # E
            # Player("F. Achelam", 6.0, 2.0),
            # Player("B. Hassan", 1.5, 7.0),
            # Player("R. Patel", 6.5, 2.0),
            # Player("H. Ssenyondo", 1.5, 5.0),
        ],

        "USA": [
            Player("S. Taylor", 6.4, 5.0, "ar", "spin"), # G
            Player("M. Patel", 6.8, 2.0, "bat", "spin"),
            Player("A. Gous", 7.3, 2.0, "bat", "spin"),
            Player("A. Jones", 7.0, 2.0, "bat", "spin"),
            Player("N. Kumar", 6.7, 2.0, "bat", "spin"),
            Player("C. Anderson", 7.8, 7.0, "ar", "pace"), # D
            Player("H. Singh", 5.5, 7.4, "ar", "spin"), # B
            Player("J. Singh", 4.5, 6.9, "bowl", "pace"), # E
            Player("N. Kenjige", 4.0, 7.2, "bowl", "spin"), # C
            Player("S. Netravalkar", 4.5, 7.5, "bowl", "pace"), # A
            Player("S. van Schalkwyk", 5.0, 6.9, "ar", "pace"), # F
            # Player("A. Khan", 4.5, 6.3),
            # Player("S. Jahangir", 6.8, 2.0),
            # Player("M. Kumar", 5.0, 5.5),
            # Player("N. Patel", 5.5, 5.0),
        ],

        "WI": [
            Player("B. King", 7.9, 2.5, "bat", "spin"),
            Player("S. Hope", 7.9, 2.0, "bat", "spin"),
            Player("S. Hetmyer", 8.0, 2.0, "bat", "spin"),
            Player("N. Pooran", 8.6, 2.0, "bat", "spin"),
            Player("R. Powell", 7.6, 3.0, "bat", "pace"),
            Player("A. Russell", 7.9, 6.5, "ar", "pace"), # E
            Player("S. Rutherford", 7.7, 4.8, "bat", "pace"),
            Player("R. Shepherd", 7.4, 6.9, "ar", "pace"), # D
            Player("A. Hosein", 3.1, 8.0, "bowl", "spin"), # A
            Player("G. Motie", 2.3, 7.8, "bowl", "spin"), # B
            Player("A. Joseph", 1.5, 7.7, "bowl", "pace"), # C
            # Player("O. McCoy", 1.0, 7.5),
            # Player("J. Charles", 7.3, 2.0),
            # Player("R. Chase", 6.5, 7.0),
            # Player("S. Joseph", 1.0, 7.1),
        ],
    }


# Custom bowling orders for each team
# Format: 20-character string where A=best bowler, B=2nd best, C=3rd, etc.
# Bowlers are ranked by bowling skill (DESC), then alphabetically by name for ties.
# Default pattern if not specified: "ABABCDECDECDECDEABAB" (uses top 5 bowlers)
# Example: "ABCDABCDABCDABCDABCD" - rotates through top 4 bowlers evenly
BOWLING_ORDERS = {
    # IPL Teams
    "MI": "CACBCACDFDEBDFDEABAB",
    "CSK": "BDCBDCAEAFDAEAEDBCBC",
    "SRH": "ABACACDEDEBDFDECBCBA",
    "RCB": "BABACEDECDCDCEDEBABA",
    "RR": "DBADBACECECDCDEBEABA",
    "PBKS": "DADAEDBCBCEBCFBCEADA",
    "LSG": "DCADCFABEBECDBEBADAC",
    "KKR": "DECDEABABABDABECDCEC",
    "GT": "CBDCBDAEAECAEAEDBCBD",
    "DC": "EBEBECDEACACACADBDBD",
    # IPL 2016 Teams
    "MI16": "ABABCDECDECDECDEABAB",
    "RCB16": "ABABCDECDECDECDEABAB",
    "SRH16": "ABABCDECDECDECDEABAB",
    "KKR16": "ABABCDECDECDECDEABAB",
    "DD16": "ABABCDECDECDECDEABAB",
    "KXIP16": "ABABCDECDECDECDEABAB",
    "GL16": "ABABCDECDECDECDEABAB",
    "RPS16": "ABABCDECDECDECDEABAB",
    # T20 World Cup Teams
    "AFG": "DCDCDABEABEABEABFCDC",
    "AUS": "BABDBAECDCFECDCFADAB",
    "BAN": "ACADCEBFBFCDBEBDACAD",
    "CAN": "ABABCDECDECDECDEABAB",
    "ENG": "BABABECDCDECDCDEABAE",
    "IND": "CAEACEBDBDEBDBDEACAC",
    "IRE": "ABABCDECDECDECDEABAB",
    "NAM": "ABABCDECDECDECDEABAB",
    "NEP": "ABABCDECDECDECDEABAB",
    "NED": "ABABCDECDECDECDEABAB",
    "NZL": "ABADBDECECDECECDABAB",
    "OMN": "ABABCDECDECDECDEABAB",
    "PAK": "BCABCDAEFECDECEDBABA",
    "PNG": "ABABCDECDECDECDEABAB",
    "SCO": "ABABCDECDECDECDEABAB",
    "RSA": "BABDADCECEDCECEDBABA",
    "SRL": "CDCDEABABEABABFEDCDC",
    "UGA": "ABABCDECDECDECDEABAB",
    "USA": "ABABCDECDECDECDEABAB",
    "WI": "CDCDEABEABEABEABDCDC",
}


def get_bowling_orders():
    """Return the custom bowling orders dictionary."""
    return BOWLING_ORDERS


def get_bowling_order(team_name):
    """Get the bowling order for a specific team, or None if not customized."""
    return BOWLING_ORDERS.get(team_name)


def get_player(name):
    """Look up a Player by name across all squads (names are unique). None if unknown."""
    for squad in get_teams().values():
        for player in squad:
            if player.name == name:
                return player
    return None


def get_bowler_ranking(team):
    """
    Rank bowlers by bowling skill (DESC), then alphabetically by name for ties.
    Returns a dict mapping letter (A, B, C, ...) to Player object.
    A = best bowler, B = 2nd best, etc.
    """
    # Sort by bowling skill DESC, then by name ASC for ties
    sorted_bowlers = sorted(team, key=lambda p: (-p.bowling, p.name))
    ranking = {}
    for i, player in enumerate(sorted_bowlers):
        letter = chr(ord('A') + i)
        ranking[letter] = player
    return ranking



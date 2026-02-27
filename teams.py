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
        ],

        # T20 World Cup 2024 Teams
        "AFG": [
            Player("R. Gurbaz", 8.2, 2.0),
            Player("H. Zazai", 7.5, 2.0),
            Player("I. Zadran", 7.8, 2.0),
            Player("N. Zadran", 7.2, 2.0),
            Player("K. Janat", 6.8, 6.5),
            Player("A. Omarzai", 7.4, 7.5),
            Player("M. Nabi", 7.0, 7.7),
            Player("R. Khan", 6.0, 9.3),
            Player("F. Farooqi", 2.0, 8.0),
            Player("N. Haq", 1.5, 7.8),
            Player("N. Ahmad", 1.3, 8.0),
            # Player("F. Ahmad", 5.5, 7.5),
            # Player("N. Kharote", 5.0, 5.5),
            # Player("M. Ishaq", 6.5, 2.0),
            # Player("G. Naib", 6.5, 6.0),
        ],

        "AUS": [
            Player("T. Head", 9.0, 2.0),
            Player("D. Warner", 8.8, 2.5),
            Player("M. Marsh", 7.9, 5.0),
            Player("M. Wade", 7.8, 2.0),
            Player("G. Maxwell", 8.2, 6.1),
            Player("T. David", 8.3, 2.0),
            Player("M. Stoinis", 7.1, 6.2),
            Player("P. Cummins", 3.9, 8.3),
            Player("M. Starc", 2.6, 8.8),
            Player("J. Hazlewood", 1.5, 8.7),
            Player("A. Zampa", 1.0, 8.5),
            # Player("N. Ellis", 4.0, 8.0),
            # Player("C. Green", 7.2, 4.5),
            # Player("A. Agar", 6.5, 7.5),
            # Player("J. Inglis", 7.5, 2.0),
        ],

        "BAN": [
            Player("N. Shanto", 7.6, 2.0),
            Player("L. Das", 7.6, 2.0),
            Player("T. Hridoy", 7.3, 2.0),
            Player("S. Hasan", 7.2, 8.2),
            Player("S. Sarkar", 7.1, 2.5),
            Player("J. Ali", 6.9, 2.0),
            Player("M. Hasan", 6.5, 7.1),
            Player("T. Ahmed", 1.5, 7.8),
            Player("S. Islam", 1.5, 7.2),
            Player("T. Sakib", 1.4, 7.3),
            Player("M. Rahman", 1.0, 8.3),
            # Player("R. Hossain", 2.5, 7.8),
            # Player("T. Islam", 5.0, 7.5),
            # Player("M. Mahmudullah", 6.8, 3.0),
            # Player("T. Hasan", 6.5, 2.0),
        ],

        "CAN": [
            Player("A. Johnson", 6.0, 2.0),
            Player("N. Dhaliwal", 6.5, 2.0),
            Player("P. Singh", 5.5, 5.0),
            Player("D. Bajwa", 6.0, 3.0),
            Player("N. Kirton", 6.5, 2.0),
            Player("S. Movva", 6.5, 2.0),
            Player("J. Siddiqui", 5.5, 6.4),
            Player("D. Heyliger", 1.5, 5.6),
            Player("S. Zafar", 1.7, 6.3),
            Player("K. Sana", 1.5, 6.2),
            Player("J. Gordon", 1.3, 6.5),
            # Player("R. Singh", 6.0, 2.0),
            # Player("R. Pathan", 6.0, 5.0),
            # Player("N. Dutta", 1.1, 6.1),
            # Player("R. Joshi", 1.0, 6.0),
        ],

        "ENG": [
            Player("P. Salt", 8.7, 2.0),
            Player("J. Bairstow", 8.3, 2.0),
            Player("J. Buttler", 9.0, 2.0),
            Player("H. Brook", 8.3, 2.0),
            Player("W. Jacks", 8.0, 6.0),
            Player("L. Livingstone", 7.7, 6.8),
            Player("M. Ali", 6.5, 7.8),
            Player("S. Curran", 6.4, 7.7),
            Player("J. Archer", 2.3, 8.8),
            Player("M. Wood", 1.5, 8.2),
            Player("A. Rashid", 1.5, 8.0),
            # Player("C. Jordan", 1.5, 8.1),
            # Player("R. Topley", 1.0, 8.0),
            # Player("T. Hartley", 1.0, 7.7),
            # Player("B. Duckett", 7.9, 2.0),
        ],

        "IND": [
            Player("R. Sharma", 8.5, 2.0),
            Player("Y. Jaiswal", 8.7, 2.0),
            Player("V. Kohli", 9.1, 2.0),
            Player("S. Yadav", 8.9, 2.0),
            Player("R. Pant", 8.3, 2.0),
            Player("H. Pandya", 8.1, 8.0),
            Player("R. Jadeja", 7.1, 7.9),
            Player("A. Patel", 6.8, 8.0),
            Player("K. Yadav", 2.5, 9.0),
            Player("J. Bumrah", 1.0, 9.4),
            Player("A. Singh", 1.0, 8.6),
            # Player("S. Samson", 8.4, 2.0),
            # Player("M. Siraj", 1.0, 8.2),
            # Player("Y. Chahal", 1.0, 8.2),
            # Player("S. Dube", 7.9, 6.0),
        ],

        "IRE": [
            Player("A. Balbirnie", 7.1, 2.0),
            Player("P. Stirling", 7.2, 5.2),
            Player("L. Tucker", 7.1, 2.0),
            Player("H. Tector", 6.9, 5.6),
            Player("C. Campher", 6.4, 5.9),
            Player("G. Dockrell", 6.3, 7.0),
            Player("G. Delany", 6.4, 6.3),
            Player("R. Adair", 6.0, 2.0),
            Player("M. Adair", 4.4, 7.6),
            Player("J. Little", 1.0, 7.3),
            Player("C. Young", 1.5, 6.8),
            # Player("B. McCarthy", 2.6, 6.0),
            # Player("B. White", 1.0, 6.4),
            # Player("G. Hume", 4.5, 5.5),
            # Player("N. Rock", 5.1, 2.0),
        ],

        "NAM": [
            Player("M. van Lingen", 6.5, 3.0),
            Player("N. Davin", 6.1, 2.0),
            Player("G. Erasmus", 7.8, 4.0),
            Player("J. Smit", 7.1, 7.8),
            Player("D. Wiese", 7.2, 6.6),
            Player("J. Frylinck", 6.4, 7.0),
            Player("Z. Green", 6.5, 2.0),
            Player("M. Kruger", 6.0, 2.0),
            Player("D. Leicher", 5.8, 5.0),
            Player("R. Trumpelmann", 1.0, 6.9),
            Player("T. Lungameni", 1.0, 6.2),
            # Player("B. Scholtz", 1.0, 6.1),
            # Player("J. Kotze", 6.5, 1.0),
            # Player("P. Blignaut", 5.1, 1.0),
            # Player("B. Shikongo", 1.5, 7.0),
        ],

        "NEP": [
            Player("K. Bhurtel", 6.6, 2.0),
            Player("A. Sheikh", 6.2, 2.0),
            Player("R. Paudel", 6.5, 5.0),
            Player("DS. Airee", 7.9, 7.7),
            Player("K. Malla", 6.3, 4.0),
            Player("G. Jha", 6.1, 6.5),
            Player("K. KC", 5.5, 6.5),
            Player("S. Kami", 5.0, 6.5),
            Player("L. Rajbanshi", 1.5, 6.2),
            Player("A. Bohara", 1.0, 7.0),
            Player("S. Lamichhane", 1.0, 8.0),
            # Player("KS. Airee", 5.2, 5.7),
            # Player("S. Jora", 5.6, 2.0),
            # Player("S. Dhakal", 1.5, 5.2),
            # Player("A. Sah", 5.5, 2.0),
        ],

        "NED": [
            Player("M. Levitt", 6.8, 2.0),
            Player("M. O'Dowd", 7.0, 2.0),
            Player("V. Singh", 6.2, 2.0),
            Player("S. Engelbrecht", 5.7, 4.0),
            Player("B. de Leede", 6.9, 6.3),
            Player("S. Edwards", 6.5, 2.0),
            Player("T. Nidamanuru", 5.2, 2.0),
            Player("L. van Beek", 2.6, 6.8),
            Player("T. Pringle", 3.0, 6.3),
            Player("P. van Meekeren", 2.1, 7.5),
            Player("V. Kingma", 1.0, 6.7),
            # Player("W. Barresi", 6.7, 2.0),
            # Player("S. Zulfiqar", 4.2, 5.5),
            # Player("A. Dutt", 1.4, 6.0),
            # Player("K. Klein", 1.0, 7.8),
        ],

        "NZL": [
            Player("F. Allen", 8.3, 2.0),
            Player("D. Conway", 8.4, 2.0),
            Player("R. Ravindra", 8.2, 5.5),
            Player("K. Williamson", 8.4, 2.0),
            Player("D. Mitchell", 8.2, 2.0),
            Player("G. Phillips", 8.3, 6.3),
            Player("M. Santner", 6.1, 7.9),
            Player("L. Ferguson", 3.5, 8.1),
            Player("T. Boult", 2.0, 8.9),
            Player("I. Sodhi", 1.0, 8.1),
            Player("T. Southee", 1.0, 8.5),
            # Player("J. Neesham", 7.2, 6.8),
            # Player("M. Chapman", 7.8, 2.0),
            # Player("M. Bracewell", 7.7, 6.1),
            # Player("M. Henry", 1.0, 7.9),
        ],

        "OMN": [
            Player("N. Khushi", 5.8, 1.0),
            Player("P. Athavale", 6.1, 1.0),
            Player("A. Ilyas", 6.6, 6.9),
            Player("Z. Maqsood", 6.7, 6.4),
            Player("M. Nadeem", 6.0, 5.8),
            Player("K. Kail", 5.8, 2.0),
            Player("K. Prajapati", 5.7, 2.5),
            Player("A. Khan", 5.6, 4.2),
            Player("M. Khan", 5.2, 6.1),
            Player("K. Kaleemullah", 4.0, 6.0),
            Player("B. Khan", 1.5, 7.8),
            # Player("S. Ahmed", 3.0, 6.0),
            # Player("S. Khan", 5.6, 3.0),
            # Player("R. Rafiullah", 5.1, 5.2),
            # Player("F. Butt", 2.2, 6.2),
        ],

        "PAK": [
            Player("B. Azam", 8.3, 2.0),
            Player("I. Ahmed", 7.4, 2.0),
            Player("F. Zaman", 8.1, 2.0),
            Player("M. Rizwan", 8.1, 2.0),
            Player("S. Ayub", 7.5, 2.0),
            Player("I. Wasim", 6.3, 7.2),
            Player("A. Ahmed", 4.0, 7.6),
            Player("H. Rauf", 1.0, 8.2),
            Player("M. Amir", 1.0, 8.5),
            Player("N. Shah", 1.0, 8.3),
            Player("S. Afridi", 1.2, 8.8),
            # Player("S. Khan", 6.5, 7.0),
            # Player("U. Khan", 7.0, 2.0),
            # Player("A. Afridi", 3.6, 6.5),
            # Player("A. Khan", 6.9, 2.0),
        ],

        "PNG": [
            Player("T. Ura", 7.4, 1.0),
            Player("S. Bau", 6.5, 1.0),
            Player("A. Vala", 7.2, 6.1),
            Player("L. Siaka", 6.3, 2.0),
            Player("H. Hiri", 5.5, 2.0),
            Player("C. Amini", 6.8, 6.3),
            Player("K. Doriga", 5.4, 2.0),
            Player("A. Nao", 1.5, 6.6),
            Player("C. Soper", 1.0, 7.1),
            Player("K. Morea", 1.0, 6.5),
            Player("J. Kariko", 1.0, 6.5),
            # Player("H. Vare", 5.5, 6.0),
            # Player("J. Gardner", 5.0, 6.5),
            # Player("S. Kamea", 4.5, 6.0),
            # Player("N. Vanua", 5.5, 5.5),
        ],

        "SCO": [
            Player("G. Munsey", 7.6, 2.0),
            Player("M. Jones", 6.6, 2.0),
            Player("B. McMullen", 7.2, 5.1),
            Player("R. Berrington", 7.3, 2.0),
            Player("M. Leask", 6.6, 6.5),
            Player("M. Cross", 6.6, 2.0),
            Player("C. Greaves", 5.4, 6.4),
            Player("M. Watt", 4.0, 7.5),
            Player("S. Sharif", 3.8, 6.9),
            Player("B. Wheal", 1.8, 6.2),
            Player("B. Currie", 1.0, 7.7),
            # Player("O. Hairs", 6.0, 1.0),
            # Player("C. Tear", 5.0, 1.0),
            # Player("J. Jarvis", 4.8, 5.7),
            # Player("C. Sole", 1.0, 6.1),
        ],

        "RSA": [
            Player("Q. de Kock", 8.4, 2.0),
            Player("A. Markram", 8.5, 2.0),
            Player("R. Rickelton", 8.2, 2.0),
            Player("H. Klaasen", 9.0, 2.0),
            Player("T. Stubbs", 8.6, 5.5),
            Player("D. Miller", 8.5, 2.0),
            Player("M. Jansen", 6.3, 8.2),
            Player("A. Nortje", 1.2, 8.6),
            Player("K. Rabada", 1.2, 8.9),
            Player("K. Maharaj", 1.0, 8.2),
            Player("T. Shamsi", 1.0, 8.3),
            # Player("G. Coetzee", 1.0, 8.3),
            # Player("O. Baartman", 3.5, 7.5),
            # Player("B. Fortuin", 3.0, 7.6),
            # Player("R. Hendricks", 7.6, 2.0),
        ],

        "SRL": [
            Player("P. Nissanka", 8.4, 2.0),
            Player("K. Mendis", 8.2, 2.0),
            Player("KA. Mendis", 7.2, 5.0),
            Player("C. Asalanka", 7.6, 4.8),
            Player("A. Mathews", 7.7, 7.0),
            Player("D. Shanaka", 7.6, 6.5),
            Player("D. de Silva", 7.4, 5.4),
            Player("W. Hasaranga", 6.0, 8.5),
            Player("M. Theekshana", 1.0, 8.2),
            Player("N. Thushara", 1.0, 7.9),
            Player("M. Pathirana", 1.0, 8.1),
            # Player("D. Chameera", 1.5, 7.8),
            # Player("D. Madushanka", 1.5, 7.5),
            # Player("D. Wellalage", 1.5, 7.8),
            # Player("S. Samarawickrama", 7.0, 2.0),
        ],

        "UGA": [
            Player("S. Ssesazi", 6.4, 2.0),
            Player("R. Mukasa", 6.3, 2.0),
            Player("R. Obuya", 6.0, 3.5),
            Player("D. Nakrani", 6.1, 4.5),
            Player("R. Shah", 6.7, 2.0),
            Player("A. Ramjani", 6.2, 7.4),
            Player("K. Waiswa", 5.3, 6.2),
            Player("B. Masaba", 1.0, 6.5),
            Player("F. Nsubuga", 1.0, 7.2),
            Player("J. Miyagi", 1.0, 6.4),
            Player("C. Kyewuta", 1.0, 6.3),
            # Player("F. Achelam", 6.0, 2.0),
            # Player("B. Hassan", 1.5, 7.0),
            # Player("R. Patel", 6.5, 2.0),
            # Player("H. Ssenyondo", 1.5, 5.0),
        ],

        "USA": [
            Player("S. Taylor", 6.4, 5.0),
            Player("M. Patel", 6.8, 2.0),
            Player("A. Gous", 7.3, 2.0),
            Player("A. Jones", 7.0, 2.0),
            Player("N. Kumar", 6.7, 2.0),
            Player("C. Anderson", 7.8, 7.0),
            Player("H. Singh", 5.5, 7.4),
            Player("J. Singh", 4.5, 6.9),
            Player("N. Kenjige", 4.0, 7.2),
            Player("S. Netravalkar", 4.5, 7.5),
            Player("S. van Schalkwyk", 5.0, 6.9),
            # Player("A. Khan", 4.5, 6.3),
            # Player("S. Jahangir", 6.8, 2.0),
            # Player("M. Kumar", 5.0, 5.5),
            # Player("N. Patel", 5.5, 5.0),
        ],

        "WI": [
            Player("B. King", 8.1, 2.5),
            Player("S. Hope", 8.2, 2.0),
            Player("S. Hetmyer", 8.0, 2.0),
            Player("N. Pooran", 8.6, 2.0),
            Player("R. Powell", 7.7, 2.0),
            Player("A. Russell", 7.9, 6.5),
            Player("S. Rutherford", 7.7, 4.8),
            Player("R. Shepherd", 7.1, 6.9),
            Player("G. Motie", 4.3, 7.8),
            Player("A. Hosein", 2.1, 8.0),
            Player("A. Joseph", 2.5, 7.7),
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
    "MI": "ABABCDECDECDECDEABAB",
    "CSK": "ABABCDECDECDECDEABAB",
    "SRH": "ABABCDECDECDECDEABAB",
    "RCB": "ABABCDECDECDECDEABAB",
    "RR": "ABABCDECDECDECDEABAB",
    "PBKS": "ABABCDECDECDECDEABAB",
    "LSG": "ABABCDECDECDECDEABAB",
    "KKR": "ABABCDECDECDECDEABAB",
    "GT": "ABABCDECDECDECDEABAB",
    "DC": "ABABCDECDECDECDEABAB",
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
    "AFG": "ABABCDECDECDECDEABAB",
    "AUS": "ABABCDECDECDECDEABAB",
    "BAN": "ABABCDECDECDECDEABAB",
    "CAN": "ABABCDECDECDECDEABAB",
    "ENG": "ABABCDECDECDECDEABAB",
    "IND": "ABABCDECDECDECDEABAB",
    "IRE": "ABABCDECDECDECDEABAB",
    "NAM": "ABABCDECDECDECDEABAB",
    "NEP": "ABABCDECDECDECDEABAB",
    "NED": "ABABCDECDECDECDEABAB",
    "NZL": "ABABCDECDECDECDEABAB",
    "OMN": "ABABCDECDECDECDEABAB",
    "PAK": "ABABCDECDECDECDEABAB",
    "PNG": "ABABCDECDECDECDEABAB",
    "SCO": "ABABCDECDECDECDEABAB",
    "RSA": "ABABCDECDECDECDEABAB",
    "SRL": "ABABCDECDECDECDEABAB",
    "UGA": "ABABCDECDECDECDEABAB",
    "USA": "ABABCDECDECDECDEABAB",
    "WI": "ABABCDECDECDECDEABAB",
}


def get_bowling_orders():
    """Return the custom bowling orders dictionary."""
    return BOWLING_ORDERS


def get_bowling_order(team_name):
    """Get the bowling order for a specific team, or None if not customized."""
    return BOWLING_ORDERS.get(team_name)


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

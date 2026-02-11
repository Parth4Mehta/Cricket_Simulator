import os
import json

MATCH_DIR = os.path.join("database", "match_stats")


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def infer_and_write_results():
    if not os.path.exists(MATCH_DIR):
        print("No match_stats directory found.")
        return
    files = [f for f in os.listdir(MATCH_DIR) if f.lower().endswith('.json')]
    if not files:
        print("No match JSON files found.")
        return

    for fn in files:
        path = os.path.join(MATCH_DIR, fn)
        try:
            data = load_json(path)
        except Exception as e:
            print(f"Skipping {fn}: failed to read ({e})")
            continue

        if 'result' in data:
            print(f"{fn}: already has result, skipping")
            continue

        meta = data.get('meta', {})
        teamA = meta.get('teamA')
        teamB = meta.get('teamB')
        if not teamA or not teamB:
            print(f"{fn}: missing meta.teamA/teamB, skipping")
            continue

        A_section = data.get(teamA, {})
        B_section = data.get(teamB, {})
        A_bat = A_section.get('batting', [])
        B_bat = B_section.get('batting', [])

        A_score = sum((b.get('runs', 0) for b in A_bat))
        B_score = sum((b.get('runs', 0) for b in B_bat))

        # count wickets lost by counting dismissals not 'not out'
        def wickets_lost(bat_list):
            c = 0
            for b in bat_list:
                dis = b.get('dismissal', '')
                if isinstance(dis, str) and dis.strip().lower() != 'not out' and dis.strip() != '':
                    c += 1
            return c

        A_wk = wickets_lost(A_bat)
        B_wk = wickets_lost(B_bat)

        if A_score > B_score:
            winner = teamA
            margin = f"{A_score - B_score} runs"
        elif B_score > A_score:
            winner = teamB
            wickets_remaining = 10 - B_wk
            if wickets_remaining < 0:
                # fallback
                margin = f"{B_score - A_score} runs"
            else:
                margin = f"{wickets_remaining} wickets"
        else:
            winner = "TIE"
            margin = ""

        result = {"winner": winner, "by": margin, "A_score": A_score, "B_score": B_score}
        data['result'] = result
        try:
            save_json(path, data)
            print(f"Updated {fn} with result: {result}")
        except Exception as e:
            print(f"Failed to update {fn}: {e}")


if __name__ == '__main__':
    infer_and_write_results()

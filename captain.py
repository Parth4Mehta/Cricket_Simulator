"""
captain.py

Live choices: the user makes the captain's calls for both sides of a match.

- Toss: the toss winner's bat/bowl decision.
- Batting: the openers before an innings, and the next batter at each wicket.
- Bowling: the bowler for every over. The team's normal bowling order is the
  default, so pressing Enter keeps it.

Every prompt accepts Enter (keep the default) and "auto" (play the rest of
this innings automatically). It is a whole word because single letters pick
bowlers (A = best bowler). The simulation enforces the bowling rules itself
(4 overs max, no two overs in a row), so this module only offers legal options
and never has the final say on legality.
"""
import builtins

AUTO = "auto"


class LiveCaptain:
    def __init__(self, input_fn=None, print_fn=None):
        # Look up input/print at call time so a patched input() (tests) is used.
        self._input = input_fn or (lambda prompt="": builtins.input(prompt))
        self._print = print_fn or (lambda *a: builtins.print(*a))
        self.auto = False

    def start_innings(self):
        """Live prompts resume at the start of every innings, even after 'a'."""
        self.auto = False

    def _ask(self, prompt):
        answer = self._input(prompt).strip().lower()
        if answer == AUTO:
            self.auto = True
            self._print("  -> auto for the rest of this innings")
        return answer

    # ----- toss -----------------------------------------------------------
    def choose_toss(self, toss_winner):
        while True:
            answer = self._input(f"\n{toss_winner} won the toss. Bat or bowl? (bat/bowl, Enter = bat): ").strip().lower()
            if answer in ("", "bat", "b"):
                return "BAT"
            if answer in ("bowl", "w", "field"):
                return "BOWL"
            self._print("  Please type bat or bowl.")

    # ----- batting --------------------------------------------------------
    def choose_openers(self, team_name, lineup):
        """Return the two lineup indices that open. Default: the first two."""
        if self.auto:
            return 0, 1
        self._print(f"\n{team_name} batting. Choose your openers:")
        for i, p in enumerate(lineup, 1):
            self._print(f"  {i:2d}. {p.name:<22} {p.role.upper():<4} bat {p.batting}")
        while True:
            answer = self._ask("Openers (two numbers, e.g. '1 2'; Enter = 1 2; auto = rest of innings): ")
            if answer in ("", AUTO):
                return 0, 1
            parts = answer.replace(",", " ").split()
            try:
                picks = [int(x) - 1 for x in parts]
            except ValueError:
                picks = []
            if len(picks) == 2 and picks[0] != picks[1] and all(0 <= k < len(lineup) for k in picks):
                return picks[0], picks[1]
            self._print("  Enter two different numbers from the list.")

    def choose_next_batter(self, team_name, lineup, candidates, situation):
        """Return the lineup index of the next batter. candidates[0] is the default."""
        default = candidates[0]
        if self.auto:
            return default
        self._print(f"\nWICKET! {situation}")
        for k in candidates:
            p = lineup[k]
            self._print(f"  {k + 1:2d}. {p.name:<22} {p.role.upper():<4} bat {p.batting}")
        while True:
            answer = self._ask(f"Next batter for {team_name} (Enter = {lineup[default].name}; auto = rest of innings): ")
            if answer in ("", AUTO):
                return default
            try:
                pick = int(answer) - 1
            except ValueError:
                pick = None
            if pick in candidates:
                return pick
            self._print("  Pick a number from the list.")

    # ----- bowling --------------------------------------------------------
    def choose_bowler(self, team_name, over_num, ranking, allowed, default, overs_left, situation):
        """Return the Player to bowl this over. `ranking` maps letter -> Player."""
        if self.auto:
            return default
        self._print(f"\nOver {over_num + 1} | {situation}")
        letters = {}
        for letter, p in ranking.items():
            if p.bowling < 3 and p is not default:
                continue  # hide non-bowlers to keep the list short
            ok = p in allowed
            if ok:
                letters[letter.lower()] = p
            mark = f"{overs_left[p.name]} left" if ok else ("bowled last over" if overs_left[p.name] else "done")
            self._print(f"  {letter}. {p.name:<22} {p.style:<5} bowl {p.bowling:<4} {mark}")
        while True:
            answer = self._ask(f"{team_name} bowler (Enter = {default.name}; letter to change; auto = rest of innings): ")
            if answer in ("", AUTO):
                return default
            if answer in letters:
                return letters[answer]
            self._print("  Pick an available letter.")

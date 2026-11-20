"""
captain.py

Live choices: the user makes the captain's calls for both sides of a match.

- Toss: the toss winner's bat/bowl decision.
- Batting: the openers before an innings, and the next batter at each wicket.
- Bowling: the bowler for every over. The team's normal bowling order is the
  default, so pressing Enter keeps it.

In a real terminal, each choice is an arrow-key menu (questionary) that is
erased once you pick, so the choices don't pile up on screen. The default is
pre-selected, so Enter keeps it, and the last item plays the rest of the
innings automatically. Without a terminal (tests, piped input) or without
questionary installed, the same choices are typed instead: Enter keeps the
default, "auto" plays the rest of the innings, and batters and bowlers are
picked by list number or by (part of) their name.

The simulation enforces the bowling rules itself
(4 overs max, no two overs in a row), so this module only offers legal options
and never has the final say on legality.
"""
import builtins
import sys

AUTO = "auto"
AUTO_LABEL = ">> auto: play the rest of this innings"
MIN_LISTED_BOWLING = 5  # bowlers rated below this are hidden from the bowler list


def _match(answer, options):
    """Resolve an answer to one of `options` ({number: player}) by number or by name.

    A name matches if it is unique (case-insensitive, any part of the name)."""
    if answer.isdigit():
        return options.get(int(answer))
    hits = [pl for pl in options.values() if answer in pl.name.lower()]
    return hits[0] if len(hits) == 1 else None


def _batter_line(number, p, default=False):
    mark = "  <- default" if default else ""
    return f"  {number:2d}. {p.name:<22} {p.role.upper():<4}  batting {p.batting:>4}{mark}"


def _terminal_menu():
    """The questionary module if arrow-key menus can be shown, else None."""
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        return None
    try:
        import questionary
    except ImportError:
        return None
    return questionary


def _bowler_label(p, status, is_default):
    mark = "  <- default" if is_default else ""
    return f"{p.name:<22} {p.style:<5} bowling {p.bowling:>4}  {status}{mark}"


class LiveCaptain:
    def __init__(self, input_fn=None, print_fn=None, menu=None):
        """input_fn/print_fn: typed prompts (default: input/print).
        menu: a questionary-like module for arrow-key menus. By default menus
        are used when running in a real terminal and no input_fn is given."""
        # Look up input/print at call time so a patched input() (tests) is used.
        self._input = input_fn or (lambda prompt="": builtins.input(prompt))
        self._print = print_fn or (lambda *a: builtins.print(*a))
        self._menu = menu if menu is not None else (None if input_fn or print_fn else _terminal_menu())
        self.auto = False

    def _choose(self, message, options, default, with_auto=True):
        """Arrow-key menu, erased once answered.

        options: list of (label, value, disabled_reason_or_None).
        Returns the chosen value, or AUTO (and switches auto on)."""
        q = self._menu
        choices = [q.Choice(title=label, value=i, disabled=reason)
                   for i, (label, _, reason) in enumerate(options)]
        default_idx = next(i for i, (_, value, _) in enumerate(options) if value == default)
        if with_auto:
            choices.append(q.Choice(title=AUTO_LABEL, value=AUTO))
        picked = q.select(message, choices=choices, default=choices[default_idx], qmark="",
                          instruction="(arrows + Enter)", erase_when_done=True).unsafe_ask()
        if picked == AUTO:
            self.auto = True
            return AUTO
        return options[picked][1]

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
        """Return "BAT", "BOWL", or None to let the simulation decide at random."""
        if self._menu:
            options = [("Bat first", "BAT", None), ("Bowl first", "BOWL", None), ("Random (auto)", None, None)]
            return self._choose(f"{toss_winner} won the toss", options, "BAT", with_auto=False)
        while True:
            answer = self._input(f"\n{toss_winner} won the toss. Bat or bowl? (bat/bowl, Enter = bat; auto = random): ").strip().lower()
            if answer in ("", "bat", "b"):
                return "BAT"
            if answer in ("bowl", "w", "field"):
                return "BOWL"
            if answer == AUTO:
                return None
            self._print("  Please type bat, bowl or auto.")

    # ----- batting --------------------------------------------------------
    def choose_openers(self, team_name, lineup):
        """Return the two lineup indices that open. Default: the first two."""
        if self.auto:
            return 0, 1
        if self._menu:
            options = [(_batter_line(i, p).strip(), i - 1, None) for i, p in enumerate(lineup, 1)]
            first = self._choose(f"{team_name} batting: choose opener 1", options, 0)
            if first == AUTO:
                return 0, 1
            second_default = 1 if first != 1 else 0
            rest = [o for o in options if o[1] != first]
            second = self._choose(f"{team_name} batting: choose opener 2 (opener 1: {lineup[first].name})",
                                  rest, second_default)
            return first, (second_default if second == AUTO else second)
        self._print(f"\n{team_name} batting. Choose your openers:")
        for i, p in enumerate(lineup, 1):
            self._print(_batter_line(i, p))
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
        if self._menu:
            options = [(_batter_line(k + 1, lineup[k], k == default).strip(), k, None) for k in candidates]
            pick = self._choose(f"WICKET! {situation}\n  Next batter for {team_name}", options, default)
            return default if pick == AUTO else pick
        self._print(f"\nWICKET! {situation}")
        options = {k + 1: lineup[k] for k in candidates}
        for number, p in options.items():
            self._print(_batter_line(number, p, default=(number == default + 1)))
        while True:
            answer = self._ask(f"Next batter for {team_name} (Enter = {lineup[default].name}; number or name; auto = rest of innings): ")
            if answer in ("", AUTO):
                return default
            player = _match(answer, options)
            if player is not None:
                return next(k for k in candidates if lineup[k] is player)
            self._print("  Pick a number or a name from the list.")

    # ----- bowling --------------------------------------------------------
    def choose_bowler(self, team_name, over_num, ranking, allowed, default, overs_left, situation):
        """Return the Player to bowl this over.

        `ranking` maps letter -> Player, best bowler first. The list shows
        bowlers rated MIN_LISTED_BOWLING or more, numbered in that order (so a
        bowler keeps the same number all innings), plus the default and, if
        none of those can bowl, everyone who can.
        """
        if self.auto:
            return default
        listed = [p for p in ranking.values() if p.bowling >= MIN_LISTED_BOWLING or p is default]
        if not any(p in allowed for p in listed):
            listed += [p for p in ranking.values() if p in allowed and p not in listed]
        if self._menu:
            options = []
            for p in listed:
                left = overs_left[p.name]
                if p in allowed:
                    status = f"{left} over{'s' if left != 1 else ''} left"
                    options.append((_bowler_label(p, status, p is default), p, None))
                else:
                    reason = f"bowled last over, {left} left" if left else "4 overs done"
                    options.append((_bowler_label(p, "", False).rstrip(), p, reason))
            pick = self._choose(f"Over {over_num + 1} | {situation}\n  {team_name} bowler", options, default)
            return default if pick == AUTO else pick
        options = {}
        self._print(f"\nOver {over_num + 1} | {situation}")
        for number, p in enumerate(listed, 1):
            left = overs_left[p.name]
            if p in allowed:
                options[number] = p
                status = f"{left} over{'s' if left != 1 else ''} left"
            elif left:
                status = f"bowled last over ({left} left)"
            else:
                status = "4 overs done"
            mark = "  <- default" if p is default else ""
            self._print(f"  {number:2d}. {p.name:<22} {p.style:<5} bowling {p.bowling:>4}  {status}{mark}")
        while True:
            answer = self._ask(f"{team_name} bowler (Enter = {default.name}; number or name; auto = rest of innings): ")
            if answer in ("", AUTO):
                return default
            player = _match(answer, options)
            if player is not None:
                return player
            self._print("  Pick an available bowler by number or name.")

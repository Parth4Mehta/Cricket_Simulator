#!/usr/bin/env python3
"""
CricSim - Cricket League Simulator
Main entry point for the application.
"""

import sys
from match_simulator import choose_profile, choose_profile_default, simulate_match
from league_simulator import simulate_league, select_teams
from database import print_caps_and_table, clear_database, get_points_table_sorted
from teams import get_teams


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print("       🏏 CRICSIM - Cricket League Simulator 🏏")
    print("="*70)
    print()


def show_main_menu():
    """Display the main menu and get user choice."""
    print("\n=== MAIN MENU ===")
    print("1. Simulate a League (Double Round-Robin + Playoffs)")
    print("2. Simulate a Single Match")
    print("3. View Current Stats")
    print("4. View Full Player Stats (Top Players)")
    print("5. Clear Database & Start Fresh")
    print("6. Configure Game Difficulty")
    print("7. Exit")
    print()
    
    choice = input("Select an option (1-7): ").strip()
    return choice


def menu_simulate_league():
    """Simulate a full league."""
    print("\n" + "="*70)
    print("LEAGUE SIMULATION")
    print("="*70)
    
    try:
        simulate_league()
    except KeyboardInterrupt:
        print("\n\nLeague simulation cancelled.")
    except Exception as e:
        print(f"\nError during league simulation: {e}")


def menu_simulate_match():
    """Simulate a single match."""
    print("\n" + "="*70)
    print("SINGLE MATCH SIMULATION")
    print("="*70)
    
    all_teams = list(get_teams().keys())
    
    print(f"\nAvailable teams ({len(all_teams)} total):")
    for idx, team in enumerate(all_teams, 1):
        print(f"{idx:2d}. {team}")
    
    print()
    try:
        team1_idx = int(input("Select team 1 (enter number): ")) - 1
        if not (0 <= team1_idx < len(all_teams)):
            print("Invalid selection!")
            return
        
        team2_idx = int(input("Select team 2 (enter number): ")) - 1
        if not (0 <= team2_idx < len(all_teams)):
            print("Invalid selection!")
            return
        
        if team1_idx == team2_idx:
            print("Teams must be different!")
            return
        
        team1 = all_teams[team1_idx]
        team2 = all_teams[team2_idx]
        
        ball_by_ball = input("Show ball-by-ball (y/n, default: n): ").strip().lower() == "y"
        
        simulate_match(team1, team2, ball_by_ball=ball_by_ball)
    except ValueError:
        print("Invalid input!")
    except KeyboardInterrupt:
        print("\n\nMatch simulation cancelled.")
    except Exception as e:
        print(f"Error during match simulation: {e}")


def menu_view_stats():
    """View current statistics."""
    print("\n" + "="*70)
    print("CURRENT STATISTICS")
    print("="*70)
    
    try:
        print_caps_and_table()
    except Exception as e:
        print(f"Error displaying stats: {e}")


def menu_view_full_stats():
    """View full player statistics (top players across all categories)."""
    print("\n" + "="*70)
    print("FULL PLAYER STATISTICS")
    print("="*70)
    print("\nFetching and displaying comprehensive player statistics...")
    print("(Running top_players analysis)\n")
    
    try:
        # Import and run top_players main function
        from top_players import main as top_players_main
        sys.argv = [sys.argv[0], "--print"]  # Set args to print output
        top_players_main()
    except KeyboardInterrupt:
        print("\n\nFull stats display cancelled.")
    except Exception as e:
        print(f"Error displaying full stats: {e}")
        import traceback
        traceback.print_exc()


def menu_clear_database():
    """Clear database and start fresh."""
    print("\n" + "="*70)
    print("CLEAR DATABASE")
    print("="*70)
    print("\nThis will delete all statistics and match records!")
    
    confirm = input("Are you sure? (yes/no): ").strip().lower()
    if confirm == "yes":
        clear_database()
        print("Database cleared successfully!")
    else:
        print("Operation cancelled.")


def menu_configure():
    """Configure game difficulty."""
    print("\n" + "="*70)
    print("GAME CONFIGURATION")
    print("="*70)
    print("\nChoose your game difficulty profile:")
    
    choose_profile()


def main():
    """Main application loop."""
    print_banner()
    print("Welcome to CricSim!")
    print("Load default difficulty (Balanced)...")
    choose_profile_default()
    
    while True:
        try:
            choice = show_main_menu()
            
            if choice == "1":
                menu_simulate_league()
            elif choice == "2":
                menu_simulate_match()
            elif choice == "3":
                menu_view_stats()
            elif choice == "4":
                menu_view_full_stats()
            elif choice == "5":
                menu_clear_database()
            elif choice == "6":
                menu_configure()
            elif choice == "7":
                print("\nThanks for using CricSim! Goodbye!\n")
                sys.exit(0)
            else:
                print("Invalid choice! Please select 1-7.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            confirm = input("Exit? (yes/no): ").strip().lower()
            if confirm == "yes":
                print("\nThanks for using CricSim! Goodbye!\n")
                sys.exit(0)
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Returning to main menu...\n")


if __name__ == "__main__":
    main()

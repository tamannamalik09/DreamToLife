#!/usr/bin/env python3
"""
DreamToLife - Entry point CLI

This script provides a terminal menu for interacting with the DreamToLife
multi-agent system. It imports the package implemented in `dreamtolife_app`.

Beginner-friendly, heavily commented, and no external dependencies.
"""
from datetime import datetime
from dreamtolife_app.coordinator import CoordinatorAgent
from dreamtolife_app.journal import DreamJournal
import sys


def main_menu():
    coordinator = CoordinatorAgent()
    journal = DreamJournal()

    while True:
        print("\n==================================================")
        print("🌙 DREAMTOLIFE — Multi-Agent Dream Reflection System")
        print("==================================================")
        print("1. Analyze New Dream")
        print("2. View Dream History")
        print("3. View Growth Report")
        print("4. View Recurring Themes")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            dream_text = input("\n📝 Enter your dream description (be as detailed as you like):\n")
            if not dream_text.strip():
                print("Please enter a non-empty dream description.")
                continue
            result = coordinator.analyze_dream(dream_text)
            # Save to journal
            journal.add_entry(result)
            # Print report
            print_report(result)

        elif choice == "2":
            entries = journal.get_all_entries()
            if not entries:
                print("No dreams saved yet.")
                continue
            for i, e in enumerate(entries, 1):
                print(f"\n----- Dream #{i} — {e.get('date')} -----")
                print(e.get("report_text", "(no report)") )

        elif choice == "3":
            report = coordinator.growth_agent.generate_growth_report(journal.path)
            print(report)

        elif choice == "4":
            recurring = coordinator.growth_agent.recurring_themes(journal.path)
            if not recurring:
                print("No recurring themes detected yet.")
            else:
                print("\n🔁 Recurring Themes and Symbols:")
                for k, v in recurring.items():
                    print(f"- {k}: {v} occurrences")

        elif choice == "5":
            print("Goodbye — keep reflecting 🌱")
            sys.exit(0)

        else:
            print("Invalid choice. Enter 1-5.")


def print_report(result: dict):
    # Prints the formatted DreamToLife report to terminal
    print("\n==================================================")
    print("🌙 DREAMTOLIFE REPORT")
    print("==================================================")
    print("📝 Dream Summary")
    print(result.get("summary", "(no summary)"))
    print("\n🎭 Emotion Analysis")
    for emo, score in result.get("emotions", {}).items():
        print(f"- {emo}: {score}%")
    print("\n🔍 Symbols Detected")
    for s in result.get("symbols", []):
        print(f"- {s}")
    print("\n💡 Themes Identified")
    for t in result.get("themes", []):
        print(f"- {t}")
    print("\n📖 Dream Narrative")
    print(result.get("narrative", "(narrative unavailable)"))
    print("\n🧠 Reflection Questions")
    for q in result.get("reflection_questions", []):
        print(f"- {q}")
    print("\n✅ Daily Actions")
    print(f"- {result.get('daily_action')}")
    print("\n🎯 Weekly Challenge")
    print(f"- {result.get('weekly_challenge')}")
    print("\n🌱 Personal Growth Insight")
    print(result.get("growth_insight"))
    print("\n📊 Dream Scorecard")
    for k, v in result.get("scorecard", {}).items():
        print(f"- {k}: {v}")
    print("\n🔗 AI Image Prompt (mock)")
    print(result.get("image_prompt"))
    print("\n==================================================")


if __name__ == "__main__":
    main_menu()

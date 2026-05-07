"""
Personal Expense Tracker
========================
Track, categorize, and analyze your daily expenses.
"""

import json
import os
from datetime import datetime
from collections import defaultdict



DATA_FILE = r"C:\Users\shaik\Downloads\files\expenses.json"

CATEGORIES = [
    "Food & Dining",
    "Transport",
    "Shopping",
    "Entertainment",
    "Health & Medical",
    "Bills & Utilities",
    "Education",
    "Other"
]



def load_expenses():
    """Load expenses from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    """Save expenses to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def generate_id(expenses):
    """Generate a unique integer ID."""
    return max((e["id"] for e in expenses), default=0) + 1




def add_expense(expenses):
    """Prompt user and add a new expense."""
    print("\n--- Add New Expense ---")
    try:
        amount = float(input("Amount (₹): ").strip())
    except ValueError:
        print(" Invalid amount. Please enter a number.")
        return

    print("Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
    try:
        cat_choice = int(input("Select category (number): ").strip())
        category = CATEGORIES[cat_choice - 1]
    except (ValueError, IndexError):
        print(" Invalid category selection.")
        return

    description = input("Description (optional): ").strip() or "No description"
    date_input = input("Date (YYYY-MM-DD) [press Enter for today]: ").strip()
    if not date_input:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
        except ValueError:
            print(" Invalid date format.")
            return

    expense = {
        "id": generate_id(expenses),
        "amount": round(amount, 2),
        "category": category,
        "description": description,
        "date": date,
        "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f" Expense added! [ID: {expense['id']}]")


def view_expenses(expenses):
    """Display all expenses in a table."""
    if not expenses:
        print("\n No expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    print(f"{'ID':<5} {'Date':<12} {'Category':<20} {'Amount':>10}  Description")
    print("-" * 70)
    total = 0
    for e in sorted(expenses, key=lambda x: x["date"], reverse=True):
        print(f"{e['id']:<5} {e['date']:<12} {e['category']:<20} ₹{e['amount']:>9.2f}  {e['description']}")
        total += e["amount"]
    print("-" * 70)
    print(f"{'TOTAL':<38} ₹{total:>9.2f}")


def delete_expense(expenses):
    """Delete an expense by ID."""
    view_expenses(expenses)
    if not expenses:
        return
    try:
        eid = int(input("\nEnter ID to delete: ").strip())
    except ValueError:
        print(" Invalid ID.")
        return

    for i, e in enumerate(expenses):
        if e["id"] == eid:
            expenses.pop(i)
            save_expenses(expenses)
            print(" Expense deleted.")
            return
    print(" ID not found.")


def edit_expense(expenses):
    """Edit an existing expense."""
    view_expenses(expenses)
    if not expenses:
        return
    try:
        eid = int(input("\nEnter ID to edit: ").strip())
    except ValueError:
        print(" Invalid ID.")
        return

    for e in expenses:
        if e["id"] == eid:
            print(f"\nEditing Expense ID {eid}  (press Enter to keep current value)")

            amt_input = input(f"Amount [₹{e['amount']}]: ").strip()
            if amt_input:
                try:
                    e["amount"] = round(float(amt_input), 2)
                except ValueError:
                    print(" Invalid amount — keeping original.")

            print("Categories:")
            for i, cat in enumerate(CATEGORIES, 1):
                print(f"  {i}. {cat}")
            cat_input = input(f"Category [{e['category']}]: ").strip()
            if cat_input:
                try:
                    e["category"] = CATEGORIES[int(cat_input) - 1]
                except (ValueError, IndexError):
                    print(" Invalid selection — keeping original.")

            desc_input = input(f"Description [{e['description']}]: ").strip()
            if desc_input:
                e["description"] = desc_input

            date_input = input(f"Date [{e['date']}]: ").strip()
            if date_input:
                try:
                    datetime.strptime(date_input, "%Y-%m-%d")
                    e["date"] = date_input
                except ValueError:
                    print(" Invalid date — keeping original.")

            save_expenses(expenses)
            print(" Expense updated.")
            return
    print(" ID not found.")




def search_expenses(expenses):
    """Search by keyword in description or category."""
    keyword = input("\nSearch keyword: ").strip().lower()
    results = [
        e for e in expenses
        if keyword in e["description"].lower() or keyword in e["category"].lower()
    ]
    if results:
        print(f"\n Found {len(results)} result(s):")
        print(f"{'ID':<5} {'Date':<12} {'Category':<20} {'Amount':>10}  Description")
        print("-" * 70)
        for e in results:
            print(f"{e['id']:<5} {e['date']:<12} {e['category']:<20} ₹{e['amount']:>9.2f}  {e['description']}")
    else:
        print(" No results found.")


def filter_by_date(expenses):
    """Filter expenses between two dates."""
    start = input("Start date (YYYY-MM-DD): ").strip()
    end = input("End date   (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        print(" Invalid date format.")
        return

    results = [e for e in expenses if start <= e["date"] <= end]
    if results:
        total = sum(e["amount"] for e in results)
        print(f"\n Expenses from {start} to {end}:")
        print(f"{'ID':<5} {'Date':<12} {'Category':<20} {'Amount':>10}  Description")
        print("-" * 70)
        for e in sorted(results, key=lambda x: x["date"]):
            print(f"{e['id']:<5} {e['date']:<12} {e['category']:<20} ₹{e['amount']:>9.2f}  {e['description']}")
        print("-" * 70)
        print(f"{'Total':<38} ₹{total:>9.2f}")
    else:
        print(" No expenses in that range.")



def monthly_summary(expenses):
    """Show a month-wise spending summary."""
    if not expenses:
        print("\n No data to summarize.")
        return

    monthly = defaultdict(float)
    for e in expenses:
        month = e["date"][:7]   
        monthly[month] += e["amount"]

    print("\n--- Monthly Summary ---")
    print(f"{'Month':<12} {'Total Spent':>14}")
    print("-" * 28)
    for month in sorted(monthly):
        print(f"{month:<12} ₹{monthly[month]:>13.2f}")
    print("-" * 28)
    print(f"{'Grand Total':<12} ₹{sum(monthly.values()):>13.2f}")


def category_summary(expenses):
    """Show spending breakdown by category."""
    if not expenses:
        print("\n No data to summarize.")
        return

    cat_totals = defaultdict(float)
    grand = sum(e["amount"] for e in expenses)
    for e in expenses:
        cat_totals[e["category"]] += e["amount"]

    print("\n--- Category Breakdown ---")
    print(f"{'Category':<22} {'Amount':>10}  {'Share':>8}")
    print("-" * 44)
    for cat, total in sorted(cat_totals.items(), key=lambda x: -x[1]):
        pct = (total / grand * 100) if grand else 0
        bar = "█" * int(pct / 5)
        print(f"{cat:<22} ₹{total:>9.2f}  {pct:>6.1f}%  {bar}")
    print("-" * 44)
    print(f"{'TOTAL':<22} ₹{grand:>9.2f}")


def top_expenses(expenses):
    """Show the top 5 largest expenses."""
    if not expenses:
        print("\n No data available.")
        return
    top = sorted(expenses, key=lambda x: x["amount"], reverse=True)[:5]
    print("\n--- Top 5 Expenses ---")
    print(f"{'Rank':<6} {'Date':<12} {'Category':<20} {'Amount':>10}  Description")
    print("-" * 70)
    for rank, e in enumerate(top, 1):
        print(f"{rank:<6} {e['date']:<12} {e['category']:<20} ₹{e['amount']:>9.2f}  {e['description']}")


def set_budget_alert(expenses):
    """Warn if this month's spending exceeds a given budget."""
    try:
        budget = float(input("Set monthly budget (₹): ").strip())
    except ValueError:
        print(" Invalid amount.")
        return

    this_month = datetime.today().strftime("%Y-%m")
    spent = sum(e["amount"] for e in expenses if e["date"].startswith(this_month))
    remaining = budget - spent

    print(f"\n Budget:    ₹{budget:.2f}")
    print(f" Spent:     ₹{spent:.2f}")
    if remaining >= 0:
        print(f" Remaining: ₹{remaining:.2f}")
    else:
        print(f"  OVER BUDGET by ₹{abs(remaining):.2f}!")




def export_to_csv(expenses):
    if not expenses:
        print("\n Nothing to export.")
        return
    
    filename = f"expenses_{datetime.today().strftime('%Y%m%d_%H%M%S')}.csv"
    filename = os.path.join(os.path.dirname(__file__), filename)
    
    try:
        with open(filename, "w", newline='') as f:
            
            pass
        print(f"\n Exported to {filename}")
    except PermissionError:
        print("\n Permission denied! Close the file if it's open in Excel.")

MENU = """
╔══════════════════════════════════════╗
║     Personal Expense Tracker         ║
╠══════════════════════════════════════╣
║  1. Add Expense                      ║
║  2. View All Expenses                ║
║  3. Edit Expense                     ║
║  4. Delete Expense                   ║
║──────────────────────────────────────║
║  5. Search Expenses                  ║
║  6. Filter by Date Range             ║
║──────────────────────────────────────║
║  7. Monthly Summary                  ║
║  8. Category Breakdown               ║
║  9. Top 5 Expenses                   ║
║ 10. Set Budget Alert                 ║
║──────────────────────────────────────║
║ 11. Export to CSV                    ║
║  0. Exit                             ║
╚══════════════════════════════════════╝
"""

def main():
    expenses = load_expenses()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if   choice == "1":  add_expense(expenses)
        elif choice == "2":  view_expenses(expenses)
        elif choice == "3":  edit_expense(expenses)
        elif choice == "4":  delete_expense(expenses)
        elif choice == "5":  search_expenses(expenses)
        elif choice == "6":  filter_by_date(expenses)
        elif choice == "7":  monthly_summary(expenses)
        elif choice == "8":  category_summary(expenses)
        elif choice == "9":  top_expenses(expenses)
        elif choice == "10": set_budget_alert(expenses)
        elif choice == "11": export_to_csv(expenses)
        elif choice == "0":
            print("\n Goodbye! Keep tracking your expenses.\n")
            break
        else:
            print(" Invalid option. Please try again.")


if __name__ == "__main__":
    main()

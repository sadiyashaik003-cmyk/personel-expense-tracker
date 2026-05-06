# 💰 Personal Expense Tracker

A command-line Python mini-project to track, categorize, and analyze your daily expenses.

---

## 📁 Project Structure

```
expense_tracker/
├── expense_tracker.py   ← Main application
├── expenses.json        ← Data storage (auto-created)
└── README.md            ← This file
```

---

## 🚀 How to Run

```bash
python expense_tracker.py
```

> **Requirements:** Python 3.6+  — No external libraries needed!

---

## ✨ Features

| # | Feature              | Description                                    |
|---|----------------------|------------------------------------------------|
| 1 | Add Expense          | Log amount, category, description, and date   |
| 2 | View All Expenses    | Tabular view of all records with total        |
| 3 | Edit Expense         | Modify any field of an existing expense       |
| 4 | Delete Expense       | Remove an expense by ID                       |
| 5 | Search               | Find expenses by keyword                      |
| 6 | Filter by Date Range | View expenses between two dates               |
| 7 | Monthly Summary      | Month-wise total spending                     |
| 8 | Category Breakdown   | Visual bar chart of spending by category      |
| 9 | Top 5 Expenses       | Largest expenses ranked                       |
|10 | Budget Alert         | Set a monthly budget and track overspending   |
|11 | Export to CSV        | Save all data as a `.csv` file                |

---

## 🗂️ Expense Categories

- Food & Dining
- Transport
- Shopping
- Entertainment
- Health & Medical
- Bills & Utilities
- Education
- Other

---

## 💾 Data Storage

All expenses are stored locally in **`expenses.json`**.  
The file is created automatically on first use.

---

## 📤 CSV Export

Use option **11** to export all expenses to a timestamped CSV file, e.g.:  
`expenses_20250501_143022.csv`

---

## 🧑‍💻 Example Usage

```
Choose an option: 1

--- Add New Expense ---
Amount (₹): 450
Categories:
  1. Food & Dining
  ...
Select category (number): 1
Description (optional): Lunch at Dominos
Date (YYYY-MM-DD) [press Enter for today]: 
✅ Expense added! [ID: 9]
```

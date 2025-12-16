# 🚢 Ships CLI – Python Command Line Data Explorer

A Python-based Command Line Interface (CLI) application for exploring, searching, and visualizing ship data from a structured JSON dataset.

This project demonstrates **clean CLI design**, **defensive data handling**, and **modular Python architecture**, with a strong focus on readability and maintainability.

---

## 📌 Project Overview

The Ships CLI allows users to interactively explore a real-world ship dataset directly from the terminal.

Users can:
- List ship countries (unique & sorted)
- Identify countries with the most ships
- Group ships by type
- Search ships by name (partial & case-insensitive)
- Generate histograms from numeric data
- Plot ship positions on a world map

The application runs continuously until the user exits or presses `Ctrl + C`.

---

## 🎯 Learning Goals

This project was built to strengthen:

- Python data structures (`list`, `dict`, `set`)
- Command-line interface architecture
- Input parsing & validation
- Defensive programming techniques
- Separation of concerns
- Data aggregation using `Counter`
- Basic data visualization with `matplotlib`

---

## 🧠 Key Design Decisions

### Command Dispatcher Pattern
Commands are mapped to handler functions using a dictionary, avoiding long `if / elif` chains and making the CLI easily extensible.

### Defensive Data Access
Missing or malformed data is safely handled using:
- `.get()` lookups
- `try / except` blocks
- fallback values (e.g. empty strings)

### Readable & Pythonic Code
The code favors clarity and intent:
- descriptive function names
- small, single-purpose helpers
- built-in tools like `Counter.most_common()`

---

## ⚙️ Available Commands

### `help`
Show all available commands and usage instructions.

---

### `show_countries`
List all ship countries:
- removes duplicates
- sorts alphabetically

```bash
show_countries
```

top_countries <num>

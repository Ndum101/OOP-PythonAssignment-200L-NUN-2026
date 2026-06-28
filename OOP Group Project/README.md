# Library Management System — OOP Group Project

## Group Members

| Name                          | Matric Number |
|-------------------------------|---------------|
| Ndubuisi Johnkennedy Okeke    | 242030102     |
| Rahmatallahi Ismael Mustapha  | 241030101     |
| Faisal Bagudu Ibrahim         | 242030094     |
| Tomiwa Giwa                   | 242030015     |

**Course:** Object-Oriented Programming  
**Level:** 200L  
**University:** Nigerian University of Nissi (NUN)  
**Year:** 2026  

---

## Project Description

A Library Management System built in Python using Object-Oriented Programming principles.
The system allows librarians to manage books, register members, issue and return books,
and track all borrowing records.

## Files

| File            | Description                                          |
|-----------------|------------------------------------------------------|
| `library.py`    | Core OOP logic — Book, Member, IssuedRecord, Library |
| `gui.py`        | Tkinter GUI — full graphical interface               |
| `library.json`  | Persistent data store (auto-updated on every action) |

## How to Run

### GUI version (recommended)
```bash
python gui.py
```

### Terminal version
```bash
python library.py
```

> Both files must be in the same folder as `library.json`.

## Features

- Add, search, and view books with copy tracking
- Register and manage library members
- Issue books to members (14-day loan period)
- Return books with automatic date recording
- View all borrow records with overdue detection
- Data persists automatically via `library.json`

"""
============================================================
  OOP Group Project — Library Management System (GUI)
============================================================
  Group Members:
    Ndubuisi Johnkennedy Okeke     | 242030102
    Rahmatallahi Ismael Mustapha   | 241030101
    Faisal Bagudu Ibrahim          | 242030094
    Tomiwa Giwa                    | 242030015
============================================================
  Course:     Object-Oriented Programming
  Level:      200L
  University: Nigerian University of Nissi (NUN)
  Year:       2026
============================================================
  GUI Module — built with Tkinter (standard library, no
  extra installs needed). Run this file to launch the app.
  Requires library.py and library.json in the same folder.
============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
from library import Library

LOAN_DAYS = 14
ACCENT   = "#2563EB"
ACCENT_H = "#1D4ED8"
BG       = "#F8FAFC"
CARD     = "#FFFFFF"
BORDER   = "#E2E8F0"
TEXT     = "#0F172A"
MUTED    = "#64748B"
SUCCESS  = "#16A34A"
DANGER   = "#DC2626"
WARNING  = "#D97706"


def today():
    return datetime.now().strftime("%Y-%m-%d")

def add_days(d, n):
    dt = datetime.strptime(d, "%Y-%m-%d") + timedelta(days=n)
    return dt.strftime("%Y-%m-%d")


class StyledButton(tk.Button):
    def __init__(self, parent, text, command, style="default", **kwargs):
        colors = {
            "primary": (ACCENT,   "#FFFFFF", ACCENT_H),
            "danger":  ("#FEE2E2", DANGER,   "#FECACA"),
            "default": (CARD,      TEXT,      "#F1F5F9"),
        }
        bg, fg, hbg = colors.get(style, colors["default"])
        super().__init__(
            parent, text=text, command=command,
            bg=bg, fg=fg, activebackground=hbg, activeforeground=fg,
            relief="flat", bd=0, padx=14, pady=7,
            font=("Segoe UI", 10), cursor="hand2", **kwargs
        )
        self.configure(highlightbackground=BORDER, highlightthickness=1)


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lib = Library()
        self.title("Library Management System — OOP Group Project")
        self.geometry("980x640")
        self.resizable(True, True)
        self.configure(bg=BG)
        self._build_ui()
        self.show_page("dashboard")

    def _build_ui(self):
        # ── Sidebar ──────────────────────────────────────────────
        sidebar = tk.Frame(self, bg="#1E293B", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_frame = tk.Frame(sidebar, bg="#1E293B", pady=20, padx=16)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="📚 Libris", font=("Segoe UI", 15, "bold"),
                 bg="#1E293B", fg="#F8FAFC").pack(anchor="w")
        tk.Label(logo_frame, text="Library System", font=("Segoe UI", 9),
                 bg="#1E293B", fg="#94A3B8").pack(anchor="w")

        sep = tk.Frame(sidebar, bg="#334155", height=1)
        sep.pack(fill="x", padx=16)

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "🏠  Dashboard"),
            ("books",     "📖  Books"),
            ("members",   "👥  Members"),
            ("issued",    "📋  Issued Books"),
        ]
        nav_frame = tk.Frame(sidebar, bg="#1E293B", pady=8)
        nav_frame.pack(fill="x")
        for key, label in nav_items:
            btn = tk.Button(
                nav_frame, text=label, anchor="w",
                command=lambda k=key: self.show_page(k),
                bg="#1E293B", fg="#CBD5E1", activebackground="#334155",
                activeforeground="#F8FAFC", relief="flat", bd=0,
                padx=20, pady=10, font=("Segoe UI", 10), cursor="hand2",
                width=22
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        # ── Main area ────────────────────────────────────────────
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        # Top bar
        topbar = tk.Frame(self.main, bg=CARD, height=56)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        inner_top = tk.Frame(topbar, bg=CARD)
        inner_top.pack(fill="both", expand=True, padx=20, pady=10)
        self.page_title = tk.Label(inner_top, text="Dashboard",
                                   font=("Segoe UI", 14, "bold"),
                                   bg=CARD, fg=TEXT)
        self.page_title.pack(side="left")
        btn_frame = tk.Frame(inner_top, bg=CARD)
        btn_frame.pack(side="right")
        StyledButton(btn_frame, "+ Add Book",   self.open_add_book,   "primary").pack(side="left", padx=4)
        StyledButton(btn_frame, "+ Add Member", self.open_add_member, "primary").pack(side="left", padx=4)
        StyledButton(btn_frame, "Issue Book",   self.open_borrow,     "default").pack(side="left", padx=4)
        StyledButton(btn_frame, "Return Book",  self.open_return,     "default").pack(side="left", padx=4)

        sep2 = tk.Frame(self.main, bg=BORDER, height=1)
        sep2.pack(fill="x")

        # Page container
        self.container = tk.Frame(self.main, bg=BG)
        self.container.pack(fill="both", expand=True, padx=24, pady=20)

        # Build all pages
        self.pages = {}
        self.pages["dashboard"] = self._build_dashboard()
        self.pages["books"]     = self._build_books()
        self.pages["members"]   = self._build_members()
        self.pages["issued"]    = self._build_issued()

    # ── Navigation ───────────────────────────────────────────────
    def show_page(self, key):
        for k, f in self.pages.items():
            f.pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        for k, b in self.nav_buttons.items():
            b.configure(bg="#334155" if k == key else "#1E293B",
                        fg="#F8FAFC" if k == key else "#CBD5E1")
        titles = {"dashboard": "Dashboard", "books": "Books",
                  "members": "Members", "issued": "Issued Books"}
        self.page_title.configure(text=titles.get(key, key.title()))
        refresh = {"dashboard": self.refresh_dashboard,
                   "books":     self.refresh_books,
                   "members":   self.refresh_members,
                   "issued":    self.refresh_issued}
        refresh[key]()

    # ── Dashboard ────────────────────────────────────────────────
    def _build_dashboard(self):
        frame = tk.Frame(self.container, bg=BG)

        stats_row = tk.Frame(frame, bg=BG)
        stats_row.pack(fill="x", pady=(0, 20))
        self.stat_frames = {}
        for col, (key, label) in enumerate([
            ("total_books",  "Total Books"),
            ("available",    "Available Copies"),
            ("active_loans", "Active Loans"),
            ("members",      "Members"),
        ]):
            card = tk.Frame(stats_row, bg=CARD, relief="flat",
                            highlightbackground=BORDER, highlightthickness=1)
            card.grid(row=0, column=col, padx=(0, 12) if col < 3 else 0, sticky="nsew")
            stats_row.columnconfigure(col, weight=1)
            tk.Label(card, text=label, font=("Segoe UI", 9),
                     bg=CARD, fg=MUTED, pady=6).pack(anchor="w", padx=14)
            val = tk.Label(card, text="0", font=("Segoe UI", 26, "bold"),
                           bg=CARD, fg=TEXT)
            val.pack(anchor="w", padx=14)
            tk.Frame(card, bg=BG, height=10).pack()
            self.stat_frames[key] = val

        tk.Label(frame, text="Recent Activity", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 8))

        cols = ("Member", "Book", "Borrowed", "Due Date", "Status")
        self.dash_tree = self._make_tree(frame, cols)
        self.dash_tree.pack(fill="both", expand=True)
        return frame

    def refresh_dashboard(self):
        lib = self.lib
        total_books  = len(lib.books)
        avail        = sum(b.available_copies for b in lib.books.values())
        active_loans = sum(1 for r in lib.records if r.return_date is None)
        members      = len(lib.members)
        self.stat_frames["total_books"].configure(text=str(total_books))
        self.stat_frames["available"].configure(text=str(avail))
        self.stat_frames["active_loans"].configure(text=str(active_loans))
        self.stat_frames["members"].configure(text=str(members))

        tree = self.dash_tree
        for row in tree.get_children():
            tree.delete(row)
        for r in reversed(lib.records[-10:]):
            m    = lib.members.get(r.member_id)
            b    = lib.books.get(r.book_id)
            mname = m.name if m else "Unknown"
            btitle = b.title if b else "Unknown"
            if r.return_date:
                status = "Returned"
                tag = "returned"
            elif r.due_date < today():
                status = "Overdue"
                tag = "overdue"
            else:
                status = "Active"
                tag = "active"
            tree.insert("", "end", values=(mname, btitle, r.borrow_date, r.due_date, status), tags=(tag,))
        tree.tag_configure("returned", foreground=SUCCESS)
        tree.tag_configure("overdue",  foreground=DANGER)
        tree.tag_configure("active",   foreground=ACCENT)

    # ── Books ─────────────────────────────────────────────────────
    def _build_books(self):
        frame = tk.Frame(self.container, bg=BG)
        search_row = tk.Frame(frame, bg=BG)
        search_row.pack(fill="x", pady=(0, 12))
        tk.Label(search_row, text="🔍", bg=BG, font=("Segoe UI", 11)).pack(side="left")
        self.book_search = tk.StringVar()
        self.book_search.trace("w", lambda *_: self.refresh_books())
        tk.Entry(search_row, textvariable=self.book_search,
                 font=("Segoe UI", 11), relief="flat",
                 bg=CARD, fg=TEXT, insertbackground=TEXT,
                 highlightbackground=BORDER, highlightthickness=1,
                 width=40).pack(side="left", padx=8, ipady=5)

        cols = ("ID", "Title", "Author", "Available", "Total")
        self.books_tree = self._make_tree(frame, cols)
        self.books_tree.column("ID",        width=50,  stretch=False)
        self.books_tree.column("Available", width=90,  stretch=False)
        self.books_tree.column("Total",     width=70,  stretch=False)
        self.books_tree.pack(fill="both", expand=True)
        return frame

    def refresh_books(self):
        q = self.book_search.get().lower() if hasattr(self, "book_search") else ""
        tree = self.books_tree
        for row in tree.get_children():
            tree.delete(row)
        for b in self.lib.books.values():
            if q and q not in b.title.lower() and q not in b.author.lower():
                continue
            tag = "out" if b.available_copies == 0 else ("low" if b.available_copies <= 2 else "ok")
            tree.insert("", "end",
                        values=(b.book_id, b.title, b.author, b.available_copies, b.total_copies),
                        tags=(tag,))
        tree.tag_configure("ok",  foreground=SUCCESS)
        tree.tag_configure("low", foreground=WARNING)
        tree.tag_configure("out", foreground=DANGER)

    # ── Members ───────────────────────────────────────────────────
    def _build_members(self):
        frame = tk.Frame(self.container, bg=BG)
        search_row = tk.Frame(frame, bg=BG)
        search_row.pack(fill="x", pady=(0, 12))
        tk.Label(search_row, text="🔍", bg=BG, font=("Segoe UI", 11)).pack(side="left")
        self.member_search = tk.StringVar()
        self.member_search.trace("w", lambda *_: self.refresh_members())
        tk.Entry(search_row, textvariable=self.member_search,
                 font=("Segoe UI", 11), relief="flat",
                 bg=CARD, fg=TEXT, insertbackground=TEXT,
                 highlightbackground=BORDER, highlightthickness=1,
                 width=40).pack(side="left", padx=8, ipady=5)

        cols = ("ID", "Name", "Email", "Books Issued")
        self.members_tree = self._make_tree(frame, cols)
        self.members_tree.column("ID",          width=50,  stretch=False)
        self.members_tree.column("Books Issued",width=100, stretch=False)
        self.members_tree.pack(fill="both", expand=True)
        return frame

    def refresh_members(self):
        q = self.member_search.get().lower() if hasattr(self, "member_search") else ""
        tree = self.members_tree
        for row in tree.get_children():
            tree.delete(row)
        for m in self.lib.members.values():
            if q and q not in m.name.lower() and q not in m.email.lower():
                continue
            issued = len(m.issued_books)
            tag = "has_books" if issued > 0 else ""
            tree.insert("", "end",
                        values=(m.member_id, m.name, m.email, issued),
                        tags=(tag,))
        tree.tag_configure("has_books", foreground=ACCENT)

    # ── Issued ────────────────────────────────────────────────────
    def _build_issued(self):
        frame = tk.Frame(self.container, bg=BG)
        cols  = ("Member", "Book", "Borrowed", "Due Date", "Returned", "Status")
        self.issued_tree = self._make_tree(frame, cols)
        self.issued_tree.column("Borrowed",  width=100, stretch=False)
        self.issued_tree.column("Due Date",  width=100, stretch=False)
        self.issued_tree.column("Returned",  width=100, stretch=False)
        self.issued_tree.column("Status",    width=90,  stretch=False)
        self.issued_tree.pack(fill="both", expand=True)
        return frame

    def refresh_issued(self):
        tree = self.issued_tree
        for row in tree.get_children():
            tree.delete(row)
        for r in reversed(self.lib.records):
            m  = self.lib.members.get(r.member_id)
            b  = self.lib.books.get(r.book_id)
            mn = m.name if m else "Unknown"
            bt = b.title if b else "Unknown"
            ret = r.return_date or "—"
            if r.return_date:
                status, tag = "Returned", "returned"
            elif r.due_date < today():
                status, tag = "Overdue",  "overdue"
            else:
                status, tag = "Active",   "active"
            tree.insert("", "end",
                        values=(mn, bt, r.borrow_date, r.due_date, ret, status),
                        tags=(tag,))
        tree.tag_configure("returned", foreground=SUCCESS)
        tree.tag_configure("overdue",  foreground=DANGER)
        tree.tag_configure("active",   foreground=ACCENT)

    # ── Modals ────────────────────────────────────────────────────
    def open_add_book(self):
        win = self._modal("Add Book", 360, 280)
        fields = {}
        for label, key, ph in [
            ("Title",   "title",  "e.g. Things Fall Apart"),
            ("Author",  "author", "e.g. Chinua Achebe"),
            ("Copies",  "copies", "1"),
        ]:
            tk.Label(win, text=label, font=("Segoe UI", 10),
                     bg=CARD, fg=MUTED).pack(anchor="w", padx=24, pady=(10, 2))
            e = tk.Entry(win, font=("Segoe UI", 11), relief="flat",
                         bg=BG, fg=TEXT, insertbackground=TEXT,
                         highlightbackground=BORDER, highlightthickness=1)
            e.insert(0, ph)
            e.pack(fill="x", padx=24, ipady=5)
            fields[key] = e

        def submit():
            title  = fields["title"].get().strip()
            author = fields["author"].get().strip()
            try:
                copies = int(fields["copies"].get().strip())
            except ValueError:
                copies = 1
            if not title or not author:
                messagebox.showerror("Missing fields", "Title and author are required.", parent=win)
                return
            self.lib.add_book(title, author, copies)
            win.destroy()
            self.refresh_books()
            self.refresh_dashboard()

        StyledButton(win, "Add Book", submit, "primary").pack(pady=16)

    def open_add_member(self):
        win = self._modal("Register Member", 360, 240)
        fields = {}
        for label, key, ph in [
            ("Full Name",      "name",  "e.g. Amara Okafor"),
            ("Email Address",  "email", "e.g. amara@email.com"),
        ]:
            tk.Label(win, text=label, font=("Segoe UI", 10),
                     bg=CARD, fg=MUTED).pack(anchor="w", padx=24, pady=(10, 2))
            e = tk.Entry(win, font=("Segoe UI", 11), relief="flat",
                         bg=BG, fg=TEXT, insertbackground=TEXT,
                         highlightbackground=BORDER, highlightthickness=1)
            e.insert(0, ph)
            e.pack(fill="x", padx=24, ipady=5)
            fields[key] = e

        def submit():
            name  = fields["name"].get().strip()
            email = fields["email"].get().strip()
            if not name or not email:
                messagebox.showerror("Missing fields", "Name and email are required.", parent=win)
                return
            self.lib.register_member(name, email)
            win.destroy()
            self.refresh_members()
            self.refresh_dashboard()

        StyledButton(win, "Register", submit, "primary").pack(pady=16)

    def open_borrow(self):
        win = self._modal("Issue a Book", 380, 260)
        tk.Label(win, text="Member", font=("Segoe UI", 10),
                 bg=CARD, fg=MUTED).pack(anchor="w", padx=24, pady=(14, 2))
        member_var = tk.StringVar()
        member_map = {f"{m.name} (ID: {m.member_id})": m.member_id
                      for m in self.lib.members.values()}
        ttk.Combobox(win, textvariable=member_var,
                     values=list(member_map.keys()),
                     state="readonly", font=("Segoe UI", 10)).pack(fill="x", padx=24)

        tk.Label(win, text="Book", font=("Segoe UI", 10),
                 bg=CARD, fg=MUTED).pack(anchor="w", padx=24, pady=(10, 2))
        book_var = tk.StringVar()
        book_map = {f"{b.title} ({b.available_copies} left)": b.book_id
                    for b in self.lib.books.values() if b.available_copies > 0}
        ttk.Combobox(win, textvariable=book_var,
                     values=list(book_map.keys()),
                     state="readonly", font=("Segoe UI", 10)).pack(fill="x", padx=24)

        def submit():
            ms = member_var.get(); bs = book_var.get()
            if not ms or not bs:
                messagebox.showerror("Select both", "Please select a member and a book.", parent=win)
                return
            mid = member_map[ms]; bid = book_map[bs]
            self.lib.borrow_book(mid, bid)
            win.destroy()
            self.refresh_books(); self.refresh_issued(); self.refresh_dashboard()

        StyledButton(win, "Issue Book", submit, "primary").pack(pady=18)

    def open_return(self):
        win = self._modal("Return a Book", 380, 260)
        tk.Label(win, text="Member", font=("Segoe UI", 10),
                 bg=CARD, fg=MUTED).pack(anchor="w", padx=24, pady=(14, 2))
        member_var = tk.StringVar()
        active_members = {m for m in self.lib.members.values() if m.issued_books}
        member_map = {f"{m.name} (ID: {m.member_id})": m.member_id for m in active_members}
        mc = ttk.Combobox(win, textvariable=member_var,
                          values=list(member_map.keys()),
                          state="readonly", font=("Segoe UI", 10))
        mc.pack(fill="x", padx=24)

        tk.Label(win, text="Book to Return", font=("Segoe UI", 10),
                 bg=CARD, fg=MUTED).pack(anchor="w", padx=24, pady=(10, 2))
        book_var = tk.StringVar()
        bc = ttk.Combobox(win, textvariable=book_var,
                          state="readonly", font=("Segoe UI", 10))
        bc.pack(fill="x", padx=24)

        def on_member_select(event=None):
            ms = member_var.get()
            if not ms: return
            mid = member_map[ms]
            m   = self.lib.members[mid]
            book_map_local = {self.lib.books[bid].title: bid
                              for bid in m.issued_books if bid in self.lib.books}
            bc["values"] = list(book_map_local.keys())
            bc.book_map  = book_map_local

        mc.bind("<<ComboboxSelected>>", on_member_select)
        bc.book_map = {}

        def submit():
            ms = member_var.get(); bs = book_var.get()
            if not ms or not bs:
                messagebox.showerror("Select both", "Please select a member and a book.", parent=win)
                return
            mid = member_map[ms]; bid = bc.book_map.get(bs)
            if not bid:
                messagebox.showerror("Error", "Book not found.", parent=win)
                return
            self.lib.return_book(mid, bid)
            win.destroy()
            self.refresh_books(); self.refresh_issued()
            self.refresh_members(); self.refresh_dashboard()

        StyledButton(win, "Confirm Return", submit, "primary").pack(pady=18)

    # ── Helpers ───────────────────────────────────────────────────
    def _make_tree(self, parent, columns):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=CARD, fieldbackground=CARD,
                        foreground=TEXT, rowheight=32,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background=BG, foreground=MUTED,
                        font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#EFF6FF")],
                  foreground=[("selected", ACCENT)])
        frame = tk.Frame(parent, bg=CARD,
                         highlightbackground=BORDER, highlightthickness=1)
        tree  = ttk.Treeview(frame, columns=columns, show="headings",
                              selectmode="browse", style="Treeview")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="w", width=140)
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        return frame

    def _modal(self, title, w, h):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry(f"{w}x{h}")
        win.configure(bg=CARD)
        win.resizable(False, False)
        win.grab_set()
        tk.Label(win, text=title, font=("Segoe UI", 13, "bold"),
                 bg=CARD, fg=TEXT, pady=14).pack()
        tk.Frame(win, bg=BORDER, height=1).pack(fill="x")
        return win


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()

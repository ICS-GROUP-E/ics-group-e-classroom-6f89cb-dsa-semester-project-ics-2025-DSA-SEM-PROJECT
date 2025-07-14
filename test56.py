"""
Zettelkasten Note Manager

This script implements a desktop note-taking application inspired by the
Zettelkasten method and modern tools like Obsidian. It allows users to create
a network of interconnected notes, fostering a personal knowledge management system.

The application is built using Python with the standard Tkinter library for the GUI,
and it demonstrates the practical application of several fundamental data structures.

Core Features:
- Hierarchical note organization (Tree structure).
- Bi-directional linking between notes (Graph structure).
- Tagging system for categorization (Hash Map implementation).
- Back/Forward navigation history (Stack implementation).
- A list of recently viewed notes (Linked List implementation).
- Full-text search across note titles and content.
- Visualization of the note graph.

Data Structures Implemented:
- Graph: by Adrian
- Stack: by Aoi
- Linked List: by Austin
- Tree: by Jeremy
- Hash Map: by Kindness

Required Libraries:
- networkx
- matplotlib
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, scrolledtext
import sqlite3
import uuid
import collections
import sys
import time
import re
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Data Structure and Logic Classes ---

# --- 1. Graph Data Structure by Adrian ---
class Graph:
    """
    A Graph data structure to manage relationships (links) between notes.
    Implemented by Adrian.
    This uses an adjacency list (a dictionary) to store connections,
    providing an efficient way to represent and query the web of notes.
    """
    def __init__(self, logger_callback=None):
        self.graph = collections.defaultdict(list)
        self.logger = logger_callback if logger_callback else print
        self.logger("Graph: Initialized.")

    def add_note(self, note_id: str):
        if note_id not in self.graph:
            self.graph[note_id] = []

    def add_link(self, note1_id: str, note2_id: str):
        if note1_id == note2_id: return
        self.add_note(note1_id)
        self.add_note(note2_id)
        if note2_id not in self.graph[note1_id]: self.graph[note1_id].append(note2_id)
        if note1_id not in self.graph[note2_id]: self.graph[note2_id].append(note1_id)
        self.logger(f"Graph: Linked '{note1_id}' <-> '{note2_id}'.")

    def remove_note(self, note_id: str):
        if note_id in self.graph:
            for other_note_id in list(self.graph.keys()):
                if note_id in self.graph[other_note_id]:
                    self.graph[other_note_id].remove(note_id)
            del self.graph[note_id]
            self.logger(f"Graph: Removed note '{note_id}'.")

    def remove_link(self, note1_id: str, note2_id: str):
        if note1_id in self.graph and note2_id in self.graph[note1_id]: self.graph[note1_id].remove(note2_id)
        if note2_id in self.graph and note1_id in self.graph[note2_id]: self.graph[note2_id].remove(note1_id)
        self.logger(f"Graph: Unlinked '{note1_id}' and '{note2_id}'.")

    def get_connected_notes(self, note_id: str) -> list[str]:
        return self.graph.get(note_id, [])

# --- 2. Stack Data Structure by Aoi ---
class NoteNavigationStack:
    """Manages navigation history using two stacks for back/forward functionality."""
    def __init__(self, logger_callback=None):
        self.previous_notes = []
        self.next_notes = []
        self.current_note_id = None
        self.logger = logger_callback if logger_callback else print
        self.logger("Stack: Initialized navigation history.")

    def visit_note(self, note_id: str):
        if note_id == self.current_note_id: return
        if self.current_note_id is not None:
            self.previous_notes.append(self.current_note_id)
        self.current_note_id = note_id
        self.next_notes.clear()
        self.logger(f"Stack: Visited '{note_id}'. History: {len(self.previous_notes)} back, {len(self.next_notes)} fwd.")

    def go_back(self):
        if not self.previous_notes: return None
        if self.current_note_id is not None:
            self.next_notes.append(self.current_note_id)
        self.current_note_id = self.previous_notes.pop()
        return self.current_note_id

    def go_forward(self):
        if not self.next_notes: return None
        if self.current_note_id is not None:
            self.previous_notes.append(self.current_note_id)
        self.current_note_id = self.next_notes.pop()
        return self.current_note_id

# --- 3. Linked List Data Structure by Austin ---
class Note:
    """Represents a single Note object, used by the Linked List."""
    def __init__(self, note_id: str, title: str):
        self.id = note_id
        self.title = title

class CircularListNode:
    """Node for the Circular Doubly Linked List."""
    def __init__(self, note: Note):
        self.note = note
        self.next_node = None
        self.previous_node = None

class CircularDoublyLinkedNotesList:
    """A Circular Doubly Linked List to store recently viewed notes."""
    def __init__(self, capacity: int = 10, logger_callback=None):
        self.start_node = None
        self.size = 0
        self.capacity = capacity
        self.logger = logger_callback if logger_callback else print
        self.logger(f"LinkedList: Initialized with capacity {self.capacity}.")

    def insert_note(self, note: Note):
        if self.start_node:
            current = self.start_node
            for _ in range(self.size):
                if current.note.id == note.id:
                    self.remove_note_by_id(note.id)
                    break
                current = current.next_node

        new_node = CircularListNode(note)
        if self.start_node is None:
            new_node.next_node = new_node
            new_node.previous_node = new_node
            self.start_node = new_node
        else:
            last_node = self.start_node.previous_node
            new_node.next_node = self.start_node
            new_node.previous_node = last_node
            last_node.next_node = new_node
            self.start_node.previous_node = new_node
            self.start_node = new_node

        self.size += 1
        if self.capacity and self.size > self.capacity:
            self.remove_oldest_note()

    def remove_oldest_note(self):
        if self.size == 0: return
        if self.size == 1:
            self.start_node = None
        else:
            last_node = self.start_node.previous_node
            second_last = last_node.previous_node
            second_last.next_node = self.start_node
            self.start_node.previous_node = second_last
        self.size -= 1

    def remove_note_by_id(self, note_id: str):
        if self.start_node is None: return False
        current = self.start_node
        found = False
        for _ in range(self.size):
            if current.note.id == note_id:
                found = True
                break
            current = current.next_node
        if found:
            if self.size == 1:
                self.start_node = None
            else:
                current.previous_node.next_node = current.next_node
                current.next_node.previous_node = current.previous_node
                if current == self.start_node:
                    self.start_node = current.next_node
            self.size -= 1
            return True
        return False

    def get_recent_notes(self) -> list[Note]:
        notes = []
        if self.start_node is None: return notes
        current = self.start_node
        count = 0
        while count < self.capacity and count < self.size:
            notes.append(current.note)
            current = current.next_node
            count += 1
        return notes

# --- 4. SQLite Database Manager ---
class NoteDatabase:
    """Manages SQLite database interactions, including tags and parent-child relationships."""
    def __init__(self, db_name="zettelkasten_obsidian.db", logger_callback=None):
        self.db_name = db_name
        self.conn = None
        self.logger = logger_callback if logger_callback else print
        self.connect()
        if self.conn: self.create_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
            self.logger(f"DB: Connected to '{self.db_name}'.")
        except sqlite3.Error as e:
            sys.__stderr__.write(f"CRITICAL DB ERROR: {e}\n")
            self.conn = None

    def disconnect(self):
        if self.conn: self.conn.close()

    def create_tables(self):
        if not self.conn: return
        try:
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT, parent_id TEXT,
                    FOREIGN KEY (parent_id) REFERENCES notes(id) ON DELETE SET NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS note_links (
                    source_note_id TEXT NOT NULL, target_note_id TEXT NOT NULL,
                    PRIMARY KEY (source_note_id, target_note_id),
                    FOREIGN KEY (source_note_id) REFERENCES notes(id) ON DELETE CASCADE,
                    FOREIGN KEY (target_note_id) REFERENCES notes(id) ON DELETE CASCADE
                )
            """)
            cursor.execute("CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS note_tags (
                    note_id TEXT NOT NULL, tag_id INTEGER NOT NULL,
                    PRIMARY KEY (note_id, tag_id),
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            sys.__stderr__.write(f"CRITICAL DB ERROR: Could not create tables: {e}\n")

    def execute_query(self, query, params=(), fetch=None):
        if not self.conn: return None if fetch else False
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            if fetch == 'one': result = cursor.fetchone()
            elif fetch == 'all': result = cursor.fetchall()
            else: result = True
            self.conn.commit()
            return result
        except sqlite3.Error as e:
            self.logger(f"DB Error on query '{query}': {e}")
            return None if fetch else False

    def get_all_notes(self):
        rows = self.execute_query("SELECT id, title, parent_id FROM notes ORDER BY title COLLATE NOCASE", fetch='all')
        return [dict(row) for row in rows] if rows else []

    def get_note(self, note_id: str):
        row = self.execute_query("SELECT * FROM notes WHERE id = ?", (note_id,), fetch='one')
        return dict(row) if row else None

    def search_notes(self, term: str):
        like_term = f'%{term}%'
        query = "SELECT id, title, parent_id FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY title COLLATE NOCASE"
        rows = self.execute_query(query, (like_term, like_term), fetch='all')
        return [dict(row) for row in rows] if rows else []

    def get_tags_for_note(self, note_id: str):
        query = "SELECT t.name FROM tags t JOIN note_tags nt ON t.id = nt.tag_id WHERE nt.note_id = ?"
        rows = self.execute_query(query, (note_id,), fetch='all')
        return [row['name'] for row in rows] if rows else []

    def get_all_unique_tags(self):
        rows = self.execute_query("SELECT name FROM tags ORDER BY name COLLATE NOCASE", fetch='all')
        return [row['name'] for row in rows] if rows else []

    def get_notes_for_tag(self, tag_name: str):
        query = """
            SELECT n.id, n.title, n.parent_id FROM notes n
            JOIN note_tags nt ON n.id = nt.note_id
            JOIN tags t ON nt.tag_id = t.id
            WHERE t.name = ?
            ORDER BY n.title COLLATE NOCASE
        """
        rows = self.execute_query(query, (tag_name,), fetch='all')
        return [dict(row) for row in rows] if rows else []

    def update_note_tags(self, note_id: str, tags: list[str]):
        self.execute_query("DELETE FROM note_tags WHERE note_id = ?", (note_id,))
        for tag_name in tags:
            tag_name = tag_name.strip().lower()
            if not tag_name: continue
            tag_row = self.execute_query("SELECT id FROM tags WHERE name = ?", (tag_name,), fetch='one')
            if not tag_row:
                self.execute_query("INSERT INTO tags (name) VALUES (?)", (tag_name,))
                tag_id = self.execute_query("SELECT last_insert_rowid()", fetch='one')[0]
            else:
                tag_id = tag_row['id']
            self.execute_query("INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))
        return True

# --- 5. Note Manager (Central Orchestrator) ---
class NoteManager:
    """Orchestrates interactions between the GUI, data structures, and database."""
    def __init__(self, db_name="zettelkasten_obsidian.db", logger_callback=None):
        self.logger = logger_callback if logger_callback else print
        self.db = NoteDatabase(db_name, self.logger)
        if not self.db.conn: raise RuntimeError("Database initialization failed.")

        self.graph = Graph(self.logger)
        self.navigation_history = NoteNavigationStack(self.logger)
        self.recent_notes = CircularDoublyLinkedNotesList(logger_callback=self.logger)

        self._load_initial_data()

    def _load_initial_data(self):
        notes = self.db.get_all_notes()
        for note in notes:
            self.graph.add_note(note['id'])
        links = self.db.execute_query("SELECT source_note_id, target_note_id FROM note_links", fetch='all')
        if links:
            for link in links:
                self.graph.add_link(link['source_note_id'], link['target_note_id'])
        self.logger("Manager: Initial data loaded.")

    def create_note(self, title: str, content: str = "", parent_id: str = None):
        new_id = str(uuid.uuid4())
        if self.db.execute_query("INSERT INTO notes (id, title, content, parent_id) VALUES (?, ?, ?, ?)", (new_id, title, content, parent_id)):
            self.graph.add_note(new_id)
            return new_id
        return None

    def get_note_with_tags(self, note_id: str):
        note = self.db.get_note(note_id)
        if note:
            note = dict(note)
            note['tags'] = self.db.get_tags_for_note(note_id)
            self.navigation_history.visit_note(note_id)
            self.recent_notes.insert_note(Note(note['id'], note['title']))
            return note
        return None

    def update_note(self, note_id: str, title: str, content: str, tags: list[str]):
        if self.db.execute_query("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id)):
            return self.db.update_note_tags(note_id, tags)
        return False

    def delete_note(self, note_id: str):
        if self.db.execute_query("DELETE FROM notes WHERE id = ?", (note_id,)):
            self.graph.remove_note(note_id)
            self.recent_notes.remove_note_by_id(note_id)
            return True
        return False

    def link_notes(self, note1_id: str, note2_id: str):
        if self.db.execute_query("INSERT OR IGNORE INTO note_links VALUES (?, ?)", (note1_id, note2_id)) and \
           self.db.execute_query("INSERT OR IGNORE INTO note_links VALUES (?, ?)", (note2_id, note1_id)):
            self.graph.add_link(note1_id, note2_id)
            return True
        return False

    def unlink_notes(self, note1_id: str, note2_id: str):
        if self.db.execute_query("DELETE FROM note_links WHERE (source_note_id=? AND target_note_id=?) OR (source_note_id=? AND target_note_id=?)", (note1_id, note2_id, note2_id, note1_id)):
            self.graph.remove_link(note1_id, note2_id)
            return True
        return False

    def get_related_notes(self, note_id: str):
        related_ids = self.graph.get_connected_notes(note_id)
        return [self.db.get_note(r_id) for r_id in related_ids if self.db.get_note(r_id)]

    def close(self):
        self.db.disconnect()
        self.logger("Manager: Application shutting down.")

# --- 6. Custom Logger ---
class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
    def write(self, str_input):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, str_input, (self.tag,))
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')
    def flush(self): pass

# --- 7. Main Tkinter GUI Application ---
class ZettelkastenApp(tk.Tk):
    """Main application GUI, built with standard Tkinter and ttk."""
    def __init__(self):
        super().__init__()

        self.FONT_FAMILY = "Segoe UI"
        self.title("Zettelkasten Note Manager")
        self.geometry("1600x900")
        self.configure(bg="#2B2B2B")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=300)
        self.grid_columnconfigure(1, weight=3, minsize=600)
        self.grid_columnconfigure(2, weight=1, minsize=300)

        self._setup_logger()
        # FIX: Assign self.logger before other methods use it
        self.logger = self.logger_write
        try:
            self.note_manager = NoteManager(logger_callback=self.logger)
        except RuntimeError as e:
            messagebox.showerror("Fatal Error", f"Application could not start: {e}")
            self.destroy(); return

        self._gui_current_note_id = None
        self._create_widgets()
        self._load_notes_tree()
        self._load_tags_pane()
        self._setup_keyboard_shortcuts()
        self._update_treeview_style()

    def _setup_logger(self):
        self.log_text_widget = scrolledtext.ScrolledText(self, height=8, wrap=tk.WORD,
                                                         bg="#313335", fg="#A9B7C6",
                                                         font=(self.FONT_FAMILY, 10),
                                                         bd=0, relief=tk.FLAT, state='disabled')
        self.log_text_widget.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=(5,10))
        self.log_text_widget.tag_config("stdout", foreground="#6A8759")
        self.log_text_widget.tag_config("error", foreground="#D32F2F")
        sys.stdout = TextRedirector(self.log_text_widget, "stdout")
        sys.stderr = TextRedirector(self.log_text_widget, "error")

    def logger_write(self, message):
        timestamp = time.strftime("%H:%M:%S")
        sys.stdout.write(f"[{timestamp}] {message}\n")

    def _create_widgets(self):
        # --- Left Pane ---
        left_pane = tk.Frame(self, bg="#2B2B2B")
        left_pane.grid(row=0, column=0, sticky="nsew", padx=(10, 2))
        left_pane.grid_rowconfigure(2, weight=1)
        left_pane.grid_rowconfigure(4, weight=1)
        left_pane.grid_columnconfigure(0, weight=1)

        control_frame = tk.Frame(left_pane, bg="#2B2B2B")
        control_frame.grid(row=0, column=0, sticky="ew", pady=10)

        add_note_btn = tk.Button(control_frame, text="New", command=self._add_note)
        add_note_btn.pack(side=tk.LEFT, padx=(0,5))
        self.back_btn = tk.Button(control_frame, text="←", command=self._go_back)
        self.back_btn.pack(side=tk.LEFT, padx=5)
        self.forward_btn = tk.Button(control_frame, text="→", command=self._go_forward)
        self.forward_btn.pack(side=tk.LEFT, padx=5)
        delete_note_btn = tk.Button(control_frame, text="Delete", command=self._delete_selected_note, bg="#D32F2F", fg="white")
        delete_note_btn.pack(side=tk.LEFT, padx=5)

        self.search_entry = ttk.Entry(left_pane, font=(self.FONT_FAMILY, 10))
        self.search_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._search_notes)

        self.notes_tree = ttk.Treeview(left_pane, show="tree")
        self.notes_tree.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.notes_tree.bind("<<TreeviewSelect>>", self._on_note_select)

        tags_label_frame = tk.LabelFrame(left_pane, text="Tags", bg="#2B2B2B", fg="#A9B7C6")
        tags_label_frame.grid(row=4, column=0, sticky="nsew", pady=(0, 10))
        self.tags_frame = tk.Frame(tags_label_frame, bg="#313335")
        self.tags_frame.pack(fill="both", expand=True)

        # --- Middle Pane ---
        editor_pane = tk.Frame(self, bg="#2B2B2B")
        editor_pane.grid(row=0, column=1, sticky="nsew", padx=5)
        editor_pane.grid_rowconfigure(1, weight=1)
        editor_pane.grid_columnconfigure(0, weight=1)

        editor_top_frame = tk.Frame(editor_pane, bg="#2B2B2B")
        editor_top_frame.grid(row=0, column=0, sticky="ew", pady=10)
        editor_top_frame.grid_columnconfigure(0, weight=1)

        self.note_title_entry = tk.Entry(editor_top_frame, font=(self.FONT_FAMILY, 18, "bold"), bg="#313335", fg="#A9B7C6", relief=tk.FLAT)
        self.note_title_entry.grid(row=0, column=0, sticky="ew")

        save_btn = tk.Button(editor_top_frame, text="Save", command=self._save_note)
        save_btn.grid(row=0, column=1, padx=(10, 0))

        self.note_content_text = scrolledtext.ScrolledText(editor_pane, font=(self.FONT_FAMILY, 12), wrap=tk.WORD, bg="#2B2B2B", fg="#A9B7C6", relief=tk.FLAT, bd=0)
        self.note_content_text.grid(row=1, column=0, sticky="nsew")

        self.tags_entry = tk.Entry(editor_pane, font=(self.FONT_FAMILY, 10), bg="#313335", fg="#A9B7C6", relief=tk.FLAT)
        self.tags_entry.grid(row=2, column=0, sticky="ew", pady=(2, 0))

        # --- Right Pane ---
        right_pane = tk.Frame(self, bg="#2B2B2B")
        right_pane.grid(row=0, column=2, sticky="nsew", padx=(2, 10))
        right_pane.grid_rowconfigure(1, weight=1)
        right_pane.grid_rowconfigure(3, weight=1)
        right_pane.grid_columnconfigure(0, weight=1)

        context_button_frame = tk.Frame(right_pane, bg="#2B2B2B")
        context_button_frame.grid(row=0, column=0, sticky="ew", pady=10)

        link_btn = tk.Button(context_button_frame, text="Link to Note", command=self._link_notes_dialog)
        link_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,5))
        visualize_btn = tk.Button(context_button_frame, text="Visualize Graph", command=self._visualize_graph)
        visualize_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5,0))

        linked_label_frame = tk.LabelFrame(right_pane, text="Linked Notes", bg="#2B2B2B", fg="#A9B7C6")
        linked_label_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.linked_notes_frame = tk.Frame(linked_label_frame, bg="#313335")
        self.linked_notes_frame.pack(fill="both", expand=True)

        recent_label_frame = tk.LabelFrame(right_pane, text="Recently Viewed", bg="#2B2B2B", fg="#A9B7C6")
        recent_label_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        self.recent_notes_frame = tk.Frame(recent_label_frame, bg="#313335")
        self.recent_notes_frame.pack(fill="both", expand=True)

    def _setup_keyboard_shortcuts(self):
        self.bind("<Control-s>", lambda event: self._save_note())
        self.bind("<Control-n>", lambda event: self._add_note())
        self.bind("<Control-f>", lambda event: self.search_entry.focus())
        self.logger("Shortcuts: Ctrl+S (Save), Ctrl+N (New), Ctrl+F (Search) are active.")

    def _update_treeview_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#313335", foreground="#A9B7C6", fieldbackground="#313335", borderwidth=0, font=(self.FONT_FAMILY, 10))
        style.map('Treeview', background=[('selected', '#4A90E2')], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading", background="#3C3F41", foreground="#A9B7C6", font=(self.FONT_FAMILY, 10, 'bold'), borderwidth=0)

    def _load_notes_tree(self, notes_list=None):
        for i in self.notes_tree.get_children(): self.notes_tree.delete(i)
        notes = notes_list if notes_list is not None else self.note_manager.db.get_all_notes()
        self.note_map = {note['id']: note for note in notes}

        children_map = collections.defaultdict(list)
        root_notes = []
        for note_id, note in self.note_map.items():
            parent_id = note.get('parent_id')
            if parent_id in self.note_map: children_map[parent_id].append(note_id)
            else: root_notes.append(note_id)

        def insert_children(parent_node, children_ids):
            for child_id in sorted(children_ids, key=lambda x: self.note_map[x]['title']):
                child_note = self.note_map[child_id]
                child_node_id = self.notes_tree.insert(parent_node, 'end', text=f"  {child_note['title']}", iid=child_id, open=True)
                if child_id in children_map: insert_children(child_node_id, children_map[child_id])

        for note_id in sorted(root_notes, key=lambda x: self.note_map[x]['title']):
            note = self.note_map[note_id]
            node_id_tree = self.notes_tree.insert('', 'end', text=note['title'], iid=note_id, open=True)
            if note_id in children_map: insert_children(node_id_tree, children_map[note_id])

    def _load_tags_pane(self):
        for widget in self.tags_frame.winfo_children(): widget.destroy()
        all_btn = tk.Button(self.tags_frame, text="All Notes", anchor="w", command=lambda: self._load_notes_tree())
        all_btn.pack(fill="x", padx=5, pady=2)
        for tag in self.note_manager.db.get_all_unique_tags():
            btn = tk.Button(self.tags_frame, text=f"#{tag}", anchor="w", command=lambda t=tag: self._filter_by_tag(t))
            btn.pack(fill="x", padx=5, pady=2)

    def _filter_by_tag(self, tag_name):
        notes = self.note_manager.db.get_notes_for_tag(tag_name)
        self._load_notes_tree(notes)
        self.logger(f"Filter: Showing notes with tag '{tag_name}'.")

    def _clear_editor(self):
        self._gui_current_note_id = None
        self.note_title_entry.delete(0, 'end')
        self.note_content_text.delete("1.0", 'end')
        self.tags_entry.delete(0, 'end')
        self.title("Zettelkasten Note Manager")
        self._load_linked_notes_list(None)
        self._load_recent_notes_list()

    def _display_note_in_editor(self, note_id: str):
        note = self.note_manager.get_note_with_tags(note_id)
        if note:
            self._gui_current_note_id = note['id']
            self.note_title_entry.delete(0, 'end')
            self.note_title_entry.insert(0, note['title'])

            self.note_content_text.delete("1.0", 'end')
            self.note_content_text.insert("1.0", note['content'] or "")

            self.tags_entry.delete(0, 'end')
            self.tags_entry.insert(0, ", ".join(note['tags']))
            self.title(f"{note['title']} - Zettelkasten")
            self._load_linked_notes_list(note_id)
            self._load_recent_notes_list()
            self._update_nav_buttons()
        else:
            self._clear_editor()

    def _load_linked_notes_list(self, note_id):
        for widget in self.linked_notes_frame.winfo_children(): widget.destroy()
        if not note_id: return
        related_notes = self.note_manager.get_related_notes(note_id)
        if not related_notes:
            tk.Label(self.linked_notes_frame, text="No linked notes.", bg="#313335", fg="#A9B7C6").pack(pady=5)
            return
        for note in related_notes:
            btn = tk.Button(self.linked_notes_frame, text=note['title'], anchor="w", command=lambda n_id=note['id']: self._on_context_note_click(n_id))
            btn.pack(fill="x", pady=2)

    def _load_recent_notes_list(self):
        for widget in self.recent_notes_frame.winfo_children(): widget.destroy()
        recent_notes = self.note_manager.recent_notes.get_recent_notes()
        if not recent_notes:
            tk.Label(self.recent_notes_frame, text="No recent notes.", bg="#313335", fg="#A9B7C6").pack(pady=5)
            return
        for note in recent_notes:
            btn = tk.Button(self.recent_notes_frame, text=note.title, anchor="w", command=lambda n_id=note.id: self._on_context_note_click(n_id))
            btn.pack(fill="x", pady=2)

    def _on_context_note_click(self, note_id):
        self.notes_tree.selection_set(note_id)
        self.notes_tree.see(note_id)
        self._display_note_in_editor(note_id)

    def _on_note_select(self, event=None):
        selected_ids = self.notes_tree.selection()
        if not selected_ids: return
        self._display_note_in_editor(selected_ids[0])

    def _add_note(self):
        parent_id = self.notes_tree.selection()[0] if self.notes_tree.selection() else None
        title = simpledialog.askstring("New Note", "Enter note title:", parent=self)
        if title:
            new_id = self.note_manager.create_note(title, "", parent_id)
            if new_id:
                self._load_notes_tree()
                self._load_tags_pane()
                self.notes_tree.selection_set(new_id)
                self.notes_tree.see(new_id)
                self._display_note_in_editor(new_id)
            else:
                messagebox.showerror("Error", "Failed to add note.")

    def _save_note(self):
        if not self._gui_current_note_id: return
        content = self.note_content_text.get("1.0", tk.END).strip()
        title = self.note_title_entry.get().strip()
        tags = [tag.strip() for tag in self.tags_entry.get().split(',') if tag.strip()]
        if not title:
            messagebox.showerror("Input Error", "Title cannot be empty.")
            return
        if self.note_manager.update_note(self._gui_current_note_id, title, content, tags):
            self.logger_write(f"GUI: Note '{title}' saved.")
            self._load_notes_tree()
            self._load_tags_pane()
            self.notes_tree.selection_set(self._gui_current_note_id)
        else:
            messagebox.showerror("Error", "Failed to update note.")

    def _delete_selected_note(self):
        selected_ids = self.notes_tree.selection()
        if not selected_ids:
            messagebox.showwarning("No Selection", "Please select a note to delete.")
            return
        note_id = selected_ids[0]
        note_title = self.note_map[note_id]['title']
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{note_title}'?"):
            if self.note_manager.delete_note(note_id):
                self._load_notes_tree()
                self._load_tags_pane()
                self._clear_editor()
            else:
                messagebox.showerror("Error", "Failed to delete note.")

    def _search_notes(self, event=None):
        search_term = self.search_entry.get().strip()
        self._load_notes_tree(self.note_manager.db.search_notes(search_term))

    def _link_notes_dialog(self):
        if not self._gui_current_note_id:
            messagebox.showwarning("No Note Selected", "Please select a note to link from.")
            return
        dialog = tk.Toplevel(self)
        dialog.title("Link Note")
        dialog.geometry("350x450")
        dialog.transient(self)
        dialog.grab_set()
        tk.Label(dialog, text=f"Select note to link to:").pack(pady=10)
        frame = tk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        listbox = tk.Listbox(frame, bg="#313335", fg="#A9B7C6", selectbackground="#4A90E2", borderwidth=0, highlightthickness=0)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.configure(yscrollcommand=scrollbar.set)
        all_notes = self.note_manager.db.get_all_notes()
        note_map = {}
        for note in all_notes:
            if note['id'] != self._gui_current_note_id:
                listbox.insert(tk.END, note['title'])
                note_map[listbox.size() - 1] = note['id']
        def perform_link():
            selected_indices = listbox.curselection()
            if not selected_indices: return
            target_note_id = note_map[selected_indices[0]]
            if self.note_manager.link_notes(self._gui_current_note_id, target_note_id):
                self._load_linked_notes_list(self._gui_current_note_id)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to link notes.", parent=dialog)
        tk.Button(dialog, text="Link", command=perform_link).pack(pady=10)

    def _go_back(self):
        note_id = self.note_manager.navigation_history.go_back()
        if note_id:
            self._display_note_in_editor(note_id)
            self.notes_tree.selection_set(note_id)
            self.notes_tree.see(note_id)
        else:
            self.logger_write("GUI: No previous notes in history.")
        self._update_nav_buttons()

    def _go_forward(self):
        note_id = self.note_manager.navigation_history.go_forward()
        if note_id:
            self._display_note_in_editor(note_id)
            self.notes_tree.selection_set(note_id)
            self.notes_tree.see(note_id)
        else:
            self.logger_write("GUI: No next notes in history.")
        self._update_nav_buttons()

    def _update_nav_buttons(self):
        back_state = "normal" if self.note_manager.navigation_history.previous_notes else "disabled"
        forward_state = "normal" if self.note_manager.navigation_history.next_notes else "disabled"
        self.back_btn.config(state=back_state)
        self.forward_btn.config(state=forward_state)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.note_manager.close()
            self.destroy()

    def _visualize_graph(self):
        """Creates a new window and displays the note graph."""
        graph_window = tk.Toplevel(self)
        graph_window.title("Note Graph Visualization")
        graph_window.geometry("800x600")
        graph_window.transient(self)
        graph_window.grab_set()

        G = nx.Graph()
        all_notes = self.note_manager.db.get_all_notes()

        labels = {note['id']: (note['title'][:15] + '...' if len(note['title']) > 15 else note['title']) for note in all_notes}

        for note in all_notes:
            G.add_node(note['id'])

        for note_id, connections in self.note_manager.graph.graph.items():
            for connected_id in connections:
                G.add_edge(note_id, connected_id)

        fig, ax = plt.subplots(facecolor='#2B2B2B')
        pos = nx.spring_layout(G, k=0.5, iterations=50)

        nx.draw_networkx_nodes(G, pos, node_color='#4A90E2', node_size=1500, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color='#A9B7C6', width=1.0, alpha=0.7, ax=ax)
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='white', ax=ax)

        ax.set_facecolor('#2B2B2B')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    try:
        app = ZettelkastenApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        import traceback
        messagebox.showerror("Fatal Startup Error", f"An unexpected error occurred: {e}\n\n{traceback.format_exc()}")

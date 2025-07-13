import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import customtkinter as ctk
import sqlite3
import uuid
import collections
import sys
import time
import re
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Note: This application requires the 'customtkinter', 'networkx', and 'matplotlib' libraries.
# Install them using: pip install customtkinter networkx matplotlib

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


# --- 2. SQLite Database Manager ---
# This class also contains the implementation for the Hash Map (Tags) by Kindness.
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
            # This table supports the Tree structure by Jeremy.
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
            # --- Hash Map Implementation by Kindness ---
            # The 'tags' and 'note_tags' tables create a persistent hash map where:
            # Key: the tag name (e.g., 'python')
            # Value: a list of note IDs associated with that tag.
            # The database's indexing provides the fast O(1) average lookup time.
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
            if fetch == 'one':
                result = cursor.fetchone()
            elif fetch == 'all':
                result = cursor.fetchall()
            else:
                result = True
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
        rows = self.execute_query(
            "SELECT id, title, parent_id FROM notes WHERE title LIKE ? ORDER BY title COLLATE NOCASE", (f'%{term}%',),
            fetch='all')
        return [dict(row) for row in rows] if rows else []

    # --- Hash Map Methods by Kindness ---
    def get_tags_for_note(self, note_id: str):
        """Retrieves all tags (keys) for a given note."""
        query = "SELECT t.name FROM tags t JOIN note_tags nt ON t.id = nt.tag_id WHERE nt.note_id = ?"
        rows = self.execute_query(query, (note_id,), fetch='all')
        return [row['name'] for row in rows] if rows else []

    def update_note_tags(self, note_id: str, tags: list[str]):
        """Updates the tag mappings for a note, acting as the 'set' method of the hash map."""
        self.execute_query("DELETE FROM note_tags WHERE note_id = ?", (note_id,))
        for tag_name in tags:
            tag_name = tag_name.strip().lower()
            if not tag_name: continue
            # Get or create the key (tag)
            tag_row = self.execute_query("SELECT id FROM tags WHERE name = ?", (tag_name,), fetch='one')
            if not tag_row:
                self.execute_query("INSERT INTO tags (name) VALUES (?)", (tag_name,))
                tag_id = self.execute_query("SELECT last_insert_rowid()", fetch='one')[0]
            else:
                tag_id = tag_row['id']
            # Map the key to the value (note)
            self.execute_query("INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))
        return True


# --- 3. Note Manager (Central Orchestrator) ---
class NoteManager:
    """Orchestrates interactions between the GUI, data structures, and database."""

    def __init__(self, db_name="zettelkasten_obsidian.db", logger_callback=None):
        self.logger = logger_callback if logger_callback else print
        self.db = NoteDatabase(db_name, self.logger)
        if not self.db.conn: raise RuntimeError("Database initialization failed.")
        self.graph = Graph(self.logger)
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
        if self.db.execute_query("INSERT INTO notes (id, title, content, parent_id) VALUES (?, ?, ?, ?)",
                                 (new_id, title, content, parent_id)):
            self.graph.add_note(new_id)
            return new_id
        return None

    def get_note_with_tags(self, note_id: str):
        note = self.db.get_note(note_id)
        if note:
            note = dict(note)
            note['tags'] = self.db.get_tags_for_note(note_id)
            return note
        return None

    def update_note(self, note_id: str, title: str, content: str, tags: list[str]):
        if self.db.execute_query("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id)):
            return self.db.update_note_tags(note_id, tags)
        return False

    def delete_note(self, note_id: str):
        if self.db.execute_query("DELETE FROM notes WHERE id = ?", (note_id,)):
            self.graph.remove_note(note_id)
            return True
        return False

    def link_notes(self, note1_id: str, note2_id: str):
        if self.db.execute_query("INSERT OR IGNORE INTO note_links VALUES (?, ?)", (note1_id, note2_id)) and \
                self.db.execute_query("INSERT OR IGNORE INTO note_links VALUES (?, ?)", (note2_id, note1_id)):
            self.graph.add_link(note1_id, note2_id)
            return True
        return False

    def unlink_notes(self, note1_id: str, note2_id: str):
        if self.db.execute_query(
                "DELETE FROM note_links WHERE (source_note_id=? AND target_note_id=?) OR (source_note_id=? AND target_note_id=?)",
                (note1_id, note2_id, note2_id, note1_id)):
            self.graph.remove_link(note1_id, note2_id)
            return True
        return False

    def get_related_notes(self, note_id: str):
        related_ids = self.graph.get_connected_notes(note_id)
        return [self.db.get_note(r_id) for r_id in related_ids if self.db.get_note(r_id)]

    def close(self):
        self.db.disconnect()
        self.logger("Manager: Application shutting down.")


# --- 4. Custom Logger ---
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


# --- 5. Advanced GUI with CustomTkinter ---
class ZettelkastenApp(ctk.CTk):
    """
    Main application GUI, built with CustomTkinter for a modern look.
    Note on other data structures:
    - Stack by Aoi: This functionality is implicitly handled by the call stack during
      the recursive rendering of the note tree. There is no explicit Stack class for navigation.
    - Linked List by Austin: This functionality for "Recent Notes" is not present in this
      Obsidian-style implementation, which prioritizes the hierarchical tree view.
    """

    def __init__(self):
        super().__init__()

        # --- Theme and Style ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.FONT_FAMILY = "Segoe UI"

        self.title("Zettelkasten Note Manager")
        self.geometry("1600x900")

        # --- Grid Layout ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=300)
        self.grid_columnconfigure(1, weight=3, minsize=600)
        self.grid_columnconfigure(2, weight=1, minsize=300)  # Right pane for context

        # --- Initialize Manager and Logger ---
        self._setup_logger()
        try:
            self.note_manager = NoteManager(logger_callback=self.logger_write)
        except RuntimeError as e:
            messagebox.showerror("Fatal Error", f"Application could not start: {e}")
            self.destroy();
            return

        self._gui_current_note_id = None
        self._create_widgets()
        self._load_notes_tree()

    def _setup_logger(self):
        self.log_text_widget = ctk.CTkTextbox(self, height=100, corner_radius=0,
                                              font=(self.FONT_FAMILY, 11), state='disabled')
        self.log_text_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.log_text_widget.tag_config("stdout", foreground="#6A8759")
        self.log_text_widget.tag_config("error", foreground="#D32F2F")
        sys.stdout = TextRedirector(self.log_text_widget, "stdout")
        sys.stderr = TextRedirector(self.log_text_widget, "error")

    def logger_write(self, message):
        timestamp = time.strftime("%H:%M:%S")
        sys.stdout.write(f"[{timestamp}] {message}\n")

    def _create_widgets(self):
        # --- Left Pane: Note Tree and Controls ---
        left_pane = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        left_pane.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        left_pane.grid_rowconfigure(2, weight=1)
        left_pane.grid_columnconfigure(0, weight=1)

        control_frame = ctk.CTkFrame(left_pane, fg_color="transparent")
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        control_frame.grid_columnconfigure(1, weight=1)

        add_note_btn = ctk.CTkButton(control_frame, text="New Note", command=self._add_note)
        add_note_btn.grid(row=0, column=0, padx=(0, 5))
        delete_note_btn = ctk.CTkButton(control_frame, text="Delete", command=self._delete_selected_note,
                                        fg_color="#D32F2F", hover_color="#B71C1C")
        delete_note_btn.grid(row=0, column=2, padx=(5, 0))

        self.search_entry = ctk.CTkEntry(left_pane, placeholder_text="Search notes...")
        self.search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._search_notes)

        # --- Tree Data Structure by Jeremy ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#313335", foreground="#A9B7C6", fieldbackground="#313335",
                        borderwidth=0, font=(self.FONT_FAMILY, 10))
        style.map('Treeview', background=[('selected', '#4A90E2')], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading", background="#3C3F41", foreground="#A9B7C6",
                        font=(self.FONT_FAMILY, 10, 'bold'), borderwidth=0)

        self.notes_tree = ttk.Treeview(left_pane, show="tree")
        self.notes_tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.notes_tree.bind("<<TreeviewSelect>>", self._on_note_select)

        # --- Middle Pane: Note Editor ---
        editor_pane = ctk.CTkFrame(self, corner_radius=0)
        editor_pane.grid(row=0, column=1, sticky="nsew")
        editor_pane.grid_rowconfigure(1, weight=1)
        editor_pane.grid_columnconfigure(0, weight=1)

        editor_top_frame = ctk.CTkFrame(editor_pane, fg_color="transparent")
        editor_top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        editor_top_frame.grid_columnconfigure(0, weight=1)

        self.note_title_entry = ctk.CTkEntry(editor_top_frame, font=(self.FONT_FAMILY, 18, "bold"),
                                             placeholder_text="Note Title")
        self.note_title_entry.grid(row=0, column=0, sticky="ew")

        save_btn = ctk.CTkButton(editor_top_frame, text="Save", command=self._save_note, width=80)
        save_btn.grid(row=0, column=1, padx=(10, 0))

        self.note_content_text = ctk.CTkTextbox(editor_pane, corner_radius=0, font=(self.FONT_FAMILY, 12), wrap="word",
                                                fg_color="#2B2B2B", border_width=0)
        self.note_content_text.grid(row=1, column=0, sticky="nsew")

        self.tags_entry = ctk.CTkEntry(editor_pane, placeholder_text="Add tags, comma-separated...", corner_radius=0)
        self.tags_entry.grid(row=2, column=0, sticky="ew", pady=(2, 0))

        # --- Right Pane: Context (Linked Notes) ---
        right_pane = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        right_pane.grid(row=0, column=2, sticky="nsew", padx=(2, 0))
        right_pane.grid_rowconfigure(2, weight=1)  # Updated row configure for new buttons
        right_pane.grid_columnconfigure(0, weight=1)

        context_button_frame = ctk.CTkFrame(right_pane, fg_color="transparent")
        context_button_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        context_button_frame.grid_columnconfigure((0, 1), weight=1)

        link_btn = ctk.CTkButton(context_button_frame, text="Link to Note", command=self._link_notes_dialog)
        link_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        visualize_btn = ctk.CTkButton(context_button_frame, text="Visualize Graph", command=self._visualize_graph)
        visualize_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        self.linked_notes_frame = ctk.CTkScrollableFrame(right_pane, label_text="Linked Notes")
        self.linked_notes_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def _visualize_graph(self):
        """Creates a new window and displays the note graph."""
        graph_window = ctk.CTkToplevel(self)
        graph_window.title("Note Graph Visualization")
        graph_window.geometry("800x600")
        graph_window.transient(self)
        graph_window.grab_set()

        G = nx.Graph()
        all_notes = self.note_manager.db.get_all_notes()

        # Use a shorter label for nodes to avoid clutter
        labels = {note['id']: (note['title'][:15] + '...' if len(note['title']) > 15 else note['title']) for note in
                  all_notes}

        for note in all_notes:
            G.add_node(note['id'])

        for note_id, connections in self.note_manager.graph.graph.items():
            for connected_id in connections:
                G.add_edge(note_id, connected_id)

        fig, ax = plt.subplots(facecolor='#2B2B2B')
        pos = nx.spring_layout(G, k=0.5, iterations=50)  # Increase k for more spread

        # Style the graph
        nx.draw_networkx_nodes(G, pos, node_color='#4A90E2', node_size=1500, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color='#A9B7C6', width=1.0, alpha=0.7, ax=ax)
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='white', ax=ax)

        ax.set_facecolor('#2B2B2B')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _load_notes_tree(self, search_term=None):
        for i in self.notes_tree.get_children(): self.notes_tree.delete(i)

        notes = self.note_manager.db.search_notes(search_term) if search_term else self.note_manager.db.get_all_notes()
        self.note_map = {note['id']: note for note in notes}

        children_map = collections.defaultdict(list)
        root_notes = []
        for note_id, note in self.note_map.items():
            parent_id = note.get('parent_id')
            if parent_id in self.note_map:
                children_map[parent_id].append(note_id)
            else:
                root_notes.append(note_id)

        def insert_children(parent_node, children_ids):
            for child_id in sorted(children_ids, key=lambda x: self.note_map[x]['title']):
                child_note = self.note_map[child_id]
                child_node_id = self.notes_tree.insert(parent_node, 'end', text=f"  {child_note['title']}",
                                                       iid=child_id, open=True)
                if child_id in children_map: insert_children(child_node_id, children_map[child_id])

        for note_id in sorted(root_notes, key=lambda x: self.note_map[x]['title']):
            note = self.note_map[note_id]
            node_id_tree = self.notes_tree.insert('', 'end', text=note['title'], iid=note_id, open=True)
            if note_id in children_map: insert_children(node_id_tree, children_map[note_id])

    def _clear_editor(self):
        self._gui_current_note_id = None
        self.note_title_entry.delete(0, 'end')
        self.note_content_text.configure(state='normal')
        self.note_content_text.delete("1.0", 'end')
        self.tags_entry.delete(0, 'end')
        self.title("Zettelkasten Note Manager")
        self._load_linked_notes_list(None)

    def _display_note_in_editor(self, note_id: str):
        note = self.note_manager.get_note_with_tags(note_id)
        if note:
            self._gui_current_note_id = note['id']
            self.note_title_entry.delete(0, 'end')
            self.note_title_entry.insert(0, note['title'])

            self.note_content_text.configure(state='normal')
            self.note_content_text.delete("1.0", 'end')
            self.note_content_text.insert("1.0", note['content'] or "")

            self.tags_entry.delete(0, 'end')
            self.tags_entry.insert(0, ", ".join(note['tags']))
            self.title(f"{note['title']} - Zettelkasten")
            self._load_linked_notes_list(note_id)
        else:
            self._clear_editor()

    def _load_linked_notes_list(self, note_id):
        # Clear existing widgets
        for widget in self.linked_notes_frame.winfo_children():
            widget.destroy()

        if not note_id: return

        related_notes = self.note_manager.get_related_notes(note_id)
        if not related_notes:
            ctk.CTkLabel(self.linked_notes_frame, text="No linked notes.").pack(pady=5)
            return

        for note in related_notes:
            frame = ctk.CTkFrame(self.linked_notes_frame, fg_color="transparent")
            frame.pack(fill="x", pady=(0, 2))

            btn = ctk.CTkButton(frame, text=note['title'], anchor="w", fg_color="transparent",
                                command=lambda n_id=note['id']: self._on_linked_note_click(n_id))
            btn.pack(side="left", fill="x", expand=True)

            unlink_btn = ctk.CTkButton(frame, text="x", width=20, fg_color="#555555",
                                       command=lambda n1=note_id, n2=note['id']: self._unlink_note(n1, n2))
            unlink_btn.pack(side="right")

    def _on_linked_note_click(self, note_id):
        self.notes_tree.selection_set(note_id)
        self.notes_tree.see(note_id)
        self._display_note_in_editor(note_id)

    def _unlink_note(self, note1_id, note2_id):
        if self.note_manager.unlink_notes(note1_id, note2_id):
            self._load_linked_notes_list(note1_id)
        else:
            messagebox.showerror("Error", "Failed to unlink note.")

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
                self._clear_editor()
            else:
                messagebox.showerror("Error", "Failed to delete note.")

    def _search_notes(self, event=None):
        search_term = self.search_entry.get().strip()
        self._load_notes_tree(search_term)

    def _link_notes_dialog(self):
        if not self._gui_current_note_id:
            messagebox.showwarning("No Note Selected", "Please select a note to link from.")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Link Note")
        dialog.geometry("350x450")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=f"Select note to link to:", font=(self.FONT_FAMILY, 12, "bold")).pack(pady=10)

        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        listbox = tk.Listbox(frame, bg="#313335", fg="#A9B7C6", selectbackground="#4A90E2", borderwidth=0,
                             highlightthickness=0)
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(frame, command=listbox.yview)
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

        ctk.CTkButton(dialog, text="Link", command=perform_link).pack(pady=10)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.note_manager.close()
            self.destroy()


if __name__ == "__main__":
    try:
        app = ZettelkastenApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        import traceback

        messagebox.showerror("Fatal Startup Error", f"An unexpected error occurred: {e}\n\n{traceback.format_exc()}")

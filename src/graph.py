# src/graph.py
"""
This module contains the Graph class for managing links between notes.
"""

class Graph:
    """
    A class to represent connections between notes using a directed graph.

    The graph is implemented using an adjacency list, which is a dictionary
    where keys are note IDs and values are lists of note IDs they link to.
    """

    def __init__(self):
        """
        Initializes the Graph with an empty adjacency list.
        """
        self.adj_list = {}

    def add_note(self, note_id: str) -> bool:
        """
        Adds a new note (vertex) to the graph.

        Args:
            note_id: The unique identifier for the note.

        Returns:
            True if the note was added successfully, False otherwise.
        """
        if note_id in self.adj_list:
            print(f"GRAPH_LOG: Attempted to add existing note '{note_id}'.")
            return False
        
        self.adj_list[note_id] = []
        print(f"GRAPH_LOG: Added note '{note_id}' to the graph.")
        return True

    def add_link(self, from_note_id: str, to_note_id: str) -> bool:
        """
        Adds a directed link (edge) from one note to another.

        Args:
            from_note_id: The ID of the note where the link originates.
            to_note_id: The ID of the note where the link terminates.

        Returns:
            True if the link was created successfully, False otherwise.
        """
        # Ensure both notes exist in the graph
        if from_note_id not in self.adj_list or to_note_id not in self.adj_list:
            print(f"GRAPH_LOG: Error: Cannot create link between non-existent notes.")
            return False

        # Prevent duplicate links
        if to_note_id in self.adj_list[from_note_id]:
            print(f"GRAPH_LOG: Link from '{from_note_id}' to '{to_note_id}' already exists.")
            return False

        self.adj_list[from_note_id].append(to_note_id)
        print(f"GRAPH_LOG: Linked note '{from_note_id}' -> '{to_note_id}'.")
        return True

    def remove_note(self, note_id: str) -> bool:
        """
        Removes a note and all of its associated links from the graph.

        Args:
            note_id: The unique identifier for the note to remove.

        Returns:
            True if the note was removed successfully, False if it did not exist.
        """
        if note_id not in self.adj_list:
            print(f"GRAPH_LOG: Attempted to remove non-existent note '{note_id}'.")
            return False

        # Delete the vertex itself
        del self.adj_list[note_id]

        # Remove all incoming edges to the deleted vertex
        for key in self.adj_list:
            self.adj_list[key] = [n_id for n_id in self.adj_list[key] if n_id != note_id]

        print(f"GRAPH_LOG: Removed note '{note_id}' and all its links.")
        return True

    def get_linked_notes(self, note_id: str) -> list:
        """
        Returns a list of note IDs linked from a given note.

        Args:
            note_id: The unique identifier for the note.

        Returns:
            A list of note IDs, or an empty list if the note has no links or doesn't exist.
        """
        return self.adj_list.get(note_id, [])

    def get_incoming_links(self, note_id: str) -> list:
        """
        Finds all notes that have a link TO the given note_id. This is useful
        for displaying "backlinks" in the UI.

        Args:
            note_id: The unique identifier for the note.

        Returns:
            A list of note IDs that link to the specified note.
        """
        incoming = []
        for key, links in self.adj_list.items():
            if note_id in links:
                incoming.append(key)
        return incoming

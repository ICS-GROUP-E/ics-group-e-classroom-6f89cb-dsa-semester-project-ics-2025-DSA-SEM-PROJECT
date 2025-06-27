# tests/test_graph.py
"""
This module contains unit tests for the Graph class.
It uses the pytest framework to ensure the Graph data structure
is correct, robust, and handles edge cases properly.
"""

import pytest
from src.graph import Graph  # Ensure your project structure allows this import

# Pytest fixture to create a pre-populated graph for testing
@pytest.fixture
def sample_graph():
    """Returns a Graph instance with some notes and links for testing."""
    g = Graph()
    g.add_note("note_A")
    g.add_note("note_B")
    g.add_note("note_C")
    g.add_link("note_A", "note_B")  # A -> B
    g.add_link("note_B", "note_C")  # B -> C
    g.add_link("note_A", "note_C")  # A -> C
    return g

# --- Test Class for Graph ---

class TestGraph:
    """Groups all tests related to the Graph data structure."""

    def test_init(self):
        """Test the graph is initialized correctly."""
        g = Graph()
        assert g.adj_list == {}

    def test_add_note(self):
        """Test adding a new, unique note."""
        g = Graph()
        assert g.add_note("new_note") is True
        assert "new_note" in g.adj_list
        assert g.adj_list["new_note"] == []

    def test_add_duplicate_note(self):
        """Test that adding a duplicate note fails."""
        g = Graph()
        g.add_note("new_note")
        assert g.add_note("new_note") is False

    def test_add_link(self, sample_graph):
        """Test adding a valid, unique link."""
        # The link A -> B is already in the fixture
        assert "note_B" in sample_graph.adj_list["note_A"]

    def test_add_duplicate_link(self, sample_graph):
        """Test that adding a duplicate link fails."""
        assert sample_graph.add_link("note_A", "note_B") is False

    def test_add_link_to_nonexistent_note(self):
        """Test linking from or to a note that doesn't exist."""
        g = Graph()
        g.add_note("note_A")
        assert g.add_link("note_A", "nonexistent") is False
        assert g.add_link("nonexistent", "note_A") is False

    def test_remove_note(self, sample_graph):
        """Test removing a note and all its connections."""
        sample_graph.remove_note("note_B")
        # Check that note_B is gone
        assert "note_B" not in sample_graph.adj_list
        # Check that the link A -> B is gone
        assert "note_B" not in sample_graph.adj_list["note_A"]
        
    def test_remove_nonexistent_note(self, sample_graph):
        """Test that removing a note that doesn't exist fails."""
        assert sample_graph.remove_note("nonexistent") is False

    def test_get_linked_notes(self, sample_graph):
        """Test retrieving all outgoing links from a note."""
        # Note A links to B and C
        linked = sample_graph.get_linked_notes("note_A")
        assert "note_B" in linked
        assert "note_C" in linked
        assert len(linked) == 2

    def test_get_linked_notes_for_nonexistent_note(self, sample_graph):
        """Test getting links for a note that doesn't exist."""
        assert sample_graph.get_linked_notes("nonexistent") == []

    def test_get_incoming_links(self, sample_graph):
        """Test retrieving all incoming links to a note."""
        # Note C receives links from A and B
        incoming = sample_graph.get_incoming_links("note_C")
        assert "note_A" in incoming
        assert "note_B" in incoming
        assert len(incoming) == 2

    def test_get_incoming_links_for_note_with_none(self, sample_graph):
        """Test getting incoming links for a note that has none."""
        assert sample_graph.get_incoming_links("note_A") == []


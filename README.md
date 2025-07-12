[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/__oZ-IAL)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19822520&assignment_repo_type=AssignmentRepo)
# DSA-SEM-PROJECT-
DATA STRUCTURES AND ALGORITHMS SEMESTER PROJECT

      README.md
Zettelkasten Note Manager
A desktop application for building a personal knowledge base, inspired by the Zettelkasten method and modern note-taking apps like Obsidian.

Overview
This application allows users to create, edit, and manage a network of interconnected notes. It provides a hierarchical view of notes, supports linking between notes to create a knowledge graph, and uses a tagging system for organization. The core of the application is built on fundamental data structures, demonstrating their practical application in a real-world project.

Features
Hierarchical Note Organization: Create notes within other notes to build a tree-like structure.

Note Linking: Create bi-directional links between notes to form a connected web of ideas.

Tagging System: Assign tags to notes for easy categorization and retrieval (Hash Map implementation).

Full-Text Search: Search for notes by title or content.

Graph Visualization: View a graphical representation of how your notes are interconnected.

Modern UI: Built with customtkinter for a clean, modern, and theme-able interface.

Persistent Storage: All notes, links, and tags are saved in an SQLite database.

Data Structures Used
Tree (Jeremy): Implemented using a ttk.Treeview widget, with the hierarchy managed through a parent_id relationship in the database. This allows for an intuitive, folder-like organization of notes.

Graph (Adrian): Implemented using a defaultdict as an adjacency list in the Graph class and visualized with networkx and matplotlib. This powers the core linking feature.

Hash Map (Kindness): Implemented using the SQLite database with two tables (tags and note_tags) to create a persistent, key-value mapping for tags to notes. This provides efficient tag-based lookups.

Stack (Aoi): In the final Obsidian-style version, explicit stack-based navigation was removed in favor of direct interaction with the note tree. However, the concept of a stack is implicitly used in the recursive function calls that build the tree view.

Linked List (Austin): The "Recently Viewed Notes" feature, which used a Linked List in earlier iterations, was removed in the final design to align more closely with the Obsidian-style interface, which prioritizes the persistent tree and graph structures.

Setup and Installation
Clone the repository:

git clone <your-repo-url>
cd <your-repo-directory>

Set up a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required libraries:

pip install customtkinter networkx matplotlib

Run Instructions
To run the application, execute the main Python script from the root of the project directory:

python your_main_script_name.py

Branch Conventions
Each student must create a feature branch named: regNo_<YourRegNo>_<ModuleName>

Example: regNo_P123456_graph

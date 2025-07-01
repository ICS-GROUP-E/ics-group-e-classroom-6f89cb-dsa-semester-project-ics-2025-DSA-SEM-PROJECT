#Stack implementation using Python list

"""
This class aims to allow the user to navigate through their notes history, that is, to keep track of
their previous note (previous_note), their current note being displayed and their next note (next_note).

Stacks is a LIFO data structure.
The current class implements forward and backward stacks.
Use of indexes to track the previous, current and next notes.
"""

class Navigation_history:
    def __init__(self,all_notes):
        self.all_notes = all_notes#Holds all the user's notes
        self.previous_note = [] #Creating empty stack lists
        self.next_note = []
        self.current_note = None

    def open(self,index):
        """
        Opening a note using its index . First checking if the index exists , that is,
        if the index used exists or not in the current list of notes
        """
        if index <0 or index >= len(self.all_notes):
            print("Note index is invalid.")
            return

        if self.current_note is not None:
            self.previous_note.append(self.current_note)
            self.next_note.clear()

        self.current_note = self.all_notes[index]
        self.display()

    def back_note(self):
        if self.current_note is not None:
            self.next_note.append(self.current_note)
            self.current_note = self.previous_note.pop()
            self.display()

    def forward_note(self):
        """
        The aim is to display the following note as the current note. This means moving the
        current note to the previous note stack and displaying the next note currently at the
        top of the stack.

        The current node is then displayed.
        """
        if not self.next_note:
            print("None.")
            return

        self.previous_note.append(self.current_note)
        self.current_note = self.next_note.pop()
        self.display()

    #Displaying the current note and its data.
    def display(self):
        print("------Current note:--------")
        print(self.current_note)
        print ("--------------------------")

    #Displaying number of notes saved in their history
    def __len__(self):
        return len(self.previous_note)+ len(1 if self.current_note else 0)+len(self.next_note)


if __name__ =='__main__':
    all_notes=[
             "Note 1 : Exam Venues",
             "Note 2 : Chicken Soup Recipe",
             "Note 3: Types of Algorithms",
    ]

    track_1 = Navigation_history(all_notes)
    #Open a note
    track_1.open(0)
    #Open another note
    track_1.open(1)
    #Go back to the first opened note
    track_1.back_note()
    #Open another note
    track_1.open(2)
    #return to the second note
    track_1.back_note()

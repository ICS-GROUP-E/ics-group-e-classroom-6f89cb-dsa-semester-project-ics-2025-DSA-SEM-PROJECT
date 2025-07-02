class StudentNode:
    def __init__(self,student_id , name , course , gpa):
        self.student_id = student_id   #Unique ID(e.g , "P12345")
        self.name = name
        self.course = course
        self.gpa = gpa
        self.next = None    #Pointer to the next node

class StudentLinkedList:
    def __init__(self):
        self.head = None  #Initailize empty list
        self.size = 0     #Track number of students (0(1) size checks)

    # --- CORE METHODS ---
    def add_student(self, student_id, name, course, gpa):
        """
        Add student to the end of the linked list.
        Time Complexity: O(n) - must traverse entire list
        """
        #Input Validation
        if not isinstance(student_id, str):
            raise TypeError("Student ID must be a string")
        if not isinstance(name, str):
            raise TypeError("Name must be a string  ")
        if not isinstance(course, str):
            raise TypeError("Course must be a string")
        if not isinstance(gpa, (int,float)) or gpa < 0 or gpa > 4.0:
            raise ValueError("GPA must be a number between 0 and 4.0")

        if self.search_student(student_id) is not None:
            raise ValueError(f"Student ID {student_id} already exists")


        new_node = StudentNode(student_id, name, course, gpa)

        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def delete_student(self,student_id):
        """
        Delete student by ID. Returns True if deleted, False if not found
        Time Complexity: 0(n) - worse case traverse entire list
        """
        current = self.head
        previous = None

        while current:
            if current.student_id == student_id:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                self.size -= 1
                return True
            previous = current
            current = current.next
        return  False

    def search_student(self, student_id):
        """
        Search for student by ID. Return student dat if found . None otherwise.
        Time Complexity: 0(n) - worse case traverse entire list
        """
        current = self.head
        while current:
            if current.student_id == student_id:
                return {
                    'id': current.student_id,
                    'name':current.name,
                    'course': current.course,
                    'gpa': current.gpa,
                }
            current = current.next
        return None

    def display_all(self):
        """
        Print all students in the list.
        Time Complexity: 0(n) - must visit every node
        """
        current = self.head
        if not current:
            print("No students in the list")
            return

        print("\nStudent Records:")
        print("-----------------")
        while current:
            print(f"ID: {current.student_id}")
            print(f"Name: {current.name}")
            print(f"Course: {current.course}")
            print(f"GPA: {current.gpa}")
            print("----------------")
            current = current.next

    def get_size(self):
        """
        Return number of students in list.
        Time Complexity: 0(1) - uses size counter
        """
        return  self.size

    def add_student_sorted(self, student_id, name, course, gpa):
        """
        Insert student sorted by GPA(high to low)
        """
        #Input Validation
        if not isinstance(student_id, str):
            raise TypeError("Student ID must be a string")
        if not isinstance(name, str):
            raise TypeError("Name must be a string  ")
        if not isinstance(course, str):
            raise TypeError("Course must be a string")
        if not isinstance(gpa, (int,float)) or gpa < 0 or gpa > 4.0:
            raise ValueError("GPA must be a number between 0 and 4.0")

        new_node = StudentNode(student_id, name, course, gpa)
        if not self.head or self.head.gpa < new_node.gpa:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.gpa >= new_node.gpa:
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.size += 1


#Example Usage
if __name__ == "__main__":
    ll = StudentLinkedList()

    #Add students
    ll.add_student("P123", "Alice", "Computer Science", 3.8)
    ll.add_student("P456", "Bob", "Engineering", 3.5)
    ll.add_student("P789", "Charlie", "Mathematics", 3.2)

    #Display all
    ll.display_all()

    #Search
    print("\nSearching for P456:")
    print(ll.search_student("P456"))

    #Delete
    print("\nDeleting P123...")
    ll.delete_student("P123")
    ll.display_all()

    #Size
    print(f"\nTotal students: {ll.get_size()}")






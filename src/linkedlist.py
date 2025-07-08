class StudentNode:
    def __init__(self, student_id, name, course, gpa):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.gpa = gpa
        self.next = None

class StudentLinkedList:
    def __init__(self):
        self.head = None

    def add_student(self, student_id, name, course, gpa):
        new_node = StudentNode(student_id, name, course, gpa)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete_student(self, student_id):
        current = self.head
        prev = None
        while current and current.student_id != student_id:
            prev = current
            current = current.next
        if current:
            if prev:
                prev.next = current.next
            else:
                self.head = current.next
            return True
        return False

    def search_student(self, student_id):
        current = self.head
        while current:
            if current.student_id == student_id:
                return current
            current = current.next
        return None

    def display_all(self):
        current = self.head
        while current:
            print(f"ID: {current.student_id}, Name: {current.name}, Course: {current.course}, GPA: {current.gpa}")
            current = current.next
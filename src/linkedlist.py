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

    def add_student(self, student_id, name, course, gpa):
        pass   #Placeholder

    def delete_student(self,student_id):
        pass   #Placeholder

    def search_student(self, student_id):
        pass   #Placeholder

    def display_all(self):
        pass    #Placeholder

    def display_all(self):
        pass    #Placeholder

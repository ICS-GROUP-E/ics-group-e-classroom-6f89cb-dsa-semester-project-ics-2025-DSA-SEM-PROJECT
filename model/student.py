class Student:
    def __init__(self, student_id, name, course, year, gpa):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.year = year
        self.gpa = gpa

    def __repr__(self):
        return f"Student({self.student_id}, {self.name}, {self.course}, Year: {self.year}, GPA: {self.gpa})"

    def to_tuple(self):
        return (self.student_id, self.name, self.course, self.year, self.gpa)

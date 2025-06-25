from stack_db import save_to_db, delete_from_db, pop_undo

student1 = {
    'id' : 'P12345',
    'name' : 'Baba Pima',
    'course' : 'ICS',
    'year' : 2,
    'gpa' : 3.87

}

save_to_db(student1)

delete_from_db('P12345')

pop_undo()

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        all_marks = sum(self.grades.values(), start=[])
        if all_marks == []:
            return f'Имя: {self.name}' + '\n' + f'Фамилия: {self.surname}' + '\n'\
                + f'Нет оценок за дз'  + '\n'\
                    + f'Курсы в процессе изучения: {", ".join(list(self.grades.keys()))}' + '\n'\
                        +f'Завершенные курсы: {", ".join(self.finished_courses)}'
        else:
            return f'Имя: {self.name}' + '\n' + f'Фамилия: {self.surname}' + '\n'\
                + f'Средняя оценка за дз: {round(sum(all_marks) / len(all_marks), 2)}'  + '\n'\
                    + f'Курсы в процессе изучения: {", ".join(list(self.grades.keys()))}' + '\n'\
                        +f'Завершенные курсы: {", ".join(self.finished_courses)}'

    def __lt__(self, other):
        if not isinstance(other, Student):
           print('Not a Student!')
           return
        all_marks_self, all_marks_other = sum(self.grades.values(), start=[]), sum(other.grades.values(), start=[])
        return round(sum(all_marks_self) / len(all_marks_self), 2) < round(sum(all_marks_other) / len(all_marks_other), 2)



    def add_courses(self, course_name):
        self.finished_courses.append(course_name)   

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'        
 
     
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}' + '\n' + f'Фамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        all_marks = sum(self.grades.values(), start=[])
        return f'Имя: {self.name}' + '\n' + f'Фамилия: {self.surname}' + '\n'\
            + f'Средняя оценка за лекции: {round(sum(all_marks) / len(all_marks), 2)}'   

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
           print('Not a Lecturer!')
           return
        all_marks_self, all_marks_other = sum(self.grades.values(), start=[]), sum(other.grades.values(), start=[])
        return round(sum(all_marks_self) / len(all_marks_self), 2) < round(sum(all_marks_other) / len(all_marks_other), 2)


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f'Имя: {self.name}' + '\n' + f'Фамилия: {self.surname}'

def count_avg_hw(students, course):
    """ 
    Allows to count average mark of different students. 
    Requires list of students and name of course
    """
    marks = []
    for student in students:
        marks += student.grades[course]
    return round(sum(marks) / len(marks), 2)

def count_avg_lecture(lectures, course):
    """ 
    Allows to count average mark of different lectures. 
    Requires list of lectures and name of course
    """    
    marks = []
    for lecture in lectures:
        marks += lecture.grades[course]
    return round(sum(marks) / len(marks), 2)

if __name__ == '__main__':
    student1 = Student('Kirill', 'Student1', 'male')
    student2 = Student('Konst', 'Student2', 'male')
    student1.courses_in_progress += ['Python']
    student2.courses_in_progress += ['Python']

    reviewer = Reviewer('Some', 'Buddy')
    reviewer.courses_attached += ['Python']

    reviewer.rate_hw(student1, 'Python', 10)
    reviewer.rate_hw(student1, 'Python', 9)
    reviewer.rate_hw(student1, 'Python', 9)
    reviewer.rate_hw(student2, 'Python', 8)
    reviewer.rate_hw(student2, 'Python', 9)
    reviewer.rate_hw(student2, 'Python', 10)

    lecturer1 = Lecturer('Oleg', 'Lecturer1')
    lecturer2 = Lecturer('Elena', 'Lecturer2')
    lecturer1.courses_attached += ['Python']
    lecturer2.courses_attached += ['Python']

    student1.rate_lecturer(lecturer1, 'Python', 10)
    student1.rate_lecturer(lecturer1, 'Python', 9)
    student1.rate_lecturer(lecturer1, 'Python', 9)
    student2.rate_lecturer(lecturer2, 'Python', 8)
    student2.rate_lecturer(lecturer2, 'Python', 9)
    student2.rate_lecturer(lecturer2, 'Python', 10)

    print(student1)
    print(student2)
    print(reviewer)
    print(lecturer1)
    print(lecturer2)
    print(student1 > student2)
    print(lecturer1 > lecturer2)

    print(count_avg_hw([student1, student2], 'Python'))
    print(count_avg_hw([lecturer1, lecturer2], 'Python'))
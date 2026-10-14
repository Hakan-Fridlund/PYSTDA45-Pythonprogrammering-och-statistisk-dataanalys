"""
Excersice from week3_excersises:
 Projekt 1 Course register (CSV + OOP)
- Create a  CSV `enrollments.csv` with columns: `student,course,points`.
- Create a Class student with the attributes `name` and `points`.
- Create a Class `Course` with `name` and a list of students.

- Read CSV-file row by row Create a Student object for each row and 
add the object in the right Course
- Print the number of students and average number of score for each course.
- Save a summary to `course_summary.json` (list with  `{course, n_students, avg_points}`).
"""
import csv

students = []

class Student:
    def __init__(self, name: str, points: int):
        self.name = name
        self.points = points

    def __str__(self):
        return f"Student name: {self.name} Points: {self.points}"

    def __repr__(self):
        return self.__str__()


class Course:
    def __init__(self, name: str, students: list[Student] ):
        self.name = name
        self.students = students

    def __str__(self):
        student_strings = [str(student) for student in self.students]
        all_students = "\n".join(student_strings)
        return f"Course: {self.name}\nStudents:\n{all_students}\n"

    def __repr__(self):
        return self.__str__()

    # TODO should return number of students and average points 
    def get_average_number(self):
        ...


def load_students_from_file(path="files/enrollments.csv"):
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            current_student = Student(
                name=row["student"], 
                points=row["points"]
            )
            students.append(current_student)


def load_courses_from_file(path="files/enrollments.csv") -> list[Course]:
    unique_course_names = set()

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
        # adds the course name to a set(duplicate is removed automatically)
            unique_course_names.add(row["course"])

    courses_dict = {course_name: [] for course_name in unique_course_names}

    with open(path, "r", encoding="utf-8") as file: # open the file again since empty from last reader loop
        reader = csv.DictReader(file)

        for index, row in enumerate(reader):
            course_name = row["course"]
            existing_student = students[index] # get the student from students list we got from load_students function
            courses_dict[course_name].append(existing_student) # add the student to the right course list

    courses = []
    for course_name, student_list in courses_dict.items():
        # creates a course and appends it to a list
        courses.append(Course(name=course_name, students=student_list))
        
    return courses

# TODO Save a summary to `course_summary.json` (list with  `{course, n_students, avg_points}`).
def save_summary(path="files/course_summary.json"):
    ...

load_students_from_file()
print(load_courses_from_file())

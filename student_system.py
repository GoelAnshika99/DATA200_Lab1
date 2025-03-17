import csv
import random
import time
import getpass
from login_system import Login
from course_system import Course
from grade_system import Grade
class Student:
    def __init__(self, student_records, grades_file, login_file, course_file):
        self.student_records = student_records
        self.grades_file = grades_file
        self.login_file = login_file
        self.course_file = course_file
        self.courses = Course(course_file)
        self.grades = Grade(grades_file)
    def load_grades(self):
        grades = {}
        with open(self.grades_file, mode = 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                try:
                    if len(row) >= 3:
                        grade = row[0]
                        min_marks = int(row[2])
                        max_marks = int(row[1])
                        grades[grade] = (max_marks, min_marks)
                except ValueError as e:
                    print(f"Error processing row {row}: {e}")
        return grades
    def assign_grades(self, marks):
        grades = self.load_grades()
        for grade, (max_marks, min_marks) in grades.items():
            if min_marks <= marks <= max_marks:
                return grade
        return 'F'
    def get_valid_marks(self):
        while True:
            try:
                marks = int(input("Enter your marks for the course (between 0 and 100): "))
                if 0 <= marks <= 100:
                    return marks
                else:
                    print("Error: Marks must be between 0 and 100. Please try again.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid integer between 0 and 100.")
    def create_student(self, email):
        course_ids = []
        try:
            with open(self.course_file, mode = 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    course_ids.append(row[1])
        except FileNotFoundError:
            print(f"Error: The course file was not found.")
            return
        found = False
        with open(self.student_records, mode = 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == email:
                    found = True
                    print(f"A record with this email ({email}) already exists.")
                    return
        if not found:
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            address = input("Enter your address: ")
            phone_number = input("Enter your phone number: ")
            courses = []
            while True:
                course_id = input("Enter your course id (or 'done' to finish): ")
                course_id = course_id.lower().replace(" ", "")
                if course_id.lower() == 'done':
                    break
                if course_id not in course_ids:
                    print(f"Invalid course ID: {course_id}. Please enter a valid course ID.")
                    continue
                marks = self.get_valid_marks()
                grade = self.assign_grades(marks)
                courses.append((course_id, marks, grade))
            for course_id, marks, grade in courses:
                with open(self.student_records, mode = 'a', newline = '') as file:
                    writer = csv.writer(file)
                    writer.writerow([first_name, last_name, email, address, phone_number, course_id, marks, grade])
            print(f"Student record created for {first_name} {last_name}.")
        else:
            return
    def view_student_records(self, email):
        found = False
        total_marks = 0
        num_courses = 0
        courses = []
        with open(self.student_records, mode = 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == email:
                    if not found:
                        print("Student Record:")
                        print(f"Name: {row[0]} {row[1]}")
                        print(f"Email: {row[2]}")
                        print(f"Address: {row[3]}")
                        print(f"Phone Number: {row[4]}")
                        found = True
                    course_id = row[5]
                    marks = int(row[6])
                    courses.append((course_id, marks, row[7]))
                    total_marks += marks
                    num_courses += 1
        if not found:
            print("No records found for this email.")
            return
        courses.sort(key = lambda x : x[0])
        for course in courses:
            print(f"Course ID: {course[0]}")
            print(f"Marks: {course[1]}")
            print(f"Grade: {course[2]}")
            print("-" * 30)
        if num_courses > 0:
            average_marks = total_marks/num_courses
            print(f"\nTotal Marks: {total_marks}")
            print(f"Average Marks: {average_marks:.2f}")
        else:
            print("No course records available to calculate total or average marks.")
    def update_student_info(self, email):
        row = []
        found = False
        with open(self.student_records, mode = 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        for row in rows:
            if row[2] == email:
                print(f"Found your record: {row}")
                row[3] = input(f"Enter new address (current: {row[3]}): ")
                row[4] = input(f"Enter new phone number (current: {row[4]}): ")
                found = True
                break
        if found:
            with open(self.student_records, mode = 'w', newline = '') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Your information has been updated.")
        else:
            print("Record not found.")
    def delete_student_account(self, email):
        rows = []
        with open(self.student_records, mode = 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        initial_row_count = len(rows)
        rows = [row for row in rows if row[2] != email]
        if len(rows) < initial_row_count:
            with open(self.student_records, mode = 'w', newline = '') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
            print(f"Student account with email {email} has been deleted from student records.")
        else:
            print(f"No student records found for email {email} in student records.")
        login_rows = []
        with open(self.login_file, mode = 'r') as file:
            reader = csv.reader(file)
            login_rows = list(reader)
        login_row_count = len(login_rows)
        login_rows = [row for row in login_rows if row[0] != email or row[2] != "student"]
        if len(login_rows) < login_row_count:
            with open(self.login_file, mode = 'w', newline = '') as file:
                writer = csv.writer(file)
                writer.writerows(login_rows)
            print(f"Student account with email {email} has been deleted from login system.")
        else:
            print(f"No login record found for email {email} in the login system.")
    def search_student_by_email(self, email):
        start_time = time.time()
        self.view_student_records(email)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to search for the student record: {elapsed_time:.4f} seconds")
    def add_course(self, email):
        valid_course_ids = []
        try:
            with open(self.course_file, mode = 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    valid_course_ids.append(row[1].lower().replace(" ",""))
        except FileNotFoundError:
            print("Error: The course file was not found.")
            return
        first_name = last_name = address = phone_number = course_id = None
        marks = 0
        grade = 'F'
        with open(self.student_records, mode = 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            student_found = False
            for row in rows:
                if row[2] == email:
                    first_name = row[0]
                    last_name = row[1]
                    address = row[3]
                    phone_number = row[4]
                    student_found = True
                    break
        if student_found:
            enrolled_courses = [row[5].lower().replace(" ", "") for row in rows if row[2] == email]
            while True:
                course_id = input(f"Enter the course ID to enroll (eg, data200, data201): ").strip()
                course_id = course_id.lower().replace(" ", "")
                if course_id not in valid_course_ids:
                    print(f"Invalid course ID: {course_id}. Please enter a valid course ID from the course list.")
                    continue
                if course_id in enrolled_courses:
                    print(f"You are already enrolled in the course {course_id}. Please select a different course.")
                    continue
                marks = self.get_valid_marks()
                grade = self.assign_grades(marks)
                with open(self.student_records, mode = 'a', newline = '') as file:
                    writer = csv.writer(file)
                    writer.writerow([first_name, last_name, email, address, phone_number, course_id, marks, grade])
                print(f"Course {course_id} added for {first_name} {last_name}. Marks: {marks}, Grade: {grade}.")
                add_another = input("Do you want to add another course? (y/n): ").lower()
                if add_another != 'y':
                    break
        else:
            print("Student with this email not found in the reocrds.")
    def drop_course(self, email):
        student_courses = []
        first_name = last_name = address = phone_number = None
        with open(self.student_records, mode = 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if row[2] == email:
                    if first_name is None:
                        first_name = row[0]
                        last_name = row[1]
                        address = row[3]
                        phone_number = row[4]
                    student_courses.append(row)
        if len(student_courses) == 0:
            print("No student found with this email in the records.")
            return
        if len(student_courses) == 1:
            print("You should be enrolled in at least one course.\nCannot drop course.")
            return
        print(f"You are enrolled in the following courses:")
        for i, course in enumerate(student_courses, 1):
            print(f"{i}. {course[5]} (Marks: {course[6]}, Grade: {course[7]})")
        course_to_drop = int(input("Enter the number of the course you want to drop: "))
        if 1 <= course_to_drop <= len(student_courses):
            dropped_course = student_courses.pop(course_to_drop-1)
            print(f"Course {dropped_course[5]} dropped successfully.")
        rows = []
        with open(self.student_records, mode = 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        initial_row_count = len(rows)
        rows = [row for row in rows if row[2] != email]
        if len(rows) < initial_row_count:
            with open(self.student_records, mode = 'w', newline = '') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        else:
            print(f"No student records found for email {email} in student records.")
        for first_name, last_name, email, address, phone_number, course_id, marks, grade in student_courses:
            with open(self.student_records, mode = 'a', newline = '') as file:
                writer = csv.writer(file)
                writer.writerow([first_name, last_name, email, address, phone_number, course_id, marks, grade])
    def view_courses(self):
        self.courses.display_courses()
    def view_grade_lookup(self):
        self.grades.view_grades()
    def view_professor_by_course(self):
        from faculty_system import Faculty
        faculty = Faculty()
        faculty.display_professors_by_course()
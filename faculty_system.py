import csv
import statistics
from student_system import Student
from course_system import Course
import time
class Faculty:
    def __init__(self, faculty_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/faculty_data.csv",
                 course_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/course_records.csv",
                 student_records = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/student_records.csv",
                 grade_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/grades.csv",
                 login_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/login.csv"):
        self.faculty_file = faculty_file
        self.course_file = course_file
        self.student_records = student_records
        self.grade_file = grade_file
        self.login_file = login_file
        self.courses = Course(course_file)
        self.student = Student(student_records, grade_file, login_file, course_file)
    def display_faculty_info(self, email):
        found = False
        try:
            with open(self.faculty_file, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) == 7 and row[2].lower() == email.lower():
                        first_name, last_name, email, address, phone_number, course_id, rank = row
                        found = True
                        print("Professor Information:")
                        print(f"Name: {first_name} {last_name}")
                        print(f"Email: {email}")
                        print(f"Address: {address}")
                        print(f"Phone Number: {phone_number}")
                        print(f"Course ID: {course_id}")
                        print(f"Rank: {rank}")
                        break
                if not found:
                    print(f"No professor with the email: {email}")
        except FileNotFoundError:
            print(f"Error: The faculty file {self.faculty_file} was not found.")
        except Exception as e:
            print(f"An error occurred while reading the faculty data: {e}")
    def create_professor(self):
        valid_course_ids = []
        try:
            with open(self.course_file, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    valid_course_ids.append(row[1].lower().replace(" ",""))
        except FileNotFoundError:
            print(f"Error: The faculty file {self.course_file} was not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading the course file: {e}")
            return
        email = input("Enter your email: ")
        if self.is_email_exists(email):
            print(f"A professor with email {email} already exists.")
            return
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        address = input("Enter your address: ")
        phone_number = input("Enter your phone number: ")
        while True:
            course_id = input("Enter the course ID you will be teaching (eg. data200, data201): ").lower().replace(" ","")
            if course_id not in valid_course_ids:
                print(f"Invalid course ID: {course_id}. Please enter a valid course ID from the course list.")
                continue
            print("\nPlease choose your rank from the following options: ")
            print("1. Junior Professor")
            print("2. Assistant Professor")
            print("3. Head of Department")
            rank_choice = input("Enter the number corressponding to your rank: ").strip()
            if rank_choice == '1':
                rank = "junior professor"
            elif rank_choice == '2':
                rank = "assistant professor"
            elif rank_choice == '3':
                rank = "head of department"
            else:
                print("Invalid choice. Please enter a valid rank choice.")
                continue
            with open(self.faculty_file, mode = 'a', newline = '') as file:
                writer = csv.writer(file)
                writer.writerow([first_name, last_name, email, address, phone_number, course_id, rank])
            print(f"Account created successfully for {first_name} {last_name}.")
            break
    def is_email_exists(self, email):
        try:
            with open(self.faculty_file, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) == 7 and row[2].lower() == email.lower():
                        return True
            return False
        except FileNotFoundError:
            print(f"Error: The faculty file {self.faculty_file} was not found.")
            return False
        except Exception as e:
            print(f"An error while while checking the email: {e}")
            return False
    def display_professors_by_course(self):
        professors_by_course = {}
        try:
            with open(self.faculty_file, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    first_name = row[0]
                    last_name = row[1]
                    email = row[2]
                    course_id = row[5]
                    rank = row[6]
                    if course_id not in professors_by_course:
                        professors_by_course[course_id] = []
                    professors_by_course[course_id].append((first_name+" "+last_name, rank))
        except FileNotFoundError:
            print(f"Error: The file {self.faculty_file} was not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading the faculty records: {e}")
            return
        if not professors_by_course:
            print("No professors found.")
            return
        print("\nProfessors grouped by course ID:")
        for course_id, professors in professors_by_course.items():
            print(f"\nCourse ID: {course_id}")
            for professor in professors:
                print(f"Name: {professor[0]}, Rank: {professor[1]}")
    def modify_professor_info(self, email):
        found = False
        rows = []
        try:
            with open(self.faculty_file, mode = 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
        except FileNotFoundError:
            print(f"Error: The file {self.faculty_file} was not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading the faculty records: {e}")
            return
        for i, row in enumerate(rows):
            if row[2] == email:
                found = True
                print(f"Professor found: {row[0]} {row[1]}")
                print(f"Current Address: {row[3]}")
                print(f"Current Phone Number: {row[4]}")
                new_address = input("Enter your new address: ")
                new_phone = input("Enter your new phone number: ")
                row[3] = new_address
                row[4] = new_phone
                try:
                    with open(self.faculty_file, mode = 'w', newline = '') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)
                    print("Professor's information updated successfully.")
                except Exception as e:
                    print(f"An error occurred while updating the records: {e}")
                break
        if not found:
            print("No professor found with the given email.")
    def view_average_and_median_marks(self):
        course_marks = {}
        try:
            with open(self.student_records, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    course_id = row[5]
                    marks = int(row[6])
                    if course_id not in course_marks:
                        course_marks[course_id] = []
                    course_marks[course_id].append(marks)
        except FileNotFoundError:
            print(f"Error: The file {self.student_records} was not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading the student records: {e}")
            return
        course_stats = []
        for course_id, marks in course_marks.items():
            try:
                avg_marks = sum(marks)/len(marks)
                median_marks = statistics.median(marks)
                course_stats.append((course_id, avg_marks, median_marks))
            except Exception as e:
                print(f"Error processing course {course_id}: {e}")
        start_time = time.time()
        course_stats.sort(key = lambda x: x[1], reverse = True)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to sort the courses by average marks: {elapsed_time:.4f} seconds")
        for course_id, avg_marks, median_marks in course_stats:
            print(f"Course ID: {course_id}")
            print(f"Average Marks: {avg_marks:.2f}")
            print(f"Median Marks: {median_marks}\n")
    def search_professor_by_email(self, email):
        start_time = time.time()
        self.display_faculty_info(email)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to search for the professor record: {elapsed_time:.4f} seconds")
    def modify_marks(self, email):
        students_in_course = []
        try:
            with open(self.student_records, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[2].lower() == email.lower():
                        students_in_course.append(row)
        except FileNotFoundError:
            print(f"Error: The student records file was not found.")
            return
        if not students_in_course:
            print(f"No student found with email {email}.")
            return
        print(f"\nStudent found: {students_in_course[0][0]} {students_in_course[0][1]} (Email: {students_in_course[0][2]})")
        print(f"Student is enrolled in the following courses:")
        student_courses = set()
        for row in students_in_course:
            student_courses.add(row[5].lower())
        for course_id in student_courses:
            print(course_id)
        course_id = input("Enter the course ID you want to modify marks for: ").lower().replace(" ", "")
        if course_id.lower().replace(" ","") not in student_courses:
            print(f"Student is not enrolled in course {course_id}. Please enter a valid course ID.")
            return
        while True:
            try:
                new_marks = int(input(f"Enter the new marks for {email} in course {course_id}: "))
                if 0 <= new_marks <= 100:
                    break
                else:
                    print("Error: Marks must be between 0 and 100. Please try again.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid integer between 0 and 100.")
        student = Student(self.student_records, self.grade_file, self.login_file, self.course_file)
        new_grade = student.assign_grades(new_marks)
        updated_records = []
        updated = False
        try:
            with open(self.student_records, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[2].lower() == email.lower() and row[5].lower() == course_id:
                        row[6] = str(new_marks)
                        row[7] = new_grade
                        updated = True
                    updated_records.append(row)
        except FileNotFoundError:
            print(f"Error: The student records file was not found.")
            return
        if updated:
            with open(self.student_records, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_records)
            print(f"Marks and grade updated successfully for {email} in {course_id}.")
        else:
            print(f"Failed to update marks and grade for {email} in {course_id}.")
    def view_courses(self):
        self.courses.display_courses()
    def add_course(self):
        course_name = input("Enter the course name you want to add: ")
        course_id = input("Enter the course ID: ")
        course_id = course_id.lower().replace(" ","")
        credits = input("Enter the number of credits: ")
        course_exists = False
        try:
            with open(self.course_file, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[1].lower() == course_id:
                        course_exists = True
                        break
        except FileNotFoundError:
            print(f"The course records file {self.course_file} was not found.")
            return
        if course_exists:
            print(f"Course with ID {course_id} already exists. Please enter a valid course ID.")
            return
        with open(self.course_file, mode = 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow([course_name, course_id, credits])
        print(f"Course {course_name} with ID {course_id} and {credits} has been added successfully.")
    def get_professor_rank(self,email):
        try:
            found = False
            with open(self.faculty_file, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[2] == email:
                        found = True
                        return row[6].strip().lower().replace(" ", "")
            if found == False:
                print(f"Professor {email} was not found.")
                return
        except FileNotFoundError:
            print(f"Error: The faculty file {self.faculty_file} was not found.")
        return None
    def delete_course(self, course_id):
        course_id = course_id.lower().replace(" ","")
        course_exists = False
        try:
            with open(self.course_file, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[1].lower().replace(" ", "") == course_id:
                        course_exists = True
                        break
        except FileNotFoundError:
            print(f"Error: The course file '{self.course_file}' was not found.")
            return
        if not course_exists:
            print(f"Error: Course with ID '{course_id}' does not exist in the course records.")
            return
        try:
            course_rows = []
            with open(self.course_file, mode = 'r') as file:
                reader = csv.reader(file)
                course_rows = list(reader)
            course_rows = [row for row in course_rows if row[1] != course_id]
            with open(self.course_file, mode = 'w', newline = '') as file:
                writer = csv.writer(file)
                writer.writerows(course_rows)
            print(f"Course {course_id} has been deleted from course_records.csv")
        except FileNotFoundError:
            print(f"Error: The course file '{self.course_file}' was not found.")
            return
        try:
            student_to_be_removed = []
            update_student_records = []
            student_courses = {}
            with open(self.student_records, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    student_email = row[2]
                    course_id = row[5]
                    if student_email in student_courses:
                        student_courses[student_email].append(course_id)
                    else:
                        student_courses[student_email] = [course_id]
            for student_email, courses in student_courses.items():
                if course_id.lower().replace(" ", "") in courses:
                    if len(courses) == 1:
                        student_to_be_removed.append(student_email)
                    else:
                        update_student_records.append(student_email)
            for email in student_to_be_removed:
                self.student.delete_student_account(email)
            new_student_records = []
            with open(self.student_records, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)
                new_student_records.append(header)
                for row in rows:
                    if row[2] in update_student_records and row[5] == course_id:
                        continue
                    else:
                        new_student_records.append(row)
            with open(self.student_records, mode = 'w', newline = '') as file:
                writer = csv.writer(file)
                writer.writerows(new_student_records)
        except FileNotFoundError:
            print(f"Error: The student records file '{self.student_records}' was not found.")
    def load_data(self):
        student = []
        with open(self.student_records, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cleaned_row = {key.strip(): value for key, value in row.items()}
                student.append({
                    'first_name': cleaned_row['first_name'],
                    'last_name': cleaned_row['last_name'],
                    'email': cleaned_row['email'],
                    'address': cleaned_row['address'],
                    'phone_number': cleaned_row['phone_number'],
                    'course_id': cleaned_row['course_id'],
                    'marks': int(cleaned_row['marks'])
                })
        return student
    def get_grade_lookup(self):
        grades = ['A+', 'A', 'B', 'C', 'D', 'E', 'F']
        grade_lookup = []
        print("Please enter the grade ranges for each grade:")
        while True:
            try:
                minimum_A_plus = int(input("Enter the minimum marks for grade A+: "))
                if minimum_A_plus < 0 or minimum_A_plus > 100:
                    print("Error: The minimum for grade A+ must be between 0 and 100.")
                    continue
                grade_lookup.append({'grade': 'A+', 'minimum': minimum_A_plus, 'maximum': 100})
                break
            except ValueError:
                print("Error: Please enter a valid integer for the minimum marks of A+.")
        previous_minimum = grade_lookup[0]['minimum']
        for i, grade in enumerate(grades[1:-1]):
            while True:
                try:
                    minimum = int(input(f"Enter the minimum marks for grade {grade}: "))
                    maximum = previous_minimum - 1
                    print(f"Maximum marks for grade {grade}: {maximum}")
                    if maximum < minimum:
                        print(f"Error: Maximum marks for {grade} must be greater than or equal to minimum marks.")
                        continue
                    grade_lookup.append({'grade': grade, 'minimum': minimum, 'maximum': maximum})
                    previous_minimum = minimum
                    break
                except ValueError:
                    print("Error: Please enter valid integer values for minimum and maximum.")
        maximum_F = previous_minimum - 1
        if maximum_F <= 0:
            print(f"Error: Invalid maximum {maximum_F} for grade F. Maximum must be a positive number.")
        else:
            grade_lookup.append({'grade': 'F', 'minimum': 0, 'maximum': maximum_F})
        return grade_lookup
    def check_overlap(self, grades):
        grades.sort(key=lambda x: x['minimum'])
        for i in range(1, len(grades)):
            if grades[i]['minimum'] <= grades[i-1]['maximum']:
                print(f"Overlap detected between {grades[i-1]['grade']} and {grades[i]['grade']}")
                return False
        return True
    def assign_grade(self, marks, grades):
        for grade in grades:
            if grade['minimum'] <= marks <= grade['maximum']:
                return grade['grade']
        return 'F'
    def update_student_grades(self, students, grades):
        for student in students:
            student['grade'] = self.assign_grade(student['marks'], grades)
        return students
    def save_updated_data(self, students):
        with open(self.student_records, mode='w', newline='') as file:
            fieldnames = ['first_name', 'last_name', 'email', 'address', 'phone_number', 'course_id', 'marks', 'grade']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
        print(f"Student records updated and saved to {self.student_records}.")
    def save_grade_lookup_to_file(self, grade_lookup):
        grade_order = ['A+', 'A', 'B', 'C', 'D', 'E', 'F']
        grade_lookup_sorted = sorted(grade_lookup, key=lambda x: grade_order.index(x['grade']))
        with open(self.grade_file, mode='w', newline='') as file:
            fieldnames = ['grades', 'maximum', 'minimum']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for grade in grade_lookup_sorted:
                writer.writerow({
                    'grades': grade['grade'],
                    'maximum': grade['maximum'],
                    'minimum': grade['minimum']
                })
        print(f"Modified grade lookup saved to '{self.grade_file}' in the correct order.")
    def delete_faculty_account(self, email):
        rows = []
        with open(self.faculty_file, mode = 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        initial_row_count = len(rows)
        rows = [row for row in rows if row[2] != email]
        if len(rows) < initial_row_count:
            with open(self.faculty_file, mode = 'w', newline = '') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
            print(f"Faculty account with email {email} has been deleted from faculty records.")
        else:
            print(f"No faculty records found for email {email} in faculty records.")
        login_rows = []
        with open(self.login_file, mode = 'r') as file:
            reader = csv.reader(file)
            login_rows = list(reader)
        login_row_count = len(login_rows)
        login_rows = [row for row in login_rows if row[0] != email or row[2] != "professor"]
        if len(login_rows) < login_row_count:
            with open(self.login_file, mode = 'w', newline = '') as file:
                writer = csv.writer(file)
                writer.writerows(login_rows)
            print(f"Faculty account with email {email} has been deleted from login system.")
        else:
            print(f"No login record found for email {email} in the login system.")
    def sort_student_records(self):
        print("Sort the students records by:")
        print("1. Email")
        print("2. Marks")
        choice = input("Enter your choice (1 or 2): ")
        try:
            with open(self.student_records, mode = 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                student_records = list(reader)
        except FileNotFoundError:
            print(f"Error: The file '{self.student_records}' was not found.")
            return
        start_time = time.time()
        if choice == '1':
            student_records.sort(key=lambda x: x[2].lower())
        elif choice == '2':
            student_records.sort(key=lambda x: int(x[6]), reverse=True)
        else:
            print("invalid choice. Please enter 1 or 2")
            return
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\nSorting took {elapsed_time:.4f} seconds.")
        try:
            with open(self.student_records, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(student_records)
            print("\nStudent records have been sorted and saved.")
        except FileNotFoundError:
            print(f"Error: The file {self.student_records} was not found.")
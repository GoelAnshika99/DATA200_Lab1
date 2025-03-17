import csv
import random
import getpass
class Login:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.shift_value = 5
    def encrypt_password(self, password):
        encrypted = ''.join(chr((ord(char) + self.shift_value) % 256) for char in password)
        return encrypted
    def decrypt_password(self, encrypted_password):
        decrypted = ''.join(chr((ord(char) - self.shift_value) % 256) for char in encrypted_password)
        return decrypted
    def create_account(self, role):
        print(f"Creating a new {role} account.........")
        while True:
            email = input("Enter your email: ")
            email_exists = False
            with open(self.csv_file, mode = 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    stored_email, _, stored_role = row
                    if stored_email == email:
                        email_exists = True
                        break
            if email_exists:
                print("Email already exists. Please enter a different email.")
            else:
                password = getpass.getpass("Enter your password: ")
                encrypted_password = self.encrypt_password(password)
                with open(self.csv_file, mode = 'a', newline = '') as file:
                    writer = csv.writer(file)
                    writer.writerow([email, encrypted_password, role])
                print(f"Account created successfully for {email} as a {role}.")
                return email
    def authenticate_user(self, role):
        print(f"Please log in as a {role}.")
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")
        encrypted_input_password = self.encrypt_password(password)
        with open(self.csv_file, mode = 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                stored_email, stored_encrypted_password, stored_role = row
                if stored_role == role and stored_email == email:
                    if stored_encrypted_password == encrypted_input_password:
                        print(f"Login successful! Welcome back, {email} ({stored_role}).")
                        return True
        print("Login failed. Incorrect email or password.")
        return False
    def change_password(self, email, role):
        old_password = getpass.getpass("Enter your old password: ")
        encrypted_old_password = self.encrypt_password(old_password)
        with open(self.csv_file, mode = 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        found = False
        for row in rows:
            if row[0] == email and row[2] == role and row[1] == encrypted_old_password:
                found = True
                new_password = getpass.getpass("Enter your new password: ")
                encrypted_new_password = self.encrypt_password(new_password)
                row[1] = encrypted_new_password
                break
        if found:
            with open(self.csv_file, mode = 'w', newline = '') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print(f"Password changed successfully for {email}.")
        else:
            print("Incorrect old password. Unable to change password.")
    def student_menu(self, student, email):
        from student_system import Student
        while True:
            print("\n--------Sub Student Menu--------")
            print("1. View your records")
            print("2. Update your information")
            print("3. Delete your account")
            print("4. Search student by email")
            print("5. Add course")
            print("6. Delete course")
            print("7. View Course List")
            print("8. View Grade Lookup")
            print("9. View professor by course")
            print("10. Change Password")
            print("11. Return to main menu")
            choice = input("Please choose an option (1/2/3/4/5/6/7/8/9/10/11): ")
            if choice == '1':
                email = input("Enter your email to view your records: ")
                student.view_student_records(email)
            elif choice == '2':
                email = input("Enter your email to update your information: ")
                student.update_student_info(email)
            elif choice == '3':
                email = input("Enter your email to delete your account: ")
                student.delete_student_account(email)
            elif choice == '4':
                email = input("Enter the email to search for student records: ")
                student.search_student_by_email(email)
            elif choice == '5':
                email = input("Enter the email to add course: ")
                student.add_course(email)
            elif choice == '6':
                email = input("Enter the email to drop course: ")
                student.drop_course(email)
            elif choice == '7':
                student.view_courses()
            elif choice == '8':
                student.view_grade_lookup()
            elif choice == '9':
                student.view_professor_by_course()
            elif choice == '10':
                login_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/login.csv"
                login = Login(login_file)
                email = input("Enter your email: ")
                login.change_password(email, "student")
            elif choice == '11':
                break
            else:
                print("Invalid option. Please try again.")
    def professor_menu(self, faculty, email):
        from faculty_system import Faculty
        from student_system import Student
        while True:
            print("\n--------Sub Professor Menu--------")
            print("1. View your details")
            print("2. View professor list by Course ID")
            print("3. Modify your details")
            print("4. View Course Performance (sorted by average marks)")
            print("5. Sort student data by email or marks")
            print("6. Search student by email")
            print("7. Search professor by email")
            print("8. Modify student marks")
            print("9. Delete student account")
            print("10. View Course List")
            print("11. Add Course")
            print("12. Delete Course")
            print("13. Modify Grade Lookup")
            print("14. Delete your account")
            print("15. Change password")
            print("16. Return to main menu")
            choice = input("Please choose an option (1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16): ")
            if choice == '1':
                email = input("Enter your email to view your records: ")
                faculty.display_faculty_info(email)
            elif choice == '2':
                faculty.display_professors_by_course()
            elif choice == '3':
                email = input("Enter your email to modify records: ")
                faculty.modify_professor_info(email)
            elif choice == '4':
                faculty.view_average_and_median_marks()
            elif choice == '5':
                faculty.sort_student_records()
            elif choice == '6':
                student_records = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/student_records.csv"
                grade_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/grades.csv"
                login_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/login.csv"
                course_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/course_records.csv"
                student = Student(student_records, grade_file, login_file, course_file)
                email = input("Enter the email to search for student records: ")
                import time
                start_time = time.time()
                student.search_student_by_email(email)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time taken to search for the student record: {elapsed_time:.4f} seconds")
            elif choice == '7':
                email = input("Enter the email to search for professor: ")
                faculty.search_professor_by_email(email)
            elif choice == '8':
                email = input("Enter the email of the student for which you want to modify marks: ")
                faculty.modify_marks(email)
            elif choice == '9':
                student_records = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/student_records.csv"
                grade_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/grades.csv"
                login_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/login.csv"
                course_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/course_records.csv"
                student = Student(student_records, grade_file, login_file, course_file)
                prof_email = input("Enter your email to delete a student account: ")
                rank = faculty.get_professor_rank(prof_email)
                if rank == "headofdepartment":
                    email = input("Enter the email of the student whose account you want to delete: ")
                    student.delete_student_account(email)
                else:
                    print("Permission denied: Only the Head of Department can delete a student account.")
            elif choice == '10':
                faculty.view_courses()
            elif choice == '11':
                prof_email = input("Enter your email to add course: ")
                rank = faculty.get_professor_rank(prof_email)
                if rank == "headofdepartment":
                    faculty.add_course()
                else:
                    print("Permission denied: Only the Head of Department can add a course.")
            elif choice == '12':
                prof_email = input("Enter your email to delete course: ")
                rank = faculty.get_professor_rank(prof_email)
                if rank == "headofdepartment":
                    course_id = input("Enter the course ID you want to delete: ")
                    faculty.delete_course(course_id)
                else:
                    print("Permission denied: Only the Head of Department can delete a course.")
            elif choice == '13':
                prof_email = input("Enter your email to modify grade lookup: ")
                rank = faculty.get_professor_rank(prof_email)
                if rank == "headofdepartment":
                    students = faculty.load_data()
                    grade_lookup = faculty.get_grade_lookup()
                    if faculty.check_overlap(grade_lookup):
                        updated_students = faculty.update_student_grades(students, grade_lookup)
                        faculty.save_updated_data(updated_students)
                        faculty.save_grade_lookup_to_file(grade_lookup)
                    else:
                        print("Please fix the overlap in grade ranges.")
                else:
                    print("Permission denied: Only the Head of Department can modify grade lookup.")
            elif choice == '14':
                email = input("Enter your email to delete account: ")
                faculty.delete_faculty_account(email)
            elif choice == '15':
                login_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/login.csv"
                login = Login(login_file)
                email = input("Enter your email: ")
                login.change_password(email, "professor")
            elif choice == '16':
                break
            else:
                print("Invalid option. Please try again.")
    def main_menu(self):
        from student_system import Student
        from faculty_system import Faculty
        while True:
            print("\n--------Main Menu--------")
            print("1. Student")
            print("2. Professor")
            print("3. Exit")
            choice = input("Please choose an option (1/2/3): ")
            if choice == '1':
                while True:
                    print("\n--------Student Menu--------")
                    print("1. New User")
                    print("2. Existing User")
                    print("3. Return to main menu")
                    student_choice = input("Please choose an option (1/2/3): ")
                    if student_choice == "1":
                        email = self.create_account("student")
                        student_records = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/student_records.csv"
                        grade_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/grades.csv"
                        login_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/login.csv"
                        course_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/course_records.csv"
                        student = Student(student_records, grade_file, login_file, course_file)
                        student.create_student(email)
                    elif student_choice == "2":
                        email = self.authenticate_user("student")
                        if email:
                            student_records = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/student_records.csv"
                            grade_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/grades.csv"
                            login_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/login.csv"
                            course_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/course_records.csv"
                            student = Student(student_records, grade_file, login_file, course_file)
                            self.student_menu(student, email)
                    elif student_choice == "3":
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == '2':
                while True:
                    print("\n--------Professor Menu--------")
                    print("1. New User")
                    print("2. Existing User")
                    print("3. Return to main menu")
                    prof_choice = input("Please choose an option (1/2/3): ")
                    if prof_choice == "1":
                        email = self.create_account("professor")
                        faculty = Faculty()
                        faculty.create_professor()
                    elif prof_choice == "2":
                        email = self.authenticate_user("professor")
                        if email:
                            faculty = Faculty()
                            self.professor_menu(faculty, email)
                    elif prof_choice == "3":
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == '3':
                print("Exiting the system.......")
                return
            else:
                print("Invalid option. Please try again.")
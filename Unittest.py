import unittest
import csv
import os
import time
from io import StringIO
from random import choice, randint
class TestStudentManagement(unittest.TestCase):
    def setUp(self):
        self.student_file = 'C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/test_student_records.csv'
        self.course_file = 'C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/test_course_records.csv'
        self.faculty_file = 'C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/test_faculty_data.csv'
        self.create_test_student_data(1000)
        self.create_test_course_data()
        self.create_test_faculty_data()
    def create_test_student_data(self, num_records):
        with open(self.student_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "email", "address", "phone_number", "course_id", "marks", "grade"])
            for _ in range(num_records):
                first_name = choice(['John', 'Jane', 'Alice', 'Bob'])
                last_name = choice(['Smith', 'Doe', 'Johnson', 'Brown'])
                email = f"{first_name.lower()}.{last_name.lower()}@example.com"
                address = f"123 {last_name} St"
                phone_number = f"555-{randint(1000, 9999)}"
                course_id = choice(['CS101', 'CS102', 'CS103', 'CS104'])
                marks = randint(0, 100)
                grade = self.assign_grade(marks)
                writer.writerow([first_name, last_name, email, address, phone_number, course_id, marks, grade])
    def create_test_course_data(self):
        courses = [("CS101", "101", 3), ("CS102", "102", 3), ("CS103", "103", 4)]
        with open(self.course_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "id", "credits"])
            for course in courses:
                writer.writerow(course)
    def create_test_faculty_data(self):
        faculties = [("Dr. John", "Doe", "john.doe@faculty.com", "123 Faculty Rd", "555-1234", "CS101", "Assistant Professor"),
                     ("Dr. Alice", "Smith", "alice.smith@faculty.com", "456 Faculty Rd", "555-5678", "CS102", "Junior Professor")]
        with open(self.faculty_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "email", "address", "phone_number", "course_id", "rank"])
            for faculty in faculties:
                writer.writerow(faculty)
    def assign_grade(self, marks):
        if marks >= 90:
            return 'A'
        elif marks >= 80:
            return 'B'
        elif marks >= 70:
            return 'C'
        elif marks >= 60:
            return 'D'
        else:
            return 'F'
    def test_add_student(self):
        new_student = ["Emma", "Watson", "emma.watson@example.com", "789 Example Rd", "555-8765", "CS104", 85, "B"]
        with open(self.student_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_student)
        with open(self.student_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertTrue(any(row[2] == new_student[2] for row in rows))
    def test_delete_student(self):
        student_email_to_delete = "alice.johnson@example.com"
        with open(self.student_file, mode='r') as file:
            rows = list(csv.reader(file))
        rows = [row for row in rows if row[2] != student_email_to_delete]
        with open(self.student_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        with open(self.student_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertTrue(all(row[2] != student_email_to_delete for row in rows))
    def test_modify_student(self):
        student_email_to_modify = "jane.doe@example.com"
        new_marks = 95
        new_grade = self.assign_grade(new_marks)
        # Modify student marks
        with open(self.student_file, mode='r') as file:
            rows = list(csv.reader(file))
        for row in rows:
            if row[2] == student_email_to_modify:
                row[6] = new_marks
                row[7] = new_grade
        with open(self.student_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        # Verify modification
        with open(self.student_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            modified_student = next(row for row in rows if row[2] == student_email_to_modify)
            self.assertEqual(int(modified_student[6]), new_marks)
            self.assertEqual(modified_student[7], new_grade)
    def test_sort_student_records_by_marks(self):
        total_start_time = time.time()
        with open(self.student_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)
        rows.sort(key=lambda x: int(x[6]), reverse=True)
        with open(self.student_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "email", "address", "phone_number", "course_id", "marks", "grade"])
            writer.writerows(rows)
        total_end_time = time.time()
        print(f"Total time taken to sort student record by marks    : {total_end_time - total_start_time} seconds")
        self.assertTrue(all(int(rows[i][6]) >= int(rows[i+1][6]) for i in range(len(rows)-1)))
    def test_sort_student_records_by_email(self):
        total_start_time = time.time()
        with open(self.student_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)
        rows.sort(key=lambda x: x[2])
        with open(self.student_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "email", "address", "phone_number", "course_id", "marks", "grade"])
            writer.writerows(rows)
        total_end_time = time.time()
        print(f"Total time taken to sort student record by email: {total_end_time - total_start_time} seconds")
        self.assertTrue(all(rows[i][2] <= rows[i+1][2] for i in range(len(rows)-1)))
    def test_search_student(self):
        student_email = "john.smith@example.com"
        start_time = time.time()
        with open(self.student_file, mode='r') as file:
            reader = csv.reader(file)
            student = next((row for row in reader if row[2] == student_email), None)
        end_time = time.time()
        print(f"Time taken to search for student: {end_time - start_time} seconds")
        self.assertIsNotNone(student)
    def test_add_faculty(self):
        new_faculty = ["Dr. Emma", "Watson", "emma.watson@faculty.com", "789 Faculty Rd", "555-8765", "CS104", "Assistant Professor"]
        with open(self.faculty_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_faculty)
        with open(self.faculty_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertTrue(any(row[2] == new_faculty[2] for row in rows))
    def test_delete_faculty(self):
        faculty_email_to_delete = "emma.watson@faculty.com"
        with open(self.faculty_file, mode='r') as file:
            rows = list(csv.reader(file))
        rows = [row for row in rows if row[2] != faculty_email_to_delete]
        with open(self.faculty_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        with open(self.faculty_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertTrue(all(row[2] != faculty_email_to_delete for row in rows))
    def test_modify_faculty(self):
        faculty_email_to_modify = "john.doe@faculty.com"
        new_rank = "Junior Professor"
        with open(self.faculty_file, mode='r') as file:
            rows = list(csv.reader(file))
        for row in rows:
            if row[2] == faculty_email_to_modify:
                row[6] = new_rank
        with open(self.faculty_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        with open(self.faculty_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            modified_faculty = next(row for row in rows if row[2] == faculty_email_to_modify)
            self.assertEqual(modified_faculty[6], new_rank)
if __name__ == "__main__":
    unittest.main()
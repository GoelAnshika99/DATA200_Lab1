import csv
class Grade:
    def __init__(self, grade_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/grades.csv"):
        self.grade_file = grade_file
        self.grade_lookup = self.load_grade_lookup()
    def load_grade_lookup(self):
        grade_lookup = {}
        try:
            with open(self.grade_file, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) == 3:
                        grade_lookup[row[0]] = {'max_marks': int(row[1]), 'min_marks': int(row[2])}
        except FileNotFoundError:
            print(f"Error: {self.grade_file} not found.")
        except Exception as e:
            print(f"An error occurred while loading grade lookup: {e}")
        return grade_lookup
    def view_grades(self):
        if self.grade_lookup:
            print("Grade Lookup")
            for grade, info in self.grade_lookup.items():
                print(f"{grade}: Max Marks = {info['max_marks']}, Min Marks = {info['min_marks']}")
        else:
            print("No grade information available.")
import csv
class Course:
    def __init__(self, course_file):
        self.course_file = course_file
    def display_courses(self):
        try:
            with open(self.course_file, mode = 'r') as file:
                reader = csv.reader(file)
                print("\n--------Course Details--------")
                print(f"{'Course Name':<20} {'Course ID':<10} {'Credits':<7}")
                print("-"*40)
                for row in reader:
                    course_name, course_id, credits = row
                    print(f"{course_name:<20} {course_id:<20} {credits:<7}")
        except FileNotFoundError:
            print(f"Error: The file '{self.course_file}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
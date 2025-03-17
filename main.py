from student_system import Student
from login_system import Login
import csv
def main():
    login_file = "C:/Users/aradh/Desktop/DATA 200 Python Programming/Lab1/login.csv"
    try:
        with open(login_file, mode = 'r') as file:
            pass
    except FileNotFoundError:
        with open(login_file, mode = 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["email", "password", "role"])
    login_system = Login(login_file)
    login_system.main_menu()
if __name__ == "__main__":
    main()
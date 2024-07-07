#import pymongo
import subprocess

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # In a real application, you would compare the entered username and password
    # with values stored securely (e.g., in a database).
    # For this example, let's just use hardcoded values.
    if username == "admin" and password == "password":
        print("Login successful!")
        subprocess.Popen(["python","main.py"]) 
    else:
        print("Login failed. Please try again.")

# Main function to run the program
def main():
    print("Welcome to the login form!")
    login()

if __name__ == "__main__":
    main()


import sys
from app.database import init_db, Session
from app.models import User, Medicine, Prescription

def show_menu():
    print("\nSelect an option:")
    print("1. Signup")
    print("2. Login")
    print("3. Search Medicine")
    print("4. Diagnose and Get Prescription")
    print("5. View Prescriptions")
    print("6. Exit")

def signup(session):
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    existing_user = User.find_by_username(session, username)
    if existing_user:
        print("Username already taken!")
    else:
        user = User.create(session, username, password)
        print(f"User {username} created successfully.")

def login(session):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user = User.find_by_username(session, username)
    if user and user.password == password:
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Invalid credentials.")
        return None

def search_medicine(session):
    name = input("Enter the medicine name to search: ")
    medicines = Medicine.search_by_name(session, name)
    if medicines:
        for medicine in medicines:
            print(f"{medicine.id}: {medicine.name} - {medicine.description}")
    else:
        print("No medicines found.")

def diagnose_and_prescribe(session, user):
    sickness = input("Enter your sickness: ")
    medicines = input("Enter comma-separated medicine IDs for your prescription: ").split(',')
    prescribed_medicines = [session.query(Medicine).get(int(medicine_id)) for medicine_id in medicines]
    
    prescription_list = [medicine.name for medicine in prescribed_medicines]
    prescription = Prescription.create(session, user.id, sickness, ", ".join(prescription_list))
    print(f"Prescription created for {sickness}.")

def view_prescriptions(session, user):
    prescriptions = session.query(Prescription).filter_by(user_id=user.id).all()
    if prescriptions:
        for prescription in prescriptions:
            print(f"Diagnosis: {prescription.diagnosis}, Medicines: {prescription.prescribed_medicines}")
    else:
        print("No prescriptions found.")

def main():
    init_db()  # Initialize the database
    session = Session()

    user = None

    while True:
        show_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            signup(session)
        elif choice == "2":
            user = login(session)
        elif choice == "3":
            if user:
                search_medicine(session)
            else:
                print("Please login first.")
        elif choice == "4":
            if user:
                diagnose_and_prescribe(session, user)
            else:
                print("Please login first.")
        elif choice == "5":
            if user:
                view_prescriptions(session, user)
            else:
                print("Please login first.")
        elif choice == "6":
            print("Exiting the program.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

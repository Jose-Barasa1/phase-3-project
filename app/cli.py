from app.database import init_db, Session
from app.models import Medicine, User, Prescription

# Initialize the database
init_db()

# Signup: Create a new user if username is not taken
def signup(username, password):
    session = Session()
    if session.query(User).filter(User.username == username).first():
        print("Username taken.")
    else:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        print(f"User '{username}' created successfully!")

# Login: Check if username and password match an existing user
def login(username, password):
    session = Session()
    user = session.query(User).filter(User.username == username, User.password == password).first()
    if user:
        print("Login successful!")
        return user
    print("Invalid credentials.")
    return None

# Generate diagnosis based on user input
def generate_diagnosis(sickness):
    mapping = {'headache': 'Migraine', 'fever': 'Flu', 'cough': 'Cold', 'allergy': 'Allergic reaction'}
    return mapping.get(sickness.lower(), 'Unknown sickness')

# Create a new medicine in the database
def create_medicine(name, price, description, category):
    session = Session()
    if session.query(Medicine).filter(Medicine.name == name).first():
        print(f"Medicine '{name}' already exists.")
    else:
        session.add(Medicine(name=name, price=price, description=description, category=category))
        session.commit()
        print(f"Medicine '{name}' created successfully.")

# Find Medicine by Category
def find_medicine_by_category(category):
    session = Session()
    medicines = session.query(Medicine).filter(Medicine.category.ilike(f'%{category}%')).all()
    if medicines:
        for med in medicines:
            print(f"{med.name} - {med.price} Ksh - {med.description} ({med.category})")
    else:
        print(f"No medicines found under the category: {category}")

# Find Medicine by Name
def find_medicine_by_name(name):
    session = Session()
    medicine = session.query(Medicine).filter(Medicine.name.ilike(f'%{name}%')).first()
    if medicine:
        print(f"{medicine.name} - {medicine.price} Ksh - {medicine.description} ({medicine.category})")
    else:
        print(f"Medicine '{name}' not found.")

# Main menu after login
def start_cli():
    session = Session()
    logged_in_user = None

    while True:
        if logged_in_user is None:
            print("\nWelcome to MedHub CLI!")
            print("1. Signup")
            print("2. Login")
            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                signup(username, password)
                print("Please login now.")
                username = input("Enter username: ")
                password = input("Enter password: ")
                logged_in_user = login(username, password)  # Log in the user
                if logged_in_user:
                    continue  # If login is successful, continue to the main menu
            elif choice == '2':
                print("Exiting...")
                break
            else:
                print("Invalid option.")
        else:
            # If the user is logged in, show the main menu
            print(f"\nWelcome {logged_in_user.username}!")
            print("1. View all medicines")
            print("2. Find a medicine by name")
            print("3. Find medicines by category")
            print("4. Make a diagnosis and get a prescription")
            print("5. View user info")
            print("6. Log out")
            print("7. Exit")
            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                medicines = Medicine.get_all(session)
                for med in medicines:
                    print(f"{med.name} - {med.price} Ksh - {med.description} ({med.category})")

            elif sub_choice == '2':
                medicine_name = input("Enter medicine name: ")
                find_medicine_by_name(medicine_name)

            elif sub_choice == '3':
                category = input("Enter medicine category (e.g. Pain reliever, Antibiotics, Allergy medicine): ")
                find_medicine_by_category(category)

            elif sub_choice == '4':
                sickness = input("Describe your sickness: ")
                print("Diagnosing...")
                diagnosis = generate_diagnosis(sickness)
                print(f"Diagnosis: {diagnosis}")
                prescribed_medicines = []
                if "headache" in diagnosis:
                    prescribed_medicines.append("Aspirin")
                    prescribed_medicines.append("Ibuprofen")
                if "fever" in diagnosis:
                    prescribed_medicines.append("Paracetamol")
                    prescribed_medicines.append("Ciprofloxacin")

                for med in prescribed_medicines:
                    print(f"- {med}")

                total_price = 0
                for medicine_name in prescribed_medicines:
                    medicine = session.query(Medicine).filter(Medicine.name == medicine_name).first()
                    if medicine:
                        total_price += medicine.price

                print(f"\nTotal price for medicines: {total_price} Ksh")
                confirm_payment = input(f"Do you confirm the payment of {total_price} Ksh? (yes/no): ")
                if confirm_payment.lower() == 'yes':
                    print("Payment successful!")
                    prescription = Prescription(user_id=logged_in_user.id, medicines=prescribed_medicines, total_price=total_price)
                    session.add(prescription)
                    session.commit()
                    print("Prescription saved!")
                else:
                    print("Payment canceled. No prescription created.")

            elif sub_choice == '5':
                print(f"User: {logged_in_user.username}")

            elif sub_choice == '6':  # Log out the user
                print(f"Logging out {logged_in_user.username}...")
                logged_in_user = None  # Reset logged-in user

            elif sub_choice == '7':
                print("Exiting...")
                break

            else:
                print("Invalid option.")

# Run the CLI app
if __name__ == "__main__":
    start_cli()


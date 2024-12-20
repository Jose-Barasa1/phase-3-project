import time
from app.database import init_db, Session
from app.models import Medicine, User, Prescription

init_db()

medicines_list = [
    {'name': 'Aspirin', 'price': 3555.00, 'description': 'Pain reliever', 'category': 'Pain reliever'},
    {'name': 'Paracetamol', 'price': 3456, 'description': 'Fever reducer', 'category': 'Pain reliever'},
    {'name': 'Ibuprofen', 'price': 4000, 'description': 'Anti-inflammatory', 'category': 'Pain reliever'},
    {'name': 'Amoxicillin', 'price': 1235, 'description': 'Antibiotic', 'category': 'Antibiotics'},
    {'name': 'Ciprofloxacin', 'price': 1832, 'description': 'Antibiotic', 'category': 'Antibiotics'},
    {'name': 'Cetirizine', 'price': 7123, 'description': 'Antihistamine', 'category': 'Allergy medicine'},
    {'name': 'Loratadine', 'price': 8000, 'description': 'Allergy medicine', 'category': 'Allergy medicine'}
]

def signup(username, password):
    session = Session()
    if session.query(User).filter(User.username == username).first():
        print("Username already taken.")
    else:
        session.add(User(username=username, password=password))
        session.commit()
        print(f"User {username} created successfully!")

def login(username, password):
    session = Session()
    return session.query(User).filter(User.username == username, User.password == password).first()

def generate_diagnosis(sickness):
    diagnosis = {'headache': 'Migraine or tension headache', 'fever': 'Flu or viral infection', 'cough': 'Cold or respiratory infection', 'allergy': 'Allergic reaction'}
    return diagnosis.get(sickness.lower(), 'Unknown sickness')

# Function to delete a user's profile
def delete_user(logged_in_user):
    session = Session()
    logged_in_user = session.merge(logged_in_user)
    confirm_delete = input(f"Are you sure you want to delete the profile of {logged_in_user.username}? (yes/no): ").lower()
    if confirm_delete == 'yes':
        # Deleting the user
        session.query(Prescription).filter(Prescription.user_id == logged_in_user.id).delete()
        session.delete(logged_in_user)
        session.commit()
        print(f"User {logged_in_user.username} has been deleted successfully.")
        return None  # Return None to log out the user
    else:
        print("User deletion canceled.")
    return logged_in_user  # Return the logged-in user if they canceled

def start_cli():
    session = Session()
    logged_in_user = None
    while True:
        if logged_in_user is None:
            print("\n1. Signup\n2. Exit")
            choice = input("Choice: ")
            if choice == '1':
                username = input("Username: ")
                password = input("Password: ")
                signup(username, password)
                logged_in_user = login(username, password)
            elif choice == '2':
                break
            else:
                print("Invalid choice.")
        else:
            print(f"\nWelcome {logged_in_user.username}!\n1. View medicines\n2. Find medicine\n3. Add medicine\n4. Diagnose and prescribe\n5. User info\n6. Delete profile\n7. Logout\n8. Exit")
            sub_choice = input("Choice: ")

            if sub_choice == '1':
                for med in Medicine.get_all(session): 
                    print(f"{med.name} - {med.price} Ksh - {med.description} ({med.category})")
            elif sub_choice == '2':
                name = input("Enter medicine name: ")
                medicine = Medicine.get_by_name(session, name)
                if medicine: 
                    print(f"Found {name}: {medicine}")
                else: 
                    print(f"{name} not found.")
            elif sub_choice == '3':
                name = input("Name: ")
                price = float(input("Price: "))
                description = input("Description: ")
                category = input("Category: ")
                session.add(Medicine(name=name, price=price, description=description, category=category))
                session.commit()
                print(f"Medicine {name} added.")
            elif sub_choice == '4':
                sickness = input("Describe sickness: ")
                print("Diagnosing...")
                time.sleep(2)  # Delay for effect
                diagnosis = generate_diagnosis(sickness)
                print(f"Diagnosis: {diagnosis}")
                time.sleep(2)  # Wait before showing prescription

                print("Suggested medicines based on diagnosis:")
                time.sleep(1)
                prescribed_meds = ['Aspirin', 'Paracetamol'] if 'headache' in diagnosis else ['Ibuprofen', 'Ciprofloxacin']
                for med in prescribed_meds:
                    print(f"- {med}")
                    time.sleep(1)  # Pause between each medicine

                total = sum(med['price'] for med in medicines_list if med['name'] in prescribed_meds)
                print(f"\nTotal: {total} Ksh")
                time.sleep(2)  # Pause before payment confirmation

                confirm_payment = input(f"Confirm payment of {total} Ksh? (yes/no): ")
                if confirm_payment.lower() == 'yes':
                    print("Processing payment...")
                    time.sleep(2)  # Simulate payment processing time
                    prescription = Prescription(user_id=logged_in_user.id, medicines=prescribed_meds, total_price=total)
                    session.add(prescription)
                    session.commit()
                    print("Payment successful! Prescription saved.")
                else:
                    print("Payment canceled.")
            elif sub_choice == '5':
                print(f"User: {logged_in_user.username}")
            elif sub_choice == '6':
                logged_in_user = delete_user(logged_in_user)  # Call the delete function
            elif sub_choice == '7':
                logged_in_user = None  # Log out the user
            elif sub_choice == '8':
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    start_cli()

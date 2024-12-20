# MedHub CLI Application
 **By Jose' Barasa**

## Project Description
 MedHub is a Python-based Command-Line Interface (CLI) application designed for managing medical data, including user profiles, medicines, and prescriptions. The application leverages SQLAlchemy ORM to interact with a relational database, enabling users to sign up, log in, add and view medicines, receive diagnoses, and generate prescriptions.

 ### Features
- User Management: Users can sign up, log in, and manage their profiles.
- Medicine Inventory: Users can view, add, and search for medicines in the system.
- Diagnosis & Prescription: Based on symptoms, users can receive a diagnosis and suggested medicines with a total cost.
- Prescription History: Users can save and view their prescription history.
- Profile Deletion: Users have the option to delete their profiles.
- Persistent Database: The application uses SQLAlchemy to persist user data, medicines, and prescriptions.
#### Requirements
- Python 3.12 or higher
- SQLAlchemy ORM
- pip (for dependency management)
 
 *** To install the necessary dependencies, run:**

##### bash
Copy code
***pipenv install sqlalchemy***
Alternatively, you can use pipenv:

##### bash
Copy code
***pipenv install***
###### Setup Instructions
Clone the Repository: Clone this repository to your local machine.

##### bash
Copy code
git clone <git@github.com:Jose-Barasa1/phase-3-project.git>

 cd medhub

Install Dependencies: Use the pip or pipenv command to install the dependencies.

- Database Initialization: The database is initialized automatically upon the first run of the application. It uses SQLAlchemy for data modeling.

- Running the Application: To run the application, use the following command:

 ###### bash
Copy code
*** python app/cli.py***
Follow the on-screen prompts to interact with the application.

###### Application Workflow
- Main Menu (Unauthenticated Users)
- Sign Up: Create a new user profile.
- Exit: Exit the application.
- Main Menu (Authenticated Users)
- View Medicines: View all medicines in the inventory.
- Find Medicine: Search for a medicine by name.
- Add Medicine: Add a new medicine to the inventory.
- Diagnose and Prescribe: Receive a diagnosis based on symptoms and a list of prescribed medicines.
- User Info: View information about the logged-in user.
- Delete Profile: Delete the logged-in user's profile.
- Logout: Log out from the application.
- Exit: Exit the application.

##### Example Workflow
- User Sign-Up:
Upon launching the application, users are prompted to create a new account by entering a username and password.

- Medicine Management:
Users can view all medicines, search by name, and add new medicines to the system.

- Diagnosis & Prescription:
By describing symptoms (e.g., "headache"), users receive a diagnosis along with suggested medicines. A payment confirmation process follows the prescription generation.

- Profile Deletion:
Users have the option to delete their profiles, which also removes all associated data.

##### Data Model
The application uses SQLAlchemy ORM to manage three primary models: User, Medicine, and Prescription.

##### User Model
Attributes:

- id: Integer, unique identifier (auto-incremented).
- username: String, unique username.
- password: String, user's password.
- Methods:

- create(): Adds a new user to the database.
- delete(): Deletes a user from the database.
- get_all(): Retrieves all users.
- get_by_id(): Finds a user by their ID.
##### Medicine Model
 Attributes:

- id: Integer, unique identifier (auto-incremented).
- name: String, name of the medicine.
- price: Float, price of the medicine.
- description: String, description of the medicine.
- category: String, category of the medicine (e.g., Pain Reliever, Antibiotic).
##### Methods:

- create(): Adds a new medicine to the database.
- delete(): Deletes a medicine from the database.
- get_all(): Retrieves all medicines.
- get_by_id(): Finds a medicine by its ID.
###### Prescription Model
Attributes:

- id: Integer, unique identifier (auto-incremented).
- user_id: Integer, references the user to whom the prescription belongs.
- medicines: List of medicine names in the prescription.
- total_price: Float, total cost of the prescription.
#### Methods:

- create(): Creates a new prescription.
- get_by_user_id(): Retrieves prescriptions by user ID.
##### Project Structure
The project follows a well-organized structure, which helps with maintainability and scalability:


medhub/
│
├── app/
│   ├── cli.py              # Main CLI script
│   ├── database.py         # Database initialization and session management
│   ├── models.py           # SQLAlchemy models for User, Medicine, and Prescription
│
├── README.md               # Project documentation
└── Pipfile                 # Pipenv dependency file
##### Contributing
If you'd like to contribute to the project, please fork the repository, make your changes, and submit a pull request. Contributions are welcome to improve functionality, fix bugs, or enhance the user experience.

 ##### License
This project is licensed under the MIT License.

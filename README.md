# Student project: software-fishersfritz

The Master's program in Software Projects focuses on applying advanced software development techniques and methodologies practically. 
We gain hands-on experience designing, implementing, and managing complex software projects while integrating cutting-edge technologies and agile practices.

# Introduction

This project, **Fishersfritz**, is an app designed for hobby fishermen to record and manage their fishing catches. Developed as part of the Agile Software Engineering course within the *Digital Technology & Innovation* master's program at [FH Wien der WKW](https://www.fh-wien.ac.at/), this web application provides an intuitive interface for logging fish catches and managing records.
The app also validates whether a specific fish can be caught during the selected time, considering seasonal restrictions ("Schonzeiten") and more.

## Use cases from a fisher's perspective
- **Add a fish catch:** Input details such as fish type, location, date, time, weight, and length.
- **View recorded catches:** See a list of documented catches with relevant details.
- **Edit recorded catches:** Update details of previous entries.
- **Delete recorded catches:** Remove specific catch entries from the list.

### Integrated background operations
- **Season & length validation:** Validate whether the selected fish type can be caught at the chosen time (based on data from the database) or the minimum length.
- **Predefined fish types:** Retrieve and pre-fill the fish selection dropdown with options from the database.
- **Location autofill:** Automatically fill in the current location using GPS.

## Setup instruction
Ensure that Python 3 and flask are installed, along with `pip` for package management.

It is recommended to use a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\Activate.ps1  # Windows
```

### Installation Steps
1. **Navigate to the project root**:
   ```bash
   cd software-fishersfritz
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   ```bash
   cd backend
   python3 setup_db.py  # Initializes the database
   ```

4. **Run backend services**:
   The following Python script must be executed:
   ```bash
   python3 app.py  # Main application
   ```

5. **Run the frontend**:
   Open `frontend/index.html` in your browser or start a local server:
   ```bash
   cd frontend
   python3 -m http.server 4000  # Replace 4000 with an available port if needed
   ```
   Access the application in your browser at `http://localhost:4000/`.

## Adding New Catches
To add new fish catches via the app:
1. Open the application.
2. Fill in the form fields:
   - **Fish type:** Select from the dropdown.
   - **Location:** Coordinates auto-filled via GPS or manually input.
   - **Date & time:** Enter the date and time of the catch.
   - **Weight and length:** Provide additional catch details.
3. Click "Save" to store the entry.

## Managing Catches
- **Edit:** Click the "Edit" button next to an entry to update details.
- **Delete:** Click the "Delete" button to remove a record.

## Credits
This project is part of the Agile Software Engineering course and was built collaboratively to demonstrate key concepts of web app development.

*Lukas Fassl, Usame Firat, Daniel Gunkel, Phillip Sucic*

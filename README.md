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
- **Season validation:** Validate whether the selected fish type can be caught at the chosen time (based on data from the database).
- **Predefined fish types:** Retrieve and pre-fill the fish selection dropdown with options from the database.
- **Location autofill:** Automatically fill in the current location using GPS.

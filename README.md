# Password Strength Analyzer

A Python-based cybersecurity web application that evaluates password strength, identifies common security risks, and provides recommendations to improve password security.

## Features

- **Password Strength Scoring:** Rates passwords on a scale of 0–100.
- **Character Analysis:** Checks password length and character variety.
- **Common Password Detection:** Identifies passwords included in a local common-password list.
- **Pattern Detection:** Detects repeated characters and predictable sequences.
- **Security Risk Analysis:** Highlights potential weaknesses and provides recommendations.
- **Analysis History:** Stores previous assessment metadata using SQLite.
- **Interactive Dashboard:** Displays strength ratings, scores, issues, and suggestions.
- **Automated Tests:** Includes unit tests for core password-analysis logic.

## Tech Stack

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- SQLite
- Python `unittest`

## Project Structure

```text
PasswordStrengthAnalyzer/
├── app.py
├── analyzer.py
├── security.py
├── database.py
├── common_passwords.txt
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   ├── index.html
│   └── history.html
├── static/
│   ├── style.css
│   └── script.js
└── tests/
    └── test_analyzer.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PasswordStrengthAnalyzer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open this address in your browser:

`http://127.0.0.1:5000`

The SQLite database and its table are initialized automatically.

## Run Tests

Run the automated tests from the project root:

```bash
python -m unittest discover -s tests -v
```

## How It Works

1. The user enters a test password in the web interface.
2. Flask validates the request.
3. The analysis module evaluates length, character variety, common-password matches, repeated characters, and predictable sequences.
4. The security module identifies additional password risks.
5. The dashboard displays the score, strength rating, issues, and suggestions.
6. SQLite stores assessment metadata for the history page.

## Privacy and Security

- The database stores assessment metadata, not raw passwords.
- Passwords are sent to the application's Flask backend for analysis.
- The built-in checks are educational heuristics and do not guarantee that a password is secure.
- The search-space estimate is theoretical, not a reliable real-world password-cracking-time prediction.
- The common-password list is limited and does not represent every known compromised password.

**Important:** Do not enter passwords used for real accounts. This project is an educational demonstration, not a substitute for a professional password-security assessment.

## Future Improvements

- Add a privacy-preserving breached-password check using a k-anonymity API.
- Improve password-strength estimation with a maintained password-strength library.
- Add additional unit and integration tests.
- Improve dashboard accessibility and mobile responsiveness.
- Add charts and filtering to analysis history.

## Author

**Sucharita Gali**

Cyber Security Student | Python | Web Development | Cybersecurity Projects
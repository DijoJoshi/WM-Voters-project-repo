# White Matrix Voting System 🗳️

A secure, web-based voting application built with **Flask** and **Google OAuth 2.0**. This system allows users to authenticate via Google, view a list of candidates, and cast a single vote.

## 🚀 Features
* **Google OAuth Integration**: Secure login using Google accounts.
* **One-Vote Logic**: Prevents users from voting more than once.
* **Live Results**: Real-time voter registry and vote tallying.
* **Mobile Responsive**: Works on desktops, tablets, and phones.

## 🛠️ Requirements
To run this project locally, you need:
* Python 3.8 or higher
* A Google Cloud Console project (for OAuth credentials)
* The following Python libraries:
  * `Flask`
  * `Flask-SQLAlchemy`
  * `Flask-Login`
  * `Authlib`
  * `requests`
  * `python-dotenv`
* Tip:Use venv for minimal conflicts and easy cleanup

## 💻 Setup Instructions

1. **First, Clone the repository**:
   ```bash
   git clone https://github.com/DijoJoshi/WM-Voters-project-repo
   cd WM-Voters-project-repo
   ```

2. **Do remember to create an .env in main folder (where app.py is) and input client id and client secrets of your choosing from your own console.**
   ```plaintext
   GOOGLE_CLIENT_ID=your_id_here
   GOOGLE_CLIENT_SECRET=your_secret_here
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
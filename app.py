import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from authlib.integrations.flask_client import OAuth

# Required 4 local testing w/o HTTPS
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "WHITE_MATRIX_VOTING_SECRET"

# Database Configuration (SQLite)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'testvoter.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "home"
oauth = OAuth(app)

# --- GOOGLE OAUTH CONFIGURATION ----
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    has_voted = db.Column(db.Boolean, default=False)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    bio = db.Column(db.String(500))
    linkedin = db.Column(db.String(200))
    vote_count = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('auth_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google')
def auth_google():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(email=user_info['email'], name=user_info['name'])
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('view_candidates'))

@app.route('/test_login')
def test_login():
    user = User.query.filter_by(email="tester@whitematrix.com").first()
    if not user:
        user = User(email="tester@whitematrix.com", name="Internal Tester")
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('view_candidates'))

@app.route('/candidates')
@login_required
def view_candidates():
    candidates = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates)

@app.route('/vote/<int:cid>', methods=['POST'])
@login_required
def vote(cid):
    if not current_user.has_voted:
        candidate = Candidate.query.get(cid)
        candidate.vote_count += 1
        current_user.has_voted = True
        db.session.commit()
    return redirect(url_for('results'))

@app.route('/results')
@login_required
def results():
    voters = User.query.filter_by(has_voted=True).all()
    candidates = Candidate.query.all()
    return render_template('voters.html', voters=voters, candidates=candidates)

@app.route('/stats')
def get_stats():
    candidates = Candidate.query.all()
    stats = {c.name: c.vote_count for c in candidates}
    return render_template('voters.html', stats=stats)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not Candidate.query.first():
            db.session.add_all([
                Candidate(name="Angel Reji",
                          bio="Frontend Specialist",
                          linkedin="https://www.linkedin.com/in/angel-reji-6ab4a2390"),
                Candidate(name="Dijo Joshi", 
                          bio="Backend Specialist",
                          linkedin="https://www.linkedin.com/in/dijojoshi")
            ])
            db.session.commit()
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# SECURITY: This key encrypts your session cookies
app.config['SECRET_KEY'] = 'super-secret-key-123'

# MOCK DATABASE: In a real app, this would be a SQL database
users = {
    "admin": generate_password_hash("password123")
}

@app.route('/')
def home():
    return '<h1>Home Page</h1><a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_password_hash = users.get(username)
        
        # SECURITY: check_password_hash prevents plain-text comparisons
        if user_password_hash and check_password_hash(user_password_hash, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        
        return "Invalid username or password!"
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # AUTHORIZATION: Check if user is actually logged in
    if 'user' in session:
        return f"<h1>Welcome to the Secure Dashboard, {session['user']}!</h1><a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)s
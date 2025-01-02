from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
@login_required
def calculate():
    age = int(request.form['age'])
    gender = request.form['gender']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    body_fat = request.form.get('body_fat')
    goal = request.form['goal']
    dietary_pref = request.form['dietary_pref']
    activity_level = request.form['activity_level']

    # Example BMR calculation using Harris-Benedict equation
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # Adjust BMR based on activity level
    if activity_level == 'sedentary':
        calories = bmr * 1.2
    elif activity_level == 'light':
        calories = bmr * 1.375
    elif activity_level == 'moderate':
        calories = bmr * 1.55
    elif activity_level == 'active':
        calories = bmr * 1.725
    elif activity_level == 'very active':
        calories = bmr * 1.9

    # Adjust calories for goal
    if goal == 'weight_loss':
        calories -= 500
    elif goal == 'weight_gain':
        calories += 500

    # Calculate macronutrient distribution based on dietary preference
    if dietary_pref == 'balanced':
        carbs = 0.5 * calories / 4
        protein = 0.2 * calories / 4
        fats = 0.3 * calories / 9
    elif dietary_pref == 'low_carb':
        carbs = 0.25 * calories / 4
        protein = 0.4 * calories / 4
        fats = 0.35 * calories / 9
    elif dietary_pref == 'high_protein':
        carbs = 0.3 * calories / 4
        protein = 0.4 * calories / 4
        fats = 0.3 * calories / 9

    return render_template('result.html', 
                           calories=f"{calories:.0f}", 
                           carbs=f"{carbs:.0f}", 
                           protein=f"{protein:.0f}", 
                           fats=f"{fats:.0f}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
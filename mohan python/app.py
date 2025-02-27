from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Expense Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Expense {self.name} - {self.amount}>'

# Home Route
@app.route('/')
def index():
    expenses = Expense.query.all()  # Retrieve all expenses
    return render_template('index.html', expenses=expenses)

# Add Expense Route
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date = request.form['date']

        new_expense = Expense(name=name, amount=float(amount), date=date)
        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_expense.html')

# Analyze Route
@app.route('/analyze')
def analyze():
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar()  # Sum of all expenses
    return render_template('analyze.html', total=total_expenses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)

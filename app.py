from flask import Flask, render_template, request, redirect, session
from database_connection import db_connect
from flask import jsonify
app = Flask(__name__)

# Generate a strong secret key
import secrets
app.secret_key = secrets.token_hex(16)

# Establish database connection
db = db_connect()
cursor = db.cursor()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        job = request.form['job']
        department = request.form['department']
        salary = request.form['salary']
        phone = request.form['phone']
        # Save user data to the database
        cursor.execute("INSERT INTO users (firstname, lastname, email, password, job, department, salary, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (firstname, lastname, email, password, job, department, salary, phone))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if user exists in the database
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            session['email'] = email
            return redirect('/employee_list')
        else:
            return "Invalid email or password"
    return render_template('login.html')


@app.route('/employee_list')
def employee_list():
    if 'email' not in session:
        return redirect('/login')
    # Fetch employee details from the database
    cursor.execute("SELECT firstname, lastname, email, job FROM users")
    employees = cursor.fetchall()
    return render_template('employee_list.html', employees=employees)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')



@app.route('/delete/<email>', methods=['POST'])
def delete_employee(email):
    if 'email' not in session or session['email'] != email:
        return jsonify({'error': 'Unauthorized access!'}), 401
    try:
        # Delete the employee from the database
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        db.commit()
        # Return a success response
        return jsonify({'success': True}), 200
    except mysql.connector.Error as e:
        # Return an error response if deletion fails
        return jsonify({'error': str(e)}), 500



@app.route('/view/<email>')
def view_employee(email):
    # Fetch employee details from the database and pass them to the template
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    employee = cursor.fetchone()
    return render_template('view_employee.html', employee=employee)

if __name__ == '__main__':
    app.run(debug=True)


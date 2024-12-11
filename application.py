# application.py
pip install bottle

from bottle import Bottle, request, template
import sqlite3

app = Bottle()

# SQLite connection
conn = sqlite3.connect('hospital_management.db')
cursor = conn.cursor()

# Home route
@app.route('/')
def home():
    # Fetch data from both tables and join them
    cursor.execute('''
        SELECT Hospital.id, Hospital.name, Hospital.location, Management.manager_name, Management.contact_number
        FROM Hospital
        INNER JOIN Management ON Hospital.id = Management.id
    ''')
    result = cursor.fetchall()
    return template('home', rows=result)

# Create route
@app.route('/create', method='GET')
def create_form():
    return template('create')

@app.route('/create', method='POST')
def create():
    # Get data from the form
    name = request.forms.get('name')
    location = request.forms.get('location')
    manager_name = request.forms.get('manager_name')
    contact_number = request.forms.get('contact_number')

    # Insert data into Hospital table
    cursor.execute('INSERT INTO Hospital (name, location) VALUES (?, ?)', (name, location))
    conn.commit()
    hospital_id = cursor.lastrowid

    # Insert data into Management table
    cursor.execute('INSERT INTO Management (id, manager_name, contact_number) VALUES (?, ?, ?)',
                   (hospital_id, manager_name, contact_number))
    conn.commit()

    return home()

# Update route
@app.route('/update/<id>', method='GET')
def update_form(id):
    cursor.execute('SELECT * FROM Hospital WHERE id=?', (id,))
    hospital_data = cursor.fetchone()
    cursor.execute('SELECT * FROM Management WHERE id=?', (id,))
    management_data = cursor.fetchone()
    return template('update', hospital=hospital_data, management=management_data)

@app.route('/update/<id>', method='POST')
def update(id):
    # Get data from the form
    name = request.forms.get('name')
    location = request.forms.get('location')
    manager_name = request.forms.get('manager_name')
    contact_number = request.forms.get('contact_number')

    # Update data in Hospital table
    cursor.execute('UPDATE Hospital SET name=?, location=? WHERE id=?', (name, location, id))
    conn.commit()

    # Update data in Management table
    cursor.execute('UPDATE Management SET manager_name=?, contact_number=? WHERE id=?',
                   (manager_name, contact_number, id))
    conn.commit()

    return home()

# Delete route
@app.route('/delete/<id>')
def delete(id):
    # Delete data from both tables based on hospital ID
    cursor.execute('DELETE FROM Hospital WHERE id=?', (id,))
    conn.commit()
    cursor.execute('DELETE FROM Management WHERE id=?', (id,))
    conn.commit()

    return home()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

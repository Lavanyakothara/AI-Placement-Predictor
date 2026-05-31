from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ==========================
# HOME PAGE
# ==========================
@app.route('/')
def home():
    return render_template('index.html')


# ==========================
# SUBMIT FORM
# ==========================
@app.route('/submit', methods=['POST'])
def submit():

    name = request.form['name']
    cgpa = float(request.form['cgpa'])
    python_skill = int(request.form['python_skill'])
    dsa_skill = int(request.form['dsa_skill'])
    projects = int(request.form['projects'])

    score = (cgpa * 5) + (python_skill * 3) + (dsa_skill * 3) + (projects * 5)

    if score >= 80:
        prediction = "🟢 High Placement Chance"
    elif score >= 60:
        prediction = "🟡 Medium Placement Chance"
    else:
        prediction = "🔴 Low Placement Chance"

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name, cgpa, python_skill, dsa_skill, projects, score)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, cgpa, python_skill, dsa_skill, projects, score))

    conn.commit()
    conn.close()

    return f"""
    <html>
    <body style='font-family:Arial;text-align:center;background:#f5f5f5;padding:50px;'>

    <div style='background:white;padding:30px;border-radius:20px;width:500px;margin:auto;'>

    <h1>🚀 Placement Result</h1>

    <h3>Name: {name}</h3>

    <h2 style='color:#4f46e5'>
    Placement Score: {score}
    </h2>

    <h2>{prediction}</h2>

    <br>

    <a href='/'>🏠 Home</a><br><br>
    <a href='/students'>👥 Students</a><br><br>
    <a href='/dashboard'>📊 Dashboard</a>

    </div>

    </body>
    </html>
    """


# ==========================
# ALL STUDENTS
# ==========================
@app.route('/students')
def students():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    output = """
    <h1>👥 All Students</h1>

    <a href='/'>Home</a><hr>
    """

    for student in data:

        output += f"""
        <p>
        <b>ID:</b> {student[0]}<br>
        <b>Name:</b> {student[1]}<br>
        <b>CGPA:</b> {student[2]}<br>
        <b>Score:</b> {student[6]}<br>

        <a href='/delete/{student[0]}'>
        Delete Student
        </a>

        </p>
        <hr>
        """

    return output


# ==========================
# SEARCH PAGE
# ==========================
@app.route('/search')
def search():

    return """
    <h1>🔍 Search Student</h1>

    <form action='/search_result' method='POST'>

    <input type='text'
    name='name'
    placeholder='Enter Student Name'>

    <input type='submit'
    value='Search'>

    </form>
    """


# ==========================
# SEARCH RESULT
# ==========================
@app.route('/search_result', methods=['POST'])
def search_result():

    name = request.form['name']

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE name=?",
        (name,)
    )

    student = cursor.fetchone()

    conn.close()

    if student:

        return f"""
        <h1>Student Found</h1>

        <p>Name: {student[1]}</p>
        <p>CGPA: {student[2]}</p>
        <p>Score: {student[6]}</p>

        <a href='/search'>Search Again</a>
        """

    return """
    <h1>Student Not Found</h1>
    <a href='/search'>Try Again</a>
    """


# ==========================
# RANKING
# ==========================
@app.route('/ranking')
def ranking():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, score FROM students ORDER BY score DESC"
    )

    students = cursor.fetchall()

    conn.close()

    output = "<h1>🏆 Student Ranking</h1>"

    rank = 1

    for student in students:

        output += f"""
        <p>
        Rank {rank} :
        {student[0]}
        -
        {student[1]}
        </p>
        """

        rank += 1

    return output


# ==========================
# DASHBOARD
# ==========================
@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(score) FROM students")
    highest_score = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM students")
    average_score = cursor.fetchone()[0]

    cursor.execute(
        "SELECT name, score FROM students ORDER BY score DESC LIMIT 1"
    )

    top_student = cursor.fetchone()

    conn.close()

    return f"""
    <html>

    <head>

    <style>

    body{{
        font-family:Arial;
        background:linear-gradient(135deg,#4f46e5,#7c3aed,#ec4899);
        padding:30px;
    }}

    h1{{
        color:white;
        text-align:center;
    }}

    .dashboard{{
        display:grid;
        grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
        gap:20px;
    }}

    .card{{
        background:white;
        padding:25px;
        border-radius:20px;
        text-align:center;
    }}

    .value{{
        font-size:28px;
        font-weight:bold;
    }}

    </style>

    </head>

    <body>

    <h1>📊 Dashboard</h1>

    <div class='dashboard'>

        <div class='card'>
            <h2>👥 Students</h2>
            <div class='value'>{total_students}</div>
        </div>

        <div class='card'>
            <h2>🏆 Highest Score</h2>
            <div class='value'>{highest_score}</div>
        </div>

        <div class='card'>
            <h2>📈 Average Score</h2>
            <div class='value'>{round(average_score,2)}</div>
        </div>

        <div class='card'>
            <h2>🚀 Top Student</h2>
            <div class='value'>{top_student[0]}</div>
            <p>{top_student[1]}</p>
        </div>

    </div>

    <br>

    <a href='/' style='color:white'>
    Home
    </a>

    </body>

    </html>
    """


# ==========================
# DELETE STUDENT
# ==========================
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return """
    <h1>Student Deleted Successfully</h1>

    <a href='/students'>
    Back to Students
    </a>
    """


# ==========================
# RUN APP
# ==========================
if __name__ == '__main__':
    app.run(debug=True)
from os.path import dirname, join as join_path
from os import chdir
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# DEMO STUFF

@app.route('/')
def view_hello():
    return 'Hello World!'

@app.route('/demo-1')
def view_demo_1():
    return render_template('demo-1.html', name='bob')

@app.route('/demo-2/<name>')
def view_demo_2(name):
    return render_template('demo-1.html', name=name)

@app.route('/demo-3')
def view_demo_3():
    names = ['Alice', 'Bob', 'Charlie']
    return render_template('demo-3.html', salutation='Roll call', names=names)

# STUDENT DIRECTORY APP

class Student:
    def __init__(self, first_name, last_name, username, majors, advisor):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.majors = majors
        self.advisor = advisor

def get_data():
    students = []
    with open(join_path(dirname(__file__), 'students.csv')) as fd:
        for line in fd.read().splitlines():
            name, username, majors, advisor = line.split('\t')
            last_name, first_name = name.split(', ')
            students.append(Student(first_name, last_name, username, majors, advisor))
    return sorted(students, key=(lambda s: s.username))

@app.route('/directory')
def view_directory():
    stu = get_data()
    return render_template('directory.html', students = stu)

@app.route('/directory/<username>')
def view_student(username):
    my_list = get_data()
    for student in my_list:
        if student.username == username:
            student = student
            number = my_list.index(student)
            if my_list.index(student) == 0:
                previous_student = my_list[-1]
                next_student = my_list[number + 1]
            elif my_list.index(student) == len(my_list) - 1:
                next_student = my_list[0]
                previous_student = my_list[number - 1]
            else:
                next_student = my_list[number + 1]
                previous_student = my_list[number - 1]
            return render_template('student.html', student = student, prev_student = previous_student, next_student = next_student)

# DON'T TOUCH THE CODE BELOW THIS LINE

@app.route('/css/<file>')
def view_css(file):
    return send_from_directory('css', file)

@app.route('/images/<file>')
def view_images(file):
    return send_from_directory('images', file)

if __name__ == '__main__':
    #print(get_data())
    chdir(dirname(__file__))
    app.run(debug=True)

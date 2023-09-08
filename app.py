import os
import asyncio

from flask import Flask,request,render_template,make_response,jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
from src.database.connect import get_db_connection
from src.tasks.notifications import notifications


template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)
CORS(app, resources={r'/*': {'origins': '*'}})

sched = BackgroundScheduler(daemon=True)
sched.add_job(notifications,'interval',seconds=30)
sched.start()


@app.route("/")
def home():
     return render_template('index.html')

@app.route("/templates/equipes",methods=['GET','POST'])
def equipes():
    if request.method == 'GET':  
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from shifts")
        shifts = cursor.fetchall()
        print(shifts)
        return render_template("equipes.html",shifts=shifts)
    else:
        data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        sql = f"INSERT INTO shifts (name,description) VALUES('{data['name']}','{data['description']}')"        
        cursor.execute(sql)
        connection.commit()
        return jsonify({'data': data})
        
@app.route("/templates/funcionarios",methods=['GET','POST'])
def funcionarios():
    if request.method == 'GET':   
        connection = get_db_connection()
        cursor_shifts = connection.cursor(dictionary=True)
        cursor_shifts.execute("select * from shifts")
        shifts = cursor_shifts.fetchall()
        
        cursor_contributions = connection.cursor(dictionary=True)
        cursor_contributions.execute("select * from contributions")
        contributions = cursor_contributions.fetchall()

        return render_template("funcionarios.html", shifts=shifts, contributions=contributions)
    else: 
        data = request.get_json()
        print(data)
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        sql = f"INSERT INTO contributions (shift_id,name,phone,email) VALUES({int(data['shift_id'])},'{data['name']}','{data['phone']}','{data['email']}')"
        cursor.execute(sql)
        connection.commit()
        return jsonify({'data': data})

@app.route("/templates/tarefas",methods=['GET','POST'])
def tarefas():
    if request.method == 'GET':
        connection = get_db_connection()
        cursor_tasks = connection.cursor(dictionary=True)
        cursor_tasks.execute("select * from tasks")
        tasks = cursor_tasks.fetchall()       
        return render_template("tarefas.html",tasks=tasks)
    else:  
        data = request.get_json()
        print(data)
        sql = f"INSERT INTO tasks (name, description) VALUES('{data['name']}','{data['description']}')"
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql)
        connection.commit()      
        return jsonify({'data':data})

@app.route("/templates/horarios",methods=['GET','POST'])
def horarios():   
    if request.method == 'GET':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from schedules")
        schedules = cursor.fetchall()
        return render_template("horarios.html",schedules=schedules)
    else:
        data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        sql = f"INSERT INTO schedules (time) VALUES('{data['time']}')"
        cursor.execute(sql)
        connection.commit()
        return jsonify({'data': data})

@app.route("/templates/tarefas_colaboradores",methods=['GET','POST'])
def tarefas_colaboradores():
    if request.method == 'GET':
        connection = get_db_connection()

        cursor_tasks = connection.cursor(dictionary=True)
        cursor_tasks.execute("select * from tasks")
        tasks = cursor_tasks.fetchall()

        cursor_contribution = connection.cursor(dictionary=True)
        cursor_contribution.execute("select * from contributions")
        contributions = cursor_contribution.fetchall()
        return render_template("tarefas_colaboradores.html",tasks=tasks, contributions=contributions)
    else:
        data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        sql = f"INSERT INTO contributors_tasks (contributor_id,task_id) VALUES ({int(data['contributor_id'])},{int(data['task_id'])})"
        cursor.execute(sql)
        connection.commit()
        return jsonify({'data': data})
    
@app.route("/templates/tarefas_schedules", methods=['GET','POST'])
def tarefas_schedules():
    if request.method == 'GET':
        connection = get_db_connection()
        cursor_tasks = connection.cursor(dictionary=True)
        cursor_tasks.execute("select * from tasks")
        tasks = cursor_tasks.fetchall()

        cursor_schedules = connection.cursor(dictionary=True)
        cursor_schedules.execute("select * from schedules")
        schedules = cursor_schedules.fetchall()        
        return render_template("tarefas_schedules.html",tasks=tasks, schedules=schedules)
    
    else:
        data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        sql = f"INSERT INTO schedules_tasks (task_id,schedule_id) VALUES({int(data['task_id'])},{int(data['schedule_id'])})"
        print(sql)
        cursor.execute(sql)
        connection.commit()
        return jsonify({'data': data})


@app.route("/api/schedules", methods=['GET','POST'])
def schedules():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        response_object['message'] = 'schedules added!'
    else:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from tasks")
        result = cursor.fetchall()
        response_object['schedules'] = result
    return jsonify(response_object)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0',port=80)
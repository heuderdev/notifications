import asyncio

from src.database.connect import get_db_connection

from mysql.connector import  Error

import uuid

import datetime
def notifications():
    print("notifications")
    agora = datetime.datetime.now().strftime("%H:%M")
    try:
      connection =get_db_connection()
      cursor = connection.cursor()
      sql=f"SELECT  DISTINCT  contributions.id as contributions_id, tasks.id as tasks_id,tasks.name AS tasks_name, schedules.time AS schedules_time, contributions.name AS contributions_name	from tasks   inner join schedules_tasks on schedules_tasks.task_id = tasks.id inner join schedules on schedules.id = schedules_tasks.schedule_id   inner join contributors_tasks on  contributors_tasks.task_id = tasks.id   inner join contributions on contributions.id = contributors_tasks.contributor_id WHERE schedules.time = '14:20'"
      cursor.execute(sql)
      notification = cursor.fetchall()     
      print(notification)
      for r in notification:
        sql = f"INSERT INTO notifications (code_uuid,task_id,contributor_id) VALUES('{str(uuid.uuid4())}','{r[1]}','{r[0]}')"
        cursor.execute(sql)
        connection.commit()
    except Error as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import sqlite3
import json
from rest_framework.authentication import TokenAuthentication

# --------------------
# DB CONNECTION
# --------------------
def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

# --------------------
# HTML VIEWS (No Auth)
# --------------------
def index(request):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM task').fetchall()
    conn.close()
    return render(request, 'task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        status = request.POST['status']
        conn = get_db_connection()
        conn.execute('INSERT INTO task (title, description, due_date, status) VALUES (?, ?, ?, ?)',
                     (title, description, due_date, status))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/')
    return render(request, 'add_task.html')

def delete_task(request, task_id):
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('DELETE FROM task WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
    return redirect('/')

def update_status(request, task_id):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM task WHERE id = ?", (task_id,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return redirect(reverse('task_list'))

        current_status = result[0]
        new_status = "Completed" if current_status == "Pending" else "Pending"
        cursor.execute("UPDATE task SET status = ? WHERE id = ?", (new_status, task_id))
        conn.commit()
        conn.close()
        return redirect(reverse('task_list'))

def completed_tasks(request):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM task WHERE status = "Completed"').fetchall()
    conn.close()
    return render(request, 'completed_tasks.html', {'tasks': tasks})

# --------------------
# API VIEWS (JWT Protected)
# --------------------
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_tasks(request):
    if request.method == 'GET':
        conn = get_db_connection()
        tasks = conn.execute('SELECT * FROM task').fetchall()
        conn.close()
        return JsonResponse([dict(task) for task in tasks], safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        required_fields = ['title', 'description', 'due_date', 'status']
        missing = [field for field in required_fields if field not in data]
        if missing:
            return JsonResponse(
                {"error": f"Missing required fields: {', '.join(missing)}"},
                status=400
            )

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO task (title, description, due_date, status) VALUES (?, ?, ?, ?)',
            (data['title'], data['description'], data['due_date'], data['status'])
        )
        conn.commit()
        conn.close()
        return JsonResponse({'message': 'Task created successfully.'}, status=201)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_task_detail(request, task_id):
    conn = get_db_connection()
    if request.method == 'GET':
        task = conn.execute('SELECT * FROM task WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        if task:
            return JsonResponse(dict(task))
        else:
            return JsonResponse({'error': 'Task not found'}, status=404)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        conn.execute('UPDATE task SET title=?, description=?, due_date=?, status=? WHERE id=?',
                     (data['title'], data['description'], data['due_date'], data['status'], task_id))
        conn.commit()
        conn.close()
        return JsonResponse({'message': 'Task updated successfully.'})

    elif request.method == 'DELETE':
        conn.execute('DELETE FROM task WHERE id=?', (task_id,))
        conn.commit()
        conn.close()
        return JsonResponse({'message': 'Task deleted successfully.'})

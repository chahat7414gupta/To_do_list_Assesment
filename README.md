
# 📝 To-Do List Project (Django + SQLite)

A simple To-Do List web application built using **Django**, with:

- RESTful APIs using raw SQL (no ORM)
- Web interface using HTML templates
- SQLite for database
- Manual table setup (no models used)

---

## 🚀 Features

- Create, view, update, and delete tasks via API
- Add and manage tasks via HTML forms
- Tasks include: `title`, `description`, `due_date`, and `status`
- Mark task as completed from UI and move to a separate "Completed Tasks" list

---

## ⚙️ Setup Instructions

### 1. Install Django
```bash
pip install django
```

### 2. Clone the Project
```bash
git clone <your-repo-url>
cd todo_project_Company
```

### 3. Create the Database Table (manual step)
Use SQLite or VS Code extension to run this SQL:

```sql
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    due_date TEXT,
    status TEXT
);
```

### 4. Run Migrations and Start Server
```bash
python manage.py migrate
python manage.py runserver
```

---

## 🌐 Web Access

- Open in browser: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Add Task: `/add/`
- Completed Tasks: Automatically shown on main page

---

## 🔌 API Endpoints

### 🔍 Get All Tasks
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/
```

### ➕ Create Task
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/   -H "Content-Type: application/json"   -d '{"title":"New Task","description":"Details","due_date":"2025-08-10","status":"Pending"}'
```

### 📄 Get Task by ID
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/1/
```

### ✏️ Update Task by ID
```bash
curl -X PUT http://127.0.0.1:8000/api/tasks/1/   -H "Content-Type: application/json"   -d '{"title":"Updated","description":"Updated","due_date":"2025-08-15","status":"Completed"}'
```

### ❌ Delete Task by ID
```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/
```

---

## 🖥️ Frontend Functionality

- View tasks on homepage
- Add task via `/add/`
- Change task status via "Mark Completed" button
- Completed tasks are shown in a separate list

---

## 🧪 Testing

You can use `curl`, Postman, or browser to test endpoints.  
Basic functionality is verified via browser and API requests.

---

## 🧠 Notes

- ✅ No ORM: Uses `sqlite3` and raw SQL
- ✅ CSRF protection enabled on all forms
- ✅ Templates used for displaying and adding tasks
- ✅ Task status toggle available from frontend
- ❌ No authentication or user management

---

## 📦 Deployment

For testing or lightweight production:
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🛠️ VS Code Extension to View Database

- **SQLite** by Alex Covizzi  
  🔗 https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite

Use it to view and modify `db.sqlite3` in GUI.

---

## 📁 Project Structure

```
todo_project_Company/
├── manage.py
├── db.sqlite3
├── taskmanager/
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   ├── add_task.html
│   │   └── list_tasks.html
│   └── ...
└── ...
```

---

## 📬 Contact

For any issues, feel free to raise an issue or contact the project owner.

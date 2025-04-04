# 📝 Notes API

A powerful Notes application built with Django REST Framework that supports user authentication, categorized note management, search functionality, and AI-powered note summarization using the OpenAI API.

API Documentation: https://documenter.getpostman.com/view/37120850/2sB2cUA2pu

---

## 🚀 Features

- ✅ User registration and JWT-based authentication  
- 🧠 AI-generated note summarization via OpenAI API  
- 🗂️ Categorize and tag notes  
- 🔍 Search by title, tag, or category  
- 📬 Email reminders (background tasks using Celery)  
- 🧱 Full CRUD for notes  

---

## 🛠️ Tech Stack

- Django + Django REST Framework  
- MySQL  
- JWT Authentication  
- OpenAI API  
- Celery  

---

## 🔐 Authentication

Most endpoints require JWT authentication.  
Send your token via the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

---

## 📚 Endpoints

### 1. Register

**POST** `/notesapi/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "username": "username",
  "email": "valid_email@example.com",
  "password": "strong_password"
}
```

**Responses:**
- `201 Created` – Successfully registered
- `400 Bad Request` – Invalid input data

---

### 2. Login

**POST** `/notesapi/auth/login`

Authenticate the user and receive JWT tokens.

**Request Body:**
```json
{
  "email": "valid_email@example.com",
  "password": "your_password"
}
```

**Responses:**
- `200 OK` – Successfully logged in (returns tokens)
- `400 Bad Request` – Invalid credentials

---

### 3. Create a Note

**POST** `/notesapi/notes`

Create a new note.

**Request Body:**
```json
{
  "title": "Meeting Notes",
  "category": { "name": "work" },
  "tags": ["meeting", "work", "important"],
  "content": "Discussed project milestones and deadlines.",
  "reminder_date": "2025-04-10"
}
```

**Responses:**
- `201 Created` – Note created
- `400 Bad Request` – Invalid input data

---

### 4. Get All Notes

**GET** `/notesapi/notes`

Retrieve all notes.

**Responses:**
- `200 OK` – List of notes
- `401 Unauthorized` – Missing or invalid token

---

### 5. Search Notes by Title

**GET** `/notesapi/note/title/<note_title>`

**Responses:**
- `200 OK` – Notes found
- `404 Not Found` – No notes with the given title

---

### 6. Update Note by Title

**PUT** `/notesapi/note/title/<note_title>`

Update note content by its title.

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "category": { "name": "updated-category" },
  "tags": ["tag1", "tag2"],
  "reminder_date": "2025-05-01"
}
```

**Responses:**
- `200 OK` – Note updated
- `400 Bad Request` – Invalid input
- `404 Not Found` – Note not found

---

### 7. Delete Note by Title

**DELETE** `/notesapi/note/title/<note_title>`

**Responses:**
- `204 No Content` – Successfully deleted
- `404 Not Found` – Note not found

---

### 8. Get Notes by Category

**GET** `/notesapi/notes/search/category/<category_name>`

**Responses:**
- `200 OK` – Notes found
- `404 Not Found` – No notes in this category

---

### 9. Get All Categories

**GET** `/notesapi/categories`

**Responses:**
- `200 OK` – List of categories

---

### 10. Bulk Delete Notes by Category

**DELETE** `/notesapi/notes/bulkdelete/category/<category_name>`

**Responses:**
- `204 No Content` – Notes deleted
- `404 Not Found` – No matching notes

---

### 11. Search Notes by Tag

**GET** `/notesapi/notes/search/tag/<tag_name>`

**Responses:**
- `200 OK` – Notes with the tag
- `404 Not Found` – No notes with this tag

---

### 12. Bulk Delete Notes by Tag

**DELETE** `/notesapi/notes/bulkdelete/tag/<tag_name>`

**Responses:**
- `204 No Content` – Notes deleted
- `404 Not Found` – No notes found





Celery Integration in Notes API
This project uses Celery for asynchronous task processing. Celery is a distributed task queue that allows you to run tasks in the background, such as sending reminder emails for notes. Below is an explanation of how celery.py and task.py are configured and how they work together.

Celery Configuration (celery.py)
The celery.py file is the entry point for configuring Celery in the project. It sets up the Celery app and schedules periodic tasks using Celery Beat.

Key Components:
Environment Setup:

The os.environ.setdefault ensures that the Django settings module is loaded for Celery to access the project's configuration.
Celery App Initialization:

The Celery app is initialized with the project name (Notes_API).
Task Scheduling:

The beat_schedule dictionary defines periodic tasks. In this case, the send_email_to_remind task is scheduled to run daily at 6:00 (6:0 AM).
Configuration:

Celery is configured to use Django settings by specifying the namespace='CELERY'.
Task Auto-discovery:

The app.autodiscover_tasks() automatically discovers tasks defined in the tasks.py file of installed Django apps.

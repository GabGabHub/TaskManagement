import requests
from webScrapper import scrape_github_issues

API_URL = "http://127.0.1.1:8008/"

def create_task(title, description, priority):
    payload = {
        "title": title,
        "description": description,
        "priority": priority
    }
    r = requests.post(f"{API_URL}/tasks/", json=payload)
    return r.json()

def get_tasks():
    r = requests.get(f"{API_URL}/tasks/")
    return r.json()

def assign_task(task, current_user):
    if not current_user:
        return {"error": "Not logged in"}

    r = requests.put(
        f"{API_URL}/tasks/{task}",
        json=current_user["username"]
    )
    return r.json()

def complete_task(task):
    r = requests.put(
        f"{API_URL}/tasks/complete/{task}",
    )
    return r.json()

def delete_task(task):
    r = requests.delete(
        f"{API_URL}/tasks/{task}",
    )
    return r.json()


def format_tasks(tasks):
    if not tasks:
        return "No tasks found."
    output = ""
    for t in tasks:
        output += (
            f"Title: {t['title']}\n"
            f"Description: {t['description']}\n"
            f"Status: {t['status']}\n"
            f"Priority: {t['priority']}\n"
            f"Assigned To: {t['assignedTo']}\n"
            "------------------------\n"
        )
    return output

# f"Title: {t["title"]}\n"
#             f"Description: {t["description"]}\n"
#             f"Status: {t["status"]}\n"
#             f"Priority: {t["priority"]}\n"
#             f"Assigned To: {t["assignedTo"]}\n"

def login_or_create(username, role):
    if not username:
        return "Username cannot be empty."

    USERS = requests.get(f"{API_URL}/users/").json()
    
    if username in [x['username'] for x in USERS]:
        for name in USERS:
            if name['username'] == username:
                user = name
        return f"Welcome back, {user['username']} ({user['role']})!", user
    else:
        payload = {
            "username": username,
            "role": role,
        }
        requests.post(f"{API_URL}/users/", json=payload)

        return f"User {username} created with role '{role}'.", payload

def show_task(tasks, index):
    if not tasks:
        return "No tasks imported yet.", index
    index = max(0, min(index, len(tasks)-1))
    task = tasks[index]
    task_text = f"**{task['title']}**\n\n{task['description']}\n"
    return task_text, index

def load_tasks():
    tasks = scrape_github_issues()
    index = 0
    return tasks, index, *show_task(tasks, index)

def scroll_left(tasks, index):
    index = max(0, index-1)
    return show_task(tasks, index)

def scroll_right(tasks, index):
    index = min(len(tasks)-1, index+1)
    return show_task(tasks, index)

def import_current_task(tasks, index, priority):
    task = tasks[index]
    msg = create_task(task['title'], task['description'], priority)
    return msg


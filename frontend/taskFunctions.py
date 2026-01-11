import requests

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

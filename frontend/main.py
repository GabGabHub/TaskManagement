import datetime
import gradio as gr
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

def assign_task(task, username):
    r = requests.put(
        f"{API_URL}/tasks/{task}",
        json=username
    )
    return current_user

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
            f"Title: {t["title"]}\n"
            f"Description: {t["description"]}\n"
            f"Status: {t["status"]}\n"
            f"Priority: {t["priority"]}\n"
            f"Assigned To: {t["assignedTo"]}\n"
            "------------------------\n"
        )
    return output




def login_or_create(username, role, user_state):
    if not username:
        return "Username cannot be empty.", user_state

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

        user = {"username": username, "role": role}
        return f"User {username} created with role '{role}'.", user






with gr.Blocks(title="Task Management App") as demo:
    current_user = gr.State(None)
    current_user.value = {}

    gr.Markdown("# Task Management Dashboard")

    with gr.Tab("Login"):
        gr.Markdown("### Login or Create User")

        username_input = gr.Textbox(label="Username")
        role_input = gr.Dropdown(
            choices=["user", "admin"],
            value="user",
            label="Role"
        )

        login_btn = gr.Button("Login / Create")
        status_output = gr.Textbox(label="Status", interactive=False)

        login_btn.click(
            fn=login_or_create,
            inputs=[username_input, role_input, current_user],
            outputs=[status_output, current_user]
            )

    with gr.Tab("Welcome"):
        title = gr.Textbox(f"Welcome! {current_user}")
        update_btn = gr.Button("Update")

        def update():
            title.value = current_user

        update_btn.click(
            fn= update
        )

    with gr.Tab("Create Task"):
        title = gr.Textbox(label="Title")
        description = gr.Textbox(label="Description")
        priority = gr.Dropdown(["low", "medium", "high"], label="Priority")
        create_btn = gr.Button("Create Task")
        create_output = gr.JSON()

        create_btn.click(
            create_task,
            inputs=[title, description, priority],
            outputs=create_output
        )

    with gr.Tab("View Tasks"):
        load_btn = gr.Button("Load Tasks")
        tasks_output = gr.Textbox(lines=15)

        load_btn.click(
            lambda: format_tasks(get_tasks()),
            outputs=tasks_output
        )

    with gr.Tab("Assign Task"):
        task = gr.Textbox(label="Task Name")
        username = current_user
        assign_btn = gr.Button("Assign to Me")
        assign_output = gr.JSON()

        assign_btn.click(
            assign_task,
            inputs=[task],
            outputs=assign_output
        )
    
    with gr.Tab("Complete Task"):
        task = gr.Textbox(label="Task Name")
        assign_btn = gr.Button("Complete")
        assign_output = gr.JSON()

        assign_btn.click(
            complete_task,
            inputs=[task],
            outputs=assign_output
        )

    with gr.Tab("Delete Task"):
        task = gr.Textbox(label="Task Name")
        assign_btn = gr.Button("Delete")
        assign_output = gr.JSON()

        assign_btn.click(
            delete_task,
            inputs=[task],
            outputs=assign_output
        )

demo.launch()
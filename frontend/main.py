import gradio as gr
import requests

from taskFunctions import create_task,complete_task,get_tasks,assign_task,delete_task,format_tasks

API_URL = "http://127.0.1.1:8008/"


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

with gr.Blocks(title="Task Management App") as demo:
    current_user = gr.State({})

    gr.Markdown("# Task Management Dashboard")

    with gr.Tab("Login"):
        gr.Markdown("### Login or Create User")

        username_input = gr.Textbox(label="Username")
        role_input = gr.Dropdown(["user", "admin"], value="user")
        login_btn = gr.Button("Login / Create")
        status_output = gr.Textbox(interactive=False)

        login_btn.click(
            fn=login_or_create,
            inputs=[username_input, role_input],
            outputs=[status_output, current_user]
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
            inputs=[task, current_user],
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
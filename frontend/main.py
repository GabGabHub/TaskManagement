import gradio as gr
import requests

from taskFunctions import create_task,complete_task,get_tasks,assign_task,delete_task,format_tasks,show_task,load_tasks,scroll_left,scroll_right,import_current_task,login_or_create

API_URL = "http://127.0.1.1:8008/"

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

    with gr.Tab("Import issues from Github"):
        import_btn = gr.Button("Load Tasks from Github")
        
        with gr.Row("Task"):
            with gr.Column(scale=1):
                pass  
            with gr.Column(scale=2, min_width=300):
                task_display = gr.Markdown("No tasks loaded yet", elem_classes="centered")
            with gr.Column(scale=1):
                pass  

        priority = gr.Dropdown(["low", "medium", "high"], label="Priority")
        
        with gr.Row("Buttons"):
            left_btn = gr.Button("⟵")
            import_btn_task = gr.Button("Import Task")
            right_btn = gr.Button("⟶")
        
        status = gr.JSON()
        
        tasks_state = gr.State([])
        index_state = gr.State(0)
        
        import_btn.click(load_tasks, outputs=[tasks_state, index_state, task_display, index_state])
        left_btn.click(scroll_left, inputs=[tasks_state, index_state], outputs=[task_display, index_state])
        right_btn.click(scroll_right, inputs=[tasks_state, index_state], outputs=[task_display, index_state])
        import_btn_task.click(import_current_task, inputs=[tasks_state, index_state, priority], outputs=status)

demo.launch()
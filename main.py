from fasthtml.common import *

app,rt = fast_app()

@rt('/')
def get():
    information = Div("Download a file you can import into your calendar.")

    # TODO: https://docs.fastht.ml/tutorials/quickstart_for_web_devs.html#forms
    due_date = Input(id="due-date", name="due-date", type="date", placeholder="Due date")
    form = Form(Group(due_date, Button("Download")))

    return Title('Preg Cal'), Main(H1('Pregnancy Calendar'), information, form, cls='container')

# python main.py
serve()
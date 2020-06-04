from app import app


@app.route('/')
def homepage():
    return '<h1 style="color:red;">Hi yashodara</h1>'

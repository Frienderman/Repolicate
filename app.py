from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def show_index():
    with open("index.html") as file:
        return file.read()

if __name__ == "__main__":
    app.run()
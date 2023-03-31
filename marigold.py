from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run(debug="True")



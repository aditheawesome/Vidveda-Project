from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")


def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)


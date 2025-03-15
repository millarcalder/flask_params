from flask_parameters import Flask

app = Flask(__name__)


@app.route("/foo")
def foo(arg, kwarg=123) -> dict:
    return {"arg": arg, "kwarg": kwarg}


@app.route("/strict_foo")
def strict_foo(arg: str, kwarg: int = 123) -> dict:
    return {"arg": arg, "kwarg": kwarg}


if __name__ == "__main__":
    app.run()

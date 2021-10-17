from flask import render_template

from dolt import app


@app.errorhandler(401)
def bad_request(_):
    return render_template("errors/401.html"), 401


@app.errorhandler(404)
def page_not_found(_):
    return render_template("errors/404.html"), 404

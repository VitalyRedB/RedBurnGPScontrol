from flask import Flask, jsonify, render_template, request
from db import get_points
from add_point import handle_add_point

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/api/points")
def api_points():
    user_id = request.args.get("user_id")
    date = request.args.get("date")
    time_from = request.args.get("time_from")
    time_to = request.args.get("time_to")

    points = get_points(user_id=user_id, date=date, time_from=time_from, time_to=time_to)
    return jsonify([
        {"user_id": p[0], "date": p[1], "time": p[2], "lat": p[3], "lon": p[4]}
        for p in points
    ])

@app.route("/api/add_point", methods=["POST"])
def api_add_point():
    return handle_add_point()

if __name__ == "__main__":
    app.run(debug=True)




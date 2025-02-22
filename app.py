from flask import Flask, render_template, request, redirect, url_for, jsonify, session, Response
import cv2
from detector import Monitor  # OpenCV monitoring script

app = Flask(_name_)
app.secret_key = "your_secret_key"  # Required for session management
monitor = Monitor()

# Dummy user credentials (Replace with database logic)
VALID_USERNAME = "student"
VALID_PASSWORD = "password123"

camera = cv2.VideoCapture(0)  # Initialize camera


def gen_frames():
    """ Generate frames from the webcam for live streaming. """
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/", methods=["GET", "POST"])
def login():
    """ Handle user login. """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username  # Store session
            return redirect(url_for("exam"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/exam")
def exam():
    """ Exam page with live monitoring (only accessible after login). """
    if "user" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in
    return render_template("monitor.html")


@app.route("/logout")
def logout():
    """ Logout and clear session. """
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/video_feed")
def video_feed():
    """ Live video streaming route. """
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/start_camera")
def start_camera():
    """ Start camera monitoring. """
    monitor.start_monitoring()
    return jsonify({"status": "Camera Started"})


@app.route("/stop_camera")
def stop_camera():
    """ Stop camera monitoring. """
    monitor.stop_monitoring()
    return jsonify({"status": "Camera Stopped"})


@app.route("/check_suspicious")
def check_suspicious():
    """ Check for suspicious activity (e.g., multiple faces detected). """
    suspicious, reason = monitor.check_activity()
    return jsonify({"suspicious": suspicious, "reason": reason})


@app.route("/report")
def report():
    """ View suspicious activity report. """
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("report.html", username=session["user"], exam_name="Math Exam", suspicious_logs=monitor.get_logs())


if _name_ == "_main_":
    app.run(debug=True) 
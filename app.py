from flask import Flask, render_template, redirect, request, url_for, session
from io import BytesIO
from flask_socketio import SocketIO, emit
from scripts.emotion_reader import predict_with_model
from scripts.conversational_chatbot import chat_with_model
from datetime import timedelta
import matplotlib.pyplot as plt

uploaded_image = None
app = Flask(__name__)
app.secret_key = "very-secret-key"
socketio = SocketIO(app, cors_allowed_origins="*")
@app.route("/", methods=["POST", "GET"])
@app.route("/upload_image", methods=["POST", "GET"])

def upload_image():
    if request.method == "POST":
        global uploaded_image
        if 'image' not in request.files:
            return 'No file part', print(request.files)

        file = request.files['image']

        if file.filename == '':
            return 'No selected file'

        if file:
            img_bytes = file.read()
            uploaded_image = plt.imread(BytesIO(img_bytes), format=".jpg")

            emotion = predict_with_model(uploaded_image)

            app.permanent_session_lifetime = timedelta(hours=2)
            session.permanent = True
            session["emotion"] = emotion
            session["greeted"] = False

            return redirect(url_for("chat"))

    else:
        return render_template("upload_image.html")

@app.route("/chat")
def chat():
    if "emotion" not in session:
        return redirect(url_for("upload_image"))
    return render_template("chat_page.html", emotion=session["emotion"])

@socketio.on("connect")
def handle_connect():
    if session.get("greeted"):
        return

    session["greeted"] = True
    emotion = session.get("emotion", "neutral")

    opening_message = chat_with_model(user_message=None, emotion=emotion)

    emit("ai_message", {"message": opening_message})

@socketio.on("user_message")
def handle_user_message(data):
    user_text = data["message"]
    emotion = session.get("emotion", "neutral")

    ai_reply = chat_with_model(user_message=user_text, emotion=emotion)

    emit("ai_message", {"message": ai_reply})

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

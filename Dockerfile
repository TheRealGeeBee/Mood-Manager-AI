FROM python:3.13

COPY /model Mood-Manager-AI/model
COPY /scripts Mood-Manager-AI/scripts
COPY /templates Mood-Manager-AI/templates
COPY /static Mood-Manager-AI/static
COPY /requirements.txt Mood-Manager-AI/requirements.txt
COPY /LICENSE /LICENSE
COPY /README.md /Mood-Manager-AI/README.md
COPY /app.py /Mood-Manager-AI/app.py

RUN pip install -r /Mood-Manager-AI/requirements.txt

ENTRYPOINT ["python", "app.py"]
CMD ["--port", "5000"]
FROM python:3.11

COPY requirements.txt /

RUN pip3 install --upgrade pip

RUN pip3 install -r /requirements.txt



COPY . /apis

WORKDIR /apis



EXPOSE 8080
# docker build -t pxio-backend:1.0.0 .
# docker run -it --rm -p 8080:8080 hello-flask:1.0.0
# OR
# docker run -dp 127.0.0.1:3000:3000 getting-started
# tutorial: https://developers.redhat.com/articles/2023/08/17/how-deploy-flask-application-python-gunicorn#containerization
# https://docs.docker.com/get-started/02_our_app/




CMD ["gunicorn","--config", "gunicorn_config.py", "apis:app", "--log-file", "-"]
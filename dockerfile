FROM alpine:latest
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
# RUN pip install --upgrade pip
WORKDIR /app
RUN python3 -m venv /app/venv --system-site-packages
RUN . /app/venv/bin/activate
COPY schema.sql app.py requirements.txt /app/
RUN /app/venv/bin/pip3 --no-cache-dir install -r requirements.txt
CMD ["/app/venv/bin/python3", "app.py"]
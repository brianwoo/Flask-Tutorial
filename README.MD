# How to Make a Web API Using Flask in Python 3
https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3


# Docker build
docker build -t flask-app .

# Docker run
docker run -p5000:5000 --name flask-app -v .\db:/app/db flask-app



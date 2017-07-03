sudo apt-get install docker.io -y
git clone https://github.com/UCL-CloudLabs/Docker-sample.git
cd Docker-sample
sudo docker build -t hello-flask .
sudo docker run -p 5000:5000 hello-flask

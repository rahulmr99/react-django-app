Rooftop 
=======
Project Explanation


## Installation

1. create docker image by going into the folder which contains docker-compose.yml and type

```bash
docker-compose build
```

2. run the docker image by

```bash
docker-compose up
```
or 
```bash
docker-compose up -d 
```

to run as daemon

3. see the docker running process by going into a new terminal and typeing

```bash
docker ps
```
or 
```bash
docker ps -a
```

4. migrate the tables by going into the container and perform migrations

```bash
docker exec -it CONTAINER_ID sh
```

```bash
python manage.py migrate
```

4. click the link of the docker from the terminal or got from "docker ps" command her its

```bash
http://0.0.0.0:8000/
```

5. for front end you can access the react page via link for network provided after running the "docker-compose up" command for example

```bash
http://172.29.0.2:3000
```

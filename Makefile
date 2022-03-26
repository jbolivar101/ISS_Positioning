#NAME ?= jbolivar

all: build run push

images:
	docker images | grep jbolivar101

ps:
	docker ps -a | grep jbolivar101

build:
	docker build -t jbolivar101/ISS_Docker:ISS_Positioning .

run:
	docker run --name "ISS_Docker" -d -p 5004:5000 jbolivar101/ISS_Docker:ISS_Positioning

push:
	docker push jbolivar101/ISS_Docker:ISS_Positioning

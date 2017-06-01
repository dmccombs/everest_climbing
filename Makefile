DIR=$(shell pwd)
IMAGE_NAME=strava-climb

build:
	docker build -t $(IMAGE_NAME) -f Dockerfile .

up: build
	docker run -d -v $(DIR):/docker --name $(IMAGE_NAME) -it $(IMAGE_NAME)

shell:
	docker exec -it $(IMAGE_NAME) /bin/bash

clean:
	-docker stop $(IMAGE_NAME)
	-docker rm $(IMAGE_NAME)
	-docker rmi $(IMAGE_NAME)

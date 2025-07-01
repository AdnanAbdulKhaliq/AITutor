DB_CONTAINER_NAME=english-tutor-db
DB_IMAGE_NAME=english-tutor-db-image

include app.env
export

.PHONY: build run start stop logs clean

build:
	docker build -t $(DB_IMAGE_NAME) -f Dockerfile .

run:
	docker run --name $(DB_CONTAINER_NAME) \
		-e POSTGRES_USER=$(DB_USER) \
		-e POSTGRES_PASSWORD=$(DB_PASSWORD) \
		-e POSTGRES_DB=$(DB_NAME) \
		-p 5432:5432 -d $(DB_IMAGE_NAME)

start:
	docker start $(DB_CONTAINER_NAME)

stop:
	docker stop $(DB_CONTAINER_NAME)

logs:
	docker logs $(DB_CONTAINER_NAME)

clean:
	docker rm $(DB_CONTAINER_NAME)
	docker rmi $(DB_IMAGE_NAME)

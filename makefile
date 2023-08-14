VERSION := $(shell git log --pretty=format:'' | wc -l)

build:
	docker build -t freegpt:$(VERSION) . -f ./Dockerfile

run:
	docker-compose up --build

stop:
	docker compose --file 'docker-compose.yml' --project-name 'freegpt' stop

clean: stop
	docker compose --file 'docker-compose.yml' --project-name 'freegpt' down

status:
	@if docker images | grep -q freegpt; then \
        echo "Freegpt Builded"; \
	else \
		echo "No Image Builded"; \
    fi
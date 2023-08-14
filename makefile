VERSION := $(shell git log --pretty=format:'' | wc -l)

build:
	docker build -t free_gpt:$(VERSION) . -f ./Dockerfile

run:
	docker-compose up --build

stop:
	docker compose --file 'docker-compose.yml' --project-name 'free_gpt' stop

clean: stop
	docker compose --file 'docker-compose.yml' --project-name 'free_gpt' down

status:
	@if docker images | grep -q free_gpt; then \
        echo "Free_gpt Builded"; \
	else \
		echo "No Image Builded"; \
    fi
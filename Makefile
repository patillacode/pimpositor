install: python-install
full-reset: repo-pull docker-reset

python-install:
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt && \

serve:
	. venv/bin/activate && \
	FLASK_APP=flaskr FLASK_ENV=development \
	APP_SETTINGS=flaskr.config.DevelopmentConfig \
	flask run

docker-reset:
	echo "Stopping container..." && \
	docker stop pimpositor || true && \
	echo "Deleting container..." && \
	docker rm pimpositor || true && \
	echo "Deleting image..." && \
	docker rmi pimpositor || true && \
	echo "Rebuilding image..." && \
	docker build --tag pimpositor . && \
	echo "Running new image in new container..." && \
	docker run -d --name pimpositor --publish 5053:5053 pimpositor && \
	echo "Set restart on failure..." && \
	docker update --restart=on-failure pimpositor

repo-pull:
	git pull origin master

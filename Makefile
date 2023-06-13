token ?= bark_token
datasource ?= qq

init-pre-commit:
	git config --global url."https://".insteadOf git://
	pre-commit install
	pre-commit run --all-files

update-pre-commit:
	pre-commit autoupdate

test:
	pytest --cov -s ./tests
	coverage html

server:
	python -m magpie server -r ./rules.json

check:
	python -m magpie check -r ./rules.json -d $(datasource) --bark-token $(token)

build-docker-image:
	docker build -f Dockerfile -t magpie:latest .

docker-run-server:
	docker run --rm \
 		-v `pwd`/rules.json:/app/rules.json \
		-p 8000:8000 magpie:latest \
		python -m magpie server -r ./rules.json

docker-check:
	docker run --rm \
 		-v `pwd`/rules.json:/app/rules.json \
		magpie:latest \
		python -m magpie check -r ./rules.json -d $(datasource) --bark-token $(token)

.PHONY: install

PIP_INDEX = https://mirrors.aliyun.com/pypi/simple/

# install local dependencies
install:
	pip install --upgrade --index-url ${PIP_INDEX} pip
	pip install --upgrade --index-url ${PIP_INDEX} -r requirements/local.txt

# initialize project develop environment
pyenv:
	pyenv virtualenv 3.8.2 {{cookiecutter.project_name}}
	# activate virtualenv -> install deps -> add project root path to import path
	pyenv local tmp; \
	eval "$$(pyenv init -)"; \
	pyenv activate; \
	make install; \
	echo $$(pwd) >>  "$$(find $$VIRTUAL_ENV -name 'site-packages')/_venv_.pth"

# make this project online
online:
	docker-compose up -d --remove-orphans
	docker-compose ps

# prepare: npm install gql-generator -g
# generate graphql query sample for tests, see `tests/conftest.py`
# Notice: these test resource files will not and should not be committed to VCS
gen-graphql-query:
	rm -rf ./tests/unit_tests/resource/schema
	mkdir -p ./tests/unit_tests/resource/schema
	gqlg --schemaFilePath ./schema.graphql --destDirPath ./tests/unit_tests/resource/schema

# test all tests
test: gen-graphql-query
	pytest -v --cov=app --cov-report term-missing -c setup.cfg --alluredir=./dist/allure tests

# show test report
test-report: test
	# prepare install allure by `brew install allure` in macOS
	allure serve ./dist/allure

# build docker image
docker-build:
	docker build -t dcr.teletraan.io/{{cookiecutter.project_name}}/backend:dev-latest .

# push docker image to private hub
docker-push:
	docker push dcr.teletraan.io/{{cookiecutter.project_name}}/backend:dev-latest

history:
	alembic history

migrations-%:
	alembic revision --autogenerate -m "$*"

downdb-%:
	alembic downgrade $*

migrate:
	alembic upgrade head

cleardb:
	alembic downgrade base


db.rebuild:
	rm -rf migrations
	dropdb mdc_inspectors
	createdb mdc_inspectors
	make db.init

db.init:
	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade

deploy:
	git push heroku master

load_from_socrata:
	python ./inspectors/scripts/pull_inspection_data.py

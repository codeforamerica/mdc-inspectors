
db.rebuild:
	rm -rf migrations
	dropdb mdc_inspectors
	createdb mdc_inspectors
	make db.init

db.init:
	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade

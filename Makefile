
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

add_fake_users:
	python ./inspectors/scripts/add_fake_users.py

add_fake_inspections:
	python ./inspectors/scripts/add_fake_inspections.py

fake_data:
	make add_fake_inspections
	make add_fake_users

request_feedback:
	python ./inspectors/scripts/send_requests_for_feedback.py

create_test_db:
	createdb mdc_inspectors_test

destroy_test_db:
	dropdb mdc_inspectors_test

test:
	export CONFIG='inspectors.settings.TestConfig'
	nosetests \
		--verbose \
		--nocapture \
		--with-coverage \
		--cover-package=./inspectors \
		--cover-erase

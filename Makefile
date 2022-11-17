install:
	pip install -r requirements.txt

generate-listings-outcode-csv-file:
	 python manage.py generate_outcode_listings

run:
	python manage.py runserver

build:
	docker build -t pass-the-keys .

run-docker:
	docker run -p 8000:8000 pass-the-keys

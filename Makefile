reqi = requirements.in requirements-dev.in
reqo = $(reqi:.in=.txt)

all: start

start:
	@docker-compose up

restart:
	@docker-compose exec hue kill -HUP 1

%.txt: %.in $(REQ)
	@pip-compile --output-file=$@ $<

requirements: $(reqo)

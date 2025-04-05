
IMAGE=lelem:1
CONT=lelem

DOCKER_RUN_ARGS=--name $(CONT) -it --rm -v $(PWD):/x -w /x

ifeq ($(DIAG),1)
DOCKER_RUN_ARGS += -d
endif

ifneq ($(DEVKA),)
DOCKER_RUN_ARGS += -v /v:/v
endif

build:
	@docker buildx build --build-context classico=./classico -t $(IMAGE) .

run:
	@docker run $(DOCKER_RUN_ARGS) $(IMAGE)

ps:
	@docker ps

stop:
	@docker stop $(CONT)

sh:
	@docker exec -it $(CONT) bash -l

install:
	@uv pip install -e .

uninstall:
	@uv pip uninstall lelem

clean:
	@rm -rf lelem.egg-info

mypy:
	@mypy lelem/


IMAGE=llm-actor:1
CONT=llm-actor

# GPT=comp|resp
# GEM
# ANT
# DEEP
# LC langchain
# OPEN openai completions API, can handle GEM, DEEP

build:
	@docker buildx build --build-context classico=/v/classico/classico -t $(IMAGE) .

run:
ifeq ($(DIAG),1)
	@docker run --name $(CONT) -it --rm -v /v:/v $(IMAGE)
else
	@docker run -d --name $(CONT) -it --rm -v /v:/v $(IMAGE)
endif

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

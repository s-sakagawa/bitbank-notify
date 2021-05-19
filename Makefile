IMAGE_NAME := bitbank-notify
CONTAINER_NAME := bitbank-notify

.PHONY: build
build:
		@docker build . -t $(IMAGE_NAME)

.PHONY: run
run:
		@docker run --rm -it --name $(CONTAINER_NAME) $(IMAGE_NAME) $(ARGS)

.PHONY: bash
bash: ARGS=bash
export ARGS
bash:
		@$(MAKE) run

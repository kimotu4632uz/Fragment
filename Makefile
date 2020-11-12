TODO := \
"run,die" \
"run,kill"


comma := ,
status = $(word 2,$(subst $(comma), ,$1))

define inst
hello
world!
endef

.PHONY: install
install: ## install files
    @echo $1

.PHONY: uninstall
uninstall: ## delete files
    @rm -rf /tmp

.PHONY: help
help:
    @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

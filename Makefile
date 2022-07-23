help:
	@echo "====================="
	@echo "Krux Installer Tasks"
	@echo "====================="
	@echo ""
	@echo "help: show this message"
	@echo "build: builds a docker container"
	@echo "run/<os>: runs a docker image to build app. <os> can be 'linux', 'mac' or 'win'"

cache/create:
	@touch yarn.lock
	@if [ ! -f .yarn-cache.tgz ]; \
	then \
		echo "==> Init empty .yarn-cache.tgz" && tar cvzf .yarn-cache.tgz --files-from /dev/null; \
	fi

build/installer:
	@docker-compose build installer

cache/copy:
	@docker-compose run installer cat /tmp/yarn.lock > /tmp/yarn.lock

cache/diff:
	@if !diff -q yarn.lock /tmp/yarn.lock > /dev/null 2>&1; \
	then \
		echo "==> Saving yarn cache" \
		docker-compose run installer tar czf - /app/.yarn-cache > .yarn-cache.tgz \
		echo "==> Saving yarn.lock" \
		cp /tmp/yarn.lock yarn.lock; \
	fi

docker/build: cache/create build/installer cache/copy cache/diff

build/linux:
	@docker-compose run installer yarn run electron:build --linux

build/mac:
	@docker-compose run installer yarn run electron:build --mac

build/windows:
	# @docker-compose run installer Xvfb :0 -screen 0 1024x768x16
	@docker-compose run installer yarn run electron:build --win

install:
	@yarn install

all: install docker/build build/linux build/win build/mac

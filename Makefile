help:
	@echo "====================="
	@echo "Krux Installer Tasks"
	@echo "====================="
	@echo ""
	@echo "help: show this message"
	@echo "build: builds a docker container"
	@echo "run/<os>: runs a docker image to build app. <os> can be 'linux', 'mac' or 'win'"


docker/cache/create:
	@touch yarn.lock
	@if [ ! -f .yarn-cache.tgz ]; \
	then \
		echo "==> Init empty .yarn-cache.tgz" && tar cvzf .yarn-cache.tgz --files-from /dev/null; \
	fi

docker/cache/copy:
	@echo "==> Copying container /tmp/yarn.lock to host /tmp/yarn.lock"
	@docker-compose run installer cat /tmp/yarn.lock > /tmp/yarn.lock

docker/cache/diff:
	@echo "==> Checking diff between yarn.lock and /tmp/yarn.lock"
	@if !diff -q yarn.lock /tmp/yarn.lock > /dev/null 2>&1; \
	then \
		echo "==> Saving container /app/.yarn-cache to host .yarn-cache.tgz" \
		docker-compose run installer tar czf - /app/.yarn-cache > .yarn-cache.tgz \
		echo "==> Saving /tmp/yarn.lock to yarn.lock" \
		cp /tmp/yarn.lock yarn.lock; \
	fi

docker/build/%:
	@$(MAKE) docker/cache/create
	@docker-compose build --remove-orphans installer
	@$(MAKE) docker/cache/copy
	@$(MAKE) docker/cache/diff
	@docker-compose run installer yarn run electron:build --$(echo $@ | cut -d/ -f3)

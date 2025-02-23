l-build:
	docker compose -f  local.yaml up --build 

l-up:
	docker compose -f local.yaml up 

l-stop:
	docker compose -f local.yml stop

l-down:
	docker compose -f local.yaml down

l-logs:
	docker compose -f local.yaml logs

web-shell:
	docker exec -it web bash
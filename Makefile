.PHONY: up down logs test chaos-test clean

up:
	docker-compose -f docker-compose.yml up -d --build

down:
	docker-compose -f docker-compose.yml down

logs:
	docker-compose -f docker-compose.yml logs -f

test:
	docker-compose -f docker-compose.yml exec backend pytest
	docker-compose -f docker-compose.yml exec frontend npm test

test-frontend:
    docker-compose -f docker-compose.yml exec frontend npm test

chaos-test:
	@echo "Starting Chaos Test: Killing Redis..."
	docker-compose -f docker-compose.yml kill redis
	@echo "Waiting for recovery..."
	sleep 5
	docker-compose -f docker-compose.yml start redis
	@echo "Redis restarted. Check logs for recovery."

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

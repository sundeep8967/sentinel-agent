.PHONY: test run clean

test:
	pytest demo_repo/test_metrics_engine.py

run:
	python3 app/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

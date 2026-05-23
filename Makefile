.PHONY: test lint

# Run the full test suite (including coverage)
# uv will ensure the correct interpreter & env are used

test:
	uv run pytest --cov=moodlog --cov-report=term-missing

# Lint the codebase with ruff (check only)
lint:
	uv run ruff check .

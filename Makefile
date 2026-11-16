# Common student commands. Edit when commands change; copy for a small Python app.
.PHONY: install run test
install:
	uv sync --locked
	uv run playwright install chromium

run:
	uv run python main.py

test:
	uv run pytest -q

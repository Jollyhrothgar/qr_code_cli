.PHONY: install uninstall dev clean

install:
	uv tool install -e . --force

uninstall:
	uv tool uninstall qr-create

dev:
	uv sync

clean:
	rm -rf .venv __pycache__ *.egg-info

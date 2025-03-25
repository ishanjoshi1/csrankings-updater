# Running the Executable
Download the latest executable from Releases and run it from a terminal. For example, if you downloaded the executable to your desktop, do the following:
```
cd path/to/desktop
./main
```

# Contributing

## Getting Started
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't.
- Make sure tkinter works on your machine. On MacOS, you might have to install ```python-tk``` from homebrew. Check if any similar issue exists for your OS.
- Run ```uv sync``` to install dependencies.

## Running the Code
Run ```uv run main.py```.

## Before Committing Code
Run ```uv run ruff format``` and ```uv run ruff check --fix``` and fix the errors. If any linting rule doesn't make sense, please let me know and we can talk about it.

## Building an Executable
Run ```uv run pyinstaller --onefile --windowed main.py```. The executable should be in the dist folder.

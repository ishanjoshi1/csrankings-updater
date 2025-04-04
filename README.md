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

## Instructions
1. Fork the repository with all the default options. Instructions to fork can be found [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo?tool=webui#forking-a-repository). If a fork on your account already exists, delete that and re-fork.

1. Clone the forked repository in this folder. To do this, run the following command from the root folder of this project (csrankings-updater). Replace YOUR_GITHUB_USERNAME with your github username in the command.
    ```
    git clone --depth 1 https://github.com/YOUR_GITHUB_USERNAME/CSrankings
    ```
    You should now have a ```CSRankings``` folder in your root directory.

1. Run ```./dist/main```, add the data and check faculty to be added/deleted, and press done. This should update the required files locally

1. Run the following command to add and commit changes to your fork
    ```
    git -C CSRankings add . && git -C CSRankings commit -m "Modified faculty" && git -C CSRankings push
    ```

1. Double-Check everything and only then Create a Pull Request (PR)

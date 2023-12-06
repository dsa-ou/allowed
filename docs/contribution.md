# Contributing to `allowed`

Welcome to `allowed`! We appreciate your interest in contributing. Whether you're a seasoned developer or just getting started, we encourage and value all contributions.

If you're new to `git`, `GitHub` or version control in general, consider reading some of the introductory materials listed under [Additional Resources](#additional-resources) at the bottom of this guide.

## Getting Started

### 1. Fork the Repository

A "fork" is a copy of a repository that allows you to freely experiment with changes without affecting the original project. To create a fork, you'll need a GitHub account.

On the GitHub page for the `allowed` repository, click on the "Fork" button at the top right. This creates a personal copy of the project under your GitHub account. You'll be able to make changes to this copy and propose them to the original project using a "pull request" (we'll get to that later).

### 2. Clone Your Fork

"Cloning" is the process of downloading a copy of your fork (the one on GitHub) to your local machine. This allows you to work on the project using your favorite code editor and test your changes before proposing them to the original project.

To clone your fork, you'll need to have Git installed on your computer. If you don't have Git installed, you can download it from the [official Git website](https://git-scm.com/downloads).

Once you have Git installed, open a terminal (Command Prompt on Windows, Terminal app on macOS, or your preferred terminal in Linux), and run the following commands:

```bash
git clone https://github.com/your-username/allowed.git
cd allowed
```
> Replace `your-username` with your GitHub username.

## Setting Up Python and Poetry

### 1. Install Python

To contribute to `allowed`, you'll need Python version 3.10 or above. If you're not sure which version of Python you have, you can check by opening a terminal and running the following command:

```bash
python3 --version
```

This command should print the version of Python that's currently installed. If you see a version number that's 3.10 or above, you're good to go! If not, or if you see an error message saying that `python3` is not recognized as a command, you'll need to install Python.

> You can download Python from the [official Python website](https://www.python.org/downloads/). Make sure to download Python 3.10 or above.

### 2. Install Poetry

Poetry is a tool for managing Python project dependencies. It makes it easy to install, update, and remove the libraries that your project uses. It also helps to ensure that your project works the same way on all developers' machines, which makes collaboration easier.

The recommended way to install Poetry is with the [official installer](https://python-poetry.org/docs/#installing-with-the-official-installer). You can do this with the following commands:

#### Linux, MacOS, WSL:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

> This command downloads the Poetry installer script and runs it with Python.

#### Windows:

```Powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

> This command does the same thing, but uses PowerShell syntax, which is the default command-line interface on Windows.

### 3. Install Dependencies

Now that you have Python and Poetry installed, you can install the dependencies for the `allowed` project. "Dependencies" are other Python libraries that `allowed` uses to provide its features.

Navigate to the `allowed` project directory in your terminal (you should already be there if you followed the previous steps) and run the following command:

```bash
poetry install
```

This command tells Poetry to install the dependencies listed in the `pyproject.toml` file - a file that describes the project and the additional libraries it relies on.

### 4. Activate the Environment

Finally, you can activate your Poetry virtual environment. A "virtual environment" is a self-contained environment that has its own set of installed libraries, separate from other projects. This helps to prevent conflicts between different projects' dependencies.

You can activate the virtual environment with the following command:

```bash
poetry shell
```

This command starts a new shell (a command-line interface) that's configured to use the `allowed` project's virtual environment. Any Python commands you run in this shell will use the `allowed` project's dependencies.

## Makefile Commands
If you're using a Linux or WSL environment, you can make use of the following `make` commands:

- `make install`: Installs project dependencies.
- `make update`: Updates project dependencies to their latest compatible versions.
- `make fmt`: Formats your code in accordance to the project's style conventions.
- `make lint`: Checks your code for errors.
- `make test`: Runs all the project's tests.

If you're using Windows then you will need to run each tool individually. You can view all the commands inside the `Makefile`.

## Making Contributions

### 1. Create a New Branch for Your Changes

In Git, a "branch" is like a parallel version of the codebase. It allows you to work on your changes without affecting the main codebase until you're ready to merge your changes.

To create a new branch, use the following command:

```bash
git checkout -b feature-or-fix-branch
```
>Replace `feature-or-fix-branch` with a descriptive name for your branch. This name should briefly describe the feature you're adding or the issue you're fixing.

Now you're ready to start making changes to the code!

### 2. Stage and Commit Your Changes
Once you've made your changes, you'll need to "stage" and "commit" them. Staging is the process of selecting specific changes that you want to commit. A "commit" is like a snapshot of your code at a specific point in time.

To stage all your changes, use the following command:
```bash
git add .
```
>This command stages all changes in the current directory and its subdirectories.

Next, commit your changes with the following command:
```bash
git commit -m "Your descriptive commit message"
```
>Replace `"Your descriptive commit message"` with a brief description of the changes you've made. This message should help other developers understand what you did and why.

### 3. Push Your Changes to Your Fork
Now that your changes are committed, you can "push" them to your fork on GitHub. Pushing is the process of uploading your local commits to a remote repository.

To push your changes, use the following command:
```bash
git push origin feature-or-fix-branch
```
>Replace `feature-or-fix-branch` with the name of your branch. This command pushes your changes to your fork on GitHub.

### 4. Create a Pull Request
A "pull request" is a proposal to merge your changes into the main codebase. It allows other developers to review your changes and provide feedback before the changes are merged.

To create a pull request, go to the GitHub page for your fork, switch to the branch that you just pushed, and click on the "New Pull Request" button.

### 5. Engage in Discussions
After you've created a pull request, other developers might ask questions or provide feedback about your changes. Be sure to respond to these comments and address any feedback they provide. This collaborative process is a key part of open source development, and it helps to ensure that all changes are beneficial and free of bug

## Additional Resources

- [Introduction to git and Version Control](https://docs.github.com/en/get-started/using-git/about-git): A comprehensive guide to understanding Git.
- [GitHub Hello World Guide](https://docs.github.com/en/get-started/quickstart/hello-world): A beginner-friendly guide to using GitHub.
- [Poetry Documentation](https://python-poetry.org/): Learn more about Poetry and its features.

## Thank You
Remember, every contribution is valuable, no matter how small. Feel free to reach out if you have any questions or need assistance.
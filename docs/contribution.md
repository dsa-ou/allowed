# Code contributions

This guide will walk you through the process of setting up your development environment and contributing code to the `allowed` project. If you prefer not to use the command line, you can also use [GitHub Desktop](https://desktop.github.com/) to perform many of the steps described below.

If you're new to `Git`, `GitHub` or version control in general, consider reading some of the introductory materials listed under [Additional Resources](#additional-resources) at the bottom of this guide. Mastering these tools will put you at a great advantage when applying for jobs in the software industry, or when working on your own projects.

### A note to Windows users

If you're using Windows, you'll need to install the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) (WSL) to run the commands in this guide. WSL is a compatibility layer that allows you to run Linux programs on Windows. It's required because the `allowed` project uses some Linux-specific tools.

## Getting Started

### 1. Fork the Repository

> :bulb: A "fork" is a copy of a repository that allows you to freely experiment with changes without affecting the original project.
> To create a fork, you'll need a [GitHub account](https://docs.github.com/en/get-started/quickstart/creating-an-account-on-github).

On the GitHub page for the `allowed` repository, click on the "Fork" button at the top right. This creates a personal copy of the project under your GitHub account. You'll be able to make changes to this copy and propose them to the original project using a "pull request" (we'll get to that later).

### 2. Clone Your Fork

> :bulb: "Cloning" is the process of downloading a copy of your fork (the one on GitHub) to your local machine. This allows you to work on the project using your favorite code editor and test your changes before proposing them to the original project.

To clone your fork, you'll need to have Git installed on your computer. If you don't have Git installed, you can download it from the [official Git website](https://git-scm.com/downloads).

Once you have Git installed, open a terminal (Terminal app on macOS, or your preferred terminal in Linux/WSL), and run the following commands in the directory where you want to store the project:

```bash
git clone https://github.com/your-username/allowed.git
cd allowed
```
> :bulb: Replace `your-username` with your GitHub username.

## Setting Up Python and Poetry

### 1. Install Python

To contribute to `allowed`, you'll need Python version 3.10. If you're not sure which version of Python you have, you can check by opening a terminal and running the following command:

```bash
python3 --version
```

This command should print the version of Python that's currently installed. If it's 3.10, you're good to go! If not, or if you see an error message saying that `python3` is not recognized as a command, you'll need to install Python.

> :bulb: You can download Python from the [official Python website](https://www.python.org/downloads/). Make sure to download Python 3.10.

### 2. Install Poetry

> :bulb: [Poetry](https://python-poetry.org/) is a tool for managing Python project dependencies. It makes it easy to install, update, and remove the libraries that your project uses. It also helps to ensure that your project works the same way on all developers' machines, which makes collaboration easier.

The recommended way to install Poetry is with the [official installer](https://python-poetry.org/docs/#installing-with-the-official-installer). You can use the following command to download the Poetry installer script and run it with Python:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

If you get an error message about an invalid certificate, you need to run the
'Install Certificates' command in the Python folder.

Finally, you need to add `export PATH="$HOME/.local/bin:$PATH"` to your shell
startup file, which is in your home directory and is called `.zshrc`, `.bashrc` or similar.
Type `echo $0` in the terminal to find out which shell you're using.

### 3. Install Dependencies
> :bulb: "Dependencies" are other Python libraries that `allowed` uses to provide its features.

Now that you have Python and Poetry installed, you can install the dependencies for the `allowed` project.

Navigate to the `allowed` project directory in your terminal (you should already be there if you followed the previous steps) and run the following command:

```bash
make install
```

> :bulb: This command tells Poetry to install the dependencies listed in [`pyproject.toml`](https://python-poetry.org/docs/pyproject/). This is a file that describes the project and the additional libraries it relies on.

That's it! You're all set up! :tada:

Have a cup of tea and a biscuit, you've earned it! :cookie: :tea:

## Making Contributions

### 1. Find an Issue to Work On

> :bulb: An "issue" is a task that needs to be completed to improve the project. Issues can be bugs that need to be fixed, features that need to be added, or improvements to the project's documentation.

To find an issue to work on, go to the [project's issue tracker](https://github.com/dsa-ou/allowed/issues). Here you'll find a list of all the issues that have been reported by other collaborators. You can also add your own issues if you find a bug or have an idea for a new feature.

Let everyone else know that you're working on an issue by leaving a comment on the issue page. This will help to avoid duplicate work and ensure that everyone is working together. Don't be afraid to ask questions about the issue here if you're not sure how to proceed.

> :bulb: If you're a beginner, you might want to start with an issue that's labelled "good first issue". These issues are designed to be beginner-friendly and are a great way to get started.

### 2. Create a New Branch for Your Changes

> :bulb: In Git, a "branch" is like a parallel version of the codebase. It allows you to work on your changes without affecting the main codebase until you're ready to merge your changes.

Before you start making changes, you'll need to create a new branch for your work. To do this, run the following command in your terminal:

```bash
git checkout -b feature-or-fix-branch
```
> :bulb: Replace `feature-or-fix-branch` with a descriptive name for your branch. This name should briefly describe the feature you're adding or the issue you're fixing.

Now you're ready to start making changes to the code!

> :bulb: It's a good idea to make small, incremental changes and commit them often. This will make it easier to review your changes and revert them if necessary.

### 3. Test Your Changes

Before sharing your new features or fixes, it's important to check that you haven't broken anything! Your environment provides a few short commands that will help you to check your work and ensure you're following the project's style conventions.

```bash
make format
```
> This command formats your code in accordance with the project's style conventions.

```bash
make lint
```
> This command checks your code for errors.

```bash
make run_tests
```
> This command runs some tests within the created Poetry environment
> and other tests in the current environment. The latter will only pass if
> your environment has Python 3.10 to 3.12 installed but _not_ IPython or pytype.

If you have a virtual environment with a specific version of Python and pytype
you want to test, activate that environment and then type
```bash
tests/tests.sh run
```
> This executes the same tests as for the Poetry environment, but runs them
> in the current environment instead.

Be sure to resolve any errors that arise before moving on to the next step.

### 4. Stage and Commit Your Changes
> :bulb: "Staging" is the process of selecting specific changes that you want to commit. A "commit" is like a snapshot of your code at a specific point in time. It allows you to save your changes and add a descriptive message that explains what you've done.

Once you've made your changes, you'll need to stage and commit them.

To stage all your changes, use the following command:
```bash
git add .
```
> :bulb: This command stages all changes in the current directory and its subdirectories. You can see which files have been staged by running `git status`.

Next, commit your changes:
```bash
git commit -m "Your descriptive commit message"
```
> :bulb: Replace `"Your descriptive commit message"` with a brief description of the changes you've made. This message should help other developers understand what you did and why.

### 5. Push Your Changes to Your Fork

> :bulb: "Pushing" is the process of uploading your local commits to a remote repository (in this case, your fork on GitHub).

Now that your changes are committed, you can push them to your fork on GitHub.

To push your changes, use the following command:
```bash
git push origin feature-or-fix-branch
```
> :bulb: Replace `feature-or-fix-branch` with the name of your branch. This command pushes your changes to your fork on GitHub.

### 6. Create a Pull Request
> :bulb: A "pull request" is a proposal to merge your changes into the main codebase. It allows other developers to review your changes and provide feedback before the changes are merged.

To create a pull request, go to the GitHub page for your fork, switch to the branch that you just pushed via the "branch" dropdown menu, and click on the "New Pull Request" button. This will take you to a page where you can review your changes and create a pull request.

### 7. Engage in Discussions
After you've created a pull request, other developers might ask questions or provide feedback about your changes. Be sure to respond to these comments and address any feedback they provide. This collaborative process is a key part of open source development, and it helps to ensure that all changes are beneficial and free of bugs.

## Makefile Command Reference
When working with the `allowed` environment, you can make use of the following `make` commands to quickly perform common tasks:

- `make install`: Installs project dependencies.
- `make update`: Updates project dependencies to their latest compatible versions.
- `make format`: Formats your code in accordance with the project's style conventions.
- `make lint`: Checks your code for errors.
- `make run_tests`: Runs all the project's tests and checks against the expected outputs.
- `make create_tests`: Runs tests  and stores outputs.

After changing the behaviour or messages of `allowed`,
do `make run_tests` to check that the outputs have changed as expected,
then do `make create_tests` so that the new outputs are saved for future runs.
The new outputs must be committed with the changes to `allowed`.

## Additional Resources

- [Creating a GitHub Account](https://docs.github.com/en/get-started/quickstart/creating-an-account-on-github): A step-by-step guide to creating a GitHub account.
- [GitHub Hello World Guide](https://docs.github.com/en/get-started/quickstart/hello-world): A beginner-friendly guide to using GitHub.
- [Introduction to git and Version Control](https://docs.github.com/en/get-started/using-git/about-git): A comprehensive guide to understanding Git.
- [Setting up Git](https://docs.github.com/en/get-started/quickstart/set-up-git): A guide to installing and configuring Git.

## Thank You

If this all feels a bit too overwhelming, don't worry! There is more to a project than just code.
You can contribute in [other ways](../README.md).

Feel free to reach out on the project's [discussion forum](https://github.com/dsa-ou/allowed/discussions) if you have any questions or need help getting started. M269 students may prefer to post to the module's 'Technical Forum' for further guidance.

Thank you for your interest in contributing to `allowed`! :heart:
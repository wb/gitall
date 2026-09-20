# GitAll

Run one command across the Git repositories directly beneath a directory.

GitAll is intentionally small: it discovers repositories, runs the requested
command in stable name order, and reports any failures. It has no dependencies
beyond Python 3.9 or newer and Git.

## Usage

Run a Git command in every repository beneath the current directory:

```console
$ gitall status --short
alpha
beta
```

Arguments are passed to Git exactly as provided, including spaces and shell
metacharacters:

```console
$ gitall commit -m "Document the release"
```

Select or exclude repositories:

```console
$ gitall --include api,website status
$ gitall --exclude archived,prototype fetch --prune
$ gitall --include-from repositories.txt status
```

`--include-from` accepts one repository path per line. Explicit paths are
resolved relative to the directory where GitAll starts and may not be absolute,
traverse through `..`, or resolve through a symlink to somewhere outside that
directory.

Run a non-Git command with `--raw`:

```console
$ gitall --raw python3 -m unittest
```

Raw commands are executed directly, without an implicit shell. If shell syntax
is genuinely required, invoke a shell explicitly:

```console
$ gitall --raw sh -c 'git branch --show-current | sed "s/^/branch: /"'
```

Check out the latest commit on a branch before a given date:

```console
$ gitall --date 2024-01-01 checkout main
```

This leaves each repository in a detached-HEAD state at the selected commit.

Run `gitall --help` for all options.

## Output and failures

Repositories are processed alphabetically. GitAll continues after an individual
command fails, prints a summary of failed repositories, and exits with status 1
if any command failed.

Use `--quiet` repeatedly to reduce GitAll's headings and separators, or
`--verbose` to show the command and starting directory. Set `NO_COLOR` to disable
GitAll's own terminal colors.

## Installation

Clone the repository, then link the executable into a user-owned directory on
your `PATH`:

```sh
git clone https://github.com/wb/gitall.git
mkdir -p ~/.local/bin
ln -s "$(pwd)/gitall/gitall" ~/.local/bin/gitall
```

Alternatively, copy the `gitall` file anywhere on your `PATH`. It must remain
executable.

## Safety

GitAll can run destructive Git or system commands across many repositories.
It does not ask for confirmation, so review the command and selected repositories
before running it.
Shell interpretation occurs only when you explicitly invoke a shell.

## Development

Run the dependency-free test suite with:

```sh
python3 -m unittest discover -s tests -v
```

## License

GitAll is available under the [MIT License](LICENSE).

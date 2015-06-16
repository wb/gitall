#GitAll

Easily run git commands across all your repositories.

##How to use GitAll

    usage: gitall [-h] [-I includefile] [-i include] [-e exclude] [-d date] [-n]
                  [-q] [-v] [-r]
                  ...

    Perform a git operation on multiple git repositories in subfolders

    positional arguments:
      operation             The git operation to perform on each repository, i.e.
                            the part usually put after 'git '. (unless running in
                            --raw mode)

    optional arguments:
      -h, --help            show this help message and exit
      -I includefile, --include-from includefile
                            Read repositories to operate on from specified file.
      -i include, --include include
                            Specify comma-separated list of repositories to use.
                            Suppresses automatic repo detection
      -e exclude, --exclude exclude
                            Specify comma-separated list of repositories to
                            exclude. Applied after auto-detect or include(-file)
      -d date, --date date  Specify checkout by date instead of ref. This
                            parameter must be used with gitall checkout <branch>.
                            The date format is YYYY-MM-DD HH:MM:SS or a shorter
                            format. See also the date format used by git rev-list
      -n, --noseparator     Suppress printing of separator line between
                            repositories.
      -q, --quiet           decrease output verbosity. Repeat for more silence, or
                            to cancel out -v
      -v, --verbose         increase output verbosity. Repeat for more noise, or
                            to cancel out -q
      -r, --raw             Treat the specified command as a 'full' command, i.e.
                            not a git 'sub'-command. Example: gitall --raw cat
                            .gitignore

    NOTE: --quiet and --verbose cancel each other out one by one so '-qqv' gives
    the same result as '-q'

##Installing GitAll

My personal preference is to clone the git repo and then create a symbolic in
`/usr/bin/gitall` pointing to the cloned `gitall`.
This way, the command is accessible to all users of the
computer, but still remains within the repository for easy updates. An example
of how to do this follows:

    // make the command executable
    $ chmod +x gitall

    // create the symbolic link (cannot be a relative path)
    $ sudo ln -s <full path to this repository>/gitall /usr/bin/gitall

If you get the message `env: python2: No such file or directory` when trying to
run gitall, your Python install is broken (this the default on Mac OS X). Either
make a [fresh install](https://www.python.org/downloads/) of Python 2, or do this:

    // workaround: symlink python2 to python
    $ sudo ln -s $(which python){,2}

##Sample Output

Run the command `gitall --verbose status` and see the following output: (if you have a colour terminal, the output is coloured for better readability)


    Running command: git status
    gitall started in:  /Users/Walter/GitHub
    --------------------------------------------------------------------------------
    Current repo: color
    # On branch master
    nothing to commit (working directory clean)
    --------------------------------------------------------------------------------
    Current repo: gitall
    # On branch master
    #
    # Initial commit
    #
    # Untracked files:
    #   (use "git add <file>..." to include in what will be committed)
    #
    #   README.md
    #   gitall
    nothing added to commit but untracked files present (use "git add" to track)
    --------------------------------------------------------------------------------

Running without the --verbose, reduces unneccesary output clutter (the first 2 status lines and "Current repo:"), and adding one or more --quiet (or e.g. -q, -qq) reduces noise even further.

##Disclaimer

Be careful! There are no checks currently in place, so whatever git commands you pass in will be executed in all git repositories below the current directory!

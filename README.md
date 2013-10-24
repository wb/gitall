#GitAll

Easily run git commands in multiple subdirectories.

##How to use GitAll

	usage: gitall [-h] [-n] [-q] [-v] command

	Perform a git command on multiple git repositories in subfolders

	positional arguments:
	  command            The git command to perform on each repository. I.e. the
	                     part usually put after 'git'

	optional arguments:
	  -h, --help         show this help message and exit
	  -n, --noseparator  Suppress printing of separator line between repositories.
	  -q, --quiet        decrease output verbosity. Repeat for more silence, or to
	                     cancel out -v
	  -v, --verbose      increase output verbosity. Repeat for more noise, or to
	                     cancel out -q

	NOTE: --quiet and --verbose cancel out each other. e.g. '-qqv' = '-q'

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
	#	README.md
	#	gitall
	nothing added to commit but untracked files present (use "git add" to track)
	--------------------------------------------------------------------------------

Running without the --verbose, reduces unneccesary output clutter (the first 2 status lines and "Current repo:"), and adding one or more --quiet (or e.g. -q, -qq) reduces noise even further.

##Disclaimer

Be careful! There are no checks currently in place, so whatever git commands you pass in will be executed in all git repositories in the current or specified directory!

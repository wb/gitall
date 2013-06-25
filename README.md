
#GitAll

Easily run git commands in multiple subdirectories.

##How to use GitAll

    Usage: gitall command

##Installing GitAll

My personal preference is to create a symbolic link between `gitall` and
`/usr/bin/gitall`. This way, the command is accessible to all users of the
computer, but still remains within the repository for easy updates. An example
of how to do this follows:

    // make the command executable
    $ chmod +x gitall

    // create the symbolic link (cannot be a relative path)
    $ sudo ln -s <full path to this repository>/gitall /usr/bin/gitall

##Sample Output

Run the command `gitall status` and see the following output: (if you have a colour terminal, the output is coloured for better readability)


	################################################################################

	Running command: git status
	gitall started in:  /Users/Walter/GitHub
	################################################################################

	Current repo: color
	# On branch master
	nothing to commit (working directory clean)

	################################################################################

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

	################################################################################


##Disclaimer

Be careful! There are no checks currently in place, so whatever git commands you pass in will be executed in all git repositories in the current or specified directory!
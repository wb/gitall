
#GitAll

Easily run git commands in multiple subdirectories.

##How to use GitAll

    Usage: gitall [options] command

    Options:
      -h, --help            show this help message and exit
      -d DIRECTORY, --directory=DIRECTORY
                        Specify the parent directory. Omit to use current
                        directory.


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


	################################################################################
	
	Running command: git status
	
	################################################################################
	
	Current respository location: /Users/Walter/GitHub/color
	# On branch master
	nothing to commit (working directory clean)
	
	################################################################################
	
	Current respository location: /Users/Walter/GitHub/gitall
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
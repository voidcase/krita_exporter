# How to use

	krita-exporter /dir/with/your/kra/file/tree /dir/where/you/want/your/exported/file/tree

So for example, if this is your source directory:

	img/
		backgrounds/
			level1.kra
			level2.kra
			level3.kra
			bonus_level.kra
		sprites/
			protagonist.kra
			enemy_skeleton.kra

Your destination directory will look like this after running the command:

	img/
		backgrounds/
			level1.png
			level2.png
			level3.png
			bonus_level.png
		sprites/
			protagonist.png
			enemy_skeleton.png

## optional arguments:

	  -h, --help     show this help message and exit
	  --force        Export even those files which already have not been modified
					 since the last export.
	  --purge        empty destination folder before refilling
	  -c, --confirm  manually confirm that the changed files are the ones you want
					 to change
	  -w, --watch    poll directory for changes, run until exited.

Beyond that just read the code, it's pretty small :)

# How to use

Make sure that you have `krita` installed first. If it's called something else on your system for some reason, specify that name with the `--alt` flag.

	python3 krita_exporter.py /dir/with/your/kra/file/tree /dir/where/you/want/your/exported/file/tree

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

Default export format is `png`. You can set it with `--format`.

Beyond that just read the code, it's pretty small :)

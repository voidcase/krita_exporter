# How to use

Make sure that you have `krita` installed first. If it's called something else on your system for some reason, specify that name with the `--alt` flag.

	python3 krita_exporter.py /dir/with/your/kra/file/tree /dir/where/you/want/your/exported/file/tree | sh

`| sh` is because the script just prints the commands to stdout so you can inspect them first if you want to.
Default export format is `png`. You can set it with `--format`.

Beyond that just read the code, it's pretty small :)

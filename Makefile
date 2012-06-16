all:
	gcc -O2 -ansi -Wall -Werror -o bussize bussize.c
	gcc -O2 -ansi -Wall -Werror -o busorder busorder.c

	python u-autotool --help > /dev/null

	python -c "import py_compile ; py_compile.compile(\"u-autotool\")"

install:
	cp u-autotool ~/sandbox/bin
	cp -r ua ~/sandbox/bin
	cp bussize ~/sandbox/bin
	cp busorder ~/sandbox/bin

clean:
	rm -f ./bussize ./busorder ./u-autotoolc ./ua/*.pyc


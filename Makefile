all:
	gcc -O2 -ansi -Wall -Werror -o bussize bussize.c
	gcc -O2 -ansi -Wall -Werror -o busorder busorder.c

	python -c "import py_compile ; py_compile.compile(\"u-autotool\")"

install:
	cp u-autotool /usr/bin
	cp bussize /usr/bin
	cp busorder /usr/bin

clean:
	rm -f ./bussize ./busorder ./u-autotoolc


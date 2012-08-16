all:
	python u-autotool --help > /dev/null

install:
	cp u-autotool ~/sandbox/bin
	cp -r ua ~/sandbox/bin

clean:
	rm -f ./ua/*.pyc


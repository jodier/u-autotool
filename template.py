#!/usr/bin/env python

#############################################################################

import zlib, base64

#############################################################################

configure_fp = open('configure.sh', "r")
bussize_fp = open('bussize.c', "r")
busorder_fp = open('busorder.c', "r")

configure = configure_fp.read()
bussize = bussize_fp.read().replace('%', '%%')
busorder = busorder_fp.read().replace('%', '%%')

#############################################################################

if __name__ == '__main__':


	#####################################################################
	# TOOlS								    #
	#####################################################################

	TOOLS = 'cat > bussize_$$.c << EOF\n%s\nEOF\n\ncat > busorder_$$.c << EOF\n%s\nEOF' % (bussize, busorder)

	configure = configure.replace('$$TOOLS$$', TOOLS)

	#####################################################################
	# TEMPLATE							    #
	#####################################################################

	configure = base64.b64encode(zlib.compress(configure, 9))

	#####################################################################

	i = 1

	TEMPLATE = 'template = \\\n\tb\''

	for c in configure:
		TEMPLATE += '%c' % c

		i += 1

		if i == 65:
			i = 1;

			TEMPLATE += '\' +\\\n\tb\''

	TEMPLATE += '\'\n\n'

	#####################################################################

	print(TEMPLATE)

	#####################################################################


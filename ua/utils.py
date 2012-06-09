#############################################################################
# Author  : Jerome ODIER
#
# Email   : jerome.odier@cern.ch
#
# Version : 1.0 beta (2010-2012)
#
#
# This file is part of U-AUTOTOOL.
#
#  u-autotool is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  u-autotool is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import os, re, sys, glob, subprocess, xml.dom.minidom

#############################################################################
# XML									    #
#############################################################################

def getStripedIAttribute(self, name):
	return self.getAttribute(name).strip()

xml.dom.minidom.Element.getStripedIAttribute = \
					getStripedIAttribute

#############################################################################

def getStripedLAttribute(self, name):
	return self.getAttribute(name).strip().lower()

xml.dom.minidom.Element.getStripedLAttribute = \
					getStripedLAttribute

#############################################################################

def getStripedUAttribute(self, name):
	return self.getAttribute(name).strip().upper()

xml.dom.minidom.Element.getStripedUAttribute = \
					getStripedUAttribute

#############################################################################

def getItemsByLAttrName(self, name):
	s = self.getAttribute(name).strip().lower()

	if len(s) == 0:
		result = [                ]
	else:
		result = re.split('\W+', s)

	return result

xml.dom.minidom.Element.getItemsByLAttrName = \
					getItemsByLAttrName

#############################################################################

def getItemsByUAttrName(self, name):
	s = self.getAttribute(name).strip().upper()

	if len(s) == 0:
		result = [                ]
	else:
		result = re.split('\W+', s)

	return result

xml.dom.minidom.Element.getItemsByUAttrName = \
					getItemsByUAttrName

#############################################################################
# CONTEXT								    #
#############################################################################

COMPS = {
	'c': '$GCC',
	'c++': '$GXX',
	'objective-c': '$ACC',
	'objective-c++': '$AXX',
}

#############################################################################

HELLOWORLDS = {
	'c': 'int main(void) { return 0; }',
	'c++': 'int main(void) { return 0; }',
	'objective-c': 'int main(void) { return 0; }',
	'objective-c++': 'int main(void) { return 0; }',
}

#############################################################################

class context:
	#####################################################################

	def __init__(self, debug = '', verbose = False):

		#############################################################
		# GLOBAL						    #
		#############################################################

		self.build_targets = set([
			# EMPTY #
			# EMPTY #
			# EMPTY #
		])

		self.build_types = [
			'UND',
			'LIB',
			'EXE',
		]

		self.build_links = [
			'SHARED',
			'STATIC',
			'BOTH',
		]

		#############################################################
		# TREE							    #
		#############################################################

		self.fuses = []
		self.deps = []
		self.needed_deps = set([])
		self.option_deps = set([])
		self.projects = []
		self.links = []

		#############################################################
		# OTHER							    #
		#############################################################

		self.debug = debug

		self.verbose = verbose

		self.cmdline = 'python %s' % sys.argv[0]

		self.debug_nr = 0
		self.ooops_nr = 0
		self.error_nr = 0

#############################################################################
# TREES									    #
#############################################################################

def myprint(s, shift):

	for i in xrange(shift):
		sys.stdout.write(' ')

	print(s)

#############################################################################

def displayTree(T, level = 0):
	#####################################################################
	# LISTS								    #
	#####################################################################

	if   type(T).__name__ == 'list':

		for item in enumerate(T):

			myprint('idx: %d' % item[0], level)

			displayTree(item[1], level + 4)

	#####################################################################
	# DICTS								    #
	#####################################################################

	elif type(T).__name__ == 'dict':

		for item in T.iteritems():

			myprint('key: %s' % item[0], level)

			displayTree(item[1], level + 4)

	#####################################################################
	# LEAFS								    #
	#####################################################################

	else:
		myprint(T, level)

#############################################################################
# PATHS									    #
#############################################################################

OS_ENVIRON = {
	'BIN': '${OS_BIN}',
	'INC': '${OS_INC}',
	'LIB': '${OS_LIB}',
	'SRC': '${OS_SRC}',
}

#############################################################################

def resolveEnv(ctx, s):
	result = ''

	for part in re.split('(\$\{[^\}]+\})', s):

		if len(part) > 3 and part[0] == '$' and part[+1] == '{' and part[-1] == '}':
			part = part[+2: -1]

			if not os.environ.has_key(part):
				ooops(ctx, 'Environnement variable `%s` not defined !' % part)
			else:
				result += os.environ[part]
		else:
			result += part

	return result

#############################################################################

def resolveVar(ctx, s):
	result = ''

	for part in re.split('(\$\([^\)]+\))', s):

		if len(part) > 3 and part[0] == '$' and part[+1] == '(' and part[-1] == ')':
			part = part[+2: -1]

			if not OS_ENVIRON.has_key(part):
				ooops(ctx, 'Internal variable `%s` not defined !' % part)

			else:
				result += OS_ENVIRON[part]
		else:
			result += part

	return result

#############################################################################

def protect(ctx, s):
	s = s.replace('\\', '\\\\')
	s = s.replace('$(', '\\$(')
	s = s.replace('${', '\\${')
	s = s.replace('!{', '${')

	return s

#############################################################################

def unprotect(ctx, s):

	return resolveVar(ctx, s).replace('!{', '${')

#############################################################################

def buildPaths(ctx, s):
	s = resolveEnv(ctx, s)

	return [os.path.normpath(f).replace('\\', '/') for f in glob.iglob(s)]

#############################################################################

def relpath1(path):
	return os.path.relpath(path, '.').replace('\\', '/')

os.path.relpath1 = \
		relpath1

#############################################################################

def relpath2(path):
	return os.path.relpath('.', path).replace('\\', '/')

os.path.relpath2 = \
		relpath2

#############################################################################
# SUBPROCESS								    #
#############################################################################

def popen(command):
	p = subprocess.Popen(
		command,
		shell = True,
		stdout = sys.stdout,
		stderr = sys.stderr,
		universal_newlines = True
	)

	return p.wait()

#############################################################################
# MESSAGES								    #
#############################################################################

def debug(ctx, msg):
	print('[Debug] %s' % msg)
	ctx.debug_nr += 1

#############################################################################

def ooops(ctx, msg):
	print('[Ooops] %s' % msg)
	ctx.ooops_nr += 1

#############################################################################

def error(ctx, msg):
	print('[Error] %s' % msg)
	ctx.error_nr += 1

#############################################################################

def fatal(ctx, msg):
	print('[Fatal] %s' % msg)
	sys.exit(1)

#############################################################################

def status(ctx):
	if ctx.debug_nr > 0\
	   or		\
	   ctx.ooops_nr > 0\
	   or		\
	   ctx.error_nr > 0:

		print('')

		if ctx.debug_nr > 0:
			print('There are %d \'debug\' messages !' % ctx.debug_nr)

		if ctx.ooops_nr > 0:
			print('There are %d \'ooops\' messages !' % ctx.ooops_nr)

		if ctx.error_nr > 0:
			print('There are %d \'error\' messages !' % ctx.error_nr)

#############################################################################


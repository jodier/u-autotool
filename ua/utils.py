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

EXTS = {
	'c': '.c',
	'c++': '.cc',
	'objective-c': '.m',
	'objective-c++': '.mm',
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

	def __init__(self):

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

		self.debug = '-O0'

		self.verbose = False

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
# VALUES								    #
#############################################################################

UA_ENVIRON = {
	'BIN': '${OS_BIN}',
	'INC': '${OS_INC}',
	'LIB': '${OS_LIB}',
	'SRC': '${OS_SRC}',
}

#############################################################################

ENV_RE = re.compile('\$\{[ \t]*([^ \t\}]+)[ \t]*\}')
VAR_RE = re.compile('\$\([ \t]*([^ \t\)]+)[ \t]*\)')

#############################################################################

def resolveEnv(ctx, s):
	print(s)
	while True:
		#############################################################

		m = ENV_RE.search(s)

		if m is None:
			break

		#############################################################

		key = m.group(1)
		val = ((((''))))

		if os.environ.has_key(key):
			val = os.environ[key]
		else:
			ooops(ctx, 'Environ variable `%s` not defined !' % key)

		#############################################################

		s = s[: m.start()] + val + s[m.end():]

		#############################################################

	return s

#############################################################################

def resolveVar(ctx, s):

	while True:
		#############################################################

		m = VAR_RE.search(s)

		if m is None:
			break

		#############################################################

		key = m.group(1)
		val = ((((''))))

		if UA_ENVIRON.has_key(key):
			val = UA_ENVIRON[key]
		else:
			ooops(ctx, 'Internal variable `%s` not defined !' % key)

		#############################################################

		s = s[: m.start()] + val + s[m.end():]

		#############################################################

	return s

#############################################################################

def resolve(ctx, s):
	s = s.replace('!(', '$(')
	s = s.replace('!{', '${')
	s = resolveEnv(ctx, s)

	return s

#############################################################################

def protect(ctx, s):
	s = s.replace('\\', '\\\\')
	s = s.replace('$(', '\\$(')
	s = s.replace('${', '\\${')
	s = s.replace('!(', '$(')
	s = s.replace('!{', '${')

	return s

#############################################################################

def unprotect(ctx, s):
	s = resolveVar(ctx, s)
	s = s.replace('!(', '$(')
	s = s.replace('!{', '${')

	return s

#############################################################################

PROJECT_name_RE = re.compile('\$\([ \t]*PROJECT_name[ \t]*\)')
PROJECT_NAME_RE = re.compile('\$\([ \t]*PROJECT_NAME[ \t]*\)')

#############################################################################

def process(ctx, name, s):
	name_lower = name.lower()
	name_upper = name.upper()

	s = s.strip()

	s = PROJECT_name_RE.sub(name_lower, s)
	s = PROJECT_NAME_RE.sub(name_upper, s)

	return s

#############################################################################

def processAndProtect(ctx, name, s):

	return protect(ctx, process(ctx, name, s))

#############################################################################

def processAndUnprotect(ctx, name, s):

	return unprotect(ctx, process(ctx, name, s))

#############################################################################

def buildPaths(ctx, name, s):
	s = resolveEnv(ctx, process(ctx, name, s))

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


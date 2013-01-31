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

import os, re, ua

#############################################################################

INC_RE = re.compile('#include[ \t]*"([^"]+)"')

#############################################################################

def makedeps(ctx, L, M, old_fileName, new_fileName):

	if new_fileName in M:

		return False

	#####################################################################

	try:
		fp = open(new_fileName, "r")

		lines = fp.readlines()

	except IOError:
		#ua.utils.ooops(ctx, 'From `%s`, could not open file `%s`' % (old_fileName, new_fileName))

		return False

	#####################################################################

	dirName = os.path.dirname(new_fileName)

	#####################################################################

	old_fileName = new_fileName

	#####################################################################

	M.append(new_fileName)

	#####################################################################

	for line in lines:

		m = INC_RE.search(line)

		if not m is None:

			new_fileName = os.path.normpath(dirName + os.path.sep + m.group(1))

			if makedeps(ctx, L, M, old_fileName, new_fileName) != False:

				L.append('\\$(SRC_PREFIX)/%s' % \
						new_fileName.replace('\\', '/'))

	#####################################################################

	fp.close()

	return True

#############################################################################

def buildRules(ctx, NAME, src, opt, inc, targets, fuses):

	dirname = os.path.dirname(src)
	basename = os.path.basename(src)

	(shortname, extension) = os.path.splitext(basename)

	EXTENSION = '.o'

	#####################################################################

	if len(dirname) > 0:
		obj = ('\\$(PWD_PREFIX)/%s/%s_%s%s') % (dirname.replace('\\', '/'), NAME, shortname, EXTENSION)

		src = ('\\$(SRC_PREFIX)/%s/'+'%s%s') % (dirname.replace('\\', '/'),       shortname, extension)

		fname = dirname + os.path.sep + basename

	else:
		obj = ('\\$(PWD_PREFIX)/%s_%s%s') % (NAME, shortname, EXTENSION)

		src = ('\\$(SRC_PREFIX)/'+'%s%s') % (      shortname, extension)

		fname = basename

	#####################################################################

	L = [src]
	M = [   ]

	makedeps(ctx, L, M, 'none', fname)

	rules = '%s: \\\\\n %s\n' % (obj, ' \\\\\n '.join(L))

	#####################################################################

	if len(opt) > 0:
		opt = ' ' + opt
	if len(inc) > 0:
		inc = ' ' + inc

	#####################################################################

	rules += '\t@install -d \`dirname \$@\`\n'

	if ctx.verbose == False:
		rules += '\t@printf "Building \$@\t"\n'

		if   extension in ['.c']:
			rules += '\t@\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -c -o \$@ \$<\n' % (NAME, opt, NAME, inc)
		elif extension in ['.cc', '.cpp', '.cxx']:
			rules += '\t@\$(GXX) \$(GXX_OPT_%s)%s \$(GXX_INC_%s)%s -c -o \$@ \$<\n' % (NAME, opt, NAME, inc)
		elif extension in ['.m']:
			rules += '\t@\$(ACC) \$(ACC_OPT_%s)%s \$(ACC_INC_%s)%s -c -o \$@ \$<\n' % (NAME, opt, NAME, inc)
		elif extension in ['.mm']:
			rules += '\t@\$(AXX) \$(AXX_OPT_%s)%s \$(AXX_INC_%s)%s -c -o \$@ \$<\n' % (NAME, opt, NAME, inc)

		elif extension in ['.l']:
			rules += '\t@\$(FLEX) -o \$(basename \$<).c \$<\n'
			rules += '\t@\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -xc -c -o \$@ \$(basename \$<).c\n' % (NAME, opt, NAME, inc)
			rules += '\t@\$(RM) \$(basename \$<).c\n'
		elif extension in ['.y']:
			rules += '\t@\$(BISON) -o\$(basename \$<).c \$<\n'
			rules += '\t@\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -xc -c -o \$@ \$(basename \$<).c\n' % (NAME, opt, NAME, inc)
			rules += '\t@\$(RM) \$(basename \$<).c\n'

		elif extension in ['.s', '.S', '.asm']:
			rules += '\t@\$(GCC) \$(GCC_OPT_%s)%s -c -o \$@ \$<\n' % (NAME, opt)

		rules += '\t@printf "\\033[69G[ \\033[32m Ok. \\033[0m ]\\n"\n'

	else:
		rules += '\t@printf "\\033[36m%s>\\033[0m "\n' % NAME

		if   extension in ['.c']:
			rules += '\t\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -c -o \$@ \$<\n' % (NAME, opt, NAME, inc)
		elif extension in ['.cc', '.cpp', '.cxx']:
			rules += '\t\$(GXX) \$(GXX_OPT_%s)%s \$(GXX_INC_%s)%s -c -o \$@ \$<\n' % (NAME, opt, NAME, inc)
		elif extension in ['.m']:
			rules += '\t\$(ACC) \$(ACC_OPT_%s)%s \$(ACC_INC_%s)%s -c -o \$@ \$<\n' % (NAME, opt, NAME, inc)
		elif extension in ['.mm']:
			rules += '\t\$(AXX) \$(AXX_OPT_%s)%s \$(AXX_INC_%s)%s -c -o \$@ \$<\n' % (NAME, opt, NAME, inc)

		elif extension in ['.l']:
			rules += '\t\$(FLEX) -o \$(basename \$<).c \$<\n'
			rules += '\t\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -xc -c -o \$@ \$(basename \$<).c\n' % (NAME, opt, NAME, inc)
			rules += '\t@\$(RM) \$(basename \$<).c\n'
		elif extension in ['.y']:
			rules += '\t\$(BISON) -o\$(basename \$<).c \$<\n'
			rules += '\t\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -xc -c -o \$@ \$(basename \$<).c\n' % (NAME, opt, NAME, inc)
			rules += '\t@\$(RM) \$(basename \$<).c\n'

		elif extension in ['.s', '.S', '.asm']:
			rules += '\t\$(GCC) \$(GCC_OPT_%s)%s -c -o \$@ \$<\n' % (NAME, opt)

		rules += '\t@printf "\\033[69G[ \\033[32m Ok. \\033[0m ]\\n"\n'

	rules += '\n'

	#####################################################################

	return src, obj, rules, targets, fuses

#############################################################################


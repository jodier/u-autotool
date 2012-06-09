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

def makedeps(ctx, L, fileName):
	#####################################################################

	dirName = os.path.dirname(fileName)

	#####################################################################

	try:
		file = open(fileName, "r")

		lines = file.readlines()

	except IOError:
		ua.utils.ooops(ctx, 'Could not find file `%s`' % fileName)
		return

	#####################################################################

	for line in lines:
		m = INC_RE.match(line)

		if not m is None:
			f = os.path.normpath(dirName + '/' + m.group(1))

			L.append('\\$(SRC_PREFIX)/%s' % f.replace('\\', '/'))

			makedeps(ctx, L, f)

	#####################################################################

	file.close()

#############################################################################

def buildRules(ctx, projetName, src, opt, inc, targets, fuses):

	dirname = os.path.dirname(src).replace('\\', '/')
	basename = os.path.basename(src).replace('\\', '/')

	ext = os.path.splitext(basename)

	#####################################################################

	obj = '\\$(PWD_PREFIX)/%s/%s_%s%s' % (dirname, projetName, ext[0], '.o')

	src = '\\$(SRC_PREFIX)/%s/%s%s' % (dirname, ext[0], ext[1])

	#####################################################################

	L = [src]

	makedeps(ctx, L, dirname + '/' + basename)

	rules = '%s: \\\\\n %s\n' % (obj, ' \\\\\n '.join(L))

	#####################################################################

	rules += '\t@install -d \`dirname \$@\`\n'

	if ctx.verbose == False:
		rules += '\t@printf "Building \$@\t"\n'

		if   ext[1] in ['.c']:
			rules += '\t@\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -c -o \$@ \$<\n' % (projetName, opt, projetName, inc)
		elif ext[1] in ['.cc', '.cpp', '.cxx']:
			rules += '\t@\$(GXX) \$(GXX_OPT_%s)%s \$(GXX_INC_%s)%s -c -o \$@ \$<\n' % (projetName, opt, projetName, inc)
		elif ext[1] in ['.m']:
			rules += '\t@\$(ACC) \$(ACC_OPT_%s)%s \$(ACC_INC_%s)%s -c -o \$@ \$<\n' % (projetName, opt, projetName, inc)
		elif ext[1] in ['.mm']:
			rules += '\t@\$(AXX) \$(AXX_OPT_%s)%s \$(AXX_INC_%s)%s -c -o \$@ \$<\n' % (projetName, opt, projetName, inc)

		elif ext[1] in ['.l']:
			rules += '\t@\$(FLEX) -o \$(basename \$<).c \$<\n'
			rules += '\t@\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -xc -c -o \$@ \$(basename \$<).c\n' % (projetName, opt, projetName, inc)
			rules += '\t@\$(RM) \$(basename \$<).c\n'
		elif ext[1] in ['.y']:
			rules += '\t@\$(BISON) -o\$(basename \$<).c \$<\n'
			rules += '\t@\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -xc -c -o \$@ \$(basename \$<).c\n' % (projetName, opt, projetName, inc)
			rules += '\t@\$(RM) \$(basename \$<).c\n'

		elif ext[1] in ['.s', '.S', '.asm']:
			rules += '\t@\$(GCC) \$(GCC_OPT_%s)%s -c -o \$@ \$<\n'

		rules += '\t@printf "\\033[69G[ \\033[32m Ok. \\033[0m ]\\n"\n'
	else:
#		rules += '\t@printf "Building \$@\t"\n'

		if   ext[1] in ['.c']:
			rules += '\t\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -c -o \$@ \$<\n' % (projetName, opt, projetName, inc)
		elif ext[1] in ['.cc', '.cpp', '.cxx']:
			rules += '\t\$(GXX) \$(GXX_OPT_%s)%s \$(GXX_INC_%s)%s -c -o \$@ \$<\n' % (projetName, opt, projetName, inc)
		elif ext[1] in ['.m']:
			rules += '\t\$(ACC) \$(ACC_OPT_%s)%s \$(ACC_INC_%s)%s -c -o \$@ \$<\n' % (projetName, opt, projetName, inc)
		elif ext[1] in ['.mm']:
			rules += '\t\$(AXX) \$(AXX_OPT_%s)%s \$(AXX_INC_%s)%s -c -o \$@ \$<\n' % (projetName, opt, projetName, inc)

		elif ext[1] in ['.l']:
			rules += '\t\$(FLEX) -o \$(basename \$<).c \$<\n'
			rules += '\t\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -xc -c -o \$@ \$(basename \$<).c\n' % (projetName, opt, projetName, inc)
			rules += '\t@\$(RM) \$(basename \$<).c\n'
		elif ext[1] in ['.y']:
			rules += '\t\$(BISON) -o\$(basename \$<).c \$<\n'
			rules += '\t\$(GCC) \$(GCC_OPT_%s)%s \$(GCC_INC_%s)%s -xc -c -o \$@ \$(basename \$<).c\n' % (projetName, opt, projetName, inc)
			rules += '\t@\$(RM) \$(basename \$<).c\n'

		elif ext[1] in ['.s', '.S', '.asm']:
			rules += '\t\$(GCC) \$(GCC_OPT_%s)%s -c -o \$@ \$<\n'

#		rules += '\t@printf "\\033[69G[ \\033[32m Ok. \\033[0m ]\\n"\n'

	rules += '\n'

	#####################################################################

	return src, obj, rules, targets, fuses

#############################################################################


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

import os, re, subprocess

#############################################################################

def buildRules(ctx, projetName, src, opt, inc, targets, fuses):

	pipe = subprocess.Popen(
		'gcc -DAUTOGEN -x c -E -MM -MG %s' % src,
		shell = True,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		universal_newlines = True
	)

	stdout, stderr = pipe.communicate()

	if pipe.returncode != 0:

		if not stdout is None:
			print(stdout)

		if not stderr is None:
			print(stderr)

		sys.exit(pipe.returncode)

	##

	if len(opt) > 0:
		opt = ' ' + opt

	if len(inc) > 0:
		inc = ' ' + inc

	##

	dir = os.path.dirname(src)
	ext = os.path.splitext(src)

	#####################################################################

	L = re.split('[\s:\\\\]+', stdout.strip())

	#####################################################################

	rules = ''

	for i in range(len(L)):

		if i == 0x0000:
			if len(dir) == 0:
				L[i] = '\\$(PWD_PREFIX)/' + ''  +  '' + projetName + '_' + L[i]
			else:
				L[i] = '\\$(PWD_PREFIX)/' + dir + '/' + projetName + '_' + L[i]

			rules += L[i] + ': \\\\\n'
		else:
			L[i] = '\\$(SRC_PREFIX)/' + L[i]

			if i < len(L) - 1:
				rules += '\t' + L[i] + ' \\\\\n'
			else:
				rules += '\t' + L[i] + '' + '\n'

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

		elif ext[1] in ['.s', '.S']:
			rules += '\t@\$(GCC) -c -o \$@ \$<\n'

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

		elif ext[1] in ['.s', '.S']:
			rules += '\t\$(GCC) -c -o \$@ \$<\n'

#		rules += '\t@printf "\\033[69G[ \\033[32m Ok. \\033[0m ]\\n"\n'

	rules += '\n'

	#####################################################################

	src = L[1]
	obj = L[0]

	return src, obj, rules, targets, fuses

#############################################################################


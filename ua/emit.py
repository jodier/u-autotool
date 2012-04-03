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

import os, sys, zlib, base64, ua.utils, ua.rules, subprocess

#############################################################################

template = \
	b'eNrNWutz2jgQ/3z6K3TUGQdaQy7J5ENSd2oeyfmGAAPkwlySA8cI8NXYjG3apNf7' +\
	b'32/18AObhKQxbTJTkLQr7W8fWq1E3/xaubWcij9D6E2efwj1urVhp9s41QfqaGx5' +\
	b'jjEnWNoboc5lPRwvo3qvH3bkytL3KrZrGracOxhrggPiB1j5igvSWa1WOEHBjDgI' +\
	b'Y+io8tQ0ZTSx0nyDQYJvABCnb9+u4dOS6wHlCo+WTF3FH2FVxXLd8L5YjoxvToBB' +\
	b'8GGsCclYmTjkLlC8pRNYcyIDkdg+SfNMnWWSBVBkgSQBPwOIUO1RIDHPU4B0Yxxa' +\
	b'V5UNb43ZulqrqVdjRt5XZc9wbOuWT8g5DE6bDVBjYpM7rAxkVNV77ZYq31q+62Dl' +\
	b'fiyjPkUbULh5i4aVzxp9dUSjDyvj5XwxN8yZ5RC8/wFXxuRzxVna9ih3uZ1u+49G' +\
	b'Ld5lcjTSuzgVI7mb+aLX6Km7xdwXniwdM7DAWabrTKzp0iPDGbEX6F8IH9MI8Pv3' +\
	b'uNE+hY4ye4cVhdJw5m9s+QvbuIf4t3zMWAxnjMmdFSDEORQFQmBKApU7LZoZScUT' +\
	b'18OciPCjf1cSZ7uJ1154ZGLdqdwhEaPl+IFh27CdbOJDD3P6xuXjDLoiwv2HmEFK' +\
	b'FPQWBFQV3cANhZIxFjMwTRf+RqGrQbVGsL+cUME8xLCxYHJFLwe5fCWQu+Mj6nCa' +\
	b'qcB/+Df0X/4xB652FyzqwCtSCY1dxMLNh/OME2i25am0pJaKQguIIHVE7hYeLgwE' +\
	b'XwEfY/nqb/WmpF7vlkvXRXkkmE9O+PTkZFlOEolvmA/LjSI2WkHkGwmGV2VEARix' +\
	b'Jg7h9ewrwRRNS2WWx6aKcMhMFSlodeoOjwNlhr+JPRxOS+369aYj5syF02XvGBPP' +\
	b'c71jvHQ8YrpTx/oK8cYNdxxasBCGrgif0M5j1yG5RxJz3YjhE1kBNAw8fHVsu1+I' +\
	b'd3wDrSVsFWiNEHNsqam3LgZCtXZv2NLOG6o8HOq9Yf9iwOOD6V9q9walbyWt02k2' +\
	b'4LuudS/11tp5wJicd663zi7XMsICSUa93VvLBuNJNq1V77b1+lpWQUuyczbuMt35' +\
	b'bNjWGPNIxrKwkSx8JDzE/ZOzZziAU9jpaeEQKXBgv8O0GIRPjbU13u7CBy9aoEFL' +\
	b'C/hiJUUhd4CwJ7YSjZLwEA+3MLC4V0CvYe93rduoR6VC2XflmNbX+notphmc1Bg0' +\
	b'0tMShNU5MgrDpHna1M56qqz4M8Mj40SMhFH7MKjxPasXt4trfA9HlGVGkmJssFEe' +\
	b'wWbb34OsTO7Ig+g48YmWg/35ai0nEsKrCrdkSpJXU5K8/UQE0Kp6S4UrOW3qrZpq' +\
	b'Oaa9HBPahRu16nvmls6l26XvwxEp7scjXlkc7EeJvHrR6+l/NVTLP9iv6v0eN8Zq' +\
	b'FuGFrDhSV7NJaHh6w4tCQQzWQm/MD/ZjgjjY0xngpQtF2/WlC0U76ykLPbTIyhZ4' +\
	b'EqJJR69lVmPBGPWPDtd47ejw5V47OnzASkeHeD2w7/PepuUe8uF343uWLx9daSsO' +\
	b'/blJKcoPrjcm3mqCsK0gsEky3NrdeqML8dbU+8NGq65rrViPW2u6jrWqn2VY16oM' +\
	b't0jLcBzi+z9Abai5cjdkgD/gcuXc+EToPb9MLzTho0W+st7gSMjC8HyC6JC2DNy5' +\
	b'EVgm3L3v8ZQ4xDMCuBTd3uOlYgAxcF27TFnz1Zu+sdKgQfQRlVbSiL5r0mIa0XdF' +\
	b'Wk8jrQvfXSQeAUVdzR/sWG0tHut4gc3e6WiJvo0DWGxMKWpipS7FqTTusfBFcTUh' +\
	b'Rc3cYWWLIykzhLJVkpQZQtl6ScoMoWztJGWGtvmDgRS3k78XSHE7+ctB4g1s28+n' +\
	b'qZev9Ftq6oEqdzS0NpR4jYhocSjxIhGxLcMPGmpG1obvrbiIYriWdmMPFSvQrdIT' +\
	b'mY5RWFkyjHIyRZolwygnU/BZMnTzf0umsSR0icMq1oWOCV1SZKYLHRO6pMhMFzom' +\
	b'dEmRt6IL3QBCl3gvxLrQMaFLisx0oWNClxSZ6ULHhC4p8lZ0gXNi2O70VZ5maYEq' +\
	b'aX9qelOrNhuMSDVR9DJWdGFdpgSlUCWUJlCagsLw5w5wMGAAQYbAWmRjwsICIh8T' +\
	b'ZhXg8seiCWMlsWi1WgaLVqttH8sau2hr7KL9ALvQhfmhvONjEBSd5UW4B7hzK1Am' +\
	b'njEnysK1nABqWmXiuMrt0rIDy8HKJf0hRrlk78dYWVgLwpyZ64Ja3gi1vBHmXk/v' +\
	b'lN1jDJ8m+uXjwgMUE1yoAoCx5UwB8cdrpwAUHhZFLMJDqBAGVb8TtWkwYcXEiksn' +\
	b'w7/3iXWv8PXewcHVwf68/anMmntzfEMlJHBsBjIYcHGhbaMeje6w/WIg8004NGEQ' +\
	b'bcUgYvNH7Zfj2AxEGERbMYiWMIj2AoNsK+DsTWrRC0aRw929hdsu+08TALtYNgX6' +\
	b'Z0blnbmif3pRvmD3vLie9hyf3W/SjV2YhHKlV6vPq7+7s5+Zt/wesO2ngJ/6CCAe' +\
	b'stPPH6/+p7LtuP5/x2ygeA=='

#############################################################################

def configure(ctx):
	#####################################################################
	# CONFIGURE HELP						    #
	#####################################################################

	HELP = ''

	for fuse in ctx.fuses:
		if len(fuse['keys']) == 0:
			S1 = '      --enable-%s' % fuse['name']
		else:
			S1 = '      --enable-%s=VALUE' % fuse['name']

		S2 = '      --disable-%s' % fuse['name']

		HELP += S1 + ''.join([' ' for i in range(max(0, 30 - len(S1)))]) + 'enable %s\n' % fuse['help']
		HELP += '                              [%s]\n' % fuse['default']
		HELP += S2 + ''.join([' ' for i in range(max(0, 30 - len(S2)))]) + 'disable %s\n' % fuse['help']

	#####################################################################
	# CONFIGURE PARSER						    #
	#####################################################################

	PARSER = ''

	for fuse in ctx.fuses:
		if len(fuse['keys']) == 0:
			PARSER += '    --enable-%s)\n' % fuse['name']
			PARSER += '      FUSES[\'%s\']=""\n' % fuse['name']
			PARSER += '      ;;\n'
		else:
			PARSER += '    --enable-%s=*)\n' % fuse['name']
			PARSER += '      FUSES[\'%s\']="$arg"\n' % fuse['name']
			PARSER += '      ;;\n'

		PARSER += '    --disable-%s)\n' % fuse['name']
		PARSER += '      unset FUSES[\'%s\']\n' % fuse['name']
		PARSER += '      ;;\n'
		
	#####################################################################
	# CONFIGURE PROLOG						    #
	#####################################################################

	PROLOG = ''

	for link in ctx.links:

		pipe = subprocess.Popen('cd %s && %s %s' % (link['dir'], '%s%s' % (sys.argv[0], ctx.cmdline), link['base']), shell = True, universal_newlines = True)

		if pipe.wait() == 0:
			if len(link['targets']) == 0:
				PROLOG += 'install -d %s' % link['dir']							+ '\n' +\
					  ''										+ '\n' +\
					  'cd %s' % link['dir']								+ '\n' +\
					  ''										+ '\n' +\
					  'case $SRC_PREFIX in'								+ '\n' +\
					  ' /*)'									+ '\n' +\
					  '    $SRC_PREFIX/%s/configure $@' % (link['dir'])				+ '\n' +\
					  '    if test $? -ne 0;'							+ '\n' +\
					  '    then'									+ '\n' +\
					  '      exit 1'								+ '\n' +\
					  '    fi'									+ '\n' +\
					  '  ;;'									+ '\n' +\
					  '  *)'									+ '\n' +\
					  '    %s/$SRC_PREFIX/%s/configure $@' % (link['rid'], link['dir'])		+ '\n' +\
					  '    if test $? -ne 0;'							+ '\n' +\
					  '    then'									+ '\n' +\
					  '      exit 1'								+ '\n' +\
					  '    fi'									+ '\n' +\
					  '  ;;'									+ '\n' +\
					  'esac'									+ '\n' +\
					  ''										+ '\n' +\
					  'cd %s' % link['rid']								+ '\n' +\
					  ''										+ '\n' +\
					  ''
			else:
				for target in link['targets']:
					PROLOG += 'if test $OS_NAME = \'__IS_%s\';' % target				+ '\n' +\
						  'then'								+ '\n' +\
						  ''									+ '\n' +\
						  '  install -d %s' % link['dir']					+ '\n' +\
						  ''									+ '\n' +\
						  '  cd %s' % link['dir']						+ '\n' +\
						  ''									+ '\n' +\
						  '  case $SRC_PREFIX in'						+ '\n' +\
						  '   /*)'								+ '\n' +\
						  '      $SRC_PREFIX/%s/configure $@' % (link['dir'])			+ '\n' +\
						  '      if test $? -ne 0;'						+ '\n' +\
						  '      then'								+ '\n' +\
						  '        exit 1'							+ '\n' +\
						  '      fi'								+ '\n' +\
						  '    ;;'								+ '\n' +\
						  '    *)'								+ '\n' +\
						  '      %s/$SRC_PREFIX/%s/configure $@' % (link['rid'], link['dir'])	+ '\n' +\
						  '      if test $? -ne 0;'						+ '\n' +\
						  '      then'								+ '\n' +\
						  '        exit 1'							+ '\n' +\
						  '      fi'								+ '\n' +\
						  '    ;;'								+ '\n' +\
						  '  esac'								+ '\n' +\
						  ''									+ '\n' +\
						  '  cd %s' % link['rid']						+ '\n' +\
						  ''									+ '\n' +\
						  'fi'									+ '\n' +\
						  ''									+ '\n' +\
						  ''

	#####################################################################
	# CONFIGURE TESTS						    #
	#####################################################################

	TESTS = 'AVAILABLE=\'\'\n\n'

	#####################################################################

	XXXS = ctx.option_deps.   union  (ctx.needed_deps)
	YYYS = ctx.option_deps.difference(ctx.needed_deps)

#	print(ctx.option_deps, XXXS, YYYS)

	#####################################################################

	for target in ctx.build_targets:

		#################################
		# PASS 1			#
		#################################

		L = []

		for dep in ctx.deps:

			if dep in XXXS:

				L.append(dep)

		#################################
		# PASS 2			#
		#################################

		if len(L) > 0:
			lang = ctx.deps[dep]['lang']

			TESTS += '#############################################################################\n\n'

			TESTS += 'if test $OS_NAME = \'__IS_%s\';\n' % target +\
				 'then\n\n'

			TESTS += '  #########\n\n'

			for dep in L:

				if ctx.deps[dep]['targets'].has_key(target):

					info = ctx.deps[dep]['targets'][target]

					TESTS += '  opt_%s="%s"\n' % (dep, info['opt'])
					TESTS += '  opt_%s_resolved="%s"\n' % (dep, info['opt_resolved'])
					TESTS += '  inc_%s="%s"\n' % (dep, info['inc'])
					TESTS += '  inc_%s_resolved="%s"\n' % (dep, info['inc_resolved'])
					TESTS += '  lib_%s="%s"\n' % (dep, info['lib'])
					TESTS += '  lib_%s_resolved="%s"\n' % (dep, info['lib_resolved'])

					txt = info['txt']
				else:
					TESTS += '  opt_%s=""\n' % dep
					TESTS += '  opt_%s_resolved=""\n' % dep
					TESTS += '  inc_%s=""\n' % dep
					TESTS += '  inc_%s_resolved=""\n' % dep
					TESTS += '  lib_%s=""\n' % dep
					TESTS += '  lib_%s_resolved=""\n' % dep

					txt = ua.utils.HELLOWORLDS[lang]

				TESTS += '\n'

				TESTS += '  #########\n\n'

				TESTS += '  cat << EOF | %s -x%s $opt_%s_resolved $inc_%s_resolved -o /tmp/___%s - $lib_%s_resolved\n' % (ua.utils.COMPS[lang], lang, dep, dep, dep, dep) +\
					 '%s\n\n' % txt +\
					 'EOF\n\n'

				TESTS += '  #########\n\n'

				TESTS += '  if test $? -eq 0;\n' +\
					 '  then\n' +\
					 '    printf "Checking for %s\\033[69G[ \\033[32m Ok. \\033[0m ]\\n"\n' % dep +\
					 '    AVAILABLE="$AVAILABLE -DHAVE_%s"\n' % dep.upper() +\
					 '  else\n'

				if dep in YYYS:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[33mWarn.\\033[0m ]\\n"\n' % dep +\
						  '    AVAILABLE="$AVAILABLE -UHAVE_%s"\n' % dep.upper() +\
						  '    opt_%s=\'\'\n' % dep +\
						  '    inc_%s=\'\'\n' % dep +\
						  '    lib_%s=\'\'\n' % dep +\
						  '#   exit 1\n'
				else:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[31mError\\033[0m ]\\n"\n' % dep +\
						  '    AVAILABLE="$AVAILABLE -UHAVE_%s"\n' % dep.upper() +\
						  '    opt_%s=\'\'\n' % dep +\
						  '    inc_%s=\'\'\n' % dep +\
						  '    lib_%s=\'\'\n' % dep +\
						  '    exit 1\n'

				TESTS += '  fi\n\n'

				TESTS += '  #########\n\n'

			TESTS += 'fi\n\n'

	#####################################################################
	# CONFIGURE EPILOG						    #
	#####################################################################

	EPILOG = ''

	#####################################################################

	for project in ctx.projects:
		opts = ''
		incs = ''
		libs = ''

		for _opt in project['opts']:
			opts += ' %s' % _opt

		for _inc in project['incs']:
			incs += ' %s' % _inc

		for _lib in project['libs']:
			libs += ' %s' % _lib

		for _use in project['uses']:

			if ctx.deps.has_key(_use):
				opts += ' $opt_%s' % _use
				incs += ' $inc_%s' % _use
				libs += ' $lib_%s' % _use
			else:
				ua.utils.ooops(ctx, 'dependency `%s` not defined !' % _use)

		##

		NAME = project['NAME']

		##

		EPILOG += 'GCC_OPT_%s=\$(GCC_OPT)%s\n' % (NAME, opts)
		EPILOG += 'GCC_INC_%s=\$(GCC_INC)%s\n' % (NAME, incs)
		EPILOG += 'GCC_LIB_%s=\$(GCC_LIB)%s\n' % (NAME, libs)
		EPILOG += '\n'

		EPILOG += 'GXX_OPT_%s=\$(GCC_OPT_%s)\n' % (NAME, NAME)
		EPILOG += 'GXX_INC_%s=\$(GCC_INC_%s)\n' % (NAME, NAME)
		EPILOG += 'GXX_LIB_%s=\$(GCC_LIB_%s)\n' % (NAME, NAME)
		EPILOG += '\n'

		EPILOG += 'ACC_OPT_%s=\$(GCC_OPT_%s)\n' % (NAME, NAME)
		EPILOG += 'ACC_INC_%s=\$(GCC_INC_%s)\n' % (NAME, NAME)
		EPILOG += 'ACC_LIB_%s=\$(GCC_LIB_%s)\n' % (NAME, NAME)
		EPILOG += '\n'

		EPILOG += 'AXX_OPT_%s=\$(GCC_OPT_%s)\n' % (NAME, NAME)
		EPILOG += 'AXX_INC_%s=\$(GCC_INC_%s)\n' % (NAME, NAME)
		EPILOG += 'AXX_LIB_%s=\$(GCC_LIB_%s)\n' % (NAME, NAME)
		EPILOG += '\n'

	#####################################################################
	# MAKEFILE RULES						    #
	#####################################################################

	RULES = ''

	#####################################################################

	RULES += 'all_rules ='

	for project in ctx.projects:

		if len(project['targets']) == 0:
			RULES += ' all_%s' % project['name']

	RULES += '\n'
	RULES += '\n'

	RULES += 'install_rules ='

	for project in ctx.projects:

		if len(project['targets']) == 0:
			RULES += ' install_%s' % project['name']

	RULES += '\n'
	RULES += '\n'

	RULES += 'clean_rules ='

	for project in ctx.projects:

		if len(project['targets']) == 0:
			RULES += ' clean_%s' % project['name']

	RULES += '\n'
	RULES += '\n'

	#####################################################################

	for project in ctx.projects:

		if len(project['targets']) != 0:
			RULES += 'ifneq (\\$(findstring %s, \\$(GCC_OPT)),)\n' % target +\
				 '  all_rules += all_%s\n' % project['name'] +\
				 '  install_rules += install_%s\n' % project['name'] +\
				 '  clean_rules += clean_%s\n' % project['name'] +\
				 'endif\n'

	RULES += '\n'

	#####################################################################

	RULES += 'all: \\$(all_rules)\n'

	for link in ctx.links:

		if len(link['targets']) == 0:
			RULES += '\t@make -C "%s" all\n' % link['dir']
		else:
			for target in link['targets']:
				RULES += 'ifneq (\\$(findstring %s, \\$(GCC_OPT)),)\n' % target +\
					 '\t@make -C "%s" all\n' % link['dir'] +\
					 'endif\n'

	RULES += '\n'

	#####################################################################

	RULES += 'install: \\$(install_rules)\n'

	for link in ctx.links:

		if len(link['targets']) == 0:
			RULES += '\t@make -C "%s" install\n' % link['dir']
		else:
			for target in link['targets']:
				RULES += 'ifneq (\\$(findstring %s, \\$(GCC_OPT)),)\n' % target +\
					 '\t@make -C "%s" install\n' % link['dir'] +\
					 'endif\n'

	RULES += '\n'

	#####################################################################

	RULES += 'clean: \\$(clean_rules)\n'

	for link in ctx.links:

		if len(link['targets']) == 0:
			RULES += '\t@make -C "%s" clean\n' % link['dir']
		else:
			for target in link['targets']:
				RULES += 'ifneq (\\$(findstring %s, \\$(GCC_OPT)),)\n' % target +\
					 '\t@make -C "%s" clean\n' % link['dir'] +\
					 'endif\n'

	RULES += '\n'

	#####################################################################

	RULES += 'distclean: \\$(clean_rules)\n'

	for link in ctx.links:

		if len(link['targets']) == 0:
			RULES += '\t@make -C "%s" distclean\n' % link['dir']
		else:
			for target in link['targets']:
				RULES += 'ifneq (\\$(findstring %s, \\$(GCC_OPT)),)\n' % target +\
					 '\t@make -C "%s" distclean\n' % link['dir'] +\
					 'endif\n'

	RULES += '\n'

	#####################################################################

	RULES += '\t@\$(RM) ./Makefile.conf ./Makefile\n\n'

	#####################################################################

	for project in ctx.projects:
		RULES += '#############################################################################\n\n'

		srcs1 = ''
		objs1 = ''
		srcs2 = ''
		objs2 = ''
		rules = ''

		##

		NAME = project['NAME']

		##

		for src in project['srcs']:

			src, obj, rule, targets = ua.rules.buildRules(ctx, NAME, src['path'], src['opt'], src['inc'], src['targets'])

			if len(targets) == 0:
				srcs1 += ' \\\\\n %s' % src
				objs1 += ' \\\\\n %s' % obj
			else:
				for target in targets:
					srcs2 += 'ifneq (\\$(findstring %s, \\$(GCC_OPT)),)\n' % target +\
						 '  SRCS_%s += %s\n' % (NAME, src) +\
						 'endif\n'
					objs2 += 'ifneq (\\$(findstring %s, \\$(GCC_OPT)),)\n' % target +\
						 '  OBJS_%s += %s\n' % (NAME, obj) +\
						 'endif\n'

			rules += rule

		if len(srcs2) > 0:
			srcs2 = '\n' + srcs2
		if len(objs2) > 0:
			objs2 = '\n' + objs2

		##

		for obj in project['objs']:
			objs1 += ' \\\\\n %s' % obj

		##

		RULES += 'SRCS_%s =%s\n%s\nOBJS_%s =%s\n%s\n%s' % (NAME, srcs1, srcs2, NAME, objs1, objs2, rules)

	#####################################################################

	for project in ctx.projects:
		RULES += '#############################################################################\n\n'

		name = project['name']
		NAME = project['NAME']

		#####################################################

		if project['type'] == 'UND':

			#############################################

			RULES += 'all_%s: \$(OBJS_%s)\n' % (name, NAME)
			RULES += '\n'

			if len(project['txts']) > 0:
				RULES += '%s\n' % project['txts'][0]

			RULES += '\n'

			#############################################

			RULES += 'install_%s:\n' % (name)
			RULES += '\n'

			if len(project['txts']) > 1:
				RULES += '%s\n' % project['txts'][1]

			RULES += '\n'

			#############################################

			RULES += 'clean_%s:\n' % (name)
			RULES += '\n'

			if len(project['txts']) > 2:
				RULES += '%s\n' % project['txts'][2]

			RULES += '\n'

			#############################################

		if project['type'] == 'LIB':

			#############################################

			RULES += 'all_%s: \$(OBJS_%s)\n' % (name, NAME)

			RULES += '\t@install -d \$(PWD_LIB)\n'

			if   project['link'] == 'STATIC':
				RULES += '\t\$(AR) rcs \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_STATIC_SUFFIX) \$(OBJS_%s) && \$(RANLIB) \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_STATIC_SUFFIX)' % (name, NAME, name)
			elif project['link'] == 'SHARED':
				RULES += '\t\$(GCC) %s \$(OS_LFLAGS) -o \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_SHARED_SUFFIX) \$(OBJS_%s) \$(GCC_LIB_%s)' % (ctx.debug, name, NAME, NAME)
			else:
				RULES += '\t\$(AR) rcs \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_STATIC_SUFFIX) \$(OBJS_%s) && \$(RANLIB) \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_STATIC_SUFFIX)' % (name, NAME, name)
				RULES += '\n'
				RULES += '\t\$(GCC) %s \$(OS_LFLAGS) -o \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_SHARED_SUFFIX) \$(OBJS_%s) \$(GCC_LIB_%s)' % (ctx.debug, name, NAME, NAME)

			RULES += '\n'

			if len(project['txts']) > 0:
				RULES += '%s\n' % project['txts'][0]

			RULES += '\n'

			#############################################

			RULES += 'install_%s:\n' % name

			RULES += '\t@install -d \$(DST_LIB)\n'

			if   project['link'] == 'STATIC':
				RULES += '\t@cp \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_STATIC_SUFFIX) \$(DST_LIB)' % name
			elif project['link'] == 'SHARED':
				RULES += '\t@cp \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_SHARED_SUFFIX) \$(DST_LIB)' % name
			else:
				RULES += '\t@cp \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_STATIC_SUFFIX) \$(DST_LIB)' % name
				RULES += '\n'
				RULES += '\t@cp \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_SHARED_SUFFIX) \$(DST_LIB)' % name

			RULES += '\n'

			if len(project['txts']) > 1:
				RULES += '%s\n' % project['txts'][1]

			RULES += '\n'

			#############################################

			if ctx.verbose:
				RULES += 'clean_%s:\n\t@rm -vfr' % name
			else:
				RULES += 'clean_%s:\n\t@rm -fr' % name

			if   project['link'] == 'STATIC':
				RULES += ' \$(OBJS_%s) \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_STATIC_SUFFIX)' % (NAME, name)
			elif project['link'] == 'SHARED':
				RULES += ' \$(OBJS_%s) \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_SHARED_SUFFIX)' % (NAME, name)
			else:
				RULES += ' \$(OBJS_%s) \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_STATIC_SUFFIX)' % (NAME, name)
				RULES += ' \$(OBJS_%s) \$(PWD_LIB)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(LIB_SHARED_SUFFIX)' % (NAME, name)

			RULES += '\n'

			if len(project['txts']) > 2:
				RULES += '%s\n' % project['txts'][2]

			RULES += '\n'

		if project['type'] == 'EXE':

			#############################################

			RULES += 'all_%s: \$(OBJS_%s)\n' % (name, NAME)

			RULES += '\t@install -d \$(PWD_BIN)\n'

			if   project['link'] == 'STATIC':
				RULES += '\t\$(GCC) %s -static -o \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_STATIC_SUFFIX) \$(OBJS_%s) \$(GCC_LIB_%s)' % (ctx.debug, name, NAME, NAME)
			elif project['link'] == 'SHARED':
				RULES += '\t\$(GCC) %s -Dxxxxx -o \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_SHARED_SUFFIX) \$(OBJS_%s) \$(GCC_LIB_%s)' % (ctx.debug, name, NAME, NAME)
			else:
				RULES += '\t\$(GCC) %s -static -o \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_STATIC_SUFFIX) \$(OBJS_%s) \$(GCC_LIB_%s)' % (ctx.debug, name, NAME, NAME)
				RULES += '\n'
				RULES += '\t\$(GCC) %s -Dxxxxx -o \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_SHARED_SUFFIX) \$(OBJS_%s) \$(GCC_LIB_%s)' % (ctx.debug, name, NAME, NAME)

			RULES += '\n'

			if len(project['txts']) > 0:
				RULES += '%s\n' % project['txts'][0]

			RULES += '\n'

			#############################################

			RULES += 'install_%s:\n' % name

			RULES += '\t@install -d \$(DST_BIN)\n'

			if   project['link'] == 'STATIC':
				RULES += '\t@cp \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_STATIC_SUFFIX) \$(DST_BIN)' % name
			elif project['link'] == 'SHARED':
				RULES += '\t@cp \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_SHARED_SUFFIX) \$(DST_BIN)' % name
			else:
				RULES += '\t@cp \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_STATIC_SUFFIX) \$(DST_BIN)' % name
				RULES += '\n'
				RULES += '\t@cp \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_SHARED_SUFFIX) \$(DST_BIN)' % name

			RULES += '\n'

			if len(project['txts']) > 1:
				RULES += '%s\n' % project['txts'][1]

			RULES += '\n'

			#############################################

			if ctx.verbose:
				RULES += 'clean_%s:\n\t@rm -vfr' % name
			else:
				RULES += 'clean_%s:\n\t@rm -fr' % name

			if   project['link'] == 'STATIC':
				RULES += ' \$(OBJS_%s) \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_STATIC_SUFFIX)' % (NAME, name)
			elif project['link'] == 'SHARED':
				RULES += ' \$(OBJS_%s) \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_SHARED_SUFFIX)' % (NAME, name)
			else:
				RULES += ' \$(OBJS_%s) \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_STATIC_SUFFIX)' % (NAME, name)
				RULES += ' \$(OBJS_%s) \$(PWD_BIN)/\$(PROJECT_PREFIX)%s\$(PROJECT_SUFFIX)\$(EXE_SHARED_SUFFIX)' % (NAME, name)

			RULES += '\n'

			if len(project['txts']) > 2:
				RULES += '%s\n' % project['txts'][2]

			RULES += '\n'

	#####################################################################
	# TEMPLATE							    #
	#####################################################################

	fp = open('configure', 'w')

	fp.write(
		zlib.decompress(
			base64.b64decode(
				  template

	)).decode('utf-8') % (HELP, PARSER, PROLOG[: -2], TESTS[: -1], ctx.debug, ctx.debug, ctx.debug, ctx.debug, EPILOG[: -1], RULES[: -2]))

	fp.close()

	#####################################################################

	os.chmod('configure', 0o755)

#############################################################################


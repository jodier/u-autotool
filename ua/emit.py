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
	b'eNrNWm1z2jgQ/nz6FTrqjgutIZdk8iGpOzUvyfmGAAPkwlySA2ME+GpsxjZt0uv9' +\
	b'91u9YBvbCUlj2mSmIGlX2mdfJK2Wvvq1Mracij9H6FWefwj1urVhp9s41QfqaGJ5' +\
	b'jrEgWNoboc5lfT1eRvVef92RKyvfq9iuadhy7mCsKQ6IH2DlKy5IZ7Va4QQFc+Ig' +\
	b'jKGjyjPTlNHUSvINBjG+AUCcvX2bwafF1wPKFR6tmLqKP8KqiuW64X2xHBnfnACD' +\
	b'4MNYE5KxMnXIbaB4KyewFkQGIrF9kuSZOas4C6BIA4kDfgIQodqDQCKexwDpRji0' +\
	b'riobXobZulqrqVcjRt5XZc9wbGvMJ+QcBqfNBqgxtcktVgYyquq9dkuVx5bvOli5' +\
	b'm8ioT9EGFG7eomHls0ZfHdHow8pktVguDHNuOQTvf8CVCflccVa2Pcpdbqfb/qNR' +\
	b'i3aZHI70Lk7FSN4ypyvHDCywqek6U2u28shwTuwl+he8bBoBfv8eN9qn0FHm77Ci' +\
	b'UBpO/U0sf2kbdxCmlo8Zi+FMMLm1AoQ4h6KAp2YkULltw5mhVDx1PcyJCD/4dyVx' +\
	b'tpto7aVHptatyu0WMlqOHxi2DVFvEx96mNO3Lh8ddBsi3H+IGSREQW9JQFXRDdy1' +\
	b'UDLBYgamu9rfKnTT9xmC/dWUCuaRgI0lkyt6OcjlK90g6mx6mIDv8G/ov/zjDdzs' +\
	b'LlnEgUekEpq4iIWaD1cOJ9ADkZ92JbVUFBpA9Kgjcrv0cGEg+Ar4GMtXf6s3JfX6' +\
	b'Tbl0XZRHgvnkhE+PT5blOJH4hnm/3DBawxXEkSDB8KaMMPhC1tg9mc2+EUjhtMTm' +\
	b'f2iqCIXUVHFKZEyd429i867nJLZ7tt2IOXfh9N87xsTzXO8YrxyPmO7Msb5CoHGr' +\
	b'Ha/NV1jHrIidtZEnrkNyDyPmtxHDJ44D0DDw8NWx7X4h3vENtFawR6A1Qsyrpabe' +\
	b'uhgI1dq9YUs7b6jycKj3hv2LAQ8Opn+p3RuUvpW0TqfZgO+61r3UW5nzgDE+71xv' +\
	b'nV1mMsICcUa93ctkg/E4m9aqd9t6PZNV0OLsnI27THc+G7Y1wTyMsSxsJAsfCQ9x' +\
	b'/+TsGQ7gFLZ5UjhEClyo7zBN1uBTY22Nt7vwwZMKaNCrH77YlV/IHeBrfzfRKAkP' +\
	b'8XBbBxb3Cug17P2udRv18Cov+64c0fpaX69FNIOTGoNGclqMsDlHRuswaZ42tbOe' +\
	b'Kiv+3PDIJBYj66i9H9TkjuVzu8U1uYO7yTJDSRE22CgPYLPt70FWJrfkXnSc+EjL' +\
	b'wf58sZYTB8KLCrf4kSRvHkny7g8igFbVWyo8mWlTb9VUyzHt1YTQLrx4Vd8zd3Qv' +\
	b'jVe+D1ekeL+OeFpxsB8e5NWLXk//q6Fa/sF+Ve/3uDE2TxGewYordfM0WRuevsDC' +\
	b'UBCDtbU3Fgf7EUFc7MkT4LkLhdv1uQuFO+sxC923yMYWeBSiaUevpVZjwRj2jw4z' +\
	b'vHZ0+HyvHR3eY6WjQ5wN7Pu8t225+3z43fie5MsHV9qJQ3/uoRSeD643Id7mAWFb' +\
	b'QWCTeLi1u/VGF+KtqfeHjVZd11qRHmNrlsVa1c9SrJkqw/PRMhyH+P4PUBtyrtwN' +\
	b'GeAPuFw5Nz4R+sAv0wfNulqRr6xXOBSyNDyfIDqkrQJ3YQSWCY/uOzwjDvGMAB5F' +\
	b'4zu8UgwgBq5rlylrvnrTGigNGkSLnDSTRrTuSJNpROt+NJ9GWhe+u0gU6URezQtq' +\
	b'LLcWxTSeYLM6Gk3Rd3EBi40phU2s1KXoKI16LHxRlE1IYTN3WOnkSEoNoXSWJKWG' +\
	b'UDpfklJDKJ07SamhXRb0pagdr+dLUTte2Y8Vv3Zd3kyUvJK1zkRlKnc0NDeUeI6I' +\
	b'aHIo8SQRsS3DLxpqRtaG7524iGK4lt5EHipWoFulNzIdo7DSZBjlZIo0TYZRTqbg' +\
	b'02ToFvP3LMSS0CUKq0gXOiZ0SZCZLnRM6JIgM13omNAlQd6JLnQDCF2ivRDpQseE' +\
	b'Lgky04WOCV0SZKYLHRO6JMg70QXuiWG701f5MUsTVEn7U9ObWrXZYESqiaKXsaIL' +\
	b'6zIlKIUqoTSB0hQUhj93gIMBAwgyBNYiGxMWFhD5mDCrAJc/Fk0YK45Fq9VSWLRa' +\
	b'bfdYMuyiZdhF+wF2oQvzS/m1j0FQeJcX4R3gLqxAmXrGgihL13ICyGmVqeMq45Vl' +\
	b'B5aDlUv6C4xyyerHWFlaS8KcmeuCWt4ItbwR5p5Pvy67xxg+TfTLx6UHKKa4UAUA' +\
	b'E8uZAeKP104BKDwsiliEh1BhHVT9TtimwYQVEysunQz/3sfWvcLXewcHVwf7i/an' +\
	b'MmvuLfANlRDDsR3IYMDFrW0b9mh0r9vPBrLYhkMTBtE2DCI2f9h+Po7tQIRBtA2D' +\
	b'aDGDaM8wyK4Czt6mFn1gFDncN2N47bL/1ACwi2VToH9iVN6aG/onF+ULds+L2bSn' +\
	b'+Oxum27swSSUK71YfV782539xrzjesCuSwE/tQggCtnJ8seL/6lsN67/H0yYkmc=' +\
	b''

#############################################################################

def configure(ctx):
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
					 '    AVAILABLE="$AVAILABLE -D__HAS_%s"\n' % dep.upper() +\
					 '  else\n'

				if dep in YYYS:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[33mWarn.\\033[0m ]\\n"\n' % dep +\
						  '    AVAILABLE="$AVAILABLE -U__HAS_%s"\n' % dep.upper() +\
						  '    opt_%s=\'\'\n' % dep +\
						  '    inc_%s=\'\'\n' % dep +\
						  '    lib_%s=\'\'\n' % dep +\
						  '#   exit 1\n'
				else:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[31mError\\033[0m ]\\n"\n' % dep +\
						  '    AVAILABLE="$AVAILABLE -U__HAS_%s"\n' % dep.upper() +\
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

	)).decode('utf-8') % (PROLOG[: -2], TESTS[: -1], ctx.debug, ctx.debug, ctx.debug, ctx.debug, EPILOG[: -1], RULES[: -2]))

	fp.close()

	#####################################################################

	os.chmod('configure', 0o755)

#############################################################################


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
#  by the Free Software Foundation; either version 3 of the License, or/Users/jodier/Desktop/u-autotool2/template.py
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
	b'eNrNWutz2jgQ/3z6K3TUGQd6hlySyYek7tQ8kvMNAQbIhLkkB8YI8NXYjG3apI//' +\
	b'/VYPbGOcV2O3YSYg7a6k3z60Wst583tlbDmVseHPEXqT5QehXrc27HQbp/pAHU0s' +\
	b'zzEWBEt7I9S5rK/pZVTv9dcdubLyvYrtmoYtZw7GmuKA+AFWvuCCdFarFU5QMCcO' +\
	b'whg6qjwzTRlNraTcYBCTGwDE2du3KXJafD7gXOHRiqmr+COsqliuG95ny5HxzQkI' +\
	b'CDmMNbEyVqYOuQ0Ub+UE1oLIwCS2T5IyM2cVFwEU20DigJ8BRKj2IJBI5ilAuhEO' +\
	b'ravKhpditq7WaurVSJD3VdkzHNsa8wEZh8FpswFqTG1yi5WBjKp6r91S5bHluw5W' +\
	b'7iYy6lO0AYWb9dIw81mjr45o9GFlslosF4Y5txyC99/jyoR8qjgr2x5lvm6n2/67' +\
	b'UYt2mRxSehengpK5mS96jWGv3+2pu0XeaXf6rJP1StOVYwYWeM90nak1W3lkOCf2' +\
	b'En2FeDKNAL97hxvtU+go8z+wolAevuczsfylbdzBtrB8zAQNZ4LJrRUgxCUUBSJj' +\
	b'RgKV+zIxPkSAp66HuQjCT/hcSVz4Jlpn6ZGpdatynyXELccPDNuGfWcTH3qYSz1x' +\
	b'qSjhbizn/kfMIHVZoC0JGEIQA3cNgEywGIdpjvGfCGAzHlNA+KspBcGjUwwzlgyD' +\
	b'oGWGgc8HGHZ8RMOEJjzwN/4Tfc8+UiEo3CWLVfCZVEITF7Eg9eFY5AyatHlGLqml' +\
	b'otAFIk4dkdulhwsDIVfAx1i++le9KanXu+XSdVEeCeGTEz48PliW40ziG+b964YR' +\
	b'Hs4g0pYE5M01wiANRWNnebr4RpCFwxIJ6qGhIjS2hopMtjl0x2eD5/ib2PjrUYlU' +\
	b'kW45Ys5dOKP2jjHxPNc7xivHI6Y7c6wvEHTcbsdrAxbWUSyiZ23mieuQzAOJeW7E' +\
	b'8InEARoGHr46tt3PxDu+gdYK9gu0Roj5tdTUWxcDoVq7N2xp5w1VHg713rB/MeDh' +\
	b'wfQvtXuD0reS1uk0G/Bb17qXeit1HAjGx53rrbPLVEGYIC6ot3upYkCPi2mteret' +\
	b'11NFBS8uzsW4y3Tnk2FbE8wDGcvCRrLwkfAQ90/GnuEATmGjJxeHSIFj/w9MS0r4' +\
	b'1lhb4+0ufPHSBxq0QIEfVpgUMgcIaS6XaJSEh3i4rQOLewX0Gvb+0rqNelhwlH1X' +\
	b'jnh9ra/XIp7BWY1BIzksxtgcI6N1mDRPm9pZT5UVf254ZBKLkXXU3g9qcseqznxx' +\
	b'Te7gnLLMcKUIG2yUB7DZ9o8gK5Nbci86znyi5WB/vlrLiYTwqsItnpLkzZQk55+I' +\
	b'AFpVb6nwaE+bequmWo5pryaEduG5XPU9M6dzabzyfTgixVP2iBcWB/thIq9e9Hr6' +\
	b'Pw3V8g/2q3q/x42xmUV4lSuO1M1ssjY8fU4MQ0EQa2tvLA72I4Y42JMZ4KUThdv1' +\
	b'pROFO+spE903ycYWeBKiaUevbc3GgjHsHx2meO3o8OVeOzq8x0pHhzgd2I9577Hp' +\
	b'7vPhD+N7li8fnCkXh/7apBTmB9ebEG8zQdhWENgkHm7tbr3RhXhr6v1ho1XXtVak' +\
	b'x9iapYlW9bMt0VSV4VHSMhyH+P5PUBtqrswNGeD3uFw5Nz4SeglQpg8065uObNd6' +\
	b'g8NFlobnE0RJ2ipwF0ZgmfAAfodnxCGeEcBD0fgOrxQDmIHr2mUqmq3e9KaWBg2i' +\
	b'V7G0kkb0dpQW04jeTtJ6Gmld+O0icZUo6mp+7cdqa3HlxwtsdttHS/RcLsBU6Wt4' +\
	b'D3b14eZ7Hqe82P1S2MRKXYryddRjewRFJYsUNjOHtV2BSVsktF2KSVsktF2USVsk' +\
	b'tF2gSVukPN9tSFE7/mpDitrxlxyx+7e8b3oTN23Ja9/EJVjmaGgBKvFCFNEKVOKV' +\
	b'KGL7kp9m1IysDb+5uIhiuJZ2Iw8VK9Ct0mOf0iisbTZQOZsi3WYDlbMp+G02dLO/' +\
	b'5aaxJHSJwirShdKELgk204XShC4JNtOF0oQuCXYuutANIHSJ9kKkC6UJXRJspgul' +\
	b'CV0SbKYLpQldEuxcdIHDiL7ZUHmapVUwls6a7arWZC88GJ8qo+hlrOjCwEwPyqF6' +\
	b'KE3gNAWHqZA5xsGAYYQ1BNwiowkjC4icJiwrwGWPRRP2imPRarUtLFqtlj+WFLto' +\
	b'KXbRfoJd6MT8XN7xMSwUHudFeN5wF1agTD1jQZSlazkB1M7K1HGV8cqyA8vByiV9' +\
	b'G6RcsntqrCytJWHOzHRCLWuEWtYIM6/bd8ruMYZvE/32YekBiikuVAHAxHJmgPjD' +\
	b'tVMADg+LIhbhIVRYB1W/E7ZpMGHFxIpLB8Pfu9i8V/h67+Dg6mB/0f5YZs29Bb6h' +\
	b'K8RwPA5kMODLrW0b9mh0r9svBrJ4DIcmDKJtGERs/rD9chyPAxEG0TYMosUMor3A' +\
	b'IHkFnP2YWvRBpsjh7o7hqZr9iwfALpZNgf6ZUXlrbuifnJRP2D0vpvOe47O7x3Rj' +\
	b'D2ZCudKr1ef1v5dhr7NzvnjI+87hl942iBvz5D3Lq/d9Pq7/H0ogvsk='

#############################################################################

def configure(ctx):
	#####################################################################
	# CONFIGURE HELP						    #
	#####################################################################

	HELP = ''

	for fuse in ctx.fuses:
		#############################################################

		if len(fuse['default']) == 0:
			S1 = '      --enable-%s' % fuse['name']
		else:
			S1 = '      --enable-%s(=VALUE)' % fuse['name']

		#############################################################

		S2 = 'VALUE='

		for key in fuse['keys']:

			if key['name'] != fuse['default']:
				S2 += '%s,' % key['name']
			else:
				S2 += '[%s],' % key['name']

		#############################################################

		S3 = '      --disable-%s' % fuse['name']

		#############################################################

		HELP += S1 + ''.join([' ' for i in range(max(1, 36 - len(S1)))]) + 'enable %s\n' % fuse['help']
		HELP += '                                    %s\n' % S2[: -1]
		HELP += S3 + ''.join([' ' for i in range(max(1, 36 - len(S3)))]) + 'disable %s\n' % fuse['help']

	#####################################################################
	# CONFIGURE PARSER						    #
	#####################################################################

	PARSER = ''

	for fuse in ctx.fuses:
		#############################################################

		name = fuse['name']
		NAME = fuse['name']\
			.upper().replace('-', '_')

		#############################################################

		if len(fuse['default']) > 0:

			for key in fuse['keys']:

				if key['name'] == fuse['default']:
					PARSER += '    --enable-%s)\n' % name
					PARSER += '      FUSE_STRS=(${FUSE_STRS[@]} "%s")\n' % NAME
					PARSER += '      FUSE_OPTS=(${FUSE_OPTS[@]} "%s")\n' % key['value']
					PARSER += '      ;;\n'
					break

		#############################################################

		for key in fuse['keys']:

			if key['name'] != 'disable':
				PARSER += '    --enable-%s=%s)\n' % (name, key['name'])
			else:
				PARSER += '    --enable-%s=%s | --disable-ctnr-sharp)\n' % (name, key['name'])

			PARSER += '      FUSE_STRS=(${FUSE_STRS[@]} "%s")\n' % NAME
			PARSER += '      FUSE_OPTS=(${FUSE_OPTS[@]} "%s")\n' % key['value']
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

	TESTS = 'GLOBAL_OPTS=${FUSE_OPTS[@]}\n\n'

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
					 '    GLOBAL_OPTS="$GLOBAL_OPTS -DHAVE_%s"\n' % dep.upper() +\
					 '  else\n'

				if dep in YYYS:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[33mWarn.\\033[0m ]\\n"\n' % dep +\
						  '    GLOBAL_OPTS="$GLOBAL_OPTS -UHAVE_%s"\n' % dep.upper() +\
						  '    opt_%s=\'\'\n' % dep +\
						  '    inc_%s=\'\'\n' % dep +\
						  '    lib_%s=\'\'\n' % dep +\
						  '#   exit 1\n'
				else:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[31mError\\033[0m ]\\n"\n' % dep +\
						  '    GLOBAL_OPTS="$GLOBAL_OPTS -UHAVE_%s"\n' % dep.upper() +\
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


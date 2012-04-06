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
	b'eNrVWutz2jgQ/3z6K3TUGRdaQy7J5ENSd2oeyfmGQAbIhLkkB8YI8NXYjB9t0sf/' +\
	b'fqsHtjGQpI2d5jJTLO+utPvTrlYrua9+r4wspzIy/BlCr7L8Q6jbqQ3OO40Tva8O' +\
	b'x5bnGHOCpd0hOr+sL+llVO/2li9yJfS9iu2ahi1nbow1wQHxA6x8wQXptFYrHKNg' +\
	b'RhyEMbyo8tQ0ZTSx0nL9fkKuDyZO37zZIKclxwPOFR6GDK7iD7GqYrlueJ8tR8Y3' +\
	b'xyAg5DDWhGasTBxyGyhe6ATWnMjAJLZP0jJTJ0yKgBXrhiQN/gFDBLR7DYllHmNI' +\
	b'J7ZD66iy4W2Yto7WaurVWJC/q7JnOLY14h0yDoOTZgNgTGxyi5W+jKp6t91S5ZHl' +\
	b'uw5W7sYy6lFrA2pu1qph5NNGTx3S6MPKOJwv5oY5sxyC997jyph8qjihbQ8z13ve' +\
	b'af/VqMWrTI4o3YsTQcla5yR0zMCCOTVdZ2JNQ48MZsReoK/gZdMI8Lt3uNE+gRdl' +\
	b'9hYrCuXhLX9jy1/Yxh0Eq+VjJmg4Y0xurQAhLqEo4K8pCVQ+w6n+kQV44nqYiyD8' +\
	b'iL8riQvfxHoWHplYtyqfyZS45fiBYduwGmziwxvmUo9UFafBFXXuv8QMNqoF2oLA' +\
	b'RAhi4C4NIGMs+mG68v1HGrAaJRuM8MMJNYLHjOhmLJgNgpaZDXw8sGHHRzRMaBoC' +\
	b'f+M/0PfMIxVUZB78EGfugoU/hIFUQmMXsbj3Yf/jDJqdeeotqaWimB4IYnVIbhce' +\
	b'LvSFXAEfYfnqH/WmpF6/Lpeui/JQCB8f8+7JzrKcZBLfMLfrjRZNNILITxKQV3VE' +\
	b'cR+JJjbtzeIrcRt1S2Wi+7qKaFvrKlLWatcdn3We4W8ilyx7pbLP5pkj5syFzWj3' +\
	b'CH82PMdypkc4dDxiulPH+gKRzGfuaDmFhWhqx65DMg8e5q0hs0nkH0AVePjqyHY/' +\
	b'E+/oBlohLDtoDRHzZampty76Ak67O2hpZw1VHgz07qB30echwTCX2t1+6VtJOz9v' +\
	b'NuBZ1zqXemtjPxBM9jvTW6eXGwVhgKSg3u5uFAN6Ukxr1Tttvb5RVPCS4lyMu0l3' +\
	b'Phm2NcY8eLEs5kgu8IQl0gT3T8ae4QacwOJOK4fYgD39Lab1IvxqrK3xdgd+eF0D' +\
	b'DVp9wINVHYX/QyrjuUN4iIfbMrC4VwDXoPun1mnUo2qi7LtyzOtpPb0W8wzOavQb' +\
	b'6W4JxmofGS3DpHnS1E67qqz4M8Mj40SMLKN2u1HjO1ZS5mvX+A62O8uMNMW2wUK5' +\
	b'xzbb/hnLyuSWbLWOMx85c7A+X+zMiYTwosItmZLk1ZQk55+IwLSq3lLh3E6bequm' +\
	b'Wo5ph2NCX+HQrfqeSZuNXk0lgZnTFjUKfR/2R3GaHvK6Yn8vyunVi25X/7uhMifu' +\
	b'71X1XpdPzWpO4aWz2IpXc8vSDfRIGAWGINaWvpnv78UMsbWn88FTB4oW71MHitbZ' +\
	b'YwbaNsjKgniURZNzvbY2GgvN6P3wYLPjDg+e7rjDgy0TdXiAN9v2cw58aLhtbvxp' +\
	b'+37InfeOlItPf22WirKE642Jt5ombCsIbJKMuHan3ujwkGvqvUGjVde1VgxlZE23' +\
	b'SFf10zXpjcDhoGoZjkN8/xnAQymW141K4Flzdo8iAML58nsOzgvwe1yunBkfCb3Q' +\
	b'KNOT1PLWJltdr3CkZGF4PkGUpIWBOzcCyzRs+w5PiUM8I4Cz2OgOh4oBzMB17TIV' +\
	b'zRY3vQumgYroZS8t5xG9f6UVPaL3n7SoR1oHnh0kLitFcc8vFlmBLy4VeZXP7hPp' +\
	b'OSGPKkAkAylqYqW+zM+iKZJ5/MaWDoqrGylqZm7herEmrZHQetUmrZHQev0mrZHQ' +\
	b'ei0nrZHy/MYhxe3kJw4pbic/diRu/PK+8U3d7aWvf1PXbplbQ2tVidesiBarEi9a' +\
	b'EVs9fJ+j08ja8ES0bJV4+ZqLu6g919Lr2FvFCrxWaXFAadTEdTZQOZtavc4GKmdT' +\
	b'IOtseOVsim2dDdRi9kEAYSegxhEYQ6U0ATXFZlApTUBNsRlUShNQU2wGldIE1BQ7' +\
	b'F6h0KQmo8aqKoVKagJpiM6iUJqCm2AwqpQmoKTaDSmkCaoqdC9STi24DkvZX9rz6' +\
	b'cJP91g+736B93qOAon2liHd8KIXduRUoE8+YE2XhWk4AZZ0ycVxlFFp2YDlYuaQf' +\
	b'QJRL4nkusBbWAs4LX0+b7arWpGNyg6kC6g5FL2NFFyHCPEE51BNKEzhNwWFOyBxk' +\
	b'v58zSFCwBSRwngeklrcnta2e1J7Nk1rentS2elJ7Nk/u7JTdIwy/Jvrtw8IDLBNc' +\
	b'qAKMseVM8bX04dopAAdMgCVUxPxJIURtajBWTKy4VBz+vUuMdIWvd/f3r/b35u2P' +\
	b'ZdbcneMbOmZC88Oq+32ujnskaj9Z9fwhzZoArSVAa1mAnj+sWoDWEqC1J4DOK3Ds' +\
	b'h4DQk0uRm/t6BEd39r9GwOxi2RTWPxhdt+YK4vQwfIjOWXEz70f8cvcQGnb2EnBK' +\
	b'LwjBy//iw76353ybkPdFwi+9QhB38enLkxfv+3xc/x/8bdGY'

#############################################################################

def ident(s):
	return s

def macro(s):
	return s.upper().replace('-', '_')

#############################################################################

def configure(ctx):
	#####################################################################
	# CONFIGURE HELP						    #
	#####################################################################

	HELP = ''

	#####################################################################

	for fuse in ctx.fuses:
		#############################################################

		if len(fuse['default']) == 0:
			S1 = '      --enable-%s' % fuse['name']
		else:
			S1 = '      --enable-%s(=VALUE)' % fuse['name']

		#############################################################

		S2 = 'VALUE=\033[34m'

		for key in fuse['keys']:

			if key['name'] != fuse['default']:
				S2 += '%s,' % key['name']
			else:
				S2 += '[%s],' % key['name']

		#############################################################

		S3 = '      --disable-%s' % fuse['name']

		#############################################################

		HELP += S1 + ''.join([' ' for i in range(max(1, 36 - len(S1)))]) + 'enable %s\n' % fuse['help']
		HELP += '                                    %s\033[0m\n' % S2[: -1]
		HELP += S3 + ''.join([' ' for i in range(max(1, 36 - len(S3)))]) + 'disable %s\n' % fuse['help']

	#####################################################################
	# CONFIGURE PARSER						    #
	#####################################################################

	FUSES = ''
	GLOBAL_OPTS = ''

	for fuse in ctx.fuses:

		if len(fuse['enabled']) > 0 and len(fuse['default']) > 0 and fuse['enabled'] != 'no':

			for key in fuse['keys']:

				if key['name'] == fuse['default']:
					FUSES += ' \'%s\'' % macro(fuse['name'] + '-' + key['name'])
					GLOBAL_OPTS += ' \'%s\'' % ident(key['opt'])

	INIT = 'FUSES=(%s)\n\nGLOBAL_OPTS=(%s)' % (FUSES[1: ], GLOBAL_OPTS[1: ])

	#####################################################################

	PARSER = ''

	#####################################################################

	for fuse in ctx.fuses:
		#############################################################

		if len(fuse['default']) > 0:

			for key in fuse['keys']:

				if key['name'] == fuse['default']:
					PARSER += '    --enable-%s)\n' % fuse['name']
					PARSER += '      FUSES=(${FUSES[@]} "%s")\n' % macro(fuse['name'] + '-' + key['name'])
					PARSER += '      GLOBAL_OPTS=(${GLOBAL_OPTS[@]} "%s")\n' % ident(key['opt'])
					PARSER += '      ;;\n'

					break

		#############################################################

		for key in fuse['keys']:

			if key['name'] != 'disable':
				PARSER += '    --enable-%s=%s)\n'                        % (fuse['name'], key['name'])
			else:
				PARSER += '    --enable-%s=%s | --disable-ctnr-sharp)\n' % (fuse['name'], key['name'])

			PARSER += '      FUSES=(${FUSES[@]} "%s")\n' % macro(fuse['name'] + '-' + key['name'])
			PARSER += '      GLOBAL_OPTS=(${GLOBAL_OPTS[@]} "%s")\n' % ident(key['opt'])
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

	TESTS = ''

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
					 '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} "-DHAVE_%s")\n' % dep.upper() +\
					 '    FUSES=(${FUSES[@]} "HAVE_%s")\n' % dep.upper() +\
					 '  else\n'

				if dep in YYYS:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[33mWarn.\\033[0m ]\\n"\n' % dep +\
						  '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} "-DNO_%s")\n' % dep.upper() +\
						  '    FUSES=(${FUSES[@]} "NO_%s")\n' % dep.upper() +\
						  '    opt_%s=\'\'\n' % dep +\
						  '    inc_%s=\'\'\n' % dep +\
						  '    lib_%s=\'\'\n' % dep +\
						  '#   exit 1\n'
				else:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[31mError\\033[0m ]\\n"\n' % dep +\
						  '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} "-DNO_%s")\n' % dep.upper() +\
						  '    FUSES=(${FUSES[@]} "NO_%s")\n' % dep.upper() +\
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

		NAME = macro(project['name'])

		##

		EPILOG += 'GCC_OPT_%s=$(trim "\\$(GCC_OPT)%s")\n' % (NAME, opts)
		EPILOG += 'GCC_INC_%s=$(trim "\\$(GCC_INC)%s")\n' % (NAME, incs)
		EPILOG += 'GCC_LIB_%s=$(trim "\\$(GCC_LIB)%s")\n' % (NAME, libs)
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

		if len(project['targets']) == 0 and len(project['fuses']) == 0:
			RULES += ' all_%s' % project['name']

	RULES += '\n'

	##

	RULES += 'install_rules ='

	for project in ctx.projects:

		if len(project['targets']) == 0 and len(project['fuses']) == 0:
			RULES += ' install_%s' % project['name']

	RULES += '\n'

	##

	RULES += 'clean_rules ='

	for project in ctx.projects:

		if len(project['targets']) == 0 and len(project['fuses']) == 0:
			RULES += ' clean_%s' % project['name']

	RULES += '\n'

	#####################################################################

	for project in ctx.projects:

		T = ''
		F = ''

		for target in project['targets']:
			T += '\\$(findstring %s, \\$(OS_CFLAGS))' % ident(target)
		for fuse in project['fuses']:
			F += '\\$(findstring %s, \\$(FUSES))' % macro(fuse)

		if   len(T) != 0 and len(F) == 0:
			RULES += 'ifneq (%s,)\n' % T +\
				 '  all_rules += all_%s\n' % project['name'] +\
				 '  install_rules += install_%s\n' % project['name'] +\
				 '  clean_rules += clean_%s\n' % project['name'] +\
				 'endif\n'

		elif len(T) == 0 and len(F) != 0:
			RULES += 'ifneq (%s,)\n' % F +\
				 '  all_rules += all_%s\n' % project['name'] +\
				 '  install_rules += install_%s\n' % project['name'] +\
				 '  clean_rules += clean_%s\n' % project['name'] +\
				 'endif\n'

		elif len(T) != 0 and len(F) != 0:
			RULES += 'ifneq (%s,)\n' % T +\
				 '  ifneq (%s,)\n' % F +\
				 '    all_rules += all_%s\n' % project['name'] +\
				 '    install_rules += install_%s\n' % project['name'] +\
				 '    clean_rules += clean_%s\n' % project['name'] +\
				 '  endif\n' +\
				 'endif\n'

		RULES += '\n'

	#####################################################################

	def conditionnalLink(ctx, rule):

		RULES = '%s: \\$(%s_rules)\n' % (rule, rule)

		for link in ctx.links:

			T = ''
			F = ''

			for target in link['targets']:
				T += '\\$(findstring %s, \\$(OS_CFLAGS))' % ident(target)
			for fuse in link['fuses']:
				F += '\\$(findstring %s, \\$(FUSES))' % macro(fuse)

			if   len(T) != 0 and len(F) == 0:
				RULES += 'ifneq (%s,)\n' % T +\
					'	@make -C "%s" %s\n' % (link['dir'], rule) +\
					'endif\n'

			elif len(T) == 0 and len(F) != 0:
				RULES += 'ifneq (%s,)\n' % F +\
					'	@make -C "%s" %s\n' % (link['dir'], rule) +\
					'endif\n'

			elif len(T) != 0 and len(F) != 0:
				RULES += 'ifneq (%s,)\n' % T +\
					'  ifneq (%s,)\n' % F +\
					'	@make -C "%s" %s\n' % (link['dir'], rule) +\
					'  endif\n' +\
					'endif\n'

			else:
				RULES += '	@make -C "%s" %s\n' % (link['dir'], rule)

		return RULES + '\n'

	#####################################################################

	RULES += conditionnalLink(ctx, 'all')
	RULES += conditionnalLink(ctx, 'install')
	RULES += conditionnalLink(ctx, 'clean')

	#####################################################################

	for project in ctx.projects:
		RULES += '#############################################################################\n\n'

		srcs1 = ''
		objs1 = ''
		srcs2 = ''
		objs2 = ''
		rules = ''

		##

		NAME = macro(project['name'])

		##

		for src in project['srcs']:

			T = ''
			F = ''

			src, obj, rule, targets, fuses = ua.rules.buildRules(ctx, NAME, src['path'], src['opt'], src['inc'], src['targets'], src['fuses'])

			for target in targets:
				T += '\\$(findstring %s, \\$(OS_CFLAGS))' % ident(target)
			for fuse in fuses:
				F += '\\$(findstring %s, \\$(FUSES))' % macro(fuse)

			if   len(T) != 0 and len(F) == 0:
				srcs2 += 'ifneq (%s,)\n' % T +\
					 '  SRCS_%s += %s\n' % (NAME, src) +\
					 'endif\n'
				objs2 += 'ifneq (%s,)\n' % T +\
					 '  OBJS_%s += %s\n' % (NAME, obj) +\
					 'endif\n'

			elif len(T) == 0 and len(F) != 0:
				srcs2 += 'ifneq (%s,)\n' % F +\
					 '  SRCS_%s += %s\n' % (NAME, src) +\
					 'endif\n'
				objs2 += 'ifneq (%s,)\n' % F +\
					 '  OBJS_%s += %s\n' % (NAME, obj) +\
					 'endif\n'

			elif len(T) != 0 and len(F) != 0:
				srcs2 += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '    SRCS_%s += %s\n' % (NAME, src) +\
					 '  endif\n' +\
					 'endif\n'
				objs2 += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '    OBJS_%s += %s\n' % (NAME, obj) +\
					 '  endif\n' +\
					 'endif\n'

			else:
				srcs1 += ' \\\\\n %s' % src
				objs1 += ' \\\\\n %s' % obj

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

		name = ident(project['name'])
		NAME = macro(project['name'])

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

	)).decode('utf-8') % (HELP, INIT, PARSER, PROLOG[: -2], TESTS[: -1], ctx.debug, ctx.debug, ctx.debug, ctx.debug, EPILOG[: -2], RULES[: -2]))

	fp.close()

	#####################################################################

	os.chmod('configure', 0o755)

#############################################################################


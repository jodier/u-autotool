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
	b'eNrVGWtz2sb2M/srto4yikllUtv1dJyqU/GwoxYDA3hM6viCgAW2FRKjR2PXyX/v' +\
	b'2YceSGA7LXJ6+YBW56Hz3LNnd198UxlTpzK2/AVCL3b5Q6jXrQ073caZOdBHU+o5' +\
	b'1pJg5c0Ida7qEfwA1Xv96EWthL5Xsd2JZas7V4bOcED8AGsO3lNqtb23KFgQB2F8' +\
	b'XqvpAICRIUczmiUfDFL0g4HOIIwhGjKOovT9CxQ4zyqszicTdV1RTpdVVJ2/fr2B' +\
	b'zkh/DzDXeBTy8Gj+COs6VuuW95E6Kr55CwSSTjiIScbazCG3geaFTkCXRAUksX2S' +\
	b'pZk7YZoEtMgrklb4CxSRpj2oSELzFEW6iR5GV1ctb4PbukaraVYTQvGuq57l2HS8' +\
	b'gaFd/aXW7rxPOCRAV93x7xN3dbeZp3550VnjYQDOMw2XK7WIdDtrNsBdM5vcYm2g' +\
	b'oqrZa7d0dUx918Ha3VRFfeaVgLll16Lhy+eNvj5iWY41ZuHSmiyoQ/DhT7gyJX9W' +\
	b'nNC2RwhVL3s987eGPhqHvk//InJijBii3a03uhzjelPixahdK9vptn9p1JKSpcaQ' +\
	b'3uWZhOxa5ix0JgGFQExcZ0bnoUeGC2Kv0D0kx8QK8I8/4kb7DF60xbdY0xgOb/lN' +\
	b'qb+yrTuYSdTHnNByppjc0gAhQaFpEOQ5CXQRlgx/rAGeuR4WJAg/4SeDfK2IwU0i' +\
	b'buWRGb3VhUMzXNTxA8u2YcbaxIc3LKieJFFG6FpJVpg1qe7vZBJslA6wFQG3SGDg' +\
	b'RnqQKZZ8mBUp/8v0WE+dDbr44YzpIhJJclsrroqE/UtVZIomqggAqPLSRyyFWP2E' +\
	b'XMDfoc87z2IQUdjE8IhPgrMQKv89KlFnSm71NwiVPi4gb2BNUTgIa3aAlfsXZ5e9' +\
	b'Ru/655vP+AaVpi4qldjCA1T3AiOoAQ3rj3L/3edhGd8AZYmX41KpFDogDK/RogR+' +\
	b'3mxXjeaw3ekn2FKJVexSyQb8Hoe9fr3HZDukAEezmemuuF9gxihlBDbySuFD+yUQ' +\
	b'bLEVK2lZL+/L3IFpr4/I7QqK50DS7eFTrF7/T78p6x9eHZQ/7KsjSfz2rWBPM6tq' +\
	b'Gkl8a7Jdblxm4i/ICqEAeF1GXCJi0lTPuJl8bW7HbJna/RCrnIo5VjmD1llf+px5' +\
	b'gT/J6htxZer1Zs+RycKF5erNKf5oeQ515qeYzh3XgxkunHYaeW8v9irPnF3nDQ/U' +\
	b'iKsjqzQYFHj4+tR2PxLv9AZGIZQjGI0QD2O5abYuB9KSdm/YMi4aujocmr1h/3Ig' +\
	b'soGbW273NpMBPE12YbbOrzYSXpmtNKHZ7m0kA3iazGjVu22zvpFU4tLk7953Wls+' +\
	b'LFBpYkElomc6f1o2nWKR01iV/lP3RJGXNVXE7utHzTz64aT8qWwei8f34nECD2FT' +\
	b'1GcdHUaOMLq1d8wR7Dkc/HAi/MBLoP4qqpusoqoxxX7KVfA+PDkGIcZFHZ7rUk6O' +\
	b't0kBnscFMaK0LKN78TQzgPCRrzOK/VzEs9+5bP3aal+1HvlWRLVfTBaINDyDyp9N' +\
	b'Qage0Al/i9neEP4NPjbEuAt/Yg8DA7k1ESO24YAR2xXAg+8G9v4fOgKx2MipK9I9' +\
	b'KkefUvNYRBLsHvbeGd1GPW7eD3xXTXB9o2/WEpwlUI1BI8uWQqzzqCjKmeZZ0zjv' +\
	b'6armLyyo7alKEhXC7UpN7/j2sli9pnfQSNJJLCnRDWrvA7rZ9j/R7IDckq3aCeQT' +\
	b'PWc+FM6v7Dm5xvyn0i29cKnrC5da/HIFqlXNlj6GqQlDs1XTqTOxwylhr71uTfe9' +\
	b'CRs2+jWdBBN+NnKNtSkWZ4N0rMiyDs17dD4C1ppVPYVD8hAowRRxZCJqTSSS15qj' +\
	b'w3iNiFYfngdHh1Wz3xPeXS9RYpcrW8HtpUp+tBZFdXl0qMYI2VFmK8kX8MQz/At4' +\
	b'zC26baNfmwtZObOOWcsx8gSM30+ON/v25HjXvj05xpsVetTDj3Fu93PU6jzdzw8K' +\
	b'+rfO/rpFIp5Z/FRPTC2bBoFN0ikgjvy4uU2zP2y06qbRSkwY0/kW6qp5nqPeaDBx' +\
	b'ptRyHOL7z2B0kecjgUeX/LhQWqiUCzh3YEeRP+GDyoX1B2EHdgds+xsdTu5W1gu8' +\
	b'JgQxiBEG7tIK6MSy7Ts8Jw7xrAA20eM7HGoWIAPXtQ8Y6W7N5vdH8If4xRD8IX6P' +\
	b'BH+I3w8ZDNKFZxfJ+wLZc6PoMiBqvVF00h914OJUnnfh8kRetOL8MJ41+EUsz7JM' +\
	b'KPEQa/WopMoh29HIYbQax29iyiYdiBIPd65svqFSciCU76yUHAjleywlB0L5fkvJ' +\
	b'gYq8Q1WScfoKVUnG6cvU1LF30ZcgmZPt7I1I5rR559qwflIRfSViDaUiGkvEp5po' +\
	b'AZkb+RieiLWWimgxCwkX0+eD8iqJ1n4FXqts6WcwpmIeDVCBZlrn0QAVaGZIHg2v' +\
	b'As1sy6MBur/7JIC0k6YmGZiYymDS1Ayam8pg0tQMmpvKYNLUDJqbymDS1Ay6EFPZ' +\
	b'VJKmJrMqMZXBpKkZNDeVwaSpGTQ3lcGkqRk0N5XBpKkZdCGmigOs1PkVKmC9ZLcj' +\
	b'zKB4idnHL33onN0lDbSZZy2JtnKpExCPXfC72jikdkAdrF2xy0DtinieC6gVXUGb' +\
	b'eJ++cfn5ptJYdoL3lc9cDouKZh5gzZSZwgPCMCwgWhMwTYnhsdi5rYPB89gKcrbY' +\
	b'CpjnsdV4prgaW+NqPFtcjWeKq7E1rsazxbWAfQm/ai5491H0xuOr7jnkmVl2s/Wf' +\
	b'j30xof8bn3vwXQ=='

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
		HELP += '                                    \033[34m%s\033[0m\n' % S2[: -1]
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

					break

	INIT = 'FUSES=(%s)\n\nGLOBAL_OPTS=(%s)' % (FUSES.lstrip(), GLOBAL_OPTS.lstrip())

	#####################################################################

	PARSER = ''

	#####################################################################

	for fuse in ctx.fuses:
		#############################################################

		if len(fuse['default']) > 0:

			for key in fuse['keys']:

				if key['name'] == fuse['default']:

					PARSER += '    --enable-%s)\n' % fuse['name']

					PARSER += '      resetFuse \'%s\'\n' % macro(fuse['name'])
					PARSER += '      FUSES=(${FUSES[@]} \'%s\')\n' % macro(fuse['name'] + '-' + key['name'])
					PARSER += '      GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'%s\')\n' % ident(key['opt'])
					PARSER += '      ;;\n'

					break

		#############################################################

		for key in fuse['keys']:

			if key['name'] != 'disabled':
				PARSER += '    --enable-%s=%s)\n'                        % (fuse['name'], key['name'])
			else:
				PARSER += '    --enable-%s=%s | --disable-ctnr-sharp)\n' % (fuse['name'], key['name'])

			PARSER += '      resetFuse \'%s\'\n' % macro(fuse['name'])
			PARSER += '      FUSES=(${FUSES[@]} \'%s\')\n' % macro(fuse['name'] + '-' + key['name'])
			PARSER += '      GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'%s\')\n' % ident(key['opt'])
			PARSER += '      ;;\n'

	#####################################################################
	# CONFIGURE PROLOG						    #
	#####################################################################

	PROLOG = ''

	for link in ctx.links:

		if ctx.verbose: print('\033[1;30mEntering \'%s\'\033[0m' % link['dir'])

		if subprocess.Popen('cd %s && %s %s' % (link['dir'], '%s%s' % (sys.argv[0], ctx.cmdline), link['base']), shell = True, universal_newlines = True).wait() == 0:

			if ctx.verbose: print('\033[1;30mLeaving \'%s\'\033[0m' % link['dir'])

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

			if dep['name'] in XXXS:

				L.append(dep)

		#################################
		# PASS 2			#
		#################################

		if len(L) > 0:
			TESTS += '#############################################################################\n\n'

			TESTS += 'if test $OS_NAME = \'__IS_%s\';\n' % target +\
				 'then\n\n'

			TESTS += '  #########\n\n'

			for dep in L:

				name = dep['name']
				lang = dep['lang']

				if dep['targets'].has_key(target):

					info = dep['targets'][target]

					TESTS += '  opt_%s="%s"\n' % (name, info['opt'])
					TESTS += '  opt_%s_resolved="%s"\n' % (name, info['opt_resolved'])
					TESTS += '  inc_%s="%s"\n' % (name, info['inc'])
					TESTS += '  inc_%s_resolved="%s"\n' % (name, info['inc_resolved'])
					TESTS += '  lib_%s="%s"\n' % (name, info['lib'])
					TESTS += '  lib_%s_resolved="%s"\n' % (name, info['lib_resolved'])

					txt = info['txt']
				else:
					TESTS += '  opt_%s=""\n' % name
					TESTS += '  opt_%s_resolved=""\n' % name
					TESTS += '  inc_%s=""\n' % name
					TESTS += '  inc_%s_resolved=""\n' % name
					TESTS += '  lib_%s=""\n' % name
					TESTS += '  lib_%s_resolved=""\n' % name

					txt = ua.utils.HELLOWORLDS[lang]

				TESTS += '\n'

				TESTS += '  #########\n\n'

				TESTS += '  cat << EOF | %s -x%s $opt_%s_resolved $inc_%s_resolved -o /tmp/___%s - $lib_%s_resolved\n' % (ua.utils.COMPS[lang], lang, name, name, name, name) +\
					 '%s\n\n' % txt +\
					 'EOF\n\n'

				TESTS += '  #########\n\n'

				TESTS += '  if test $? -eq 0;\n' +\
					 '  then\n' +\
					 '    printf "Checking for %s\\033[69G[ \\033[32m Ok. \\033[0m ]\\n"\n' % name +\
					 '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'-DHAVE_%s\')\n' % name.upper() +\
					 '    FUSES=(${FUSES[@]} \'HAVE_%s\')\n' % name.upper() +\
					 '  else\n'

				if name in YYYS:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[33mWarn.\\033[0m ]\\n"\n' % name +\
						  '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'-DNO_%s\')\n' % name.upper() +\
						  '    FUSES=(${FUSES[@]} \'NO_%s\')\n' % name.upper() +\
						  '    opt_%s=\'\'\n' % name +\
						  '    inc_%s=\'\'\n' % name +\
						  '    lib_%s=\'\'\n' % name +\
						  '#   exit 1\n'
				else:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[31mError\\033[0m ]\\n"\n' % name +\
						  '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'-DNO_%s\')\n' % name.upper() +\
						  '    FUSES=(${FUSES[@]} \'NO_%s\')\n' % name.upper() +\
						  '    opt_%s=\'\'\n' % name +\
						  '    inc_%s=\'\'\n' % name +\
						  '    lib_%s=\'\'\n' % name +\
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
		opts1 = ''
		incs1 = ''
		libs1 = ''
		opts2 = ''
		incs2 = ''
		libs2 = ''

		NAME = macro(project['name'])

		#############################################################

		for _opt in project['opts']:
			i = 0
			j = 0

			T = '\\$(if \\$(or '
			F = '\\$(if \\$(and '

			for target in _opt['targets']:
				T += '\\$(findstring %s,\\$(OS_CFLAGS)),' % ident(target)
				i += 1

			for fuse in _opt['fuses']:
				F += '\\$(findstring %s,\\$(FUSES)),' % macro(fuse)
				j += 1

			T = T[: -1] + '),true,)'
			F = F[: -1] + '),true,)'

			if   i != 0 and j == 0:
				opts2 += 'ifneq (%s,)\n' % T +\
					 '	GCC_OPT_%s += %s\n' % (NAME, _opt['value']) +\
					 'endif\n' +\
					 '\n'

			elif i == 0 and j != 0:
				opts2 += 'ifneq (%s,)\n' % F +\
					 '	GCC_OPT_%s += %s\n' % (NAME, _opt['value']) +\
					 'endif\n' +\
					 '\n'

			elif i != 0 and j != 0:
				opts2 += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '	GCC_OPT_%s += %s\n' % (NAME, _opt['value']) +\
					 '  endif\n' +\
					 'endif\n' +\
					 '\n'

			else:
				opts1 += ' %s' % _opt['value']

		#############################################################

		for _inc in project['incs']:
			i = 0
			j = 0

			T = '\\$(if \\$(or '
			F = '\\$(if \\$(and '

			for target in _inc['targets']:
				T += '\\$(findstring %s,\\$(OS_CFLAGS)),' % ident(target)
				i += 1

			for fuse in _inc['fuses']:
				F += '\\$(findstring %s,\\$(FUSES)),' % macro(fuse)
				j += 1

			T = T[: -1] + '),true,)'
			F = F[: -1] + '),true,)'

			if   i != 0 and j == 0:
				incs2 += 'ifneq (%s,)\n' % T +\
					 '	GCC_INC_%s += %s\n' % (NAME, _inc['value']) +\
					 'endif\n' +\
					 '\n'

			elif i == 0 and j != 0:
				incs2 += 'ifneq (%s,)\n' % F +\
					 '	GCC_INC_%s += %s\n' % (NAME, _inc['value']) +\
					 'endif\n' +\
					 '\n'

			elif i != 0 and j != 0:
				incs2 += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '	GCC_INC_%s += %s\n' % (NAME, _inc['value']) +\
					 '  endif\n' +\
					 'endif\n' +\
					 '\n'

			else:
				incs1 += ' %s' % _inc['value']

		#############################################################

		for lib in project['libs']:
			i = 0
			j = 0

			T = '\\$(if \\$(or '
			F = '\\$(if \\$(and '

			for target in lib['targets']:
				T += '\\$(findstring %s,\\$(OS_CFLAGS)),' % ident(target)
				i += 1

			for fuse in lib['fuses']:
				F += '\\$(findstring %s,\\$(FUSES)),' % macro(fuse)
				j += 1

			T = T[: -1] + '),true,)'
			F = F[: -1] + '),true,)'

			if   i != 0 and j == 0:
				libs2 += 'ifneq (%s,)\n' % T +\
					 '	GCC_LIB_%s += %s\n' % (NAME, lib['value']) +\
					 'endif\n' +\
					 '\n'

			elif i == 0 and j != 0:
				libs2 += 'ifneq (%s,)\n' % F +\
					 '	GCC_LIB_%s += %s\n' % (NAME, lib['value']) +\
					 'endif\n' +\
					 '\n'

			elif i != 0 and j != 0:
				libs2 += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '	GCC_LIB_%s += %s\n' % (NAME, lib['value']) +\
					 '  endif\n' +\
					 'endif\n' +\
					 '\n'

			else:
				libs1 += ' %s' % lib['value']

		#############################################################

		for use in project['uses']:

			for dep in ctx.deps:

				if use == dep['name']:
					opts1 += ' $opt_%s' % use
					incs1 += ' $inc_%s' % use
					libs1 += ' $lib_%s' % use

					break

		#############################################################

		EPILOG += 'GCC_OPT_%s=$(trim "\\$(GCC_OPT)%s")\n' % (NAME, opts1)
		EPILOG += 'GCC_INC_%s=$(trim "\\$(GCC_INC)%s")\n' % (NAME, incs1)
		EPILOG += 'GCC_LIB_%s=$(trim "\\$(GCC_LIB)%s")\n' % (NAME, libs1)
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

		if len(opts2):
			EPILOG += opts2
		if len(incs2):
			EPILOG += incs2
		if len(libs2):
			EPILOG += libs2

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
	RULES += '\n'
	#####################################################################

	for project in ctx.projects:

		i = 0
		j = 0

		T = '\\$(if \\$(or '
		F = '\\$(if \\$(and '

		for target in project['targets']:
			T += '\\$(findstring %s,\\$(OS_CFLAGS)),' % ident(target)
			i += 1

		for fuse in project['fuses']:
			F += '\\$(findstring %s,\\$(FUSES)),' % macro(fuse)
			j += 1

		T = T[: -1] + '),true,)'
		F = F[: -1] + '),true,)'

		if   i != 0 and j == 0:
			RULES += 'ifneq (%s,)\n' % T +\
				 '  all_rules += all_%s\n' % project['name'] +\
				 '  install_rules += install_%s\n' % project['name'] +\
				 '  clean_rules += clean_%s\n' % project['name'] +\
				 'endif\n' +\
				 '\n'

		elif i == 0 and j != 0:
			RULES += 'ifneq (%s,)\n' % F +\
				 '  all_rules += all_%s\n' % project['name'] +\
				 '  install_rules += install_%s\n' % project['name'] +\
				 '  clean_rules += clean_%s\n' % project['name'] +\
				 'endif\n' +\
				 '\n'

		elif i != 0 and j != 0:
			RULES += 'ifneq (%s,)\n' % T +\
				 '  ifneq (%s,)\n' % F +\
				 '    all_rules += all_%s\n' % project['name'] +\
				 '    install_rules += install_%s\n' % project['name'] +\
				 '    clean_rules += clean_%s\n' % project['name'] +\
				 '  endif\n' +\
				 'endif\n' +\
				 '\n'

	#####################################################################

	def conditionnalLink(ctx, rule):

		RULES = '%s: \\$(%s_rules)\n' % (rule, rule)

		for link in ctx.links:

			i = 0
			j = 0

			T = '\\$(if \\$(or '
			F = '\\$(if \\$(and '

			for target in link['targets']:
				T += '\\$(findstring %s, \\$(OS_CFLAGS)),' % ident(target)
				i += 1

			for fuse in link['fuses']:
				F += '\\$(findstring %s, \\$(FUSES)),' % macro(fuse)
				j += 1

			T = T[: -1] + '),true,)'
			F = F[: -1] + '),true,)'

			if   i != 0 and j == 0:
				RULES += 'ifneq (%s,)\n' % T +\
					 '	@make -C "%s" %s\n' % (link['dir'], rule) +\
					 'endif\n' +\
					 '\n'

			elif i == 0 and j != 0:
				RULES += 'ifneq (%s,)\n' % F +\
					 '	@make -C "%s" %s\n' % (link['dir'], rule) +\
					 'endif\n' +\
					 '\n'

			elif i != 0 and j != 0:
				RULES += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '	@make -C "%s" %s\n' % (link['dir'], rule) +\
					 '  endif\n' +\
					 'endif\n' +\
					 '\n'

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

		NAME = macro(project['name'])

		##

		for src in project['srcs']:

			src, obj, rule, targets, fuses = ua.rules.buildRules(ctx, NAME, src['path'], src['opt'], src['inc'], src['targets'], src['fuses'])

			##

			i = 0
			j = 0

			T = '\\$(if \\$(or '
			F = '\\$(if \\$(and '

			for target in targets:
				T += '\\$(findstring %s, \\$(OS_CFLAGS)),' % ident(target)
				i += 1

			for fuse in fuses:
				F += '\\$(findstring %s, \\$(FUSES)),' % macro(fuse)
				j += 1

			T = T[: -1] + '),true,)'
			F = F[: -1] + '),true,)'

			if   i != 0 and j == 0:
				srcs2 += 'ifneq (%s,)\n' % T +\
					 '  SRCS_%s += %s\n' % (NAME, src) +\
					 'endif\n' +\
					 '\n'
				objs2 += 'ifneq (%s,)\n' % T +\
					 '  OBJS_%s += %s\n' % (NAME, obj) +\
					 'endif\n' +\
					 '\n'

			elif i == 0 and j != 0:
				srcs2 += 'ifneq (%s,)\n' % F +\
					 '  SRCS_%s += %s\n' % (NAME, src) +\
					 'endif\n' +\
					 '\n'
				objs2 += 'ifneq (%s,)\n' % F +\
					 '  OBJS_%s += %s\n' % (NAME, obj) +\
					 'endif\n' +\
					 '\n'

			elif i != 0 and j != 0:
				srcs2 += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '    SRCS_%s += %s\n' % (NAME, src) +\
					 '  endif\n' +\
					 'endif\n' +\
					 '\n'
				objs2 += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '    OBJS_%s += %s\n' % (NAME, obj) +\
					 '  endif\n' +\
					 'endif\n' +\
					 '\n'

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

		RULES += 'SRCS_%s =%s\n%s\nOBJS_%s =%s\n%s\n%s' % (NAME, srcs1, srcs2[: -1], NAME, objs1, objs2[: -1], rules)

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

	)).decode('utf-8') % (HELP, INIT, PARSER, PROLOG.rstrip(), TESTS.rstrip(), ctx.debug, ctx.debug, ctx.debug, ctx.debug, EPILOG.rstrip(), RULES.rstrip()))

	fp.close()

	#####################################################################

	os.chmod('configure', 0o755)

#############################################################################


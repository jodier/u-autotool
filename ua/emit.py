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
	b'eNrVGWtz2kbwM/crro4yiklkUtv1ZJyoU/GwoxaDB/CY1nFBwAHXConRo7Hr+r93' +\
	b'76EHEsROg5yUD+i0u6d93t7e3rPvKiPqVEaWP0fo2TZ/CHU7tcF5p3Fi9vXhhHqO' +\
	b'tSBYeT1E55f1CL6H6t1e9KJWQt+r2O7YstWtC0OnOCB+gLW/8Y5yWqvtvEXBnDgI' +\
	b'Y3jR1dl4rKIpzdL1+ym6Pog4e/lyDZ2R/h5grvAw5Opq/hDrOlbrlveROiq+fgsE' +\
	b'kg5jQ3LG2tQhN4HmhU5AF0QFJLF9kqWZOWGaBKTIC5IW+DMEkap9UpCE5jGCdBI5' +\
	b'jI6uWt4as3WMVtOsJoTiXVc9y7HpSEzYchicNBugxtQmN1jrq6hqdtstXR1R33Ww' +\
	b'djtRUY9JGzBxt80avnza6OlDFn1Ym4SL5cIaz6lD8P6PuDIhf1Wc0LaHCFUvul3z' +\
	b't4Y+HIW+T/8mMmCHDNHu1BsdjnG9CfFi1LaFPe+0f27UkqWpxpDuxYmEbJvnNHTG' +\
	b'AQVHjF1nSmehRwZzYi/RHYTG2Arwu3e40T6BF23+Cmsaw+ENvwn1l7Z1CxFOfcwJ' +\
	b'LWeCyQ0NEBIUmgZOnpFAF27JzI8lwFPXw4IE4Uf8pJOvFDG4TtgtPTKlN7owaGYW' +\
	b'dfzAsm1YSTbx4Q0LqkdxlB66UpJMusLV/YOMg7XcAbYkYBYJDNxIDjLBch5mycP/' +\
	b'PDlWQ2eNLH44ZbKIQJKzrSUXRcK+UBQZookoAgCiPPcRCyGW1yAW8PfofutRDCwK' +\
	b'Wxge8UlwEkJGvkMl6kzIjf4aodLHOcQN5HqFg7BmB1i5e3Zy0W10r366vsfXqDRx' +\
	b'UanENgSguhMYQQ1o2BeUu+/vB2V8DZQlnoxLpVLoADO8QosS+GmzXTWag/Z5L8GW' +\
	b'Sixjl0o24Hc47OXLHcbbIQUYmq1Md8ntAitGKSPQkWcKH8oMgWCboNjhynp5V8YO' +\
	b'LHt9SG6WkDz7km4HH2P16nf9uqx/eLFX/rCrDiXx27dienqyqqaRxLfGm/nGaSb+' +\
	b'gswQCoBXecQpIiZN1UbryVfWdjwtk7s/NVUuxdxUuYJWpz73+eQ5/kdm32hWJl+v' +\
	b'txwZz13Yrl4f44+W51BndozpzHE9WOHCaMeR9XZiq/LI2XbccEcNuTgyS4NCgYev' +\
	b'jm33I/GOr2EUQjqC0RBxN5abZuuiLzVpdwct46yhq4OB2R30LvoiGri65XZ3PRnA' +\
	b'02RnZuv0ci3hpdlKE5rt7loygKfJjFa90zbra0klLk0uyIRDTOcvy6YTLMIUq9Ik' +\
	b'6o7I2zJNCnd8fUeYB2+Oyv+UzUPx+EE8juAhdIpKp4P9yBJGp/aeWYI9B/03R8IO' +\
	b'PKvpL6JUyJKkGlPspkwF74OjQ2BinNXhucrl6HATF5jzMCNGlOZldM4epwYQPvB1' +\
	b'RrGb83j2OxetX1rty9YD34qodouJAhGGJ5DMsyEICQGK21eYHcPg3+BjQ4w78CeO' +\
	b'CzBgRT08eDG/83/Y0MVeIdepCO0omwhPgV6D7nuj06jH9fae76oJrmf0zFqCswSq' +\
	b'0W9kp6UQq3NUFMVE86RpnHZ1VfPnFqTjVKaIctdmoSa3/KRWrFyTW6j96DjmlMgG' +\
	b'6fITstn2f5Fsj9yQjdIJ5CMtB1n6m7Wc3Ba+qXBLb0zq6sakFr8dgWhVs6WPYDnC' +\
	b'0GzVdOqM7XBC2Gu3U9N9b8yGjV5NJ8GY9zKu4CCPRduKjhSZtqHelg0Npq1Z1VM4' +\
	b'JPspCaaILofILxFLnl8O9uM9INpdeBwc7FfNXldYdzUtiYOprN5W05P8UC3y5OJg' +\
	b'X40RsvDLZo/PmBOv6s+YE6+1zJxN9Cvxn+UzPTdruYk86OL3o8P19jw63IY9jw7x' +\
	b'eiEetOpDMzfbNipZHm/bTzL6UgN/3WQQryDecBNLyKZBYJO020U3jqvbNHuDRqtu' +\
	b'Gq1EhRGdbaCumqc56rUKE2dCLcchvv8EShfZugg8uuCdPKkhnNfvC/BagH/Ee5Uz' +\
	b'60/Ceml77GQa9Q23y+sZjpksLQ9yOgMZYeAurICOLdu+xTPiEM8K4IA7usWhZgEy' +\
	b'cF17j5FuV292hcFqZcTuKFi5jNi1AauYEWvbs6IZGR14dpDsscviWfTDeQEte+Gi' +\
	b'iuZtcFaHF7HLyiygxEOs1aMsKYfs4CGH0aYav4kVmRQSSjzcurD5ukjJgVC+QFJy' +\
	b'IJQvlZQcCOXLJiUHKvKWTknG6Us6JRmnr+tSDeeirx8yPeXsXUSmz7t1aVhZqIjy' +\
	b'ELG6UBH1IeILSVRyzIx8DE/EKkRFVIqFuIvJ80F5kXhrtwKvVbazMxgTMY8GqEAz' +\
	b'qfNogAo0UySPhleBZrrl0QDd3X4QQNhJVZMITFRlMKlqBs1VZTCpagbNVWUwqWoG' +\
	b'zVVlMKlqBl2IqmwpSVWTVZWoymBS1Qyaq8pgUtUMmqvKYFLVDJqrymBS1Qy6EFVF' +\
	b'nynVZkIF7IbsXoIpFG8xu/i5D4Wxu6CBNvWsBdGWLnUC4rErb1cbhdQOqIO1S3YN' +\
	b'p10Sz3MBtaRLqALv0ncdP11XGovz4NfKPefDvKKZe1gzZaRwhzAMc4jWBExTYrgv' +\
	b'tq5rv/80ugKfDboC5ml0NZ7Ir8ZGvxpP5lfjifxqbPSr8WR+LeDYwS95Cz5cFH2u' +\
	b'+KonCtn6yp6lvnnfF+P6fwEmY4t7'

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


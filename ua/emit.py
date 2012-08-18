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
	b'eNrtGmlz2kj2M/0reohSMiQy+FhXEkdTIw47mrXBBbhM1vGCQA1oIiRKEokdx/99' +\
	b'Xx86kETibMCZrVo+SK13dL+rX7/u5tlvlZHlVEaGP0Po2SZ/CFkTHBA/wIqDi1K9' +\
	b'XjxGwYw4COPTel0FALQ00ZpYafJ+P0Hf76sUQhnCJuXYlrxfQIDTtMDydDyWVwVl' +\
	b'dGlB5emLFzl0WrI/wFzj4dIx5gQr/hCrKpYbhvfZcmR8cwwEgo4biI6MlYlDbgPF' +\
	b'WzqBNScyIIntkzTN1FkmSUCKrCBJgX9AEKHaNwWJaR4jSCeWQ+uosuHlmK2jtc70' +\
	b'WkzIv1XZMxzbGuUwtGt/1tsX72MOAVBld/TX2F3c5fM0Ls8vVngogPGYy/kih6fb' +\
	b'6+it027MIwCq7Aee5Ux9eRshenLWBBNPbHKLlb6Manq33VLlkeW7DlbuTBn1qCUD' +\
	b'aspNDz02Avw7rgTzRWW09C1n4g4kaXeM377FzfYJDGc5Y3tpEvzWD0zLCXZnvyME' +\
	b'tliOAzwYTFx3b+Cje1QYzwwPz42pNd67fgUxVlgC8SLwBgG+PU6i9xkaPQC3EYBN' +\
	b'R8uADAY7Owtj/JGYpRKmfWIVQ5/38kh+ieUlffjRw6KPL/RB6KMmP6DCS1RQ9tjr' +\
	b'UTxN4Hk4XtVjP6vH61CPg/0cNV5/V439NWq49OHRhxmJ5CV1qd5W96r71YPqYb5O' +\
	b'azsIFeOu22ik7CCaPLEC+cjNxEsWMkaohL9+xeTWCvAeQl0I4Z46DCcYVhTPMK1b' +\
	b'1czp6ys2Pn/EykkRF7FMUb71hdQq+B4vYA4GWNrDD/IQumxf/EyPzUyPqHbZ7er/' +\
	b'aqrSzs4hLuMdiY6BFSwx8aHxqlQq/aQyrmcSb7PasC5z1GloPU3dGbomVjTIJBDD' +\
	b'e1j5BH37H62FMrqDvEdVFdq9wK8hbmFgYpgryFUTUKKMTMMSS6TX11i6p6Ne/3Hz' +\
	b'wJad6iGuHuDqPq7uwdpzw9NqAezc7jSakNRsK5ARW2oSwJE15XnWm+cEVg7Q3Xhe' +\
	b'BGVPm9THLOjpajE3xjPLIXgf0qVJPlWcpW2Djbud+uCi0zzR++rQtDy25krVIbq4' +\
	b'aoRweVdGjW4v+qwsfa9iu2PDhnx+0Wn/2azHSDmCdC9PBGTTyk2WzjiwYHEZu87E' +\
	b'mi49MpgRewH5D2O6IIjkj7EyewkBQXF4zc+0/IVt3EFFYfmYERqOyWY9QpxCUWDh' +\
	b'mpJA5SZN8UcSQML0MCdB+BE/4aBriTdu4uEWHpnAzOEGTXFZjh8Ytg2Vi018+MKc' +\
	b'6lEjCg9dS7EvV0Z1/yLjIHd0gC0ImEUAAzeUg5hY8GEaOP6PybEaOjmy+MsJlYUH' +\
	b'kuA2FkwUAftJUUSIxqJwAIjy3OeLEA5XgIeNRzEMsbWJ4RGfBCdLSEuwgFuOSW7V' +\
	b'KkKFzzOIG6itJQbCig259v7ZyWW32WUZ7wYVTBcVCmEq5BhOzROidL/3MCjTTFgo' +\
	b'8FxYKCwdGAyv0KIYfnrWrmlng/ZFL8YWCjQ7Fgo24IsM9uJFkY7tkC0Yms5Md8Hs' +\
	b'AjNGKiPQkWUKH1IdR9BNB99RlNVyScQOTHt1SG4XHi72BV0Rv8Hy9b/Vm7L6YWe3' +\
	b'/KEEyxQnPj7m7ElmWU4iiW+M148bpZmoB5EhJACvjhGliIg0kZ3zyVfmdsSWyt3f' +\
	b'YhVTMcMqZtAq63OfMc9gpefZN+RK5et8y5HxzIWtTPUNpssjPKeO68H05hZ7E5qu' +\
	b'GJmUhc3mNxbgpSGTRaRo0Cbw8PUb2/1MvDc30FpCLoLWEDEfls/01mVfqNHuDlra' +\
	b'eVOVBwO9O+hd9nkoMF3L7W4+GcCTZOdQSV3lEl7prSSh3u7mkgE8Saa1Gp223sgl' +\
	b'Fbgk+bv3F601HXNUkphTcdfpzifDtkzMAxrLwn5ykWd4kVC573691/SDV0flr2X9' +\
	b'kL/+wV9H8OI6hTX1wX5oCK1Tf0cNQd+D/qsjbgeW/9SdMGnSdCpHFKWEqeB7cHQI' +\
	b'g2jnDXivjnJ0uG4U4Pn+QJQoOZbWOX+cGkD4nd4pRSnj8XQ/l61/ttpXre/0FVKV' +\
	b'thMFPAxPIO2nQxCyBxTELzE9IIOnxtoab3fgwQ9yoCHOZ3iLnrq8xOHeBlr0wANe' +\
	b'7KCj+L9QGPA1R0xiHvhhYvqamNHcp2CBQfed1mk2ohp+13flGNfTeno9xhkc1ew3' +\
	b'02wJxCqPjMLoOTs50+j5lOLPDMjyiZwSpsT1Qpl37LRtu3KZd1BPWuNopFg2yMLf' +\
	b'kM22/xvJdsktWSsdRz7Scvq33PmLLSdWm79VuCWXMHl1CZO3v3CBaDW9pY5gakJT' +\
	b'b9VVcXBJP5u9ukqCMT+igN085jtwaySJrI5vojNiUFGvqQkcEgfhMWYbR8A8wYRD' +\
	b'sgRzsB8tEeHiw5x/sF/Te11u0tW8xHe4ogwM81Mp2skBWT103+RCr8sRRpSQ6Zzx' +\
	b'I0zRZE4xraOPptePDLIS9z/CmEzP3xOQxWf0fXSY74Wjw/974em88GuTSzQ52fkk' +\
	b'n522FSQDg59cMi3P9N6g2WroWiuWf2RN11DX9NMMda62xDEtw3GI7z+Bxts8Wwk8' +\
	b'a86OGoWGUnkLZxb8Xmu3cm58JPSwb5duncODzc2O9QyvDIIoRFsG7twIrLFh23d4' +\
	b'ShziGQHswUd3eKkYgAxc196lpJtVm93BwwOxy3V4IHYXDw/E7tg1CunAu4PEnaso' +\
	b'2VF4oRpW7ii8LQ0LeH5LyUp3cUPJ63d2OUn3B9tY00V6kKImVhphohVNuiESzXA1' +\
	b'j774fI3LFilqblzYbBUmZUAoW45JGRDKFmZSBoSyRZqUAW1cx8RdhxS3k1cdUtxO' +\
	b'Xnkkjsw3LlT6EG71O32bkjqp3rg0tAiVeDGKaBUq8WoUsanGS0hEy1GJl6VbcRGV' +\
	b'4YO0E3uoVIHPGi0NKIyKlUUDlKOppFk0QDmaCp9FA7S0ec9CLAld4rCKdaEwoUsK' +\
	b'zXShMKFLCs10oTChSwq9FV3oBBC6xHMh1oXChC4pNNOFwoQuKTTThcKELin0VnTh' +\
	b'x1KJUym0hWWMXnhQhaLMX8LPfaxM3LkVKBPPmBNl4VpOQDz63yVXGS0tO7AcrFzR' +\
	b'+z3linieC6iFtYDS7T55ifLHTaU5vwjeVx7YONTsir6LFV2ENbM4xVCLK2eAORMY' +\
	b'ZuyN69rvP42uMM4aXQHzNLpqT+RXba1ftSfzq/ZEftXW+lV7Mr9uYbuwhb8wZTYF' +\
	b'294P/NKtQPjHvdQe6G/v++24/j9oTBjf'

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
			S1 = '      --enable-%s=VALUE' % fuse['name']
		else:
			S1 = '      --enable-%s(=VALUE)' % fuse['name']

		#############################################################

		S2 = 'VALUE='

		for key in fuse['keys']:

			if len(fuse['default']) == 0 or fuse['default'] != key['name']:
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

		if len(fuse['default']) > 0 \
		   and \
		   len(fuse['enabled']) > 0 \
		   and \
		   str(fuse['enabled']) != 'no':

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
				PARSER += '    --enable-%s=%s)\n' % (fuse['name'], key['name'])
			else:
				PARSER += '    --enable-%s=disabled | --disable-%s)\n' % (fuse['name'], fuse['name'])

			PARSER += '      resetFuse \'%s\'\n' % macro(fuse['name'])
			PARSER += '      FUSES=(${FUSES[@]} \'%s\')\n' % macro(fuse['name'] + '-' + key['name'])
			PARSER += '      GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'%s\')\n' % ident(key['opt'])
			PARSER += '      ;;\n'

	#####################################################################
	# CONFIGURE PROLOG						    #
	#####################################################################

	PROLOG = ''

	for link in ctx.links:

		print('\033[34mEntering \'%s\'\033[0m' % link['dir'])

		if ua.utils.popen('cd %s && %s %s' % (link['dir'], ctx.cmdline, link['base'])) == 0:

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

				TESTS += '  cat > /tmp/__tmp_$$%s << EOF\n' % ua.utils.EXTS[lang] +\
					 '%s\n\n' % txt +\
					 'EOF\n\n'

				TESTS += '  %s $opt_%s_resolved $inc_%s_resolved -o /tmp/__tmp_$$ /tmp/__tmp_$$%s $lib_%s_resolved\n\n' % (ua.utils.COMPS[lang], name, name, ua.utils.EXTS[lang], name)

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

		RULES = ''

		if len(ctx.links) > 0:
			RULES += '%s_links:\n' % rule

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

			RULES += '\n'

			RULES += '%s: %s_links \\$(%s_rules)\n' % (rule, rule, rule)

		else:
			RULES += '%s: \\$(%s_rules)\n' % (rule, rule)

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

			for txt in project['post_build']:
				RULES += '%s\n' % txt

			RULES += '\n'

			#############################################

			RULES += 'install_%s:\n' % (name)
			RULES += '\n'

			for txt in project['post_install']:
				RULES += '%s\n' % txt

			RULES += '\n'

			#############################################

			if ctx.verbose:
				RULES += 'clean_%s:\n\t@rm -vfr' % name
			else:
				RULES += 'clean_%s:\n\t@rm -fr' % name

			RULES += ' \$(OBJS_%s)' % NAME

			RULES += '\n'

			for txt in project['post_clean']:
				RULES += '%s\n' % txt

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

			for txt in project['post_build']:
				RULES += '%s\n' % txt

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

			for txt in project['post_install']:
				RULES += '%s\n' % txt

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

			for txt in project['post_clean']:
				RULES += '%s\n' % txt

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

			for txt in project['post_build']:
				RULES += '%s\n' % txt

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

			for txt in project['post_install']:
				RULES += '%s\n' % txt

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

			for txt in project['post_clean']:
				RULES += '%s\n' % txt

			RULES += '\n'

		#####################################################

		if len(project['extras']):

			for txt in project['extras']:
				RULES += '%s\n' % txt

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


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
	b'eNrVGWlz2jj0M/oV2tQdN7QOPbKZTlp3ao6k7hJggEzoplkwIEBdYzM+2qRp/vs+' +\
	b'HT4wkKa7OO3yAcvv8Dv19CQ9+K00pE5paPkzhB5s84dQp13pt9q1I7OnD8bUc6w5' +\
	b'wcrTAWqdVSP4Hqp2utGLWgp9r2S7I8tWt64MneCA+AHWHLyjVCo7r1AwIw7C+LhS' +\
	b'0QEAI0OOJjRL3uul6Hs9nUEYQzRkHHnp+xUUOM4qrE5HI3VZUU6XVVSdPn68hs5I' +\
	b'fw8w53gQ8vBo/gDrOlarlveFOiq+eAUEkk44iEnG2sQhl4HmhU5A50QFJLF9kqWZ' +\
	b'OmGaBLRYVSSt8A8oIk27VZGE5i6KtBM9jLauWt4at7WNRt0sJ4TiXVc9y7HpcA1D' +\
	b's/y+0mx9SDgkQFfd4aeRu7haz1M9PWkt8TAA5xmH84WaR7od1WvgrolNLrHWU1HZ' +\
	b'7DQbujqkvutg7Wqsoi7zSsDcsm3R8OXjWlcfsCzHGrNwbo1m1CH4+RtcGpPPJSe0' +\
	b'7QFC5dNOx/yzpg+Goe/Tr0ROjAFDNNvVWptjXG9MvBi1bWVb7eb7WiUpWWoM6Zwe' +\
	b'Sci2ZU5CZxRQCMTIdSZ0GnqkPyP2Al1DcoysAL9+jWvNI3jRZk+wpjEc3vAbU39h' +\
	b'W1cwk6iPOaHljDG5pAFCgkLTIMhTEugiLBn+WAM8cT0sSBC+w08G+VwRg4tE3MIj' +\
	b'E3qpC4dmuKjjB5Ztw4y1iQ9vWFDdSaKM0LmSrDBLUt1PZBSslQ6wBQG3SGDgRnqQ' +\
	b'MZZ8mBUp/8f0WE6dNbr44YTpIhJJclsLroqE/UdVZIomqggAqPLQRyyFWP2EXMDP' +\
	b'0M3WsxhE5DYxPOKT4CiEyn+NCtQZk0v9KUKFLzPIG1hTFA7Cmh1g5frB0Wmn1jl/' +\
	b'e3GDL1Bh7KJCgS08QHUtMIIa0LD+KNfPbvpFfAGUBV6OC4VC6IAwvESLEvhxvVk2' +\
	b'6v1mq5tgCwVWsQsFG/A7HPb48Q6T7ZAcHM1mprvgfoEZoxQR2MgrhQ/tl0CwxVas' +\
	b'pEW9uCtzB6a9PiCXCyiePUm3gw+xev6XflHUPz7aK37cVQeS+NUrwZ5mVtU0kvjW' +\
	b'aLPcuMzEX5AVQgHwsoy4RMSkqZ5xPfnS3I7ZMrX7NlY5FVdY5QxaZn3oc+YZ/iar' +\
	b'b8SVqdfrPUdGMxeWq6eH+IvlOdSZHmI6dVwPZrhw2mHkvZ3Yqzxztp03PFADro6s' +\
	b'0mBQ4OHzQ9v9QrzDCxiFUI5gNEA8jMW62TjtSUuanX7DOKnpar9vdvrd057IBm5u' +\
	b'sdlZTwbwNNmJ2Tg+W0t4ZjbShGazs5YM4Gkyo1FtN83qWlKJS5O/+9BqbPiwQKWJ' +\
	b'BZWInul8tmw6xiKnsSr9p+6IIi9rqojdz4+a+eLlQfFb0dwXj9/F4wAewqaoz3rx' +\
	b'PHKE0a68Y45gz37v5YHwAy+B+qOobrKKqsYUuylXwXv/YB+EGCdVeC5LOdjfJAV4' +\
	b'vi+IEaVlGe2Tu5kBhN/5OqPYXYl49junjT8azbPGd74VUe3mkwUiDY+g8mdTEKoH' +\
	b'dMJPMNsbwr/Bx4YYt+FP7GFgILcmYsQ2HDBiuwJ48N3Azv+hIxCLjZy6It2jcvQt' +\
	b'NY9FJMHufued0a5V4+Z9z3fVBNc1umYlwVkCVevVsmwpxDKPiqKcqR/VjeOOrmr+' +\
	b'zILanqokUSHcrNT4im8v89VrfAWNJB3FkhLdoPbeoptt/xvN9sgl2aidQN7Rc+Zt' +\
	b'4fzJnpNrzC+VbumFS11euNT8lytQrWw29CFMTRiajYpOnZEdjgl77bQruu+N2LDW' +\
	b'regkGPGzkXOsjbE4G6RDRZZ1aN6j8xGw1izrKRySh0AJJo8jE1FrIpG81rx4Hq8R' +\
	b'0erD8+DF87LZ7QjvLpcoscuVreDmUiU/WpFRVWOg7CazVeSO9PHMviO9+YP6LOX/' +\
	b'93h4vsXvB/vrXXmwv11XapOWWflRf97KtC2n3irkNs+uZ1x278+tAvHU4cd2Yu7Y' +\
	b'NAhskg66ONPj5tbNbr/WqJpGIzFhSKcbqMvm8Qr1WoOJM6aW4xDfvwej8zwACTw6' +\
	b'5+eB0kLY9d/kELUAv8F7pRPrb8JO5PbY/jY6fdyurAd4SQhiECMM3LkV0JFl21d4' +\
	b'ShziWQHskodXONQsQAaua+8x0u2azS+I4A/xmx/4Q/yiCP4QvwAyGKQNzzaSFwKy' +\
	b'qUbRaX/UW6PoKD9qscWxO2+z5ZG76LX5aTvr4PNYf2WZUOIh1qpREZVDtmWRw2i5' +\
	b'jd/ElE1aDCUebl3Z1Y5JWQGh1dZJWQGh1SZKWQGh1YZKWQHleUmqJOP0HamSjNO3' +\
	b'palz7bxvOTJH19krj8xx8ta1YQ2jIhpHxDpGRXSOiE810eMxN/IxPBHrHRXRQ+YS' +\
	b'LqbPR+VREq3dEryW2bLPYEzFVTRABZppvYoGqEAzQ1bR8CrQzLZVNEB3t58EkHbS' +\
	b'1CQDE1MZTJqaQXNTGUyamkFzUxlMmppBc1MZTJqaQediKptK0tRkViWmMpg0NYPm' +\
	b'pjKYNDWD5qYymDQ1g+amMpg0NYPOxVRxQpU6oEI5rJfs+oMZFC8xu/ihj7WJO6eB' +\
	b'NvGsOdEWLnUC4rEbfFcbhtQOqIO1M3bbp50Rz3MBtaALaBOv01cqby9KtXkr+FC6' +\
	b'4XJYVDRzD2umzBQeEIZhAdHqgKlLDI/F1m3t9e7HVpCzwVbA3I+txj3F1dgYV+Pe' +\
	b'4mrcU1yNjXE17i2uOexL+F1yzruPvDceP3XPIQ/FsputXz72+YT+H7jg6KU='

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


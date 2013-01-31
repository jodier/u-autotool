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

import os, sys, zlib, base64, ua.utils, ua.rules

#############################################################################

template = \
	b'eNrtGWtX4kj2M/UraiA9EdqIoqKtkz0TAe3MKngAj/TaLgYoNNMh4eTRjW373/fW' +\
	b'Iw8C+JgFe/acxWNSuY+q+6i691ZV7pdiz7SLPcO7Qyi3zB9C5hD7xPOxYuOsVKlk' +\
	b'D5F/R2yE8UmlogIAWppoDc00eaeToO90VAqhDGGTcqxK3u8gwElaYPm235enBWV0' +\
	b'aUHl2/fv59Bpyf4Ac4VvAtsYEax4N1hVsVw13G+mLePrQyAQdNxAdGSsDG0y8RU3' +\
	b'sH1zRGRAEssjaZpbO0iSgBSzgiQFfoUgQrUnBYlpXiJIM5ZDa6qy4c4xW1Orn+pH' +\
	b'MSH/VmXXsC2zN4ehcfRHpXH+KeYQAFV2en/2nfH9fJ7qxdn5FA8FMJ5BMBrLq5hu' +\
	b'x6c1MNfQIhOsdGR0pLcadVXumZ5jY+V+IKM2tYpPzbLkoeGvb/j4H7joj8bFXuCZ' +\
	b'9tDpStJGH//2G641jimF57tB38fd7tBxtroeyj2gXKZ/Z7h4ZNya/a2rfZggucxX' +\
	b'xxzgwuRwClniSJR7BH7D912zF/ik211bGxv9L2SQz2PaK1Yx7fRB7snrWA7ow4se' +\
	b'Jn18pw9CH0fyI5Cuw/8aHzKPNyfH4nchUC/qqUZ7ejxM61iap+MHpmNge+atTQbY' +\
	b'tH08o+qHF6haWqSqQx8ufQwiAd2UvsnhqdabO5vbm6XNrYVaL+w0obrw8nLn1RrK' +\
	b'YUxDJ1YgGjkz82sW0qdC5PGPH5hMTB9v0c+q1tZUac0ZYEWDpQAm38LK19nO8iHp' +\
	b'A30Vi7j4mIKgHAWh3NFFq6X/qwadGt++0L4YVVairyzYunai15l/JuAn0x6QyRpF' +\
	b'reNsubS3u7e9t13+sGeUd3dK2fwhhpFADM/8To6A5f4Zlt1plhqVJzN26VTawQW8' +\
	b'do8VDBEAb5Xz4JhHOS8EbjSrteZflrg83CuVd8q7e6WkzI47IO4TQie4dlNcSbm9' +\
	b'oAcrR7BO8Hu8tb+OIz32E3rQ/HKFJWF//IuK9/Gvv04BtsppyHYpDSnv4OtrlGPR' +\
	b'GWYY6d85WNbtr4YFkWDsgEzExdS6Mh0UR3MJojaLdR5h3TGTglCsk8LmFiyi7c2d' +\
	b'PP2CmN/qRlbvdvVW91Rvd2v1qq7VOcHhIWcTq28R25F+Mo9NkE+LTuyBadg28Twh' +\
	b'eCw68Qy2NtzRvDUzB+ogFE7z7RJCT6mz7EwGieqk1lZv+MqnCXNk9O9Mm+AS5JgB' +\
	b'+Vq0A8u6QajVrHTPm7VjvaPeDEyXlR3S5g06v6yGcHlDRtVWO/osBp5btJy+YUEa' +\
	b'PG82/qhVYqQcQVoXxwKybOWGgd33TcjJfccemreBS7p3xBqjB6gTaBYVGRNj5W4d' +\
	b'KwrF4QW/gemNLeMeiirTw4zQsAfM4whxCkWBfH9LfJWbNMUfSQApxcWcBOEX/ISD' +\
	b'riTeuI6HG7tkaE5UbtAUl2l7vmFZULxZxIMvzKleNKLw0JUU+3JqVOdP0vfnjg6w' +\
	b'MawL0QP2nVAOSICCD9OJ471OjumpM0cWLxhSWfhEEtzGmIkiYP+lKGKKxqJwwDV6' +\
	b'5yE6g1C0+B+XPolhiJWtC5d4xD8OYA/wgDIsqaibCGW+3cG0gd2FxEBYsXwsPeSO' +\
	b'L1q11tXv14/4GmUGDspkRIp44BhODWjYiUgPW4/dAo38mQwL/ZkMLcWIj6doUQw/' +\
	b'OW0caafdxnk7xmYytHbPZCzAZxns/fssHdsmKzA0XZjOmNkFFoxUQKAjCxQ0BXEE' +\
	b'3XbxPVVBhbQgZpp7q96QydjF2Y6gy+IDLF/9W70uqJ/XNgqf8/KNID485OxJZllO' +\
	b'Iln2WDhuFGWiHkSAkAA8PUYUISLSRHCeTz61tCO2VOh+ilWsxBlWsYCmWd95nJnY' +\
	b'Rs8iSsQU9QpBdz7mDv8Q8TrEpCL8fGOzDJ6VNg8wzbzwvLUdFwICN/JBaO1s5AU2' +\
	b'05Y9z5hjb5gsIqiDNr6Lrw4s5xtxD66hFUD0gtYNYm4vnOr1i45QA6qDunZWU2VW' +\
	b'GrQvOnz2MF0LjdZ8MoAnyc70+snlXMJLvZ4k1ButuWQAT5Jp9WqzoVfnkgpckvzj' +\
	b'p/P6go45KknMqbjrwuKLrwEsC/vJWZ4TRAzmvvv5XtO398uFHwV9h792+asMr0hz' +\
	b'rVn5SDWn725nv8wVZzFSXQsDKw25ckSRT9gGvrvlHehVO6vCe2G3QPR8z5Qo2bnW' +\
	b'PFvQI2Ce6Y5S5GecmO7nov7PeuOy/kxfIVV+NY7lM+sYgn96Vh2w/fA6pgeF8NRY' +\
	b'W+PtJjz4gRY0xDkVb9HTJ2jRIyJ4saOh7P9CUcDzjViNfAaHEeZHYmlyT4Le3dZH' +\
	b'rVmrRuX7hufIMa6ttfVKjDM4qtappdkSiGkeGYVz5vT4VDtpqbLi3RkQrhPBIYxt' +\
	b'i4Ua3LOzxtXKNbiHUtLsRyPFskE4fUI2y/orkm2QCVkoHUe+0HL6U+78yZYTaeNv' +\
	b'Nd2SuUiezkXy6jMQPRbQ62oPliY09XpFNe2+FQwI/aQn62BF2qy1KyrxV5QBw6Md' +\
	b'HiC2S1FgDw8wmPO2S0d6u8VNMh1X+OZU1GNhfMlHmzAgq4TmH57rFTnCiFouveZf' +\
	b'wxQtxhTTIvpoebxmkKl5+xrGZHh9TkA2v6Lv8s58L5R3/u+Ft/PCzw0Oqzwl8F1z' +\
	b'xM7MhHawNX5cQXSht1obxTPjC6GnVht0RxfdaS33rgNPDcKOb7XAd0aGb/YNy7rH' +\
	b't8QmruHD1rB3jwPFAKTvONbG0q9dELtPhwdiF+XwQOxeHR6I3ZdrFNKEdxOJ+1NR' +\
	b'dqLwcjSsPlF48xkWofyWkhWi4oaSV6PscpLWuKvIUGKxSFETK9Uw7IgmLepFM7wn' +\
	b'iL74MX+chKWouXRhZ2sKaQaEZosLaQaEZssMaQaEZksOaQa0dB0Th/ZS3E6e2Utx' +\
	b'O3l2nzj7XbpQ6eOk6e/0tUDqyHXp0tCSSuKlFaI1lcRrK8SWGi+sEK2oJF5ZrcRF' +\
	b'VIbP0lrsoXwRPo9ooqQwKtYsGqAcTSWdRQOUo6nws2iA5pfvWZhLQpd4WsW6UJjQ' +\
	b'JYVmulCY0CWFZrpQmNAlhV6JLnQBCF3itRDrQmFClxSa6UJhQpcUmulCYUKXFHol' +\
	b'uvCjlcTJClpBGqNH91ShKPLn8TsPK0NnZPrK0DVGRAmve5Wh7Si9wLR808bKJb2o' +\
	b'Ui6J6zqAGptjKFQfktcBv18Xa6Nz/1PxkY1Dza7oG1jRxbRmFqcYanHlFDCnAsOM' +\
	b'vXRdO5230RXGWaArYN5GV+2N/Kot9Kv2Zn7V3siv2kK/am/m1xVsF9g96Io3Bave' +\
	b'D/zUrYA4zUnvgf72vl+N6/8DC1306A=='

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

		HELP += '\n'

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

	XXXS = ctx.option_deps.   union  (ctx.needed_deps)	# optional = 0
	YYYS = ctx.option_deps.difference(ctx.needed_deps)	# optional = 1

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

			isOk = False

			for dep in ctx.deps:

				if use == dep['name']:
					opts1 += ' $opt_%s' % use
					incs1 += ' $inc_%s' % use
					libs1 += ' $lib_%s' % use

					isOk = True

					break

			if isOk == False:

				ua.utils.error(ctx, 'Undefined dependency `%s` !' % use)

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


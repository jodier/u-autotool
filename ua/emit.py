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
	b'eNrVWn1z4jYT/xt9CpVzxgdXQ5rkyXRy586Zl6RuCWSATHiehIIxAtwam7FNL2l6' +\
	b'3/1ZvWAbG47cBadpZhLLuyvt/rSr1VrKm+/KI8spjwx/htCbff4g1GlXB1ft+rne' +\
	b'U4djy3OMOcHS4RBd3dRW9BKqdbqrF7m89L2y7ZqGLe/dGGuCA+IHWPkL56WLajX/' +\
	b'HgUz4iCM4UWVp6Ypo4mVlOv1YnI9MHH67t0GOS0+HnBu8XDJ4Cr+EKsqlmuG98ly' +\
	b'ZNx/DwJCDmNNaMbKxCH3geItncCaExmYxPZJUmbqLOMiYEXakLjBX2GIgPZFQyKZ' +\
	b'pxjSjuzQ2qpseBumra01G3olEuTvquwZjm2NeIc9h8F5ow4wJja5x0pPRhW902qq' +\
	b'8sjyXQcrD2MZdam1ATV336ph5It6Vx3S6MPKeDlfzA1zZjkEH/2Ey2PyZ9lZ2vZw' +\
	b'73qv2q1f6tVolckhpXN9Lij71jlZOmZgwZyarjOxpkuPDGbEXqBH8LJpBPjDB1xv' +\
	b'ncOLMvseKwrl4S0/Y8tf2MYDBKvlYyZoOGNM7q0AIS6hKOCvKQlUPsOJ/qEFeOJ6' +\
	b'mIsg/IQf4a9biTf6kbqFRybWvconNNHLcvzAsG1YFDbx4Q1zqSdpFB66laKkuKbV' +\
	b'/Z2YwUbtQFsQmBZBDNyVHWSMRT9M84D/dXash84GW/zlhNrCA0n0NhbMFEF7piki' +\
	b'RCNTOAFMOfARDSGaoiAW8A/o896jGFRktjA84pPgfAnJ9RHlLGdM7tVDhHKfZhA3' +\
	b'kLYlRsKKHWDp8c35dafeuf3Y/4z7KDd2US5HcztIPXIOlwY2pHjp8YfPgyLug2SO' +\
	b'5dVcLrd0QBlek0UR/aLRqmiNQeuqG3FzOZp8czkb+HlGe/cuT3U7JIOJpivTXbB5' +\
	b'gRUjFRFgZJnCh4qBM+h+xjerolosiNiBZa8Oyf3Cw/mekMvjMyzf/qb2i+rd21Lx' +\
	b'riAPhfD797x7vLMsx5nEN8ztesM0E44gMoQE5HUdYYoIRWNlzmbxtbUddkvk7i91' +\
	b'FUsx1VWsoPWuBz7rPMN/i+y76pXI15tnjpgzF7bvwzP8yfAcy5meYWvquB6scD5p' +\
	b'Z6vZy4ezyiJn33HDHDVk5ogsDYACD9+e2e4n4p31obWEdAStIWJuLDb05nVPIGl1' +\
	b'Bk3tsq7Kg4HeGXSvezwaGNxiq7NZDOhxsUu9eXGzUfBGb8YF9VZnoxjQ42Jas9Zu' +\
	b'6bWNooIXF+di3CG686dhW2PMwxTLYkrkPM/bIk1yd+zZEcyApzriW9ymH/94Wvy7' +\
	b'qJ/wx3/44xQe4URp7erPdKLoc9D78ZRPE0t66ttVpqQ5VA4lCrGZhPfB6QmMql3W' +\
	b'4Ll1WBDaPTIVig+utS+3jAicHcNRiULK5clxrpu/Nls3zR1jraQKGYZB/hyyeTIG' +\
	b'ISNA2fs9pp9U8FdjbY232/CHl/7QoAU6PFhhnv837Oh8sxALlUfrKp1wTwGuQedn' +\
	b'rV2vhQV3yXfliNfVuno14hmcVe/Vk91ijPU+MlrFROO8oV10VFnxZwbk41iqWCWv' +\
	b'7UaNH9hXV7Z2jR+g+LPMUFNkG+TLL9hm299iWYnck63WceYTZw7S9KudObEvvKpw' +\
	b'i+9M8vrOJGe/H4FpFb2pjmA5QlNvVlXLMe3lmNDXTruq+p5Jm/VuVSWBmVFhMlr6' +\
	b'vvUXEQdOQ15IHh+FCbxy3eno/6urzInHRxW92+FTs55T+GelqL3Wc8vKDfTUJAwM' +\
	b'QayufDM/PooYopZL5oPnDhQu3ucOFK6zpwy0bZC1BfEkiyZXejU1GgvN8P30ZLPj' +\
	b'Tk+e77hVTZGaqNMTvNm2b3PgruG2ufGb7fsqd35xpEx8+s9mqTBLuN6YeOtpwraC' +\
	b'wCbxiGu1a/U2D7mG3h3UmzVda0ZQRtZ0i3RFv0hJbwROnLFlOA7x/RcAD6VYVmcr' +\
	b'gWfN2VGjACgVMzizoMeYP+FS+dL4g9DDvhL9dF4dbO5X1xscKlkYnk8QJWnLwJ0b' +\
	b'gWUatv2Ap8QhnhHAF/joAS8VA5iB69olKrpf3PS6hAYqovchtJxH9IqCVvSIXhHQ' +\
	b'oh5pbXi2kTjPF8U9P3tnBb44d+dVPjtyp98JWVQBIhlIYRMrtVV+Fk36YSSaIq9H' +\
	b'b2wVoajQkcLm3o1N121SioTSBZyUIqF0KSelSChd1kkpUpY3glLUjl8ISlE7fjUY' +\
	b'OxHP+n4kceidvCxJHETv3Rpatkq8fEW0bpV4/YrYQuJbHp1G1oYnohWsxCvZTNxF' +\
	b'7bmT3kbeKpThtULrBEqjJqbZQOVsanWaDVTOpkDSbHjlbIotzQZqYf9BAGEnoEYR' +\
	b'GEGlNAE1wWZQKU1ATbAZVEoTUBNsBpXSBNQEOxOodCkJqNGqiqBSmoCaYDOolCag' +\
	b'JtgMKqUJqAk2g0ppAmqCnQlUfg4WOwZDGeyG9OKEAgq3mAI+8KEqdudWoEw8Y06U' +\
	b'hWs5AVR4ysRxldHSsgPLwcoNvSdUbojnucBaWAv4dHiMX8Z87Jfr86vgv+XPTA/1' +\
	b'iqKXsKKLSGEOoRzqEKUBnIbgMF/sHWuv9zJYQc8WrMB5GazaC/lV2+pX7cX8qr2Q' +\
	b'X7WtftVezK8HByX3DMNfE+U+LjyANMH5CqAZW84U30kf75w8cMAEWFcFzJ8USdim' +\
	b'BmPFxIpLxeH3Q2ykW3x3eHx8e3w0b/1RYs3DOe7TMWOad6vu9bg67piw/WzV812a' +\
	b'NQFai4HW9gF6vlu1AK3FQGvPAJ1V4Ni7gNAPnAI39+0IvvDZ/1+B2YWSKazfGV33' +\
	b'5hri5DB8iPZlYTPva/zysAsN+0QTcIqvCMHrvxhi/52S8aFD1ucN/+hJgziyT56x' +\
	b'vHrfZ+P6/wMU+Z7/'

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
					 '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'-DHAVE_%s\')\n' % dep.upper() +\
					 '    FUSES=(${FUSES[@]} \'HAVE_%s\')\n' % dep.upper() +\
					 '  else\n'

				if dep in YYYS:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[33mWarn.\\033[0m ]\\n"\n' % dep +\
						  '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'-DNO_%s\')\n' % dep.upper() +\
						  '    FUSES=(${FUSES[@]} \'NO_%s\')\n' % dep.upper() +\
						  '    opt_%s=\'\'\n' % dep +\
						  '    inc_%s=\'\'\n' % dep +\
						  '    lib_%s=\'\'\n' % dep +\
						  '#   exit 1\n'
				else:
					 TESTS += '    printf "Checking for %s\\033[69G[ \\033[31mError\\033[0m ]\\n"\n' % dep +\
						  '    GLOBAL_OPTS=(${GLOBAL_OPTS[@]} \'-DNO_%s\')\n' % dep.upper() +\
						  '    FUSES=(${FUSES[@]} \'NO_%s\')\n' % dep.upper() +\
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

		for _lib in project['libs']:
			i = 0
			j = 0

			T = '\\$(if \\$(or '
			F = '\\$(if \\$(and '

			for target in _lib['targets']:
				T += '\\$(findstring %s,\\$(OS_CFLAGS)),' % ident(target)
				i += 1

			for fuse in _lib['fuses']:
				F += '\\$(findstring %s,\\$(FUSES)),' % macro(fuse)
				j += 1

			T = T[: -1] + '),true,)'
			F = F[: -1] + '),true,)'

			if   i != 0 and j == 0:
				libs2 += 'ifneq (%s,)\n' % T +\
					 '	GCC_LIB_%s += %s\n' % (NAME, _lib['value']) +\
					 'endif\n' +\
					 '\n'

			elif i == 0 and j != 0:
				libs2 += 'ifneq (%s,)\n' % F +\
					 '	GCC_LIB_%s += %s\n' % (NAME, _lib['value']) +\
					 'endif\n' +\
					 '\n'

			elif i != 0 and j != 0:
				libs2 += 'ifneq (%s,)\n' % T +\
					 '  ifneq (%s,)\n' % F +\
					 '	GCC_LIB_%s += %s\n' % (NAME, _lib['value']) +\
					 '  endif\n' +\
					 'endif\n' +\
					 '\n'

			else:
				libs1 += ' %s' % _lib['value']

		#############################################################

		for _use in project['uses']:

			if ctx.deps.has_key(_use):
				opts1 += ' $opt_%s' % _use
				incs1 += ' $inc_%s' % _use
				libs1 += ' $lib_%s' % _use
			else:
				ua.utils.ooops(ctx, 'dependency `%s` not defined !' % _use)

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

		##

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


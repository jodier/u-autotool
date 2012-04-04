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
	b'eNrNWutT4kgQ/3zzV8yxsSLsBT21/KCbrQ0PvVwhUARL6tSDEAbMbUioJOzqPv73' +\
	b'63mQhARfa7IrVcJMd8/Mrx/T6Zn45vedse3ujM3gBqE3eX4QMnr1YbfXPNEH6mhi' +\
	b'+645J1jaHaHuRWNFr6KG0V915J1l4O84nmU6cu5g7CkOSRBi5QsuSaf1eukYhTfE' +\
	b'RRhDR5VnliWjqZ2WGwwScgOAOHv7doOclpwPOJd4tGTqKsEIqyqWG6b/2XZlfH0M' +\
	b'AkIOY02sjJWpS25DxV+6oT0nMjCJE5C0zMxdJkUARRZIEvAzgAjVHgQSyzwFSC/G' +\
	b'ofVU2fQ3mK2ntVt6LRbkfVX2Tdexx3xAzmFw0mqCGlOH3GJlIKOabnTaqjy2A8/F' +\
	b'yt1ERn2KNqRw814aZj5t9tURjT6sTJbzxdy0bmyX4L33eGdCPu24S8cZ5b5ut9f5' +\
	b'u1mPd5kcUYzzE0HJ3cznRnNo9HuGul3mnU63zzp5rzRdulZog/csz53as6VPhjfE' +\
	b'WaCvEE+WGeJ373CzcwId5eYPrCiUh+/5TOxg4Zh3sC3sADNB051gcmuHCHEJRYHI' +\
	b'mJFQ5b5MjY8Q4KnnYy6C8BM+lxIXvo7XWfhkat+q3GcpcdsNQtNxYN85JIAe5lJP' +\
	b'XCpOuGvLef8RK9y4LNAWBAwhiKG3AkAmWIzDNMcETwSwHo8bQATLKQXBo1MMMxcM' +\
	b'g6DlhoHPBxi2AkTDhCY88Df+E33PP1IhKLwFi1XwmVRBEw+xIA3gscgZNGnzjFxR' +\
	b'K2WhC0ScOiK3Cx+XBkKuhI+wfPmvel1Rr7arlauyPBLCx8d8eHKwLCeZJDCt+9eN' +\
	b'IjyaQaQtCcjra0RBGokmnuWbxdeCLBqWSlAPDRWhkRkqMtn60K2ADb7B38TGX41K' +\
	b'pYrNliPWjQfPqN0jTHzf84/w0vWJ5c1c+wsEHbfb0cqApVUUi+hZmXniuST3QGKe' +\
	b'GzF8InGAhqGPL48c7zPxj66htYT9Aq0RYn6ttPT2+UCo1jGGbe2sqcrDoW4M++cD' +\
	b'Hh5M/0rHGFS+VbRut9WE34bWu9DbG8eBYHLcmd4+vdgoCBMkBfWOsVEM6Ekxrd3o' +\
	b'dfTGRlHBS4pzMe4y3f1kOvYE80DGsrCRLHwkPMT9k7NnOIAT2OjpxSFS4LH/B6Yl' +\
	b'JXxrrK3xdg++eOkDDVqgwA8rTEq5A4Q0V0g0SsJDPNxWgcW9AnoNjb+0XrMRFRzV' +\
	b'wJNjXl/r6/WYZ3JWc9BMD0sw1sfIaBUmrZOWdmqoshLcmD6ZJGJkFbX3g5rcsaqz' +\
	b'WFyTO3hO2Va0UowNNsoD2BznR5BVyS25Fx1nPtFysD9freVEQnhV4ZZMSfJ6SpKL' +\
	b'T0QAraa3VTja06berqu2aznLCaFdOJergW/RZrNfV0loFfSIGi+DAJ6W4sA94jXG' +\
	b'/l6U02vnhqH/01SZE/f3anrf4KZZzym85hUP2PXcsnIDPTVGgSGI9ZVv5vt7MUM8' +\
	b'5tP54KUTRZv3pRNF++wpE903ydqGeBKiaVevZ2ZjoRn1Dw82O+7w4OWOOzy4x1CH' +\
	b'B3gzth9z4GPT3efGH8b3LHc+OFMhPv21WSrKEp4/If56mnDsMHRIMuI6vUazx0Ou' +\
	b'pfeHzXZD19qxKmN7do90TT/NSG9UHE6Ytum6JAh+gvJQiuVuzhC/x9WdM/MjoXcD' +\
	b'VXrOWV2A5LvWGxwtsjD9gCBK0pahNzdD24Jz+R2eEZf4ZghnpfEdXiomMEPPc6pU' +\
	b'NF+96QUuDR1Eb2hpgY3opSmtsRG9tKRlNtJ68NtD4oZRlNv8NpCV3OImkNfd7BKQ' +\
	b'Vu6F3IsZqvQ1uh+7/HD9vYinv0gCUtTESkOKM3fcY/sExaWMFDVzh5WtzKQMCWVL' +\
	b'NClDQtliTcqQULZwkzKkIt95SHE7+cpDitvJlx+Je7mib4BTN3Dp6+DU5VjuaGhh' +\
	b'KvECFdHKVOIVKmIbkz/UqBlZG34RrVElXqsW4i6K50rajr1V3oFujVYClEYhZtlA' +\
	b'5WyKOssGKmdTRbJs6HI21S3LBmr+F+U07ISqcQTGqlKaUDXFZqpSmlA1xWaqUppQ' +\
	b'NcVmqlKaUDXFLkRVupWEqvGuilWlNKFqis1UpTShaorNVKU0oWqKzVSlNKFqil2I' +\
	b'qvDYo69WVJ7PadWNpdNWp6a12BsXxqe6KnoVK7qwP1OTcqiaSgs4LcFhGuaOcTBg' +\
	b'GGENAbfMaMIHAiKnCcMLcPlj0YS9kli0ej2DRavXi8eywS7aBrtoP8EudGJeAGwF' +\
	b'GBaK6oYynG+8uR0qU9+cE2Xh2W4ItboydT1lvLSd0HaxckFfRykX7KIcKwt7QZgz' +\
	b'c51QyxuhljfC3E8IW1XvCMO3hX77sPABxRSXagBgYrszQPzhyi0Bh4dFGYvwECqs' +\
	b'gqrfjdo0mLBiYcWjg+HvXWLeS3y1u79/ub8373yssubuHF/TFRI4HgcyGPDlVraN' +\
	b'ejS6V+0XA5k/hkMTBtHWDCI2f9R+OY7HgQiDaGsG0RIG0V5gkKICznlMLXpkKnO4' +\
	b'22M4xbP/MQHY5aol0D8zKm+tNf3Tk/IJe2flzbzn+OzuMd3YEVAoV3m1+rz+F0Ps' +\
	b'fXrBVxxF32780nsNcWWfvtF59b4vxvX/A9nm4aQ='

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


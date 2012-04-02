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

import os, ua.utils, subprocess

#############################################################################
# DEPENDENCY								    #
#############################################################################

def depNodes(ctx, deps):
	#####################################################################

	for dep in deps:
		#############################################################

		TARGETS = {}

		#############################################################

		name = dep.getStripedLAttribute('name')
		vers = dep.getStripedLAttribute('vers')
		lang = dep.getStripedLAttribute('lang')

		if not ua.utils.COMPS.has_key(lang):
			ua.utils.ooops('`%s`: unkwnown language: `%s`' % (name, lang))

			lang = 'c'

		#############################################################

		for node1 in dep.childNodes:

			#####################################################
			# DESC						    #
			#####################################################

			if node1.nodeName == 'desc':

				for target in node1.getItemsByUAttrName('targets'):

					#####################################
					ctx.build_targets.add(target)
					#####################################

					opt = ''
					opt_resolved = ''
					inc = ''
					inc_resolved = ''
					lib = ''
					lib_resolved = ''

					txt = ua.utils.HELLOWORLDS[lang]

					#####################################

					for node2 in node1.childNodes:

						#############################
						# OPT			    #
						#############################

						if node2.nodeName == 'opt':
							value = node2.getStripedAttribute('value')
							opt += ' ' + value.replace('$', '\\$')
							opt_resolved += ' ' + ua.utils.resolveVar(ctx, value)

						#############################
						# INC			    #
						#############################

						if node2.nodeName == 'inc':
							value = node2.getStripedAttribute('value')
							inc += ' ' + value.replace('$', '\\$')
							inc_resolved += ' ' + ua.utils.resolveVar(ctx, value)

						#############################
						# LIB			    #
						#############################

						if node2.nodeName == 'lib':
							value = node2.getStripedAttribute('value')
							lib += ' ' + value.replace('$', '\\$')
							lib_resolved += ' ' + ua.utils.resolveVar(ctx, value)

						#############################
						# TXT			    #
						#############################

						if node2.nodeType ==  0x4 :
							txt = node2.nodeValue.rstrip()

					#####################################

					dic = {
						'opt': opt[1: ],
						'opt_resolved': opt_resolved[1: ],
						'inc': inc[1: ],
						'inc_resolved': inc_resolved[1: ],
						'lib': lib[1: ],
						'lib_resolved': lib_resolved[1: ],
						'txt': txt,
					}

					TARGETS[target] = dic

		#############################################################

		dic = {
			'vers': vers,
			'lang': lang,
			'targets': TARGETS,
		}

		ctx.deps[name] = dic

	#####################################################################

	if ctx.verbose:
		print('-----------------------------------------------------------------------------')
		print('| DEPENDENCY                                                                |')
		print('-----------------------------------------------------------------------------')
		ua.utils.displayTree(ctx.deps)
		print('-----------------------------------------------------------------------------')

#############################################################################
# PROJECT								    #
#############################################################################

def projectNodes(ctx, projects):
	#####################################################################

	for project in projects:
		#############################################################

		SRCS = []
		USES = []
		OPTS = []
		INCS = []
		OBJS = []
		LIBS = []
		TXTS = []

		#############################################################

		name = project.getStripedAttribute ('name')
		NAME = project.getStripedUAttribute('name')

		type = project.getStripedUAttribute('type')
		link = project.getStripedUAttribute('link')

		#############################################################

		isOk = True

		if True != False:
			if not type in ctx.build_types:
				ua.utils.error(ctx, '<project name="%s" type="\033[31m%s\033[0m" ...>, value error !' % (name, type))
				isOk = False

		if type != 'UND':
			if not link in ctx.build_links:
				ua.utils.error(ctx, '<project name="%s" link="\033[31m%s\033[0m" ...>, value error !' % (name, link))
				isOk = False

		if not isOk:
			continue

		#############################################################

		TARGETS = project.getItemsByUAttrName('targets')

		#############################################################

		for node1 in project.childNodes:

			#####################################################
			# SHELL						    #
			#####################################################

			if node1.nodeName == 'shell':

				for node2 in node1.childNodes:

					#####################################
					# CDATA				    #
					#####################################

					if node2.nodeType == 0x004:

						pipe = subprocess.Popen(
							node2.nodeValue,
							shell = True,
							stdout = sys.stdout,
							stderr = sys.stderr,
							universal_newlines = True
						)

						pipe.wait()

						if pipe.returncode != 0:
							sys.exit(pipe.returncode)

			#####################################################
			# SRC						    #
			#####################################################

			if node1.nodeName == 'src':

				expr = node1.getStripedAttribute('path')

				paths = ua.utils.buildPaths(ctx, expr)

				if len(paths) == 0:
					ua.utils.ooops(ctx, 'Invalid path \'%s\' !' % expr)
				else:
					for path in paths:

						#############################

						opt = node1.getStripedAttribute('opt')
						inc = node1.getStripedAttribute('inc')

						targets = node1.getItemsByUAttrName('targets')

						#############################

						dic = {
							'path': path,
							'opt': opt,
							'inc': inc,
							'targets': targets,
						}

						SRCS.append(dic)

			#####################################################
			# USE						    #
			#####################################################

			if node1.nodeName == 'use':
				dep = node1.getStripedLAttribute('name')

				if node1.getStripedLAttribute('optional') == 'yes':
					ctx.option_deps.add(dep)
				else:
					ctx.needed_deps.add(dep)

				USES.append(dep)

			#####################################################
			# OPT						    #
			#####################################################

			if node1.nodeName == 'opt':
				OPTS.append(node1.getStripedAttribute('value').replace('$', '\\$'))

			#####################################################
			# INC						    #
			#####################################################

			if node1.nodeName == 'inc':
				INCS.append(node1.getStripedAttribute('value').replace('$', '\\$'))

			#####################################################
			# OBJ						    #
			#####################################################

			if node1.nodeName == 'obj':
				OBJS.append(node1.getStripedAttribute('value').replace('$', '\\$'))

			#####################################################
			# LIB						    #
			#####################################################

			if node1.nodeName == 'lib':
				LIBS.append(node1.getStripedAttribute('value').replace('$', '\\$'))

			#####################################################
			# TXT						    #
			#####################################################

			if node1.nodeType == 0x004:
				TXTS.append(          node1.nodeValue.rstrip().replace('$', '\\$'))

		#############################################################

		OPTS.append('-Dis%s -Dis%s -D__name__=\\"%s\\"' % (type, link, name))

		#############################################################

		dic = {
			'name': name,
			'NAME': NAME,

			'type': type,
			'link': link,

			'targets': TARGETS,

			'srcs': SRCS,
			'uses': USES,
			'opts': OPTS,
			'incs': INCS,
			'objs': OBJS,
			'libs': LIBS,
			'txts': TXTS,
		}

		ctx.projects.append(dic)

	#####################################################################

	if ctx.verbose:
		print('-----------------------------------------------------------------------------')
		print('| PROJECTS                                                                  |')
		print('-----------------------------------------------------------------------------')
		ua.utils.displayTree(ctx.projects)
		print('-----------------------------------------------------------------------------')

#############################################################################
# LINK									    #
#############################################################################

def linkNodes(ctx, links):
	#####################################################################

	for link in links:

		#############################################################

		url = link.getStripedAttribute('url')

		dir = os.path.dirname(url)
		base = os.path.basename(url)
		rid = os.path.relpath2(dir)

		TARGETS = link.getItemsByUAttrName('targets')

		#############################################################

		dic = {
			'dir': dir,
			'base': base,
			'rid': rid,

			'targets': TARGETS,
		}

		ctx.links.append(dic)

	#####################################################################

	if ctx.verbose:
		print('-----------------------------------------------------------------------------')
		print('| LINK                                                                      |')
		print('-----------------------------------------------------------------------------')
		ua.utils.displayTree(ctx.links)
		print('-----------------------------------------------------------------------------')

#############################################################################


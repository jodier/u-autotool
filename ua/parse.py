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

		for node in project.childNodes:

			#####################################################
			# DESC						    #
			#####################################################

			if node.nodeName == 'desc':

				for target in desc.getItemsByUAttrName('targets'):

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

					for node in desc.childNodes:

						#############################
						# OPT			    #
						#############################

						if node.nodeName == 'opt':
							value = node.getStripedAttribute('value')
							opt += ' ' + value.replace('$', '\\$')
							opt_resolved += ' ' + ua.utils.resolveVar(ctx, value)

						#############################
						# INC			    #
						#############################

						if node.nodeName == 'inc':
							value = node.getStripedAttribute('value')
							inc += ' ' + value.replace('$', '\\$')
							inc_resolved += ' ' + ua.utils.resolveVar(ctx, value)

						#############################
						# LIB			    #
						#############################

						if node.nodeName == 'lib':
							value = node.getStripedAttribute('value')
							lib += ' ' + value.replace('$', '\\$')
							lib_resolved += ' ' + ua.utils.resolveVar(ctx, value)

						#############################
						# TXT			    #
						#############################

						if node.nodeType ==  0x4 :
							txt = node.nodeValue.rstrip()

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
				ua.utils.ooops(ctx, '<project name="%s" type="\033[31m%s\033[0m" ...>, value error !' % (name, type))
				isOk = False

		if type != 'UND':
			if not link in ctx.build_links:
				ua.utils.ooops(ctx, '<project name="%s" link="\033[31m%s\033[0m" ...>, value error !' % (name, link))
				isOk = False

		if not isOk:
			continue

		#############################################################

		TARGETS = project.getItemsByUAttrName('targets')

		#############################################################

		for node in project.childNodes:

			#####################################################
			# SHELL						    #
			#####################################################

			if node.nodeName == 'shell':

				for node in node.childNodes:

					#####################################
					# CDATA				    #
					#####################################

					if node.nodeType == 0x004:

						pipe = subprocess.Popen(
							node.nodeValue,
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

			if node.nodeName == 'src':

				expr = node.getStripedAttribute('path')

				paths = ua.utils.buildPaths(ctx, expr)

				if len(paths) == 0:
					ua.utils.ooops(ctx, 'Invalid path \'%s\' !' % expr)
				else:
					for path in paths:

						#############################

						opt = node.getStripedAttribute('opt')
						inc = node.getStripedAttribute('inc')

						targets = node.getItemsByUAttrName('targets')

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

			if node.nodeName == 'use':
				dep = node.getStripedLAttribute('name')

				if node.getStripedLAttribute('optional') == 'yes':
					ctx.option_deps.add(dep)
				else:
					ctx.needed_deps.add(dep)

				USES.append(dep)

			#####################################################
			# OPT						    #
			#####################################################

			if node.nodeName == 'opt':
				OPTS.append(node.getStripedAttribute('value').replace('$', '\\$'))

			#####################################################
			# INC						    #
			#####################################################

			if node.nodeName == 'inc':
				INCS.append(node.getStripedAttribute('value').replace('$', '\\$'))

			#####################################################
			# OBJ						    #
			#####################################################

			if node.nodeName == 'obj':
				OBJS.append(node.getStripedAttribute('value').replace('$', '\\$'))

			#####################################################
			# LIB						    #
			#####################################################

			if node.nodeName == 'lib':
				LIBS.append(node.getStripedAttribute('value').replace('$', '\\$'))

			#####################################################
			# TXT						    #
			#####################################################

			if node.nodeType == 0x004:
				TXTS.append(          node.nodeValue.rstrip().replace('$', '\\$'))

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


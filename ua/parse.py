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

debug = False

#############################################################################
# FUSE									    #
#############################################################################

def fuseNodes(ctx, fuses):
	#####################################################################

	for fuse in fuses:
		#############################################################

		KEYS = []

		#############################################################

		for node1 in fuse.childNodes:

			#####################################################
			# KEY						    #
			#####################################################

			if node1.nodeName == 'key':

				#############################################

				name = ua.utils.resolve(ctx, node1.getStripedLAttribute('name'))
				opt = ua.utils.resolve(ctx, node1.getStripedIAttribute('opt'))

				#############################################

				if len(opt) == 0: opt = 'EmPtY'

				#############################################

				dic = {
					'name': name,
					'opt': opt,
				}

				KEYS.append(dic)

		#############################################################

		KEYS.append({
			'name': 'disabled',
			'opt': 'EmPtY',
		})

		#############################################################

		name = ua.utils.resolve(ctx, fuse.getStripedIAttribute('name'))
		default = fuse.getStripedLAttribute('default')
		enabled = fuse.getStripedLAttribute('enabled')
		help = fuse.getStripedIAttribute('help')

		#############################################################

		dic = {
			'name': name,
			'default': default,
			'enabled': enabled,
			'help': help,

			'keys': KEYS,
		}

		ctx.fuses.append(dic)

	#####################################################################

	if debug and ctx.verbose:
		print('-----------------------------------------------------------------------------')
		print('| FUSES                                                                     |')
		print('-----------------------------------------------------------------------------')
		ua.utils.displayTree(ctx.fuses)
		print('-----------------------------------------------------------------------------')

#############################################################################
# DEP									    #
#############################################################################

def depNodes(ctx, deps):
	#####################################################################

	for dep in deps:
		#############################################################

		name = ua.utils.resolve(ctx, dep.getStripedLAttribute('name'))
		vers = ua.utils.resolve(ctx, dep.getStripedLAttribute('vers'))
		lang = ua.utils.resolve(ctx, dep.getStripedLAttribute('lang'))

		if not ua.utils.COMPS.has_key(lang):
			ua.utils.ooops(ctx, 'In dep `%s`: unkwnown language: `%s`' % (name, lang))

			lang = 'c'

		#############################################################

		TARGETS = {}

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
							value = node2.getStripedIAttribute('value')
							opt          += ' ' + ua.utils.protect(ctx, value)
							opt_resolved += ' ' + ua.utils.unprotect(ctx, value)

						#############################
						# INC			    #
						#############################

						if node2.nodeName == 'inc':
							value = node2.getStripedIAttribute('value')
							inc          += ' ' + ua.utils.protect(ctx, value)
							inc_resolved += ' ' + ua.utils.unprotect(ctx, value)

						#############################
						# LIB			    #
						#############################

						if node2.nodeName == 'lib':
							value = node2.getStripedIAttribute('value')
							lib          += ' ' + ua.utils.protect(ctx, value)
							lib_resolved += ' ' + ua.utils.unprotect(ctx, value)

						#############################
						# TXT			    #
						#############################

						if node2.nodeType == 0x004:
							txt = node2.nodeValue

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
			'name': name,
			'vers': vers,
			'lang': lang,
			'targets': TARGETS,
		}

		ctx.deps.append(dic)

	#####################################################################

	if debug and ctx.verbose:
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

		name = ua.utils.resolve(ctx, project.getStripedIAttribute('name'))
		type = ua.utils.resolve(ctx, project.getStripedUAttribute('type'))
		link = ua.utils.resolve(ctx, project.getStripedUAttribute('link'))

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

		SRCS = []
		USES = []
		OPTS = []
		INCS = []
		OBJS = []
		LIBS = []

		PRE_BUILD = []
		POST_BUILD = []
		PRE_INSTALL = []
		POST_INSTALL = []
		PRE_CLEAN = []
		POST_CLEAN = []

		EXTRAS = []

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

						if ua.utils.popen(node2.nodeValue) != 0:

							sys.exit(pipe.returncode)

			#####################################################
			# SRC						    #
			#####################################################

			if node1.nodeName == 'src':

				#############################################

				expr = node1.getAttribute('path')

				paths = ua.utils.buildPaths(ctx, name, expr)

				opt = ua.utils.processAndProtect(ctx, name, node1.getAttribute('opt'))
				inc = ua.utils.processAndProtect(ctx, name, node1.getAttribute('inc'))

				targets = node1.getItemsByUAttrName('targets')
				fuses = node1.getItemsByLAttrName('fuses')

				#############################################

				if len(paths) > 0:

					for path in paths:

						dic = {
							'path': path,
							'opt': opt,
							'inc': inc,
							'targets': targets,
							'fuses': fuses,
						}

						SRCS.append(dic)

				else:
					ua.utils.ooops(ctx, 'Invalid path \'%s\' !' % expr)

			#####################################################
			# USE						    #
			#####################################################

			if node1.nodeName == 'use':
				dep = ua.utils.resolve(ctx, node1.getStripedLAttribute('name'))

				if ua.utils.resolve(ctx, node1.getStripedLAttribute('optional')) == 'yes':
					ctx.option_deps.add(dep)
				else:
					ctx.needed_deps.add(dep)

				USES.append(dep)

			#####################################################
			# OPT						    #
			#####################################################

			if node1.nodeName == 'opt':
				value = ua.utils.processAndProtect(ctx, name, node1.getAttribute('value'))

				targets = node1.getItemsByUAttrName('targets')
				fuses = node1.getItemsByLAttrName('fuses')

				dic = {
					'value': value,
					'targets': targets,
					'fuses': fuses,
				}

				OPTS.append(dic)

			#####################################################
			# INC						    #
			#####################################################

			if node1.nodeName == 'inc':
				value = ua.utils.processAndProtect(ctx, name, node1.getAttribute('value'))

				targets = node1.getItemsByUAttrName('targets')
				fuses = node1.getItemsByLAttrName('fuses')

				dic = {
					'value': value,
					'targets': targets,
					'fuses': fuses,
				}

				INCS.append(dic)

			#####################################################
			# OBJ						    #
			#####################################################

			if node1.nodeName == 'obj':
				value = ua.utils.processAndProtect(ctx, name, node1.getAttribute('value'))

				targets = node1.getItemsByUAttrName('targets')
				fuses = node1.getItemsByLAttrName('fuses')

				dic = {
					'value': value,
					'targets': targets,
					'fuses': fuses,
				}

				OBJS.append(dic)

			#####################################################
			# LIB						    #
			#####################################################

			if node1.nodeName == 'lib':
				value = ua.utils.processAndProtect(ctx, name, node1.getAttribute('value'))

				targets = node1.getItemsByUAttrName('targets')
				fuses = node1.getItemsByLAttrName('fuses')

				dic = {
					'value': value,
					'targets': targets,
					'fuses': fuses,
				}

				LIBS.append(dic)

			#####################################################
			# PRE_BUILD					    #
			#####################################################

			if node1.nodeName == 'pre_build':

				for node2 in node1.childNodes:

					if node2.nodeType == 0x004:
						PRE_BUILD.append('\t' + ua.utils.processAndProtect(ctx, name, node2.nodeValue))

			#####################################################
			# POST_BUILD					    #
			#####################################################

			if node1.nodeName == 'post_build':

				for node2 in node1.childNodes:

					if node2.nodeType == 0x004:
						POST_BUILD.append('\t' + ua.utils.processAndProtect(ctx, name, node2.nodeValue))

			#####################################################
			# PRE_INSTALL					    #
			#####################################################

			if node1.nodeName == 'pre_install':

				for node2 in node1.childNodes:

					if node2.nodeType == 0x004:
						PRE_INSTALL.append('\t' + ua.utils.processAndProtect(ctx, name, node2.nodeValue))

			#####################################################
			# POST_INSTALL					    #
			#####################################################

			if node1.nodeName == 'post_install':

				for node2 in node1.childNodes:

					if node2.nodeType == 0x004:
						POST_INSTALL.append('\t' + ua.utils.processAndProtect(ctx, name, node2.nodeValue))

			#####################################################
			# PRE_CLEAN					    #
			#####################################################

			if node1.nodeName == 'pre_clean':

				for node2 in node1.childNodes:

					if node2.nodeType == 0x004:
						PRE_CLEAN.append('\t' + ua.utils.processAndProtect(ctx, name, node2.nodeValue))

			#####################################################
			# POST_CLEAN					    #
			#####################################################

			if node1.nodeName == 'post_clean':

				for node2 in node1.childNodes:

					if node2.nodeType == 0x004:
						POST_CLEAN.append('\t' + ua.utils.processAndProtect(ctx, name, node2.nodeValue))

			#####################################################
			# EXTRAS					    #
			#####################################################

			if node1.nodeName == 'extras':

				for node2 in node1.childNodes:

					if node2.nodeType == 0x004:
						EXTRAS.append(ua.utils.processAndProtect(ctx, name, node2.nodeValue))

		#############################################################

		OPTS.append({
			'value': '-D__IS_%s -D__IS_%s -D__name__=\\\\\\"%s\\\\\\"' % (type, link, name),
			'targets': [],
			'fuses': [],
		})

		#############################################################

		targets = project.getItemsByUAttrName('targets')
		fuses = project.getItemsByLAttrName('fuses')

		#############################################################

		dic = {
			'name': name,
			'type': type,
			'link': link,

			'targets': targets,
			'fuses': fuses,

			'srcs': SRCS,
			'uses': USES,
			'opts': OPTS,
			'incs': INCS,
			'objs': OBJS,
			'libs': LIBS,

			'pre_build': PRE_BUILD,
			'post_build': POST_BUILD,
			'pre_install': PRE_INSTALL,
			'post_install': POST_INSTALL,
			'pre_clean': PRE_CLEAN,
			'post_clean': POST_CLEAN,

			'extras': EXTRAS,
		}

		ctx.projects.append(dic)

	#####################################################################

	if debug and ctx.verbose:
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

		url = ua.utils.resolveEnv(ctx, link.getStripedIAttribute('url'))

		#############################################################

		dir = os.path.dirname(url).replace('\\', '/')
		base = os.path.basename(url).replace('\\', '/')
		rid = os.path.relpath2(dir).replace('\\', '/')

		targets = link.getItemsByUAttrName('targets')
		fuses = link.getItemsByLAttrName('fuses')

		#############################################################

		dic = {
			'dir': dir,
			'base': base,
			'rid': rid,

			'targets': targets,
			'fuses': fuses,
		}

		ctx.links.append(dic)

	#####################################################################

	if debug and ctx.verbose:
		print('-----------------------------------------------------------------------------')
		print('| LINK                                                                      |')
		print('-----------------------------------------------------------------------------')
		ua.utils.displayTree(ctx.links)
		print('-----------------------------------------------------------------------------')

#############################################################################


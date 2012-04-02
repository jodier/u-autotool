/* Author  : Jerome ODIER
 * Email   : jerome.odier@cern.ch
 *
 * Version : 1.0 (2010-2012)
 *
 *
 * This file is part of u-autotool.
 *
 *  Foobar is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License as published
 *  by the Free Software Foundation; either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Foobar is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*-------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/*-------------------------------------------------------------------------*/

int main(int argc, char **argv)
{
	/*-----------------------------------------------------------------*/

	if(argc != 2)
	{
		fprintf(stderr, "Usage: %s compiler\n\nReturns 'sizeof(long)' for 'compiler'.\n", argv[0]);

		return 1;
	}

	/*-----------------------------------------------------------------*/

	FILE *fp;

	char fname1[1024];
	char fname2[1024];

	char buffer[4096];

	/*-----------------------------------------------------------------*/

	if(strstr(argv[1], "++") == NULL)
	{
		sprintf(fname1, "___bussize_%d.c", getpid());
	}
	else
	{
		sprintf(fname1, "___bussize_%d.C", getpid());
	}

	sprintf(fname2, "___bussize_%d.o", getpid());

	/*-----------------------------------------------------------------*/

	if((fp = fopen(fname1, "wt")) == NULL)
	{
		fprintf(stderr, "could not open '%s' !\n", fname1);

		return 1;
	}

	fprintf(fp, \
		"struct __foo_s					\n"
		"{						\n"
		"	char magic1[8];				\n"
		"	long l;					\n"
		"	char magic2[8];				\n"
		"						\n"
		"} __attribute__((packed)) foo = {		\n"
		"	{'b', 'u', 's', 's', 'i', 'z', 'e', 'B'}\n"
		"	,					\n"
		"	-1					\n"
		"	,					\n"
		"	{'b', 'u', 's', 's', 'i', 'z', 'e', 'E'}\n"
		"};						\n"
	);

	fclose(fp);

	/*-----------------------------------------------------------------*/

	if(sprintf(buffer, "%s -c -o %s %s", argv[1], fname2, fname1) > 0 && system(buffer) != 0)
	{
		return 1;
	}

	/*-----------------------------------------------------------------*/

	if((fp = fopen(fname2, "rb")) == NULL)
	{
		fprintf(stderr, "could not open '%s' !\n", fname2);

		return 1;
	}

	/**/

	fseek(fp, 0, SEEK_END);
	size_t size = ftell(fp);
	fseek(fp, 0, SEEK_SET);

	/**/

	void *buff = malloc(size);

	if(fread(buff, 1, size, fp) != size)
	{
		fprintf(stderr, "could not read '%s' !\n", fname2);

		free(buff);

		fclose(fp);

		return 1;
	}

	fclose(fp);

	/*-----------------------------------------------------------------*/

	char *p1;
	char *p2;

	for(p1 = (char *) buff;; p1++)
	{
		if(strncmp(p1, "bussizeB", 8) == 0) {
			break;
		}
	}

	for(p2 = (char *) buff;; p2++)
	{
		if(strncmp(p2, "bussizeE", 8) == 0) {
			break;
		}
	}

	/*-----------------------------------------------------------------*/

	free(buff);

	remove(fname1);
	remove(fname2);

	/*-----------------------------------------------------------------*/

	p1 += 8UL;

	printf("%ld\n", 8UL * ((unsigned long) p2 - (unsigned long) p1));

	/*-----------------------------------------------------------------*/

	return 0;
}

/*-------------------------------------------------------------------------*/


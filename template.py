#!/usr/bin/env python

template='''#!/bin/bash

#############################################################################

SRC_PREFIX=`dirname $0`
PWD_PREFIX=.
DST_PREFIX='/usr/local'

#############################################################################

if test -n "$CC";
then
  GCC=$CC
  ACC=$CC
fi

if test -n "$CXX";
then
  GXX=$CXX
  AXX=$CXX
fi

#############################################################################

if test -z "$GCC";
then
  GCC='gcc'
fi

if test -z "$GXX";
then
  GXX='g++'
fi

if test -z "$ACC";
then
  if [ `uname -s` == 'Darwin' ];
  then
    ACC='gcc -fnext-runtime'
  else
    ACC='gcc -fgnu-runtime'
  fi
fi

if test -z "$AXX";
then
  if [ `uname -s` == 'Darwin' ];
  then
    AXX='g++ -fnext-runtime'
  else
    AXX='g++ -fgnu-runtime'
  fi
fi

if test -z "$AR";
then
  AR='ar'
fi

if test -z "$RANLIB";
then
  RANLIB='ranlib'
fi

if test -z "$OBJCOPY";
then
  OBJCOPY='objcopy'
fi

if test -z "$OBJDUMP";
then
  OBJDUMP='objdump'
fi

#############################################################################

FLEX='flex -X'
BISON='bison -yd'
TAR='tar'

#############################################################################

TARGET=`$GCC -dumpmachine 2> /dev/null`

BUSSIZE=`bussize "$GCC"`
BUSORDER=`busorder "$GCC"`

#############################################################################

PROJECT_PREFIX=''
PROJECT_SUFFIX=''

#############################################################################

function configure_help
{
  cat << EOF
  -h, --help                        display this help and exit

      --target=TARGET               configure for TARGET
                                    TARGET=[$TARGET]

      --prefix=PREFIX               install files in PREFIX
                                    PREFIX=[$DST_PREFIX]

      --project-prefix=PREFIX       prepend PREFIX to installed project names
                                    PREFIX=[$PROJECT_PREFIX]

      --project-suffix=SUFFIX       append SUFFIX to installed project names
                                    SUFFIX=[$PROJECT_SUFFIX]

%s
EOF

  exit 1
}

#############################################################################

%s

#############################################################################

function resetFuse
{
	index=0

	while [ $index -lt ${#FUSES[@]} ]
	do
		if [[ ${FUSES[$index]} == ${1}_* ]]
		then
			unset FUSES[$index]

			unset GLOBAL_OPTS[$index]
		fi

		let "index++"
	done
}

#############################################################################

for option in $*
do

  case $option
  in
    *=*)
      arg=`expr "X$option" : '[^=]*=\(.*\)'`
      ;;
    *)
      arg=''
      ;;
  esac

  case $option
  in
    --target=*)
      TARGET=$arg
      ;;
    --prefix=*)
      DST_PREFIX=$arg
      ;;
    --project-prefix=*)
      PROJECT_PREFIX=$arg
      ;;
    --project-suffix=*)
      PROJECT_SUFFIX=$arg
      ;;
%s    -h | --help)
      configure_help
      ;;
    *)
      echo "$0: warning: ignored option: $option"
  esac

done

#############################################################################

case `echo $TARGET | tr [:lower:] [:upper:]`
in
  *LINUX*)
    OS_NAME='__IS_TUX'
    ;;
  *OSX*)
    OS_NAME='__IS_OSX'
    ;;
  *MINGW*)
    OS_NAME='__IS_WIN'
    ;;
  *IOS*)
    OS_NAME='__IS_IOS'
    ;;
  *ANDROID*)
    OS_NAME='__IS_ANDROID'
    ;;
  *HYPNOS*)
    OS_NAME='__IS_HYPNOS'
    ;;
  *)
    echo "Invalid target '$TARGET'"

    exit 1
esac

#############################################################################

case `echo $TARGET | tr [:lower:] [:upper:]`
in
  *I386*|*I486*|*I586*|*I686*)
    BUSSIZE=32
    OS_ARCH='__ARCH_X86'
    FUSES=(${FUSES[@]} 'ARCH_X86')
    ;;
  *X86_64*|*AMD64*)
    BUSSIZE=64
    OS_ARCH='__ARCH_X86_64'
    FUSES=(${FUSES[@]} 'ARCH_X86_64')
    ;;
  *ARM*)
    BUSSIZE=32
    OS_ARCH='__ARCH_ARM'
    FUSES=(${FUSES[@]} 'ARCH_ARM')
    ;;
  *)
    OS_ARCH='__ARCH_UNKNOWN'
    FUSES=(${FUSES[@]} 'ARCH_UNKNOWN')
esac

#############################################################################

echo "For target '$TARGET': $GCC, $GXX, $ACC, $AXX, $AR, $RANLIB, $OBJCOPY, $OBJDUMP, $FLEX, $BISON"

#############################################################################

%s

#############################################################################

case $OS_NAME
in
  __IS_TUX|__IS_HYPNOS)
    LIB_SHARED_SUFFIX='.so'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX=''
    EXE_STATIC_SUFFIX=''

    OS_LFLAGS='-fPIC -shared'
    ;;
  __IS_OSX)
    LIB_SHARED_SUFFIX='.dylib'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX=''
    EXE_STATIC_SUFFIX=''

    OS_LFLAGS='-fPIC -dynamiclib'
    ;;
  __IS_WIN)
    LIB_SHARED_SUFFIX='.dll'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX='.exe'
    EXE_STATIC_SUFFIX='.exe'

    OS_LFLAGS='-fPIC -shared'
    ;;
  __IS_IOS)
    LIB_SHARED_SUFFIX='.dylib'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX=''
    EXE_STATIC_SUFFIX=''

    OS_LFLAGS='-fPIC -dynamiclib'
    ;;
  __IS_ANDROID)
    LIB_SHARED_SUFFIX='.so'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX=''
    EXE_STATIC_SUFFIX=''

    OS_LFLAGS='-fPIC -shared'
    ;;
  *)
    echo 'Invalid target'

    exit 1
esac

#############################################################################

OS_BIN=bin
OS_INC=include
OS_SRC=src
OS_ETC=etc

if [ -d /usr/lib$BUSSIZE ]
then
  OS_LIB=lib$BUSSIZE
else
  OS_LIB=lib
fi

#############################################################################

case $BUSSIZE
in
  32)
    OS_BUSSIZE=__IS_32BITS

    case $OS_NAME
    in
      __IS_TUX|__IS_HYPNOS)
        OS_CFLAGS=''
        ;;
      __IS_OSX)
        OS_CFLAGS=''
        ;;
      __IS_WIN)
        OS_CFLAGS=''
        ;;
      __IS_IOS)
        OS_CFLAGS=''
        ;;
      __IS_ANDROID)
        OS_CFLAGS=''
        ;;
    esac
    ;;
  64)
    OS_BUSSIZE=__IS_64BITS

    case $OS_NAME
    in
      __IS_TUX|__IS_HYPNOS)
        OS_CFLAGS=''
        ;;
      __IS_OSX)
        OS_CFLAGS=''
        ;;
      __IS_WIN)
        OS_CFLAGS=''
        ;;
      __IS_IOS)
        OS_CFLAGS=''
        ;;
      __IS_ANDROID)
        OS_CFLAGS=''
        ;;
    esac
    ;;
  *)
    echo 'Invalid target'

    exit 1
esac

#############################################################################

case $BUSORDER
in
  little)
    OS_BUSORDER=__IS_LIT_ENDIAN
    ;;
  big)
    OS_BUSORDER=__IS_BIG_ENDIAN
    ;;
  *)
    echo 'Invalid endianness'

    exit 1
esac

#############################################################################

%s

#############################################################################

function trim
{
    echo $*
}

#############################################################################

cat > ./Makefile.conf << EOF
#############################################################################
# Makefile.conf
#
# Automatically generated by u-autotool.
#
#############################################################################

GCC=$GCC
GXX=$GXX
ACC=$ACC
AXX=$AXX
AR=$AR
RANLIB=$RANLIB
OBJCOPY=$OBJCOPY
OBJDUMP=$OBJDUMP
FLEX=$FLEX
BISON=$BISON
TAR=$TAR

#############################################################################

OS_CFLAGS=$OS_CFLAGS -D$OS_NAME -D$OS_ARCH -D$OS_BUSSIZE -D$OS_BUSORDER
OS_LFLAGS=$OS_LFLAGS

#############################################################################

LIB_SHARED_SUFFIX=$LIB_SHARED_SUFFIX
LIB_STATIC_SUFFIX=$LIB_STATIC_SUFFIX
EXE_SHARED_SUFFIX=$EXE_SHARED_SUFFIX
EXE_STATIC_SUFFIX=$EXE_STATIC_SUFFIX

#############################################################################

SRC_PREFIX=$SRC_PREFIX
PWD_PREFIX=$PWD_PREFIX
DST_PREFIX=$DST_PREFIX

#############################################################################

PROJECT_PREFIX=$PROJECT_PREFIX
PROJECT_SUFFIX=$PROJECT_SUFFIX

#############################################################################

BIN=$OS_BIN
INC=$OS_INC
LIB=$OS_LIB
SRC=$OS_SRC
ETC=$OS_ETC

#############################################################################

SRC_BIN=\$(SRC_PREFIX)/\$(BIN)
SRC_INC=\$(SRC_PREFIX)/\$(INC)
SRC_LIB=\$(SRC_PREFIX)/\$(LIB)
SRC_SRC=\$(SRC_PREFIX)/\$(SRC)
SRC_ETC=\$(SRC_PREFIX)/\$(ETC)

#############################################################################

PWD_BIN=\$(PWD_PREFIX)/\$(BIN)
PWD_INC=\$(PWD_PREFIX)/\$(INC)
PWD_LIB=\$(PWD_PREFIX)/\$(LIB)
PWD_SRC=\$(PWD_PREFIX)/\$(SRC)
PWD_ETC=\$(PWD_PREFIX)/\$(ETC)

#############################################################################

DST_BIN=\$(DST_PREFIX)/\$(BIN)
DST_INC=\$(DST_PREFIX)/\$(INC)
DST_LIB=\$(DST_PREFIX)/\$(LIB)
DST_SRC=\$(DST_PREFIX)/\$(SRC)
DST_ETC=\$(DST_PREFIX)/\$(ETC)

#############################################################################

FUSES=${FUSES[@]}

#############################################################################

GCC_OPT=\$(OS_CFLAGS) %s -fomit-frame-pointer -fno-builtin -Wall -Werror -pipe ${GLOBAL_OPTS[@]/EmPtY/}
GCC_INC=-I. -I\$(PWD_INC)
GCC_LIB=-L. -L\$(PWD_LIB)

#############################################################################

GXX_OPT=\$(OS_CFLAGS) %s -fomit-frame-pointer -fno-builtin -Wall -Werror -pipe ${GLOBAL_OPTS[@]/EmPtY/}
GXX_INC=-I. -I\$(PWD_INC)
GXX_LIB=-L. -L\$(PWD_LIB)

#############################################################################

ACC_OPT=\$(OS_CFLAGS) %s -fomit-frame-pointer -fno-builtin -Wall -Werror -pipe ${GLOBAL_OPTS[@]/EmPtY/}
ACC_INC=-I. -I\$(PWD_INC)
ACC_LIB=-L. -L\$(PWD_LIB)

#############################################################################

AXX_OPT=\$(OS_CFLAGS) %s -fomit-frame-pointer -fno-builtin -Wall -Werror -pipe ${GLOBAL_OPTS[@]/EmPtY/}
AXX_INC=-I. -I\$(PWD_INC)
AXX_LIB=-L. -L\$(PWD_LIB)

#############################################################################

%s

#############################################################################

EOF

#############################################################################

cat > ./Makefile << EOF
#############################################################################
# Makefile
#
# Automatically generated by u-autotool.
#
#############################################################################

include ./Makefile.conf

#############################################################################

%s

############################################################################

EOF

#############################################################################

'''

import sys, zlib, base64

template = base64.b64encode(zlib.compress(template, 9))

if __name__ == '__main__':

	i = 1

	sys.stdout.write(' = \\\n\tb\'')

	for c in template:
		sys.stdout.write(c)

		i += 1

		if i == 65:
			i = 1;

			sys.stdout.write('\' +\\\n\tb\'')

	print '\'\n'


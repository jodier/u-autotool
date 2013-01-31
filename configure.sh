#!/bin/bash

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
#
#cat > /tmp/businfo_$$.c << EOF
#
#struct __foo1_s
#{
#	char magic1[8];
#	void *x;
#	char magic2[8];
#
#} __attribute__((packed)) foo1 = {
#	{'b', 'u', 's', 's', 'i', 'z', 'e', 'B'}
#	,
#	(void *) 0xFFFFFFFFU
#	,
#	{'b', 'u', 's', 's', 'i', 'z', 'e', 'E'}
#};
#
#struct __foo2_s
#{
#	char magic1[9];
#	unsigned int x;
#	char magic2[9];
#
#} __attribute__((packed)) foo2 = {
#	{'b', 'u', 's', 'o', 'r', 'd', 'e', 'r', 'B'}
#	,
#	(unsigned int) 0x04030201U
#	,
#	{'b', 'u', 's', 'o', 'r', 'd', 'e', 'r', 'E'}
#};
#
#EOF
#
#############################################################################
#(
#  $GCC -c -o /tmp/businfo_$$.o /tmp/businfo_$$.c
#
#) || exit 1
#
#DATA=$(od -An -t x1 -v /tmp/businfo_$$.o)
#DATA=${DATA// /}
#DATA=${DATA//
#/}
#
#BUSSIZE=$(awk -v DATA="$DATA" 'BEGIN {
#	x = index(DATA, "62757373697a6542"); // bussizeB
#	y = index(DATA, "62757373697a6545"); // bussizeE
#
#	print 4 * (y - x - 16);
#}')
#
#BUSORDER=$(awk -v DATA="$DATA" 'BEGIN {
#	x = index(DATA, "6275736f7264657242"); // busorderB
#	y = index(DATA, "6275736f7264657245"); // busorderE
#
#	print substr(DATA, x + 18, y - x - 18);
#}')
#
#if [[ $BUSSIZE != 8 && $BUSSIZE != 16 && $BUSSIZE != 32 && $BUSSIZE != 64 ]]
#then
#  echo 'Invalid pointer size'
#
#  exit 1
#fi
#
#case $BUSORDER
#in
#  *01020304)
#    OS_BUSORDER=__IS_LIT_ENDIAN
#    ;;
#  *04030201)
#    OS_BUSORDER=__IS_BIG_ENDIAN
#    ;;
#  *)
#    echo 'Invalid endianness'
#
#    exit 1
#esac
#
#rm /tmp/businfo_$$.c
#rm /tmp/businfo_$$.o

BUSSIZE=32

OS_BUSORDER=__IS_LIT_ENDIAN

#############################################################################

TARGET=`$GCC -dumpmachine 2> /dev/null`

SRC_PREFIX=`dirname $0`
PWD_PREFIX='.'
DST_PREFIX='/usr/local'

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
%s    --enable-*)
      ;;
    --disable-*)
      ;;
    -h | --help)
      configure_help
      ;;
    *)
      echo "$0: info: ignored option: $option"
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
    OS_ARCH='__ARCH_X86'
    FUSES=(${FUSES[@]} 'ARCH_X86')
    ;;
  *X86_64*|*AMD64*)
    OS_ARCH='__ARCH_X86_64'
    FUSES=(${FUSES[@]} 'ARCH_X86_64')
    ;;
  *ARM*)
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

    OS_LFLAGS='-shared'
    ;;
  __IS_OSX)
    LIB_SHARED_SUFFIX='.dylib'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX=''
    EXE_STATIC_SUFFIX=''

    OS_LFLAGS='-dynamiclib'
    ;;
  __IS_WIN)
    LIB_SHARED_SUFFIX='.dll'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX='.exe'
    EXE_STATIC_SUFFIX='.exe'

    OS_LFLAGS='-shared'
    ;;
  __IS_IOS)
    LIB_SHARED_SUFFIX='.dylib'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX=''
    EXE_STATIC_SUFFIX=''

    OS_LFLAGS='-dynamiclib'
    ;;
  __IS_ANDROID)
    LIB_SHARED_SUFFIX='.so'
    LIB_STATIC_SUFFIX='.a'
    EXE_SHARED_SUFFIX=''
    EXE_STATIC_SUFFIX=''

    OS_LFLAGS='-shared'
    ;;
  *)
    echo 'Invalid target'

    exit 1
esac

#############################################################################

OS_BIN=bin
OS_INC=include
OS_LIB=lib
OS_ETC=etc

#############################################################################

case $BUSSIZE
in
  32)
    OS_BUSSIZE=__IS_32BITS

    case $OS_NAME
    in
      __IS_TUX)
        OS_CFLAGS='-fPIC'
        ;;
      __IS_OSX)
        OS_CFLAGS='-fPIC'
        ;;
      __IS_WIN)
        OS_CFLAGS=''
        ;;
      __IS_IOS)
        OS_CFLAGS='-fPIC'
        ;;
      __IS_ANDROID)
        OS_CFLAGS='-fPIC'
        ;;
      __IS_HYPNOS)
        OS_CFLAGS=''
        ;;
    esac
    ;;
  64)
    OS_BUSSIZE=__IS_64BITS

    case $OS_NAME
    in
      __IS_TUX)
        OS_CFLAGS='-fPIC'
        ;;
      __IS_OSX)
        OS_CFLAGS='-fPIC'
        ;;
      __IS_WIN)
        OS_CFLAGS=''
        ;;
      __IS_IOS)
        OS_CFLAGS='-fPIC'
        ;;
      __IS_ANDROID)
        OS_CFLAGS='-fPIC'
        ;;
      __IS_HYPNOS)
        OS_CFLAGS=''
        ;;
    esac
    ;;
  *)
    echo 'Invalid target'

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
ETC=$OS_ETC

#############################################################################

SRC_BIN=\$(SRC_PREFIX)/\$(BIN)
SRC_INC=\$(SRC_PREFIX)/\$(INC)
SRC_LIB=\$(SRC_PREFIX)/\$(LIB)
SRC_ETC=\$(SRC_PREFIX)/\$(ETC)

#############################################################################

PWD_BIN=\$(PWD_PREFIX)/\$(BIN)
PWD_INC=\$(PWD_PREFIX)/\$(INC)
PWD_LIB=\$(PWD_PREFIX)/\$(LIB)
PWD_ETC=\$(PWD_PREFIX)/\$(ETC)

#############################################################################

DST_BIN=\$(DST_PREFIX)/\$(BIN)
DST_INC=\$(DST_PREFIX)/\$(INC)
DST_LIB=\$(DST_PREFIX)/\$(LIB)
DST_ETC=\$(DST_PREFIX)/\$(ETC)

#############################################################################

FUSES=${FUSES[@]}

#############################################################################

GCC_OPT=\$(OS_CFLAGS) %s -fomit-frame-pointer -fno-builtin -Wall -Werror -pipe ${GLOBAL_OPTS[@]/EmPtY/}
GCC_INC=-I. -I\$(SRC_INC)
GCC_LIB=-L. -L\$(SRC_LIB)

#############################################################################

GXX_OPT=\$(OS_CFLAGS) %s -fomit-frame-pointer -fno-builtin -Wall -Werror -pipe ${GLOBAL_OPTS[@]/EmPtY/}
GXX_INC=-I. -I\$(SRC_INC)
GXX_LIB=-L. -L\$(SRC_LIB)

#############################################################################

ACC_OPT=\$(OS_CFLAGS) %s -fomit-frame-pointer -fno-builtin -Wall -Werror -pipe ${GLOBAL_OPTS[@]/EmPtY/}
ACC_INC=-I. -I\$(SRC_INC)
ACC_LIB=-L. -L\$(SRC_LIB)

#############################################################################

AXX_OPT=\$(OS_CFLAGS) %s -fomit-frame-pointer -fno-builtin -Wall -Werror -pipe ${GLOBAL_OPTS[@]/EmPtY/}
AXX_INC=-I. -I\$(SRC_INC)
AXX_LIB=-L. -L\$(SRC_LIB)

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


#!/bin/env sh

# see https://github.com/raspiblitz/raspiblitz/blob/dev/build_sdcard.sh

me="${0##/*}"
nocolor="\033[0m"
red="\033[31m"

## usage as a function to be called whenever there is a huge mistake on the options
usage(){
  printf %s"${me} [--option <argument>]

Options:
  -h, --help                               this help info
  -a, --app-name <appname>                 the application name
  -o, --outdir <outdir>                    the output directory
  -v, --version <version>                  the application version
  -A, --architecture <arch>                the application architecture
  -m, --maintainer-name <name>             the application maintainer name
  -e, --maintainer-email <email>           the application maintainer email
  -d, --description "<description>"        the application description
  -b, --binary                             the application binary

Notes:
  all options, long and short accept --opt=value mode also
  [0|1] can also be referenced as [false|true]
"
  exit 1
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  usage
fi

## assign_value variable_name "${opt}"
## it strips the dashes and assign the clean value to the variable
## assign_value status --on IS status=on
## variable_name is the name you want it to have
## $opt being options with single or double dashes that don't require arguments
assign_value(){
  case "${2}" in
    --*) value="${2#--}";;
    -*) value="${2#-}";;
    *) value="${2}"
  esac
  case "${value}" in
    0) value="false";;
    1) value="true";;
  esac
  ## Escaping quotes is needed because else if will fail if the argument is quoted
  # shellcheck disable=SC2140
  eval "${1}"="\"${value}\""
}

## default user message
error_msg(){ printf %s"${red}${me}: ${1}${nocolor}\n"; exit 1; }

## get_arg variable_name "${opt}" "${arg}"
## get_arg service --service ssh
## variable_name is the name you want it to have
## $opt being options with single or double dashes
## $arg is requiring and argument, else it fails
## assign_value "${1}" "${3}" means it is assining the argument ($3) to the variable_name ($1)
get_arg(){
  case "${3}" in
    ""|-*) error_msg "Option '${2}' requires an argument.";;
  esac
  assign_value "${1}" "${3}"
}

## hacky getopts
## 1. if the option requires an argument, and the option is preceeded by single or double dash and it
##    can be it can be specified with '-s=ssh' or '-s ssh' or '--service=ssh' or '--service ssh'
##    use: get_arg variable_name "${opt}" "${arg}"
## 2. if a bunch of options that does different things are to be assigned to the same variable
##    and the option is preceeded by single or double dash use: assign_value variable_name "${opt}"
##    as this option does not require argument, specifu $shift_n=1
## 3. if the option does not start with dash and does not require argument, assign to command manually.
while :; do
  case "${1}" in
    -*=*) opt="${1%=*}"; arg="${1#*=}"; shift_n=1;;
    -*) opt="${1}"; arg="${2}"; shift_n=2;;
    *) opt="${1}"; arg="${2}"; shift_n=1;;
  esac
  case "${opt}" in
    -a|-a=*|--app-name|--app-name=*) get_arg app_name "${opt}" "${arg}";;
    -o|-o=*|--output-dir|--output-dir=*) get_arg output_dir "${opt}" "${arg}";;
    -v|-v=*|--version|--version=*) get_arg version "${opt}" "${arg}";;
    -A|-A=*|--architecture|--architecture=*) get_arg architecture "${opt}" "${arg}";;
    -m|-m=*|--maintainer-name|--maintainer-name=*) get_arg maintainer_name "${opt}" "${arg}";;
    -e|-e=*|--maintainer-email|--maintainer-email=*) get_arg maintainer_email "${opt}" "${arg}";;
    -d|-d=*|--description|--description=*) get_arg description "${opt}" "${arg}";;
    -b|-b=*|--binary|--binary=*) get_arg binary "${opt}" "${arg}";;
    "") break;;
    *) echo "Invalid option: ${opt}";;
  esac
  shift "${shift_n}"
done

for key in app_name output_dir version architecture maintainer_name maintainer_email description binary; do
  eval val='$'"${key}"
  [ -n "${val}" ] && printf '%s\n' "${key}=${val}"
done

if [ -z "$app_name" ] || [ -z "$output_dir" ] || [ -z "$version" ] || [ -z "$architecture" ] || [ -z "$maintainer_name" ] || [ -z "$maintainer_email" ] || [ -z "$description" ] || [ -z "$binary" ]; then
  error_msg 'one or more variables are undefined'
  exit 1
fi

mkdir -v -p ${output_dir}/${app_name}-${version}
mkdir -v -p ${output_dir}/${app_name}-${version}/DEBIAN
mkdir -v -p ${output_dir}/${app_name}-${version}/usr/bin
cp -v ${binary} ${output_dir}/${app_name}-${version}/usr/bin/${app_name}

# create control file
echo "[${app_name}] creating ${output_dir}/${app_name}-${version}/DEBIAN/control"
cat <<EOF > ${output_dir}/${app_name}-${version}/DEBIAN/control
Package: ${app_name}
Version: ${version}
Architecture: ${architecture}
Maintainer: ${maintainer_name} <${maintainer_email}>
Description: ${description}
EOF
chmod 0555 ${output_dir}/${app_name}-${version}/DEBIAN/control

# create postscript file
echo "[${app_name}] creating ${output_dir}/${app_name}-${version}/DEBIAN/postint"
cat <<EOF > ${output_dir}/${app_name}-${version}/DEBIAN/postinst
#!/bin/sh
echo "WARN: Adding user \$(whoami) to 'dialout' group to enable flash procedure..."
echo "WARN: You'll need to reboot your system to enable changes          "
usermod -a -G dialout \$(whoami)
EOF
chmod 0755 ${output_dir}/${app_name}-${version}/DEBIAN/postinst

echo "[${app_name}] setting permissions for ${output_dir}/${app_name}-${version}/usr/bin/${app_name}"
chmod +x ${output_dir}/${app_name}-${version}/usr/bin/${appname}

# build .deb
echo "[${app_name}] running dpkg-deb --build"
dpkg-deb --build ${output_dir}/${app_name}-${version}

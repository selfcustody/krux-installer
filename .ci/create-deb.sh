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
  -o, --output-dir <outdir>                the output directory
  -v, --version <version>                  the application version
  -r, --revision <revision>                the application revision
  -A, --architecture <arch>                the application architecture
  -m, --maintainer-name <name>             the application maintainer name
  -e, --maintainer-email <email>           the application maintainer email
  -d, --description "<description>"        the application description
  -b, --binary                             the application binary
  -i, --icon                               the application icon image

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
    -r|-r=*|--revision|--revision=*) get_arg revision "${opt}" "${arg}";;
    -A|-A=*|--architecture|--architecture=*) get_arg architecture "${opt}" "${arg}";;
    -m|-m=*|--maintainer-name|--maintainer-name=*) get_arg maintainer_name "${opt}" "${arg}";;
    -e|-e=*|--maintainer-email|--maintainer-email=*) get_arg maintainer_email "${opt}" "${arg}";;
    -d|-d=*|--description|--description=*) get_arg description "${opt}" "${arg}";;
    -b|-b=*|--binary|--binary=*) get_arg binary "${opt}" "${arg}";;
    -i|-i=*|--icon|--icon=*) get_arg binary "${opt}" "${arg}";;
    "") break;;
    *) echo "Invalid option: ${opt}";;
  esac
  shift "${shift_n}"
done


for key in app_name output_dir version revision architecture maintainer_name maintainer_email description binary icon; do
  eval val='$'"${key}"
  if [ -n "${val}" ]; then
      printf '%s\n' "${key}=${val}"
  elif [ -z "${val}"]; then
      error_msg "${key} undefined"
  fi
done

FULL_OUTPUT_PATH=${output_dir}/${app_name}_${version}-${revision}_${architecture}
mkdir -v -p $FULL_OUTPUT_PATH
mkdir -v -p $FULL_OUTPUT_PATH/DEBIAN
mkdir -v -p $FULL_OUTPUT_PATH/usr/local/bin
mkdir -v -p $FULL_OUTPUT_PATH/usr/share/applications
mkdir -v -p $FULL_OUTPUT_PATH/usr/share/icons/hicolor/
mkdir -v -p $FULL_OUTPUT_PATH/usr/share/icons/hicolor/512x512/
mkdir -v -p $FULL_OUTPUT_PATH/usr/share/icons/hicolor/512x512/apps
cp -v ${binary} $FULL_OUTPUT_PATH/usr/local/bin/${app_name}
convert ${icon} -resize 512x512 $FULL_OUTPUT_PATH/usr/share/icons/hicolor/512x512/apps/${app_name}.png

# create control file
echo "creating $FULL_OUTPUT_PATH/DEBIAN/control"
cat <<EOF > $FULL_OUTPUT_PATH/DEBIAN/control
Package: ${app_name}
Version: ${version}
Architecture: ${architecture}
Maintainer: ${maintainer_name} <${maintainer_email}>
Description: ${description}
EOF
chmod 0555 ${output_dir}/${app_name}-${version}/DEBIAN/control

# create desktop entry
echo "creating $FULL_OUTPUT_PATH/usr/share/applications/${app_name}.desktop"
cat <<EOF > $FULL_OUTPUT_PATH/usr/share/applications/${app_name}.desktop
[Desktop Entry]
Encoding=UTF-8
Version=${version}
Type=Application
Terminal=false
Exec=/usr/local/bin/${app_name}
Name=${app_name}
Icon=/usr/share/icons/highcolor/512x512/apps/${app_name}.png
EOF
chmod 0555 $FULL_OUTPUT_PATH/usr/share/applications/${app_name}.desktop

# create postscript file
echo "creating $FULL_OUTPUT_PATH/DEBIAN/postint"
cat <<EOF > $FULL_OUTPUT_PATH/DEBIAN/postinst
#!/bin/sh
echo "WARN: Adding user \$(whoami) to 'dialout' group to enable flash procedure..."
echo "WARN: You'll need to reboot your system to enable changes          "
usermod -a -G dialout \$(whoami)
EOF
chmod 0755 $FULL_OUTPUT_PATh/DEBIAN/postinst

echo "setting permissions for $FULL_OUTPUT_PATH/usr/local/bin/${app_name}"
chmod +x ${output_dir}/${app_name}-${version}/usr/local/bin/${app_name}

# build .deb
echo "running dpkg-deb --build --root-owner-group $FULL_OUTPUT_PATH"
dpkg-deb --build --root-owner-group $FULL_OUTPUT_PATH

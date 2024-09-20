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
  -a, --name <name>                        the application name
  -v, --version <version>                  the application version
  -m, --maintainer-name <name>             the application maintainer name
  -e, --maintainer-email <email>           the application maintainer email
  -d, --description <description>          the application description
  -r, --readme <readme>                    the application readme path
  -c, --changelog <changelog>              the application changelog path
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
    -a|-a=*|--name|--name=*) get_arg name "${opt}" "${arg}";;
    -v|-v=*|--version|--version=*) get_arg version "${opt}" "${arg}";;
    -m|-m=*|--maintainer-name|--maintainer-name=*) get_arg maintainer_name "${opt}" "${arg}";;
    -e|-e=*|--maintainer-email|--maintainer-email=*) get_arg maintainer_email "${opt}" "${arg}";;
    -d|-d=*|--description|--description=*) get_arg description "${opt}" "${arg}";;
    -c|-c=*|--changelog|--changelog=*) get_arg changelog "${opt}" "${arg}";;
    -r|-r=*|--readme|--readme=*) get_arg readme "${opt}" "${arg}";;
    -b|-b=*|--binary|--binary=*) get_arg binary "${opt}" "${arg}";;
    -i|-i=*|--icon|--icon=*) get_arg icon "${opt}" "${arg}";;
    "") break;;
    *) echo "Invalid option: ${opt}";;
  esac
  shift "${shift_n}"
done


echo "================="
echo "create-rpm v0.0.1"
echo "================="
echo ""
echo "Defined variables"
echo "-----------------"
for key in name version maintainer_name maintainer_email description binary icon changelog readme; do
  eval val='$'"${key}"
  if [ -n "${val}" ]; then
      printf '%s\n' "${key}=${val}"
  elif [ -z "${val}"]; then
      error_msg "${key} undefined"
  fi
done

echo""

# follow https://www.redhat.com/sysadmin/create-rpm-package
RELEASE=1
RPM_NAME=${name}-${version}
BUILD_PATH=$HOME/rpmbuild
TAR_PATH=$BUILD_PATH/$RPM_NAME
CHANGELOG=$(cat $changelog)

mkdir -v -p $RPM_NAME
mkdir -v -p $BUILD_PATH/
mkdir -v -p $BUILD_PATH/BUILD
mkdir -v -p $BUILD_PATH/RPMS
mkdir -v -p $BUILD_PATH/SOURCES
mkdir -v -p $BUILD_PATH/SPECS
mkdir -v -p $BUILD_PATH/SRPMS

# Place the script in the designated directory
cp -v $binary $RPM_NAME
cp -v $icon $RPM_NAME/${name}.png
cp -v $readme $RPM_NAME/README
tar -v --create --file $RPM_NAME.tar.gz $RPM_NAME
mv $RPM_NAME.tar.gz $BUILD_PATH/SOURCES

# Create a .spec file
cat <<EOF > $BUILD_PATH/SPECS/${name}.spec
Name:           ${name}
Version:        ${version}
Release:        ${RELEASE}%{?dist}
Summary:        ${description}
Group:          application
BuildArch:      %{_arch}
License:        MIT
URL:            https://github.com/selfcustody/krux-installer
Source0:        %{name}-%{version}.tar.gz

%description
${description}

%prep
%setup -q

%files
%{_bindir}/%{name}
%{_datadir}/doc/%{name}/README
%{_datarootdir}/applications/%{name}.desktop
%{_datarootdir}/icons/hicolor/512x512/apps/%{name}.png

%install
mkdir -p %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
mkdir -p %{buildroot}%{_datarootdir}/applications/%{name}
mkdir -p %{buildroot}%{_datarootdir}/icons/hicolor/512x512/apps
cp %{name} %{buildroot}%{_bindir}
cp README %{buildroot}%{_datadir}/doc/%{name}/README
cp %{name}.png %{buildroot}%{_datarootdir}/icons/hicolor/512x512/apps/%{name}.png
echo "[Desktop Entry]" > %{buildroot}%{_datarootdir}/applications/%{name}.desktop
echo "Encoding=UTF-8" >> %{buildroot}%{_datarootdir}/applications/%{name}.desktop
echo "Version=%{version}" >> %{buildroot}%{_datarootdir}/applications/%{name}.desktop
echo "Type=Application" >> %{buildroot}%{_datarootdir}/applications/%{name}.desktop
echo "Terminal=false" >> %{buildroot}%{_datarootdir}/applications/%{name}.desktop
echo "Exec=%{_bindir}/%{name}" >> %{buildroot}%{_datarootdir}/applications/%{name}.desktop
echo "Name=%{name}" >> %{buildroot}%{_datarootdir}/applications/%{name}.desktop
echo "Icon=%{_datarootdir}/icons/hicolor/512x512/apps/%{name}.png" >> %{buildroot}%{_datarootdir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%changelog
* $(LC_ALL=en_US.utf8 date +'%a %b %d %Y') ${maintainer_name} <${maintainer_email}> - ${version}-1
${CHANGELOG}

%post
echo ""
echo "                                   -------------"
echo "                                   !!!WARNING!!!"
echo "                                   -------------"
echo ""
if [ -n "\$SUDO_USER" ] && [ "\$SUDO_USER" != "root" ]; then
  echo "Adding user \$SUDO_USER to 'dialout' group to enable flash procedure..."
  echo "You'll need to reboot your system to enable changes"
  usermod -a -G dialout \$SUDO_USER
elif [ -n "\$USER" ] && [ "\$USER" != "root"]; then
  echo "Adding user \$USER to 'dialout' group to enable flash procedure..."
  echo "You'll need to reboot your system to enable changes"
  usermod -a -G dialout \$USER
fi
echo ""
echo ""

%postun
rm -v %{_datarootdir}/applications/%{name}.desktop
rm -v %{_datarootdir}/icons/hicolor/512x512/apps/%{name}.png
echo ""
echo "                                   -------------"
echo "                                   !!!WARNING!!!"
echo "                                   -------------"
echo ""
if [ -n "\$SUDO_USER" ] && [ "\$SUDO_USER" != "root" ]; then
  echo "Removing user \$SUDO_USER from 'dialout' group to disable flash procedure..."
  echo "You'll need to reboot your system to enable changes"
  usermod -a -G dialout \$SUDO_USER
elif [ -n "\$USER" ] && [ "\$USER" != "root"]; then
  echo "Removing user \$USER from 'dialout' group to disable flash procedure..."
  echo "You'll need to reboot your system to enable changes"
  usermod -a -G dialout \$USER
fi
echo ""
echo ""
EOF

echo "Resulting $BUILD_PATH/SPECS/${name}.spec"
echo "---------------------------------------------------"
cat $BUILD_PATH/SPECS/${name}.spec

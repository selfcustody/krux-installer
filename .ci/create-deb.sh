#!/bin/env bash
POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -a|--app-name)
      APPNAME="$2"
      shift # past argument
      shift # past value
      ;;
    -o|--out-dir)
      OUTDIR="$2"
      shift # past argument
      shift # past value
      ;;
    -v|--version)
      VERSION="$2"
      shift # past argument
      shift # past value
      ;;
    -A|--architecture)
      ARCHITECTURE="$2"
      shift # past argument
      shift # past value
      ;;
    -m|--maintainer-name)
      MAINTAINER_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    -e|--maintainer-email)
      MAINTAINER_EMAIL="$2"
      shift # past argument
      shift # past value
      ;;
    -d|--description)
      DESCRIPTION="$2"
      shift # past argument
      shift # past value
      ;;
    -b|--binary)
      BINARY="$2"
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

mkdir -p ${OUTDIR}
mkdir -p ${OUTDIR}/${APPNAME}
mkdir -p ${OUTDIR}/${APPNAME}/DEBIAN
mkdir -p ${OUTDIR}/${APPNAME}/usr/bin
cp ${BINARY} ${OUTDIR}/${APPNAME}/usr/bin/${APPNAME}

# create control file
echo "[${APPNAME}] creating ${OUTDIR}/${APPNAME}/DEBIAN/control"
cat <<EOF > ${OUTDIR}/${APPNAME}/DEBIAN/control
Package: ${APPNAME}
Version: ${VERSION}
Architecture: ${ARCHITECTURE}
Maintainer: ${MAINTAINER_NAME} <${MAINTAINER_EMAIL}>
Description: ${DESCRIPTION}
EOF

# create postscript file
echo "[${APPNAME}] creating ${OUTDIR}/${APPNAME}/DEBIAN/postint"
cat <<EOF > ${OUTDIR}/${APPNAME}/DEBIAN/postinst
#!/bin/env bash

echo "[${APPNAME}] creating $HOME/.config/krux-installer for settings..."
mkdir -p $HOME/.local/krux-installer

echo ""
echo "[${APPNAME}] creating $HOME/.local/krux-installer for assets..."
mkdir -p $HOME/.local/krux-installer

echo "" 
echo "[${APPNAME}] adding user '$(whoami)' to 'dialout' group to enable flash procedure..."
sudo usermod -a -G dialout

echo ""
echo "[${APPNAME}] setting permissions for ${OUTDIR}/${APPNAME}/usr/bin/${APPNAME}"
chmod +x ${OUTDIR}/${APPNAME}/usr/bin/${APPNAME}

echo ""
echo "[${APPNAME}] WARNING: you will need to reboot your system to make changes available"
EOF

# build .deb
dpkg-deb --build ${OUTDIR}/${APPNAME}

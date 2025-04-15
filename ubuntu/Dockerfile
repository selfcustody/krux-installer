# Use Ubuntu 24.04 as the base image
FROM ubuntu:24.04

ARG VERSION
ARG BUILD_DIR
ARG OUTPUT_DIR

# Set environment variables
ENV VERSION="${VERSION:-0.0.20}" \
  DEBIAN_FRONTEND=noninteractive \
  BUILD_DIR=${BUILD_DIR:-/opt/source} \
  OUTPUT_DIR=${OUTPUT_DIR:-/opt/output}

# Install system dependencies
RUN apt-get update && \
  apt-get install -y \
  git \
  build-essential \
  devscripts \
  debhelper \
  dh-python \
  libssl-dev \
  libffi-dev \
  cargo \
  python3-all \
  python3-pip \
  python3-venv \
  python3-poetry \
  rsync \
  dos2unix \
  quilt \
  && rm -rf /var/lib/apt/lists/*

# Clone and prepare source
RUN git clone https://github.com/selfcustody/krux-installer.git ${BUILD_DIR} && \
  cd ${BUILD_DIR} && \
  git fetch --tags && \
  git checkout v${VERSION} && \
  rm -rf .git* .pylint .pytest_cache e2e* htmlcov tests && \
  cd -

# Copy necessary files
COPY ../LICENSE ${BUILD_DIR}/LICENSE
COPY ../CHANGELOG.md ${BUILD_DIR}/CHANGELOG.md
COPY ubuntu/build.py /usr/local/bin/build
COPY ubuntu/debian/rules ${BUILD_DIR}/debian/rules
COPY ubuntu/debian/control ${BUILD_DIR}/debian/control
COPY ubuntu/debian/source/format ${BUILD_DIR}/debian/source/format
COPY ubuntu/debian/source/include-binaries ${BUILD_DIR}/debian/source/include-binaries

RUN chmod +x /usr/local/bin/build ${BUILD_DIR}/debian/rules

VOLUME ["/output"]

RUN find ${BUILD_DIR} -type f -name '*.pyc' -delete && \
  find ${BUILD_DIR} -type d -name '__pycache__' -exec rm -rf {} +

CMD build \
  --build-dir ${BUILD_DIR} \
  --output-dir ${OUTPUT_DIR} \
  --changelog ${BUILD_DIR}/CHANGELOG.md \
  --license ${BUILD_DIR}/LICENSE \
  --software-version ${VERSION} \
  --maintainer-name "qlrd" \
  --maintainer-email "qlrddev@gmail.com"

# MIT License

# Copyright (c) 2022 qlrd

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

FROM electronuserland/builder:wine

MAINTAINER qlrd <106913782+qlrd@users.noreply.github.com>


# See https://medium.com/hackernoon/using-yarn-with-docker-c116ad289d56
RUN mkdir /app

# This is based on a well-known trick 
# to make use of Docker layer caching
# to avoid to reinstall all your modules
# each time you build the container. 
# In this way, Yarn is executed only
# when you change pa ckage.json
# (and the first time, of course).
ADD package.json yarn.lock /tmp/
ADD .yarn-cache.tgz /app

RUN apt-get update -y && \
    apt-get install --no-install-recommends -y -q xvfb

RUN cd /tmp && yarn install
RUN ln -s /tmp/node_modules /app/node_modules && \
    ln -s /tmp/package.json /app/package.json
ADD . /app

WORKDIR /app

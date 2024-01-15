FROM arm64v8/node AS build-stage
ENV NODE_ENV "test"
ENV NODE_DOCKER true
ENV DEBUG "krux:*"
ENV USE_SYSTEM_FPM true
ENV DOCUMENTS /app/Documents

ADD . /app
WORKDIR /app
RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y \
		libopenjp2-tools \
		ruby \
		ruby-dev

RUN gem install fpm
RUN yarn install
RUN yarn run build --arm64 --linux deb
#RUN apt-get install --fix-missing -y xvfb 
#RUN yarn add --dev xvfb-maybe
#RUN node ./node_modules/.bin/xvfb-maybe \
#	./node_modules/.bin/wdio \
#	run \
#	wdio.conf.mts

FROM scratch AS export-stage
COPY --from=build-stage /app/release / 

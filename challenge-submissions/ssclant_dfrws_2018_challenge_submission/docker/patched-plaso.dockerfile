FROM log2timeline/plaso

MAINTAINER SPAWAR Systems Center ATLANTIC

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
	patch \
	python-elasticsearch

COPY plaso.p .

RUN patch -p1 -u -d /usr/lib/python2.7/dist-packages < plaso.p


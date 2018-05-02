# Before you begin

You *must* set `vm.max_map_count = 262144` in `/etc/sysctl.conf`.

*Otherwise Elasticsearch will fail to start up.*

You also need `docker` and `docker-compose`.  The Makefile will attempt to install them if missing, but will not work for all distributions.

# Build

This will build `iot-plaso:latest`, which is plaso with dfrws iot plugins.  You only have to do this once.

   `make build`

# Launching

## Launching elastic stack

   `make elastic-start`

   When finished, run `make elastic-stop`.  You can remove old containers with `make clean`

## Launching plaso

   Example of plaso launch command (shares the `/data` directory on your workstation):
      `sudo docker run -v /data/:/data iot-plaso:latest psort /data/evidences.plaso`


## Elasticsearch info
   URL:      http://localhost:9200
   Login:    elastic
   Password: changeme

## Kibana info
   URL:      http://localhost:5601
   Login:    elastic
   Password: changeme


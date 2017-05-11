#!/bin/sh

JAVA_OPTS=`echo "
  -Xms1024m
  -Xmx1024m
  -Dgatling.core.simulationClass=ria.XRoad
  -Dgatling.core.mute=true
  -Dgatling.charting.indicators.lowerBound=500
  -Dgatling.charting.indicators.higherBound=1000
  -Dgatling.charting.maxPlotPerSeries=3600
  -Dgatling.http.enableGA=false
  -Dgatling.http.ahc.keepAlive=false
  -Dgatling.http.ahc.connectTimeout=5000
  -Dgatling.http.ahc.readTimeout=15000
  -Dgatling.http.ahc.requestTimeout=15000
  ${@}
" | xargs` \
./gatling-charts-highcharts-bundle-2.2.2/bin/gatling.sh

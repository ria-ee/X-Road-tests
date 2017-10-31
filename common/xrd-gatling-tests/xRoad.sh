#!/bin/sh

JAVA_OPTS=`echo "
// Ading memory
  -Xms1024m
  -Xmx1024m
// Defaining the simulation class
  -Dgatling.core.simulationClass=ria.XRoad
// Don't ask for simulation name nor run description
  -Dgatling.core.mute=true
// Lower bound for the requests' response time to track in the reports and the console summary
  -Dgatling.charting.indicators.lowerBound=500
// Higher bound for the requests' response time to track in the reports and the console summary
  -Dgatling.charting.indicators.higherBound=1000
// Number of points per graph in Gatling reports
  -Dgatling.charting.maxPlotPerSeries=3600
// Disabling Google Analytics
  -Dgatling.http.enableGA=false
// Don't Allow pooling HTTP connections
  -Dgatling.http.ahc.keepAlive=false
// Timeout when establishing a connection
  -Dgatling.http.ahc.connectTimeout=5000
// Timeout when a used connection stays idle
  -Dgatling.http.ahc.readTimeout=15000
// Timeout of the requests
  -Dgatling.http.ahc.requestTimeout=15000
  ${@}
" | xargs` \
/var/lib/jenkins/gatling-charts-highcharts-bundle-2.2.3/bin/gatling.sh
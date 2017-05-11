package ria

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._
import java.lang.Double
import java.util.Arrays

class XRoad extends Simulation {

  // XRoad security server end-point URL. Can be overridden from command-line.
  val xRoadURL = System.getProperty("xRoadURL", "http://127.0.0.1:8080/")

  // Test scenario hold times. Default values can be overridden from command-line.
  val warmUpHoldPeriod = Integer.getInteger("warmUpHoldPeriod", 30) seconds
  val mainHoldPeriod = Integer.getInteger("mainHoldPeriod", 600) seconds
  val userBumpInterval = Integer.getInteger("userBumpInterval", 3) seconds

  // Targets for desired requests per second (increased by intervals defined above)
  val rpsTargets = System.getProperty("rpsTargets", "1,5,10,15,20,25,30,35,40,45,50").split(",")

  // Message weights (default values can be overridden from command-line). Make sure the total number is equal to 100.
  val weight2kB = Double.parseDouble(System.getProperty("weight2kB", "30.0"))
  val weight10kB = Double.parseDouble(System.getProperty("weight10kB", "60.0"))
  val weight100kB = Double.parseDouble(System.getProperty("weight100kB", "9.0"))
  val weight2MB = Double.parseDouble(System.getProperty("weight2MB", "0.9"))
  val weight10MB = Double.parseDouble(System.getProperty("weight10MB", "0.1"))

  // XRoad message body variables. Can be overridden from command-line.
  val msgXRoadInstance = System.getProperty("msgXRoadInstance", "ee-dev")
  val msgMemberClass = System.getProperty("msgMemberClass", "COM")
  val msgMemberCode = System.getProperty("msgMemberCode", "11045744")
  val msgMemberSubsystemCode = System.getProperty("msgMemberSubsystemCode", "MockSystem")
  val msgSubsystemCode = System.getProperty("msgSubsystemCode", "MockSystem")
  val msgServiceCode = System.getProperty("msgServiceCode", "mock")
  val msgServiceVersion = System.getProperty("msgServiceVersion", "v1")
  val msgUserId = System.getProperty("msgUserId", "EE1234567890")

  // Gatling HTTP request settings (refer to Gatling documentation at http://gatling.io/).
  val httpConfig = http
    .disableCaching
    .disableFollowRedirect
    .acceptHeader("text/xml")
    .disableWarmUp // That's the Gatlings own HTTP client warm-up, we don't need that as we do our own warm-up scenario.
    .extraInfoExtractor(extraInfo => List(extraInfo.session))

  // Gatling feeder for generating unique ID-s that can be used within XRoad requests
  val xRoadFeeder = Iterator.continually(Map("xRoadRequestId" -> java.util.UUID.randomUUID.toString))

  // Generate XRoad message body with unique identifier. Please note the hardcoded member and service codes.
  def makeXRoadRequest(messageSize: String) =
    feed(xRoadFeeder).exec(
      http("Message " + messageSize)
        .post(xRoadURL)
        .headers(Map(
          "Content-Type" -> "text/xml"
         ))
        .body(StringBody("""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
	xmlns:ns1="http://producer.x-road.eu"
    xmlns:xrd="http://x-road.eu/xsd/xroad.xsd"
    xmlns:id="http://x-road.eu/xsd/identifiers">
  <SOAP-ENV:Header>
    <xrd:client id:objectType="SUBSYSTEM">
      <id:xRoadInstance>""" + msgXRoadInstance + """</id:xRoadInstance>
      <id:memberClass>""" + msgMemberClass + """</id:memberClass>
      <id:memberCode>""" + msgMemberCode + """</id:memberCode>
      <id:subsystemCode>""" + msgMemberSubsystemCode + """</id:subsystemCode>
    </xrd:client>
    <xrd:service id:objectType="SERVICE">
      <id:xRoadInstance>""" + msgXRoadInstance + """</id:xRoadInstance>
      <id:memberClass>""" + msgMemberClass + """</id:memberClass>
      <id:memberCode>""" + msgMemberCode + """</id:memberCode>
      <id:subsystemCode>""" + msgSubsystemCode + """</id:subsystemCode>
      <id:serviceCode>""" + msgServiceCode + """</id:serviceCode>
      <id:serviceVersion>""" + msgServiceVersion + """</id:serviceVersion>
    </xrd:service>
    <xrd:userId>""" + msgUserId + """</xrd:userId>
    <xrd:id>${xRoadRequestId}</xrd:id>
    <xrd:protocolVersion>4.0</xrd:protocolVersion>
  </SOAP-ENV:Header>
  <SOAP-ENV:Body>
    <ns1:""" + msgServiceCode + """>
      <desiredResponseSize>""" + messageSize + """</desiredResponseSize>
    </ns1:""" + msgServiceCode + """>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""))
        .check(
          status.is(200),
          // Check that the response ID in response matches the one sent in request (e.g. sessions do not get mixed and response is valid).
          substring("""<xrd:id>${xRoadRequestId}</xrd:id>"""),
          // Check that response message does not contain fault element
          substring("""<SOAP-ENV:Fault>""").notExists,
          // Extract mock timestamp from response so it would get saved in the logs and can be used for further analyzis.
          regex("""<mockTimeStamp>([\d]+)</mockTimeStamp>""").saveAs("mockTimeStamp")
        )
    )

  // Static XRoad warm-up scenario with 2kB message and ~1 req/s held for period defined above.
  val xRoadWarmUpScenario =
    scenario("Warm up")
      .during(warmUpHoldPeriod) {
        pace(1).group("Warm up") {
          makeXRoadRequest("2kB")
        }
      }
      .inject(atOnceUsers(1))

  // Dynamic XRoad main scenario generator with defined RPS held for period defined above.
  def makeXRoadMainScenario(nextScenarioDelay: FiniteDuration, rpsTarget: Int) =
    scenario("Main " + rpsTarget)
      .during(mainHoldPeriod) {
        pace(1).group(rpsTarget + " req/s") {
          randomSwitch(
            // Message size weights can be passed from command-line, see above.
            weight2kB -> makeXRoadRequest("2kB"),
            weight10kB -> makeXRoadRequest("10kB"),
            weight100kB -> makeXRoadRequest("100kB"),
            weight2MB -> makeXRoadRequest("2MB"),
            weight10MB -> makeXRoadRequest("10MB")
          )
        }
      }
      .inject(nothingFor(nextScenarioDelay), atOnceUsers(rpsTarget))

  // Add the XRoad warm-up scenario as the first scenario.
  var xRoadScenarios = List(xRoadWarmUpScenario)
  var nextScenarioDelay = warmUpHoldPeriod

  // Dynamically populate scenario list with different target RPS together with user ramp-up intervals.
  for (rpsTarget <- rpsTargets) {
    nextScenarioDelay += userBumpInterval
    xRoadScenarios = xRoadScenarios :+ makeXRoadMainScenario(nextScenarioDelay, rpsTarget.toInt)
    nextScenarioDelay += mainHoldPeriod
  }

  // Set up Gatling scenarios and do the performance testing.
  setUp(xRoadScenarios).protocols(httpConfig)

}

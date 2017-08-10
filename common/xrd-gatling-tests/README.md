# xrd-gatling-tests

This folder contains performance testing scripts and necessary data.

For further information, refer to section 4 (Performance testing) of the [X-Road automated testing documentation](../xrd-ui-tests-python/X-road%20automated%20testing%20documentation.md)

- [binaries](binaries) - Directory placeholder for performance testing binaries
- [results](results) - Directory placeholder for performance testing results
- [gatling.wsdl](gatling.wsdl) - WSDL file for performance test service
- [gatling-mock.xml](gatling-mock.xml) - SoapUI mock used for Gatling performance testing. As it needs to be lightweight, it has not been merged with other mock services.
- [soapui-settings-gatling.xml](soapui-settings-gatling.xml) - SoapUI settings file for performance testing.
- [XRoad.scala](XRoad.scala) - Performance testing script.
- [xRoad.sh](xRoad.sh) - Linux shell script for running the performance tests with Jenkins.
- [xroad-gatling.sh](xroad-gatling.sh) - Linux shell script for running the performance tests locally.

![Logo](https://github.com/ria-ee/X-Road/blob/develop/doc/Manuals/img/eu_regional_development_fund_horizontal_div_15.png "EU logo")
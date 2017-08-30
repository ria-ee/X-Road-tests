Harmonized Xroad test environment
===================

- Common test development environment to Finland and Estonia
	- Includes servers: CA, CENTRAL SERVER, MANAGEMENT SECURITY SERVER, SECURITY SERVERS
- Can be used for testing:
	- UI and integrations, SOAP testing, Service testing and Service mocks
	- Not for performance testing!
- Benefits:
	- Tests are compatible in Estonia and Finland common test environments
		- Re-usable tests
	- Test can be easily imported to own specific environment from LXD
	- Jenkins jobs are generated and we have harmonized test data in different test environments
	- LXD will easy up environment settings work
		->Harmonised test environments setups and SOAP  testing

Repositories to Xroad test development
-------------
- Xroad test development repositoryInstall oracle-virtualbox or use ubuntu16.04 Virtualbox
	- https://github.com/ria-ee/X-Road-tests
- LXD environment ansible scripts
	- https://github.com/vrk-kpa/X-Road
- Xroad lxd test environment configs and sensitive data repository
	- https://github.com/vrk-kpa/xroad-utils

**Xroad shared repository folder structure**

```
common
	xrd-ui-tests-qautomate
		tests
		pagemodel
		etc…
	xrd-ui-tests-python
		tests
		etc…
	xrd-mock-soapui
	xrd-jmeter-tests
	xrd-gatling-tests
```

Xroad-tests naming conventions
-------------
- Xroad server naming conventions
```
MEMBER_NAMES= MemberMGM, Member1, Member2, Member3
MEMBER_CODE=00000000,00000001,00000002, 00000003,
INSTANCE_IDENTIFIER=XRD1, XRD2
MEMBER_CLASS=GOV
MEMBER_CLASS_DESCRIPTION=Government
SUBSYSTEM_CODE = MANAGEMENT, SUB_MEMBER1, SUB_MEMBER2

USERNAME=xrd
PASSWORD=secret

KEY_NAMES=xrd-automation-key-auth, xrd-automation-key-sign, or xrd-automation-key-sign-123
```
- Ansible script use ”xroad”, ”Xroad” or ”XROAD”...just avoid country specific things

- Jenkins test set job names:
```
environment-project-test_type-test_description
E.g lxd-xrd-ui-regr-configure-cs-servers
E.g lxd-xrd-soap-regr-add-sub-member-message


Environment: lxd, stage, prod
Project: xrd
Test_type: ui, soap
Test_phase: regr, stress, perf
Test_description: test set description
```

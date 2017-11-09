Harmonized X-Road test environment
===================

- LXD based common test development environment to Finland and Estonia
	- Includes servers: CA, CENTRAL SERVER, MANAGEMENT SECURITY SERVER, SECURITY SERVERS
	    - https://github.com/ria-ee/X-Road/tree/develop/ansible
- Can be used for testing:
	- UI and integrations, SOAP testing, service testing and Service mocks
	- Not for performance testing!
- Benefits:
	- Tests are compatible between Estonia and Finland common test environments
		- Re-usable tests
	- Test can be easily imported to own specific environment from LXD
	- Jenkins jobs are created by the testing person who originally created the test case and by syncing the Jenkins jobs between countries via common Github repo, we have harmonized test data in different test environments
	- Less work settings up environment in LXD

X-Road test development repositories
-------------
X-Road test development master repository
	- https://github.com/ria-ee/X-Road-tests
- LXD environment Ansible scripts
	- https://github.com/vrk-kpa/X-Road
- X-Road LXD test environment configs and sensitive data repository
	- https://github.com/vrk-kpa/xroad-utils

**X-Road shared repository folder structure**

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

X-Road-tests naming conventions
-------------
- X-Road server naming conventions
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
- In Ansible scripts avoid using country specific terms e.g. Palveluväylä or X-Tee and use generic X-Road instead

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

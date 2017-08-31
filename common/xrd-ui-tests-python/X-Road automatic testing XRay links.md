# X-Road tests based on test cases #

| **X-Road test case** | **Jira link** | **Jenkins link** |
| --- | --- | --- |
| **2.1.3** | https://jira.ria.ee/browse/XT-457 | Helper scenario, not standalone, executed by other cases. |
| **2.1.3 failure scenarios** | https://jira.ria.ee/browse/XT-457 | http://xtee-guitest.ci.kit:8080/job/xroad_ss_client_certification_failures_2_1_3/ |
| **2.1.8** | https://jira.ria.ee/browse/XT-462 | Helper scenario, not standalone, executed by other cases. |
| **2.1.9** | https://jira.ria.ee/browse/XT-463 | Helper scenario, not standalone, executed by other cases. |
| **2.2.1** | https://jira.ria.ee/browse/XT-465 | http://xtee-guitest.ci.kit:8080/job/xroad_test_2_2_1-2_2_9/ |
| **2.2.2** | https://jira.ria.ee/browse/XT-466 | http://xtee-guitest.ci.kit:8080/job/xroad_test_2_2_1-2_2_9/ |
| **2.2.5** | https://jira.ria.ee/browse/XT-469 | http://xtee-guitest.ci.kit:8080/job/xroad_test_2_2_1-2_2_9/ |
| **2.2.6** | https://jira.ria.ee/browse/XT-470 | http://xtee-guitest.ci.kit:8080/job/xroad_test_2_2_1-2_2_9/ |
| **2.2.7** | https://jira.ria.ee/browse/XT-471 | http://xtee-guitest.ci.kit:8080/job/xroad_test_2_2_1-2_2_9/ |
| **2.2.8** | https://jira.ria.ee/browse/XT-472 | http://xtee-guitest.ci.kit:8080/job/xroad_test_2_2_1-2_2_9/ |
| **2.2.9** | https://jira.ria.ee/browse/XT-473 | http://xtee-guitest.ci.kit:8080/job/xroad_test_2_2_1-2_2_9/ |
| **2.9.1** | https://jira.ria.ee/browse/XT-509 | http://xtee-guitest.ci.kit:8080/job/xroad_changing_database_rows_with_cs_gui_291/ |
| **2.10.1** | https://jira.ria.ee/browse/XT-514 | http://xtee-guitest.ci.kit:8080/job/xroad_changing_database_rows_with_ss_gui_2_10_1/ |
| **2.11.1** | https://jira.ria.ee/browse/XT-518 | http://xtee-guitest.ci.kit:8080/job/xroad_logging_in_cs_2_11_1/ |
| **2.11.2** | https://jira.ria.ee/browse/XT-519 | http://xtee-guitest.ci.kit:8080/job/xroad_logging_service_ss_2_11_2/ |

## Test case use case coverage ##
| **X-Road test case** | **Use case coverage** |
| --- | --- |
| **2.1.3** | SS_28: 1-4, 5, 3a; SS_29: 1-4, 5, 6-8, 11, 4a, 4b; SS_30: 1-2, 4-15, 4a, 6a.1, 7a.1, 9a.1, 10a.1; TRUST_14: 1-4, 3a; TRUST_08: 1-4, 5 (b), 7-8, 10, 11a; TRUST_10: 1-4, 6, 7; SS_36: 1-4, 3a |
| **2.1.8** | SERVICE_04: 1-3; SERVICE_05: 1-3 |
| **2.1.9** | SERVICE_03: 1-3; SERVICE_05: 1-3 |
| **2.2.1** | **2.1.3** (helper used); MEMBER_10: 1-3, 4-5; MEMBER_47: 1-3, 4-5; MEMBER_48: 1-6; MEMBER_37: 1-5; MEMBER_13; MEMBER_26: 1-7; MEMBER_39: 1-4; MEMBER_52: 1-2, 3 (partial); MEMBER_53: 1-3, 4a |
| **2.2.2** | **2.1.8** (helper used); SERVICE_08: 1-7, 8, 9, 6c, no log check: 3a, 4a, 5a, 7a; SERVICE_10: 1-3, 1a, 2b, 3a; SERVICE_44: 1, 1a, 1b; SERVICE_09: 1-3; SERVICE_12: 1-2; SERVICE_21: 1-2, 4-5, 4a, 5a; SERVICE_15: 1-4, 3a |
| **2.2.5** | SERVICE_14: 1-6, 3b (partial), 3c, 4a, 5a (partial) |
| **2.2.6** | SERVICE_13: 1-4, 5; SERVICE_12: 1-2 |
| **2.2.7** | SS_11: 1-5; SS_12; MEMBER_49: 1-3; MEMBER_50: 1-4; SERVICE_19: 1-3, 4, 5, 6; SERVICE_20: 1-2; SERVICE_51: 1-4 |
| **2.2.8** | SERVICE_41: 1-3, 4-6; SERVICE_42: 1-3, 4-5; SERVICE_43: 1-4, 3a |
| **2.2.9** | **2.1.8** (helper used) |
| **2.9.1** | CS_01: 1-4; MEMBER_10: 1-2, 4-5; CS_02: 1-2; MEMBER_11: 1-3, 4; MEMBER_26: 1-7 |
| **2.10.1** | SS_01: 1-4; MEMBER_47: 1-2, 4-5; SS_02: 1-2; MEMBER_49: 1-3; MEMBER_53: 1-3, 4a |
| **2.11.1** | CS_01; MEMBER_10: 1-2, 4-5, 7; CS_02; MEMBER_11; SERVICE_32: 1-3, 4-6; SERVICE_33: 1-2, 3 (partial), 4; MEMBER_15: 1-3, 5-8, 10; MEMBER_39: 1-5, 7; MEMBER_26: 1-8 |
| **2.11.2** | **2.1.8** (helper used); CS_01: 1-4; MEMBER_10: 1-2, 4-5; SS_01; MEMBER_47: 1-2, 4-5, 6 (partial), 7; SERVICE_25: 1-3, 3a; SS_02; SERVICE_08: 1-7, 8 (partial), 9 (partial), 10; SERVICE_04; SERVICE_21; SERVICE_12 |

# X-Road tests based on use cases #

| **X-Road test package** | **Test** | **Use Case** | **Jira link** | **Comment** |
| --- | --- | --- | --- | --- |
| **xroad_cs_ca** |  |  |  |  |
| | **XroadAddCa** | TRUST_08 | https://jira.ria.ee/browse/XTKB-19 |  |
| | **XroadEditCa** | TRUST_09 | https://jira.ria.ee/browse/XTKB-68 |  |
| | **XroadDeleteCa** |  TRUST_14 | https://jira.ria.ee/browse/XTKB-69 |  |
| **xroad_cs_ocsp_responder** |  |  |  |
| | **XroadAddOcspResponder** | TRUST_10 | https://jira.ria.ee/browse/XTKB-20 |  |
| | **XroadDeleteOcspResponder** | TRUST_11 | https://jira.ria.ee/browse/XTKB-67 |  |
| **xroad_audit_log** |  |  |  |  |
| | **XroadAuditLog**  | Helper | https://jira.ria.ee/browse/XTKB-8 | Can be run as helper or standalone with a custom config.ini in working directory. |
| **xroad_parse_ users_input_SS_41** |  |  |  |  |
| | **UserInputParse**  | SS_41; SS_28 4, SS_29 5, 5a.1; SS_28 4; MEMBER_47 3, MEMBER_10 4, 6; MEMBER_11 3; SERVICE_13 4; SERVICE_19 3; SERVICE_32 3; SERVICE_41 3; SERVICE_42 3; SS_29 5 | https://jira.ria.ee/browse/XTKB-13 https://jira.ria.ee/browse/XTKB-14 https://jira.ria.ee/browse/XTKB-18 https://jira.ria.ee/browse/XTKB-48 https://jira.ria.ee/browse/XTKB-52 https://jira.ria.ee/browse/XKTB-54 https://jira.ria.ee/browse/XKTB-55 https://jira.ria.ee/browse/XTKB-56 https://jira.ria.ee/browse/XTKB-57 https://jira.ria.ee/browse/XTKB-58 https://jira.ria.ee/browse/XTKB-63 | Standalone component that tests different user input parsing scenarios. |


![Logo](https://raw.githubusercontent.com/ria-ee/X-Road/develop/doc/Manuals/img/eu_regional_development_fund_horizontal_div_15.png "EU logo")
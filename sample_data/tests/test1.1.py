import sys, os

sys.path.insert(0, os.path.realpath('./'))

from unittest import TestCase

from xray_helpers.analyzer import TruncatedPhysicalPlan


class TruncatedPhysPlanTestCase(TestCase):
    """This class is speccially for testing TruncatedPhysicalPlan class and its
     functionality"""

    def setUp(self):
        self.ppid = 30
        self.test_lines = [
            {
                "line": "17/09/07 03:01:09 INFO acceleratorGenerator: TakeOrderedAndProject(limit=100, orderBy=[d_year#98 ASC NULLS FIRST,sum_agg#154 DESC NULLS LAST,brand_id#152 ASC NULLS FIRST], output=[d_year#98,brand_id#152,brand#153,sum_agg#154]) [pid: -1, id: 1, inner: false, sid: 0]: {StructType(  StructField(d_year, integer, true),  StructField(brand_id, integer, true),  StructField(brand, string, true),  StructField(sum_agg, double, true))}",
                "expected_operator": "TakeOrderedAndProject",
                "expected_info": "[pid: -1, id: 1, inner: false, sid: 0]",
                "expected_arguments": ""
            },
            {
                "line": "+- WholeStageCodegen [pid: 1, id: 2, inner: false, sid: 0]: {StructType(  StructField(d_year, integer, true),  StructField(brand_id, integer, true),  StructField(brand, string, true),  StructField(sum_agg, double, true))}",
                "expected_operator": "+- WholeStageCodegen",
                "expected_info": "[pid: 1, id: 2, inner: false, sid: 0]",
                "expected_arguments": ""
            },
            {
                "line": "        :                    +- HashAggregate(keys=[ss_ticket_number#9, ss_customer_sk#3], functions=[count(1)], output=[ss_ticket_number#9, ss_customer_sk#3, cnt#216L], result=[ss_ticket_number#9, ss_customer_sk#3, count(1)#217L AS cnt#216L]) [pid: 11, id: 12, inner: false, sid: 1]: {StructType(  StructField(ss_ticket_number, integer, true),  StructField(ss_customer_sk, integer, true),  StructField(cnt, long, false))}",
                "expected_operator": "        :                    +- HashAggregate",
                "expected_info": "[pid: 11, id: 12, inner: false, sid: 1]",
                "expected_arguments": "count"
            },
            {
                "line": "         :           +- Exchange hashpartitioning(ss_customer_sk#3, 200) [pid: 8, id: 9, inner: false, sid: 1]: {StructType(  StructField(ss_ticket_number, integer, true),  StructField(ss_customer_sk, integer, true),  StructField(cnt, long, false))}",
                "expected_operator": "         :           +- Exchange",
                "expected_info": "[pid: 8, id: 9, inner: false, sid: 1]",
                "expected_arguments": "hashpartitioning"
            },
            {
                "line": "         :                                      +- BroadcastHashJoin [ss_hdemo_sk#5], [hd_demo_sk#106], Inner, BuildRight [pid: 17, id: 18, inner: false, sid: 2]: {StructType(  StructField(ss_customer_sk, integer, true),  StructField(ss_hdemo_sk, integer, true),  StructField(ss_ticket_number, integer, true),  StructField(hd_demo_sk, integer, true))}",
                "expected_operator": "         :                                      +- BroadcastHashJoin",
                "expected_info": "[pid: 17, id: 18, inner: false, sid: 2]",
                "expected_arguments": "Inner BuildRight"
            },
            {
                "line": "         :                                         :     :     :  +- Filter((((isnotnull(ss_sold_date_sk#0) && isnotnull(ss_store_sk#7)) && isnotnull(ss_hdemo_sk#5)) && isnotnull(ss_customer_sk#3))) [pid: 23, id: 24, inner: false, sid: 2]: {StructType(  StructField(ss_sold_date_sk, integer, false),  StructField(ss_customer_sk, integer, false),  StructField(ss_hdemo_sk, integer, false),  StructField(ss_store_sk, integer, false),  StructField(ss_ticket_number, integer, true))}",
                "expected_operator": "         :                                         :     :     :  +- Filter",
                "expected_info": "[pid: 23, id: 24, inner: false, sid: 2]",
                "expected_arguments": ""
            }
        ]

    def test_operator_extraction(self):
        """Checks TruncatedPhysPlanTestCase.extract_operator_from_line()
        function. Receives line and checks result with expected operator"""

        for item in self.test_lines:
            physplan = TruncatedPhysicalPlan(item["line"], self.ppid)
            self.assertEqual(physplan.operator, item["expected_operator"])

    def test_info_extraction(self):
        """Checks TruncatedPhysPlanTestCase.extract_info_from_line()
        function. Receives line and checks result with expected operator"""

        for item in self.test_lines:
            physplan = TruncatedPhysicalPlan(item["line"], self.ppid)
            self.assertEqual(physplan.info, item["expected_info"])

    def test_arguments_extraction(self):
        """Checks TruncatedPhysPlanTestCase.extract_arguments_from_line()
        function. Receives line and checks result with expected operator"""

        for item in self.test_lines:
            physplan = TruncatedPhysicalPlan(item["line"], self.ppid)
            self.assertEqual(physplan.arguments, item["expected_arguments"])

    def test_convert_to_string(self):
        """Checks TruncatedPhysPlanTestCase.__str__() function. Receives line
        and checks result with expected string representation"""

        for item in self.test_lines:
            physplan = TruncatedPhysicalPlan(item["line"], self.ppid)
            self.assertEqual(str(physplan),
                             " ".join([item["expected_operator"],
                                       item["expected_info"],
                                       item["expected_arguments"]]
                                      )
                             )


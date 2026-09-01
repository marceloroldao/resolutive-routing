import unittest

from resolutive_routing import CreditLedger, ResourceType


class LedgerTests(unittest.TestCase):
    def test_contribution_increases_credit(self):
        ledger = CreditLedger()
        ledger.contribute("node", ResourceType.COMPUTE, 100)
        self.assertEqual(ledger.balance("node", ResourceType.COMPUTE), 100)

    def test_consumption_decreases_credit(self):
        ledger = CreditLedger()
        ledger.consume("node", ResourceType.COMPUTE, 30)
        self.assertEqual(ledger.balance("node", ResourceType.COMPUTE), -30)

    def test_failed_job_does_not_receive_full_credit(self):
        ledger = CreditLedger()
        failed = ledger.contribute("node", ResourceType.COMPUTE, 100, success=False)
        self.assertLess(failed, 100)
        self.assertEqual(failed, 10)

    def test_resource_types_remain_separate(self):
        ledger = CreditLedger()
        ledger.contribute("node", ResourceType.KNOWLEDGE, 20)
        self.assertEqual(ledger.balance("node", ResourceType.COMPUTE), 0)


if __name__ == "__main__":
    unittest.main()


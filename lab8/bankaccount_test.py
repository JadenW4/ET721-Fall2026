import unittest

from bankaccount import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Peter Pan", 100)

    def test_initial_balance(self):
        self.assertEqual(self.account.get_balance(), 100)

    def test_deposit(self):
        self.account.deposit(50)
        self.assertEqual(self.account.get_balance(), 150)

    def test_withdraw(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.get_balance(), 70)

    def test_withdraw_more_than_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(150)

    def test_deposit_and_withdraw_sequence(self):
        self.account.deposit(50)
        self.account.withdraw(25)
        self.account.deposit(100)
        self.account.withdraw(75)

        self.assertEqual(self.account.get_balance(), 150)


if __name__ == "__main__":
    unittest.main()
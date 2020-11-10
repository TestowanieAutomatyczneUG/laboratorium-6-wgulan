import math
import unittest

def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    def format_as_dollars(amount):
        return f"${amount:0,.2f}"

    for perf in invoice['performances']:
        play = plays[perf['playID']]
        if play['type'] == "tragedy":
            this_amount = 40000
            if perf['audience'] > 30:
                this_amount += 1000 * (perf['audience'] - 30)
        elif play['type'] == "comedy":
            this_amount = 30000
            if perf['audience'] > 20:
                this_amount += 10000 + 500 * (perf['audience'] - 20)

            this_amount += 300 * perf['audience']

        else:
            raise ValueError(f'unknown type: {play["type"]}')

        # add volume credits
        volume_credits += max(perf['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play["type"]:
            volume_credits += math.floor(perf['audience'] / 5)
        # print line for this order
        result += f' {play["name"]}: {format_as_dollars(this_amount/100)} ({perf["audience"]} seats)\n'
        total_amount += this_amount

    result += f'Amount owed is {format_as_dollars(total_amount/100)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result

class statementTest(unittest.TestCase):

    def test_comedy_audience_more_than_30(self):
        self.assertEqual("Statement for BigCo\n As You Like It: $580.00 (35 seats)\nAmount owed is $580.00\nYou earned 12 credits\n",
                         statement({"customer": "BigCo", "performances": [{"playID": "as-like","audience": 35}]},
                                   {"as-like": {"name": "As You Like It", "type": "comedy"}}))
    def test_comedy_audience_less_than_30(self):
        self.assertEqual(
            "Statement for BigCo\n As You Like It: $360.00 (20 seats)\nAmount owed is $360.00\nYou earned 4 credits\n",
            statement({"customer": "BigCo", "performances": [{"playID": "as-like", "audience": 20}]},
                      {"as-like": {"name": "As You Like It", "type": "comedy"}}))

    def test_tragedy_audience_less_than_20(self):
        self.assertEqual(
            "Statement for BigCo\n Hamlet: $400.00 (10 seats)\nAmount owed is $400.00\nYou earned 0 credits\n",
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet", "audience": 10}]},
                      {"hamlet": {"name": "Hamlet", "type": "tragedy"}}))

    def test_tragedy_audience_more_than_20(self):
        self.assertEqual(
            "Statement for BigCo\n Hamlet: $500.00 (40 seats)\nAmount owed is $500.00\nYou earned 10 credits\n",
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet", "audience": 40}]},
                      {"hamlet": {"name": "Hamlet", "type": "tragedy"}}))

    def test_tragedy_audience_more_than_20_and_comedy_audience_more_than_30(self):
        self.assertEqual(
            "Statement for BigCo\n Hamlet: $500.00 (40 seats)\n As You Like It: $580.00 (35 seats)\nAmount owed is $1,080.00\nYou earned 22 credits\n",
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet","audience": 40}, {"playID": "as-like","audience": 35}]},
                      {"hamlet": {"name": "Hamlet", "type": "tragedy"}, "as-like": {"name": "As You Like It", "type": "comedy"}}))

    def test_tragedy_audience_less_than_20_and_comedy_audience_more_than_30(self):
        self.assertEqual(
            "Statement for BigCo\n Hamlet: $400.00 (10 seats)\n As You Like It: $580.00 (35 seats)\nAmount owed is $980.00\nYou earned 12 credits\n",
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet","audience": 10}, {"playID": "as-like","audience": 35}]},
                      {"hamlet": {"name": "Hamlet", "type": "tragedy"}, "as-like": {"name": "As You Like It", "type": "comedy"}}))

    def test_tragedy_audience_more_than_20_and_comedy_audience_less_than_30(self):
        self.assertEqual(
            "Statement for BigCo\n Hamlet: $500.00 (40 seats)\n As You Like It: $330.00 (10 seats)\nAmount owed is $830.00\nYou earned 12 credits\n",
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet","audience": 40}, {"playID": "as-like","audience": 10}]},
                      {"hamlet": {"name": "Hamlet", "type": "tragedy"}, "as-like": {"name": "As You Like It", "type": "comedy"}}))

    def test_tragedy_audience_less_than_20_and_comedy_audience_less_than_30(self):
        self.assertEqual(
            "Statement for BigCo\n Hamlet: $400.00 (5 seats)\n As You Like It: $315.00 (5 seats)\nAmount owed is $715.00\nYou earned 1 credits\n",
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet","audience": 5}, {"playID": "as-like","audience": 5}]},
                      {"hamlet": {"name": "Hamlet", "type": "tragedy"}, "as-like": {"name": "As You Like It", "type": "comedy"}}))

    def test_no_performances(self):
        self.assertEqual(
            "Statement for BigCo\nAmount owed is $0.00\nYou earned 0 credits\n",
            statement({"customer": "BigCo", "performances": []},
                      {"hamlet": {"name": "Hamlet", "type": "tragedy"}}))

    def test_empty_plays_raises_key_error(self):
        with self.assertRaises(KeyError):
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet", "audience": 10}]}, {})

    def test_no_play_with_given_id_raises_key_error(self):
        with self.assertRaises(KeyError):
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet", "audience": 10}]},
                      {"othello": {"name": "Othello", "type": "tragedy"}})

    def test_no_audience_raises_key_error(self):
        with self.assertRaises(KeyError):
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet"}]},
                      {"hamlet": {"name": "Hamlet", "type": "tragedy"}})

    def test_wrong_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            statement({"customer": "BigCo", "performances": [{"playID": "hamlet", "audience": 10}]},
                      {"hamlet": {"name": "Hamlet", "type": "asdasd"}})

    def test_empty_invoice_raises_key_error(self):
        with self.assertRaises(KeyError):
            statement({}, {"hamlet": {"name": "Hamlet", "type": "asdasd"}})


if __name__ == "__main__":
    unittest.main()
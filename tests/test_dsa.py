import unittest
from dsa import Queue, linear_search, merge_sort

class DsaTests(unittest.TestCase):
    def test_queue_is_fifo(self):
        q = Queue(); q.enqueue('a'); q.enqueue('b')
        self.assertEqual(q.dequeue(), 'a')
        self.assertEqual(q.dequeue(), 'b')
        self.assertTrue(q.is_empty())

    def test_linear_search_is_case_insensitive(self):
        rows = [{'question_text': 'SQL basics'}, {'question_text': 'Normalization'}]
        self.assertEqual(len(linear_search(rows, 'sql', 'question_text')), 1)

    def test_merge_sort_descending(self):
        rows = [{'score': 5}, {'score': 12}, {'score': 8}]
        self.assertEqual([r['score'] for r in merge_sort(rows, key=lambda x: x['score'], reverse=True)], [12, 8, 5])

if __name__ == '__main__':
    unittest.main()

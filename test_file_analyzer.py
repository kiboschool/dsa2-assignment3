import unittest
import io
import sys
from file_analyzer import FileAnalyzer

class TestLoginManager(unittest.TestCase):
    def setUp(self):
        self.analyzer = FileAnalyzer()

    def test_add_one_document(self):
        self.analyzer.add_document('examples/example1.txt')
        self.assertEqual(len(self.analyzer.index), 129)
        self.assertEqual(self.analyzer.index['town'][0][0], -2)
        self.assertEqual(self.analyzer.index['town'][0][1], 'examples/example1.txt')
        self.assertEqual(self.analyzer.index['town'][0][2],
            [
             'tranquil town, leaving a trail of destruction in its wake.\n',
             'stand united, determined to rebuild their beloved town from the ashes. Though the road\n'
            ])

    def test_add_two_documents(self):
        self.analyzer.add_document('examples/example1.txt')
        self.analyzer.add_document('examples/example4.txt')
        self.assertEqual(len(self.analyzer.index), 167)
        self.assertEqual(self.analyzer.index['town'][0][0], -2)
        self.assertEqual(self.analyzer.index['town'][0][1], 'examples/example1.txt')
        self.assertEqual(self.analyzer.index['springs'][0][0], -4)
        self.assertEqual(self.analyzer.index['springs'][0][1], 'examples/example4.txt')

    def test_top_k_documents_one_document(self):
        self.analyzer.index = {}
        self.analyzer.index['town'] = [(
            -2,
            'examples/example1.txt',
            [
             'tranquil town, leaving a trail of destruction in its wake.\n',
             'stand united, determined to rebuild their beloved town from the ashes. Though the road\n'
            ]
        )]
        self.assertEqual(self.analyzer.top_k_documents('town', 1), ['examples/example1.txt'])

    def test_top_k_documents_four_documents(self):
        self.analyzer.index = {}
        self.analyzer.index['earthquake'] = [
            (-3, 'examples/example2.txt', ['Earthquake Ravages Sandstone Springs: Residents Grapple with Devastation\n', 'serene ambiance, was rocked by a powerful earthquake in the early morning hours.\n', 'The earthquake, measuring 6.8 on the Richter scale, struck with relentless force,\n']),
            (-3, 'examples/example4.txt', ['Sandstone Springs Rallies Together After Catastrophic Earthquake\n', 'rocked by a catastrophic earthquake in the early hours of the morning. The\n', 'earthquake, measuring 6.8 on the Richter scale, sent shockwaves rippling through\n']),
            (-1, 'examples/example3.txt', ['tight-knit community, was struck by a powerful earthquake in the early hours of the\n']),
            (-2, 'examples/example1.txt', ['Catastrophic Earthquake Hits Sandstone Springs: Community Unites in Face of Disaster\n', 'by a devastating earthquake in the early hours of the morning. The quake, registering\n'])
        ]
        self.assertEqual(self.analyzer.top_k_documents('earthquake', 3), ['examples/example2.txt', 'examples/example4.txt', 'examples/example1.txt'])

    def test_top_k_contexts_one_document(self):
        self.analyzer.index = {}
        self.analyzer.index['town'] = [(
            -2,
            'examples/example1.txt',
            [
             'tranquil town, leaving a trail of destruction in its wake.\n',
             'stand united, determined to rebuild their beloved town from the ashes. Though the road\n'
            ]
        )]
        self.assertEqual(self.analyzer.top_k_contexts('town', 1), ['tranquil town, leaving a trail of destruction in its wake.\n'])

    def test_top_k_contexts_two_documents(self):
        self.analyzer.index = {}
        self.analyzer.index['town'] = [(
            -2,
            'examples/example1.txt',
            [
             'tranquil town, leaving a trail of destruction in its wake.\n',
             'stand united, determined to rebuild their beloved town from the ashes. Though the road\n'
            ]
        ),
        (
            -1,
            'examples/example4.txt',
            [ 'tranquil town.\n' ]
        )]
        self.assertEqual(self.analyzer.top_k_contexts('town', 3), [
            'tranquil town, leaving a trail of destruction in its wake.\n',
            'stand united, determined to rebuild their beloved town from the ashes. Though the road\n',
            'tranquil town.\n'
        ])

    def test_similarity_score(self):
        self.assertEqual(self.analyzer.similarity_score('kitten', 'sitting'), 3)

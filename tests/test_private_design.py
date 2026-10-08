"""Documentation contract, not security verification of an unbuilt runtime."""
import unittest
from pathlib import Path

class PrivateDesign(unittest.TestCase):
    def test_explicit_boundaries(self):
        text=(Path(__file__).resolve().parents[1]/'docs/private-local-design.md').read_text()
        for phrase in ['Status: design only', 'outside the repository', 'no real input/output',
                       'No silent cloud sync', 'SQLite alone is not an encryption solution',
                       'using invented data', 'Network', 'Idempotency', 'Recovery',
                       'No broker login/trade execution', 'documentation only']:
            with self.subTest(phrase=phrase):self.assertIn(phrase,text)
        self.assertNotIn('docs.google.com',text)
        self.assertNotIn('@gmail.com',text)
        self.assertNotIn('1lejg96',text)

if __name__=='__main__':unittest.main()

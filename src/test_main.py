import os
import shutil
import unittest

from main import copy_site_contents


class TestMain(unittest.TestCase):
    def test_copy_site_contents(self):
        public_dir = os.path.join(".", "public")
        if os.path.exists(public_dir):
            dir_contents = os.listdir(os.path.join(".", "public"))
            self.assertEqual(len(dir_contents), 0)
        copy_site_contents()
        dir_contents = os.listdir(os.path.join(".", "public"))
        self.assertGreaterEqual(len(dir_contents), 1)
        shutil.rmtree(public_dir)


if __name__ == "__main__":
    unittest.main()

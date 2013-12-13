import os
import shutil
class BasicOperations_TestClass:

    TEST_ROOT =' __test_root__'

    def setUp(self):
        self.regenerate_root
        print(self.TEST_ROOT)
        assert os.path.isdir(self.TEST_ROOT)

    def tearDown(self):
        return True

    def test_test(self):
        assert self.bar == 1

    def regenerate_root(self):
        if os.path.isdir(self.TEST_ROOT):
            shutil.rmtree(self.TEST_ROOTT)
        os.makedirs(self.TEST_ROOT)

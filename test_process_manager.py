import os
import unittest

from process_manager import ProcessManagerError, terminate_process


class ProcessManagerTests(unittest.TestCase):
    def test_refuses_invalid_pid(self):
        for pid in (0, -1):
            with self.assertRaises(ProcessManagerError):
                terminate_process(pid)

    def test_refuses_own_pid(self):
        with self.assertRaises(ProcessManagerError):
            terminate_process(os.getpid())


if __name__ == "__main__":
    unittest.main()

import unittest
import tempfile

from backend import Backend, NoActiveTask, TaskAlreadyActive

class Test(unittest.TestCase):

    def get_dir(self):
        return tempfile.mkdtemp(prefix="timetracer-test")

    def get_backend(self):
        return Backend(self.get_dir())


    #---------------------------------------------------------


    def test_stop_on_empty_repository(self):
        backend = self.get_backend()
        self.assertRaises(NoActiveTask, backend.stop)


    def test_continue_on_empty_repository(self):
        backend = self.get_backend()
        self.assertRaises(ValueError, backend.continue_last)


    def test_history_on_empty_repository(self):
        backend = self.get_backend()
        max_category, max_name, result = backend.history()

        self.assertEquals(0, max_category)
        self.assertEquals(0, max_name)
        self.assertEquals(0, len(list(result)))


    def test_start_on_empty_repository(self):
        backend = self.get_backend()
        backend.start('category', 'task')

        max_category, max_name, result = backend.history()
        result = list(result)[0]

        self.assertEquals('category', result.get_category())
        self.assertEquals('task',     result.get_name())
        self.assertEquals(result.get_start_time(), result.get_end_time())


    def test_start_the_same_task_again(self):
        backend = self.get_backend()
        def commands():
            backend.start('category', 'task')
            backend.start('category', 'task')

        self.assertRaises(TaskAlreadyActive, commands)


    def test_stop_when_no_task_is_active(self):
        backend = self.get_backend()
        def commands():
            backend.start('category', 'task')
            backend.stop()
            backend.stop()

        self.assertRaises(NoActiveTask, commands)


    def test_continue_already_running_task(self):
        backend = self.get_backend()
        def commands():
            backend.start('category', 'task')
            backend.continue_last()

        self.assertRaises(TaskAlreadyActive, commands)


    def test_start_stop(self):
        backend = self.get_backend()
        backend.start('category',  'task')
        backend.start('category2', 'task2')
        backend.stop()

        max_category, max_name, result = backend.history()
        result = list(result)

        self.assertEquals(2, len(result))
        self.assertEquals('category2', result[0].get_category())
        self.assertEquals('task2',     result[0].get_name())
        self.assertEquals('category',  result[1].get_category())
        self.assertEquals('task',      result[1].get_name())


    def test_continue(self):
        backend = self.get_backend()
        backend.start('category',  'task')
        backend.start('category2', 'task2')
        backend.stop()
        backend.continue_last()

        max_category, max_name, result = backend.history()
        result = list(result)[0]

        self.assertEquals('category2', result.get_category())
        self.assertEquals('task2',     result.get_name())


if __name__ == '__main__':
    unittest.main()


import os
import os.path
import time
from time import strptime, strftime

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class NoActiveTask(Exception):
    pass

class TaskAlreadyActive(Exception):
    pass

class Item:
    def __init__(self, category, name, what, t):
        self.category = category
        self.name     = name
        self.what     = what
        self.time     = t

        assert what in ('start', 'stop')
        assert name != ""


    def is_running(self):
        return self.what == "start"


    def __str__(self):
        return '%s:%s\t%s\t%s' % (self.category, self.name, strftime(TIME_FORMAT, self.time), self.what)


    @staticmethod
    def fromstr(s):
        tmp = s.rstrip().split(':', 1)
        assert len(tmp) == 2
        category, tmp = tmp

        tmp = tmp.split('\t')
        assert len(tmp) == 3

        name = tmp[0]
        what = tmp[2]
        time = strptime(tmp[1], TIME_FORMAT)

        return Item(category, name, what, time)


class Status:
    def __init__(self, category, name, start_time, end_time = None):
        self.category = category
        self.name     = name
        self.start    = start_time
        self.end      = end_time

    def get_category(self):
        return self.category

    def get_name(self):
        return self.name

    def is_running(self):
        return self.end == None

    def get_start_time(self):
        return self.start


    def get_end_time(self):
        if self.is_running():
            return time.localtime()
        else:
            return self.end

    def get_timespan(self):

        t1 = int(time.mktime(self.get_start_time()))
        t2 = int(time.mktime(self.get_end_time()))

        return t2 - t1


class IOInterface:

    def __init__(self, directory):
        self.dir  = directory
        self.file = 'registry'
        self.path = os.path.join(self.dir, self.file)

        self.__initialized = False
        self.__pending = []
        self.__items = None


    def get_items(self):
        self.__initialize()
        self.__load_all()

        return self.__items


    def get_last(self):
        try:
            return self.get_items()[-1]
        except IndexError:
            return


    def append(self, item):
        self.__pending.append(item)


    def commit(self):
        if len(self.__pending) == 0:
            return

        with open(self.path, 'at') as f:
            for item in self.__pending:
                f.write(str(item))
                f.write('\n')

        self.__git("add %s" % self.path)
        self.__git('commit -m "%s"' % "update")

        if self.__items is not None:
            self.__items.extend(self.__pending)
            self.__pending = []


    def __initialize(self):
        if self.__initialized:
            return

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        if not os.path.exists(os.path.join(self.dir, '.git')):
            self.__git("init")

        self.__initialized = True


    def __load_all(self):
        if self.__items is not None:
            return

        self.__items = []
        if os.path.exists(self.path):
            with open(self.path, 'rt') as f:
                for index, line in enumerate(f):
                    self.__items.append(Item.fromstr(line))


    def __execute(self, command):
        ret = os.system(command)
        if ret != 0:
            raise ValueError("Command '%s' returned non-zero %d status" % (command, ret))


    def __git(self, params):
        self.__execute('git --git-dir=%s --work-tree=%s %s > /dev/null' % (
            os.path.join(self.dir, '.git'),
            self.dir,
            params
        ));


class Backend:
    def __init__(self, directory):
        self.io = IOInterface(directory)


    @property
    def dir(self):
        return self.io.dir


    def get_status(self):

        last = self.io.get_last()
        if last is None:
            return None

        if last.is_running():
            return Status(last.category, last.name, last.time)

        items = self.io.get_items()

        prev = items[-2]
        assert prev.is_running() == True
        assert last.category == prev.category
        assert last.name == prev.name

        return Status(last.category, last.name, prev.time, last.time)


    def start(self, category, name):

        previous = None
        last = self.io.get_last()

        if last and last.is_running():
            if category == last.category and name == last.name:
                raise TaskAlreadyActive()

            item = Item(last.category, last.name, 'stop', time.localtime())
            self.io.append(item)

            previous = self.get_status()

        item = Item(category, name, 'start', time.localtime())
        self.io.append(item)
        self.io.commit()

        return (previous, self.get_status())


    def history(self):

        items = self.io.get_items()

        result = []

        max_category = 0
        max_name     = 0

        for i in range(0, len(items), 2):
            first = items[i]
            try:
                second = items[i+1]
            except IndexError:
                second = None

            max_category = max(max_category, len(first.category))
            max_name     = max(max_name, len(first.name))

            if second:
                assert first.category == second.category
                assert first.name == second.name
                assert first.is_running() == True
                assert second.is_running() == False

                result.append(Status(first.category, first.name, first.time, second.time))
            else:
                result.append(Status(first.category, first.name, first.time))

        return max_category, max_name, reversed(result)


    def stop(self):

        last = self.io.get_last()

        if last and last.is_running():
            item = Item(last.category, last.name, 'stop', time.localtime())

            self.io.append(item)
            self.io.commit()
            return self.get_status()

        raise NoActiveTask()


    def last(self):
        last = self.io.get_last()
        if last is None:
            raise ValueError("no tasks in the history")

        return last


    def continue_last(self):
        last = self.last()

        if last.is_running():
            raise TaskAlreadyActive()
        else:
            return self.start(last.category, last.name)[1]

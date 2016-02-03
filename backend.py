import os
import os.path
import time
from time import strptime, strftime

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class NoActiveTask:
    pass

class TaskAlreadyActive:
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


class Backend:

    def __init__(self):
        self.dir  = os.path.expanduser('~/.local/tracker')
        self.file = 'registry'
        self.path = os.path.join(self.dir, self.file)

        self.items = None


    def init(self):

        if self.items is not None:
            return

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
            self.git("init")

        self.__load()
        assert self.items is not None


    def get_status(self):

        self.init()

        if len(self.items):

            last = self.items[-1]
            if last.is_running():

                return Status(last.category, last.name, last.time)
            else:

                prev = self.items[-2]
                assert prev.is_running() == True
                assert last.category == prev.category
                assert last.name == prev.name

                return Status(last.category, last.name, prev.time, last.time)
        else:
            return None


    def start(self, category, name):

        self.init()

        previous = None

        if len(self.items):
            last = self.items[-1]
            if last.is_running():
                if category == last.category and name == last.name:
                    raise TaskAlreadyActive()

                item = Item(last.category, last.name, 'stop', time.localtime())
                self.items.append(item)

                previous = self.get_status()

        item = Item(category, name, 'start', time.localtime())
        self.items.append(item)

        self.save()

        return (previous, self.get_status())


    def history(self):

        self.init()

        result = []

        max_category = 0
        max_name     = 0

        for i in xrange(0, len(self.items), 2):
            first = self.items[i]
            try:
                second = self.items[i+1]
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

        self.init()

        if len(self.items):
            last = self.items[-1]
            if last.is_running():
                item = Item(last.category, last.name, 'stop', time.localtime())
                self.items.append(item)

                self.save()
                return self.get_status()

        raise NoActiveTask()


    def continue_last(self):

        self.init()

        if len(self.items):
            last = self.items[-1]
            if last.is_running():
                raise TaskAlreadyActive()
            else:
                return self.start(last.category, last.name)[1]
        else:
            raise ValueError("no tasks in the history")


    def __load(self):
        self.items = []
        if os.path.exists(self.path):
            with open(self.path, 'rt') as f:
                for index, line in enumerate(f):
                    self.items.append(Item.fromstr(line))

    def save(self):
        tmp = os.path.join(self.dir, 'tmp')
        with open(tmp, 'wt') as f:
            for item in self.items:
                f.write(str(item))
                f.write('\n')

        os.rename(tmp, self.path)
        self.git("add %s" % self.path)
        self.git('commit -m "%s"' % "update")

    def __execute(self, command):

        ret = os.system(command)
        if ret != 0:
            raise ValueError("Command '%s' returned non-zero %d status" % (command, ret))

    def git(self, params):
        self.__execute('git --git-dir=%s --work-tree=%s %s > /dev/null' % (
            os.path.join(self.dir, '.git'),
            self.dir,
            params
        ));

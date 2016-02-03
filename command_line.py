class WrongOption(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class CommandLine:

    def __init__(self, arguments):
        self.category = ""
        self.name     = ""

        argv = arguments[:]

        if len(argv) == 0:
            self.command = "status"
            return

        if argv[0] == '--':
            self.command = "start"
            del argv[0]
        else:
            valid_commands = ("stop", "status", "continue", "history", "report", "config")
            if argv[0] in valid_commands:
                self.command = argv[0]
                del argv[0]
            else:
                self.command = "start"

        if len(argv) == 0:
            return

        tmp = ' '.join(argv)

        def normalize(s):
            return ' '.join(s.split())

        try:
            category, name = tmp.split(':', 1)

            self.category = normalize(category)
            self.name = normalize(name)
        except ValueError:
            self.category = ""
            self.name = normalize(tmp)

    def get_command(self):
        return self.command

    def get_category(self):
        return self.category

    def get_name(self):
        return self.name


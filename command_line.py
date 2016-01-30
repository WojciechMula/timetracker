class WrongOption(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class CommandLine:

    def __init__(self, argv):
        self.category = ""
        self.name     = ""

        if len(argv) == 0:
            self.command = "status"
            return

        valid_commands = ("stop", "start", "status", "continue", "history", "report", "config")
        if argv[0] not in valid_commands:
            raise WrongOption("Invalid command '%s'" % argv[0])

        self.command = argv[0]

        if len(argv) == 1:
            if self.command == "start":
                self.command = "continue"

            return

        tmp = ' '.join(argv[1:])

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


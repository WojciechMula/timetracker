import argparse

class CommandLine:
    def __init__(self, arguments):
        if not arguments:
            self.command = 'status'
            return

        valid_choices = ("start", "stop", "status", "continue", "history", "report", "config", "last")
        ap = argparse.ArgumentParser(description="Track you activity")
        ap.add_argument("command",
                        metavar="COMMAND",
                        choices=valid_choices,
                        help="%s" % (', '.join(sorted(valid_choices))))
        ap.add_argument("name",
                        metavar="NAME",
                        nargs='*',
                        help="name of task")


        args = ap.parse_args(arguments)
        if args.command == 'start':
            if not args.name:
                ap.error("name of task is required")
        else:
            if args.name:
                ap.error("given command does not require any name")

        tmp = ' '.join(args.name)

        self.command  = args.command
        try:
            self.category, self.name = tmp.split(':', 1)
        except ValueError:
            self.category = ""
            self.name     = tmp


    def get_command(self):
        return self.command

    def get_category(self):
        return self.category

    def get_name(self):
        return self.name


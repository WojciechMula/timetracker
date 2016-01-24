================================================================================
                            Time tracker
================================================================================

Basic usage
--------------------------------------------------

Start a task::

    tracker start taskname

Stop the active task::

    tracker stop

Continue the last running task::

    tracer start
    tracer continue

Show status::

    tracker
    tracker status

Examples::

    $ tracer start my new project
    Task "my new project" has started at 8:00 (2016-01-24)
    
    $ tracer
    Task "my new project" is running for 1:50h since 8.00

    $ tracer start homework
    Task "my new project" has been stopped (2:15h)
    Task "homework" started at (10:15 2016-01-24)


Taksname pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Taskname could be a single string. Each task can be **categorized**, the category
name have have to be separated by colon, for example::

    $ tracer start homepage:clean the mess
    Task "clean the mess" (homepage) started at ...


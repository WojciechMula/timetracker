================================================================================
                            Time tracker
================================================================================

Basic usage
--------------------------------------------------

Start a task::

    track taskname

Stop the active task::

    track stop

Continue the last running task::

    track continue

Show status::

    track

Examples::

    $ track my new project
    Task "my new project" has started at 8:00 (2016-01-24)
    
    $ track
    Task "my new project" is running for 1:50h since 8.00

    $ track homework
    Task "my new project" has been stopped (2:15h)
    Task "homework" started at (10:15 2016-01-24)


Taksname pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Taskname could be a single string. Each task can be **categorized**, the category
name have have to be separated by colon, for example::

    $ track homepage:clean the mess
    Task "clean the mess" (homepage) started at ...


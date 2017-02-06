================================================================================
                            Time tracker
================================================================================


Introduction
--------------------------------------------------

I use great web-app `toggl.com`__ for track my time at work. Although **toogl**
has got a lot of great features, I use it merely to record when I started and
finished a day.

__ http://toggl.com

I wanted an app which works off-line and allows me to record how much time I
spend on certain task. Of course, I could do the same writing down times, but
it is not the point.  Initially it was designed for tracking status of learning
English, i.e. for how long and how often I study. I had a pretty tough time
when I felt I didn't make any progress. This tiny utility saved me, as I could
monitor myself -- numbers don't lie.

Later I found it useful to track time spend on side projects, writing articles
for my website, processing pictures I took and so on, so forth.  Sometimes it is
interesting just to see how we spend leisure time.


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


Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Working ``git`` command.

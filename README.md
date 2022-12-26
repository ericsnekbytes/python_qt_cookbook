# SnekByte's Python Qt Cookbook

*(This doc is being actively edited, check back for updates)*

This cookbook is here to provide SIMPLE examples of how to do
common things when making apps with Qt in Python. Qt is extremely
flexible and powerful, but that sometimes means that it can be
complicated or cumbersome to do certain things.

The cookbook aims to cover a lot of common tasks, and demonstrate
concepts that are useful for Python Qt developers to know. This README
provides descriptions of all the code in this repo (below), along with
some high level overviews of Qt concepts and common gotchas/issues.

There are a few different Python Qt libraries (PySide, PyQt), and
while these libraries are nearly identical, some minor differences
exist. The app_simple examples provide working sample code for all
of the major libraries. The rest of the examples target PySide6.
It should be easy to use any of the examples, whether you're using
PySide6, PySide2, or PyQt5.

# Before You Start

See the setup section below if you need help getting set up running
the examples here.

# What's Covered In This Cookbook Project

Lightning summary/bullet points:
- Basic app initialization and startup
- Layouts
- Custom widgets
- Many standard widgets and controls
- Signals/slots
- Model/view features (tables, lists, etc.)
- Common gotchas/issues

As noted above, basic app initialization and startup, custom widgets,
layouts, and many common standard widgets and controls are covered here.
There are also samples of the Qt model/view features, which are typically
used to display tables and lists of data (this is QT's implementation of
the [MVC/Model-View-Controller design pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)).

Right now, the demos in this repo use the programmatic API (meaning
you write code to define the look and logic of your app). Qt also has
its own declarative UI language called QML that can potentially make
it easier to read and understand the layout of an application. Some
QML samples should be coming in the future.

# Things You Should Know

## Layouts

Qt's [layout system](https://doc.qt.io/qt-6/layout.html) is unique. Qt uses a
collaborative layout philosophy, where child widgets in a layout ask for space,
and the layout tries to accommodate each of them as best it can. This can lead
to some frustrating behaviors, as seemingly bizarre widget spacing or alignment
problems can pop up if you don't have a good grasp of how things work.

Widgets can compete for space, like unruly children, so a problem with one
widget might actually have its root cause in another competing widget in the
layout. When widgets have competing goals, the layout, like a patient parent,
will try to compromise and satisfy both of them as best it can.

For example, if two widgets in a layout have a "take all available vertical space"
behavior (if both have a vertical `sizePolicy` of `minimumExpanding`, for example),
the layout will first try to give all children at least as much space as their
`sizeHint()` suggests, and any leftover space will generally be split between the
two greedy widgets.

### There's too much space between my widgets!

<img width="344" alt="image" src="https://user-images.githubusercontent.com/104786633/206923177-c6898e00-7824-49d7-b745-8b0f62082c05.png">

If you find yourself with large, unwanted space between your widgets, a good way to solve that is to add a stretchable space in the layout to push your widgets up/down or left/right.

Code for the left layout:

```
  layout = QVBoxLayout()

  push_a = QPushButton('Run A')
  layout.addWidget(push_a)

  push_b = QPushButton('Run B')
  layout.addWidget(push_b)

  push_c = QPushButton('Run C')
  layout.addWidget(push_c)

  push_d = QPushButton('Run D')
  layout.addWidget(push_d)

  push_e = QPushButton('Run E')
  layout.addWidget(push_e)
```

Code for the middle layout:

```
  layout = QVBoxLayout()
  layout.addStretch()

  push_a = QPushButton('Run A')
  layout.addWidget(push_a)

  push_b = QPushButton('Run B')
  layout.addWidget(push_b)

  push_c = QPushButton('Run C')
  layout.addWidget(push_c)

  push_d = QPushButton('Run D')
  layout.addWidget(push_d)

  push_e = QPushButton('Run E')
  layout.addWidget(push_e)
```

Code for the right layout:

```
  layout = QVBoxLayout()

  push_a = QPushButton('Run A')
  layout.addWidget(push_a)

  push_b = QPushButton('Run B')
  layout.addWidget(push_b)

  push_c = QPushButton('Run C')
  layout.addWidget(push_c)
  layout.addStretch()

  push_d = QPushButton('Run D')
  layout.addWidget(push_d)

  push_e = QPushButton('Run E')
  layout.addWidget(push_e)
```

You're not really aligning your widgets to the top/bottom, in reality, `addStretch()` adds a `QSpacerItem` that requests/consumes extra vertical space from the layout in the example above. This reflects Qt's collaborative layout philosophy, where each widget tells the layout how much space it wants. The buttons above don't want any extra vertical space, but a QSpacerItem will request as much space as it can get, so it takes any extra space that's left over after the buttons take up what little vertical space they need.

## Signals and slots

*(This section is not finished)*

Signals and slots are used to pass data around between different places in
your Qt applications.

# Code Overview

You can browse the source code files above, or clone the repository
to download and run them yourself. See the Setup section if you need
more details.

## `app_simple_*.py` examples



Covered in `app_simple_*.py` modules:

- Basic app startup
- Simple nested layouts
- Custom widgets
- Standard widgets/controls
- A basic signal/slot example

## `app_table_word_pairs` example

<img width="678" alt="image" src="https://user-images.githubusercontent.com/104786633/209585806-1770f39e-4c06-4124-a344-bf2d9355a563.png">

Covered in `app_table_word_pairs.py`:

- Basic table display (display/read-only)
- QAbstractTableModel
- QTableView

This module provides a minimal example of how to display custom
data in a table using the model/view classes QAbstractTableModel
and QTableView. This simple example only covers basic display (a
read-only table, no editing features). Check the other samples
if you want model/view editing features.

## `app_table_people.py` example

<img width="678" alt="image" src="https://user-images.githubusercontent.com/104786633/206917839-f3ac0821-ca77-4188-bdde-2a112dcc24b2.png">

Covered in `app_table_people.py`:

- An editable table
- QAbstractTableModel
- QTableView
- QStyledItemDelegate

This module displays a list of people (Person objects) with
a variety of attributes, with different types, each of which can
be edited.

## `app_nano.py` example

<img width="377" alt="image" src="https://user-images.githubusercontent.com/104786633/206921925-352401b3-7006-43b2-89e6-85a73ad7e581.png">

This is a very tiny app skeleton.

# Setup

*Full coverage of install/setup issues is not practical here, but this should
cover the basics*

As noted above, you can browse the source code files on github, or clone
the repository to download and run them yourself.

You'll need to [install Python](https://www.python.org/downloads/)
(or [install Miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation),
Anaconda is not compatible with PySide6 as of this writing),
download one of the Qt libraries, and clone or download this repository
to run the examples yourself.

To run each of the different demo modules, just `python app_table_people.py`
(`python` followed by the name of the py file you want to run).

## Regular Python Setup

Once you've installed Python, you can run `pip install PySide6` to install Qt.
If you see an error about the command not being found, you'll need to fix your
`PATH` environment variable (if install succeeded, you may just need to close and
reopen your terminal), or specify the full path to pip (not preferable).

## Miniconda Setup

Once you've installed Miniconda, you can `conda create -n appdemos pip` to
create an environment with pip, `conda activate appdemos` to activate it, then
`pip install PySide6` to install Qt. If you see an error about the command not
being found, you'll need to fix your `PATH` environment variable (if install
succeeded, you may just need to close and reopen your terminal), or specify
the full path to the conda executable (not preferable).

# Final Thoughts

Submit an issue to the repo if you want to suggest a change or have
a question or bug report.

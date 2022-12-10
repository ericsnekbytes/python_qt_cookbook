# Python Qt Cookbook

(This doc is being actively edited, check back for updates)

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
used to display tables and lists of data.

Right now, the demos in this repo use the programmatic API (meaning
you write code to define the look and logic of your app). Qt also has
its own declarative UI language called QML that can potentially make
it easier to read and understand the layout of an application. Some
QML samples should be coming in the future.

# Things You Should Know

Check back for more details later, this section is being actively
developed.

## Layouts

(This section is not finished)

Qt's layout system is unique. Generally, child widgets each request space,
and the parent widget tries to accommodate each of them. When you want to
add spacing between widgets, or move them left/right or up/down, it's
often best to add a stretchable space in that widget's layout.

## Signals and slots

(This section is not finished)

Signals and slots are used to pass data around between different places in
your Qt applications.

# Code Overview

## `app_simple_*.py` examples

<img width="984" alt="image" src="https://user-images.githubusercontent.com/104786633/206873672-1165fd4c-f712-4f62-a51d-b18ae0850633.png">

Covered in `app_simple_*.py` modules:

- Basic app startup
- Simple nested layouts
- Custom widgets
- Standard widgets/controls
- A basic signal/slot example

## `app_table_word_pairs` example

<img width="678" alt="image" src="https://user-images.githubusercontent.com/104786633/206873693-3d0759b7-c1ee-476b-84cb-ffa7fee649e5.png">

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

<img width="677" alt="image" src="https://user-images.githubusercontent.com/104786633/206873713-4d1a7ede-321e-4b47-aa34-310549cdb837.png">

Covered in `app_table_people.py`:

- An editable table
- QAbstractTableModel
- QTableView
- QStyledItemDelegate

This module displays a list of people (Person objects) with
a variety of attributes, with different types, each of which can
be edited.

# Final Thoughts

Submit an issue to the repo if you want to suggest a change or have
a question. If it fits with the project, odds are good it'll be
added in the future.

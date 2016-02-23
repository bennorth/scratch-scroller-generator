Scratch project generator for 2D scroller
=========================================

Given a large image, generate a Scratch project which allows 2D
scrolling of a small viewport onto that image.  A 'player' sprite stays
centre-screen but moves around the map.  Will need a small amount of
tweaking to run with your particular project.

Requirements:

* Python 2.7;
* The [Kurt Python module](https://pypi.python.org/pypi/kurt);
* The [Python Image module](http://www.pythonware.com/products/pil/) --- could probably be made to work with Pillow instead.

Usage
-----

A mixture of edit-the-code and command-line arguments:

* Edit `chop-into-tiles.py` to give the required 'player' image details;
* Run as `python chop-into-tiles.py INPUT-LARGE-IMAGE-FILENAME OUTPUT-SB2-FILENAME`;
* Use `File / Upload from your computer` within Scratch.

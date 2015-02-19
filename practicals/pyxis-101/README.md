# Pyxis 101 tutorial

To update the practicals from the repository:

```
git clone https://github.com/ratt-ru/ratt-interferometry-course.git
cd ratt-interferometry-course/practicals/pyxis-101
git pull
```

## A simple task

Make an MS from a config file, fill it with data, make a uv-coverage plot, make an image:

```
makems makems_kat7.cfg
mv kat7_4h60s.MS_p0 kat7_4h60s.MS
```

To fill the MS with 1s, use python (or just run ```fillones.py```):

```
import pyrap.tables
tab = pyrap.tables.table('kat7_4h60s.MS',readonly=False)
data = tab.getcol('DATA')
print data.shape
print data
data[...] = 1
tab.putcol('DATA',data)
tab.putcol('CORRECTED_DATA',data)
```

And now to make an image:

```
lwimager ms=kat7_4h60s.MS npix=512 cellsize=10arcsec weight=natural fits=image.fits
tigger image.fits 
```

And to make a uv-plot:

```
pyxis kat7_4h60s.MS imager.make_image ms.plot_uvcov
```

So: _pyxis is a way to quickly call Python functions from a command line_. In addition, you have something 
called ```Pyxides```: a set of standard Python modules for various useful tasks (typically, wrapping external tools and giving them a Python interface). E.g. ```ms``` contains functions for managing MSs, ```imager``` contains functions for imaging, etc.

Try the documentation:

```
pyxis -D ms.plot_uvcov
```

## The problem

This MS corresponds to an observation of a source at Dec=-30deg. Let us now repeat this procedure for declinations
-90,-80,-70 ... +30.

Two approaches:

* Hyperactive people do thhis by hand. 12 times over.

* Lazy people write a script

* Smart & lazy people write a Pyxis script

See ```pyxis-prac101.py```. We have here a ```make_my_ms``` function.

Now run:

```
pyxis DEC=25 MS=t.MS make_my_ms
```

So, pyxis can (2) assign variables on the command line. The above call is equivalent to this piece of python:

```
DEC = 25
MS = "t.MS"
make_my_ms()
```

Note that pyxis (3) automatically loads files called ```pyxis-*.py``` and ```pyxis-*.conf``` from 
the current directory. These are called *recipes* and *configurations*. Both types are just 
Python code. Recipes will typically define our processing functions (such as ```make_my_ms()```). Configurations
usually just setup various variables and parameters.


```
 pyxis 'DEC_List=range(-90,40,10)' 'MS_Template=kat7-dec$DEC.MS' per[DEC,make_my_ms]
```






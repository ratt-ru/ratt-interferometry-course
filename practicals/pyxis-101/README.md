# Pyxis 101 tutorial

To update the practicals from the repository:

```
git clone https://github.com/ratt-ru/ratt-interferometry-course.git
```

if you haven't already done so. Then:

```
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

So: **pyxis** provides _a way to quickly call Python functions from a command line_. In addition, you have something 
called **Pyxides**: a set of standard Python modules for various useful tasks (typically, wrapping external tools and giving them a Python interface). E.g. ```ms``` contains functions for managing MSs, ```imager``` contains functions for imaging, etc.

Try the documentation:

```
pyxis -D ms.plot_uvcov
```

## A problem statement

This MS corresponds to an observation of a source at Dec=-30deg. Let us now 

* generate MSs for declinations -90,-80,-70 ... +30.

* for each, fill the data with 1s 

* for each, make uv-coverage maps

*  for each, make natuarly-weighted, uniformly-weighted, and robust=0-weighted images

Two approaches:

* Hyperactive people do this by hand. 12 times over.

* Lazy people write a script

* Clever & lazy people write a Pyxis script

## Pyxis scripts

See ```pyxis-prac101.py```. We have here a ```make_my_ms``` function.

Now run:

```
pyxis DEC=25 my.MS make_my_ms ms.plot_uvcov
```

So, pyxis _can assign variables on the command line_. The above call is equivalent to this piece of python:

```
DEC = 25
MS = "my.MS"
make_my_ms()
ms.plot_uvcov()
```

Note also that saying ```my.MS``` on the pyxis command line is equivalent to ```MS=my.MS```. MS is a spcial (probably the most special) variable which is used to indicate the current MS. This is so frequently used, that 
pyxis provides a shortcut for setting it. 

Note that pyxis (3) _automatically loads files called ```pyxis-*.py``` and ```pyxis-*.conf``` from 
the current directory_. These are called *recipes* and *configurations*. Both types are just 
Python code. Recipes will typically define our custom processing functions (such as ```make_my_ms()```). Configurations usually just setup various variables and parameters.

Note also the ```x.sh()``` calls in the recipe -- x.sh is a Pyxis shortcut for invoking external programs.

## Looping

Now, to repeat this for declinations -90 to +30. You coulds write a simple Python loop:

```
for DEC in range(-90,30,10):
  MS = "kat7-dec%d.MS"%DEC
  make_my_ms()
```

Or you could ask pyxis to do it for you:

```
 pyxis 'DEC_List=range(-90,40,10)' 'MS_Template=kat7-dec$DEC.MS' per[DEC,make_my_ms]
```

Pyxis knows about lists and can make templated variables. The built-in ```per``` function runs a loop 
over a list ("per every value of DEC from DEC_List, call this function"). 

## Looping over MSs

We've now generated a bunch of MSs. 

```
ls -ld *.MS
```

Let's fill the data with ones. See ```fill_ms()``` in our recipe. Can we call this in a loop for all MSs 
quickly? Yes, pyxis provides a shortcut:

```
pyxis *MS per_ms[fill_ms,imager.make_image]
```

Two things to note here:

* Setting a list of MSs on the command line (*.MS for example) is s shortcut for setting up ```MS_List```.

* ```per_ms[functions...]``` is a shortcut for per[MS,functions...]

And now in parallale:

```
pyxis -j4 *MS per_ms[fill_ms,imager.make_image]
```

## Changing imager weights

Try:

```
pyxis kat7-dec-30.MS imager.make_image[weight=uniform]
```

Or:

```
pyxis kat7-dec-30.MS imager.weight=uniform imager.make_image
```

The first way shows how to pass parameters to functions. The second way shows how to change defaults. The second way is just a variable asssignment (now look at the ```pyxis-prac101.conf``` file again).

## Filename management

OK, now we need to make a loop over the three weight settings and call the imager three times per MS. This is easy,
but we also want to make sure the output images are all named differently. We'll add this bit of code to 
our recipe:

```
def make_images ():
  for w,rob in ("natural",0),("uniform",0),("robust",0),("robust",1):
    imager.make_image(weight=w,robust=rob,dirty_image="$OUTFILE-$w$rob.fits")
```

and this to our configuration:

```
DESTDIR = '.'
OUTFILE_Template = "my-${MS:BASE}"
```

And now run

```
pyxis *MS per_ms[make_images]
```

Setting a variable named "XXX_Template" tells pyxis to make a variable called "XXX" whose value will be assigned
using variable expansion. Also, most string arguments to Pyxides functions (as in the call to make_image above) have variable expansion done to them automatically.

## Directory management

You now have too much crap in your directory. Remove it, and let's start again:

```
rm -f *fits
```

Let's organize things by directory, one directory by MS. Put this in your conf file:

```
DESTDIR_Template = "plots-${MS:BASE}"
OUTFILE_Template = "$DESTDIR/my-${MS:BASE}"
```

DESTDIR and OUTFILE are special variables (in the sense that Pyxides modules such as the imager know 
about them) that are used to indicate (a) a destination directory for output files, and (b) a basic name for the files.

For good measure, add this to your recipe file to save the uv-coverage plot to a PNG:

```
def make_uvcov ():
  ms.plot_uvcov(save="$OUTFILE-uvcov.png")
```

Now run:

```
pyxis *MS per_ms[make_images,make_uvcov]
```

And to admire our uv-coverage plots:

```
eog plots-*/*png
```

## Logging

Too much text on your console? Try

```
pyxis LOG=log.txt *MS per_ms[make_images]
```

All output is now logged to ```log.txt```. LOG is another special pyxis variable, setting LOG will 
automatically start logging to that file. 

But since it's a variable, we can also set it in the conf file. And we can template it, to have a separate
log file per every MS. Add this to your conf:

```
LOG_Template = "$DESTDIR/log-${MS:BASE}.txt"
```

And re-run.

##  Pyxis and screen

The ```screen``` command is generally useful for running long jobs. You can start some long task under screen,
then detach it and log out, and it will keep running inside screen.

Pyxis supports this explicitly. Try:

```
pyxis -S *MS per_ms[make_images,make_uvcov]
```

or just put SPAWN_SCREEN=True into your conf file.

# And that's all, folks!






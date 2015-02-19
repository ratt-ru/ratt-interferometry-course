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
lwimager ms=kat7_4h60s.MS npix=512 cellsize=10arcsec fits=image.fits
tigger image.fits 
```

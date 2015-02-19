import imager

def make_my_ms (dec=-30):
  conffile = MS + ".cfg";
  file(conffile,"w").write("""AntennaTableName=KAT7_ANTENNAS
NTimes=240
StepTime=60
StartFreq=1.4e9
StepFreq=10e6
NFrequencies=1
NBands=1
Declination=%f
RightAscension=0:0:0
StartTime=2011/11/16/15:00
MSName=%s
MSDesPath=.
NParts=1
WriteImagerColumns=True
WriteAutoCorr=True"""%(dec,MS));
  x.sh("makems $conffile");
  x.sh("rm -fr $MS");
  x.sh("mv ${MS}_p0 $MS");
  x.sh("rm -fr $conffile ${MS}_p0.vds $MS.gds");
  # put ones into the MS

def make_ms_series (d0=-90,d1=100,step=10):
  for dec in range(d0,d1,step):
    v.MS = "kat7-dec%d.MS"%dec;
    make_my_ms(dec);

def fill_ms ():
  tab = ms.msw();
  data = tab.getcol("DATA")
  data[...] = 1
  tab.putcol("DATA",data);
  tab.putcol("CORRECTED_DATA",data);

def make_uvcov ():
  makedir(DESTDIR);
  ms.plot_uvcov(save="$OUTFILE-uvcov.png")

def make_images ():
  for w,rob in ("natural",0),("uniform",0),("robust",0),("robust",1):
    imager.make_image(weight=w,robust=rob,dirty_image="$OUTFILE-$w$rob.fits");


# pyxis -j 4 *MS per_ms[fill_ms,make_uvcov,imager.make_image]

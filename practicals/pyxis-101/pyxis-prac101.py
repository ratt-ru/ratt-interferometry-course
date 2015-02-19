import imager

def make_my_ms ():
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
WriteAutoCorr=True"""%(DEC,MS));
  x.sh("makems $conffile");
  x.sh("rm -fr $MS");
  x.sh("mv ${MS}_p0 $MS");
  x.sh("rm -fr $conffile ${MS}_p0.vds $MS.gds");
  # put ones into the MS

def fill_ms ():
  tab = ms.msw();
  data = tab.getcol("DATA")
  data[...] = 1
  tab.putcol("DATA",data);
  tab.putcol("CORRECTED_DATA",data);


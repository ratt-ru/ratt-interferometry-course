import pyrap.tables
tab=pyrap.tables.table('kat7_4h60s.MS',readonly=False)
data=tab.getcol('DATA')
data
data[...]=1
data
tab.putcol('DATA',data)

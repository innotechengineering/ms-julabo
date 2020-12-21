# ms-julabo
Serial communication to Julabo Diamond Sous Vide

Initial implementation of RS232 control interface - UNTESTED

#### Notes:
Currently `rtscts=False` - docs say that hardware handshaking is required.  we wont know until we connect (most devices will work ok with software or automatic flow control).  if we have trouble with handshaking, we can set `rtscts=True`.  Additionally, I have provided a multipurpose adapter cable where we have CTS and RTS physically jumpered.  

Not totally sure of the DB9 sex on the Jualbo machine.  The multipurpose adapter cable will allow us to convert to any possible permutation.  

Not totally sure if a true null modem connection is required.  The multipurpose adapter cable has crossover connections should we need them.  

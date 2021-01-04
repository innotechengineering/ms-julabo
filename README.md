# ms-julabo
Serial communication to Julabo Diamond Sous Vide

### Serial Interface
The Julabo RS232 serial interface is permanently fixed at:    
 - Baudrate: 4800  
 - Parity: EVEN  
 - Data bits: 7  
 - Stop bits: 1  
 - Full hardware flow control  

A NULL modem crossover cable is required. [Buy it on Amazon](https://www.amazon.com/gp/product/B00CEMGMMM/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1) 

*NOTE* if using a USB to Serial adapter, it MUST support full hardware flow control and handshaking (it needs CTS/RTS and DSR/DTR signals).  The StarTech ICUSB232V2 has proven to work. [Buy it on Amazon](https://www.amazon.com/gp/product/B00GRP8EZU/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)  

### Communication Protocol  

The Julabo unit operates in two modes: MANUAL(local control), and REMOTE(remote control).  When in MANUAL control mode (default), the unit is operated by the user via the user interface.  When in REMOTE control mode, the unit is controlled over the serial interface.

All `read` commands can be sent regardless of the current operating mode.  

The start/stop/set_working_temp `write` commands must be sent to the unit after putting the unit into REMOTE control mode.  The unit is put into REMOTE or MANUAL control mode by using the `remote_control()` and `local_control()` methods respectively.

#### Status Messages
The Julabo documentation is not comprehensive.  Below is an incomplete table defining the various status states that were discovered by limited testing.  Status is read from the unit using the `read_status()` method.    

00 MANUAL STOP  
01 MANUAL START  
02 REMOTE STOP  
03 REMOTE START  
-08 INVALID COMMAND  
-09 COMMAND NOT ALLOWED IN CURRENT OPERATING MODE  
-10 VALUE TOO SMALL  
-11 VALUE TOO LARGE  

If a status message begins with a `-`, it indicates an error.  
  
For status 00,01,02,03 - the "manual" and "remote" indicate the control mode that the unit is currently in.  Additionally, the "start" and "stop" indicate if the unit is running or not running (which can also be queried by using the `read_circulator_status()` method.  

If status -09 is returned, the command is not allowed in the current operating mode.  Use the `remote_control()` and `local_control()` methods to toggle the operating mode appropriately.  

Status -10 and -11 occur when setting the working temperature of the bath to a value that is out of acceptable range.  

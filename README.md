# OS-Project-1
Three Programs: Encryption System

Logger – responsible for logging all activity. 

Encryption program – responsible for encrypting and decrypting strings. 

Driver program – interacts with the user to use the encryption program. The entire system will be run by running the driver program, which will launch the other programs and communicate with them through pipes. 


Files Included:
- driver.py
- encryptor.py
- logger.py

System performs encryption/decryption with the Vigenere method and logs activity to the logger program. Programs communicate with each other with 
i/o streams

The driver program is the main program the user interacts with. It displays commands, launches the logger and encryptor programs, sends encryptions/decryptions to the encryptor, sends log messages, validates input, and shuts down programs.

encryptor program performs encryptions using the Vigenere method. It accepts message commands through input from the user. Four functions it has are:

PASSKEY
sets the encryption key
ENCRYPT
encrypts text
DECRYPT
decrypts text
QUIT
terminates program

logger program records activity to a log file. Driver program sends these messages to the logger and writes messages recording date and time and actions. 




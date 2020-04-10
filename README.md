# CIS3319-lab1-DES

# Lab5: Implementation and Application of Kerberos 
  
1. All of your source code files for this lab.
2. A README file including information:
a) which language and external libraries you use.
  I used python as the primary langauge of this lab. 
  The libraries used are 
    1. Des
b) which IDE you use.
    1. I used pycharm
c) other details about how to run your code step by step (if any). TAs will look at 
and run your code, and check the printouts.
    1. Run the as_server.py first with "python as_server.py" 
    2. Run the client.py with "python client.py"
    
    

# Implementation and Application of DES

## Overall Walkthrough of Project
  1.) Creating a symmetric key for DNS
  * Key is created by A and put into a file
  * File is sent from A to B via email 
      
  2.) Socket is created
  * Chat room connection between A and B is established
      
  3.) A and B load key from file
  * Message is typed from A to B
  * Message is Encrypted
  * Message is sent
  
  4.) In chat, the key is displayed along with
  * Plaintext message
  * Encrypted message
  * Received encrypted message
  * Recieved decrypted message

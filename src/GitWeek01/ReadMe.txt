ReadMe.txt for Week01 subdirectory of Internet Programming Assignments Project
==============================================================================

Author:       Melissa Rice (UWNetID mlrice)
Last Revised: Monday 17 January 2011

Note: For testing convenience, all of the socket programs below are set up to
run on localhost. To run the server on a remote machine, just change the 
serverHost variable.  

Contents of Subdirectory:

AdditionServer.py: 
  A server-side socket which accepts a string specifying an addition operation
  and returns the sum. The string can be any arbitrary infix addition expression
  but may not contain other binary operators, although unary minus is allowed.
  For example: '3+4' or ' -5 + -8', or '-7 + 3.54 + 428 + 54 + -87'. The addition
  server will add two numbers but is not limited to two numbers. It is limited
  to a maximum of 4096 bytes in the input string. This program, together with 
  AdditionClient.py are Assignment 1 for Week 1 of the Python Internet 
  Programming Class. A switch at the top of the program controls diagnostic printing.
  
AdditionClient.py:
  A client-side socket demonstrating the use of the addition socket service in 
  AdditionServer.py. Sends an infix addition expression to the server, receives
  the sum as answer, and prints the expression and its sum. This program, together 
  with AdditionServer.py are Assignment 1 for Week 1 of the Python Internet 
  Programming Class.

EchoServerLocal.py:
  This is a short and simple but fully-commented example of a server-side socket 
  which simply echos whatever the client sends, plus some information about the
  sockets. This program derives from Lab A from Week 1 of the Python Internet
  Programming Class. The companion client-side program is EchoClientLocal.py.

EchoClientLocal.py:
  This is short and simple example of a client-side socket which simply 
  sends a string to the server-socket and prints both the sent string and the
  reply received from the socket. This program is not documented but the 
  companion server-side program EchoServerLocal.py contains all the relevant
  documentation for the socket tools used here. This program derives from 
  Lab A from Week 1 of the Python Internet Programming Class. 

  
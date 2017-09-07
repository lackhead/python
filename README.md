# python
A place to keep Python code not for a specific project (learning, experimentation, etc)

## local_conn.py

My first Python script ever! I wrote this as a solution to one of the challenges
from the [September 2017 py-study-group challenge](https://github.com/py-study-group/challenges/blob/master/September/challenges4.md). The text is as follows:
> Use Python to see who is connected your network
> Get the local IP address and subnet mask and calculate the address range in you network segment. Scan all the addresses and display those that are alive.
> Bonus Points: Extract the IPs on a CSV file

## named_pipes

Another monthly challenge from the [September 2017 py-study-group challenge](https://github.com/py-study-group/challenges/blob/master/September/challenges4.md). The text is as follows:
> Use named pipes to pass data between two Python scripts. Create two scripts, server.py and client.py:
>   * client.py uses a named pipe to send a text message to server.py.
>   * server.py waits for the message and displays its contents.
> On Linux you can use os.mkfifo() to work with named pipes and on Windows you can use Tim Golden's pywin32 module.
>
> Bonus Points: Create a class called NamedPipe that encapsulates working with named pipes.
>   * NamedPipe.__init__() method should accept one argument - the path of the named pipe (eg. '/tmp/mypipe' on Linux)
>   * NamedPipe should have three methods: read(), write() and close(). Both client.py and server.py should use NamedPipe for communication.

In solving the first problem I deviated a bit from the challenge and had the user input the message as well as having both
the server and the client loop so that the one-way chat session could continue indefiniately.



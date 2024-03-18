# simplified-FTP-server

## Group members

- Raul Jarquin Valdez (jarquinr121@csu.fullerton.edu)
- Anthony Jarjour (anthjar@csu.fullerton.edu)

## Usage

1. `python server.py <PORTNUMBER>` to run the server
2. `python client.py <server machine> <server port>` to run the client

3) Upon connecting to the server, the client prints out ftp>, which allows the user to execute the following commands.
   * ftp> get <file name> (downloads file <file name> from the server)
   * ftp> put <filename> (uploads file <file name> to the server)
   * ftp> ls(lists files on theserver)
   * ftp> quit (disconnects from the server and exits)

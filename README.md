# folder-walker

Task – Walk down folders
The program gets a root folder (a command line parameter) and walks down the folder and for each file and folder under this folder it stores its name, modification time and a checksum (the checksum algorithm is not important – md5, sha1 or any common algorithm). 
In the second run I specify a folder name under the original root folder and the program should find all the occurrences of the given folder name and list all changes under this folder (print modified, removed, added).  
It has to work on Mac, Linux and Windows.
The output format is not important – may be a command line / stdout text format – one change per line.
The data should be stored in elasticsearch running on localhost:9200. Use available libraries including 3rd party ones when possible. No need to develop functions which do already exist. You need to develop a simple data structure in elasticsearch. It is not critical to come up with the best possible structure, but it must work. 
Make a time estimate first.
Explain how the algorithm works. 
Make a time complexity estimate (best guess is ok, but explain) and offer possible improvements.  


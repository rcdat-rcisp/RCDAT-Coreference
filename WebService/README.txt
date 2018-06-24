We used SOAP for coreference web service (host address: 185.130.78.112/coref). 
For using this web service one should call it through a code. 
A sample code in this regards is presented in the directory. (CorefCaller.py)
Webservice has two options:
Usage 1: programName   InputFilePath   ResultFilePath  tokenFilePath  1 (Input is a simple text and output is list of tokens along with a file containing coreference chains)
Usage 2: programName   InputFilePath   ResultFilePath  2 (Input is a text file, each token in a line and sentences are separated with an additional \n and the output is automatic preprocess labels for each token)

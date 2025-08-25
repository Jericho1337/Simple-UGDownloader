# UGDownloader
Ultimate Guitar Downloader is a simple downloader for UG Songs
![alt text](images/execution.png)
![alt text](images/output2.png)
![alt text](images/output0.png)
![alt text](images/output1.png)
![alt text](images/input.png)

### USAGE

#### BASIC USAGE
Place yourself in the project directory
If no input file is specified, standard path "./input/songstodownload.txt" will be used
```
python3 main.py
OR
python3 main.py -i <PATH_TO_INPUT_FILE>
```

The script will produce 3 outputs in the output folder:
* TXT file containing the tab
* PDF without bold
* PDF with bold chords (experimental)

#### CHORD TRANSPOSITION
You can pass a transposing offset (positive or negative)

At the moment, transposing offset will be applied to all song listed in input file

```
python3 main.py -t <POSITIVE_OR_NEGATIVE_OFFSET>
```

In this example we transpose down of 3 semitones
```
python3 main.py -t -3
```


### INSTALLATION

```
pip3 install -r requirements.txt
```
Also Edge Webdriver must be installed: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH

**NOTE**: If you are using Visual Studio Code, Edge driver is already installed

### NEXT STEPS
* [X] Chord transposer
* [ ] TXT To PDF converter
* [ ] GUI
* [ ] add other webdrivers



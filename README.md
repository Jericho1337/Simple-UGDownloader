# Simple-UGDownloader
Simple-UGDownloader is a simple downloader for UG Songs
![alt text](images/execution.png)
![alt text](images/output2.png)
![alt text](images/output0.png)
![alt text](images/output1.png)
![alt text](images/input.png)

### INSTALLATION

```
pip3 install -r requirements.txt
```
Also Edge Webdriver must be installed: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH

**NOTE**: If you are using Visual Studio Code, Edge driver is already installed

### USAGE

#### BASIC USAGE
Place yourself in the project directory

**NOTE**: If no input file is specified, standard path "./input/songstodownload.txt" will be used

```
python3 main.py
OR
python3 main.py -i <PATH_TO_INPUT_FILE>
```

The script will produce 4 outputs in the output folder:
* TXT file containing the tab
* PDF without bold
* PDF with bold chords (uses heuristics to determine chords and make them bold)
* TRUE PDF with bold chords (uses real website parsing to bold chords)

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

#### TXT TO PDF
You can convert a TXT of a song to normal and bold PDF

```
python3 main.py -p <PATH_TO_TXTFILE>
```

**NOTE**: transposition is not supported and "-t" argument will be ignored in this mode

**NOTE**: TRUE mode isn't yet supported in TXT to PDF

### NEXT STEPS
* [X] Chord transposer
* [X] TXT To PDF converter
* [ ] TRUE Mode for TRUE TXT TO TRUE PDF
* [X] TRUE Mode transposing
* [X] Normal transposing for TXT to PDF normal mode
* [ ] GUI
* [ ] Add other webdrivers



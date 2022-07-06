# Pensamiento Computacional - Final Project

Within this repository there are different files, which all compile the final project for this course, Pensamiento Computacional. When run, part of the code would generate a music sheet from a midi file, another part of the code shall convert a music sheet into an audio in wave format, and a whole section is also dedicated to the communication between the computer and an electric xylophone: it converts the same music sheet into a list of objects which represent each note that can be read by the xylophone in order for the song to be played. And of course, finally there are tests for the functions created in order to check if everything is running as it should.

## Using the respository

First of all, the user must clone the repository into a location in the computer to use. Once done that, for the program to be executable, the user must have a device with a python interpreter.

## Installation

In order to use this respository, certain dependencies must be installed; it can be installed with pip. Once, the repository is cloned, the user needs to execute (the following model is based on the Xylophone README provided by the professors):

1. Get in the local repository.

```shell
$ cd /path/to/TP_final
```

2. Install the dependencies.

```shell
$ pip install -r requirements.txt
```

3. Install it with pip

```shell
$ pip install .
```


## Generating a music sheet

Through a terminal, must run midi2score.py and enter the respective parameters: the midi file to be converted and the name of the text file where the music sheet will be written.

Here is an example of and implementation using parser through the terminal:
![midi2score](https://user-images.githubusercontent.com/101208112/177467927-57926559-7994-4cdd-b130-9c9bfb522dd3.jpeg)


## Generating a wave file

Through a terminal, must run final_parser.py and enter the respective parameters: the instrument which includes its harmonics and the functions to use, the music sheet, the frecuency and the name of the audio file that is going to be generated.

Here is an example of and implementation using parser through the terminal:
![gen_wav](https://user-images.githubusercontent.com/101208112/177465966-33ca89ce-9b78-4320-a56c-97adac6a1baf.jpeg)


## Communicating with the xylophone

Through a terminal, must run xylophone_server.py and enter the respective parameters: the music sheet file and the instrument ID.

Here is an example of and implementation using parser through the terminal:
![xylo_data](https://user-images.githubusercontent.com/101208112/177468324-611e4c92-3e2a-4f14-8250-4a004eae2643.jpeg)


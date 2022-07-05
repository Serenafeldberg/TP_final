

import numpy as np
from scipy.io.wavfile import write
from note import Note
import functions
from typing import List

class Instrument ():
    '''
        This object creates the class Instrument

        PARAMS
        -> file: Instrument file
        -> partiture: partiture fila
        -> frecuency: sample rate
        -> filename: Name of the wave audio
    '''
    def __init__ (self, file, partiture, frecuency, filename):
        self.file = file
        self.output = filename
        self.note = Note(partiture)
        self.frecuency = frecuency
        self.duration = self.note.get_duration()
        self.instrument = self.read_file()
        self.attack_t = float(self.instrument[-3][1])
        self.decay_t = float(self.instrument[-1][1])

    def read_file (self):
        '''
        Reads the instrument file and returns a list with all the information
        '''
        all = []
        with open (self.file, 'r') as fn:
            lines = fn.readlines()
            for line in lines:
                line = line.strip("\n")
                new_lines = line.split()
                new = []
                for elem in new_lines:
                    new.append(elem)
                if len(new) != 0:
                    all.append(new)
        return all

    def get_harmonics (self):
        '''
        returns amount of harmonics
        '''
        harmonics = int(self.instrument[0][0])
        return harmonics

    def get_amplitude (self):
        '''
        Returns a dictionary, where the keys are the harmonics and the values are the amplitudes
        '''
        harmonic = self.get_harmonics()
        harm_amplitude = {}
        for i in range (1, harmonic + 1):
            line = self.instrument[i]
            h = int(line[0])
            a = float(line[1])
            harm_amplitude[h] = a

        return harm_amplitude

    def get_fn_info (self, a_list):
        '''
        Given the list of either attack, sustained or decay, it will return the name of the function and its params
        '''
        fn_name = a_list[0]
        fn_params = []
        for i in range (1, len(a_list)):
            param = float(a_list[i])
            fn_params.append(param)

        return fn_name, fn_params
        

    def all_fn (self, function, t, args):
        '''
        It is a dictionary with all the posible functions, and their corresponding formula

        PARAMS:
        -> function: name of the function needed
        -> t: array of time
        -> args: list with all the arguments needed

        returns the function valued depending the arguments
        '''
        fn = {'CONSTANT': functions.constant, 'LINEAR':  functions.linear, 'INVLINEAR': functions.invlinear, 'SIN': functions.sin
        , 'EXP': functions.exp, 'INVEXP': functions.invexp, "QUARTCOS": functions.quartcos
        , "QUARTSIN": functions.quartsin, 'HALFCOS': functions.halfcos, 'HALFSIN': functions.halfsin
        , 'LOG': functions.log, 'INVLOG': functions.invlog, 'TRI': functions.tri, 'PULSES': functions.pulses}

        fn_return = fn[function](t, *args)
        return fn_return

    def attack (self, t):
        '''
        Gets the information needed for the attack

        PARAMS
        -> t: array of time

        returns the function of the attack
        '''
        list_attack = self.instrument[-3]
        attack_name, attack_params = self.get_fn_info(list_attack)
        attack = self.all_fn(attack_name, t, attack_params)

        return attack

    def decay (self, t):
        '''
        Gets the information needed for the decay

        PARAMS
        -> t: array of time

        returns the function of the decay
        '''
        list_decay = self.instrument[-1]
        decay_name, decay_params = self.get_fn_info(list_decay)
        decay = self.all_fn(decay_name, t, decay_params)
        
        return decay

    def sustained (self, t):
        '''
        Gets the information needed for the sustenance

        PARAMS
        -> t: array of time

        returns the function of the sustenance
        '''
        list_sustained = self.instrument[-2]
        sus_name, sus_params = self.get_fn_info(list_sustained)
        sustained = self.all_fn(sus_name, t, sus_params)

        return sustained


    def gen_mod (self, t, y, duration_total):
        '''
        Modulariza la nota con ataque, sostenido, decaimiento

        PARAMS
        -> t: array of time
        -> y: array of note
        -> duration_n: duration of the note plus the decay time
        
        Returns: Array of the note modularized
        '''
        duration_n = duration_total - self.decay_t
        #attack
        data_a= self.attack(t[t < self.attack_t])
        y [t < self.attack_t] *= data_a
        

        #sustained
        data_s = self.sustained(t[(t >= self.attack_t) & (t < duration_n)])
        y [(t >= self.attack_t) & (t < duration_n)] *= data_s
        
        
        #decay
        data_d= self.decay(t[(t >= duration_n)])
        y [(t >= duration_n)] *= (data_d )
        
        return y

    def gen_tone(self, frec, end , tstart = 0):
        '''
        Creates an array of the notes signal that contains the sum of the harmonics given
        the sample rate

        PARAMS:
        -> frec: frecuency of the note
        -> end: time of duration of the note complete (atack, sustained and decay)
        -> tstart: time of start

        returns: Array of the note with the sum of harmonics and the time of attack
        '''
        
        t = np.arange(tstart, end, 1/self.frecuency) 
        yy = np.zeros_like(t)
        harmonics = self.get_harmonics()
        amplitudes = self.get_amplitude()
        if harmonics > 0:
            for i in range (harmonics):
                multiplies = list(amplitudes.keys())[i]
                a = list(amplitudes.values())[i]
                yy += (a * np.sin(2 * np.pi * multiplies * frec * t))
        
        array_mod = self.gen_mod(t, yy, (end - tstart))
        array_mod *= 0.01

        return array_mod

    def gen_track (self):
        '''
        Generates an empty array, and it will concatenate the notes depending on the time they shoud play

        returns an array with the sinthetisized notes.
        
        '''
        notes_amount = self.note.get_notes() + 1
        zero = np.zeros(int(self.frecuency * (self.duration + self.decay_t * notes_amount)), dtype= float)
        notes = self.note.read_file()
        for val in notes.keys():
            start = notes[val][0]
            duration_note = notes[val][2]
            frec = notes[val][1]
            y = self.gen_tone(frec, duration_note + self.decay_t)
            zero[int(start*self.frecuency): (int(start*self.frecuency) + len(y))] += y
            zero[zero> 1] = 1
            zero[zero < -1] = -1

        track = zero[0 : int(self.frecuency * (self.duration + self.decay_t))]
    
        return track * 100000

    def audio_wav (self):
        '''
        Generates a file.wav
        '''
        track = self.gen_track()
        write (self.output , self.frecuency , track.astype(np.int16))

ins = Instrument('piano.txt','partitura.txt', 44100, 'audio.wav')
ins.audio_wav()


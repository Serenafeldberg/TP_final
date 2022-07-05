

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from note import Note
import functions
from typing import List

class Instrument ():
    def __init__ (self, file, frecuency):
        self.file = file
        self.note = Note('partitura.txt')
        self.frecuency = frecuency
        self.duration = self.note.get_duration()
        self.instrument = self.read_file()
        self.attack_t = self.instrument[-3][1]
        self.decay_t = self.instrument[-1][1]
        

        

    def get_instrument (self):
        pass

    def read_file (self):
        all = []
        with open (self.file, 'r') as fn:
            lines = fn.readlines()
            for line in lines:
                line = line.strip("\n")
                new_lines = line.split()
                new = []
                for elem in new_lines:
                    try:
                        elem = float(elem)
                        if elem == int(elem):
                            elem = int(elem)
                    except:
                        ValueError
                    new.append(elem)
                if len(new) != 0:
                    all.append(new)
        return all

    def all_fn (self, function, t, args):
        '''
        It is a dictionary with all the posible functions, and their corresponding formula
        '''
        fn = {'CONSTANT': functions.constant, 'LINEAR':  functions.linear, 'INVLINEAR': functions.invlinear, 'SIN': functions.sin
        , 'EXP': functions.exp, 'INVEXP': functions.invexp, "QUARTCOS": functions.quartcos
        , "QUARTSIN": functions.quartsin, 'HALFCOS': functions.halfcos, 'HALFSIN': functions.halfsin
        , 'LOG': functions.log, 'INVLOG': functions.invlog, 'TRI': functions.tri, 'PULSES': functions.pulses}

        fn_return = fn[function](t, *args)
        return fn_return

    def get_params (self, a_list: List, t):
        '''
        Depending on the amount of elements in the list, and on the parameters, it will return an array valued in a function
        
        '''
        len_list = len(a_list)
        if len_list == 4:
            fn = a_list[0]
            first_param = a_list[1]
            second_param = a_list[2]
            third_param = a_list[3]
            function = self.all_fn(fn, t, [first_param, second_param, third_param])
        if len_list == 3:
            fn = a_list[0]
            first_param = a_list[1]
            second_param = a_list[2]
            function = self.all_fn(t, [first_param, second_param])
        if len_list == 2:
            fn = a_list[0]
            first_param = a_list[1]
            function = self.all_fn(fn, t, [first_param])
        if len_list == 1:
            fn = a_list[0]
            function = functions.constant(t)

        return function

    def attack (self, t):
        list_attack = self.instrument[-3]
        attack = self.get_params(list_attack, t)

        return attack

    def decay (self, t):
        list_decay = self.instrument[-1]
        decay = self.get_params(list_decay, t)
        
        return decay

    def sustained (self, t):
        list_sustained = self.instrument[-2]
        sustained = self.get_params(list_sustained, t)

        return sustained


    def gen_mod (self, t, y, duration_n):
        '''
        Modulariza la nota con ataque, sostenido, decaimiento

        PARAMS
        -> t: array of time
        -> y: array of note
        -> duration_n: duration of the note
        
        Returns: Array of the note modularized
        '''
        
        #attack
        data_a= self.attack(t[t < self.attack_t])
        y [t < self.attack_t] *= data_a

        #sustained
        data_s = self.sustained(t[(t >= self.attack_t) & (t < duration_n)])
        y [(t >= self.attack_t) & (t < duration_n)] *= data_s

        #decay
        data_d= self.decay(t[(t >= duration_n)])
        y [(t >= duration_n)] *= data_d

        return y

    def gen_tone(self, frec, end , tstart = 0):
        '''
        Creates an array of the notes signal that contains the sum of the harmonics given
        the sample rate

        PARAMS:
        -> frec: frecuency of the note
        -> end: time of duration of the note
        -> tstart: time of start

        returns: Array of the note with the sum of harmonics and the time of attack
        '''
        ins = self.read_file()
        t = np.arange(tstart, end + self.decay_t, 1/self.frecuency) 
        yy = np.zeros_like(t)
        harmonics = ins[0][0]
        if harmonics > 0:
            for i in range (1, harmonics+1):
                multiplies = ins[i][0]
                a = ins[i][1]
                yy += (a * np.sin(2 * np.pi * multiplies * frec * t))
        
        array_mod = self.gen_mod(t, yy, (end - tstart))
        array_mod *= 0.01

        plt.plot(t, array_mod)
        plt.show()

        return array_mod

    def partes (self):
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
    
        return zero * 100000

ins = Instrument('piano.txt', 44100)
y = ins.partes()

#write ('audio2.wav' , 44100, y.astype(np.int16))

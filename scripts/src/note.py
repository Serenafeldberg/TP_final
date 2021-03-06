from notes import frecuency

class Note ():
    '''
    Creates the class Note

    PARAMS 
    -> file: music sheet file
    '''
    def __init__ (self, file):
        self.file = file
        self.frecuency = frecuency
        self.notes = self.read_file()

    def read_file (self):
        '''
        Reads the music sheet and returns a disctionary with 
        the value as a list with the time of start, frecuency and duration of the note
        '''
        self.notes = {}
        with open(self.file, 'r') as fn:
            lines = fn.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
                line = lines[i].split()
                frec = self.frecuency[line[1]]
                self.notes[i] = [float(line[0]), frec, float(line[2])]

        return self.notes

    def get_duration (self):
        '''
        Returns the total duration of the song (music sheet)
        '''
        duration = 0
        bucket = 0
        notes_in_order = sorted(self.notes.values())

        if notes_in_order[0][0] != 0:
            duration += notes_in_order[0][0]

        for value in notes_in_order:
            tstart = value[0]
            d_note = value[2]
            tend = tstart + d_note
            if tend > bucket:
                if tstart < bucket:
                    d_note = tend - bucket

                if tstart > bucket:
                    blank_secs = tstart - bucket
                    duration += blank_secs
                    bucket += blank_secs

                bucket = tend
                duration += d_note
                
        return duration

    def get_notes (self):
        '''
        Gets the amount of notes that the music sheet has
        '''
        keys = list(self.notes.keys())
        return keys[-1]




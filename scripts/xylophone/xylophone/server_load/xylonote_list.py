from xylophone.xylo import XyloNote
from typing import List

def xylonote_list(filename) -> List:
    '''
    This function eliminates the notes the xylophon does not admit.

    PARAMS 
    -> filename: str, name of the music sheet

    returns a list containg either XyloNotes or nothing. 
    '''
    with open(filename, 'r') as f:

            notes = ['G4', 'G5', 'G6', 'G#4', 'G#6', 'Gb6', 'A4', 'A5', 'A6', 'A#4', 'A#5', 'A#6', 'Ab4', 'Ab5', 'Ab6', 
            'B4', 'B5', 'B6', 'Bb4', 'Bb5', 'Bb6', 'C5', 'C6', 'C7', 'C#5', 'C#6', 'C#7', 'Cb7', 'D5', 'D6', 
            'D#5', 'D#6', 'Db5', 'Db6', 'E5', 'E6', 'Eb6', 'F5', 'F6', 'F#6']

            notes_xylo = []
            velocity = 90

            for line in f:
                line1 = line.strip('\n').split()
                start = line1[0]
                note = line1[1]
                xylo_note = XyloNote(note, start, velocity)
                if note in notes:
                    notes_xylo.append(xylo_note)

            return notes_xylo

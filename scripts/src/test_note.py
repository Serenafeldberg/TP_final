
import unittest
from note import Note

note = Note('mario_bros.txt')

class Test (unittest.TestCase):

    def test_get_duration (self, duration = note.get_duration()):
        '''
        This function is used to test that the duration of the music sheet is greater than 0
        '''
        self.assertGreaterEqual(duration, 0)

    def test_get_notes (self, notes = note.get_notes()):
        '''
        This function tests that the amount of notes in the music sheet is greeatr than 0 
        '''
        self.assertLessEqual(0, notes)

    def test_read_file (self, note_dict = note.read_file()):
        '''
        This function is used to test that the first value of the dictionaty note_dict 
        is in fact the first line of the music sheet (the frecuency already changed from str to float)
        '''
        expected = [0, 1975.53 ,0.046511627906976744]
        self.assertEqual(expected, note_dict[0])

if __name__ == '__main__':
    unittest.main()

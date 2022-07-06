import numpy as np
import unittest

from instrument import Instrument

instrument = Instrument('piano.txt', 'mario_bros.txt', 44100, 'audio.wav')
t = np.arange(0, 0.27, 1/instrument.frecuency) 

class Test(unittest.TestCase):
    
    def test_get_harmonics (self, harmonic = instrument.get_harmonics(), expected = 4):
        '''
        This function tests if the amount of harmonics is right, 
        based on the harmoincs that the insutrumet has
        '''
        self.assertEquals(expected, harmonic)

    def test_get_amplitude (self, harmonic_amplitude = instrument.get_amplitude()):
        '''
        This function is able to test whether the amplitudes calculated 
        by the function is the same as in the file
        '''
        amplitudes = list(harmonic_amplitude.values())
        expected = [1, 0.72727272, 0.31818181, 0.090909]
        self.assertEqual(amplitudes, expected)

    def test_decay_t (self, decay_time = instrument.decay_t, expected = 0.06):
        '''
        This function tests if the function read_file is able to calculate the right decay time
        '''
        self.assertEqual(decay_time, expected)
    
    def test_attack_t (self, attack_time = instrument.attack_t, false_time = 0):
        '''
        This function test if the time of attack is a positive number
        '''
        self.assertFalse(attack_time < false_time)

    def test_gen_track (self, track = instrument.gen_track()):
        '''
        This function checks that the time of start of the track is 0
        '''
        self.assertEqual(track[0], 0)

    def test_get_fn_info (self ):
        '''
        This function tests if get_fn_info is able to return the correct values
        '''
        attack_name, attack_params = instrument.get_fn_info(['LINEAR', 0.02])
        self.assertEqual(attack_name, "LINEAR")
        self.assertEqual(attack_params, [0.02])

    def test_sustained (self, sus_fn = instrument.sustained(t)):
        '''
        This functions allows the user to know if the sustained array is being calculated, 
        by comparing it with the original time array
        '''
        self.assertFalse(t.all() == sus_fn.all())

    def test_decay (self, decay_fn = instrument.decay(t)):
        '''
        This function tests if the decay function works, given that it compares
        the result of decay to the same array evaluated in the function INVLINEAR
        '''
        expected  = (1 - t / instrument.decay_t)
        self.assertTrue(expected.all() == decay_fn.all())

    def test_all_fn (self):
        '''
        This function tests that all_fn is creating two different arrays,
        depending on the name of the function
        '''
        fn = instrument.all_fn('EXP', t, [0.06])
        fn_1 = instrument.all_fn("LINEAR", t, [0.06])
        self.assertNotEqual(fn.all(), fn_1.all())


if __name__ == '__main__':
    unittest.main()


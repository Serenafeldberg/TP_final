from sre_constants import IN
import unittest

from instrument import Instrument

instrument = Instrument('piano.txt', 'mario_bros.txt', 44100, 'audio.wav')

class Test(unittest.TestCase):
    def test_get_harmonics (self, harmonic = instrument.get_harmonics(), expected = 4):
        self.assertEquals(expected, harmonic)

    def test_get_amplitude (self, harmonic_amplitude = instrument.get_amplitude()):
        amplitudes = list(harmonic_amplitude.values())
        expected = [1, 0.72727272, 0.31818181, 0.090909]
        self.assertEqual(amplitudes, expected)

    def test_decay_t (self, decay_time = instrument.decay_t, expected = 0.06):
        self.assertEqual(decay_time, expected)

    
    def test_gen_track (self, track = instrument.gen_track()):
        self.assertEqual(track[0], 0)

    def test_get_fn_info (self ):
        attack_name, attack_params = instrument.get_fn_info(['LINEAR', 0.02])
        self.assertEqual(attack_name, "LINEAR")
        self.assertEqual(attack_params, [0.02])


if __name__ == '__main__':
    unittest.main()


from xm_file import XMFile
import unittest


class TestDecoding(unittest.TestCase):
    def test_header_decoding(self):
        xm_file = XMFile("example.xm")

        info = f"""
Module name: {xm_file.header.module_name}
Length: {xm_file.header.song_length}
Channels: {xm_file.header.n_channels}
Patterns: {xm_file.header.n_patterns}
Pattern order: {xm_file.header.pattern_order_table}
Instruments: {xm_file.header.n_instruments}
BPM: {xm_file.header.bpm}
Tempo: {xm_file.header.tempo}
            """

        print(info)

        self.assertEqual(xm_file.header.module_name, "Latvia Best")
        self.assertEqual(xm_file.header.song_length, 8)
        self.assertEqual(xm_file.header.n_channels, 10)
        self.assertEqual(xm_file.header.n_patterns, 8)
        self.assertEqual(xm_file.header.n_instruments, 13)
        self.assertEqual(xm_file.header.bpm, 142)
        self.assertEqual(xm_file.header.tempo, 6)

    def test_sample_decoding(self):
        xm_file = XMFile("example.xm")
        s = xm_file.instruments[0].samples[0]

        self.assertEqual(s.sample_name, "Square 3")
        self.assertEqual(s.sample_size, 256)
        self.assertEqual(s.sample_loop_start, 0)
        self.assertEqual(s.sample_loop_length, 256)
        self.assertEqual(s.volume, 64)
        self.assertEqual(s.panning, 128)

        self.assertEqual(s.sample_data(), [11322] * 65 + [-11322] * 63)

    def test_pattern_decoding(self):
        xm_file = XMFile("example.xm")

        p = xm_file.patterns[0]

        self.assertEqual(len(xm_file.patterns), xm_file.header.n_patterns)

        first_pattern = p.pattern_data()[0]

        self.assertEqual(first_pattern[0], (55, 1, 0, 0, 0))
        self.assertEqual(first_pattern[1], (62, 1, 32, 0, 0))


if __name__ == "__main__":
    unittest.main()

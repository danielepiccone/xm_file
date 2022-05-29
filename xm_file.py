import struct
from collections import namedtuple

__version__ = "0.1.0"

XMHeader = namedtuple(
    "XMHeader",
    [
        "id_text",
        "module_name",
        "magic",
        "tracker_name",
        "version",
        "header_size",
        "song_length",
        "restart_position",
        "n_channels",
        "n_patterns",
        "n_instruments",
        "flags",
        "tempo",
        "bpm",
        "pattern_order_table",
    ],
)


def read_xm_header(fh):

    # Signature

    id_text = fh.read(17)
    module_name = fh.read(20).decode("ascii")
    magic = fh.read(1)
    tracker_name = fh.read(20).decode("ascii")
    version = struct.unpack("bb", fh.read(2))

    # Header

    header_size = struct.unpack("<I", fh.read(4))[0]
    song_length = struct.unpack("H", fh.read(2))[0]
    restart_position = struct.unpack("H", fh.read(2))[0]
    n_channels = struct.unpack("H", fh.read(2))[0]
    n_patterns = struct.unpack("H", fh.read(2))[0]
    n_instruments = struct.unpack("H", fh.read(2))[0]
    flags = struct.unpack("bb", fh.read(2))
    tempo = struct.unpack("H", fh.read(2))[0]
    bpm = struct.unpack("H", fh.read(2))[0]

    pattern_order_table_size = min(256, header_size - 20)
    pattern_order_table = tuple(
        struct.unpack("B" * pattern_order_table_size, fh.read(pattern_order_table_size))
    )

    return XMHeader(
        id_text,
        module_name,
        magic,
        tracker_name,
        version,
        header_size,
        song_length,
        restart_position,
        n_channels,
        n_patterns,
        n_instruments,
        flags,
        tempo,
        bpm,
        pattern_order_table,
    )


XMPattern = namedtuple(
    "XMPattern",
    [
        "pattern_size",
        "packing_type",
        "n_rows",
        "packed_size",
        "packed_data",
    ],
)


def read_xm_pattern(fh):

    # Pattern

    pattern_size = struct.unpack("<I", fh.read(4))[0]
    packing_type = fh.read(1)
    n_rows = struct.unpack("H", fh.read(2))[0]
    packed_size = struct.unpack("H", fh.read(2))[0]
    packed_data = fh.read(packed_size)  # TODO unpack patterns

    return XMPattern(
        pattern_size, packing_type, n_rows, packed_size, lambda: packed_data
    )


XMInstrument = namedtuple(
    "XMInstrument",
    [
        # First part of the header
        "instrument_size",
        "instrument_name",
        "instrument_type",
        "n_samples",
        # Second part of the header
        "sample_header_size",
        "sample_notes_number",
        "volume_points",
        "panning_points",
        "n_volume_points",
        "n_panning_points",
        "volume_sustain_point",
        "volume_loop_start_point",
        "volume_loop_end_point",
        "panning_sustain_point",
        "panning_loop_start_point",
        "panning_loop_end_point",
        "volume_type",
        "panning_type",
        "vibrato_type",
        "vibrato_sweep",
        "vibrato_depth",
        "vibrato_rate",
        "volume_fadeout",
        # Samples
        "samples",
    ],
)


def read_xm_instrument(fh):

    # Instrument

    fh_instrument_start = fh.tell()

    instrument_size = struct.unpack("<I", fh.read(4))[0]
    instrument_name = fh.read(22).decode("ascii")
    instrument_type = struct.unpack("B", fh.read(1))[0]
    n_samples = struct.unpack("H", fh.read(2))[0]

    if n_samples > 0:
        sample_header_size = struct.unpack("<I", fh.read(4))[0]
        sample_notes_number = struct.unpack("96B", fh.read(96))
        volume_points = tuple(struct.unpack("HH", fh.read(4)) for _ in range(12))
        panning_points = tuple(struct.unpack("hh", fh.read(4)) for _ in range(12))
        n_volume_points = struct.unpack("B", fh.read(1))[0]
        n_panning_points = struct.unpack("B", fh.read(1))[0]
        volume_sustain_point = struct.unpack("B", fh.read(1))[0]
        volume_loop_start_point = struct.unpack("B", fh.read(1))[0]
        volume_loop_end_point = struct.unpack("B", fh.read(1))[0]
        panning_sustain_point = struct.unpack("B", fh.read(1))[0]
        panning_loop_start_point = struct.unpack("B", fh.read(1))[0]
        panning_loop_end_point = struct.unpack("B", fh.read(1))[0]
        volume_type = struct.unpack("B", fh.read(1))[0]
        panning_type = struct.unpack("B", fh.read(1))[0]
        vibrato_type = struct.unpack("B", fh.read(1))[0]
        vibrato_sweep = struct.unpack("B", fh.read(1))[0]
        vibrato_depth = struct.unpack("B", fh.read(1))[0]
        vibrato_rate = struct.unpack("B", fh.read(1))[0]
        volume_fadeout = struct.unpack("H", fh.read(2))[0]
    else:
        sample_header_size = None
        sample_notes_number = None
        volume_points = None
        panning_points = None
        n_volume_points = None
        n_panning_points = None
        volume_sustain_point = None
        volume_loop_start_point = None
        volume_loop_end_point = None
        panning_sustain_point = None
        panning_loop_start_point = None
        panning_loop_end_point = None
        volume_type = None
        vibrato_type = None
        panning_type = None
        vibrato_sweep = None
        vibrato_depth = None
        vibrato_rate = None
        volume_fadeout = None

    fh.seek(fh_instrument_start + instrument_size)

    samples = []
    for _ in range(n_samples):
        samples.append(read_xm_sample(fh, sample_header_size))

    return XMInstrument(
        instrument_size,
        instrument_name,
        instrument_type,
        n_samples,
        sample_header_size,
        sample_notes_number,
        volume_points,
        panning_points,
        n_volume_points,
        n_panning_points,
        volume_sustain_point,
        volume_loop_start_point,
        volume_loop_end_point,
        panning_sustain_point,
        panning_loop_start_point,
        panning_loop_end_point,
        volume_type,
        vibrato_type,
        panning_type,
        vibrato_sweep,
        vibrato_depth,
        vibrato_rate,
        volume_fadeout,
        samples,
    )


XMSample = namedtuple(
    "XMSample",
    [
        "sample_size",
        "sample_loop_start",
        "sample_loop_length",
        "volume",
        "finetune",
        "type",
        "panning",
        "relative_note",
        "sample_name",
        "sample_data",
    ],
)


def read_xm_sample(fh, sample_header_size):

    fh_sample_start = fh.tell()

    # Sample

    sample_size = struct.unpack("<I", fh.read(4))[0]
    sample_loop_start = struct.unpack("<I", fh.read(4))[0]
    sample_loop_length = struct.unpack("<I", fh.read(4))[0]
    volume = struct.unpack("b", fh.read(1))[0]
    finetune = struct.unpack("b", fh.read(1))[0]
    type = struct.unpack("B", fh.read(1))[0]
    panning = struct.unpack("B", fh.read(1))[0]
    relative_note = struct.unpack("b", fh.read(1))[0]

    fh.read(1)  # reserved

    sample_name = fh.read(22).decode("ascii")

    # 16 bit sample data
    if type >> 2 == 4:
        sample_data = struct.unpack("h" * (sample_size // 2), fh.read(sample_size))
    else:
        sample_data = struct.unpack("b" * sample_size, fh.read(sample_size))

    fh.seek(fh_sample_start + sample_size + sample_header_size)

    return XMSample(
        sample_size,
        sample_loop_start,
        sample_loop_length,
        volume,
        finetune,
        type,
        panning,
        relative_note,
        sample_name,
        lambda: sample_data,
    )


class XMFile:
    def __init__(self, filename):
        self.__fh = open(filename, "rb")
        self.header = read_xm_header(self.__fh)
        self.patterns = [
            read_xm_pattern(self.__fh) for _ in range(self.header.n_patterns)
        ]
        self.instruments = [
            read_xm_instrument(self.__fh) for _ in range(self.header.n_instruments)
        ]

    def __del__(self):
        self.__fh.close()


if __name__ == "__main__":
    xm_file = XMFile("example.xm")

    info = f"""
Module name: {xm_file.header.module_name}
Length: {xm_file.header.song_length}
Channels: {xm_file.header.n_channels}
Patterns: {xm_file.header.n_channels}
Instruments: {xm_file.header.n_instruments}
BPM: {xm_file.header.bpm}
Tempo: {xm_file.header.tempo}
    """

    print(info)

# xm_file

Library for reading and unpacking Fasttracker II modules https://en.wikipedia.org/wiki/XM_(file_format).

### Documentation

The original spec `xm.txt` is included as part of the repo

### XMFile API

**property `.header`**

Module header information

**property `.patterns`**

List of patterns (including pattern data)

**property `.instruments`**

List of instruments (including samples and sample data)

### Examples

```python
from xm_file import XMFile

xm_file = XMFile("example.xm")

info = f"""
Module name: {xm_file.header.module_name}
Length: {xm_file.header.song_length}
Channels: {xm_file.header.no_channels}
Patterns: {xm_file.header.no_channels}
Instruments: {xm_file.header.no_instruments}
BPM: {xm_file.header.bpm}
Tempo: {xm_file.header.tempo}
"""

print(info)
```

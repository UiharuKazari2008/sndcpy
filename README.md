# sndcpy (tweaked version)
This is tweaked version of original by rom1v.

This version has some features:
- Support changing sampling rate and buffer size
- Show sampling rate in notification

## Changing sampling rate
To change sampling rate, add to `am` command with `--ei SAMPLE_RATE FREQ` option.
(e.g. 88.2kHz)
```
adb shell am start com.rom1v.sndcpy/.MainActivity --ei SAMPLE_RATE 88200
```

## Changing buffer size
Buffer size options are available 5 types:
- 0: Normal (1024*1024 bytes)
- 1: Smaller (1024*512 bytes)
- 2: Small (1024*256 bytes)
- 3: Very small (1024*128 bytes)
- 4: Super small (1024*64 bytes)
Warning: decrease buffer size may make audio choppy.

To change buffer size, add to `am` command with `--ei BUFFER_SIZE_TYPE NUM` option.
```
am start com.rom1v.sndcpy/.MainActivity --ei SAMPLE_RATE 48000 --ei BUFFER_SIZE_TYPE 3
```

## Original README
See https://github.com/rom1v/sndcpy/blob/master/README.md
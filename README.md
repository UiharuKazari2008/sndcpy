# sndcpy (tweaked version)
This is tweaked version of original by rom1v.

This version has some features:
- Support changing sampling rate and buffer size
- Show sampling rate in notification
- Automatically restart on socket disconnect
- Log when socket is ready and when it's restarting.
- Corrected a bug where the AudioRecorder

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

## Relay Server
Relay servers allow multiple connections to the sndcpy server.

Requirements:
- Python 3.8+

Usage:
1. Install sndcpy apk
2. Run `start_sndcpy_relay.bat` or `start_sndcpy_relay.sh`
3. Connect localhost:28201 via FFplay, mpv etc. (when default settings. Sampling rate depends your settings)

Parameters:
All parameters are optional.

- `--sndcpy-host HOSTNAME`
  sndcpy's hostname (default: `localhost`)
- `--sndcpy-port PORT`
  sndcpy's forwarding port (default: `28200`)
- `--bind ADDR`
  Address to listen relay server (e.g. `0.0.0.0` allows you to connect in LAN networks) (default: `localhost`)
- `--port PORT`
  Port to listen relay server (default: `28201`)

## Original README
See https://github.com/rom1v/sndcpy/blob/master/README.md
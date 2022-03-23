@echo off
set samplerate=48000
if not "%1"=="" (
    set samplerate=%1
)
echo Grant PROJECT_MEDIA permission to sndcpy...
adb shell appops set com.rom1v.sndcpy PROJECT_MEDIA allow

echo Forwarding UNIX Socket...
adb forward tcp:28200 localabstract:sndcpy

echo Starting sndcpy service...
adb shell am kill com.rom1v.sndcpy
adb shell am start -n com.rom1v.sndcpy/.MainActivity --ei SAMPLE_RATE %samplerate% --ei BUFFER_SIZE_TYPE 3

timeout 2

py .\sndcpy_relay.py
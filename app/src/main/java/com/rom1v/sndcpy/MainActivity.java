package com.rom1v.sndcpy;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.projection.MediaProjectionManager;
import android.os.Bundle;
import android.util.Log;

public class MainActivity extends Activity {

    private static final int REQUEST_CODE_PERMISSION_AUDIO = 1;
    private static final int REQUEST_CODE_START_CAPTURE = 2;

    private static int mSampleRate = 48000;
    /*
        Buffer Size Types
        (decrease buffer size may make audio choppy)
        0: Normal (1024*1024 bytes)
        1: Smaller (1024*512 bytes)
        2: Small (1024*256 bytes)
        3: Very Small (1024*128 bytes)
        4: Super Small (1024*64 bytes)
    */
    private static int mBufferSizeType = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            String[] permissions = {Manifest.permission.RECORD_AUDIO};
            requestPermissions(permissions, REQUEST_CODE_PERMISSION_AUDIO);
        }

        Intent appIntent = getIntent();
        mSampleRate = appIntent.getIntExtra("SAMPLE_RATE", 48000);
        mBufferSizeType = appIntent.getIntExtra("BUFFER_SIZE_TYPE", 0);
        if (mBufferSizeType < 0) {
            mBufferSizeType = 0;
        }
        if (mBufferSizeType > 4) {
            mBufferSizeType = 4;
        }

        MediaProjectionManager mediaProjectionManager = (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
        Intent intent = mediaProjectionManager.createScreenCaptureIntent();

        startActivityForResult(intent, REQUEST_CODE_START_CAPTURE);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_CODE_START_CAPTURE && resultCode == Activity.RESULT_OK) {
            data.putExtra("SAMPLE_RATE", mSampleRate);
            data.putExtra("BUFFER_SIZE_TYPE", mBufferSizeType);
            RecordService.start(this, data);
        }
        finish();
    }
}

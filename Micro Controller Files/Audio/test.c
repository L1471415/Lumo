#include <stdint.h>
#include <math.h>
// Important Readings: 
// https://dylanmeeus.github.io/posts/audio-from-scratch-pt2/
// http://soundfile.sapp.org/doc/WaveFormat/
// https://www.mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html


int processAudioBytes(uint8_t (audioBytes*)[], int audioBytesSize, int BitsPerSample = 16000){

    if (audioBytesSize % BitsPerSample != 0){
        return -1;
    }

    

    return 0; 
}

int amplifyAudioBytes(uint8_t (audioBytes*)[], int totalBytes, float amplifer){

    for (int i = 0; i < totalBytes; i++){
        try {
        int compare = ceil(audioBytes[i] * totalBytes);
        if (compare <= 256){
            audioBytes[i] = compare;
        }
        else {
            audioBytes = 256;
        }
        }
        catch(Exception e){
            return -1;
        }
    }
    return 0;
}
import random
import os

import numpy as np

from deep_speaker.audio import read_mfcc, mfcc_fbank
from deep_speaker.batcher import sample_from_mfcc
from deep_speaker.constants import SAMPLE_RATE, NUM_FRAMES
from deep_speaker.conv_models import DeepSpeakerModel
from deep_speaker.test import batch_cosine_similarity

from audio.handling import SpeechSegment

np.random.seed(123)
random.seed(123)

model = DeepSpeakerModel()

model.m.load_weights('./files/models/deep_speaker.h5', by_name=True)


# Code taken Phillpperemy, developer of Deep-Speaker and slightly modified to work with bytes
def read_mfcc_bytes(audio_array:np.ndarray, sample_rate:int) -> np.ndarray:
    return mfcc_fbank(clean_audio(audio_array), sample_rate)


def clean_audio(audio):
    energy = np.abs(audio)
    silence_threshold = np.percentile(energy, 95)
    offsets = np.where(energy > silence_threshold)[0]
    return audio[offsets[0]:offsets[-1]]


# Original Sample Code from: Phillpperemy, developer of Deep-Speaker https://github.com/philipperemy/deep-speaker
def calculate_similarity_file_file(filepath_1, filepath_2):

    mfcc_001 = sample_from_mfcc(read_mfcc(filepath_1, SAMPLE_RATE), NUM_FRAMES)
    mfcc_002 = sample_from_mfcc(read_mfcc(filepath_2, SAMPLE_RATE), NUM_FRAMES)

    predict_001 = model.m.predict(np.expand_dims(mfcc_001, axis=0))
    predict_002 = model.m.predict(np.expand_dims(mfcc_002, axis=0))

    return batch_cosine_similarity(predict_001, predict_002)


def calculate_similarity_file_arr(sample_file, audio_array):
    mfcc_001 = sample_from_mfcc(read_mfcc(sample_file, SAMPLE_RATE), NUM_FRAMES)
    mfcc_002 = sample_from_mfcc(read_mfcc_bytes(audio_array, SAMPLE_RATE), NUM_FRAMES)

    predict_001 = model.m.predict(np.expand_dims(mfcc_001, axis=0))
    predict_002 = model.m.predict(np.expand_dims(mfcc_002, axis=0))

    return batch_cosine_similarity(predict_001, predict_002)


def calculate_similarity_file_bytes(sample_file, audio_bytes):
    audio_array = np.frombuffer(audio_bytes)

    mfcc_001 = sample_from_mfcc(read_mfcc(sample_file, SAMPLE_RATE), NUM_FRAMES)
    mfcc_002 = sample_from_mfcc(read_mfcc_bytes(audio_array, SAMPLE_RATE), NUM_FRAMES)

    predict_001 = model.m.predict(np.expand_dims(mfcc_001, axis=0))
    predict_002 = model.m.predict(np.expand_dims(mfcc_002, axis=0))

    return batch_cosine_similarity(predict_001, predict_002)


def calculate_similarity_from_segments(segment_1:SpeechSegment, segment_2:SpeechSegment) -> float:
    '''Method to calculate the similarity of 2 SpeechSegment's audio data

        Parameters:
            segment_1 (SpeechSegment): The first segment to compare
            segment_2 (SpeechSegment): The second segment to compare

        Returns (float):
            The cosine similarity of the 2 segments
    '''
    mfcc_001 = sample_from_mfcc(read_mfcc_bytes(segment_1.get_audio_array(), 16000), NUM_FRAMES)
    mfcc_002 = sample_from_mfcc(read_mfcc_bytes(segment_2.get_audio_array(), 16000), NUM_FRAMES)

    predict_001 = model.m.predict(np.expand_dims(mfcc_001, axis=0))
    predict_002 = model.m.predict(np.expand_dims(mfcc_002, axis=0))

    return batch_cosine_similarity(predict_001, predict_002)

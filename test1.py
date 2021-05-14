from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

speech_file = "D:/New folder/doctor.wav"

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=8000,
    language_code="en-IN",
    enable_speaker_diarization=True,
    diarization_speaker_count=2,
)

print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)
# print(response)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]
speaker1_transcript=''
speaker2_transcript=''
words_info = result.alternatives[0].words

# Printing out the output:
for word_info in words_info:
    if (word_info.speaker_tag==1):
        speaker1_transcript=speaker1_transcript+word_info.word+' '
    elif (word_info.speaker_tag==2):
        speaker2_transcript=speaker2_transcript+word_info.word+' '

print("speaker1: '{}'".format(speaker1_transcript))
print("speaker2: '{}'".format(speaker2_transcript))
# speaker2= '{}'.format(speaker2_transcript)
# med=["Crocin","Disprin","Paracetamol"]
# print(type(speaker2))
# r1=[]
# for i in range(len(speaker2)):
#     if med[i] in speaker2:
#         r1.append(med[i])
# print(r1)


# print(speaker1_transcript,word_info.speaker_tag)
# print(speaker2_transcript,word_info.speaker_tag)        

    # print(
    #     u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
    # )
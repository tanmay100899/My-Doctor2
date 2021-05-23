from google.cloud import speech_v1p1beta1 as speech
from fpdf import FPDF

client = speech.SpeechClient()

speech_file = "D:/New folder/s3.wav"

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

s1="speaker1: '{}'".format(speaker1_transcript)
s2="speaker2: '{}'".format(speaker2_transcript)
s3=s1+s2
# speaker2= '{}'.format(speaker2_transcript)
med1=[]
day1=[]
med=["Crocin","Disprin","Paracetamol","Dolo 650"]
for i in range(len(med)):
    if med[i] in s3:
        med1.append(med[i])
l1=s3.split()
for i in range(len(l1)):
    if "days" in l1[i] or "times" in l1[i]:
        day1.append(l1[i-1])
print(day1)


pdf = FPDF()
pdf.add_page()
pdf.ln(50)
pdf.set_font("Arial","B", size=20)
epw = pdf.w - 2*pdf.l_margin
pdf.cell(200, 10.0, txt="Demo Medical Prescription", ln=1, align="C")
# Effective page width, or just epw
# Set column width to 1/4 of effective page width to distribute content 
# evenly across table and page
col_width = epw/4
print(med1)
print(day1)

data=[['SrNo','Medicine','duration','times']]
for i in range(len(med1)):
	data.append([i+1,med1[i],day1[i*2],day1[(i*2)+1]])
pdf.ln(10)
pdf.set_font("Arial", size=10)
th = pdf.font_size
for row in data:
    for datum in row:
        pdf.cell(col_width, 4*th, str(datum), border=0)
 
    pdf.ln(4*th)
pdf.output("demo8.pdf")

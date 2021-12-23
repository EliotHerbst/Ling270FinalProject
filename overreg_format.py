import os, glob
from chaParser import Transcript

correct_irregs = set()
overreg_irregs = set()
irregulars_path = './irreg/verb-past-overreg.txt'
with open(irregulars_path, 'r') as f:
    text = f.read()
    for t in text.splitlines():
        spl = t.split()
        correct_irregs.add(spl[1])
        overreg_irregs.add(spl[2])


transcript_folder = './transcripts'
output_file = 'overreg_data.csv'
transcripts = []
for filename in glob.glob(os.path.join(transcript_folder, '*.cha')):
    with open(filename, 'r', encoding='UTF-8') as f:
        s = f.read()
        transcripts.append(Transcript(s, filename))
with open(output_file, 'w', encoding='UTF-8') as f:
    for transcript in transcripts:
        if len(transcript.languages) != 1 or transcript.languages[0] != 'eng':
            continue
        for participant in transcript.participants:    
            part = transcript.participants[participant]
            if len(part.utterances) < 1:
                continue
            f.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},\n'.format(transcript.filename, part.language, part.corpus, part.code, part.age, part.sex, part.group, transcript.name_dict[part.code], part.mlu_words, len(part.correct_irregs), len(part.overreg_irregs), ' '.join(part.correct_irregs), ' '.join(part.overreg_irregs), len(part.utterances)))
    
        
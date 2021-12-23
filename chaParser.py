from os import name
from string import ascii_letters

correct_irregs = set()
overreg_irregs = set()
irregulars_path = './irreg/verb-past-overreg.txt'
with open(irregulars_path, 'r') as f:
    text = f.read()
    for t in text.splitlines():
        spl = t.split()
        correct_irregs.add(spl[1])
        overreg_irregs.add(spl[2])

valid = set(ascii_letters + ' ')

class Participant:
    def setup(self, language, corpus, code, age, sex, group, ses, role, education, custom):
        self.language = language
        self.corpus = corpus
        self.code = code
        self.age = age
        self.sex = sex
        self.group = group
        self.ses = ses
        self.role = role
        self.education = education
        self.custom = custom
        self.utterances = []
        self.mlu_words = 0
        self.correct_irregs = []
        self.overreg_irregs = []
    
    def __init__(self, id_line):
        self.setup(*id_line.replace(',','').split('|'))

    def add_utterance(self, utterance_line):
        utterance = ''.join(filter(valid.__contains__, utterance_line.split(':\t')[1]))
        self.utterances.append(utterance)
        self.mlu_words = sum([sum(len(ut.split()) for ut in self.utterances)]) / len(self.utterances)
        for word in utterance.split():
            if word in correct_irregs:
                self.correct_irregs.append(word)
            if word in overreg_irregs:
                self.overreg_irregs.append(word)

class Transcript: 
    def __init__(self, transcript_text, filename):
        self.filename = filename
        self.languages = ''.join(transcript_text.split('@Languages:\t')[1].split('\n')[0].strip().split()).split(',')
        name_strings = transcript_text.split('@Participants:\t')[1].split('@')[0].strip().split(',')
        self.name_dict = {s.split()[0].strip() : s.split()[1].strip() for s in name_strings}
        self.participants = {id.split(None, 1)[1].strip()[0:-1].split('|')[2]: Participant(id.split(None, 1)[1].strip()[0:-1]) for id in transcript_text.split('\n') if id.startswith('@ID:')}
        for line in transcript_text.split('\n'):
            if line.startswith('*'):
                code = line[line.index('*') + 1: line.index(':')]
                self.participants[code].add_utterance(line)
    

    


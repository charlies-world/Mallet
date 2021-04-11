from compoyse.midi.Note import Note
from compoyse.midi.Rest import Rest
from compoyse.midi.Measure import Measure
from compoyse.midi.Voice import Voice
from compoyse.midi.Composition import Composition
from compoyse.midi.Meter import Meter
from compoyse.wav.AudioFile import AudioFile
from compoyse.wav.AudioClip import AudioClip
from compoyse.wav.AudioPlayer import AudioPlayer
import random
from datetime import datetime

class Mallet:
    def __init__(self,
                 pitch,
                 number_of_beats_per_measure,
                 rhythmic_value_for_beat,
                 likelihood_of_change,
                 number_of_measures,
                 maximum_number_of_notes_per_measure,
                 minimum_number_of_notes_per_measure,
                 voice_number):
        self.voice = Voice()
        self.note_letter = ''
        self.octave = 0
        self.number_of_beats_per_measure = number_of_beats_per_measure
        self.rhythmic_value = rhythmic_value_for_beat
        self.likelihood_of_change = likelihood_of_change
        self.number_of_measures = number_of_measures
        self.maximum_number_of_notes_per_measure = maximum_number_of_notes_per_measure
        self.minimum_number_of_notes_per_measure = minimum_number_of_notes_per_measure
        self.voice.set_name = 'voice' + str(voice_number)
        self.beats = []
        
        self.parse_pitch(pitch)
        self.make_beats()

        return
    
    def parse_pitch(self, pitch):
        self.note_letter = pitch[0]
        self.octave = pitch[1]
        return
    
    def make_beats(self):
        for i in range(0, self.number_of_beats_per_measure):
            self.beats.append(False)
        return
    
    def compose(self):
        self.create_first_measure()
        
        for i in range(0, self.number_of_measures - 1):
            self.choose_and_change_beats()
            self.create_and_add_measure_midi_data()
            
        return self.voice
    
    def create_first_measure(self):
        self.beats[random.randint(0, 7)] = True
        return
    
    def choose_and_change_beats(self):
        for j in range(0, len(self.beats)):
            if random.randint(0, self.likelihood_of_change) == 0:
                self.change_beat(j)
        return
    
    def change_beat(self, index_of_beat):
        if self.beats[index_of_beat] == True and self.is_not_at_minimum_number_of_notes():
            self.beats[index_of_beat] = False
        elif self.beats[index_of_beat] == False and self.is_not_at_max_number_of_notes():
            self.beats[index_of_beat] = True
        return
    
    def is_not_at_minimum_number_of_notes(self):
        number_of_notes = self.get_number_of_notes()
        return (number_of_notes >= self.minimum_number_of_notes_per_measure)    
    
    def is_not_at_max_number_of_notes(self):
        number_of_notes = self.get_number_of_notes()
        return (number_of_notes <= self.maximum_number_of_notes_per_measure)
    
    def get_number_of_notes(self):
        number_of_notes = 0
        for i in range(0, len(self.beats)):
            if self.beats[i] == True:
                number_of_notes = number_of_notes + 1
        return number_of_notes
    
    def create_and_add_measure_midi_data(self):
        measure = Measure()
        for i in range(0, len(self.beats)):
            if(self.beats[i] == True):
                beat = Note()
                beat.set_letter(self.note_letter)
                beat.set_octave(self.octave)
                beat.set_rhythmic_value([self.rhythmic_value])
                beat.set_velocity(100)
            elif(self.beats[i] == False):
                beat = Rest()
                beat.set_rhythmic_value([self.rhythmic_value])
            measure.add_beat(beat)
        self.voice.add_measure(measure)
        return

pitch_set = [
            ['G#', 2],
            ['B', 2],
            ['D', 3],
            ['F#', 3],
            ['A', 4],
            ['C#', 4],
            ['A', 5],
            ['E', 5]
            ]
number_of_measures = 300
number_of_beats_per_measure = 8
maximum_number_of_notes_per_measure = 5
minimum_number_of_notes_per_measure = 1
rhythmic_value_for_beat = 'eighth'
quarter_note_tempo = 1000
likelihood_of_change = 1000


c = Composition()
c.set_quarter_note_bpm(quarter_note_tempo)

for i in range(0, len(pitch_set)):
    mallet_voice = Mallet(pitch_set[i],
                   number_of_beats_per_measure,
                   rhythmic_value_for_beat,
                   likelihood_of_change,
                   number_of_measures,
                   maximum_number_of_notes_per_measure,
                   minimum_number_of_notes_per_measure,
                   i)
    voice = mallet_voice.compose()
    c.add_voice(voice)

now = datetime.now()
current_time_formatted = now.strftime("%d.%m.%Y %H.%M.%S")
c.write_midi_data('mallet' + ' ' + current_time_formatted)
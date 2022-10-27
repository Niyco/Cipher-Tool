import darkdetect
import json
import sys

theme_path = r'themes/'
lang_path = r'lang/'
modes = ['light', 'dark']
default_size ='1366x768'
min_size = '672x378'
check_queue_delay = 100
toolbar_step = 12
toolbar_updates = 0
toolbar_delay = 12
stages_drag_max = 8
loading_delay = 50
threaded = False
mode_name = 'default'
theme_name = 'blue'
lang_name = 'en'
morse_codes = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h',
               '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
               '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
               '-.--': 'y', '--..': 'z', '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
               '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'}
binary_codes = {'00000': 'a', '00001': 'b', '00010': 'c', '00011': 'd', '00100': 'e', '00101': 'f', '00110': 'g',
                '00111': 'h', '01000': 'i', '01001': 'j', '01010': 'k', '01011': 'l', '01100': 'm', '01101': 'n',
                '01110': 'o', '01111': 'p', '10000': 'q', '10001': 'r', '10010': 's', '10011': 't', '10100': 'u',
                '10101': 'v', '10110': 'w', '10111': 'x', '11000': 'y', '11001': 'z'}
baconian_codes = {'aaaaa': 'a', 'aaaab': 'b', 'aaaba': 'c', 'aaabb': 'd', 'aabaa': 'e', 'aabab': 'f', 'aabba': 'g',
                'aabbb': 'h', 'abaaa': 'i', 'aabaaa': 'j', 'abaab': 'k', 'ababa': 'l', 'ababb': 'm', 'abbaa': 'n',
                'abbab': 'o', 'abbba': 'p', 'abbbb': 'q', 'baaaa': 'r', 'baaab': 's', 'baaba': 't', 'abaabb': 'u',
                'baabb': 'v', 'babaa': 'w', 'babab': 'x', 'babba': 'y', 'babbb': 'z'}
baudot_codes = {'00000': ('', ''), '01000': ('\n', '\n'), '00010': ('\n', '\n'), '00100': (' ', ' '),
                '10111': ('q', '1'), '10011': ('w', '2'), '00001': ('e', '3'), '01010': ('r', '4'),
                '10000': ('t', '5'), '10101': ('y', '6'), '00111': ('u', '7'), '00110': ('i', '8'),
                '11000': ('o', '9'), '10110': ('p', '0'), '00011': ('a', '-'), '00101': ('s', '\''),
                '01001': ('d', 'WRU?'), '01101': ('f', '!'), '11010': ('g', '&'), '10100': ('h', '$'),
                '01011': ('j', 'BELL'), '01111': ('k', '('), '10010': ('l', ')'), '10001': ('z', '+'),
                '11101': ('x', '/'), '01110': ('c', ':'), '11110': ('v', '='), '11001': ('b', '?'),
                '01100': ('n', ','), '11100': ('m', '.'), '11011': ('FS', 'FS'), '11111': ('LS', 'LS')}

class Stage:
    def __init__(self, update_output):
        self.update_output = update_output
        self.update_vars = ()

    def setup(self, frame, texts):
        self.frame = frame
        self.texts = texts
        
    @staticmethod
    def update(text):
        return ((), ())

    def update_widgets(self):
        pass
    
    def display(self):
        pass

def load_constants():
    global os, mode, theme, lang, letter_frequencies, word_frequencies, alphabet
    global min_word_frequency, max_word_length, language_ioc

    theme_file = open(theme_path + theme_name + '.json')
    theme = json.load(theme_file)
    theme_file.close()
    lang_file = open(lang_path + 'lang_' + lang_name + '.json')
    lang = json.load(lang_file)
    lang_file.close()
    freq_file = open(lang_path + 'freq_' + lang_name + '.json')
    freq_data = json.load(freq_file)
    freq_file.close()
    
    if sys.platform.startswith('darwin'): os = 'macOS'
    elif sys.platform.startswith('win'): os = 'Windows'
    elif sys.platform.startswith('linux'): os = 'Linux'
    if mode_name == 'light': mode = 0
    elif mode_name == 'dark': mode = 1
    else: mode = modes.index(darkdetect.theme().lower())
    
    letter_frequencies = freq_data['letters']
    language_ioc = sum([letter_frequencies[x] ** 2 for x in letter_frequencies])
    alphabet = list(letter_frequencies.keys())
    min_word_frequency = 10 ** ((0 - len(freq_data['words']) + 1) / 100)
    max_word_length = 0
    word_frequencies = {}
    for index, bucket in enumerate(freq_data['words']):
        freq = 10 ** (-index / 100)
        for word in bucket:
            length = len(word)
            if length > max_word_length:
                max_word_length = length
            word_frequencies[word] = freq

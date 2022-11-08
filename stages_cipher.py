from defined import Stage
import tkinter as tk
import customtkinter as ctk
import unicodedata
import pickle
import base64

class BinaryCode(Stage):
    def __init__(self, update_output):
        super().__init__(update_output)
        self.encode_var = tk.IntVar(value=0)
        self.mode_var = tk.IntVar(value=0)
        self.option_var = tk.IntVar(value=0)
        self.letter_separator_var = tk.StringVar(value='')
        self.word_separator_var = tk.StringVar(value='')
        self.update_vars.extend([0, 0, 0])
    
    def setup(self, frame, constants):
        super().setup(self, frame, constants)
        self.mode_var.trace('w', self.input_update)
        self.encode_var.trace('w', self.input_update)
        self.letter_separator_var.trace('w', self.input_update)
        self.word_separator_var.trace('w', self.input_update)
        self.option_var.trace('w', self.input_update)
        self.update_vars.extend([self.letter_separator_var.get(), self.word_separator_var.get()])
        self.encode = ctk.CTkSwitch(frame, text=self.texts['encode'], onvalue=1, offvalue=0,
                                    variable=self.encode_var)
        self.cipher_radio_1 = ctk.CTkRadioButton(frame, variable=self.mode_var, value=0,
                                                 text=self.texts['cipher_radio_1'])
        self.cipher_radio_2 = ctk.CTkRadioButton(frame, variable=self.mode_var, value=1,
                                                 text=self.texts['cipher_radio_2'])
        self.cipher_radio_3 = ctk.CTkRadioButton(frame, variable=self.mode_var, value=2,
                                                 text=self.texts['cipher_radio_3'])
        self.cipher_radio_4 = ctk.CTkRadioButton(frame, variable=self.mode_var, value=3,
                                                 text=self.texts['cipher_radio_4'])
        self.option_radio_1 = ctk.CTkRadioButton(frame, variable=self.option_var, value=0,
                                                 text=self.texts['option_radio_1'])
        self.option_radio_2 = ctk.CTkRadioButton(frame, variable=self.option_var, value=1,
                                                 text=self.texts['option_radio_2'])
        self.option_radio_3 = ctk.CTkRadioButton(frame, variable=self.option_var, value=0,
                                                 text=self.texts['option_radio_3'])
        self.option_radio_4 = ctk.CTkRadioButton(frame, variable=self.option_var, value=1,
                                                 text=self.texts['option_radio_4'])
        self.option_radio_5 = ctk.CTkRadioButton(frame, variable=self.option_var, value=0,
                                                 text=self.texts['option_radio_5'])
        self.option_radio_6 = ctk.CTkRadioButton(frame, variable=self.option_var, value=1,
                                                 text=self.texts['option_radio_6'])
        self.label_1 = ctk.CTkLabel(frame, text=self.texts['label_1'])
        self.input_1 = ctk.CTkEntry(frame, textvariable=self.letter_separator_var, width=60)
        self.label_2 = ctk.CTkLabel(frame, text=self.texts['label_2'])
        self.input_2 = ctk.CTkEntry(frame, textvariable=self.word_separator_var, width=60)
    
    def input_update(self, var_name, index, mode):
        if var_name == str(self.encode_var):
            value = self.encode_var.get()
            index = 0
        elif var_name == str(self.mode_var):
            self.display()
            value = self.mode_var.get()
            index = 1
        elif var_name == str(self.option_var):
            value = self.option_var.get()
            index = 2
        elif var_name == str(self.letter_separator_var):
            var = self.letter_separator_var
            value = var.get()
            if value == self.texts['space']:
                value = ' '
            elif value == ' ':
                var.set(self.texts['space'])
            index = 3
        elif var_name == str(self.word_separator_var):
            var = self.word_separator_var
            value = var.get()
            if value == self.texts['space']:
                value = ' '
            elif value == ' ':
                var.set(self.texts['space'])
            index = 4

        self.update_vars[index] = value
        self.update_output(self)
        
    @staticmethod
    def update(text, constants, encode, mode, option, letter_separator, word_separator):
        if len(text) == 0:
            return (text, ())
        text_original = text
        text = text.lower()
        
        if mode == 0:
            codes = constants.morse_codes
            if encode:
                codes = {v: k for k, v in codes.items()}
        elif mode == 1:
            codes = constants.baconian_codes
            if option == 1:
                new_codes = {}
                to_add = 0
                for index, item in enumerate(codes.items()):
                    k, v = item
                    if index == 9 or index == 21:
                        to_add += 1
                    k = k.replace('a', '0').replace('b', '1')
                    k = format(int(k, 2) + to_add, '05b')
                    k = k.replace('0', 'a').replace('1', 'b')
                    if encode:
                        new_codes[v] = k
                    else:
                        new_codes[k] = v
                codes = new_codes
            elif encode:
                codes = {v: k for k, v in codes.items()}
        elif mode == 2:
            codes = constants.binary_codes
            if option == 1:
                codes = {format(int(k, 2) + 1, '05b'): v for k, v in codes.items()}
            if encode:
                codes = {v: k for k, v in codes.items()}
        if mode == 3:
            codes = constants.baudot_codes
            if option == 1:
                codes = {k[::-1]: v for k, v in codes.items()}
            if encode:
                new_codes_1 = {}
                new_codes_2 = {}
                for k, v in codes.items():
                    new_codes_1[v[0]] = k
                    new_codes_2[v[1]] = k
                codes = (new_codes_1, new_codes_2)

                def encode_letter(letter, shift):
                    for i in range(len(codes)):
                        if letter in codes[i]:
                            new_letter = codes[i][letter]
                            if shift != i and (i != 1 or letter not in codes[0]):
                                if i:
                                    new_letter = codes[i]['FS'] + letter_separator + new_letter
                                else:
                                    new_letter = codes[i]['LS'] + letter_separator + new_letter
                                shift = i
                            return new_letter, shift
                    return '', shift
                        
                        
            else:
                def decode_word(word, shift):
                    decoded_word = ''
                    for char in word.split(letter_separator):
                        if char in codes:
                            new_char = codes[char][shift]
                            if new_char == 'LS':
                                shift = 0
                            elif new_char == 'FS':
                                shift = 1
                            else:
                                decoded_word += new_char
                    return decoded_word, shift
        elif encode:
            def encode_letter(letter, shift):
                if letter in codes:
                    return codes[letter], shift
                return '', shift
        else:
            def decode_word(word, shift):
                decoded_word = ''
                for char in word.split(letter_separator):
                    if char in codes:
                        decoded_word += codes[char]
                return decoded_word, shift
        result = ''
            
        if encode:
            shift = 0

            if mode == 3:
                for letter in text:
                    encoded_letter, shift = encode_letter(letter, shift)
                    result += encoded_letter
                
            else:
                words = text.split(' ')
                
                for word in words:
                    if word:
                        for letter in word:
                            encoded_letter, shift = encode_letter(letter, shift)
                            result += encoded_letter
                            if letter_separator != '' and encoded_letter:
                                result += letter_separator
                        if word_separator != '':
                            result += word_separator + letter_separator
                if word_separator != '':
                    result = result.removesuffix(word_separator + letter_separator)
                result = result.removesuffix(letter_separator)

        else:
            if word_separator != '' and letter_separator != '':
                shift = 0
                for word in text.split(word_separator):
                    decoded_word, shift = decode_word(word, shift)
                    result += decoded_word
                    result += ' '
                result = result[:-1]
                
            elif letter_separator != '':
                result, shift = decode_word(text, 0)
                
            elif mode:
                text.replace(' ', '')
                blocked = ['']
                for index, character in enumerate(text):
                    blocked[-1] += character
                    if (index + 1) % 5 == 0:
                        blocked.append('')
                letter_separator = ' '
                shift = 0
                for char in blocked:
                    decoded_char, shift = decode_word(char, shift)
                    result += decoded_char
                    
            if not result.replace(' ', ''):
                result = text_original
        
        return (result, ())

    def display(self):
        self.frame.columnconfigure(0, weight=1, minsize=250)
        self.frame.columnconfigure(3, weight=0)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(4, minsize=65)
        self.frame.rowconfigure(5, minsize=65)
        self.frame.rowconfigure(6, weight=1)
        self.cipher_radio_1.grid(column=0, row=0, padx=30, pady=6, sticky='WS')
        self.cipher_radio_2.grid(column=0, row=1, padx=30, pady=6, sticky='W')
        self.cipher_radio_3.grid(column=0, row=2, padx=30, pady=6, sticky='W')
        self.cipher_radio_4.grid(column=0, row=3, padx=30, pady=6, sticky='W')
        self.label_1.grid(column=0, row=1, columnspan=2, sticky='E')
        self.input_1.grid(column=2, row=1, sticky='W')
        self.label_2.grid(column=0, row=2, columnspan=2, sticky='E')
        self.input_2.grid(column=2, row=2, sticky='W')
        self.encode.grid(column=2, row=6, padx=15, pady=15, sticky='SE')

        options_radios = [self.option_radio_1, self.option_radio_2, self.option_radio_3,
                          self.option_radio_4, self.option_radio_5, self.option_radio_6]
        mode = self.mode_var.get()
        grid_add = options_radios[(mode - 1) * 2:mode * 2]
        grid_forget = set(options_radios[:(mode - 1) * 2] + options_radios[(mode) * 2:])

        for widget in grid_forget:
            widget.grid_forget()
        if grid_add:
            grid_add[0].grid(column=0, row=4, padx=30, pady=15, sticky='WS')
            grid_add[1].grid(column=0, row=5, padx=30, pady=0, sticky='NW')

class Caesar(Stage):
    def __init__(self, update_output):
        super().__init__(update_output)
        self.encode_var = tk.IntVar(value=0)
        self.shift_var = tk.IntVar(value=0)
        self.update_vars.extend([0, 0])

    def setup(self, frame, constants):
        super().setup(self, frame, constants)
        self.encode_switch = ctk.CTkSwitch(frame, text=self.texts['encode'], onvalue=1, offvalue=0,
                                    variable=self.encode_var)
        self.shift_slider = ctk.CTkSlider(frame, from_=0, to=25, number_of_steps=25, width=375,
                                          variable=self.shift_var)
        self.label = ctk.CTkLabel(frame, text=self.texts['label'] + ' ' + str(self.shift_var.get()))
        self.text = ctk.CTkEntry(frame)
        self.shift_var.trace('w', self.trace_update)
        self.encode_var.trace('w', self.trace_update)

    def trace_update(self, var_name, index, mode):
        if var_name == str(self.shift_var):
            self.label.configure(text=self.texts['label'] + ' ' + str(self.shift_var.get()))
            self.update_vars[1] = self.shift_var.get()
        else:
            self.update_vars[0] = self.encode_var.get()
        self.update_output(self)

    @staticmethod
    def update(text, constants, encode, shift):
        if encode:
            shift = 26 - shift
            
        shifted = ''
        for letter in text:
            if letter.lower() in constants.alphabet:
                index = (constants.alphabet.index(letter.lower()) - shift) % 26
                shifted_letter = constants.alphabet[index]
                if letter.isupper():
                    shifted_letter = shifted_letter.upper()
                shifted += shifted_letter
            else:
                shifted += letter
        
        return (shifted, ())

    def display(self):
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.encode_switch.grid(row=1, column=0, padx=15, pady=15, sticky='SE')
        self.label.grid(row=0, column=0, pady=20, sticky='S')
        self.shift_slider.grid(row=1, column=0, sticky='N')

class Substitution(Stage):
    def __init__(self, update_output):
        super().__init__(update_output)
        self.encode_var = tk.IntVar(value=0)
        self.substitutions = {}
        self.update_vars.extend([0, {}])
        
    def setup(self, frame, constants):
        super().setup(self, frame, constants)
        self.encode_switch = ctk.CTkSwitch(frame, text=self.texts['encode'], onvalue=1, offvalue=0,
                                           variable=self.encode_var)
        self.input_1 = ctk.CTkEntry(frame, width=60)
        self.label = ctk.CTkLabel(frame, text='->', width=20)
        self.input_2 = ctk.CTkEntry(frame, width=60)
        self.button_1 = ctk.CTkButton(frame, text=self.texts['button_1'], width=110)
        self.button_2 = ctk.CTkButton(frame, text=self.texts['button_2'], width=110)
        self.textbox = tk.Text(frame, bd=0, bg=self.constants.theme['color']['entry'][self.constants.mode],
                               fg=constants.theme['color']['text'][self.constants.mode], width=12, state='disabled',
                               insertbackground=self.constants.theme['color']['text'][self.constants.mode],
                               selectbackground=self.constants.theme['color']['entry'][self.constants.mode])
        self.scrollbar = ctk.CTkScrollbar(frame, command=self.textbox.yview, hover=False, height=350)
        self.textbox.configure(yscrollcommand=self.scrollbar.set)
        self.keyword = ctk.CTkButton(frame, text=self.texts['keyword'], command=self.get_keyword)

        self.input_1.bind('<Tab>', lambda event: self.tab_order(0))
        self.input_2.bind('<Tab>', lambda event: self.tab_order(1))
        self.button_1.bind('<Tab>', lambda event: self.tab_order(2))
        self.button_2.bind('<Tab>', lambda event: self.tab_order(3))
        self.button_1.bind('<space>', self.subsitute)
        self.button_2.bind('<space>', self.unsubsitute)
        self.textbox.bind('<Control-c>', self.copy)
        self.textbox.bind('<Control-v>', self.paste)
        self.encode_var.trace('w', self.encode_switch_update)
        self.update_substitutions()

    def encode_switch_update(self, var, index, mode):
        self.update_vars[0] = self.encode_var.get()
        self.update_substitutions()
        self.input_1.configure(state='normal')
        self.update_output(self)

    def get_keyword(self):
        dialog = ctk.CTkInputDialog(master=None, text=self.texts['keyword'] + ':',
                                              title=self.texts['keyword'])
        keyword = dialog.get_input()
        keyword = ''.join(list({x.lower(): None for x in keyword if x.lower() in self.constants.alphabet}))
        
        key_index = 0
        value_index = 0
        self.substitutions = {}
        while key_index < len(self.constants.alphabet):
            value_index = value_index % 26
            
            if value_index < len(keyword):
                self.substitutions[self.constants.alphabet[key_index].upper()] = keyword[value_index]
            else:
                if self.constants.alphabet[value_index] in self.substitutions.values():
                    value_index += 1
                    continue
                else:
                    self.substitutions[self.constants.alphabet[key_index].upper()] = self.constants.alphabet[value_index]

            key_index += 1
            value_index += 1
                    

        self.update_vars[1] = self.substitutions
        self.update_substitutions()
        self.update_output(self)
    
    def tab_order(self, index):
        if index == 0:
            if self.encode_var.get():
                self.button_1.focus()
                self.button_1.configure(fg_color=self.constants.theme['color']['button_hover'][self.constants.mode])
            else:
                self.input_2.focus()
                return
            
        elif index == 1:
            if self.encode_var.get():
                self.input_1.configure(state='normal')
                self.input_1.focus()
                return
            else:
                self.button_1.focus()
                self.button_1.configure(fg_color=self.constants.theme['color']['button_hover'][self.constants.mode])
        
        elif index == 2:
            self.button_2.focus()
            self.button_1.configure(fg_color=self.constants.theme['color']['button'][self.constants.mode])
            self.button_2.configure(fg_color=self.constants.theme['color']['button_hover'][self.constants.mode])
        
        elif index == 3:
            if self.encode_var.get():
                self.input_1.configure(state='disabled')
                self.input_2.focus()
                self.button_2.configure(fg_color=self.constants.theme['color']['button'][self.constants.mode])
                return
            else:
                self.input_1.focus()
                self.button_2.configure(fg_color=self.constants.theme['color']['button'][self.constants.mode])
                return

        return 'break'

    def subsitute(self, event):
        input_1 = self.input_1.get()
        input_2 = self.input_2.get()
            
        if input_1 != input_2:
            if len(input_1) == len(input_2):
                for i, c in enumerate(input_1):
                    self.substitutions[c] = input_2[i]
            elif input_2 == '':
                for i, c in enumerate(input_1):
                    self.substitutions[c] = ''
                
        self.update_vars[1] = self.substitutions
        self.update_substitutions()
        self.update_output(self)

    def unsubsitute(self, event):
        input_1 = self.input_1.get()
        input_2 = self.input_2.get()
            
        if input_1 != input_2:
            if len(input_1) == len(input_2):
                for i, c in enumerate(input_1):
                    if c in self.substitutions and input_2[i] in self.substitutions.values():
                        del self.substitutions[c]
            elif input_2 == '':
                for i, c in enumerate(input_1):
                    if c in self.substitutions:
                        del self.substitutions[c]
                    
        self.update_vars[1] = self.substitutions
        self.update_substitutions()
        self.update_output(self)

    def copy(self, event):
        value = base64.b64encode(pickle.dumps(self.substitutions))
        self.frame.master.clipboard_clear()
        self.frame.master.clipboard_append(value.decode('utf-8'))
        self.frame.master.update()
        
    def paste(self, event):
        try:
            self.substitutions = pickle.loads(base64.b64decode(self.frame.master.clipboard_get()))
            self.update_vars[1] = self.substitutions
            self.update_substitutions()
            self.update_output(self)
        except pickle.UnpicklingError:
            pass
    
    @staticmethod
    def update(text, constants, encode, substitutions):
        if encode:
            substitutions = {v: k for k, v in substitutions.items()}

        result = ''
        for c in text:
            if c in substitutions:
                result += substitutions[c]
            else:
                result += c
        
        return (result, ())

    def update_substitutions(self):
        substitutions = self.substitutions.copy()

        if self.encode_var.get():
            arrow = '<-'
        else:
            arrow = '->'
            
        for letter in self.constants.alphabet:
            if letter.upper() not in substitutions:
                substitutions[letter.upper()] = ''
        substitutions = dict(sorted(substitutions.items(), key=self.substitutions_sort_key))

        formatted = '\n'.join([f'\'{k}\' {arrow} \'{v}\'' for k, v in substitutions.items()])

        self.textbox.configure(state='normal')
        self.textbox.delete(1.0, 'end')
        self.textbox.insert(1.0, formatted)
        self.textbox.configure(state='disabled')
        self.label.configure(text=arrow)

    def substitutions_sort_key(self, element):
        key = element[0]
        if key.lower() in self.constants.alphabet:
            return self.constants.alphabet.index(key.lower())
        else:
            return -1

    def display(self):
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, minsize=15)
        self.frame.columnconfigure(4, minsize=120)
        self.frame.columnconfigure(5, weight=1)
        
        self.input_1.grid(row=0, column=1, rowspan=2, padx=15)
        self.label.grid(row=0, column=2, rowspan=2)
        self.input_2.grid(row=0, column=3, rowspan=2, padx=10)
        self.button_1.grid(row=0, column=4, pady=12, sticky='S')
        self.button_2.grid(row=1, column=4, pady=12, sticky='N')
        self.keyword.grid(row=1, column=1, columnspan=3)
        self.textbox.grid(row=0, column=5, rowspan=2, columnspan=2, pady=120)
        self.scrollbar.grid(row=0, column=6, rowspan=2, pady=120, sticky='E')
        self.encode_switch.grid(row=1, column=6, padx=15, pady=15, sticky='SE')

        self.button_1.configure(fg_color=self.constants.theme['color']['button'][self.constants.mode])
        self.button_2.configure(fg_color=self.constants.theme['color']['button'][self.constants.mode])

class Affine(Stage):
    def __init__(self, update_output):
        super().__init__(update_output)
        self.encode_var = tk.IntVar(value=0)
        self.alpha_var = tk.IntVar(value=0)
        self.beta_var = tk.IntVar(value=0)
        self.update_vars.extend([0, 0, 0])

    def setup(self, frame, constants):
        super().setup(self, frame, constants)
        self.encode_switch = ctk.CTkSwitch(frame, text=self.texts['encode'], onvalue=1, offvalue=0,
                                           variable=self.encode_var)
        self.alpha_label = ctk.CTkLabel(frame)
        self.beta_label = ctk.CTkLabel(frame)
        self.alpha_slider = ctk.CTkSlider(frame, from_=0, to=11, number_of_steps=11, width=375,
                                          variable=self.alpha_var)
        self.beta_slider = ctk.CTkSlider(frame, from_=0, to=25, number_of_steps=25, width=375,
                                         variable=self.beta_var)
        self.alpha_var.trace('w', self.input_update)
        self.beta_var.trace('w', self.input_update)
        self.encode_var.trace('w', self.input_update)
        self.input_update(str(self.alpha_var), False, False, update=False)
        self.input_update(str(self.beta_var), False, False, update=False)
   
    def input_update(self, var, index, mode, update=True):
        if var == str(self.alpha_var):
            self.update_vars[1] = list(self.constants.inverses.keys())[self.alpha_var.get()]
            self.alpha_label.configure(text=self.texts['alpha_label'] + ' ' + str(self.update_vars[1]))
        elif var == str(self.beta_var):
            self.update_vars[2] = self.beta_var.get()
            self.beta_label.configure(text=self.texts['beta_label'] + ' ' + str(self.update_vars[2]))
        else:
            self.update_vars[0] = self.encode_var.get()

        if update:
            self.update_output(self)

    @staticmethod
    def update(text, constants, encode, alpha, beta):
        shifted = ''
        for letter in text:
            if letter.lower() in constants.alphabet:
                if encode:
                    print(constants.alphabet.index(letter.lower()))
                    print(alpha, beta)
                    index = (constants.alphabet.index(letter.lower()) * alpha + beta) % 26
                    print(index)
                else:
                    index = ((constants.alphabet.index(letter.lower()) - beta) * constants.inverses[alpha]) % 26
                shifted_letter = constants.alphabet[index]
                if letter.isupper():
                    shifted_letter = shifted_letter.upper()
                shifted += shifted_letter
            else:
                shifted += letter
        
        return (shifted, ())

    def display(self):
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.alpha_label.grid(row=0, column=0, sticky='S')
        self.alpha_slider.grid(row=1, column=0, pady=10)
        self.beta_label.grid(row=2, column=0, pady=10)
        self.beta_slider.grid(row=3, column=0, sticky='N')
        self.encode_switch.grid(row=4, column=0, padx=15, pady=15, sticky='SE')

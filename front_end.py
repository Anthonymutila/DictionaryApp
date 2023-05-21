import json
import tkinter as tk
from tkinter import messagebox
from difflib import get_close_matches as g
from tkinter import font


data = json.load(open('data.json'))
keys = sorted(data.keys())



def wordSeacher():
    #...............Handle the display word defination...............

    getValue = serach_var.get()
    getValue = getValue.upper()
    
    if getValue in data:
        for i, j in enumerate(data[getValue]):
            wordDefination.insert('end', str(i) + ' ' + j + '\n')
      

    #...............Handles the Error messages...............
    else:
        list = g(getValue, keys, n=3, cutoff=0.7)
        if len(list) == 0:
            wordDefination.insert('end', "Unfortunatly no word found!")
        else:
            wordSuggestion = list[0]
            answer = messagebox.askquestion(title="Suggested Word",
                                            message="Is your word " + wordSuggestion + "?")
            if answer == "yes":
                for i, j in enumerate(data[wordSuggestion]):
                    wordDefination.insert('end', str(i) + ' ' + j + '\n')

            else:
                wordDefination.insert('end', "Word does not exist")


#...............Clears the screen..............

def clear_button():
    wordDefination.delete(1.0, 'end')
    word_to_be_searched.delete(0, 'end')

#........Update_search listbox.....................


def update_Listbox(*args):
    wordListBox.delete(0, 'end')
    search_term = serach_var.get()
    for item in keys:
        if search_term.lower() in item.lower():
            wordListBox.insert('end', item)

#........Selects keys from the listbox and display the value....................


def select_word(event):
    index = wordListBox.curselection()  # gets the index of the selection
    getValue = wordListBox.get(index)
    if getValue in data:
        for i, j in enumerate(data[getValue]):
            wordDefination.insert('end', str(i) + ' ' + j + '\n')
            
    if getValue not in data:
        print('no data here come next time')



#........Constructon of  widgets ...................
#.....................................................


root = tk.Tk()
root.resizable(False,False)

root.configure(background="white")
head = 'Pocket Dictionary'
root.title(head)
big_header_Font = font.Font(family='Verdana', size=16, weight='normal',slant='italic')
listbox_Font = font.Font(family='Helvetica', size=12, weight='normal')
text_Font = font.Font(family='Courier New', size=12, weight='normal')
wordlist_Font = font.Font(family='Verdana', size=12, weight='normal')
label_Font = font.Font(family='Verdana', size=10, weight='normal')



# Define widget Frames
big_header = tk.Frame(root, borderwidth=5, relief='flat', width=65,bg='#b8b894',height=10)
big_header_label =tk.Label(big_header,text='SmartPocket Dictionary',font=big_header_Font)
entryFrame = tk.Frame(root, borderwidth=2, relief='flat', width=50,bg='#b8b894')
clear_button_frame=tk.Frame(root)

listbox_border = tk.Frame(root, bd=0, relief="sunken")#bg='#999966')

text_border_Frame = tk.Frame(root, bd=0, relief="sunken",bg='#b8b894')
# wordName = tk.Label(entryFrame, text='Search word',font=label_Font)

# State Variables
serach_var = tk.StringVar()

serach_var.trace('w', update_Listbox)

wordList = tk.Label(entryFrame, text='WordList', width=27,font=wordlist_Font)#bg='#b8b894')

word_to_be_searched = tk.Entry(entryFrame, width=74, textvariable=serach_var,font=listbox_Font)
word_to_be_searched.focus()
wordDefination = tk.Text(text_border_Frame, width=70, height=20,
                          wrap='word',borderwidth=0,highlightthickness=0,font=text_Font,background=text_border_Frame.cget("background"),)


findButton = tk.Button(entryFrame, text='Search', command=wordSeacher,font=label_Font)
wordListBox = tk.Listbox(listbox_border,borderwidth=0,highlightthickness=0, width=30, height=20,
 selectmode='single',font=listbox_Font, background=listbox_border.cget("background"),)
# bg='#999966',

update_Listbox()
scrollbar = tk.Scrollbar(listbox_border)
wordListBox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=wordListBox.yview)
clear_screen = tk.Button(root,text ='Clear Screen',command=clear_button,font=label_Font)


# Pack widgets here

big_header.pack(pady=(0,25))
big_header_label.pack()
clear_screen.pack(side = 'right',anchor='s', ipadx=5,ipady=8,)
entryFrame.pack(side='top',anchor='nw',padx=(10,10))


listbox_border.pack(side='left',padx=10, pady=10, fill=None, expand=False)

text_border_Frame.pack(side='right',padx=(11,10))




wordList.pack(side='left',pady=4,padx=(7,12))
word_to_be_searched.pack(side='left', ipady=4, padx=5)

findButton.pack(side='right', ipady=5,ipadx=8)
wordDefination.pack(side='right',padx=10,pady=10)
wordListBox.pack(side='left',padx=11,pady=11, fill="both", expand=True)
scrollbar.pack(side='right', fill='y')
# wordListBox.bind('<Double-1>',handler)
wordListBox.bind('<<ListboxSelect>>', select_word)
word_to_be_searched.bind("<Return>", lambda X: wordSeacher())


root.mainloop()

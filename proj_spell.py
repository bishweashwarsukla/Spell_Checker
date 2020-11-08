import re
from collections import Counter
import tkinter as tk  #here, tkinter library is imported for basic gui
from tkinter import ttk # ttk module is imported for some functions
from tkinter import * #import all 
 
root = tk.Tk() #root is object of class Tk
root.title('Spell Checker')	#title of the app
root.configure(bg = 'black') #background window color
 
def words(text): 
    return re.findall(r'\w+', text.lower()) #converting all texts to lower cases
 
WORDS = Counter(words(open('words.txt').read()))
 
def suggestions(nn): 
    #"Generate possible spelling correcteds for word."
    return (known([nn]) or known(edit_distance1(nn)) or known(edit_distance2(nn)) or [nn])
 
def known(nn): 
    #"The subset of 'words' that appear in the dictionary of WORDS."
    return set(o for o in nn if o in WORDS)
 
def edit_distance1(nn):
    #"All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(nn[:i], nn[i:])    for i in range(len(nn) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
 
def edit_distance2(nn): 
    #"All edits that are two edits away from `word`."
    return (e2 for e1 in edit_distance1(nn) for e2 in edit_distance1(e1))
 
def probability(nn, N=sum(WORDS.values())): 
    #"Probability of 'word'."
    return WORDS[nn] / N
 
 
 
textx=[]#empty list to store words of query
def corrected(word): 
    #returns correct word
    for mm in word:
        textx.append(max(suggestions(mm), key=probability)) 
 
name_var=tk.StringVar() #variable to store query
name_entrybox=ttk.Entry(root,width=25,textvariable=name_var,font=(name_var,23),foreground='black') #box to show our query 
name_entrybox.grid(row=0,column=2) #positioning of box
# name_label.config(font=("Enter your query", 30)) 
name_entrybox.focus() 
 
name_label=ttk.Label(root,text='Enter your query',foreground='red',background='blue') #default query asking statement
name_label.grid(row=1,column=2) #positioning
name_label.config(font=("Enter your query", 25)) #for the font size
 
 
def action():
    user_query=name_var.get() #taking query input from user
    user_query=user_query.lower()
 
    punc = '''-!()[]{};:'"\,<>./?@#$%^&*_~'''
    #the below is written for tokenization
    for ele in user_query:  #for replacing punctuation with spaces
        if ele in punc:  
            user_query = user_query.replace(ele, " ")
 
    word = user_query.split()  #tokenized words
    corrected(word)
 
    s=' ' 
    textx[0]=textx[0].capitalize() #Converting first letter of first word to upper case
    s=s.join(textx)
 
    textx.clear()
 
    global result_label
    result_label=tk.Label(root,text=s,foreground='red',background='blue')#output statement
    result_label.grid(row=6,columnspan=3) #positioning result statement 
    result_label.configure(font=(s,25))
    submit_button['state']=DISABLED
 
    name_entrybox.delete(0,tk.END)
 
def mydelete(): #to delete previous input query after showing its result
    result_label.grid_forget()
    submit_button['state']=NORMAL
 
 
submit_button=tk.Button(root,text='Submit',command=action) #submit button 
submit_button.grid(row=4,columnspan=3)
submit_button.configure(width=15)
 
delete_button=tk.Button(root,text='Delete',command=mydelete) #delete button
delete_button.grid(row=5,columnspan=3)
delete_button.configure(width=15)
 
 
root.mainloop()
 

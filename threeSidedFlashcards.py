import tkinter as tk
from tkinter import simpledialog, messagebox, DISABLED, NORMAL, BOTTOM
from tkinter import *
import json
import random

# initializing dictionaries
pinyin = {}
meaning = {}
character = {}

def save():
    data = {
        "pinyin": pinyin, # assign data in file with data in dictionary
        "meaning": meaning,
        "character": character
    }
    with open('threeSidedFlashcards.json', 'w') as file:
        json.dump(data, file, indent=6)

def load():
    global pinyin, meaning, character
    try:
        with open('threeSidedFlashcards.json', 'r') as file:
            data = json.load(file)
            pinyin = data["pinyin"] # assign dictionaries with data in file
            meaning = data["meaning"]
            character = data["character"]
    except FileNotFoundError: # when no files are found, dictionaries are initialized as empty
        pinyin = {}
        meaning = {}
        character = {}

# -------------------------START OF CREATE()-------------------------

def create():
    global createWindow, setNameEntry, setNameText, createFlashcardSetButton
    root.withdraw()
    createWindow = Toplevel(root)
    createWindow.title("Create")
    createWindow.geometry(f"700x450+{root.winfo_x()}+{root.winfo_y()}") # maintain new window in same place where root was

    setNameText = Label(createWindow, text = "Flashcard set title:",font=("Helvetica",25))
    setNameText.pack(pady=(20,7))

    setNameEntry = Entry(createWindow, width=35, font=('Helvetica',20)) # space to input title
    setNameEntry.pack(pady=7)

    createFlashcardSetButton = Button(createWindow, text = "Create flashcard set", command = createFlashcardSet)
    createFlashcardSetButton.pack(pady=7) # button calls the "next step" (function)

    homeCreate()

# setting up window to add flashcards
def createFlashcardSet():
    global pinyinEntry, meaningEntry, characterEntry
    setName = setNameEntry.get()

    duplicateName = False

    existingNames = list(pinyin.keys())
    for i in range(len(existingNames)):
        if setName == existingNames[i]:
            duplicateName = True

    if duplicateName:
        createFlashcardSetButton.destroy()
        duplicateNameText = Label(createWindow, text="Flashcard set with this name already exists, try a different name")
        duplicateNameText.pack()
        duplicateNameButton = Button(createWindow, text="Ok", command=lambda: [createWindow.destroy(), create()]) 
        duplicateNameButton.pack()
    else:
        setNameText.destroy()
        setNameEntry.destroy()
        createFlashcardSetButton.destroy()

        pinyin[setName] = {} # initialize dictionaries with input flashcard set name
        meaning[setName] = {}
        character[setName] = {}

        creatingFlashcardSetText = Label(createWindow, text="Creating flashcards for: "+setName, font=("Helvetica", 25), wraplength=525)
        creatingFlashcardSetText.pack(pady=(20,0))
        creatingFlashcardSetInstructions = Label(createWindow, text="Fill in the corresponding fields and click 'Add flashcard' to save a flashcard, once you are done adding all the flashcards you need, click 'Done'", wraplength=400)
        creatingFlashcardSetInstructions.pack(pady=20, padx=7) # text to explain how to create flashcards

        pinyinText = Label(createWindow, text="Pinyin:") 
        pinyinText.pack()

        pinyinEntry = Entry(createWindow, width=40) # individual entry boxes for pinyin, meaning and character
        pinyinEntry.pack()

        meaningText = Label(createWindow, text="Meaning:")
        meaningText.pack()

        meaningEntry = Entry(createWindow, width=40)
        meaningEntry.pack()

        characterText = Label(createWindow, text="Character:")
        characterText.pack()

        characterEntry = Entry(createWindow, width=40)
        characterEntry.pack()

        addFlashcardButton = Button(createWindow, text = "Add flashcard", command = lambda: addFlashcard(setName)) 
        # add flashcard when the fields are filled
        addFlashcardButton.pack(pady=7)

        homeButton = Button(createWindow, text="Done", command=lambda: [createWindow.destroy(), root.deiconify()]) 
        # finish making flashcards and return to menu
        homeButton.pack(pady=7)

# add flashcards to the set
def addFlashcard(setName):
    pinyinWord = pinyinEntry.get()
    meaningWord = meaningEntry.get()
    characterWord = characterEntry.get()

    i = len(pinyin[setName])
    pinyin[setName][i] = pinyinWord
    meaning[setName][i] = meaningWord
    character[setName][i] = characterWord
    save()
    pinyinEntry.delete(0, END)
    meaningEntry.delete(0, END)
    characterEntry.delete(0, END)

def homeCreate():
    global createWindow
    homeButton = Button(createWindow, text="Home", command=lambda: [createWindow.destroy(), root.deiconify()])
    homeButton.place(x=10, y=35, anchor="sw") # home button always displayed so user can return home anytime

# -------------------------END OF CREATE()-------------------------

# -------------------------START OF PRACTICE()-------------------------
def practice():
    global allFlashcardButtons, practiceWindow, selectFlashcardSetText, noFlashcardText

    root.withdraw()
    practiceWindow = Toplevel(root)
    practiceWindow.title("Practice")
    practiceWindow.geometry(f"700x450+{root.winfo_x()}+{root.winfo_y()}")

    allFlashcardButtons = []

    selectFlashcardSetText = Label(practiceWindow, text="Select the flashcard set you want to practice", font=("Helvetica",20), wraplength=525)
    selectFlashcardSetText.pack(pady=(20,7))

    noFlashcardText = Label(practiceWindow, text="If you see a blank screen, it means that no flashcards have been created", wraplength="450")
    noFlashcardText.pack(pady=(0,7))

    for i in range(len(pinyin)):
        keys_list = list(pinyin.keys())
        title = keys_list[i]
        flashcardButtons = Button(practiceWindow, text=title, command=lambda t=title: practiceFlashcardSet(t)) 
        flashcardButtons.pack(pady=7)
        allFlashcardButtons.append(flashcardButtons)

    homePractice()

# preparing screen for user to customize their practice settings
def practiceFlashcardSet(title):
    global selectedFlashcardSet, pinyinQuestion, meaningQuestion, characterQuestion, pinyinAnswer, meaningAnswer, characterAnswer, practicingFlashcardSetInstructionsText, questionFrame, answerFrame, confirmPractice, resetTypesButton
    selectedFlashcardSet=title

    selectFlashcardSetText.destroy()
    noFlashcardText.destroy()

    for i in range(len(allFlashcardButtons)):
        allFlashcardButtons[i].destroy()

    practicingFlashcardSetText = Label(practiceWindow, text="Practicing flashcards for: "+selectedFlashcardSet, font=("Helvetica", 25), wraplength=525)
    practicingFlashcardSetText.pack(pady=(20,7))
    practicingFlashcardSetInstructionsText = Label(practiceWindow, text="Choose which component you want as the question type and as the answer type", wraplength=400)
    practicingFlashcardSetInstructionsText.pack(pady=(0,7), padx=7)

    questionFrame = Frame(practiceWindow)
    questionFrame.pack(side=LEFT, fill=Y, padx=(120,20)) # defining position and padding of widget

    # questionFrame is called instead of practiceWindow
    questionText = Label(questionFrame, text="Question type:")
    questionText.pack()

    # placing buttons in a column
    pinyinQuestion = Button(questionFrame, text="Pinyin", width=15, command=lambda: selectingQuestionType("Pinyin"))
    pinyinQuestion.pack(pady=5) 

    meaningQuestion = Button(questionFrame, text="Meaning", width=15, command=lambda: selectingQuestionType("Meaning"))
    meaningQuestion.pack(pady=5)

    characterQuestion = Button(questionFrame, text="Character", width=15, command=lambda: selectingQuestionType("Character"))
    characterQuestion.pack(pady=5)

    answerFrame = Frame(practiceWindow)
    answerFrame.pack(side=RIGHT,fill=Y, padx=(20,120))

    answerText = Label(answerFrame, text="Answer type:")
    answerText.pack()

    pinyinAnswer = Button(answerFrame, text="Pinyin", width=15, command=lambda: selectingAnswerType("Pinyin"),state=DISABLED)
    pinyinAnswer.pack(pady=5)

    meaningAnswer = Button(answerFrame, text="Meaning", width=15, command=lambda: selectingAnswerType("Meaning"),state=DISABLED)
    meaningAnswer.pack(pady=5)

    characterAnswer = Button(answerFrame, text="Character", width=15, command=lambda: selectingAnswerType("Character"),state=DISABLED)
    characterAnswer.pack(pady=5)

    resetTypesButton = Button(practiceWindow, text="Reset", width=50, command=cancelTypeSelection)
    resetTypesButton.pack(side=BOTTOM, pady=(5,50))
    confirmPractice = Button(practiceWindow, text="Confirm", width=50, command=prepareQuestions, state=DISABLED)
    confirmPractice.pack(side=BOTTOM, pady=(5))

def selectingQuestionType(type):
    global selectedQuestionType
    selectedQuestionType = type # type is input through lambda function when button is pressed

    if selectedQuestionType == "Pinyin":
        pinyinQuestion.config(highlightbackground="#a3ddfc") # add colour to button that was clicked
    elif selectedQuestionType == "Meaning":
        meaningQuestion.config(highlightbackground="#a3ddfc")
    elif selectedQuestionType == "Character":
        characterQuestion.config(highlightbackground="#a3ddfc")

    if selectedQuestionType == "Pinyin":
        meaningAnswer.config(state=NORMAL) # enable buttons that are not of the same types
        characterAnswer.config(state=NORMAL)
    elif selectedQuestionType == "Meaning":
        pinyinAnswer.config(state=NORMAL)
        characterAnswer.config(state=NORMAL)
    elif selectedQuestionType == "Character":
        meaningAnswer.config(state=NORMAL)
        pinyinAnswer.config(state=NORMAL)

def selectingAnswerType(type):
    global selectedAnswerType
    selectedAnswerType = type

    if selectedAnswerType == "Pinyin":
        pinyinAnswer.config(highlightbackground="#a3ddfc")
    elif selectedAnswerType == "Meaning":
        meaningAnswer.config(highlightbackground="#a3ddfc")
    elif selectedAnswerType == "Character":
        characterAnswer.config(highlightbackground="#a3ddfc")

    confirmPractice.config(state=NORMAL)
    confirmPractice.config(highlightbackground="#a3ddfc")

# reset button if user wants to change their selection for questionType and answerType
def cancelTypeSelection():
    pinyinAnswer.config(state=DISABLED)
    meaningAnswer.config(state=DISABLED)
    characterAnswer.config(state=DISABLED)
    confirmPractice.config(state=DISABLED)
    confirmPractice.config(bg="SystemButtonFace")

    pinyinQuestion.config(bg="SystemButtonFace")
    meaningQuestion.config(bg="SystemButtonFace")
    characterQuestion.config(bg="SystemButtonFace")

    pinyinAnswer.config(bg="SystemButtonFace")
    meaningAnswer.config(bg="SystemButtonFace")
    characterAnswer.config(bg="SystemButtonFace")

# calling the dictionaries of flashcards that are going to be used
def prepareQuestions():
    global answerEntry, questions, answers, points, submit, question, questionsAnswered, randomQuestion, i
    questions = globals()[selectedQuestionType.lower()][selectedFlashcardSet] # dictionary of specific component and flashcard set is called
    answers = globals()[selectedAnswerType.lower()][selectedFlashcardSet]

    practicingFlashcardSetInstructionsText.destroy()
    questionFrame.destroy()
    answerFrame.destroy()
    confirmPractice.destroy()
    resetTypesButton.destroy()

    points = 0
    questionsAnswered = 0

    randomQuestion = list(questions.keys())
    random.shuffle(randomQuestion) # randomizing list
    i=0

    getQuestion()

# output questions one by one
def getQuestion():
    global questionsAnswered, answerType, answerEntry, submit, question, points, i
    questionsAnswered += 1
    questionType = selectedQuestionType+": "+questions[randomQuestion[i]] #randomQuestion[i] used as a key to call value in dictionary
    question = Label(practiceWindow, text=questionType, font=("Helvetica",20))
    question.pack(pady=25)

    answerType = Label(practiceWindow, text=selectedAnswerType+":", font=("Helvetica",20))
    answerType.pack(pady=7)
    answerEntry = Entry(practiceWindow, width=35, font=('Helvetica',20))
    answerEntry.pack()

    submit = Button(practiceWindow, text="Submit", command=lambda: checkAnswer(answers[randomQuestion[i]]))
    submit.pack(pady=7)

def checkAnswer(correctAnswer):
    global correctText, incorrectText, status, next, points
    submittedAnswer = answerEntry.get() # store input answer
    answerEntry.config(state=DISABLED) # user cannot modify answers after submitting an answer
    if submittedAnswer.lower() == correctAnswer.lower(): # avoids case sensitivity 
        correctText = Label(practiceWindow, text="Correct!", font=("Helvetica", 15)) # message when correct
        correctText.pack(pady=7)
        status = "correct"
        points += 1
    else:
        incorrectText = Label(practiceWindow, text="Incorrect, the correct answer is: "+correctAnswer, font=("Helvetica", 15))
        incorrectText.pack(pady=7) # message when incorrect
        status = "incorrect"

    submit.destroy()
    next = Button(practiceWindow, text="Next", command=nextQuestion)
    next.pack(pady=7)

# outputs next question until all questions are asked and calculate grade
def nextQuestion():
    global points, i
    question.destroy()
    answerType.destroy()
    answerEntry.destroy()
    next.destroy()
    i += 1
    if status == "correct":
        correctText.destroy()
    else:
        incorrectText.destroy()

    if questionsAnswered < len(questions):
        getQuestion()
    else: 
        grade = int((points * 100) / len(randomQuestion))
        gradeText = Label(practiceWindow, text="Your grade is "+str(grade)+"%", font=("Helvetica",20))
        gradeText.pack(pady=20)
        homeButton = Button(practiceWindow, text="Done", command=lambda: [practiceWindow.destroy(), root.deiconify()])
        homeButton.pack(pady=7)

def homePractice():
    global praticeWindow
    homeButton = Button(practiceWindow, text="Home", command=lambda: [practiceWindow.destroy(), root.deiconify()])
    homeButton.place(x=10, y=35, anchor="sw")

# -------------------------END OF PRACTICE()-------------------------

# -------------------------START OF EDIT()-------------------------

def edit():
    global allFlashcardButtons, editWindow, editSelectFlashcardSetText, title, noFlashcardText

    load()

    root.withdraw()
    editWindow = Toplevel(root)
    editWindow.title("Edit")
    editWindow.geometry(f"700x450+{root.winfo_x()}+{root.winfo_y()}")

    allFlashcardButtons = []

    editSelectFlashcardSetText = Label(editWindow, text="Select the flashcard set you want to edit", font=("Helvetica",20), wraplength=525)
    editSelectFlashcardSetText.pack(pady=(20,7))

    noFlashcardText = Label(editWindow, text="If you see a blank screen, it means that no flashcards have been created", wraplength="450")
    noFlashcardText.pack(pady=(0,7))

    for i in range(len(pinyin)):
        keys_list = list(pinyin.keys())
        flashcardNames = keys_list[i]
        flashcardButtons = Button(editWindow, text=flashcardNames, command=lambda title=flashcardNames: editFlashcardSet(title)) 
        flashcardButtons.pack(pady=7)
        allFlashcardButtons.append(flashcardButtons)

    homeEdit()

# preparing window by displaying entries with all the data
def editFlashcardSet(title):
    global flashcardSetName, editSelectedFlashcardSet, pinyinEditEntryList, meaningEditEntryList, characterEditEntryList, saveButton, r
    editSelectedFlashcardSet = title

    editSelectFlashcardSetText.destroy()
    noFlashcardText.destroy()
    for i in range(len(allFlashcardButtons)):
        allFlashcardButtons[i].destroy()

    flashcardSetNameLabel = Label(editWindow, text="Title: ")
    flashcardSetNameLabel.grid(row=0, column=0, pady=20, padx=(60,0))

    flashcardSetName = Entry(editWindow)
    flashcardSetName.insert(0,editSelectedFlashcardSet) 
    flashcardSetName.grid(row=0, column=1, columnspan=2, sticky="ew")

    pinyinLabel = Label(editWindow, text="Pinyin: ")
    pinyinLabel.grid(row=1, column=0, padx=(60,0))

    pinyinEditEntryList = []
    r = 2 #

    # output rows of entry boxes dynamically depending on how many flashcards are in a set
    for i in range(len(pinyin[editSelectedFlashcardSet])): 
        pinyinWords = pinyin[editSelectedFlashcardSet][str(i)]

        pinyinEditEntry = Entry(editWindow)
        pinyinEditEntry.insert(0,pinyinWords) # filling entries with stored data 
        pinyinEditEntry.grid(row=r, column=0, padx=(60,0))
        pinyinEditEntryList.append(pinyinEditEntry)

        r += 1 # go to next row

    meaningLabel = Label(editWindow, text="Meaning: ")
    meaningLabel.grid(row=1, column=1)

    meaningEditEntryList = []
    r = 2 #row
    for i in range(len(meaning[editSelectedFlashcardSet])):
        meaningWords = meaning[editSelectedFlashcardSet][str(i)]

        meaningEditEntry = Entry(editWindow)
        meaningEditEntry.insert(0,meaningWords)
        meaningEditEntry.grid(row=r, column=1)
        meaningEditEntryList.append(meaningEditEntry)

        r += 1

    characterLabel = Label(editWindow, text="Character: ")
    characterLabel.grid(row=1, column=2)

    characterEditEntryList = []
    r = 2 #row
    for i in range(len(character[editSelectedFlashcardSet])):
        characterWords = character[editSelectedFlashcardSet][str(i)]

        characterEditEntry = Entry(editWindow)
        characterEditEntry.insert(0,characterWords)
        characterEditEntry.grid(row=r, column=2)
        characterEditEntryList.append(characterEditEntry)

        r += 1

    saveButton = Button(editWindow, text="Save", command=saveEditsAttempt)
    saveButton.grid(row=r,column=1)

# duplicateName is checked first
def saveEditsAttempt():
    global editSelectedFlashcardSet, duplicateNameText

    duplicateName = checkDuplicate()

    if not duplicateName:
        saveEdits()
    else:
        # Destroy or disable the save button to prevent further interaction
        saveButton.destroy()

        # Create or update the label to notify the user of the duplicate
        duplicateNameText = Label(editWindow, text="Flashcard set with this name already exists, try a different name")
        duplicateNameText.grid(row=r, column=0, columnspan=3, sticky="ew", padx=(60,0))

        # Create the "Ok" button to recheck the name
        duplicateNameButton = Button(editWindow, text="Ok", command=handleDuplicateCheck)
        duplicateNameButton.grid(row=r+1, column=1)

# called when duplicateName is false
def saveEdits():
    global editSelectedFlashcardSet

    # arrays to store the entries
    editedPinyinList = []
    for i in range(len(pinyin[editSelectedFlashcardSet])):
        editedPinyinWord = pinyinEditEntryList[i].get()
        editedPinyinList.append(editedPinyinWord)

    editedMeaningList = []
    for i in range(len(meaning[editSelectedFlashcardSet])):
        editedMeaningWord = meaningEditEntryList[i].get()
        editedMeaningList.append(editedMeaningWord)

    editedCharacterList = []
    for i in range(len(character[editSelectedFlashcardSet])):
        editedCharacterWord = characterEditEntryList[i].get()
        editedCharacterList.append(editedCharacterWord)

    if newName == editSelectedFlashcardSet:
        # replacing old data with new data
        for i in range(len(pinyin[editSelectedFlashcardSet])):
            pinyin[editSelectedFlashcardSet][str(i)] = editedPinyinList[i]
            meaning[editSelectedFlashcardSet][str(i)] = editedMeaningList[i]
            character[editSelectedFlashcardSet][str(i)] = editedCharacterList[i]
        saveButton.destroy()
        editSuccessText = Label(editWindow, text="Flashcard set edited successfully")
        editSuccessText.grid(row=r+2, column=0, columnspan=3, sticky="ew", padx=(60,0))
        homeButton = Button(editWindow, text="Done", command=lambda: [editWindow.destroy(), root.deiconify()])
        homeButton.grid(row=r+3, column=1)
    else:
        pinyin[newName] = {}
        meaning[newName] = {}
        character[newName] = {}
        for i in range(len(pinyin[editSelectedFlashcardSet])):
            pinyin[newName][str(i)] = editedPinyinList[i]
            meaning[newName][str(i)] = editedMeaningList[i]
            character[newName][str(i)] = editedCharacterList[i]

        del pinyin[editSelectedFlashcardSet]
        del meaning[editSelectedFlashcardSet]
        del character[editSelectedFlashcardSet]

        saveButton.destroy()
        editSuccessText = Label(editWindow, text="Flashcard set edited successfully")
        editSuccessText.grid(row=r+2,column=1,padx=(60,0))
        homeButton = Button(editWindow, text="Done", command=lambda: [editWindow.destroy(), root.deiconify()]) 
        homeButton.grid(row=r+3,column=1)   
    save() 

# notifying user about duplicate
def handleDuplicateCheck():
    duplicateName = checkDuplicate() # search names in dictionary for duplicates

    if duplicateName: # notify user that it is a duplicate name
        duplicateNameText.config(text="Flashcard set with this name already exists, try a different name")
    else: 
        saveEdits()

# check if new input is still a duplicate or not
def checkDuplicate(): # search names in dictionary for duplicates
    global newName
    newName = flashcardSetName.get()
    duplicateName = False

    if newName in pinyin and newName != editSelectedFlashcardSet:
        duplicateName = True

    return duplicateName

def homeEdit():
    global editWindow, homeButton
    homeButton = Button(editWindow, text="Home", command=lambda: [editWindow.destroy(), root.deiconify()])
    homeButton.place(x=10, y=35, anchor="sw")

# -------------------------END OF EDIT()-------------------------
# -------------------------START OF DELETE()-------------------------

def delete():
    global deleteWindow, deleteSelectFlashcardSetText, allFlashcardButtons, noFlashcardText
    root.withdraw()
    deleteWindow = Toplevel(root)
    deleteWindow.title("Delete")
    deleteWindow.geometry(f"700x450+{root.winfo_x()}+{root.winfo_y()}")

    allFlashcardButtons = []

    deleteSelectFlashcardSetText = Label(deleteWindow, text="Select the flashcard set you want to delete", font=("Helvetica",20), wraplength=525)
    deleteSelectFlashcardSetText.pack(pady=(20,7))

    noFlashcardText = Label(deleteWindow, text="If you see a blank screen, it means that no flashcards have been created", wraplength="450")
    noFlashcardText.pack(pady=(0,7))

    for i in range(len(pinyin)):
        keys_list = list(pinyin.keys())
        title = keys_list[i]
        flashcardButtons = Button(deleteWindow, text=title, command=lambda deleteT=title: deleteSelectingFlashcardSet(deleteT)) 
        flashcardButtons.pack(pady=7)
        allFlashcardButtons.append(flashcardButtons)

    homeDelete()

    save()

# displaying contents of flashcards and ask for confirmation
def deleteSelectingFlashcardSet(deleteT):
    global cancelDeletionButton, confirmDeletionButton, confirmDeletionText
    deleteSelectFlashcardSetText.destroy()
    noFlashcardText.destroy()

    for i in range(len(allFlashcardButtons)):
        allFlashcardButtons[i].destroy()
    deleteFlashcardSet = deleteT

    deleteFlashcardSetText = Label(deleteWindow, text="Deleting: "+deleteFlashcardSet, font=("Helvetica",20), wraplength=525)
    deleteFlashcardSetText.pack(pady=(20,7))

    listPinyin = list(pinyin[deleteFlashcardSet].values())
    pinyinText = ", ".join(listPinyin)
    pinyinInFlashcards = Label(deleteWindow, text="Pinyin: "+pinyinText, wraplength=450)
    pinyinInFlashcards.pack()

    listMeaning = list(meaning[deleteFlashcardSet].values())
    meaningText = ", ".join(listMeaning)
    meaningInFlashcards = Label(deleteWindow, text="Meaning: "+meaningText, wraplength=450)
    meaningInFlashcards.pack()

    listCharacter = list(character[deleteFlashcardSet].values())
    characterText = ", ".join(listCharacter)
    characterInFlashcards = Label(deleteWindow, text="Character: "+characterText, wraplength=450)
    characterInFlashcards.pack()

    confirmDeletionText = Label(deleteWindow, text="Are you sure you want to delete this flashcard set? You cannot undo this action.")
    confirmDeletionText.pack(pady=(20,5))

    confirmDeletionButton = Button(deleteWindow, text="Yes", command=lambda: confirmDeletion(deleteFlashcardSet))
    confirmDeletionButton.pack(pady=7)
    cancelDeletionButton = Button(deleteWindow, text="No", command=lambda: [deleteWindow.destroy(), root.deiconify()])
    cancelDeletionButton.pack()

# called to delete dictionaries
def confirmDeletion(deleteFlashcardSet):  
    del pinyin[deleteFlashcardSet]
    del meaning[deleteFlashcardSet]
    del character[deleteFlashcardSet]
    save() # update json file

    cancelDeletionButton.destroy()
    confirmDeletionText.destroy()
    confirmDeletionButton.destroy()

    deletedText = Label(deleteWindow, text="The flashcard set has been deleted")
    deletedText.pack(pady=7)

    homeButton = Button(deleteWindow, text="Ok", command=lambda: [deleteWindow.destroy(), root.deiconify()])
    homeButton.pack()

def homeDelete():
    global deleteWindow
    homeButton = Button(deleteWindow, text="Home", command=lambda: [deleteWindow.destroy(), root.deiconify()])
    homeButton.place(x=10, y=35, anchor="sw")

# -------------------------END OF DELETE()-------------------------

def menu():
    homeText = tk.Label(root, text = "Three Sided Flashcards App", font=("Helvetica", 25))
    homeText.pack(pady=(20,7))
    optionsText = tk.Label(root, text = "Welcome! Choose one of the options below.", font="Helvetica")
    optionsText.pack(pady=(0,7))
    practice_button = Button(root, text="Practice flashcard set", width = 25, command=practice)
    create_button = Button(root, text="Create new flashcard set", width = 25, command=create)
    edit_button = Button(root, text="Edit flashcard set", width = 25, command=edit)
    delete_button = Button(root, text="Delete flashcard set", width = 25, command=delete)

    practice_button.pack(pady=7)
    create_button.pack(pady=7)
    edit_button.pack(pady=7)
    delete_button.pack(pady=7)

if __name__ == "__main__":
    load()
    root = tk.Tk() # declaring window called root
    root.title("Three Sided Flashcards App")
    root.geometry("700x450") 
    menu() # function that displays buttons for the four main features
    root.mainloop() # loop events so program keeps running during runtime
import tkinter as tk
import tkinter.filedialog
import re
from google.cloud import translate_v2 as translate
from Hook import Hook

tk.FRONT = '1.0'

def cancelCRLF(text):
    return ' '.join(text.splitlines())

def translation(text):
    translate_client = translate.Client.from_service_account_json(apiKeyJson)
    target = 'zh-TW' # 翻譯為中文
    translation = translate_client.translate(text, target_language=target)
    return translation['translatedText']

def replaceText(text):
    for element in replaceMap:
        regex = element['regexEntry'].get()
        replaceWith = element['replaceWithEntry'].get()
        if regex == '':
            break
        text = re.sub(regex, replaceWith, text)
    return text
    
def copyHookCallback(copiedText):
    # 去除換行
    noCRLF = cancelCRLF(copiedText)
    # 翻譯成中文
    translated = translation(noCRLF)
    # 替換特定文字
    replaced = replaceText(translated)
    
    translatedText.delete(tk.FRONT, tk.END)
    translatedText.insert(tk.END, replaced)
    return replaced

h = Hook()

def startCopyHookButtonClick():
    now = btnText.get()
    if now == "開始":
        h.copyHook(copyHookCallback)
        btnText.set("結束")
    else:
        h.stop()
        btnText.set("開始")

def loadAPIKeyJson():
    global apiKeyJson
    apiKeyJson = tk.filedialog.askopenfilename()
    apiKeyPathLabel.config(text=apiKeyJson)
    
def closeWindow():
    h.run = False
    root.destroy()
    
font = ('Comic Sans MS', 30, 'bold')
fontNormal = ('Comic Sans MS', 12, 'bold')

root = tk.Tk()
root.geometry('920x768')
root.title('讀 Paper 懶人器')
frameTopLeft = tk.Frame(root, relief=tk.GROOVE, borderwidth=5, height=100)
frameTopRight = tk.Frame(root, relief=tk.GROOVE, borderwidth=5)
frameBottom = tk.Frame(root, relief=tk.GROOVE, borderwidth=5)

apiKeyJson = ''
loadAPIKeyButton = tk.Button(frameTopLeft, text='載入 API_KEY.json', font=font, command=loadAPIKeyJson)
apiKeyPathLabel = tk.Label(frameTopLeft, text='', wraplength=300, font=fontNormal)

frameTopLeft.grid(row=0, column=0, sticky='news')
loadAPIKeyButton.pack(anchor=tk.W)
apiKeyPathLabel.pack(anchor=tk.W)

regexLabel = tk.Label(frameTopRight, text='Regex', font=font)
replaceWithLabel = tk.Label(frameTopRight, text='Replace With', font=font)
replaceMap = []
for i in range(1, 4):
    element = {}
    element['regexEntry'] = tk.Entry(frameTopRight, width=10, font=font)
    element['replaceWithEntry'] = tk.Entry(frameTopRight, width=10, font=font)
    element['regexEntry'].grid(row=i, column=0)
    element['replaceWithEntry'].grid(row=i, column=1)
    replaceMap.append(element)

frameTopRight.grid(row=0, column=1, sticky='news')
regexLabel.grid(row=0, column=0)
replaceWithLabel.grid(row=0, column=1)

btnText = tk.StringVar()
startCopyHookButton = tk.Button(frameBottom, textvariable=btnText, font=font, command=startCopyHookButtonClick)
btnText.set("開始")

resultLabel = tk.Label(frameBottom, text='翻譯結果', font=font)
translatedText = tk.Text(frameBottom, height=6, font=font)

scroll = tk.Scrollbar(frameBottom)
scroll.config(command=translatedText.yview)
translatedText.config(yscrollcommand=scroll.set)

frameBottom.grid(row=1, column=0, columnspan=2, sticky='news')

scroll.pack(side=tk.RIGHT, fill=tk.Y)
translatedText.pack(anchor=tk.W, side=tk.BOTTOM)
resultLabel.pack(anchor=tk.NW, side=tk.LEFT)
startCopyHookButton.pack(anchor=tk.NW, side=tk.RIGHT)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.protocol("WM_DELETE_WINDOW", closeWindow)
root.mainloop()
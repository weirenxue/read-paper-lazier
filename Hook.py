import pyperclip
import time, threading

class Hook():
    def __init__(self):
        self.run = True
    
    def copyHook(self, callback):
        self.run = True
        self.runHook(lambda : self._copyHook(callback))
        
    def _copyHook(self, callback):
        # 清除剪貼板
        copiedText = ''
        pyperclip.copy(copiedText)
        while self.run:
            # 複製事件是否發生
            tmp_value = pyperclip.paste()
            if tmp_value != copiedText and tmp_value != '':
                # 複製事件發生，對剪貼板中的文字進行處理
                copiedText = callback(tmp_value)
                # 將處理後的文字輸出至剪貼板
                pyperclip.copy(copiedText)
            time.sleep(0.1)
            
    def runHook(self, functionHandle):
        t = threading.Thread(target=functionHandle)
        t.start()
    
    def stop(self):
        self.run = False
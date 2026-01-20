class Action():
    def __init__(self, undo, redo, key = [None]):
        self.undo = undo
        self.redo = redo
        self.key = key
    def redo(self): pass
    def commit(self): redo()
    def undo(self): pass
undoList : list[Action] = []
redoList : list[Action] = []

def lastAction() -> Action :
    if(len(undoList) <= 0): return None
    return undoList[-1]

def addAction(action : Action):
    undoList.append(action)
    redoList = []
    if(len(undoList) > 100):
        undoList.pop(0)

def undo():
    if(len(undoList) <= 0): return
    action = undoList.pop()
    action.undo()
    redoList.append(action)

def redo():
    if(len(redoList) <= 0): return
    action = redoList.pop()
    action.redo()
    undoList.append(action)
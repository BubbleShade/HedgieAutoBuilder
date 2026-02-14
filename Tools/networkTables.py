import ntcore
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QLineEdit, QPushButton
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, QTimer

from PyQt6.QtGui import QPainter
import time
teamNumber = 2898

inst = ntcore.NetworkTableInstance.getDefault()

class MyPopup(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)
class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super(CustomDialog, self).__init__(parent)
        self.setWindowTitle("Connect to network tables...")
        
        # Create widgets
        layout = QVBoxLayout(self)
        label = QLabel("Enter your team number:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("0000")
        self.name_input.setValidator(QRegularExpressionValidator(QRegularExpression('^[0-9]*$')))
        ok_button = QPushButton("Connect")
        def buttonPress():
            ok_button.setDisabled(True)
            self.name_input.setDisabled(True)
            if(self.name_input.text() == ''): self.name_input.setText("0000")
            connect_to_team(int(self.name_input.text()))
            timer = QTimer(self)

            #timer.setInterval(200)
            self.iterations = 0
            def timerFun():
                text = "Connecting."
                for i in range(self.iterations % 3):
                    text += "."
                self.iterations += 1
                ok_button.setText(text)
                if(inst.isConnected()):
                    print("Successfully Connected!")
                    ok_button.setText("Successfully Connected!")
                    ok_button.clicked.disconnect()
                    ok_button.clicked.connect(self.accept)
                    ok_button.setDisabled(False)

                    timer.setParent(None)
                    timer.deleteLater()
                if(self.iterations > 30):
                    ok_button.setText("Failed to connect. Retry?")

                    ok_button.setDisabled(False)
                    self.name_input.setDisabled(False)

                    timer.setParent(None)
                    timer.deleteLater()



            timer.timeout.connect(timerFun)
            timer.start(500)
             
        
        # Connect button to close the dialog
        ok_button.clicked.connect(buttonPress)
        
        # Add widgets to layout
        layout.addWidget(label)
        layout.addWidget(self.name_input)
        layout.addWidget(ok_button)

    def get_value(self):
        return self.name_input.text()
def doit(parent):
    def thingy():
        dialog = CustomDialog(parent)
        dialog.show()
    return thingy
    #if dialog.exec() == QDialog.Accepted:
    #    print(f"User entered: {dialog.get_value()}")
def connect_to_team(number : int = teamNumber): 
    inst.setServerTeam(number)

    

def push_auto_to_network_tables(json : dict):
    executionPublisher = inst.getStringArrayTopic("QuillT/Auto/execution").publish()

    if(not inst.isConnected()):
        print("Error: Not connected to network tables")
    execution = []
    for (i,j) in json["execution"]:
        execution.append(i)
        execution.append(j)
    executionPublisher.set(execution)

    for i in json.keys():
        if(i == "execution"): continue
        pathPublisher = inst.getDoubleArrayTopic(f"QuillT/Auto/execution/{i}").publish()
        path = []
        for waypoint in json[i]:
            for ctrl in ["prevControl", "nextControl"]:

                control = waypoint[ctrl]
                if control == None:
                    path.append(-1000)
                    path.append(-1000)
                else: 
                    path.append(control["x"])
                    path.append(control['y'])

            anchor      = waypoint["anchor"]
            path.append(anchor["x"])
            path.append(anchor["y"])
            if(anchor["heading"] == None): path.append(-1000)
            else: path.append(anchor["heading"])
        print("Published: ", path)
        pathPublisher.set(value = path)
        
        

        
        


        
    

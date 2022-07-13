#!/usr/bin/env python3

import sys, random, os, time, math, re, shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from deta import Deta
from functools import partial
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
import urllib.request
from datetime import datetime

USER_ME = 0
USER_THEM = 1
USER_BOT = 2

BUBBLE_COLORS = {USER_ME: "#3DD9F5", USER_THEM: "#66FF66", USER_BOT: "#ff0000"}

BUBBLE_PADDING = QMargins(15, 5, 15, 5)
TEXT_PADDING = QMargins(25, 15, 25, 15)

class main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.stack = QStackedWidget()
        self.chatwidget = MainWindow(self)
        self.serverwidget = Server(self)
        self.profilewidget = Profile(self)
        
        self.stack.addWidget(Register(self))
        self.stack.addWidget(self.chatwidget)
        self.stack.addWidget(self.serverwidget)
        self.stack.addWidget(Maze(self))
        self.stack.addWidget(QTicTacToe(self))
        self.stack.addWidget(PreLoader(self))
        self.stack.addWidget(Ranking(self))
        self.stack.addWidget(EditPic(self))
        self.stack.addWidget(self.profilewidget)
        self.stack.addWidget(Desc(self))
        self.stack.addWidget(GuessNumber(self))
        
        #self.stack.setCurrentIndex(0)
        self.preload()
        self.tm = QTimer()
        self.tm.setSingleShot(True)
        self.tm.timeout.connect(self.chat)
        self.tm.start(2000)
        #self.chat()
        
        layout = QGridLayout()
        layout.addWidget(self.stack, 0, 0)
        self.setLayout(layout)
        self.show()
        
    def guess(self):
        self.stack.setCurrentIndex(10)
        
    def upser(self):
        self.serverwidget.checkserver()
        
    def desc(self):
        self.stack.setCurrentIndex(9)
        
    def profile(self, user):
        self.profilewidget.update(user)
        self.stack.setCurrentIndex(8)
        
    def edit(self):
        self.stack.setCurrentIndex(7)
        
    def reg(self):
        self.stack.setCurrentIndex(0)
        
    def closeEvent(self, event):
        event.accept()
        
    def preload(self):
        self.stack.setCurrentIndex(5)
        
    def rank(self):
        self.stack.setCurrentIndex(6)
        
    def connc(self):
        self.chatwidget.get_msg()
        self.chatwidget.starttimer()
        self.stack.setCurrentIndex(1)
        
    def tictactoe(self):
        self.serverwidget.stoptimer()
        self.chatwidget.stoptimer()
        self.stack.setCurrentIndex(4)
        
    def maze(self):
        self.serverwidget.stoptimer()
        self.chatwidget.stoptimer()
        self.stack.setCurrentIndex(3)
        
    def chat(self):
        self.serverwidget.startanim()
        if os.path.isfile("user.sc") and os.path.isfile("id.sc"):
            dateieiei = open("user.sc", "r")
            user2 = dateieiei.read()
            dateieiei.close()
            dateieiei = open("id.sc", "r")
            id2 = dateieiei.read()
            dateieiei.close()
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            users = deta.Base("spamchat")
            user = users.get(user2)
            try:
                id = user["id"]
            except:
                id = None
            if id == id2:
                self.serverwidget.starttimer()
                self.stack.setCurrentIndex(2)
            else:
                MessageDialog("Fehler!", "Es ist ein Fehler aufgetreten. Du konntest nicht angemeldet werden." + str(id) + "%" + str(id2))
                self.reg()
                try:
                    os.remove("id.sc")
                    os.remove("user.sc")
                except:
                    pass
        else:
            self.reg()
            
class RedButton(QPushButton):
    def __init__(self, main, source):
        super().__init__()
        
        self.source = source
        self.main = main
        
        self.setIcon(QIcon("btn.png"))
        self.setIconSize(QSize(100, 100))
        self.setFixedSize(QSize(100, 100))
        self.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
                                             
    def mousePressEvent(self, e):
        self.setIcon(QIcon("btn-prsd.png"))
        
    def mouseReleaseEvent(self, e):
        self.setIcon(QIcon("btn.png"))
        #MessageDialog("__^", str(self.source))
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "Nobody"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(self.user)
        try:
            btns = str(user["btns"])
        except:
            btns = "0"
        #MessageDialog("/", str(list(btns)))
        tt = False
        l = False
        if not str(self.source) in list(btns):
            if int(datetime.today().strftime('%Y%m%d')) > 20220727:
                tt = True
            if not tt:
                btns = str(btns) + str(self.source)
                users = deta.Base("spamchat")
                user = users.get(self.user)
                users.update({"btns": btns}, self.user)
                MessageDialog("Herzlichen Glückwunsch!", "Herzlichen Glückwunsch! Du hast einen Roten Knopf gefunden!")
            else:
                MessageDialog("Fehler", "Das Event wurde am 27.07.2022 beendet.")
        else:
            if int(datetime.today().strftime('%Y%m%d')) > 20220727:
                tt = True
            if tt:
                MessageDialog("Fehler", "Das Event wurde am 27.07.2022 beendet.")
            elif "1" in list(btns) and "2" in list(btns) and "3" in list(btns) and "4" in list(btns) and "5" in list(btns):
                MessageDialog("Herzlichen Glückwunsch!", "Du hast schon alle roten Knöpfe gefunden.")
                l = True
            else:
                MessageDialog("Fehler", "Du hast diesen Roten Knopf schon gedrückt.")
            
        if "1" in list(btns) and "2" in list(btns) and "3" in list(btns) and "4" in list(btns) and "5" in list(btns) and not l and not tt:
            MessageDialog("Herzlichen Glückwunsch!", "Herzlichen Glückwunsch!!! Du hast alle roten Knöpfe gefunden!")
            MessageDialog("Herzlichen Glückwunsch!", "Du findest jetzt einen neuen Server in der Server-Liste")
            datei = open("server.sc", "a")
            datei.write("%ghg%" + "Zahlen-Raten")
            datei.close()
            main.upser(self.main)
                    
class QLabelclick(QLabel):
    def __init__(self, main):
        super().__init__()
        self.clicked=pyqtSignal()
        self.main = main
        """
    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setPixmap(QPixmap("logo.png").scaled(150, 150))
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos())
        dropAction = drag.exec_(Qt.MoveAction)
        """
        
    def mouseReleaseEvent(self, event):
        main.maze(self.main)
    
class GuessNumber(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)

        # Layout the UI
        l = QGridLayout()
        
        self.main = main
            
        back = QPushButton("\n\n")
        back.clicked.connect(main.chat)
        back.setFont(QFont("Macondo", 20))
        back.setIcon(QIcon("back.png"))
        back.setIconSize(QSize(50, 50))
        back.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        
        
        
        self.message_input = QLineEdit()
        self.message_input.setFont(QFont("Macondo", 20))
        self.message_input.setPlaceholderText("Nachricht")

        # Buttons for from/to messages.
        self.btn1 = QPushButton("\n\n")
        self.btn1.setIcon(QIcon("send.png"))
        self.btn1.setIconSize(QSize(50, 50))
        
        self.acse = QLabel("Zahlen-Raten")
        self.acse.setAlignment(Qt.AlignCenter)
        self.acse.setFont(QFont("Macondo", 30))

        self.messages = QListView()
        self.messages.setFont(QFont("Macondo", 20))
        QScroller.grabGesture(self.messages.viewport(), QScroller.LeftMouseButtonGesture)
        self.messages.setVerticalScrollMode(self.messages.ScrollPerPixel)
        # Use our delegate to draw items in this view.
        self.messages.setItemDelegate(MessageDelegate())

        self.model = MessageModel()
        self.messages.setModel(self.model)

        self.btn1.pressed.connect(self.send)
        self.btn1.setFont(QFont("Macondo", 20))
        self.btn1.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        
        l.addWidget(back, 0, 0)
        l.addWidget(self.acse, 0, 1)
        l.addWidget(self.messages, 1, 0, 1, 3)
        l.addWidget(self.message_input, 2, 0, 2, 2)
        l.addWidget(self.btn1, 2, 2)

        self.setLayout(l)
        self.setup()
        
    def setup(self):
        self.rnd = random.randint(0, 1000)
        self.trs = 0
        self.model.add_message(USER_BOT, "(SpamBot): Ich habe mit eine Zahl zwischen 0 und 1000 ausgesucht. Dein Ziel ist es, diese Zahl zu erraten.")
        self.model.add_message(USER_BOT, "(SpamBot): Deine Zahl:")
        
    def send(self):
        nr = self.message_input.text()
        self.message_input.setText("")
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        self.model.add_message(USER_ME, "(" + self.user + "): " + nr)
        try:
            nr = int(nr)
            if nr == self.rnd:
                self.model.add_message(USER_BOT, "(SpamBot): Richtig!!! Du hast " + str(self.trs) + " Versuche gebraucht, um meine Zahl zu erraten.")
                self.model.add_message(USER_BOT, "(SpamBot): Willst do noch einmal spielen?")
                self.model.add_message(USER_ME, "(" + self.user + "): Ja")
                self.model.add_message(USER_BOT, "(SpamBot): Ok")
                self.setup()
            elif nr > self.rnd:
                self.model.add_message(USER_BOT, "(SpamBot): Meine Zahl ist kleiner als " + str(nr))
                self.trs += 1
            else:
                self.model.add_message(USER_BOT, "(SpamBot): Meine Zahl ist größer als " + str(nr))
                self.trs += 1
        except:
            self.model.add_message(USER_BOT, "(SpamBot): Du sollst eine Zahl eingeben!!!")
        
class Desc(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        self.tx = QTextEdit()
        self.tx.setPlaceholderText("Hier kannst du deine Beschreibung ändern. Du kannst auch Markdown verwenden.")
        self.tx.textChanged.connect(self.prev)
        
        new = QPushButton("\n\n")
        new.clicked.connect(main.chat)
        new.setFont(QFont("Macondo", 20))
        new.setIcon(QIcon("back.png"))
        new.setIconSize(QSize(50, 50))
        new.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        
        self.tx2 = QTextEdit()
        self.tx2.setReadOnly(True)
        self.tx2.setPlaceholderText("Vorschau")
        
        fertig = QPushButton("fertig")
        fertig.setFont(QFont("Macondo", 20))
        fertig.clicked.connect(self.finish)
        fertig.setStyleSheet("*{font-weight: bold; border: 5px solid #34dbeb; border-radius: 23px; } *:hover{  background: #34dbeb; }")
        
        ly.addWidget(new, 0, 1)
        ly.addWidget(RedButton(self.main, 3), 0, 2)
        ly.addWidget(self.tx, 1, 1)
        ly.addWidget(self.tx2, 1, 2)
        ly.addWidget(fertig, 2, 1, 2, 2)
        
        try:
            da = open("user.sc", "r")
            us = da.read()
            da.close()
        except:
            us = "nobody"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(us)
        try:
            ppdata = str(user["des"])
        except:
            ppdata = "none"
        self.tx.setText(ppdata)
        
        self.setLayout(ly)
        
    def finish(self):
        datei = open("user.sc", "r")
        self.user = datei.read()
        datei.close()
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(self.user)
        spc = str(user["des"])
        users.update({"des": self.tx.toPlainText()}, self.user)
        MessageDialog("Fertig", "Deine Beschreibung wurde gespeichert.")
        
    def prev(self):
        self.tx2.setMarkdown(self.tx.toPlainText())
        
class Profile(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        self.pp = QLabel()
        self.pp.setAlignment(Qt.AlignCenter)
        
        self.lb = QLabel("none")
        self.lb.setFont(QFont("Macondo", 50))
        self.lb.setAlignment(Qt.AlignCenter)
        
        self.des = QTextEdit()
        self.des.setAlignment(Qt.AlignCenter)
        self.des.setFont(QFont("Macondo", 20))
        self.des.setReadOnly(True)
        self.des.setStyleSheet("background: rgba(0,0,0,0%)")
        
        new = QPushButton("\n\n")
        new.clicked.connect(main.rank)
        new.setFont(QFont("Macondo", 20))
        new.setIcon(QIcon("back.png"))
        new.setIconSize(QSize(50, 50))
        new.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        
        ly.addWidget(new, 0, 1)
        ly.addWidget(self.pp, 1, 1)
        ly.addWidget(self.lb, 2, 1)
        ly.addWidget(self.des, 3, 1)
        ly.addWidget(RedButton(self.main, 1), 5, 5)
        self.setLayout(ly)
        
    def update(self, user):
        self.lb.setText(user)
        self.pp.setPixmap(QPixmap(profilepic.getqt(profilepic.getpp(profilepic.getdata(user)))).scaled(300, 300))
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(user)
        data = str(user["des"])
        
        txt2 = data.split(" ")
        links = []
        for txt in txt2:
            if re.findall('\!\[.*\]\(.*\)', txt):
                it = re.findall('\!\[.*\]\(.*\)', txt)[0]
                it = re.findall('\(.*\)', it)[0]
                it = it[:-1]
                res = it[1:]
                links.append(res)
        #print(links)
        if not os.path.exists("tmp"):
            os.makedirs("tmp")
        else:
            shutil.rmtree("tmp")
            os.makedirs("tmp")
        for url in links:
            data = data.replace(url, "tmp/" + url.split("/")[-1])
            urllib.request.urlretrieve(url, "tmp/" + url.split("/")[-1])
        
        self.des.setMarkdown(data)
        
class profilepic():
    def generatepp():
        w, h = 1000, 1000
        img = Image.new("RGB", (w, h), color="grey")
        img1 = ImageDraw.Draw(img)
        chars = '0123456789ABCDEF'
        col = '#'+''.join(random.sample(chars,6))
        edgs = col
        for z in range(0, 15):
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            edgs =  edgs + "%ghg%" + str(x) + "," + str(y)
        return edgs
        
    def add_corners(im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im
        
    def getdata(username):
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(username)
        ppdata = str(user["profilepic"])
        return ppdata
    
    def getpp(edgs):
        w, h = 1000, 1000
        img = Image.new("RGB", (w, h), color="grey")
        img1 = ImageDraw.Draw(img)
        edgs = edgs.split("%ghg%")
        for t in edgs:
            ab = t.split(",")
            try:
                x, y = ab
                x = int(x)
                y = int(y)
            except:
                x, y = 0, 0
                col = ab[0]
            shape = [(x * 100 - 100), (y * 100 - 100), (x * 100), (y * 100)]
            print(ab)
            print(shape)
            print(col)
            img1.rectangle(shape, fill=col)
        img = profilepic.add_corners(img, 100)
        #img.save('pp.png')
        return img
        
    def getqt(img):
        qim = ImageQt(img)
        pix = QPixmap.fromImage(qim)
        return(pix)
        
class PreLoader(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        logo = QLabel()
        logo.setPixmap(QPixmap("logo.png"))
        logo.setAlignment(Qt.AlignCenter)
        logo.resize(100, 100)
        self.main = main
        gr = QGridLayout()
        gr.addWidget(logo, 1, 1)
        
        rnd = random.randint(0, 10)
        if rnd == 5:
            RickDialog()
        
        effect = QGraphicsOpacityEffect(logo)
        logo.setGraphicsEffect(effect)
        self.setLayout(gr)
        self.anim_2 = QPropertyAnimation(effect, b"opacity")
        self.anim_2.setStartValue(1)
        self.anim_2.setEndValue(0)
        self.anim_2.setDuration(2000)
        self.anim_2.start()
        
class RickDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rick-Roll")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.setFont(QFont("Macondo", 20))
        self.layout = QVBoxLayout()
        rr = QLabel()
        self.movie = QMovie("rickroll.gif")
        rr.setMovie(self.movie)
        self.movie.start()
        self.layout.addWidget(rr)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.exec()
        
class BtnsDialog(QDialog):
    def __init__(self, main):
        super().__init__()
        
        self.setWindowTitle("Neues Event")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.setFont(QFont("Macondo", 20))
        self.layout = QVBoxLayout()
        message = QLabel("Das Red-Button-Event ist gestartet! In Spamchat sind insgesamt fünf rote Knöpfe versteckt.  Findest du sie alle? Du hast bis zum 27.07.2022 Zeit.")
        message.setWordWrap(True)
        self.layout.addWidget(message)
        self.layout.addWidget(RedButton(main, 4))
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.exec()
        
class MessageDialog(QDialog):
    def __init__(self, title, msg):
        super().__init__()
        self.setWindowTitle(title)
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.setFont(QFont("Macondo", 20))
        self.layout = QVBoxLayout()
        message = QLabel(msg)
        message.setWordWrap(True)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.exec()
        
class Ranking(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        self.list = QListWidget()
        self.list.setIconSize(QSize(100, 100))
        self.list.setFont(QFont("Macondo", 40))
        QScroller.grabGesture(self.list.viewport(), QScroller.LeftMouseButtonGesture)
        self.list.setVerticalScrollMode(self.list.ScrollPerPixel)
        self.list.itemClicked.connect(self.profile)
        ly.addWidget(self.list, 3, 1, 4, 2)
        
        new = QPushButton("\n\n")
        new.clicked.connect(self.back)
        new.setFont(QFont("Macondo", 20))
        new.setIcon(QIcon("back.png"))
        new.setIconSize(QSize(50, 50))
        new.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        ly.addWidget(new, 1, 1)
        ly.addWidget(QLabel(""), 1, 2)
        
        self.update()
        
        self.tm = QTimer()
        self.tm.timeout.connect(self.update)
        self.tm.start(10000)
        
        self.setLayout(ly)
        
    def back(self):
        main.chat(self.main)
        
    def profile(self, user):
        us = user.text()
        while  True:
            us = us[:-1]
            if us[-1] == " ":
                us = us[:-1]
                #MessageDialog("/", us)
                break
            else:
                pass
        main.profile(self.main, us)
        
    def update(self):
        self.list.clear()
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        chats = deta.Base("spamchat")
        res = chats.fetch()
        all_items = res.items
        def sort_by_key(list):
            return int("-" + list['spamscore'])
        all_items = sorted(all_items, key=sort_by_key)
        for item in all_items:
            self.list.addItem(QListWidgetItem(QIcon(QPixmap(profilepic.getqt(profilepic.getpp(profilepic.getdata(item["key"]))))), item["key"] + " (" + item["spamscore"] + ")"))
            
class EditPic(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        self.pixel = []
        self.bts = []
        
        #MessageDialog("zzj", str(col.currentColor().name()))
        self.color = "#00ff00"
        wd = QWidget()
        ld = QGridLayout()
        for x in range(1, 11):
            for y in range(1, 11):
                bt = QPushButton()
                bt.setCheckable(True)
                bt.setFixedSize(100, 100)
                bt.clicked.connect(partial(self.click, x, y, bt))
                bt.setStyleSheet("QPushButton { background-color: grey; margin-left: 0px }")
                ld.addWidget(bt, x, y)
                
        wd.setLayout(ld)
        
        fertig = QPushButton("fertig")
        fertig.setFixedHeight(65)
        fertig.setFont(QFont("Macondo", 20))
        fertig.clicked.connect(self.finish)
        fertig.setStyleSheet("*{font-weight: bold; border: 5px solid #34dbeb; border-radius: 30px; } *:hover{  background: #34dbeb; }")
        
        coch = QPushButton("Farbe ändern")
        coch.setFixedHeight(65)
        coch.setFont(QFont("Macondo", 20))
        coch.clicked.connect(self.choose)
        coch.setStyleSheet("*{font-weight: bold; border: 5px solid #34dbeb; border-radius: 30px; } *:hover{  background: #34dbeb; }")
        
        back = QPushButton("\n\n")
        back.clicked.connect(main.chat)
        back.setFont(QFont("Macondo", 20))
        back.setIcon(QIcon("back.png"))
        back.setIconSize(QSize(50, 50))
        back.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        
        ly.addWidget(coch, 3, 0)
        ly.addWidget(fertig, 3, 1)
        ly.addWidget(back, 0, 0)
        ly.addWidget(wd, 1, 0, 2, 0)
                
        self.setLayout(ly)
        
    def choose(self):
        col = QColorDialog()
        col.exec()
        self.color = str(col.currentColor().name())
        for button in self.bts:
            button.setStyleSheet("background-color : " + self.color)
        
    def finish(self):
        edgs = self.color
        for item in self.pixel:
            edgs =  edgs + "%ghg%" + item
        #MessageDialog("/_", edgs)
        datei = open("user.sc", "r")
        self.user = datei.read()
        datei.close()
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(self.user)
        spc = str(user["profilepic"])
        users.update({"profilepic": edgs}, self.user)
        MessageDialog("Fertig", "Dein Profilbild wurde gespeichert.")
        
    def click(self, x, y, button):
        #MessageDialog("ghj", str(x+y))
        if str(y) + ", " + str(x) in self.pixel:
            button.setStyleSheet("background-color : gray")
            self.pixel.remove(str(y) + ", " + str(x))
            self.bts.remove(button)
            #MessageDialog("iuiu", str(self.pixel))
        else:
            button.setStyleSheet("background-color : " + self.color)
            self.pixel.append(str(y) + ", " + str(x))
            self.bts.append(button)
            #MessageDialog("iuiu", str(self.pixel))
            
class Server(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "Nobody"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(self.user)
        try:
            btns = str(user["btns"])
        except:
            btns = "0"
            BtnsDialog(self.main)
        
        rang = QPushButton("Rangliste")
        rang.setFixedHeight(65)
        rang.clicked.connect(self.rank)
        rang.setFont(QFont("Macondo", 20))
        rang.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
                                             }
                                             """)
        
        edit = QPushButton("Profilbild bearbeiten")
        edit.setFixedHeight(65)
        edit.clicked.connect(main.edit)
        edit.setFont(QFont("Macondo", 20))
        edit.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
                                             }
                                             """)
                                             
        des = QPushButton("Beschreibung bearbeiten")
        des.setFixedHeight(65)
        des.clicked.connect(main.desc)
        des.setFont(QFont("Macondo", 20))
        des.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
                                             }
                                             """)
        
        new = QPushButton("Server erstellen")
        new.setFixedHeight(65)
        new.clicked.connect(self.newserver)
        new.setFont(QFont("Macondo", 20))
        new.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
                                             }
                                             """)
        
        join = QPushButton("Server beitreten")
        join.setFixedHeight(65)
        join.clicked.connect(self.joinserver)
        join.setFont(QFont("Macondo", 20))
        join.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
                                             }
                                             """)
                                             
        self.logo = QLabelclick(self.main)
        self.logo.setPixmap(QPixmap("logo.png").scaled(150, 150))
        self.logo.setAlignment(Qt.AlignCenter)
        
        effect = QGraphicsOpacityEffect(self.logo)
        self.logo.setGraphicsEffect(effect)
        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setDuration(2000)
        
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            main.stack.setCurrentIndex(0)
        
        self.listWidget = QListWidget()
        QScroller.grabGesture(self.listWidget.viewport(), QScroller.LeftMouseButtonGesture)
        self.listWidget.setVerticalScrollMode(self.listWidget.ScrollPerPixel)
        if os.path.isfile("server.sc"):
            datei = open("server.sc")
            server = datei.read()
            datei.close()
            serverlist = server.split("%ghg%")
            for item in serverlist:
                if item != "":
                    self.listWidget.addItem(item)
                else:
                    pass
        else:
            pass
            
        self.listWidget.setFont(QFont("Macondo", 30))
        self.listWidget.setStyleSheet("""QListWidget::item{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             margin: 15px;
                                             }
                                             QListWidget::item:hover{
                                             background: #34dbeb;
                                             }
                                             """)
        
        self.actual = QTimer()
        self.actual.timeout.connect(self.checkserver)
        #self.actual.start(5000)
        
        self.actualban = QTimer()
        self.actualban.timeout.connect(self.checkban)
        #self.actualban.start(5000)
        
        self.listWidget.itemClicked.connect(self.connectserver)
        
        ly.addWidget(new, 0, 0)
        ly.addWidget(self.logo, 0, 1)
        ly.addWidget(join, 0, 2)
        ly.addWidget(self.listWidget, 1, 0, 1, 3)
        ly.addWidget(rang, 2, 0)
        ly.addWidget(edit, 2, 1)
        ly.addWidget(des, 2, 2)
        self.setLayout(ly)
        
    def dragEnterEvent(self, e):
        e.accept()
        
    def dropEvent(self, e):
        position = e.pos()
        self.logo.move(position)
        e.setDropAction(Qt.MoveAction)
        e.accept()
        
    def rank(self):
        main.rank(self.main)
        
    def startanim(self):
        self.anim.start()
        
    def starttimer(self):
        self.actualban.start(5000)
        self.actual.start(5000)
    
    def stoptimer(self):
         self.actualban.stop()
         self.actual.stop()
        
    def checkban(self):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        chats = deta.Drive("spamchats-bans")
        invs = chats.get(self.user + ".sc")
        try:
            invis = invs.read().decode('utf_8')
        except:
            invis = ""
        invis = invis.split("%ghg%")
        for item in invis:
            if item != "":
                datei = open("server.sc", "r")
                self.serverlist = datei.read().split("%ghg%")
                datei.close()
                MessageDialog("info", "Du wurdest vom Server " + item.replace(".sc", "") + " gebannt.")
                self.serverlist.remove(item.replace(".sc", ""))
                try:
                    os.remove("server.sc")
                except:
                    pass
                datei = open("server.sc", "a")
                for srv in self.serverlist:
                    datei.write("%ghg%" + srv)
            self.actuserver()
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            chats = deta.Drive("spamchats-bans")
            chats.delete(self.user + ".sc")
        
    def checkserver(self):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        try:
            datei = open("id.sc", "r")
            self.id = int(datei.read())
            datei.close()
        except:
            self.id = 0
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        chats = deta.Drive("spamchats-invitations")
        invs = chats.get(self.user + ".sc")
        try:
            invis = invs.read().decode('utf_8')
        except:
            invis = ""
        invis = invis.split("%ghg%")
        for item in invis:
            if item != "":
                item = item.replace(".sc", "")
                datei = open("server.sc", "a")
                datei.write("%ghg%" + item)
                datei.close()
                deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
                chats = deta.Drive("spamchats")
                chat = chats.get(item + ".sc")
                try:
                    content = chat.read()
                    chat.close()
                    chats.put(item + ".sc", content + b"(" + b"SpamBot" + b"): " + self.user.encode('utf_8') + b" ist dem Server beigetreten." + b"%ghg%")
                except:
                    content = b""
                    print(content)
                    chats.put(item + ".sc", content + b"(" + b"SpamBot" + b"): " + self.user.encode('utf_8') + b" hat den Server erstellt." + b"%ghg%")
                chats = deta.Drive("spamchats-info")
                chat = chats.get(item + ".sc")
                try:
                    content = chat.read()
                    chat.close()
                    chats.put(item + ".sc", content + b"%ghg%" + self.user.encode('utf_8'))
                except:
                    content = b""
                    print(content)
                    chats.put(item + ".sc", content + self.user.encode('utf_8'))
            self.actuserver()
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            chats = deta.Drive("spamchats-invitations")
            chats.delete(self.user + ".sc")
        
    def joinserver(self):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        name, nameok = QInputDialog.getText(self, 'Neuer Server', 'Server-Name: ')
        id, idok = QInputDialog.getText(self, 'Neuer Server', 'Server-ID: ')
        if nameok and idok:
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            chats = deta.Drive("spamchats-ids")
            chat = chats.get(name + ".sc")
            try:
                content = chat.read()
                chat.close()
                if content.decode('utf_8') == id:
                    name.replace("%ghg%", "%ghg/%")
                    datei = open("server.sc", "a")
                    datei.write("%ghg%" + name)
                    datei.close()
                    deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
                    chats = deta.Drive("spamchats")
                    chat = chats.get(name + ".sc")
                    try:
                        content = chat.read()
                        chat.close()
                        chats.put(name + ".sc", content + b"(" + b"SpamBot" + b"): " + self.user.encode('utf_8') + b" ist dem Server beigetreten." + b"%ghg%")
                    except:
                        content = b""
                        print(content)
                        chats.put(name + ".sc", content + b"(" + b"SpamBot" + b"): " + self.user.encode('utf_8') + b" hat den Server erstellt." + b"%ghg%")
                    chats = deta.Drive("spamchats-info")
                    chat = chats.get(name + ".sc")
                    try:
                        content = chat.read()
                        chat.close()
                        chats.put(name + ".sc", content + b"%ghg%" + self.user.encode('utf_8'))
                    except:
                        content = b""
                        print(content)
                        chats.put(name + ".sc", content + self.user.encode('utf_8'))
                    self.actuserver()
                else:
                    MessageDialog("ERROR", "Falscher Server-Name oder ID.")
            except:
                MessageDialog("ERROR", "Der Server existiert nicht!")
        
    def newserver(self):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        text, ok = QInputDialog.getText(self, 'Neuer Server', 'Server-Name: ')
        if ok:
            text = text.replace("%ghg%", "%ghg/%")
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            chats = deta.Drive("spamchats")
            chat = chats.get(text + ".sc")
            try:
                content = chat.read()
                chat.close()
                MessageDialog("Fehler", "Der Server existiert schon. Wenn du ihm beitreten willst, klicke im Menü auf Server beitreten.")
            except:
                datei = open("server.sc", "a")
                datei.write("%ghg%" + text)
                datei.close()
                
                content = b""
                print(content)
                chats.put(text + ".sc", content + b"(" + b"SpamBot" + b"): " + self.user.encode('utf_8') + b" hat den Server erstellt." + b"%ghg%")
            
                chats = deta.Drive("spamchats-info")
                chat = chats.get(text + ".sc")
                try:
                    content = chat.read()
                    chat.close()
                    chats.put(text + ".sc", content + b"%ghg%" + self.user.encode('utf_8'))
                except:
                    content = b""
                    print(content)
                    chats.put(text + ".sc", content + self.user.encode('utf_8'))
                    
                chats = deta.Drive("spamchats-admins")
                chat = chats.get(text + ".sc")
                try:
                    content = chat.read()
                    chat.close()
                    chats.put(text + ".sc", content + b"%ghg%" + self.user.encode('utf_8'))
                except:
                    content = b""
                    print(content)
                    chats.put(text + ".sc", content + self.user.encode('utf_8'))
            
                chats = deta.Drive("spamchats-ids")
                chat = chats.get(text + ".sc")
                chr="0123456789"
                id = "".join(random.choices(chr,k=5))
                chats.put(text + ".sc", str(id))
                MessageDialog("Info", "Deine Server-ID ist: " + str(id) + ". Gib die Server-ID nur Personen, die dem Server beitreten sollen.")
                self.actuserver()
            
    def actuserver(self):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        self.listWidget.clear()
        if os.path.isfile("server.sc"):
            datei = open("server.sc")
            server = datei.read()
            datei.close()
            serverlist = server.split("%ghg%")
            for item in serverlist:
                if item != "":
                    self.listWidget.addItem(item)
                else:
                    pass
        else:
            pass
        
    def connectserver(self, item):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        serv = item.text()
        try:
            os.remove("actu.sc")
        except:
            pass
        if serv == "Zahlen-Raten":
            main.guess(self.main)
        else:
            datei = open("actu.sc", "a")
            datei.write(serv + ".sc")
            datei.close()
            main.connc(self.main)
        
class TicTacToe:
    class Tile:
        def __init__(self, row, column, player=None):
            self.row, self.column = row, column
            self.player = player
            self.delegate = None

        def __str__(self):
            return str(self.player) if self.player is not None else "☐"

        def completeRow(self, ticTacToe):
            row, player = self.row, self.player
            return player == ticTacToe[row, 0].player == ticTacToe[row, 1].player == ticTacToe[row, 2].player

        def completeColumn(self, ticTacToe):
            column, player = self.column, self.player
            return player == ticTacToe[0, column].player == ticTacToe[1, column].player == ticTacToe[2, column].player

        def completeDiagonal(self, ticTacToe):
            row, column, player = self.row, self.column, self.player
            if column - row == 0:
                return player == ticTacToe[0, 0].player == ticTacToe[1, 1].player == ticTacToe[2, 2].player
            if column + row == 2:
                return player == ticTacToe[0, 2].player == ticTacToe[1, 1].player == ticTacToe[2, 0].player

        def notify(self):
            if self.delegate is not None:
                self.delegate.updateEvent(self)

    class Player:
        def __init__(self, symbol):
            self.symbol = symbol

        def __repr__(self):
            return self.symbol

        def reset(self):
            pass

    class BreadthFirstSearchAI(Player):
        def __init__(self, symbol):
            super().__init__(symbol)

        def play(self, ticTacToe, recursionLevel=1):
            bestScore, bestTile = -math.inf, None

            for tile in ticTacToe.choices():
                ticTacToe.set(tile)
                score = ticTacToe.score(tile)
                if score is None:
                    opponentScore, opponentTile = self.play(ticTacToe, recursionLevel + 1)
                    score = -opponentScore
                else:
                    score /= recursionLevel
                if score > bestScore:
                    bestScore, bestTile = score, tile
                ticTacToe.clear(tile)

            return bestScore, bestTile

    def __init__(self, player, ai):
        super().__init__()
        self.player = player
        self.ai = ai
        self.size = 3
        self.next = player
        self.tiles = {}
        for row in range(self.size):
            for column in range(self.size):
                self.tiles[row, column] = TicTacToe.Tile(row, column)

    def __getitem__(self, item):
        return self.tiles[item]

    def __iter__(self):
        return iter(self.tiles.values())

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        string = ""
        for row in range(self.size):
            for column in range(self.size):
                string += str(self[row, column])
            string += "\n"
        return string

    def build(self, symbols, next):
        self.reset()
        for row, symbols_row in enumerate(symbols):
            for column, symbol in enumerate(symbols_row):
                tile = self[row, column]
                if symbol == self.player.symbol:
                    tile.player = self.player
                elif symbol == self.ai.symbol:
                    tile.player = self.ai
                else:
                    tile.player = None
        self.next = next

    def set(self, tile, notify=False):
        if tile.player is not None:
            raise RuntimeError("Inconsistent TicTacToe state")
        tile.player = self.next
        self.next = self.player if self.next == self.ai else self.ai
        if notify is True:
            tile.notify()

    def clear(self, tile, notify=False):
        if tile.player is None:
            raise RuntimeError("Inconsistent TicTacToe state")
        tile.player = None
        self.next = self.player if self.next == self.ai else self.ai
        if notify is True:
            tile.notify()

    def score(self, tile, player=None):
        def complete(ticTacToe):
            for tile in ticTacToe:
                if tile.player is None:
                    return False
            return True

        if tile.player is None:
            return None
        if player is None:
            player = tile.player
        if tile.completeRow(self):
            return +1 if tile.player == player else -1
        if tile.completeColumn(self):
            return +1 if tile.player == player else -1
        if tile.completeDiagonal(self):
            return +1 if tile.player == player else -1
        if complete(self):
            return 0
        return None

    def choices(self):
        return list(filter(lambda tile: tile.player is None, self))

    def round(self, playerTile):
        self.set(playerTile, True)
        playerScore = self.score(playerTile)
        if playerScore is not None:
            return playerScore

        _, aiTile = self.ai.play(self)
        self.set(aiTile, True)
        aiScore = self.score(aiTile)
        if aiScore is not None:
            return -aiScore
        return None

    def reset(self, notify=False):
        for tile in self:
            tile.player = None
            if notify is True:
                tile.notify()
        self.player.reset()
        self.ai.reset()
        self.next = self.player


class QTicTacToe(QWidget):
    class QTileButton(QPushButton):
        SymbolMap = {type(None): " ",
                     TicTacToe.Player: "◯",
                     TicTacToe.BreadthFirstSearchAI: "☓"}

        def __init__(self, parent):
            super(QTicTacToe.QTileButton, self).__init__(parent)
            self.setFocusPolicy(Qt.NoFocus)
            self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             background: None;
                                             }
                                             *:hover{
                                             background: None;
                                             }
                                             """)

        def clickEvent(self, tile):
            self.parent().playRound(tile)

        def updateEvent(self, tile):
            self.setEnabled(tile.player is None)
            xIconPath = "x.png"
            oIconPath = "o.png"
            self.xIcon = QIcon(xIconPath)
            self.oIcon = QIcon(oIconPath)
            self.xIcon.addPixmap(QPixmap(xIconPath), QIcon.Disabled)
            self.oIcon.addPixmap(QPixmap(oIconPath), QIcon.Disabled)
            self.setIconSize(QSize(128, 128))
            if str(tile.player) == str(self.SymbolMap[TicTacToe.Player]):
                self.setIcon(self.oIcon)
            elif str(tile.player) == str(self.SymbolMap[TicTacToe.BreadthFirstSearchAI]):
                self.setIcon(self.xIcon)
            else:
                self.setIcon(QIcon())
            self.update()

        def resizeEvent(self, resizeEvent):
            font = self.font()
            font.setBold(True)
            font.setPixelSize(round(0.50 * min(self.width(), self.height())))
            self.setFont(font)

        def sizeHint(self):
            return QSize(40, 40)

    AIs = [("Breadth First Search AI", TicTacToe.BreadthFirstSearchAI)]

    def __init__(self, main):
        super(QTicTacToe, self).__init__()
        self.main = main
        player = TicTacToe.Player(self.QTileButton.SymbolMap[TicTacToe.Player])
        ai = TicTacToe.BreadthFirstSearchAI(self.QTileButton.SymbolMap[TicTacToe.BreadthFirstSearchAI])
        self.ticTacToe = TicTacToe(player, ai)
        self.initUI()
        self.show()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        ticTaclayout = QGridLayout()
        back = QPushButton("\n\n")
        back.clicked.connect(partial(main.chat, self.main))
        back.setFont(QFont("Macondo", 20))
        back.setIcon(QIcon("back.png"))
        back.setIconSize(QSize(50, 50))
        back.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        ticTaclayout.addWidget(back, 0, 1)
        ticTaclayout.addWidget(QLabel(), 1, 0)
        ticTaclayout.setSpacing(3)
        layout.addLayout(ticTaclayout)
        self.setLayout(layout)
        for tile in self.ticTacToe:
            button = QTicTacToe.QTileButton(self)
            ticTaclayout.addWidget(button, tile.row + 2, tile.column)
            button.clicked.connect(lambda _, button=button, tile=tile: button.clickEvent(tile))
            tile.delegate = button
            pass

    def playRound(self, tile):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        gameScore = self.ticTacToe.round(tile)
        QApplication.restoreOverrideCursor()
        if gameScore is not None:
            if gameScore == +1:
                MessageDialog("Gewonnen!", "Du hast gewonnen :)")
            if gameScore == 0:
                MessageDialog("Unentschieden!", "Unentschieden :|")
            if gameScore == -1:
                MessageDialog("Verloren!", "Du hast verloren :(")
            self.ticTacToe.reset(True)

    def sizeHint(self):
        return QSize(180, 220)


class Maze(QWidget):
    class Node:
        def __init__(self, row, column):
            self.row, self.column = row, column
            self.neighbors = []
            self.links = []

        def point(self, maze):
            return QPoint(self.column * maze.paintStep, self.row * maze.paintStep)

        def closest(self, maze, point):
            closestNode, closestDistance = None, float("inf")
            for node in self.links:
                delta = point - node.point(maze)
                distance = delta.manhattanLength()
                if distance < closestDistance:
                    closestNode, closestDistance = node, distance
            return closestNode

        def crawl(self, direction, distance = 1):
            if len(self.links) > 2 and distance > 1:
                return self
            for link in self.links:
                if direction == (link.row - self.row, link.column - self.column):
                    return link.crawl(direction, distance + 1)
            else:
                return self

    def __init__(self, main):
        super(Maze, self).__init__()
        self.size = 15
        self.main = main
        self.nodes = None
        self.startNode = None
        self.finishNode = None
        self.playerNode = None
        self.paintStep = 0
        self.paintOffset = 0
        
        back = QPushButton("\n\n")
        back.clicked.connect(main.chat)
        back.setFont(QFont("Macondo", 20))
        back.setIcon(QIcon("back.png"))
        back.setIconSize(QSize(50, 50))
        back.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
                                             
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "Nobody"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(self.user)
        try:
            level = str(user["level"])
        except:
            #MessageDialog("Kein Internet!", "Ein Fehler ist aufgetreten. Deine Level können nicht aktualisiert werden.")
            level = "0"
        self.lv = QLabel("Level: " + level)
        self.lv.setFont(QFont("Macondo", 20))
        
        gr = QGridLayout()
        gr.addWidget(back, 0, 0)
        gr.addWidget(QLabel(), 0, 1)
        gr.addWidget(QLabel(), 0, 2)
        gr.addWidget(QLabel(), 0, 3)
        gr.addWidget(QLabel(), 0, 4)
        gr.addWidget(self.lv, 0, 5)
        gr.addWidget(RedButton(self.main, 2), 2, 0)
        gr.addWidget(QLabel(), 1, 1)
        self.setLayout(gr)

        self.initMaze()
        self.show()

    @pyqtProperty(QPoint)
    def player(self):
        return self._player

    @player.setter
    def player(self, point):
        self._player = point
        self.update()

    def initMaze(self):
        self.nodes = {}
        for row in range(self.size):
            for column in range(self.size):
                self.nodes[row, column] = Maze.Node(row, column)

        for (row, column), node in self.nodes.items():
            if 0 < row:
                node.neighbors.append(self.nodes[row - 1, column])
            if row < self.size - 1:
                node.neighbors.append(self.nodes[row + 1, column])
            if 0 < column:
                node.neighbors.append(self.nodes[row, column - 1])
            if column < self.size - 1:
                node.neighbors.append(self.nodes[row, column + 1])

        self.startNode = self.nodes[0, 0]
        self.finishNode = self.generateMaze(self.startNode)
        self.playerNode = self.startNode
        self.player = self.playerNode.point(self)

    def generateMaze(self, start):
        generated = set()
        deepest_node, deepest_recursion = None, -1

        def generateNode(node, recursion=0):
            nonlocal generated, deepest_node, deepest_recursion
            if node in generated:
                return
            generated.add(node)
            for neighbor in random.sample(node.neighbors, len(node.neighbors)):
                if neighbor not in generated:
                    node.links.append(neighbor)
                    neighbor.links.append(node)
                    generateNode(neighbor, recursion + 1)
            if recursion > deepest_recursion:
                deepest_node, deepest_recursion = node, recursion

        generateNode(start)
        return deepest_node

    def mousePressEvent(self, mouseEvent):
        closestNode = self.playerNode.closest(self, mouseEvent.pos() - self.paintOffset)
        direction = closestNode.row - self.playerNode.row, closestNode.column - self.playerNode.column
        crawlNode = self.playerNode.crawl(direction)

        self.animation = QPropertyAnimation(self, b"player")
        if len(crawlNode.links) > 2:
            self.animation.setEasingCurve(QEasingCurve.OutBack);
        else:
            self.animation.setEasingCurve(QEasingCurve.OutBounce);
        self.animation.setStartValue(self.player)
        self.animation.setEndValue(crawlNode.point(self))
        self.animation.setDuration(400)
        self.animation.start()

        self.playerNode = crawlNode
        if self.playerNode == self.finishNode:
            MessageDialog("Gewonnen!", "Du hast gewonnen :)")
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            users = deta.Base("spamchat")
            user = users.get(self.user)
            try:
                level = str(user["level"])
                users.update({"level": int(level) + 1}, self.user)
                self.lv.setText("Level: " + str(int(level) + 1))
            except:
                MessageDialog("Kein Internet!", "Ein Fehler ist aufgetreten. Deine Level können nicht aktualisiert werden.")
                level = "0"
            self.initMaze()

    def paintEvent(self, paintEvent):
        pen = QPen()
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        painter = QPainter(self)
        painter.translate(self.paintOffset)
        painter.setBackgroundMode(Qt.TransparentMode)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.nodes is not None:
            painted = set()

            def paintNode(node):
                nonlocal painter, painted
                if node in painted:
                    return
                painted.add(node)
                for link in node.links:
                    if link not in painted:
                        painter.drawLine(node.point(self), link.point(self))
                        paintNode(link)

            color = self.palette().color(QPalette.Dark)
            pen.setColor(color)
            pen.setWidth(0.50 * self.paintStep)
            painter.setPen(pen)
            for node in self.nodes.values():
                if paintEvent.region().contains(node.point(self)):
                    paintNode(node)

        if self.startNode is not None:
            color = self.palette().color(QPalette.Dark)
            pen.setColor(color)
            pen.setWidth(0.75 * self.paintStep)
            painter.setPen(pen)
            if paintEvent.region().contains(self.startNode.point(self)):
                painter.drawPoint(self.startNode.point(self))

        if self.finishNode is not None and paintEvent.region().contains(self.finishNode.point(self)):
            color = self.palette().color(QPalette.Dark).darker(120)
            pen.setColor(color)
            pen.setWidth(0.75 * self.paintStep)
            painter.setPen(pen)
            painter.drawPoint(self.finishNode.point(self))

        if self.player is not None:
            color = self.palette().color(QPalette.Highlight)
            color.setAlpha(196)
            pen.setColor(color)
            pen.setWidth(0.90 * self.paintStep)
            painter.setPen(pen)
            painter.drawPixmap(QPoint(self.player.x() - 50, self.player.y() - 30), QPixmap("logo-maze.png").scaledToWidth(100))

        del painter, pen

    def resizeEvent(self, resizeEvent):
        self.paintStep = min(self.width() / self.size, self.height() / self.size)
        self.paintOffset = QPoint((self.paintStep + (self.width() - self.paintStep * self.size)) / 2,
                                  (self.paintStep + (self.height() - self.paintStep * self.size)) / 2)
        self.player = self.playerNode.point(self)

    def sizeHint(self):
        paintStepHint = 40
        return QSize(self.size * paintStepHint, self.size * paintStepHint)
        
class Register(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        lab = QLabel("Du must nur noch einen Username eingeben, dann kann es los gehen!")
        lab.setFont(QFont("Macondo", 20))
        self.us = QLineEdit()
        self.us.setPlaceholderText("Username")
        self.us.setFont(QFont("Macondo", 20))
        fertig = QPushButton("\nFertig\n")
        fertig.setFont(QFont("Macondo", 20))
        fertig.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
                                             }
                                             """)
        fertig.clicked.connect(self.regg)
        plttzz = QLabel()
        
        ly.addWidget(fertig, 3, 1)
        ly.addWidget(self.us, 2, 1)
        ly.addWidget(lab, 1, 1)
        
        self.setLayout(ly)
        
    def regg(self):
        us = self.us.text()
        chr="0123456789"
        id = "".join(random.choices(chr,k=5))
        try:
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            users = deta.Base("spamchat")
            users.insert({"key": us, "id": id, "level": "0", "spamscore": "0", "profilepic": profilepic.generatepp(), "des": "Hi! Ich benutze Spamchat"})
            MessageDialog("Fertig", "Fertig! Du kannst jetzt Nachrichten senden. Deine ID ist: " + str(id))
            rigi = 1
        except:
            MessageDialog("Kein Internet!", "Bist du mit dem Internet verbunden? Vielleicht ist der Username auch schon vergeben.")
            rigi = 0
        if rigi == 1:
            dateieiei = open("user.sc", "a")
            dateieiei.write(us)
            dateieiei.close()
            dateieiei = open("id.sc", "a")
            dateieiei.write(id)
            dateieiei.close()
            main.chat(self.main)
        else:
            pass


class MessageDelegate(QStyledItemDelegate):
    """
    Draws each message.
    """

    def paint(self, painter, option, index):
        # Retrieve the user,message uple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.

        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        # draw the triangle bubble-pointer, starting from

        if user == USER_ME:
            p1 = bubblerect.topRight()
        else:
            p1 = bubblerect.topLeft()
        painter.drawPolygon(p1 + QPoint(-20, 0), p1 + QPoint(20, 0), p1 + QPoint(0, 20))

        # draw the text
        painter.setPen(Qt.black)
        self.text_side_offset, self.text_top_offset = 50, 5
        text_margins = QMargins(self.text_side_offset, self.text_top_offset, self.text_side_offset, self.text_top_offset)
        painter.drawText(option.rect.marginsRemoved(text_margins), Qt.AlignVCenter | Qt.TextWordWrap, text)

    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        # Calculate the dimensions the text will require.
        metrics = QApplication.fontMetrics()
        self.text_side_offset, self.text_top_offset = 50, 20
        text_margins = QMargins(self.text_side_offset, self.text_top_offset, self.text_side_offset, self.text_top_offset)
        rect = option.rect.marginsRemoved(text_margins)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, text)
        rect = rect.marginsAdded(text_margins)  # Re add padding for item size.
        return rect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text):
        """
        Add an message to our message list, getting the text from the QLineEdit
        """
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.messages.append((who, text))
            # Trigger refresh.
            self.layoutChanged.emit()
            
    def del_message(self):
        self.messages = []

class MainWindow(QMainWindow):
    def __init__(self, main):
        super(MainWindow, self).__init__()

        # Layout the UI
        l = QGridLayout()
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            main.stack.setCurrentIndex(0)
        self.firsttime = True
        self.oldcom = False
        self.main = main
        self.server = "none.sc"
        try:
            os.remove("actu.sc")
        except:
            pass
            
        back = QPushButton("\n\n")
        back.clicked.connect(main.chat)
        back.setFont(QFont("Macondo", 20))
        back.setIcon(QIcon("back.png"))
        back.setIconSize(QSize(50, 50))
        back.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "Nobody"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(self.user)
        try:
            spsc = str(user["spamscore"])
        except:
            #MessageDialog("Kein Internet!", "Ein Fehler ist aufgetreten. Deine Level können nicht aktualisiert werden.")
            spsc = "0"
        self.sppc = QLabel("Spamscore: " + spsc)
        self.sppc.setAlignment(Qt.AlignRight)
        self.sppc.setFont(QFont("Macondo", 20))
        
        self.message_input = QLineEdit()
        self.message_input.setFont(QFont("Macondo", 20))
        self.message_input.setPlaceholderText("Nachricht")

        # Buttons for from/to messages.
        self.btn1 = QPushButton("\n\n")
        self.btn1.setIcon(QIcon("send.png"))
        self.btn1.setIconSize(QSize(50, 50))
        
        self.acse = QLabel()
        self.acse.setAlignment(Qt.AlignCenter)
        self.acse.setFont(QFont("Macondo", 30))

        self.messages = QListView()
        self.messages.setFont(QFont("Macondo", 20))
        QScroller.grabGesture(self.messages.viewport(), QScroller.LeftMouseButtonGesture)
        self.messages.setVerticalScrollMode(self.messages.ScrollPerPixel)
        # Use our delegate to draw items in this view.
        self.messages.setItemDelegate(MessageDelegate())

        self.model = MessageModel()
        self.messages.setModel(self.model)

        self.btn1.pressed.connect(self.message_to)
        self.btn1.setFont(QFont("Macondo", 20))
        self.btn1.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: None;
                                             padding: -25px;
                                             }
                                             """)
        
        self.setup_msg()
        
        self.check = QTimer()
        self.check.timeout.connect(self.get_msg)
        #self.check.start(1000)
        
        l.addWidget(back, 0, 0)
        l.addWidget(self.acse, 0, 1)
        l.addWidget(self.sppc, 0, 3)
        l.addWidget(self.messages, 1, 0, 1, 5)
        l.addWidget(self.message_input, 2, 0, 2, 3)
        l.addWidget(self.btn1, 2, 3)
        l.addWidget(RedButton(self.main, 5), 0, 4)

        self.w = QWidget()
        self.w.setLayout(l)
        self.setCentralWidget(self.w)
        
    def starttimer(self):
        self.check.start(2000)
    
    def stoptimer(self):
        self.check.stop()
        
    def execcmd(self, msg):
        list = msg.split("-")
        if msg.startswith("!spam"):
            try:
                dur = list[1].replace(" ", "")
                ms = list[2]
                if int(dur) > 1 and int(dur) < 21:
                    for x in range(0, int(dur)):
                        self.write_msg(ms, self.user)
                else:
                    MessageDialog("ERROR", "Die Zahl " + dur + " ist zu groß. Bitte gib eine Zahl zwischen 2 und 20 ein.")
            except:
                MessageDialog("ERROR", "Der Befehl \"" + msg + "\" konnte nicht aufgeführt werden.")
                
        elif msg.startswith("!info"):
            try:
                deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
                chats = deta.Drive("spamchats-info")
                chat = chats.get(self.server)
                try:
                    content = chat.read()
                    chat.close()
                    listofuser = content.decode('utf_8').replace("%ghg%", ", ")
                except:
                    listofuser = ""
                chats = deta.Drive("spamchats-ids")
                chat = chats.get(self.server)
                try:
                    content = chat.read()
                    chat.close()
                    serverid = content.decode('utf_8')
                except:
                    serverid = ""
                datei = open("actu.sc", "r")
                MessageDialog("info", "Aktueller Server: " + datei.read().replace(".sc", "") + "\nID:" + serverid + "\nUser: " + str(listofuser))
                datei.close()
            except:
                MessageDialog("ERROR", "Der Befehl \"" + msg + "\" konnte nicht aufgeführt werden.")
                
        elif msg.startswith("!xo"):
            main.tictactoe(self.main)
            
        elif msg.startswith("!admin"):
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            chats = deta.Drive("spamchats-admins")
            chat = chats.get(self.server)
            try:
                content = chat.read()
                chat.close()
            except:
                content = b""
            content = content.decode('utf_8').split("%ghg%")
            if self.user in content:
                chats = deta.Drive("spamchats-admins")
                chat = chats.get(self.server)
                try:
                    content = chat.read()
                    chat.close()
                    chats.put(self.server, content + b"%ghg%" + list[1].encode('utf_8'))
                except:
                    content = b""
                    print(content)
                    chats.put(self.server, content + list[1].encode('utf_8'))
                MessageDialog("info", list[1] + " wurde zum Admin.")
            else:
                MessageDialog("ERROR", "Nur Admins können andere Admins hinzufügen.")
                
        elif msg.startswith("!ban"):
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            chats = deta.Drive("spamchats-admins")
            chat = chats.get(self.server)
            try:
                content = chat.read()
                chat.close()
            except:
                content = b""
            content = content.decode('utf_8').split("%ghg%")
            if self.user in content:
                name = list[1]
                chats = deta.Drive("spamchats-bans")
                invs = chats.get(name + ".sc")
                try:
                    invis = invs.read()
                except:
                    invis = b""
                datei = open("actu.sc", "r")
                chats.put(name + ".sc", invis + b"%ghg%" + datei.read().encode('utf_8'))
                datei.close()
                MessageDialog("info", "Du hast " + name + " gebannt.")
            else:
                MessageDialog("ERROR", "Nur Admins können andere Personen bannen.")
                
        elif msg.startswith("!invite"):
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            chats = deta.Drive("spamchats-admins")
            chat = chats.get(self.server)
            try:
                content = chat.read()
                chat.close()
            except:
                content = b""
            content = content.decode('utf_8').split("%ghg%")
            if self.user in content:
                name = list[1]
                chats = deta.Drive("spamchats-invitations")
                invs = chats.get(name + ".sc")
                try:
                    invis = invs.read()
                except:
                    invis = b""
                datei = open("actu.sc", "r")
                chats.put(name + ".sc", invis + b"%ghg%" + datei.read().encode('utf_8'))
                datei.close()
                MessageDialog("info", "Du hast " + name + " eingeladen.")
            else:
                MessageDialog("ERROR", "Nur Admins können andere Personen einladen.")
                
    def message_to(self):
        if self.message_input.text().startswith("!"):
            self.execcmd(self.message_input.text())
        else:
            self.model.add_message(USER_ME, self.message_input.text())
            self.write_msg(self.message_input.text(), self.user)

    def message_from(self):
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        chats = deta.Drive("spamchats")
        self.model.add_message(USER_THEM, self.message_input.text())
        self.write_msg("hallo", self.user)
        self.get_msg()
        
    def setup_msg(self):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        try:
            datei = open("actu.sc", "r")
            self.server = datei.read()
            datei.close()
        except:
            self.server = "none.sc"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        chats = deta.Drive("spamchats")
        chat = chats.get(self.server)
        try:
            content = chat.read()
            chat.close()
            listofmsgnew = content.split(b"%ghg%")
        except:
            listofmsgnew = []
        self.oldcon = listofmsgnew
        self.oldcom = True
        indx = 0
        for item in listofmsgnew:
            indx += 1
            print(item.decode('utf_8'))
            if item.decode('utf_8').startswith("(SpamBot)"):
                self.model.add_message(USER_BOT, item.decode('utf_8'))
            elif item.decode('utf_8').startswith("(" + self.user + ")"):
                self.model.add_message(USER_ME, item.decode('utf_8'))
            else:
                self.model.add_message(USER_THEM, item.decode('utf_8'))

    def get_msg(self):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        try:
            datei = open("actu.sc", "r")
            self.server = datei.read()
            datei.close()
        except:
            self.server = "none.sc"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        
        self.acse.setText(str(self.server)[:-3])
        
        chats = deta.Drive("spamchats")
        chat = chats.get(self.server)
        try:
            content = chat.read()
            chat.close()
            listofmsg = content.split(b"%ghg%")
        except:
            content = ""
            listofmsg = []
        if self.oldcom:
            if not self.oldcon == content:
                self.model.del_message()
                self.setup_msg()
                self.oldcon = content

    def write_msg(self, msg, user, repl=False):
        try:
            datei = open("user.sc", "r")
            self.user = datei.read()
            datei.close()
        except:
            self.user = "none"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        users = deta.Base("spamchat")
        user = users.get(self.user)
        if 1 == 1:
            spc = str(user["spamscore"])
            users.update({"spamscore": str(int(spc) + 1)}, self.user)
            self.sppc.setText("Spamscore: " + str(int(spc) + 1))
        else:
            MessageDialog("Kein Internet!", "Ein Fehler ist aufgetreten. Dein Spamscore kann nicht aktualisiert werden.")
            spc = "0"
        try:
            datei = open("actu.sc", "r")
            self.server = datei.read()
            datei.close()
        except:
            self.server = "none.sc"
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        chats = deta.Drive("spamchats")
        data = chats.get(self.server)
        try:
            content = data.read()
            data.close()
            if not repl:
                chats.put(self.server, content + b"(" + self.user.encode('utf_8') + b"): " + msg.replace("%ghg%", "%ghg!%").encode('utf_8') + b"%ghg%")
            else:
                chats.put(self.server, msg.encode('utf_8') + b"%ghg%")
        except:
            content = b""
            print(content)
            if not repl:
                chats.put(self.server, content + b"(" + self.user.encode('utf_8') + b"): " + msg.replace("%ghg%", "%ghg!%").encode('utf_8') + b"%ghg%")
            else:
                chats.put(self.server, msg + b"%ghg%")


app = QApplication(sys.argv)

app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

QFontDatabase.addApplicationFont("fonts/Macondo.ttf")

window = main()
window.show()
app.exec_()

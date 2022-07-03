#!/usr/bin/env python3

import sys, random, os, time, math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from deta import Deta
from functools import partial

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
        self.stack.addWidget(Register(self))
        self.stack.addWidget(self.chatwidget)
        self.stack.addWidget(self.serverwidget)
        self.stack.addWidget(Maze(self))
        self.stack.addWidget(QTicTacToe(self))
        self.stack.addWidget(PreLoader(self))
        self.stack.addWidget(Ranking(self))
        
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
        
    def reg(self):
        self.stack.setCurrentIndex(0)
        
    def closeEvent(self, event):
        MessageDialog("Beenden", "Spamchat wird beendet.")
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
                    
class QLabelclick(QLabel):
    def __init__(self, main):
        super().__init__()
        self.clicked=pyqtSignal()
        self.main = main
    def mouseReleaseEvent(self, event):
        main.maze(self.main)
        
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
        effect = QGraphicsOpacityEffect(logo)
        logo.setGraphicsEffect(effect)
        self.setLayout(gr)
        self.anim_2 = QPropertyAnimation(effect, b"opacity")
        self.anim_2.setStartValue(1)
        self.anim_2.setEndValue(0)
        self.anim_2.setDuration(2000)
        self.anim_2.start()
        
class RickDialog(QDialog):
    def __init__(self, v, f):
        super().__init__()
        self.setWindowTitle("Rick-Roll")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.setFont(QFont("Macondo", 20))
        self.layout = QVBoxLayout()
        lb = QLabel(f + " von " + v)
        rr = QLabel()
        self.movie = QMovie("rickroll.gif")
        rr.setMovie(self.movie)
        self.movie.start()
        self.layout.addWidget(lb)
        self.layout.addWidget(rr)
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
        ly.addWidget(self.list, 1, 1)
        
        new = QPushButton("\nZurück\n")
        new.clicked.connect(self.back)
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
        ly.addWidget(new, 0, 0, 1, 0)
        
        self.update()
        
        self.setLayout(ly)
        
    def back(self):
        main.chat(self.main)
        
    def update(self):
        deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
        chats = deta.Base("spamchat")
        res = chats.fetch()
        all_items = res.items
        def sort_by_key(list):
    	    return int("-" + list['spamscore'])
        all_items = sorted(all_items, key=sort_by_key)
        for item in all_items:
            self.list.addItem(item["key"] + " (" + item["spamscore"] + ")")
                                            
class Server(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        rang = QPushButton("\nRangliste\n")
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
        
        new = QPushButton("\nServer erstellen\n")
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
        
        join = QPushButton("\nServer beitreten\n")
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
                                             
        logo = QLabelclick(self.main)
        logo.setPixmap(QPixmap("logo.png").scaled(150, 150))
        logo.setAlignment(Qt.AlignCenter)
        
        effect = QGraphicsOpacityEffect(logo)
        logo.setGraphicsEffect(effect)
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
                                             border-radius: 25px;
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
        ly.addWidget(logo, 0, 1)
        ly.addWidget(join, 0, 2)
        ly.addWidget(self.listWidget, 1, 0, 1, 3)
        ly.addWidget(rang, 2, 0)
        self.setLayout(ly)
        
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
                    chats.put(item + ".sc", content + b"(" + b"spambot" + b"): " + self.user.encode('utf_8') + b" ist dem Server beigetreten." + b"%ghg%")
                except:
                    content = b""
                    print(content)
                    chats.put(item + ".sc", content + b"(" + b"spambot" + b"): " + self.user.encode('utf_8') + b" hat den Server erstellt." + b"%ghg%")
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
                        chats.put(name + ".sc", content + b"(" + b"spambot" + b"): " + self.user.encode('utf_8') + b" ist dem Server beigetreten." + b"%ghg%")
                    except:
                        content = b""
                        print(content)
                        chats.put(name + ".sc", content + b"(" + b"spambot" + b"): " + self.user.encode('utf_8') + b" hat den Server erstellt." + b"%ghg%")
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
                MessageDialog("ERROR", "Du konntest dem Server nicht beitreten")
        
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
                chats.put(text + ".sc", content + b"(" + b"spambot" + b"): " + self.user.encode('utf_8') + b" hat den Server erstellt." + b"%ghg%")
            
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
        MessageDialog("Info", "verbinden mit " + serv + "...")
        try:
            os.remove("actu.sc")
        except:
            pass
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
        back = QPushButton("\nzurück\n")
        back.clicked.connect(partial(main.chat, self.main))
        back.setFont(QFont("Macondo", 20))
        back.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
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
        
        back = QPushButton("\nzurück\n")
        back.clicked.connect(main.chat)
        back.setFont(QFont("Macondo", 20))
        back.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
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
            users.insert({"key": us, "id": id, "level": "0", "spamscore": "0", "rickroll": "0"})
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
            
        back = QPushButton("\nZurück\n")
        back.clicked.connect(main.chat)
        back.setFont(QFont("Macondo", 20))
        back.setStyleSheet("""*{
                                             font-weight: bold;
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
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
        self.btn1 = QPushButton("\nsenden!\n")

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
                                             border: 5px solid #34dbeb;
                                             border-radius: 30px;
                                             padding: -25px;
                                             }
                                             *:hover{
                                             background: #34dbeb;
                                             }
                                             """)
        
        self.setup_msg()
        
        self.check = QTimer()
        self.check.timeout.connect(self.get_msg)
        #self.check.start(1000)
        
        l.addWidget(back, 0, 0)
        l.addWidget(self.sppc, 0, 1)
        l.addWidget(self.messages, 1, 0, 1, 2)
        l.addWidget(self.message_input, 2, 0, 2, 2)
        l.addWidget(self.btn1, 4, 0, 4, 2)

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
                
        elif msg.startswith("!RickRoll"):
            deta = Deta("a0nx7pgk_CAsXSD5UjJsWT8xj9nPSAb14xduJ1fUR")
            users = deta.Base("spamchat")
            user = users.get(list[1])
            spc = str(user["rickroll"])
            users.update({"rickroll": str(int(spc) + 1)}, list[1])
                
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
            if item.decode('utf_8').startswith("(spambot)"):
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

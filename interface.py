# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaceHeNCnP.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QStackedWidget, QToolButton, QVBoxLayout, QWidget)
import res

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(693, 425)
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setStyleSheet(u"* {\n"
"	border: none;\n"
"    padding: 0px;\n"
"    margin: 0px;\n"
"    background-color: none;\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QScrollArea {\n"
"    border: 1px;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    width: 4px;\n"
"    margin: 10px 0px 10px 0px;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    height: 4px;\n"
"    margin: 0px 40px 0px 40px;\n"
"}\n"
"\n"
"QScrollBar:vertical, QScrollBar:horizontal {\n"
"    background: #dddddd;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical, QScrollBar::handle:horizontal {\n"
"    background: #424242;\n"
"    border-radius: 2px;\n"
"    min-height: 20px;\n"
"    min-width: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {\n"
"    background: #a7b308;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line, QScrollBar::sub-line {\n"
"    background: transparent;\n"
"}\n"
"\n"
"#leftMenuBar QPushButton {\n"
"	font-size: 14px;\n"
"	color: #dddddd;\n"
"	t"
                        "ext-align: left;\n"
"	padding-left: 8px;\n"
"	padding-right: 8px;\n"
"	margin: 2px 2px;\n"
"}\n"
"\n"
"#leftMenuBar QPushButton:hover {\n"
"	background: #3f4145;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#mainBtnWidget QPushButton:focus {\n"
"	background: #0f1114;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#leftMenuBar QPushButton:pressed {\n"
"	background: #2e436e;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#someMoreBtnFrame QToolButton:hover {\n"
"	background: #3f4145;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#someMoreBtnFrame QToolButton:pressed {\n"
"	background: #2e436e;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#appTitleBtn {\n"
"	padding-top: 2px;\n"
"	padding-bottom: 4px;\n"
"}\n"
"\n"
"#appIconBtn {\n"
"}\n"
"\n"
"#appIconBtn:hover {\n"
"	background: #a7b308;\n"
"	border-radius: 8px;\n"
"}\n"
"\n"
"#appIconBtn:pressed {\n"
"	background: #000000;\n"
"	border-radius: 8px;\n"
"}\n"
"\n"
"#appResetBtn,\n"
"#mediaPlayerShowBtn {\n"
"	border-radius: 8px;\n"
"}\n"
"\n"
"#appMinBtn:hover,  \n"
"#appMaxBtn:hover,\n"
"#"
                        "appResetBtn:hover,\n"
"#mediaPlayerShowBtn:hover {\n"
"	background: #404a4a;\n"
"}\n"
"\n"
"#netSpeedBtn {\n"
"	padding-bottom: 0px;\n"
"}\n"
"\n"
"#appMinBtn:pressed,\n"
"#appMaxBtn:pressed,\n"
"#appResetBtn:pressed,\n"
"#mediaPlayerShowBtn:pressed {\n"
"	background: #303a3a;\n"
"}\n"
"\n"
"#appCloseBtn:hover {\n"
"	background: #dd0000;\n"
"}\n"
"\n"
"#appCloseBtn:pressed {\n"
"	background: #ff0000;\n"
"}\n"
"\n"
"QPushButton {\n"
"	color: #dddddd;\n"
"}\n"
"\n"
"#leftMenuBar {\n"
"	background: #1e1f22;\n"
"}\n"
"\n"
"#centerMainMenu {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#headerContainer {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#searchWidget {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#footer {\n"
"	border-top: 1px solid #3b3d40;\n"
"}\n"
"\n"
"#footer QPushButton {\n"
"	font-size: 10px;\n"
"}\n"
"\n"
"#footer QLabel{\n"
"	background: #3b3d40;\n"
"	margin: 3px 3px; \n"
"	color: #00ff00;\n"
"	font-size: 12px;\n"
"	border-radius: 8px;\n"
"	padding-bottom: 1px;\n"
"	padding-left: 6px;\n"
"	padding-right: 6"
                        "px;\n"
"}\n"
"\n"
"#totalDownloadedLabel {\n"
"	text-align: left;\n"
"}\n"
"\n"
"#headerContainer {\n"
"	border-bottom: 1px solid #3b3d40;\n"
"}\n"
"\n"
"#leftMenuBar {\n"
"	border-right: 1px solid #3b3d40;\n"
"}\n"
"\n"
"#netSpeedBtn {\n"
"	font-size: 10px;\n"
"}\n"
"\n"
"#closeNotificationBtn {\n"
"	margin: 6px 6px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"#closeNotificationBtn:hover {\n"
"	background: #111111;\n"
"}\n"
"\n"
"#notificationWidget {\n"
"	margin: 10px 10px;\n"
"	background: #444444;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#notificationTitleLabel {\n"
"	font-size: 14px;\n"
"	color: #dddddd;\n"
"}\n"
"\n"
"#notificationTextLabel {\n"
"	font-size: 14px;\n"
"	color: #dddddd;\n"
"}\n"
"\n"
"#searchScrollArea {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#searchInputText {\n"
"	background: #444444;\n"
"	color: #dddddd;\n"
"	padding: 0px 12px;\n"
"	border-top-left-radius: 8px;\n"
"    border-bottom-left-radius: 8px;\n"
"}\n"
"\n"
"#searchBtn {\n"
"	background-color: #1e335e;\n"
"	border-top-right-radius"
                        ": 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"#searchBtn:hover {\n"
"	background-color: #111111;\n"
"	border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"#searchBtn:pressed {\n"
"	background-color: #a7b308;\n"
"	border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"#scrollAreaContents {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#searchOutputFrame {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#resultNameLabel {\n"
"	font-size: 14px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#searchOutputFrame QLabel {\n"
"	font-size: 12px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#searchOutputFrame QPushButton {\n"
"	font-size: 12px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#magnetLinkBtn {\n"
"	background: #DA4167;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#magnetLinkBtn:hover {\n"
"	background: #BA2147;\n"
"}\n"
"\n"
"#magnetLinkBtn:pressed {\n"
"	background: #EA5177;\n"
"}\n"
"\n"
"#downloadBtn {\n"
"	background: #87"
                        "9300;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#downloadBtn:hover {\n"
"	background: #677300;\n"
"}\n"
"\n"
"#downloadBtn:pressed {\n"
"	background: #97a310;\n"
"}\n"
"\n"
"#urlBtn {\n"
"	background: #387780;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#urlBtn:hover {\n"
"	background: #185760;\n"
"}\n"
"\n"
"#urlBtn:pressed {\n"
"	background: #488790;\n"
"}\n"
"\n"
"#favoriteBtn {\n"
"	background: #663388;\n"
"	border-radius: 6px;\n"
"}\n"
"\n"
"#favoriteBtn:hover {\n"
"	background: #6666BB;\n"
"}\n"
"\n"
"#favoriteBtn:pressed {\n"
"	background: #994444;\n"
"}\n"
"\n"
"#verifiedBtn {\n"
"	background: #000000;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#endOfSearchBtn:pressed {\n"
"	border-radius: 12px;\n"
"	background: #444444;\n"
"}\n"
"\n"
"#filesStack {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#mediaPlayerWidget {\n"
"	margin: 10px 10px;\n"
"	background: #202022;\n"
"	border-radius: 36px;\n"
"}\n"
"\n"
"#mediaProgressFrame QLabel,  #mediaProgressF"
                        "rame QPushButton{\n"
"	font-size: 12px;\n"
"    font-family: \"Helvetica\", sans-serif;\n"
"	padding: 1px 1px;\n"
"}\n"
"\n"
"#mediaProgressFrame {\n"
"	margin: 0px 8px;\n"
"}\n"
"\n"
"#mediaProgressFrame QSlider::groove:horizontal {\n"
"    border: 0px solid #535353;\n"
"    height: 6px;\n"
"    background: #4d4d4d;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"#mediaProgressFrame QSlider::handle:horizontal {\n"
"    background: #a7b308;\n"
"    width: 14px;\n"
"    height: 14px;\n"
"    margin: -6px 0px;\n"
"	border: 2px solid #a7b308;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"#mediaProgressFrame QSlider::handle:horizontal:hover {\n"
"    background: #2e436e;\n"
"	border: 2px solid #656565;\n"
"}\n"
"\n"
"#mediaProgressFrame QSlider::handle:horizontal:pressed {\n"
"    background: #2e436e;\n"
"	border: 2px solid #ff2222;\n"
"}\n"
"\n"
"#mediaProgressFrame QSlider::sub-page:horizontal {\n"
"    background: #a7b308;\n"
"    border: 1px solid #879300;\n"
"    height: 6px;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
""
                        "#mediaProgressFrame QSlider::add-page:horizontal {\n"
"    background: #2b2d30;\n"
"    border: 1px solid #3b3d40;\n"
"    height: 6px;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"#mediaPlayBtn {\n"
"	background: #2b2d30;\n"
"	border-radius: 18px;\n"
"	padding-left: 4px;\n"
"}\n"
"\n"
"#mediaNextBtn {\n"
"	background: #2b2d30;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#mediaPreviousBtn {\n"
"	background: #2b2d30;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#seekForwardBtn {\n"
"	background: #2b2d30;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#seekBackwardBtn {\n"
"	background: #2b2d30;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#mediaRightSideControlFrames QSlider::groove:horizontal {\n"
"    border: 0px solid #535353;\n"
"    height: 6px;\n"
"    background: #4d4d4d;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"#mediaRightSideControlFrames QSlider::handle:horizontal {\n"
"    background: #a7b308;\n"
"    width: 8px;\n"
"    height: 8px;\n"
"    margin: -3px 0px;\n"
"	border: 2px solid #a7b308;\n"
"    border-radius: 6px"
                        ";\n"
"}\n"
"\n"
"#mediaRightSideControlFrames QSlider::handle:horizontal:hover {\n"
"    background: #2e436e;\n"
"	border: 2px solid #656565;\n"
"}\n"
"\n"
"#mediaRightSideControlFrames QSlider::handle:horizontal:pressed {\n"
"    background: #2e436e;\n"
"	border: 2px solid #ff2222;\n"
"}\n"
"\n"
"#mediaRightSideControlFrames QSlider::sub-page:horizontal {\n"
"    background: #a7b308;\n"
"    border: 1px solid #879300;\n"
"    height: 6px;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"#mediaRightSideControlFrames QSlider::add-page:horizontal {\n"
"    background: #2b2d30;\n"
"    border: 1px solid #3b3d40;\n"
"    height: 6px;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"#mediaLeftSideControlFrames QComboBox {\n"
"	padding-left: 4px;\n"
"    color: #dddddd;\n"
"	background: #2b2d30;\n"
"	font-family: \"Segoe UI\";\n"
"	font-size: 10px; \n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"#mediaLeftSideControlFrames QComboBox:hover {\n"
"	border-style: solid; \n"
"	border-radius: 2px; \n"
"}\n"
"\n"
"#mediaButtonsFrame QComboBo"
                        "x:pressed {\n"
"	border-style: solid; \n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"#mediaLeftSideControlFrames QComboBox QAbstractItemView {\n"
"    color: white;\n"
"    background-color: #878389;\n"
"    selection-background-color: #105758; \n"
"    border: none;\n"
"}\n"
"\n"
"#mediaLeftSideControlFrames QComboBox:focus {\n"
"}\n"
"\n"
"#mediaLeftSideControlFrames QComboBox::drop-down:button\n"
"{\n"
"    border: none;\n"
"    padding: 0;\n"
"    width: 0;\n"
"}\n"
"\n"
"#mediaLeftSideControlFrames QPushButton:hover {\n"
"	background: #3b3d40;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#mediaRightSideControlFrames QPushButton:hover {\n"
"	background: #3b3d40;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#mediaLeftSideControlFrames QPushButton:pressed {\n"
"	background: #000000;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#mediaRightSideControlFrames QPushButton:pressed {\n"
"	background: #000000;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#mediaPrimaryControlsFrame QPushButton:hover {\n"
"	background: #4b4d50;\n"
"}\n"
"\n"
""
                        "#mediaPrimaryControlsFrame QPushButton:pressed {\n"
"	background: #000000;\n"
"}\n"
"\n"
"#filesScrollAreaContents {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#eachFileFrame {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#eachFileFrame QLabel {\n"
"	font-size: 12px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#eachFileFrame QPushButton {\n"
"	font-size: 12px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#fileStackTitleBtn {\n"
"	font-size: 18px;\n"
"	color: #dddddd;\n"
"}\n"
"\n"
"#playFileBtn {\n"
"	border-radius: 4px;\n"
"	background: #282828; \n"
"}\n"
"\n"
"#playFileBtn:hover {\n"
"	border-radius: 4px;\n"
"	background: #444444; \n"
"}\n"
"\n"
"#playFileBtn:pressed {\n"
"	border-radius: 4px;\n"
"	background: #111111; \n"
"}\n"
"\n"
"#filesUtilityFrame QComboBox {\n"
"	width: 40px;\n"
"	text-align: center;\n"
"	padding-left: 4px;\n"
"    color: #dddddd;\n"
"	background: #2b2d30;\n"
"	font-family: \"Segoe UI\";\n"
"	font-size: 12px; \n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"#filesUtilityFrame QComboBox:hov"
                        "er {\n"
"	border-style: solid; \n"
"	border-radius: 2px; \n"
"}\n"
"\n"
"#filesUtilityFrame QComboBox:pressed {\n"
"	border-style: solid; \n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"#filesUtilityFrame QComboBox QAbstractItemView {\n"
"    color: white;\n"
"    background-color: #878389;\n"
"    selection-background-color: #105758; \n"
"    border: none;\n"
"}\n"
"\n"
"#filesUtilityFrame QComboBox:focus {\n"
"}\n"
"\n"
"#filesUtilityFrame QComboBox::drop-down:button\n"
"{\n"
"    border: none;\n"
"    padding: 0;\n"
"    width: 0;\n"
"}\n"
"\n"
"#sortByLabel {\n"
"	color: #dddddd;\n"
"	font-size: 12px;\n"
"}\n"
"\n"
"#filesReloadBtn {\n"
"	margin-right: 18px;\n"
"	\n"
"}\n"
"\n"
"#filesReloadBtn:hover {\n"
"	border-radius: 4px;\n"
"	background: #444444; \n"
"}\n"
"\n"
"#filesReloadBtn:pressed {\n"
"	border-radius: 4px;\n"
"	background: #111111; \n"
"}\n"
"\n"
"#endOfFileBtn:pressed {\n"
"	border-radius: 12px;\n"
"	background: #444444;\n"
"}\n"
"\n"
"#scrollAreaContents {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#f"
                        "avoriteItemFrame {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#favoriteNameLabel {\n"
"	font-size: 14px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#favoriteItemFrame QLabel {\n"
"	font-size: 12px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#favoriteItemFrame QPushButton {\n"
"	font-size: 12px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#magnetLinkBtn_2 {\n"
"	background: #DA4167;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#magnetLinkBtn_2:hover {\n"
"	background: #BA2147;\n"
"}\n"
"\n"
"#magnetLinkBtn_2:pressed {\n"
"	background: #EA5177;\n"
"}\n"
"\n"
"#downloadBtn_2 {\n"
"	background: #879300;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#downloadBtn_2:hover {\n"
"	background: #677300;\n"
"}\n"
"\n"
"#downloadBtn_2:pressed {\n"
"	background: #97a310;\n"
"}\n"
"\n"
"#urlBtn_2 {\n"
"	background: #387780;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#urlBtn_2:hover {\n"
"	background: #185760;\n"
"}\n"
"\n"
"#urlBtn_2:pressed {\n"
"	background: #488790;"
                        "\n"
"}\n"
"\n"
"#removeFavoriteBtn {\n"
"	background: #333333;\n"
"	border-radius: 6px;\n"
"}\n"
"\n"
"#removeFavoriteBtn:hover {\n"
"	background: #444444;\n"
"}\n"
"\n"
"#removeFavoriteBtn:pressed {\n"
"	background: #000000;\n"
"}\n"
"\n"
"#verifiedBtn_2 {\n"
"	background: #000000;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#endOfFavoriteBtn:pressed {\n"
"	border-radius: 12px;\n"
"	background: #444444;\n"
"}\n"
"\n"
"#favoritesWidget {\n"
"	background: #2d2d30;\n"
"}\n"
"\n"
"#favoritesScrollAreaWidgetContents {\n"
"	background: #2d2d30;\n"
"}\n"
"\n"
"#favoritesMenuTitleBtn {\n"
"	font-size: 18px;\n"
"	color: #dddddd;\n"
"}\n"
"\n"
"#mediaPlayerShowBtn:checked {\n"
"	background: #000000;\n"
"}\n"
"\n"
"#historyWidget {\n"
"	background: #2d2d30;\n"
"}\n"
"\n"
"#historyNameLabel {\n"
"	font-size: 14px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#historyItemFrame QLabel {\n"
"	font-size: 12px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#historyItemFrame QPushButton {\n"
"	font-size: 12px;\n"
"	color: #fff"
                        "fff;\n"
"}\n"
"\n"
"#historyScrollAreaWidgetContents {\n"
"	background: #2b2d30;\n"
"}\n"
"\n"
"#historyItemFrame {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"\n"
"#historyMenuTitleBtn {\n"
"	font-size: 18px;\n"
"	color: #dddddd;\n"
"}\n"
"\n"
"#historyLinkBtn {\n"
"	background: #DA4167;\n"
"	padding: 1px 2px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"#historyLinkBtn:hover {\n"
"	background: #BA2147;\n"
"}\n"
"\n"
"#historyLinkBtn:pressed {\n"
"	background: #EA5177;\n"
"}\n"
"\n"
"#deleteHistoryBtn {\n"
"	background: #333333;\n"
"	border-radius: 6px;\n"
"}\n"
"\n"
"#deleteHistoryBtn:hover {\n"
"	background: #444444;\n"
"}\n"
"\n"
"#deleteHistoryBtn:pressed {\n"
"	background: #000000;\n"
"}\n"
"\n"
"#endOfHistoryBtn:pressed {\n"
"	border-radius: 12px;\n"
"	background: #444444;\n"
"}\n"
"\n"
"#helpWidget {\n"
"	background: #2d2d30;\n"
"}\n"
"\n"
"#helpLabel {\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#settingWidget {\n"
"	background: #2d2d30;\n"
"}\n"
"\n"
"#settingLeftScrollWidget {\n"
"	background: "
                        "#2d2d30;\n"
"}\n"
"\n"
"#quickSettingsMenuLabel {\n"
"	font-size: 14;\n"
"	color: #dddddd;\n"
"}\n"
"\n"
"#settingLeftScrollWidget QPushButton {\n"
"	font-size: 13px;\n"
"	background: #a7b308;\n"
"	color: 2d2d30;\n"
"	padding: 2px 4px;\n"
"	border-bottom-left-radius: 8px;\n"
"	border-bottom-right-radius: 8px;\n"
"	margin-bottom: 8px;\n"
"}\n"
"\n"
"#settingLeftScrollWidget QPushButton:hover {\n"
"	background: #b7d318;\n"
"}\n"
"\n"
"#settingLeftScrollWidget QPushButton:pressed {\n"
"	background: #97a300;\n"
"}\n"
"\n"
"#settingLeftScrollWidget QLabel {\n"
"	font-size: 13px;\n"
"	background: #222222;\n"
"	color: #dddddd;\n"
"	padding: 2px 4px;\n"
"	border-top-left-radius: 8px;\n"
"	border-top-right-radius: 8px;\n"
"	margin-top: 8px;\n"
"}\n"
"\n"
"#settingsWidget {\n"
"	background: #2d2d30;\n"
"}\n"
"\n"
"#settingsRightScrollArea {\n"
"	background: #2d2d30;\n"
"	border-radius: 20px;\n"
"}\n"
"\n"
"#settingsRightScrollWidget {\n"
"	background: #353539;\n"
"	border-radius: 20px;\n"
"}\n"
"\n"
"#settingsRightScrol"
                        "lWidget QLabel {\n"
"	color: #dddddd;\n"
"}\n"
"\n"
"#initAppWidget {\n"
"	background: #2d2d30;\n"
"}\n"
"\n"
"#initIcon {\n"
"    background-image: url(:/icons/loader-dark.gif);\n"
"}\n"
"\n"
"#label {\n"
"	color: #dddddd;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.headerContainer = QWidget(self.centralwidget)
        self.headerContainer.setObjectName(u"headerContainer")
        self.verticalLayout = QVBoxLayout(self.headerContainer)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QWidget(self.headerContainer)
        self.header.setObjectName(u"header")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.header)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.appIconTitleFrame = QFrame(self.header)
        self.appIconTitleFrame.setObjectName(u"appIconTitleFrame")
        self.appIconTitleFrame.setFrameShape(QFrame.StyledPanel)
        self.appIconTitleFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.appIconTitleFrame)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(4, 0, 6, 0)
        self.appIconBtn = QToolButton(self.appIconTitleFrame)
        self.appIconBtn.setObjectName(u"appIconBtn")
        self.appIconBtn.setMinimumSize(QSize(24, 24))
        icon = QIcon()
        icon.addFile(u":/icons/icons/activity.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.appIconBtn.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.appIconBtn)

        self.appTitleBtn = QPushButton(self.appIconTitleFrame)
        self.appTitleBtn.setObjectName(u"appTitleBtn")
        self.appTitleBtn.setMinimumSize(QSize(82, 0))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(True)
        self.appTitleBtn.setFont(font)

        self.horizontalLayout_4.addWidget(self.appTitleBtn)


        self.horizontalLayout_2.addWidget(self.appIconTitleFrame, 0, Qt.AlignLeft)

        self.headerSpacerLeft = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.headerSpacerLeft)

        self.netSpeedFrame = QFrame(self.header)
        self.netSpeedFrame.setObjectName(u"netSpeedFrame")
        self.netSpeedFrame.setFrameShape(QFrame.StyledPanel)
        self.netSpeedFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.netSpeedFrame)
        self.horizontalLayout_9.setSpacing(9)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(9, 9, 9, 9)
        self.netSpeedBtn = QPushButton(self.netSpeedFrame)
        self.netSpeedBtn.setObjectName(u"netSpeedBtn")
        self.netSpeedBtn.setMinimumSize(QSize(64, 0))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        self.netSpeedBtn.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/cil-speedometer.png", QSize(), QIcon.Normal, QIcon.Off)
        self.netSpeedBtn.setIcon(icon1)
        self.netSpeedBtn.setIconSize(QSize(14, 14))

        self.horizontalLayout_9.addWidget(self.netSpeedBtn)


        self.horizontalLayout_2.addWidget(self.netSpeedFrame, 0, Qt.AlignRight)

        self.someMoreBtnFrame = QFrame(self.header)
        self.someMoreBtnFrame.setObjectName(u"someMoreBtnFrame")
        self.someMoreBtnFrame.setFrameShape(QFrame.StyledPanel)
        self.someMoreBtnFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.someMoreBtnFrame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.headerSpacerMid = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.headerSpacerMid)

        self.themeBtn = QToolButton(self.someMoreBtnFrame)
        self.themeBtn.setObjectName(u"themeBtn")
        self.themeBtn.setMinimumSize(QSize(24, 24))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/cil-lightbulb.png", QSize(), QIcon.Normal, QIcon.Off)
        self.themeBtn.setIcon(icon2)

        self.horizontalLayout_8.addWidget(self.themeBtn)

        self.notificationBtn = QToolButton(self.someMoreBtnFrame)
        self.notificationBtn.setObjectName(u"notificationBtn")
        self.notificationBtn.setMinimumSize(QSize(24, 24))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/cil-bell.png", QSize(), QIcon.Normal, QIcon.Off)
        self.notificationBtn.setIcon(icon3)

        self.horizontalLayout_8.addWidget(self.notificationBtn)

        self.settingsBtn = QToolButton(self.someMoreBtnFrame)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setMinimumSize(QSize(24, 24))
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/cil-settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsBtn.setIcon(icon4)

        self.horizontalLayout_8.addWidget(self.settingsBtn)

        self.headerSpacerRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.headerSpacerRight)


        self.horizontalLayout_2.addWidget(self.someMoreBtnFrame, 0, Qt.AlignRight)

        self.appControlFrame = QFrame(self.header)
        self.appControlFrame.setObjectName(u"appControlFrame")
        self.horizontalLayout = QHBoxLayout(self.appControlFrame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.appMinBtn = QToolButton(self.appControlFrame)
        self.appMinBtn.setObjectName(u"appMinBtn")
        self.appMinBtn.setMinimumSize(QSize(28, 28))
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.appMinBtn.setIcon(icon5)

        self.horizontalLayout.addWidget(self.appMinBtn)

        self.appMaxBtn = QToolButton(self.appControlFrame)
        self.appMaxBtn.setObjectName(u"appMaxBtn")
        self.appMaxBtn.setMinimumSize(QSize(28, 28))
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.appMaxBtn.setIcon(icon6)

        self.horizontalLayout.addWidget(self.appMaxBtn)

        self.appCloseBtn = QToolButton(self.appControlFrame)
        self.appCloseBtn.setObjectName(u"appCloseBtn")
        self.appCloseBtn.setMinimumSize(QSize(28, 28))
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.appCloseBtn.setIcon(icon7)

        self.horizontalLayout.addWidget(self.appCloseBtn)


        self.horizontalLayout_2.addWidget(self.appControlFrame, 0, Qt.AlignRight)


        self.verticalLayout.addWidget(self.header, 0, Qt.AlignTop)


        self.verticalLayout_2.addWidget(self.headerContainer, 0, Qt.AlignTop)

        self.mainContainer = QWidget(self.centralwidget)
        self.mainContainer.setObjectName(u"mainContainer")
        self.mainContainer.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_3 = QHBoxLayout(self.mainContainer)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBar = QFrame(self.mainContainer)
        self.leftMenuBar.setObjectName(u"leftMenuBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftMenuBar.sizePolicy().hasHeightForWidth())
        self.leftMenuBar.setSizePolicy(sizePolicy1)
        self.leftMenuBar.setMaximumSize(QSize(3600, 16777215))
        self.verticalLayout_6 = QVBoxLayout(self.leftMenuBar)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.topBtnWidget = QWidget(self.leftMenuBar)
        self.topBtnWidget.setObjectName(u"topBtnWidget")
        self.verticalLayout_4 = QVBoxLayout(self.topBtnWidget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 4)
        self.pushButton = QPushButton(self.topBtnWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 32))
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/cil-menu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon8)
        self.pushButton.setAutoDefault(False)

        self.verticalLayout_4.addWidget(self.pushButton)


        self.verticalLayout_6.addWidget(self.topBtnWidget)

        self.mainBtnWidget = QWidget(self.leftMenuBar)
        self.mainBtnWidget.setObjectName(u"mainBtnWidget")
        sizePolicy1.setHeightForWidth(self.mainBtnWidget.sizePolicy().hasHeightForWidth())
        self.mainBtnWidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_3 = QVBoxLayout(self.mainBtnWidget)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.mainBtnWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 32))
        icon9 = QIcon()
        icon9.addFile(u":/icons/icons/cil-magnifying-glass.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon9)

        self.verticalLayout_3.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.mainBtnWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 32))
        icon10 = QIcon()
        icon10.addFile(u":/icons/icons/cil-data-transfer-down.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon10)

        self.verticalLayout_3.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.mainBtnWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(0, 32))
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/cil-file.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_4.setIcon(icon11)

        self.verticalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_12 = QPushButton(self.mainBtnWidget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setMinimumSize(QSize(0, 32))
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/cil-heart.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_12.setIcon(icon12)

        self.verticalLayout_3.addWidget(self.pushButton_12)

        self.pushButton_5 = QPushButton(self.mainBtnWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(0, 32))
        self.pushButton_5.setBaseSize(QSize(0, 0))
        icon13 = QIcon()
        icon13.addFile(u":/icons/icons/cil-history.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon13)

        self.verticalLayout_3.addWidget(self.pushButton_5)


        self.verticalLayout_6.addWidget(self.mainBtnWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.bottomBtnWidget = QWidget(self.leftMenuBar)
        self.bottomBtnWidget.setObjectName(u"bottomBtnWidget")
        self.bottomBtnWidget.setMinimumSize(QSize(0, 0))
        self.verticalLayout_5 = QVBoxLayout(self.bottomBtnWidget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 6)
        self.pushButton_7 = QPushButton(self.bottomBtnWidget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setMinimumSize(QSize(0, 32))
        self.pushButton_7.setIcon(icon4)

        self.verticalLayout_5.addWidget(self.pushButton_7)

        self.pushButton_6 = QPushButton(self.bottomBtnWidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(0, 32))
        icon14 = QIcon()
        icon14.addFile(u":/icons/icons/cil-comment-bubble.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon14)

        self.verticalLayout_5.addWidget(self.pushButton_6)


        self.verticalLayout_6.addWidget(self.bottomBtnWidget)


        self.horizontalLayout_3.addWidget(self.leftMenuBar)

        self.centerMainMenu = QWidget(self.mainContainer)
        self.centerMainMenu.setObjectName(u"centerMainMenu")
        self.verticalLayout_7 = QVBoxLayout(self.centerMainMenu)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.mainStack = QStackedWidget(self.centerMainMenu)
        self.mainStack.setObjectName(u"mainStack")
        self.searchStack = QWidget()
        self.searchStack.setObjectName(u"searchStack")
        self.verticalLayout_9 = QVBoxLayout(self.searchStack)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.searchWidget = QWidget(self.searchStack)
        self.searchWidget.setObjectName(u"searchWidget")
        self.verticalLayout_12 = QVBoxLayout(self.searchWidget)
        self.verticalLayout_12.setSpacing(4)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(4, 4, 4, 2)
        self.searchArea = QWidget(self.searchWidget)
        self.searchArea.setObjectName(u"searchArea")
        self.horizontalLayout_12 = QHBoxLayout(self.searchArea)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.searchInputText = QLineEdit(self.searchArea)
        self.searchInputText.setObjectName(u"searchInputText")
        self.searchInputText.setMinimumSize(QSize(0, 28))

        self.horizontalLayout_12.addWidget(self.searchInputText)

        self.searchBtn = QPushButton(self.searchArea)
        self.searchBtn.setObjectName(u"searchBtn")
        self.searchBtn.setMinimumSize(QSize(80, 28))
        icon15 = QIcon()
        icon15.addFile(u":/icons/icons/search.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.searchBtn.setIcon(icon15)
        self.searchBtn.setIconSize(QSize(24, 24))

        self.horizontalLayout_12.addWidget(self.searchBtn)


        self.verticalLayout_12.addWidget(self.searchArea)

        self.searchScrollArea = QScrollArea(self.searchWidget)
        self.searchScrollArea.setObjectName(u"searchScrollArea")
        self.searchScrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QWidget()
        self.scrollAreaContents.setObjectName(u"scrollAreaContents")
        self.scrollAreaContents.setGeometry(QRect(0, 0, 559, 728))
        self.verticalLayout_13 = QVBoxLayout(self.scrollAreaContents)
        self.verticalLayout_13.setSpacing(4)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.searchOutputFrame = QFrame(self.scrollAreaContents)
        self.searchOutputFrame.setObjectName(u"searchOutputFrame")
        self.searchOutputFrame.setMinimumSize(QSize(0, 100))
        self.searchOutputFrame.setStyleSheet(u"")
        self.searchOutputFrame.setFrameShape(QFrame.StyledPanel)
        self.searchOutputFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.searchOutputFrame)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.resultNameLabel = QLabel(self.searchOutputFrame)
        self.resultNameLabel.setObjectName(u"resultNameLabel")
        self.resultNameLabel.setFont(font)

        self.verticalLayout_14.addWidget(self.resultNameLabel)

        self.searchOutputInfoFrame1 = QFrame(self.searchOutputFrame)
        self.searchOutputInfoFrame1.setObjectName(u"searchOutputInfoFrame1")
        self.searchOutputInfoFrame1.setMaximumSize(QSize(16777215, 16))
        self.searchOutputInfoFrame1.setFrameShape(QFrame.StyledPanel)
        self.searchOutputInfoFrame1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.searchOutputInfoFrame1)
        self.horizontalLayout_13.setSpacing(16)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.resultSeederLabel = QLabel(self.searchOutputInfoFrame1)
        self.resultSeederLabel.setObjectName(u"resultSeederLabel")
        self.resultSeederLabel.setMinimumSize(QSize(72, 0))

        self.horizontalLayout_13.addWidget(self.resultSeederLabel)

        self.resultLeecherLabel = QLabel(self.searchOutputInfoFrame1)
        self.resultLeecherLabel.setObjectName(u"resultLeecherLabel")
        self.resultLeecherLabel.setMinimumSize(QSize(72, 0))

        self.horizontalLayout_13.addWidget(self.resultLeecherLabel)

        self.resultSizeLabel = QLabel(self.searchOutputInfoFrame1)
        self.resultSizeLabel.setObjectName(u"resultSizeLabel")
        self.resultSizeLabel.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_13.addWidget(self.resultSizeLabel)

        self.nsfwLabel = QLabel(self.searchOutputInfoFrame1)
        self.nsfwLabel.setObjectName(u"nsfwLabel")
        self.nsfwLabel.setMinimumSize(QSize(36, 0))

        self.horizontalLayout_13.addWidget(self.nsfwLabel)


        self.verticalLayout_14.addWidget(self.searchOutputInfoFrame1, 0, Qt.AlignLeft)

        self.searchOutputInfoFrame2 = QFrame(self.searchOutputFrame)
        self.searchOutputInfoFrame2.setObjectName(u"searchOutputInfoFrame2")
        self.searchOutputInfoFrame2.setMaximumSize(QSize(16777215, 16))
        self.searchOutputInfoFrame2.setFrameShape(QFrame.StyledPanel)
        self.searchOutputInfoFrame2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.searchOutputInfoFrame2)
        self.horizontalLayout_14.setSpacing(16)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.resultAgeLabel = QLabel(self.searchOutputInfoFrame2)
        self.resultAgeLabel.setObjectName(u"resultAgeLabel")

        self.horizontalLayout_14.addWidget(self.resultAgeLabel)

        self.resultSiteLabel = QLabel(self.searchOutputInfoFrame2)
        self.resultSiteLabel.setObjectName(u"resultSiteLabel")

        self.horizontalLayout_14.addWidget(self.resultSiteLabel)

        self.resultTypeLabel = QLabel(self.searchOutputInfoFrame2)
        self.resultTypeLabel.setObjectName(u"resultTypeLabel")
        self.resultTypeLabel.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_14.addWidget(self.resultTypeLabel)


        self.verticalLayout_14.addWidget(self.searchOutputInfoFrame2, 0, Qt.AlignLeft)

        self.searchOutputBtnsFrame = QFrame(self.searchOutputFrame)
        self.searchOutputBtnsFrame.setObjectName(u"searchOutputBtnsFrame")
        self.searchOutputBtnsFrame.setMinimumSize(QSize(0, 0))
        self.searchOutputBtnsFrame.setMaximumSize(QSize(16777215, 18))
        self.searchOutputBtnsFrame.setFrameShape(QFrame.StyledPanel)
        self.searchOutputBtnsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.searchOutputBtnsFrame)
        self.horizontalLayout_15.setSpacing(16)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.favoriteBtn = QToolButton(self.searchOutputBtnsFrame)
        self.favoriteBtn.setObjectName(u"favoriteBtn")
        self.favoriteBtn.setMinimumSize(QSize(0, 0))
        self.favoriteBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon16 = QIcon()
        icon16.addFile(u":/icons/icons/heart.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.favoriteBtn.setIcon(icon16)

        self.horizontalLayout_15.addWidget(self.favoriteBtn)

        self.magnetLinkBtn = QPushButton(self.searchOutputBtnsFrame)
        self.magnetLinkBtn.setObjectName(u"magnetLinkBtn")
        self.magnetLinkBtn.setMinimumSize(QSize(58, 0))
        self.magnetLinkBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon17 = QIcon()
        icon17.addFile(u":/icons/icons/cil-link.png", QSize(), QIcon.Normal, QIcon.Off)
        self.magnetLinkBtn.setIcon(icon17)
        self.magnetLinkBtn.setIconSize(QSize(10, 10))

        self.horizontalLayout_15.addWidget(self.magnetLinkBtn)

        self.downloadBtn = QPushButton(self.searchOutputBtnsFrame)
        self.downloadBtn.setObjectName(u"downloadBtn")
        self.downloadBtn.setMinimumSize(QSize(68, 0))
        self.downloadBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadBtn.setIcon(icon10)
        self.downloadBtn.setIconSize(QSize(10, 10))

        self.horizontalLayout_15.addWidget(self.downloadBtn)

        self.urlBtn = QPushButton(self.searchOutputBtnsFrame)
        self.urlBtn.setObjectName(u"urlBtn")
        self.urlBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon18 = QIcon()
        icon18.addFile(u":/icons/icons/cil-link-alt.png", QSize(), QIcon.Normal, QIcon.Off)
        self.urlBtn.setIcon(icon18)
        self.urlBtn.setIconSize(QSize(10, 10))

        self.horizontalLayout_15.addWidget(self.urlBtn)

        self.verifiedBtn = QPushButton(self.searchOutputBtnsFrame)
        self.verifiedBtn.setObjectName(u"verifiedBtn")
        icon19 = QIcon()
        icon19.addFile(u":/icons/icons/cil-check-alt.png", QSize(), QIcon.Normal, QIcon.Off)
        self.verifiedBtn.setIcon(icon19)
        self.verifiedBtn.setIconSize(QSize(10, 10))

        self.horizontalLayout_15.addWidget(self.verifiedBtn)


        self.verticalLayout_14.addWidget(self.searchOutputBtnsFrame, 0, Qt.AlignLeft)


        self.verticalLayout_13.addWidget(self.searchOutputFrame)

        self.frame_2 = QFrame(self.scrollAreaContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 100))
        self.frame_2.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.verticalLayout_13.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.scrollAreaContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 100))
        self.frame_3.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.verticalLayout_13.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.scrollAreaContents)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 100))
        self.frame_4.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.verticalLayout_13.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.scrollAreaContents)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 100))
        self.frame_5.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)

        self.verticalLayout_13.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.scrollAreaContents)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 100))
        self.frame_6.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}\n"
"")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.verticalLayout_13.addWidget(self.frame_6)

        self.endOfSearchBtn = QPushButton(self.scrollAreaContents)
        self.endOfSearchBtn.setObjectName(u"endOfSearchBtn")
        self.endOfSearchBtn.setMinimumSize(QSize(0, 100))

        self.verticalLayout_13.addWidget(self.endOfSearchBtn)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_2)

        self.searchScrollArea.setWidget(self.scrollAreaContents)

        self.verticalLayout_12.addWidget(self.searchScrollArea)


        self.verticalLayout_9.addWidget(self.searchWidget)

        self.mainStack.addWidget(self.searchStack)
        self.downloadStack = QWidget()
        self.downloadStack.setObjectName(u"downloadStack")
        self.verticalLayout_15 = QVBoxLayout(self.downloadStack)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.downloadStack)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"* {\n"
"	background: #2b2d30;\n"
"}")
        self.verticalLayout_41 = QVBoxLayout(self.widget)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout_41.addWidget(self.label)


        self.verticalLayout_15.addWidget(self.widget)

        self.mainStack.addWidget(self.downloadStack)
        self.filesStack = QWidget()
        self.filesStack.setObjectName(u"filesStack")
        self.verticalLayout_16 = QVBoxLayout(self.filesStack)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.filesStackWidget = QWidget(self.filesStack)
        self.filesStackWidget.setObjectName(u"filesStackWidget")
        self.filesStackWidget.setStyleSheet(u"")
        self.verticalLayout_17 = QVBoxLayout(self.filesStackWidget)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.filesWidget = QWidget(self.filesStackWidget)
        self.filesWidget.setObjectName(u"filesWidget")
        self.verticalLayout_21 = QVBoxLayout(self.filesWidget)
        self.verticalLayout_21.setSpacing(4)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(4, 4, 4, 2)
        self.filesUtilityFrame = QFrame(self.filesWidget)
        self.filesUtilityFrame.setObjectName(u"filesUtilityFrame")
        self.filesUtilityFrame.setMinimumSize(QSize(0, 20))
        self.filesUtilityFrame.setFrameShape(QFrame.StyledPanel)
        self.filesUtilityFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.filesUtilityFrame)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.fileStackTitleBtn = QPushButton(self.filesUtilityFrame)
        self.fileStackTitleBtn.setObjectName(u"fileStackTitleBtn")
        self.fileStackTitleBtn.setFont(font)

        self.horizontalLayout_24.addWidget(self.fileStackTitleBtn, 0, Qt.AlignLeft)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer)

        self.filesReloadBtn = QPushButton(self.filesUtilityFrame)
        self.filesReloadBtn.setObjectName(u"filesReloadBtn")
        self.filesReloadBtn.setMaximumSize(QSize(38, 16777215))
        icon20 = QIcon()
        icon20.addFile(u":/icons/icons/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.filesReloadBtn.setIcon(icon20)
        self.filesReloadBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_24.addWidget(self.filesReloadBtn)

        self.sortByLabel = QLabel(self.filesUtilityFrame)
        self.sortByLabel.setObjectName(u"sortByLabel")

        self.horizontalLayout_24.addWidget(self.sortByLabel, 0, Qt.AlignRight)

        self.filesSortComboBox = QComboBox(self.filesUtilityFrame)
        self.filesSortComboBox.addItem("")
        self.filesSortComboBox.addItem("")
        self.filesSortComboBox.addItem("")
        self.filesSortComboBox.addItem("")
        self.filesSortComboBox.setObjectName(u"filesSortComboBox")
        self.filesSortComboBox.setMinimumSize(QSize(32, 0))

        self.horizontalLayout_24.addWidget(self.filesSortComboBox, 0, Qt.AlignRight)


        self.verticalLayout_21.addWidget(self.filesUtilityFrame)

        self.filesScrollArea = QScrollArea(self.filesWidget)
        self.filesScrollArea.setObjectName(u"filesScrollArea")
        self.filesScrollArea.setWidgetResizable(True)
        self.filesScrollAreaContents = QWidget()
        self.filesScrollAreaContents.setObjectName(u"filesScrollAreaContents")
        self.filesScrollAreaContents.setGeometry(QRect(0, 0, 559, 624))
        self.filesScrollAreaContents.setStyleSheet(u"#filesScrollAreaContents QFrames {\n"
"	background: #111111;\n"
"}")
        self.verticalLayout_22 = QVBoxLayout(self.filesScrollAreaContents)
        self.verticalLayout_22.setSpacing(4)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.eachFileFrame = QFrame(self.filesScrollAreaContents)
        self.eachFileFrame.setObjectName(u"eachFileFrame")
        self.eachFileFrame.setMinimumSize(QSize(0, 100))
        self.eachFileFrame.setStyleSheet(u"")
        self.eachFileFrame.setFrameShape(QFrame.StyledPanel)
        self.eachFileFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.eachFileFrame)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.fileNameLabel = QLabel(self.eachFileFrame)
        self.fileNameLabel.setObjectName(u"fileNameLabel")
        self.fileNameLabel.setFont(font)

        self.verticalLayout_25.addWidget(self.fileNameLabel)

        self.frame_9 = QFrame(self.eachFileFrame)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMaximumSize(QSize(16777215, 16))
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_21.setSpacing(20)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(30, 0, 0, 0)
        self.label_2 = QLabel(self.frame_9)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_21.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_9)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_21.addWidget(self.label_3)


        self.verticalLayout_25.addWidget(self.frame_9)

        self.frame_16 = QFrame(self.eachFileFrame)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.playFileBtn = QPushButton(self.frame_16)
        self.playFileBtn.setObjectName(u"playFileBtn")
        self.playFileBtn.setMaximumSize(QSize(24, 16777215))
        icon21 = QIcon()
        icon21.addFile(u":/icons/icons/play.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon21.addFile(u":/icons/icons/help-circle.svg", QSize(), QIcon.Disabled, QIcon.Off)
        self.playFileBtn.setIcon(icon21)
        self.playFileBtn.setIconSize(QSize(24, 24))

        self.horizontalLayout_23.addWidget(self.playFileBtn)

        self.frame_15 = QFrame(self.frame_16)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMaximumSize(QSize(16777215, 16))
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_22.setSpacing(20)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.frame_15)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_22.addWidget(self.label_4)

        self.label_5 = QLabel(self.frame_15)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_22.addWidget(self.label_5)


        self.horizontalLayout_23.addWidget(self.frame_15)


        self.verticalLayout_25.addWidget(self.frame_16)


        self.verticalLayout_22.addWidget(self.eachFileFrame)

        self.frame_10 = QFrame(self.filesScrollAreaContents)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 100))
        self.frame_10.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)

        self.verticalLayout_22.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.filesScrollAreaContents)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 100))
        self.frame_11.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)

        self.verticalLayout_22.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.filesScrollAreaContents)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 100))
        self.frame_12.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)

        self.verticalLayout_22.addWidget(self.frame_12)

        self.frame_14 = QFrame(self.filesScrollAreaContents)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(0, 100))
        self.frame_14.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)

        self.verticalLayout_22.addWidget(self.frame_14)

        self.endOfFileBtn = QPushButton(self.filesScrollAreaContents)
        self.endOfFileBtn.setObjectName(u"endOfFileBtn")
        self.endOfFileBtn.setMinimumSize(QSize(0, 100))

        self.verticalLayout_22.addWidget(self.endOfFileBtn)

        self.verticalSpacer_3 = QSpacerItem(20, 27, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_3)

        self.filesScrollArea.setWidget(self.filesScrollAreaContents)

        self.verticalLayout_21.addWidget(self.filesScrollArea)

        self.videoOutputFrame = QFrame(self.filesWidget)
        self.videoOutputFrame.setObjectName(u"videoOutputFrame")
        self.videoOutputFrame.setFrameShape(QFrame.StyledPanel)
        self.videoOutputFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_24 = QVBoxLayout(self.videoOutputFrame)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_21.addWidget(self.videoOutputFrame)


        self.verticalLayout_17.addWidget(self.filesWidget)

        self.mediaPlayerWidget = QFrame(self.filesStackWidget)
        self.mediaPlayerWidget.setObjectName(u"mediaPlayerWidget")
        self.mediaPlayerWidget.setMinimumSize(QSize(0, 0))
        self.mediaPlayerWidget.setMaximumSize(QSize(16777215, 100))
        self.mediaPlayerWidget.setStyleSheet(u"")
        self.verticalLayout_18 = QVBoxLayout(self.mediaPlayerWidget)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.mediaPlayerFrame1 = QFrame(self.mediaPlayerWidget)
        self.mediaPlayerFrame1.setObjectName(u"mediaPlayerFrame1")
        self.mediaPlayerFrame1.setFrameShape(QFrame.StyledPanel)
        self.mediaPlayerFrame1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.mediaPlayerFrame1)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.mediaPlayerFrame2 = QFrame(self.mediaPlayerFrame1)
        self.mediaPlayerFrame2.setObjectName(u"mediaPlayerFrame2")
        self.mediaPlayerFrame2.setFrameShape(QFrame.StyledPanel)
        self.mediaPlayerFrame2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.mediaPlayerFrame2)
        self.verticalLayout_19.setSpacing(4)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(-1, 10, 10, 10)
        self.mediaProgressFrame = QFrame(self.mediaPlayerFrame2)
        self.mediaProgressFrame.setObjectName(u"mediaProgressFrame")
        self.mediaProgressFrame.setMaximumSize(QSize(16777215, 20))
        self.mediaProgressFrame.setFrameShape(QFrame.StyledPanel)
        self.mediaProgressFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.mediaProgressFrame)
        self.horizontalLayout_16.setSpacing(12)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.currentPlayingBtn = QPushButton(self.mediaProgressFrame)
        self.currentPlayingBtn.setObjectName(u"currentPlayingBtn")

        self.horizontalLayout_16.addWidget(self.currentPlayingBtn)

        self.mediaProgressSlider = QSlider(self.mediaProgressFrame)
        self.mediaProgressSlider.setObjectName(u"mediaProgressSlider")
        self.mediaProgressSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_16.addWidget(self.mediaProgressSlider)

        self.remainingMediaBtn = QPushButton(self.mediaProgressFrame)
        self.remainingMediaBtn.setObjectName(u"remainingMediaBtn")

        self.horizontalLayout_16.addWidget(self.remainingMediaBtn)


        self.verticalLayout_19.addWidget(self.mediaProgressFrame)

        self.mediaControlFrame = QFrame(self.mediaPlayerFrame2)
        self.mediaControlFrame.setObjectName(u"mediaControlFrame")
        sizePolicy1.setHeightForWidth(self.mediaControlFrame.sizePolicy().hasHeightForWidth())
        self.mediaControlFrame.setSizePolicy(sizePolicy1)
        self.mediaControlFrame.setFrameShape(QFrame.StyledPanel)
        self.mediaControlFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.mediaControlFrame)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.mediaLeftSideControlFrames = QFrame(self.mediaControlFrame)
        self.mediaLeftSideControlFrames.setObjectName(u"mediaLeftSideControlFrames")
        sizePolicy.setHeightForWidth(self.mediaLeftSideControlFrames.sizePolicy().hasHeightForWidth())
        self.mediaLeftSideControlFrames.setSizePolicy(sizePolicy)
        self.mediaLeftSideControlFrames.setFrameShape(QFrame.StyledPanel)
        self.mediaLeftSideControlFrames.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.mediaLeftSideControlFrames)
        self.horizontalLayout_20.setSpacing(10)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, 0, 0, 0)
        self.mediaFolderBtn = QPushButton(self.mediaLeftSideControlFrames)
        self.mediaFolderBtn.setObjectName(u"mediaFolderBtn")
        self.mediaFolderBtn.setMinimumSize(QSize(0, 20))
        icon22 = QIcon()
        icon22.addFile(u":/icons/icons/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaFolderBtn.setIcon(icon22)

        self.horizontalLayout_20.addWidget(self.mediaFolderBtn)

        self.playerLockBtn = QPushButton(self.mediaLeftSideControlFrames)
        self.playerLockBtn.setObjectName(u"playerLockBtn")
        self.playerLockBtn.setMinimumSize(QSize(0, 20))
        icon23 = QIcon()
        icon23.addFile(u":/icons/icons/cil-lock-locked.png", QSize(), QIcon.Normal, QIcon.Off)
        self.playerLockBtn.setIcon(icon23)

        self.horizontalLayout_20.addWidget(self.playerLockBtn)

        self.playbackSpeedCombobox = QComboBox(self.mediaLeftSideControlFrames)
        self.playbackSpeedCombobox.addItem("")
        self.playbackSpeedCombobox.addItem("")
        self.playbackSpeedCombobox.addItem("")
        self.playbackSpeedCombobox.addItem("")
        self.playbackSpeedCombobox.addItem("")
        self.playbackSpeedCombobox.addItem("")
        self.playbackSpeedCombobox.setObjectName(u"playbackSpeedCombobox")
        self.playbackSpeedCombobox.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_20.addWidget(self.playbackSpeedCombobox)

        self.playerUndockBtn = QPushButton(self.mediaLeftSideControlFrames)
        self.playerUndockBtn.setObjectName(u"playerUndockBtn")
        self.playerUndockBtn.setMinimumSize(QSize(0, 20))
        icon24 = QIcon()
        icon24.addFile(u":/icons/icons/cil-input.png", QSize(), QIcon.Normal, QIcon.Off)
        self.playerUndockBtn.setIcon(icon24)
        self.playerUndockBtn.setIconSize(QSize(16, 16))

        self.horizontalLayout_20.addWidget(self.playerUndockBtn)

        self.mediaStopBtn = QPushButton(self.mediaLeftSideControlFrames)
        self.mediaStopBtn.setObjectName(u"mediaStopBtn")
        self.mediaStopBtn.setMinimumSize(QSize(0, 20))
        icon25 = QIcon()
        icon25.addFile(u":/icons/icons/cil-media-stop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaStopBtn.setIcon(icon25)

        self.horizontalLayout_20.addWidget(self.mediaStopBtn)


        self.horizontalLayout_17.addWidget(self.mediaLeftSideControlFrames, 0, Qt.AlignLeft)

        self.mediaPrimaryControlsFrame = QFrame(self.mediaControlFrame)
        self.mediaPrimaryControlsFrame.setObjectName(u"mediaPrimaryControlsFrame")
        sizePolicy1.setHeightForWidth(self.mediaPrimaryControlsFrame.sizePolicy().hasHeightForWidth())
        self.mediaPrimaryControlsFrame.setSizePolicy(sizePolicy1)
        self.horizontalLayout_18 = QHBoxLayout(self.mediaPrimaryControlsFrame)
        self.horizontalLayout_18.setSpacing(8)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.seekBackwardBtn = QPushButton(self.mediaPrimaryControlsFrame)
        self.seekBackwardBtn.setObjectName(u"seekBackwardBtn")
        self.seekBackwardBtn.setMinimumSize(QSize(24, 24))
        icon26 = QIcon()
        icon26.addFile(u":/icons/icons/cil-media-skip-backward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.seekBackwardBtn.setIcon(icon26)
        self.seekBackwardBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_18.addWidget(self.seekBackwardBtn)

        self.mediaPreviousBtn = QPushButton(self.mediaPrimaryControlsFrame)
        self.mediaPreviousBtn.setObjectName(u"mediaPreviousBtn")
        self.mediaPreviousBtn.setMinimumSize(QSize(24, 24))
        icon27 = QIcon()
        icon27.addFile(u":/icons/icons/cil-media-step-backward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaPreviousBtn.setIcon(icon27)
        self.mediaPreviousBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_18.addWidget(self.mediaPreviousBtn)

        self.mediaPlayBtn = QPushButton(self.mediaPrimaryControlsFrame)
        self.mediaPlayBtn.setObjectName(u"mediaPlayBtn")
        self.mediaPlayBtn.setMinimumSize(QSize(36, 36))
        icon28 = QIcon()
        icon28.addFile(u":/icons/icons/play.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaPlayBtn.setIcon(icon28)
        self.mediaPlayBtn.setIconSize(QSize(28, 28))

        self.horizontalLayout_18.addWidget(self.mediaPlayBtn)

        self.mediaNextBtn = QPushButton(self.mediaPrimaryControlsFrame)
        self.mediaNextBtn.setObjectName(u"mediaNextBtn")
        self.mediaNextBtn.setMinimumSize(QSize(24, 24))
        icon29 = QIcon()
        icon29.addFile(u":/icons/icons/cil-media-step-forward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaNextBtn.setIcon(icon29)
        self.mediaNextBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_18.addWidget(self.mediaNextBtn)

        self.seekForwardBtn = QPushButton(self.mediaPrimaryControlsFrame)
        self.seekForwardBtn.setObjectName(u"seekForwardBtn")
        self.seekForwardBtn.setMinimumSize(QSize(24, 24))
        icon30 = QIcon()
        icon30.addFile(u":/icons/icons/cil-media-skip-forward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.seekForwardBtn.setIcon(icon30)
        self.seekForwardBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_18.addWidget(self.seekForwardBtn)


        self.horizontalLayout_17.addWidget(self.mediaPrimaryControlsFrame, 0, Qt.AlignHCenter)

        self.mediaRightSideControlFrames = QFrame(self.mediaControlFrame)
        self.mediaRightSideControlFrames.setObjectName(u"mediaRightSideControlFrames")
        sizePolicy.setHeightForWidth(self.mediaRightSideControlFrames.sizePolicy().hasHeightForWidth())
        self.mediaRightSideControlFrames.setSizePolicy(sizePolicy)
        self.mediaRightSideControlFrames.setFrameShape(QFrame.StyledPanel)
        self.mediaRightSideControlFrames.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.mediaRightSideControlFrames)
        self.horizontalLayout_19.setSpacing(2)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, -1, 0)
        self.mediaRepeatBtn = QPushButton(self.mediaRightSideControlFrames)
        self.mediaRepeatBtn.setObjectName(u"mediaRepeatBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mediaRepeatBtn.sizePolicy().hasHeightForWidth())
        self.mediaRepeatBtn.setSizePolicy(sizePolicy2)
        self.mediaRepeatBtn.setMinimumSize(QSize(0, 20))
        icon31 = QIcon()
        icon31.addFile(u":/icons/icons/cil-loop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaRepeatBtn.setIcon(icon31)

        self.horizontalLayout_19.addWidget(self.mediaRepeatBtn)

        self.mediaShuffleBtn = QPushButton(self.mediaRightSideControlFrames)
        self.mediaShuffleBtn.setObjectName(u"mediaShuffleBtn")
        self.mediaShuffleBtn.setMinimumSize(QSize(0, 20))
        icon32 = QIcon()
        icon32.addFile(u":/icons/icons/cil-infinity.png", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaShuffleBtn.setIcon(icon32)

        self.horizontalLayout_19.addWidget(self.mediaShuffleBtn)

        self.mediaMuteBtn = QPushButton(self.mediaRightSideControlFrames)
        self.mediaMuteBtn.setObjectName(u"mediaMuteBtn")
        self.mediaMuteBtn.setMinimumSize(QSize(0, 20))
        icon33 = QIcon()
        icon33.addFile(u":/icons/icons/cil-volume-high.png", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaMuteBtn.setIcon(icon33)
        self.mediaMuteBtn.setIconSize(QSize(16, 16))

        self.horizontalLayout_19.addWidget(self.mediaMuteBtn)

        self.mediaVolumeSlider = QSlider(self.mediaRightSideControlFrames)
        self.mediaVolumeSlider.setObjectName(u"mediaVolumeSlider")
        self.mediaVolumeSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_19.addWidget(self.mediaVolumeSlider)


        self.horizontalLayout_17.addWidget(self.mediaRightSideControlFrames, 0, Qt.AlignRight)


        self.verticalLayout_19.addWidget(self.mediaControlFrame)


        self.verticalLayout_20.addWidget(self.mediaPlayerFrame2)


        self.verticalLayout_18.addWidget(self.mediaPlayerFrame1)


        self.verticalLayout_17.addWidget(self.mediaPlayerWidget)


        self.verticalLayout_16.addWidget(self.filesStackWidget)

        self.mainStack.addWidget(self.filesStack)
        self.favoritesStack = QWidget()
        self.favoritesStack.setObjectName(u"favoritesStack")
        self.verticalLayout_26 = QVBoxLayout(self.favoritesStack)
        self.verticalLayout_26.setSpacing(0)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.favoritesWidget = QWidget(self.favoritesStack)
        self.favoritesWidget.setObjectName(u"favoritesWidget")
        self.favoritesWidget.setStyleSheet(u"")
        self.verticalLayout_27 = QVBoxLayout(self.favoritesWidget)
        self.verticalLayout_27.setSpacing(4)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(4, 4, 4, 2)
        self.favoritesUtilityFrame = QFrame(self.favoritesWidget)
        self.favoritesUtilityFrame.setObjectName(u"favoritesUtilityFrame")
        self.favoritesUtilityFrame.setMinimumSize(QSize(0, 20))
        self.favoritesUtilityFrame.setFrameShape(QFrame.StyledPanel)
        self.favoritesUtilityFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.favoritesUtilityFrame)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.favoritesMenuTitleBtn = QPushButton(self.favoritesUtilityFrame)
        self.favoritesMenuTitleBtn.setObjectName(u"favoritesMenuTitleBtn")
        self.favoritesMenuTitleBtn.setFont(font)

        self.horizontalLayout_25.addWidget(self.favoritesMenuTitleBtn, 0, Qt.AlignLeft)


        self.verticalLayout_27.addWidget(self.favoritesUtilityFrame)

        self.favoritesScrollArea = QScrollArea(self.favoritesWidget)
        self.favoritesScrollArea.setObjectName(u"favoritesScrollArea")
        self.favoritesScrollArea.setWidgetResizable(True)
        self.favoritesScrollAreaWidgetContents = QWidget()
        self.favoritesScrollAreaWidgetContents.setObjectName(u"favoritesScrollAreaWidgetContents")
        self.favoritesScrollAreaWidgetContents.setGeometry(QRect(0, 0, 559, 624))
        self.verticalLayout_29 = QVBoxLayout(self.favoritesScrollAreaWidgetContents)
        self.verticalLayout_29.setSpacing(4)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.favoriteItemFrame = QFrame(self.favoritesScrollAreaWidgetContents)
        self.favoriteItemFrame.setObjectName(u"favoriteItemFrame")
        self.favoriteItemFrame.setMinimumSize(QSize(0, 100))
        self.favoriteItemFrame.setStyleSheet(u"")
        self.favoriteItemFrame.setFrameShape(QFrame.StyledPanel)
        self.favoriteItemFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.favoriteItemFrame)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.favoriteNameLabel = QLabel(self.favoriteItemFrame)
        self.favoriteNameLabel.setObjectName(u"favoriteNameLabel")
        self.favoriteNameLabel.setFont(font)

        self.verticalLayout_28.addWidget(self.favoriteNameLabel)

        self.favoriteInfoFrame1 = QFrame(self.favoriteItemFrame)
        self.favoriteInfoFrame1.setObjectName(u"favoriteInfoFrame1")
        self.favoriteInfoFrame1.setMaximumSize(QSize(16777215, 16))
        self.favoriteInfoFrame1.setFrameShape(QFrame.StyledPanel)
        self.favoriteInfoFrame1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.favoriteInfoFrame1)
        self.horizontalLayout_26.setSpacing(16)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.resultSeederLabel_2 = QLabel(self.favoriteInfoFrame1)
        self.resultSeederLabel_2.setObjectName(u"resultSeederLabel_2")
        self.resultSeederLabel_2.setMinimumSize(QSize(72, 0))

        self.horizontalLayout_26.addWidget(self.resultSeederLabel_2)

        self.resultLeecherLabel_2 = QLabel(self.favoriteInfoFrame1)
        self.resultLeecherLabel_2.setObjectName(u"resultLeecherLabel_2")
        self.resultLeecherLabel_2.setMinimumSize(QSize(72, 0))

        self.horizontalLayout_26.addWidget(self.resultLeecherLabel_2)

        self.resultSizeLabel_3 = QLabel(self.favoriteInfoFrame1)
        self.resultSizeLabel_3.setObjectName(u"resultSizeLabel_3")
        self.resultSizeLabel_3.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_26.addWidget(self.resultSizeLabel_3)

        self.nsfwLabel_2 = QLabel(self.favoriteInfoFrame1)
        self.nsfwLabel_2.setObjectName(u"nsfwLabel_2")
        self.nsfwLabel_2.setMinimumSize(QSize(36, 0))

        self.horizontalLayout_26.addWidget(self.nsfwLabel_2)


        self.verticalLayout_28.addWidget(self.favoriteInfoFrame1, 0, Qt.AlignLeft)

        self.favoriteOutputInfoFrame2 = QFrame(self.favoriteItemFrame)
        self.favoriteOutputInfoFrame2.setObjectName(u"favoriteOutputInfoFrame2")
        self.favoriteOutputInfoFrame2.setMaximumSize(QSize(16777215, 16))
        self.favoriteOutputInfoFrame2.setFrameShape(QFrame.StyledPanel)
        self.favoriteOutputInfoFrame2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.favoriteOutputInfoFrame2)
        self.horizontalLayout_27.setSpacing(16)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.resultAgeLabel_2 = QLabel(self.favoriteOutputInfoFrame2)
        self.resultAgeLabel_2.setObjectName(u"resultAgeLabel_2")

        self.horizontalLayout_27.addWidget(self.resultAgeLabel_2)

        self.resultSiteLabel_2 = QLabel(self.favoriteOutputInfoFrame2)
        self.resultSiteLabel_2.setObjectName(u"resultSiteLabel_2")

        self.horizontalLayout_27.addWidget(self.resultSiteLabel_2)

        self.resultTypeLabel_2 = QLabel(self.favoriteOutputInfoFrame2)
        self.resultTypeLabel_2.setObjectName(u"resultTypeLabel_2")
        self.resultTypeLabel_2.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_27.addWidget(self.resultTypeLabel_2)


        self.verticalLayout_28.addWidget(self.favoriteOutputInfoFrame2, 0, Qt.AlignLeft)

        self.favoriteBtnFrame = QFrame(self.favoriteItemFrame)
        self.favoriteBtnFrame.setObjectName(u"favoriteBtnFrame")
        self.favoriteBtnFrame.setMinimumSize(QSize(0, 0))
        self.favoriteBtnFrame.setMaximumSize(QSize(16777215, 18))
        self.favoriteBtnFrame.setFrameShape(QFrame.StyledPanel)
        self.favoriteBtnFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.favoriteBtnFrame)
        self.horizontalLayout_28.setSpacing(16)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.removeFavoriteBtn = QToolButton(self.favoriteBtnFrame)
        self.removeFavoriteBtn.setObjectName(u"removeFavoriteBtn")
        self.removeFavoriteBtn.setMinimumSize(QSize(0, 0))
        self.removeFavoriteBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon34 = QIcon()
        icon34.addFile(u":/icons/icons/trash-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.removeFavoriteBtn.setIcon(icon34)

        self.horizontalLayout_28.addWidget(self.removeFavoriteBtn)

        self.magnetLinkBtn_2 = QPushButton(self.favoriteBtnFrame)
        self.magnetLinkBtn_2.setObjectName(u"magnetLinkBtn_2")
        self.magnetLinkBtn_2.setMinimumSize(QSize(58, 0))
        self.magnetLinkBtn_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.magnetLinkBtn_2.setIcon(icon17)
        self.magnetLinkBtn_2.setIconSize(QSize(10, 10))

        self.horizontalLayout_28.addWidget(self.magnetLinkBtn_2)

        self.downloadBtn_2 = QPushButton(self.favoriteBtnFrame)
        self.downloadBtn_2.setObjectName(u"downloadBtn_2")
        self.downloadBtn_2.setMinimumSize(QSize(68, 0))
        self.downloadBtn_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadBtn_2.setIcon(icon10)
        self.downloadBtn_2.setIconSize(QSize(10, 10))

        self.horizontalLayout_28.addWidget(self.downloadBtn_2)

        self.urlBtn_2 = QPushButton(self.favoriteBtnFrame)
        self.urlBtn_2.setObjectName(u"urlBtn_2")
        self.urlBtn_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.urlBtn_2.setIcon(icon18)
        self.urlBtn_2.setIconSize(QSize(10, 10))

        self.horizontalLayout_28.addWidget(self.urlBtn_2)

        self.verifiedBtn_2 = QPushButton(self.favoriteBtnFrame)
        self.verifiedBtn_2.setObjectName(u"verifiedBtn_2")
        self.verifiedBtn_2.setIcon(icon19)
        self.verifiedBtn_2.setIconSize(QSize(10, 10))

        self.horizontalLayout_28.addWidget(self.verifiedBtn_2)


        self.verticalLayout_28.addWidget(self.favoriteBtnFrame, 0, Qt.AlignLeft)


        self.verticalLayout_29.addWidget(self.favoriteItemFrame)

        self.frame_19 = QFrame(self.favoritesScrollAreaWidgetContents)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMinimumSize(QSize(0, 100))
        self.frame_19.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)

        self.verticalLayout_29.addWidget(self.frame_19)

        self.frame_8 = QFrame(self.favoritesScrollAreaWidgetContents)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 100))
        self.frame_8.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)

        self.verticalLayout_29.addWidget(self.frame_8)

        self.frame_7 = QFrame(self.favoritesScrollAreaWidgetContents)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 100))
        self.frame_7.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)

        self.verticalLayout_29.addWidget(self.frame_7)

        self.frame = QFrame(self.favoritesScrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 100))
        self.frame.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_29.addWidget(self.frame)

        self.endOfFavoritesBtn = QPushButton(self.favoritesScrollAreaWidgetContents)
        self.endOfFavoritesBtn.setObjectName(u"endOfFavoritesBtn")
        self.endOfFavoritesBtn.setMinimumSize(QSize(0, 100))

        self.verticalLayout_29.addWidget(self.endOfFavoritesBtn)

        self.verticalSpacer_4 = QSpacerItem(20, 101, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_4)

        self.favoritesScrollArea.setWidget(self.favoritesScrollAreaWidgetContents)

        self.verticalLayout_27.addWidget(self.favoritesScrollArea)


        self.verticalLayout_26.addWidget(self.favoritesWidget)

        self.mainStack.addWidget(self.favoritesStack)
        self.historyStack = QWidget()
        self.historyStack.setObjectName(u"historyStack")
        self.verticalLayout_30 = QVBoxLayout(self.historyStack)
        self.verticalLayout_30.setSpacing(0)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.historyWidget = QWidget(self.historyStack)
        self.historyWidget.setObjectName(u"historyWidget")
        self.verticalLayout_31 = QVBoxLayout(self.historyWidget)
        self.verticalLayout_31.setSpacing(4)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_31.setContentsMargins(4, 4, 4, 2)
        self.historyUtilityFrame = QFrame(self.historyWidget)
        self.historyUtilityFrame.setObjectName(u"historyUtilityFrame")
        self.historyUtilityFrame.setMinimumSize(QSize(0, 20))
        self.historyUtilityFrame.setFrameShape(QFrame.StyledPanel)
        self.historyUtilityFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.historyUtilityFrame)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.historyMenuTitleBtn = QPushButton(self.historyUtilityFrame)
        self.historyMenuTitleBtn.setObjectName(u"historyMenuTitleBtn")
        self.historyMenuTitleBtn.setFont(font)

        self.horizontalLayout_32.addWidget(self.historyMenuTitleBtn, 0, Qt.AlignLeft)


        self.verticalLayout_31.addWidget(self.historyUtilityFrame)

        self.historyScrollArea = QScrollArea(self.historyWidget)
        self.historyScrollArea.setObjectName(u"historyScrollArea")
        self.historyScrollArea.setWidgetResizable(True)
        self.historyScrollAreaWidgetContents = QWidget()
        self.historyScrollAreaWidgetContents.setObjectName(u"historyScrollAreaWidgetContents")
        self.historyScrollAreaWidgetContents.setGeometry(QRect(0, 0, 559, 520))
        self.verticalLayout_33 = QVBoxLayout(self.historyScrollAreaWidgetContents)
        self.verticalLayout_33.setSpacing(4)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.verticalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.historyItemFrame = QFrame(self.historyScrollAreaWidgetContents)
        self.historyItemFrame.setObjectName(u"historyItemFrame")
        self.historyItemFrame.setMinimumSize(QSize(0, 100))
        self.historyItemFrame.setStyleSheet(u"")
        self.historyItemFrame.setFrameShape(QFrame.StyledPanel)
        self.historyItemFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.historyItemFrame)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.historyNameLabel = QLabel(self.historyItemFrame)
        self.historyNameLabel.setObjectName(u"historyNameLabel")
        self.historyNameLabel.setFont(font)

        self.verticalLayout_32.addWidget(self.historyNameLabel)

        self.historyInfoFrame1 = QFrame(self.historyItemFrame)
        self.historyInfoFrame1.setObjectName(u"historyInfoFrame1")
        self.historyInfoFrame1.setMaximumSize(QSize(16777215, 16))
        self.historyInfoFrame1.setFrameShape(QFrame.StyledPanel)
        self.historyInfoFrame1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.historyInfoFrame1)
        self.horizontalLayout_29.setSpacing(16)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.historySeederLabel = QLabel(self.historyInfoFrame1)
        self.historySeederLabel.setObjectName(u"historySeederLabel")
        self.historySeederLabel.setMinimumSize(QSize(72, 0))

        self.horizontalLayout_29.addWidget(self.historySeederLabel)

        self.historyLeecherLabel = QLabel(self.historyInfoFrame1)
        self.historyLeecherLabel.setObjectName(u"historyLeecherLabel")
        self.historyLeecherLabel.setMinimumSize(QSize(72, 0))

        self.horizontalLayout_29.addWidget(self.historyLeecherLabel)

        self.historySizeLabel = QLabel(self.historyInfoFrame1)
        self.historySizeLabel.setObjectName(u"historySizeLabel")
        self.historySizeLabel.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_29.addWidget(self.historySizeLabel)

        self.historyPathLabel = QLabel(self.historyInfoFrame1)
        self.historyPathLabel.setObjectName(u"historyPathLabel")

        self.horizontalLayout_29.addWidget(self.historyPathLabel)


        self.verticalLayout_32.addWidget(self.historyInfoFrame1, 0, Qt.AlignLeft)

        self.historyInfoFrame2 = QFrame(self.historyItemFrame)
        self.historyInfoFrame2.setObjectName(u"historyInfoFrame2")
        self.historyInfoFrame2.setMaximumSize(QSize(16777215, 16))
        self.historyInfoFrame2.setFrameShape(QFrame.StyledPanel)
        self.historyInfoFrame2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.historyInfoFrame2)
        self.horizontalLayout_30.setSpacing(16)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.historyNsfwLabel = QLabel(self.historyInfoFrame2)
        self.historyNsfwLabel.setObjectName(u"historyNsfwLabel")

        self.horizontalLayout_30.addWidget(self.historyNsfwLabel)

        self.historyElapsedLabel = QLabel(self.historyInfoFrame2)
        self.historyElapsedLabel.setObjectName(u"historyElapsedLabel")
        self.historyElapsedLabel.setMinimumSize(QSize(36, 0))

        self.horizontalLayout_30.addWidget(self.historyElapsedLabel)

        self.historyTimestampLabel = QLabel(self.historyInfoFrame2)
        self.historyTimestampLabel.setObjectName(u"historyTimestampLabel")

        self.horizontalLayout_30.addWidget(self.historyTimestampLabel)


        self.verticalLayout_32.addWidget(self.historyInfoFrame2, 0, Qt.AlignLeft)

        self.historyBtnFrame = QFrame(self.historyItemFrame)
        self.historyBtnFrame.setObjectName(u"historyBtnFrame")
        self.historyBtnFrame.setMinimumSize(QSize(0, 0))
        self.historyBtnFrame.setMaximumSize(QSize(16777215, 18))
        self.historyBtnFrame.setFrameShape(QFrame.StyledPanel)
        self.historyBtnFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.historyBtnFrame)
        self.horizontalLayout_31.setSpacing(32)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.deleteHistoryBtn = QToolButton(self.historyBtnFrame)
        self.deleteHistoryBtn.setObjectName(u"deleteHistoryBtn")
        self.deleteHistoryBtn.setMinimumSize(QSize(0, 0))
        self.deleteHistoryBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.deleteHistoryBtn.setIcon(icon34)

        self.horizontalLayout_31.addWidget(self.deleteHistoryBtn)

        self.historyLinkBtn = QPushButton(self.historyBtnFrame)
        self.historyLinkBtn.setObjectName(u"historyLinkBtn")
        self.historyLinkBtn.setMinimumSize(QSize(58, 0))
        self.historyLinkBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.historyLinkBtn.setIcon(icon17)
        self.historyLinkBtn.setIconSize(QSize(10, 10))

        self.horizontalLayout_31.addWidget(self.historyLinkBtn)


        self.verticalLayout_32.addWidget(self.historyBtnFrame, 0, Qt.AlignLeft)


        self.verticalLayout_33.addWidget(self.historyItemFrame)

        self.frame_13 = QFrame(self.historyScrollAreaWidgetContents)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 100))
        self.frame_13.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)

        self.verticalLayout_33.addWidget(self.frame_13)

        self.frame_18 = QFrame(self.historyScrollAreaWidgetContents)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 100))
        self.frame_18.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)

        self.verticalLayout_33.addWidget(self.frame_18)

        self.frame_17 = QFrame(self.historyScrollAreaWidgetContents)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMinimumSize(QSize(0, 100))
        self.frame_17.setStyleSheet(u"* {\n"
"	background: #222222;\n"
"	border-radius: 12px;\n"
"}")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)

        self.verticalLayout_33.addWidget(self.frame_17)

        self.endOfHistoryBtn = QPushButton(self.historyScrollAreaWidgetContents)
        self.endOfHistoryBtn.setObjectName(u"endOfHistoryBtn")
        self.endOfHistoryBtn.setMinimumSize(QSize(0, 100))
        self.endOfHistoryBtn.setStyleSheet(u"")

        self.verticalLayout_33.addWidget(self.endOfHistoryBtn)

        self.verticalSpacer_5 = QSpacerItem(20, 101, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_33.addItem(self.verticalSpacer_5)

        self.historyScrollArea.setWidget(self.historyScrollAreaWidgetContents)

        self.verticalLayout_31.addWidget(self.historyScrollArea)


        self.verticalLayout_30.addWidget(self.historyWidget)

        self.mainStack.addWidget(self.historyStack)
        self.settingsStack = QWidget()
        self.settingsStack.setObjectName(u"settingsStack")
        self.verticalLayout_36 = QVBoxLayout(self.settingsStack)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.settingsWidget = QWidget(self.settingsStack)
        self.settingsWidget.setObjectName(u"settingsWidget")
        self.horizontalLayout_33 = QHBoxLayout(self.settingsWidget)
        self.horizontalLayout_33.setSpacing(4)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(4, 4, 4, 2)
        self.settingLeftWidget = QWidget(self.settingsWidget)
        self.settingLeftWidget.setObjectName(u"settingLeftWidget")
        self.verticalLayout_37 = QVBoxLayout(self.settingLeftWidget)
        self.verticalLayout_37.setSpacing(0)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(0, 0, 0, 2)
        self.quickSettingsMenuLabel = QLabel(self.settingLeftWidget)
        self.quickSettingsMenuLabel.setObjectName(u"quickSettingsMenuLabel")
        self.quickSettingsMenuLabel.setFont(font)

        self.verticalLayout_37.addWidget(self.quickSettingsMenuLabel)

        self.settingLeftScrollArea = QScrollArea(self.settingLeftWidget)
        self.settingLeftScrollArea.setObjectName(u"settingLeftScrollArea")
        self.settingLeftScrollArea.setWidgetResizable(True)
        self.settingLeftScrollWidget = QWidget()
        self.settingLeftScrollWidget.setObjectName(u"settingLeftScrollWidget")
        self.settingLeftScrollWidget.setGeometry(QRect(0, 0, 125, 480))
        self.verticalLayout_39 = QVBoxLayout(self.settingLeftScrollWidget)
        self.verticalLayout_39.setSpacing(0)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(0, 0, 8, 0)
        self.qSettingNsfwLabel = QLabel(self.settingLeftScrollWidget)
        self.qSettingNsfwLabel.setObjectName(u"qSettingNsfwLabel")
        self.qSettingNsfwLabel.setFont(font)

        self.verticalLayout_39.addWidget(self.qSettingNsfwLabel)

        self.qSettingNsfwBtn = QPushButton(self.settingLeftScrollWidget)
        self.qSettingNsfwBtn.setObjectName(u"qSettingNsfwBtn")

        self.verticalLayout_39.addWidget(self.qSettingNsfwBtn)

        self.label_7 = QLabel(self.settingLeftScrollWidget)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_39.addWidget(self.label_7)

        self.pushButton_16 = QPushButton(self.settingLeftScrollWidget)
        self.pushButton_16.setObjectName(u"pushButton_16")

        self.verticalLayout_39.addWidget(self.pushButton_16)

        self.label_8 = QLabel(self.settingLeftScrollWidget)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_39.addWidget(self.label_8)

        self.pushButton_15 = QPushButton(self.settingLeftScrollWidget)
        self.pushButton_15.setObjectName(u"pushButton_15")

        self.verticalLayout_39.addWidget(self.pushButton_15)

        self.label_9 = QLabel(self.settingLeftScrollWidget)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_39.addWidget(self.label_9)

        self.pushButton_14 = QPushButton(self.settingLeftScrollWidget)
        self.pushButton_14.setObjectName(u"pushButton_14")

        self.verticalLayout_39.addWidget(self.pushButton_14)

        self.label_10 = QLabel(self.settingLeftScrollWidget)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_39.addWidget(self.label_10)

        self.pushButton_13 = QPushButton(self.settingLeftScrollWidget)
        self.pushButton_13.setObjectName(u"pushButton_13")

        self.verticalLayout_39.addWidget(self.pushButton_13)

        self.label_11 = QLabel(self.settingLeftScrollWidget)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_39.addWidget(self.label_11)

        self.pushButton_11 = QPushButton(self.settingLeftScrollWidget)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.verticalLayout_39.addWidget(self.pushButton_11)

        self.label_12 = QLabel(self.settingLeftScrollWidget)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_39.addWidget(self.label_12)

        self.pushButton_10 = QPushButton(self.settingLeftScrollWidget)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.verticalLayout_39.addWidget(self.pushButton_10)

        self.label_13 = QLabel(self.settingLeftScrollWidget)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_39.addWidget(self.label_13)

        self.pushButton_9 = QPushButton(self.settingLeftScrollWidget)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.verticalLayout_39.addWidget(self.pushButton_9)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_39.addItem(self.verticalSpacer_6)

        self.settingLeftScrollArea.setWidget(self.settingLeftScrollWidget)

        self.verticalLayout_37.addWidget(self.settingLeftScrollArea)


        self.horizontalLayout_33.addWidget(self.settingLeftWidget, 0, Qt.AlignLeft)

        self.settingsRightWidget = QWidget(self.settingsWidget)
        self.settingsRightWidget.setObjectName(u"settingsRightWidget")
        self.verticalLayout_38 = QVBoxLayout(self.settingsRightWidget)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(0, 0, 0, 2)
        self.settingsRightScrollArea = QScrollArea(self.settingsRightWidget)
        self.settingsRightScrollArea.setObjectName(u"settingsRightScrollArea")
        self.settingsRightScrollArea.setWidgetResizable(True)
        self.settingsRightScrollWidget = QWidget()
        self.settingsRightScrollWidget.setObjectName(u"settingsRightScrollWidget")
        self.settingsRightScrollWidget.setGeometry(QRect(0, 0, 430, 362))
        self.verticalLayout_40 = QVBoxLayout(self.settingsRightScrollWidget)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.label_6 = QLabel(self.settingsRightScrollWidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_40.addWidget(self.label_6)

        self.settingsRightScrollArea.setWidget(self.settingsRightScrollWidget)

        self.verticalLayout_38.addWidget(self.settingsRightScrollArea)


        self.horizontalLayout_33.addWidget(self.settingsRightWidget)


        self.verticalLayout_36.addWidget(self.settingsWidget)

        self.mainStack.addWidget(self.settingsStack)
        self.helpStack = QWidget()
        self.helpStack.setObjectName(u"helpStack")
        self.verticalLayout_34 = QVBoxLayout(self.helpStack)
        self.verticalLayout_34.setSpacing(0)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.helpWidget = QWidget(self.helpStack)
        self.helpWidget.setObjectName(u"helpWidget")
        self.verticalLayout_35 = QVBoxLayout(self.helpWidget)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.helpLabel = QLabel(self.helpWidget)
        self.helpLabel.setObjectName(u"helpLabel")

        self.verticalLayout_35.addWidget(self.helpLabel)


        self.verticalLayout_34.addWidget(self.helpWidget)

        self.mainStack.addWidget(self.helpStack)
        self.initAppStack = QWidget()
        self.initAppStack.setObjectName(u"initAppStack")
        self.verticalLayout_42 = QVBoxLayout(self.initAppStack)
        self.verticalLayout_42.setSpacing(0)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.verticalLayout_42.setContentsMargins(0, 0, 0, 0)
        self.initAppWidget = QWidget(self.initAppStack)
        self.initAppWidget.setObjectName(u"initAppWidget")
        self.horizontalLayout_34 = QHBoxLayout(self.initAppWidget)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.initIcon = QLabel(self.initAppWidget)
        self.initIcon.setObjectName(u"initIcon")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.initIcon.sizePolicy().hasHeightForWidth())
        self.initIcon.setSizePolicy(sizePolicy3)
        self.initIcon.setMinimumSize(QSize(200, 200))
        self.initIcon.setMaximumSize(QSize(200, 200))
        self.initIcon.setSizeIncrement(QSize(0, 0))
        self.initIcon.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_34.addWidget(self.initIcon, 0, Qt.AlignHCenter)


        self.verticalLayout_42.addWidget(self.initAppWidget)

        self.mainStack.addWidget(self.initAppStack)

        self.verticalLayout_7.addWidget(self.mainStack)

        self.footerContainer = QWidget(self.centerMainMenu)
        self.footerContainer.setObjectName(u"footerContainer")
        self.footerContainer.setMinimumSize(QSize(0, 0))
        self.verticalLayout_8 = QVBoxLayout(self.footerContainer)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.notificationWidget = QWidget(self.footerContainer)
        self.notificationWidget.setObjectName(u"notificationWidget")
        self.notificationWidget.setMinimumSize(QSize(0, 0))
        self.notificationWidget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_11 = QHBoxLayout(self.notificationWidget)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.notificationTextAreaFrame = QFrame(self.notificationWidget)
        self.notificationTextAreaFrame.setObjectName(u"notificationTextAreaFrame")
        self.notificationTextAreaFrame.setFrameShape(QFrame.StyledPanel)
        self.notificationTextAreaFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.notificationTextAreaFrame)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(20, 14, 20, 20)
        self.notificationTitleLabel = QLabel(self.notificationTextAreaFrame)
        self.notificationTitleLabel.setObjectName(u"notificationTitleLabel")
        self.notificationTitleLabel.setFont(font)
        self.notificationTitleLabel.setWordWrap(True)

        self.verticalLayout_11.addWidget(self.notificationTitleLabel)

        self.notificationTextLabel = QLabel(self.notificationTextAreaFrame)
        self.notificationTextLabel.setObjectName(u"notificationTextLabel")
        self.notificationTextLabel.setWordWrap(True)

        self.verticalLayout_11.addWidget(self.notificationTextLabel)

        self.notificationSpacer = QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_11.addItem(self.notificationSpacer)


        self.horizontalLayout_11.addWidget(self.notificationTextAreaFrame)

        self.notificationCloseFrame = QFrame(self.notificationWidget)
        self.notificationCloseFrame.setObjectName(u"notificationCloseFrame")
        self.notificationCloseFrame.setFrameShape(QFrame.StyledPanel)
        self.notificationCloseFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.notificationCloseFrame)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 12, 12, 0)
        self.closeNotificationBtn = QPushButton(self.notificationCloseFrame)
        self.closeNotificationBtn.setObjectName(u"closeNotificationBtn")
        self.closeNotificationBtn.setMinimumSize(QSize(32, 32))
        self.closeNotificationBtn.setMaximumSize(QSize(32, 32))
        icon35 = QIcon()
        icon35.addFile(u":/icons/icons/cil-x-circle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.closeNotificationBtn.setIcon(icon35)
        self.closeNotificationBtn.setIconSize(QSize(32, 32))

        self.verticalLayout_10.addWidget(self.closeNotificationBtn, 0, Qt.AlignRight)


        self.horizontalLayout_11.addWidget(self.notificationCloseFrame, 0, Qt.AlignTop)


        self.verticalLayout_8.addWidget(self.notificationWidget)

        self.footer = QWidget(self.footerContainer)
        self.footer.setObjectName(u"footer")
        self.horizontalLayout_5 = QHBoxLayout(self.footer)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.downloadSpeedFrame = QFrame(self.footer)
        self.downloadSpeedFrame.setObjectName(u"downloadSpeedFrame")
        self.downloadSpeedFrame.setFrameShape(QFrame.StyledPanel)
        self.downloadSpeedFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.downloadSpeedFrame)
        self.horizontalLayout_7.setSpacing(8)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(6, 0, 0, 0)
        self.downloadSpeedBtn = QPushButton(self.downloadSpeedFrame)
        self.downloadSpeedBtn.setObjectName(u"downloadSpeedBtn")
        icon36 = QIcon()
        icon36.addFile(u":/icons/icons/cil-chevron-double-down.png", QSize(), QIcon.Normal, QIcon.Off)
        self.downloadSpeedBtn.setIcon(icon36)
        self.downloadSpeedBtn.setIconSize(QSize(12, 12))

        self.horizontalLayout_7.addWidget(self.downloadSpeedBtn)

        self.uploadSpeedBtn = QPushButton(self.downloadSpeedFrame)
        self.uploadSpeedBtn.setObjectName(u"uploadSpeedBtn")
        icon37 = QIcon()
        icon37.addFile(u":/icons/icons/cil-chevron-double-up.png", QSize(), QIcon.Normal, QIcon.Off)
        self.uploadSpeedBtn.setIcon(icon37)
        self.uploadSpeedBtn.setIconSize(QSize(12, 12))

        self.horizontalLayout_7.addWidget(self.uploadSpeedBtn)


        self.horizontalLayout_5.addWidget(self.downloadSpeedFrame, 0, Qt.AlignLeft)

        self.logWidget = QWidget(self.footer)
        self.logWidget.setObjectName(u"logWidget")
        self.horizontalLayout_10 = QHBoxLayout(self.logWidget)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.logLabel = QLabel(self.logWidget)
        self.logLabel.setObjectName(u"logLabel")
        sizePolicy.setHeightForWidth(self.logLabel.sizePolicy().hasHeightForWidth())
        self.logLabel.setSizePolicy(sizePolicy)
        self.logLabel.setTextFormat(Qt.AutoText)
        self.logLabel.setScaledContents(False)
        self.logLabel.setAlignment(Qt.AlignCenter)
        self.logLabel.setWordWrap(False)

        self.horizontalLayout_10.addWidget(self.logLabel)


        self.horizontalLayout_5.addWidget(self.logWidget)

        self.footerRightBtnFrame = QFrame(self.footer)
        self.footerRightBtnFrame.setObjectName(u"footerRightBtnFrame")
        self.footerRightBtnFrame.setFrameShape(QFrame.StyledPanel)
        self.footerRightBtnFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.footerRightBtnFrame)
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 4, 0)
        self.totalDownloadedLabel = QPushButton(self.footerRightBtnFrame)
        self.totalDownloadedLabel.setObjectName(u"totalDownloadedLabel")
        self.totalDownloadedLabel.setMinimumSize(QSize(65, 0))
        icon38 = QIcon()
        icon38.addFile(u":/icons/icons/cil-cloud-download.png", QSize(), QIcon.Normal, QIcon.Off)
        self.totalDownloadedLabel.setIcon(icon38)
        self.totalDownloadedLabel.setIconSize(QSize(14, 14))

        self.horizontalLayout_6.addWidget(self.totalDownloadedLabel)

        self.internetConnectivityBtn = QPushButton(self.footerRightBtnFrame)
        self.internetConnectivityBtn.setObjectName(u"internetConnectivityBtn")
        icon39 = QIcon()
        icon39.addFile(u":/icons/icons/cil-wifi-signal-4.png", QSize(), QIcon.Normal, QIcon.Off)
        self.internetConnectivityBtn.setIcon(icon39)
        self.internetConnectivityBtn.setIconSize(QSize(14, 14))

        self.horizontalLayout_6.addWidget(self.internetConnectivityBtn)

        self.mediaPlayerShowBtn = QPushButton(self.footerRightBtnFrame)
        self.mediaPlayerShowBtn.setObjectName(u"mediaPlayerShowBtn")
        self.mediaPlayerShowBtn.setMinimumSize(QSize(18, 18))
        icon40 = QIcon()
        icon40.addFile(u":/icons/icons/cil-speaker.png", QSize(), QIcon.Normal, QIcon.Off)
        self.mediaPlayerShowBtn.setIcon(icon40)
        self.mediaPlayerShowBtn.setIconSize(QSize(14, 14))
        self.mediaPlayerShowBtn.setCheckable(True)
        self.mediaPlayerShowBtn.setChecked(True)

        self.horizontalLayout_6.addWidget(self.mediaPlayerShowBtn)

        self.appResetBtn = QPushButton(self.footerRightBtnFrame)
        self.appResetBtn.setObjectName(u"appResetBtn")
        self.appResetBtn.setMinimumSize(QSize(18, 18))
        self.appResetBtn.setIcon(icon20)
        self.appResetBtn.setIconSize(QSize(14, 14))

        self.horizontalLayout_6.addWidget(self.appResetBtn)


        self.horizontalLayout_5.addWidget(self.footerRightBtnFrame, 0, Qt.AlignRight)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)
        self.horizontalLayout_5.setStretch(2, 1)

        self.verticalLayout_8.addWidget(self.footer)


        self.verticalLayout_7.addWidget(self.footerContainer)


        self.horizontalLayout_3.addWidget(self.centerMainMenu)


        self.verticalLayout_2.addWidget(self.mainContainer)

        MainWindow.setCentralWidget(self.centralwidget)
#if QT_CONFIG(shortcut)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(MainWindow)

        self.mainStack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.appIconBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.appTitleBtn.setText(QCoreApplication.translate("MainWindow", u"Bitroid DM", None))
        self.netSpeedBtn.setText(QCoreApplication.translate("MainWindow", u"12.3 KB/s", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.notificationBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.settingsBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.appMinBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.appMaxBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.appCloseBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"   Menu", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"   Search", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"   Downloads", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"   Files", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"   Favorites", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"   History", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"   Settings", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"   Help", None))
        self.searchInputText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the shortest possible query to search...", None))
        self.searchBtn.setText("")
        self.resultNameLabel.setText(QCoreApplication.translate("MainWindow", u"Harry Potter and the Order of the Phoenix 2007 1080p BrRip x264 YIFY", None))
        self.resultSeederLabel.setText(QCoreApplication.translate("MainWindow", u"Seeder: 9999", None))
        self.resultLeecherLabel.setText(QCoreApplication.translate("MainWindow", u"Leecher: 9999", None))
        self.resultSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size: 9999.0 GB", None))
        self.nsfwLabel.setText(QCoreApplication.translate("MainWindow", u"NSFW", None))
        self.resultAgeLabel.setText(QCoreApplication.translate("MainWindow", u"Age: 4 weeks", None))
        self.resultSiteLabel.setText(QCoreApplication.translate("MainWindow", u"Site: thepiratebay", None))
        self.resultTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Type: TV - HEVC/x265", None))
        self.favoriteBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.magnetLinkBtn.setText(QCoreApplication.translate("MainWindow", u"Magnet", None))
        self.downloadBtn.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.urlBtn.setText(QCoreApplication.translate("MainWindow", u"Page URL", None))
        self.verifiedBtn.setText(QCoreApplication.translate("MainWindow", u"Verified", None))
        self.endOfSearchBtn.setText(QCoreApplication.translate("MainWindow", u"No More Results!", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Downloads", None))
        self.fileStackTitleBtn.setText(QCoreApplication.translate("MainWindow", u"Files", None))
        self.filesReloadBtn.setText("")
        self.sortByLabel.setText(QCoreApplication.translate("MainWindow", u"Sort By:", None))
        self.filesSortComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Name", None))
        self.filesSortComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Size", None))
        self.filesSortComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Type", None))
        self.filesSortComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Date", None))

        self.fileNameLabel.setText(QCoreApplication.translate("MainWindow", u"Mirzapur 2020 S02 Hindi 720p AMZN WEBRip x264 AAC 5.1 MSubs - LO", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Size: 9999.9 GB", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Extension: .jquery", None))
        self.playFileBtn.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Type: Video File", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Last Modified: 2 minutes ago", None))
        self.endOfFileBtn.setText(QCoreApplication.translate("MainWindow", u"No More Files!", None))
        self.currentPlayingBtn.setText(QCoreApplication.translate("MainWindow", u"03:45:59", None))
        self.remainingMediaBtn.setText(QCoreApplication.translate("MainWindow", u"-04:48:57", None))
        self.mediaFolderBtn.setText("")
        self.playerLockBtn.setText("")
        self.playbackSpeedCombobox.setItemText(0, QCoreApplication.translate("MainWindow", u"0.5x", None))
        self.playbackSpeedCombobox.setItemText(1, QCoreApplication.translate("MainWindow", u"0.75x", None))
        self.playbackSpeedCombobox.setItemText(2, QCoreApplication.translate("MainWindow", u"1.0x", None))
        self.playbackSpeedCombobox.setItemText(3, QCoreApplication.translate("MainWindow", u"1.25x", None))
        self.playbackSpeedCombobox.setItemText(4, QCoreApplication.translate("MainWindow", u"1.75x", None))
        self.playbackSpeedCombobox.setItemText(5, QCoreApplication.translate("MainWindow", u"2.0x", None))

        self.playerUndockBtn.setText("")
        self.mediaStopBtn.setText("")
        self.seekBackwardBtn.setText("")
        self.mediaPreviousBtn.setText("")
        self.mediaPlayBtn.setText("")
        self.mediaNextBtn.setText("")
        self.seekForwardBtn.setText("")
        self.mediaRepeatBtn.setText("")
        self.mediaShuffleBtn.setText("")
        self.mediaMuteBtn.setText("")
        self.favoritesMenuTitleBtn.setText(QCoreApplication.translate("MainWindow", u"Favorites", None))
        self.favoriteNameLabel.setText(QCoreApplication.translate("MainWindow", u"Harry Potter and the Order of the Phoenix 2007 1080p BrRip x264 YIFY", None))
        self.resultSeederLabel_2.setText(QCoreApplication.translate("MainWindow", u"Seeder: 9999", None))
        self.resultLeecherLabel_2.setText(QCoreApplication.translate("MainWindow", u"Leecher: 9999", None))
        self.resultSizeLabel_3.setText(QCoreApplication.translate("MainWindow", u"Size: 9999.0 GB", None))
        self.nsfwLabel_2.setText(QCoreApplication.translate("MainWindow", u"NSFW", None))
        self.resultAgeLabel_2.setText(QCoreApplication.translate("MainWindow", u"Age: 4 weeks", None))
        self.resultSiteLabel_2.setText(QCoreApplication.translate("MainWindow", u"Site: thepiratebay", None))
        self.resultTypeLabel_2.setText(QCoreApplication.translate("MainWindow", u"Type: TV - HEVC/x265", None))
        self.removeFavoriteBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.magnetLinkBtn_2.setText(QCoreApplication.translate("MainWindow", u"Magnet", None))
        self.downloadBtn_2.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.urlBtn_2.setText(QCoreApplication.translate("MainWindow", u"Page URL", None))
        self.verifiedBtn_2.setText(QCoreApplication.translate("MainWindow", u"Verified", None))
        self.endOfFavoritesBtn.setText(QCoreApplication.translate("MainWindow", u"No More Favorite Items", None))
        self.historyMenuTitleBtn.setText(QCoreApplication.translate("MainWindow", u"History", None))
        self.historyNameLabel.setText(QCoreApplication.translate("MainWindow", u"Harry Potter and the Order of the Phoenix 2007 1080p BrRip x264 YIFY", None))
        self.historySeederLabel.setText(QCoreApplication.translate("MainWindow", u"Seeder: 9999", None))
        self.historyLeecherLabel.setText(QCoreApplication.translate("MainWindow", u"Leecher: 9999", None))
        self.historySizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size: 9999.0 GB", None))
        self.historyPathLabel.setText(QCoreApplication.translate("MainWindow", u"Path: C:/Users/Name/Downloads", None))
        self.historyNsfwLabel.setText(QCoreApplication.translate("MainWindow", u"NSFW", None))
        self.historyElapsedLabel.setText(QCoreApplication.translate("MainWindow", u"Elapsed: 12 Hours", None))
        self.historyTimestampLabel.setText(QCoreApplication.translate("MainWindow", u"Date: 21:37:59 03/04/2023", None))
        self.deleteHistoryBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.historyLinkBtn.setText(QCoreApplication.translate("MainWindow", u"Magnet", None))
        self.endOfHistoryBtn.setText(QCoreApplication.translate("MainWindow", u"No More History!", None))
        self.quickSettingsMenuLabel.setText(QCoreApplication.translate("MainWindow", u"Quick Settings", None))
        self.qSettingNsfwLabel.setText(QCoreApplication.translate("MainWindow", u"NSFW Contents", None))
        self.qSettingNsfwBtn.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"No More Settings Available for Now!", None))
        self.helpLabel.setText(QCoreApplication.translate("MainWindow", u"Can't Help Right Now", None))
        self.initIcon.setText("")
        self.notificationTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Notifications:", None))
        self.notificationTextLabel.setText(QCoreApplication.translate("MainWindow", u"This was a notification and this might can contain some suggestions for the respective notification. This can be automated by hiding and showing of this notification frame.", None))
        self.closeNotificationBtn.setText("")
        self.downloadSpeedBtn.setText(QCoreApplication.translate("MainWindow", u"00.0 MB/s", None))
        self.uploadSpeedBtn.setText(QCoreApplication.translate("MainWindow", u"00.0 KB/s", None))
        self.logLabel.setText(QCoreApplication.translate("MainWindow", u"Connected to Internet!", None))
        self.totalDownloadedLabel.setText(QCoreApplication.translate("MainWindow", u"1.2GB", None))
        self.internetConnectivityBtn.setText("")
        self.mediaPlayerShowBtn.setText("")
        self.appResetBtn.setText("")
    # retranslateUi


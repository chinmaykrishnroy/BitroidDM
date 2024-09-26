styles = """
* {
	border: none;
    padding: 0px;
    margin: 0px;
    background-color: none;
    font-family: "Segoe UI";
    font-size: 22px;
}

QScrollArea {
    border: 1px;
}

QScrollBar:vertical {
    width: 4px;
    margin: 10px 0px 10px 0px;
}

QScrollBar:horizontal {
    height: 4px;
    margin: 0px 40px 0px 40px;
}

QScrollBar:vertical, QScrollBar:horizontal {
    background: #dddddd;
    border-radius: 2px;
}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #424242;
    border-radius: 2px;
    min-height: 20px;
    min-width: 20px;
}

QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
    background: #a7b308;
    border-radius: 2px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    background: transparent;
}

#leftMenuBar QPushButton {
	font-size: 18px;
	color: #dddddd;
	text-align: left;
	padding-left: 12px;
	padding-right: 12px;
	margin: 2px 2px;
}

#leftMenuBar QPushButton:hover {
	background: #3f4145;
	border-radius: 4px;
}

#mainBtnWidget QPushButton:focus {
	background: #0f1114;
	border-radius: 4px;
}

#leftMenuBar QPushButton:pressed {
	background: #2e436e;
	border-radius: 4px;
}

#someMoreBtnFrame QToolButton:hover {
	background: #3f4145;
	border-radius: 12px;
}

#someMoreBtnFrame QToolButton:pressed {
	background: #2e436e;
	border-radius: 12px;
}

#appTitleBtn {
    font-size: 21px;
	padding-top: 2px;
	padding-bottom: 4px;
}

#appIconBtn {
}

#appIconBtn:hover {
	background: #a7b308;
	border-radius: 8px;
}

#appIconBtn:pressed {
	background: #000000;
	border-radius: 8px;
}

#appResetBtn,
#mediaPlayerShowBtn {
	border-radius: 8px;
}

#appMinBtn:hover,  
#appMaxBtn:hover,
#appResetBtn:hover,
#mediaPlayerShowBtn:hover {
	background: #404a4a;
}

#netSpeedBtn {
	padding-bottom: 0px;
}

#appMinBtn:pressed,
#appMaxBtn:pressed,
#appResetBtn:pressed,
#mediaPlayerShowBtn:pressed {
	background: #303a3a;
}

#appCloseBtn:hover {
	background: #dd0000;
}

#appCloseBtn:pressed {
	background: #ff0000;
}

QPushButton {
	color: #dddddd;
}

#leftMenuBar {
	background: #1e1f22;
}

#centerMainMenu {
	background: #2b2d30;
}

#headerContainer {
	background: #2b2d30;
}

#searchWidget {
	background: #2b2d30;
}

#footer {
	border-top: 1px solid #3b3d40;
}

#footer QPushButton {
	font-size: 11px;
}

#footer QLabel{
	background: #3b3d40;
	margin: 3px 3px; 
	color: #00ff00;
	font-size: 13px;
	border-radius: 8px;
	padding-bottom: 1px;
	padding-left: 6px;
	padding-right: 6px;
}

#totalDownloadedLabel {
	text-align: left;
}

#headerContainer {
	border-bottom: 1px solid #3b3d40;
}

#leftMenuBar {
	border-right: 1px solid #3b3d40;
}

#netSpeedBtn {
	font-size: 12px;
}

#closeNotificationBtn {
	margin: 6px 6px;
	border-radius: 10px;
}

#closeNotificationBtn:hover {
	background: #111111;
}

#notificationWidget {
	margin: 10px 10px;
	background: #444444;
	border-radius: 12px;
}

#notificationTitleLabel {
	font-size: 16px;
	color: #dddddd;
}

#notificationTextLabel {
	font-size: 16px;
	color: #dddddd;
}

#searchScrollArea {
	background: #2b2d30;
}

#searchInputText {
	font-size: 18px;
	background: #444444;
	color: #dddddd;
	padding: 0px 12px;
	border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}

#searchBtn {
	background-color: #1e335e;
	border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

#searchBtn:hover {
	background-color: #111111;
	border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

#searchBtn:pressed {
	background-color: #a7b308;
	border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

#scrollAreaContents {
	background: #2b2d30;
}

#searchOutputFrame {
	background: #222222;
	border-radius: 12px;
}

#searchOutputFrame QLabel {
	font-size: 16px;
	color: #ffffff;
}

#searchOutputBtnsFrame QPushButton {
	font-size: 14px;
	color: #ffffff;
}

#magnetLinkBtn {
	background: #DA4167;
	padding: 2px 4px;
	border-radius: 4px;
}

#magnetLinkBtn:hover {
	background: #BA2147;
}

#magnetLinkBtn:pressed {
	background: #EA5177;
}

#downloadBtn {
	background: #879300;
	padding: 2px 4px;
	border-radius: 4px;
}

#downloadBtn:hover {
	background: #677300;
}

#downloadBtn:pressed {
	background: #97a310;
}

#urlBtn {
	background: #387780;
	padding: 2px 4px;
	border-radius: 4px;
}

#urlBtn:hover {
	background: #185760;
}

#urlBtn:pressed {
	background: #488790;
}

#favoriteBtn {
	background: #663388;
	border-radius: 6px;
}

#favoriteBtn:hover {
	background: #6666BB;
}

#favoriteBtn:pressed {
	background: #994444;
}

#verifiedBtn {
	background: #000000;
	padding: 2px 4px;
	border-radius: 4px;
}

#endOfSearchBtn:pressed {
	border-radius: 12px;
	background: #444444;
}

#filesStack {
	background: #2b2d30;
}

#mediaPlayerWidget {
	margin: 10px 10px;
	background: #202022;
	border-radius: 46px;
}

#mediaProgressFrame QLabel,  #mediaProgressFrame QPushButton{
	font-size: 12px;
    font-family: "Helvetica", sans-serif;
	padding: 1px 1px;
}

#mediaProgressFrame {
	margin: 0px 8px;
}

#mediaProgressFrame QSlider::groove:horizontal {
    border: 0px solid #535353;
    height: 6px;
    background: #4d4d4d;
    border-radius: 3px;
}

#mediaProgressFrame QSlider::handle:horizontal {
    background: #a7b308;
    width: 14px;
    height: 14px;
    margin: -6px 0px;
	border: 2px solid #a7b308;
    border-radius: 9px;
}

#mediaProgressFrame QSlider::handle:horizontal:hover {
    background: #2e436e;
	border: 2px solid #656565;
}

#mediaProgressFrame QSlider::handle:horizontal:pressed {
    background: #2e436e;
	border: 2px solid #ff2222;
}

#mediaProgressFrame QSlider::sub-page:horizontal {
    background: #a7b308;
    border: 1px solid #879300;
    height: 6px;
    border-radius: 3px;
}

#mediaProgressFrame QSlider::add-page:horizontal {
    background: #2b2d30;
    border: 1px solid #3b3d40;
    height: 6px;
    border-radius: 3px;
}

#mediaPlayBtn {
	background: #2b2d30;
	border-radius: 24px;
	padding-left: 6px;
}

#mediaNextBtn {
	background: #2b2d30;
	border-radius: 16px;
}

#mediaPreviousBtn {
	background: #2b2d30;
	border-radius: 16px;
}

#seekForwardBtn {
	background: #2b2d30;
	border-radius: 16px;
}

#seekBackwardBtn {
	background: #2b2d30;
	border-radius: 16px;
}

#mediaRightSideControlFrames QSlider::groove:horizontal {
    border: 0px solid #535353;
    height: 6px;
    background: #4d4d4d;
    border-radius: 3px;
}

#mediaRightSideControlFrames QSlider::handle:horizontal {
    background: #a7b308;
    width: 8px;
    height: 8px;
    margin: -3px 0px;
	border: 2px solid #a7b308;
    border-radius: 6px;
}

#mediaRightSideControlFrames QSlider::handle:horizontal:hover {
    background: #2e436e;
	border: 2px solid #656565;
}

#mediaRightSideControlFrames QSlider::handle:horizontal:pressed {
    background: #2e436e;
	border: 2px solid #ff2222;
}

#mediaRightSideControlFrames QSlider::sub-page:horizontal {
    background: #a7b308;
    border: 1px solid #879300;
    height: 6px;
    border-radius: 3px;
}

#mediaRightSideControlFrames QSlider::add-page:horizontal {
    background: #2b2d30;
    border: 1px solid #3b3d40;
    height: 6px;
    border-radius: 3px;
}

#mediaLeftSideControlFrames QComboBox {
	padding-left: 4px;
    color: #dddddd;
	background: #2b2d30;
	font-family: "Segoe UI";
	font-size: 10px;
	border: 8px solid #202022; 
	border-radius: 2px;
}



#mediaButtonsFrame QComboBox:pressed {
	border-style: solid; 
	border-radius: 2px;
}

#mediaLeftSideControlFrames QComboBox QAbstractItemView {
    color: white;
    background-color: #474349;
    selection-background-color: #105758; 
    border: none;
}

#mediaLeftSideControlFrames QComboBox:focus {
}

#mediaLeftSideControlFrames QComboBox::drop-down:button
{
    border: none;
    padding: 0;
    width: 0;
}

#mediaLeftSideControlFrames QPushButton:hover {
	background: #3b3d40;
	border-radius: 4px;
}

#mediaRightSideControlFrames QPushButton:hover {
	background: #3b3d40;
	border-radius: 4px;
}

#mediaLeftSideControlFrames QPushButton:pressed {
	background: #000000;
	border-radius: 4px;
}

#mediaRightSideControlFrames QPushButton:pressed {
	background: #000000;
	border-radius: 4px;
}

#mediaPrimaryControlsFrame QPushButton:hover {
	background: #4b4d50;
}

#mediaPrimaryControlsFrame QPushButton:pressed {
	background: #000000;
}

#filesScrollAreaContents {
	background: #2b2d30;
}

#eachFileFrame {
	background: #222222;
	border-radius: 12px;
}

#eachFileFrame QLabel {
	font-size: 16px;
	color: #ffffff;
}

#eachFileFrame QPushButton {
	font-size: 12px;
	color: #ffffff;
}

#fileStackTitleBtn {
	font-size: 22px;
	color: #dddddd;
}

#playFileBtn {
	border-radius: 4px;
	background: #282828; 
}

#playFileBtn:hover {
	border-radius: 4px;
	background: #444444; 
}

#playFileBtn:pressed {
	border-radius: 4px;
	background: #111111; 
}

#filesUtilityFrame QComboBox {
	width: 40px;
	text-align: center;
	padding-left: 4px;
    color: #dddddd;
	background: #2b2d30;
	font-family: "Segoe UI";
	font-size: 14px; 
	border-radius: 2px;
}

#filesUtilityFrame QComboBox:hover {
	border-style: solid; 
	border-radius: 2px; 
}

#filesUtilityFrame QComboBox:pressed {
	border-style: solid; 
	border-radius: 2px;
}

#filesUtilityFrame QComboBox QAbstractItemView {
    color: white;
    background-color: #878389;
    selection-background-color: #105758; 
    border: none;
}

#filesUtilityFrame QComboBox:focus {
}

#filesUtilityFrame QComboBox::drop-down:button
{
    border: none;
    padding: 0;
    width: 0;
}

#sortByLabel {
	color: #dddddd;
	font-size: 14px;
}

#filesReloadBtn {
	margin-right: 18px;
	
}

#filesReloadBtn:hover {
	border-radius: 4px;
	background: #444444; 
}

#filesReloadBtn:pressed {
	border-radius: 4px;
	background: #111111; 
}

#endOfFileBtn:pressed {
	border-radius: 12px;
	background: #444444;
}

#scrollAreaContents {
	background: #2b2d30;
}

#favoriteItemFrame {
	background: #222222;
	border-radius: 12px;
}

#favoriteNameLabel {
	font-size: 14px;
	color: #ffffff;
}

#favoriteItemFrame QLabel {
	font-size: 16px;
	color: #ffffff;
}

#favoriteItemFrame QPushButton {
	font-size: 14px;
	color: #ffffff;
}

#magnetLinkBtn_2 {
	background: #DA4167;
	padding: 2px 4px;
	border-radius: 4px;
}

#magnetLinkBtn_2:hover {
	background: #BA2147;
}

#magnetLinkBtn_2:pressed {
	background: #EA5177;
}

#downloadBtn_2 {
	background: #879300;
	padding: 2px 4px;
	border-radius: 4px;
}

#downloadBtn_2:hover {
	background: #677300;
}

#downloadBtn_2:pressed {
	background: #97a310;
}

#urlBtn_2 {
	background: #387780;
	padding: 2px 4px;
	border-radius: 4px;
}

#urlBtn_2:hover {
	background: #185760;
}

#urlBtn_2:pressed {
	background: #488790;
}

#removeFavoriteBtn {
	background: #333333;
	border-radius: 6px;
}

#removeFavoriteBtn:hover {
	background: #444444;
}

#removeFavoriteBtn:pressed {
	background: #000000;
}

#verifiedBtn_2 {
	background: #000000;
	padding: 2px 4px;
	border-radius: 4px;
}

#endOfFavoriteBtn:pressed {
	border-radius: 12px;
	background: #444444;
}

#favoritesWidget {
	background: #2d2d30;
}

#favoritesScrollAreaWidgetContents {
	background: #2d2d30;
}

#favoritesMenuTitleBtn {
	font-size: 22px;
	color: #dddddd;
}

#mediaPlayerShowBtn:checked {
	background: #000000;
}

#historyWidget {
	background: #2d2d30;
}

#historyNameLabel {
	font-size: 14px;
	color: #ffffff;
}

#historyItemFrame QLabel {
	font-size: 16px;
	color: #ffffff;
}

#historyItemFrame QPushButton {
	font-size: 14px;
	color: #ffffff;
}

#historyScrollAreaWidgetContents {
	background: #2b2d30;
}

#historyItemFrame {
	background: #222222;
	border-radius: 12px;
}

#historyMenuTitleBtn {
	font-size: 22px;
	color: #dddddd;
}

#historyLinkBtn {
	background: #DA4167;
	padding: 1px 2px;
	border-radius: 4px;
}

#historyLinkBtn:hover {
	background: #BA2147;
}

#historyLinkBtn:pressed {
	background: #EA5177;
}

#deleteHistoryBtn {
	background: #333333;
	border-radius: 6px;
}

#deleteHistoryBtn:hover {
	background: #444444;
}

#deleteHistoryBtn:pressed {
	background: #000000;
}

#endOfHistoryBtn:pressed {
	border-radius: 12px;
	background: #444444;
}

#helpWidget {
	background: #2d2d30;
}

#helpLabel {
	color: #ffffff;
}

#settingWidget {
	background: #2d2d30;
}

#settingLeftScrollWidget {
	background: #2d2d30;
}

#quickSettingsMenuLabel {
    font-size: 22px;
	color: #dddddd;
}

#settingLeftScrollWidget QPushButton {
	font-size: 16px;
	background: #a7b308;
	color: 2d2d30;
	padding: 4px 12px;
	border-bottom-left-radius: 12px;
	border-bottom-right-radius: 12px;
	margin-bottom: 8px;
}

#settingLeftScrollWidget QComboBox {
	height: 21px;
	font-size: 16px;
	background: #a7b308;
	color: 2d2d30;
	padding: 4px 12px;
	border-bottom-left-radius: 12px;
	border-bottom-right-radius: 12px;
	margin-bottom: 8px;
}

#settingLeftScrollWidget QComboBox::drop-down:button
{
    border: none;
    padding: 0;
    width: 0;
}

#settingLeftScrollWidget QPushButton:hover {
	background: #b7d318;
}

#settingLeftScrollWidget QPushButton:pressed {
	background: #97a300;
}

#settingLeftScrollWidget QLabel {
	font-size: 16px;
	background: #222222;
	color: #dddddd;
	padding: 4px 12px;
	border-top-left-radius: 12px;
	border-top-right-radius: 12px;
	margin-top: 8px;
}

#settingsWidget {
	background: #2d2d30;
}

#settingsRightScrollArea {
	background: #2d2d30;
	border-radius: 20px;
}

#settingsRightScrollWidget {
	background: #353539;
	border-radius: 20px;
}

#settingsRightScrollWidget QLabel {
	color: #dddddd;
}

#initAppWidget {
	background: #2d2d30;
}

#initIcon {
    background-image: url(:/icons/loader-dark.gif);
}

#label {
	color: #dddddd;
}

#initLabelBtn2 {
	font-size: 84px;
	text-align: left;
	color: #a7b308;
}

#initLabelBtn2:hover {
	color: #000000;
}

#initLabelBtn {
	text-align: left;
	font-size: 14px;
}
"""
styles_default = """
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

#scrollAreaContents {
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

#filesPathInput {
	font-size: 14px;
	background: #1f2023;
	color: #dddddd;
	border-top-left-radius: 4px;
	border-bottom-left-radius: 4px;
	padding: 4px 10px;
	margin-left: 8px;
}

#filesPathDropdownBtn {
	background: #1f2023;
	color: #dddddd;
	border-left: 1px solid #3b3d40;
	border-top-right-radius: 4px;
	border-bottom-right-radius: 4px;
	margin-right: 6px;
}

#filesPathDropdownBtn:hover {
	background: #26282d;
}

#filesPathDropdownBtn:pressed {
	background: #111111;
}

QMenu {
	background: #2b2d30;
	color: #dddddd;
	border: 1px solid #3b3d40;
	border-radius: 6px;
	padding: 2px 6px;
}

QMenu::item {
	font-size: 13px;
	min-height: 18px;
	padding: 2px 18px 2px 10px;
	border-radius: 4px;
}

QMenu::icon {
	padding-left: 6px;
	padding-right: 6px;
}

QMenu::item:selected {
	background: #387780;
	color: #ffffff;
}

QMenu::item:disabled {
	color: #777777;
}

QMenu::separator {
	height: 1px;
	background: #3b3d40;
	margin: 2px 6px;
}

#filesUtilityFrame QPushButton {
	border-radius: 4px;
	color: #dddddd;
}

#filesUtilityFrame QPushButton:hover {
	background: #444444;
}

#filesUtilityFrame QPushButton:pressed {
	background: #111111;
}

#fileManagerRow {
	background: #202124;
	border-radius: 8px;
}

#fileManagerRow:hover {
	background: #26282d;
}

#fileManagerOpenBtn {
	background: #2b2d30;
	border-radius: 6px;
}

#fileManagerNameLabel {
	font-size: 15px;
	font-weight: 600;
	color: #ffffff;
}

#fileManagerMetaLabel,
#fileEmptyStateLabel {
	font-size: 12px;
	color: #b8b8b8;
}

#fileManagerRenameInput {
	font-size: 15px;
	font-weight: 600;
	color: #ffffff;
	background: #111214;
	border: 1px solid #387780;
	border-radius: 4px;
	padding: 2px 6px;
}

#filePropertiesDialog {
	background: #2b2d30;
}

#filePropertiesHeader {
	background: transparent;
}

#filePropertiesHeaderTitle {
	color: #dddddd;
	font-size: 13px;
	font-weight: 600;
}

#filePropertiesDialog QLabel {
	color: #dddddd;
	font-size: 13px;
}

#filePropertiesTitle {
	color: #ffffff;
	font-size: 18px;
	font-weight: 600;
}

#filePropertiesCloseBtn {
	color: #ffffff;
	background: #387780;
	border-radius: 4px;
	font-size: 13px;
	padding: 0px 10px;
}

#filePropertiesCloseBtn:hover {
	background: #185760;
}

#filePropertiesTitleCloseBtn {
	background: transparent;
	border-radius: 4px;
}

#filePropertiesTitleCloseBtn:hover {
	background: #444444;
}

#fileEmptyStateFrame {
	background: #202124;
	border-radius: 8px;
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

#torrentManagerWidget,
#torrentRightPane,
#torrentAddDialog,
#torrentMagnetDialog {
	background: #2b2d30;
}

#torrentToolbar,
#torrentSidebar,
#torrentAddHeader,
#torrentAddFooter,
#torrentAddOptionsPane,
#torrentAddFilesPane,
#torrentFilesTab,
#torrentOverviewTab {
	background: #2b2d30;
}

QSplitter#torrentMainSplitter::handle,
QSplitter#torrentAddSplitter::handle {
	background: #2b2d30;
	border: 0px;
	width: 4px;
}

QSplitter#torrentDetailSplitter::handle {
	background: #2b2d30;
	border-top: 2px solid #3b3d40;
	border-bottom: 1px solid #1f2023;
	height: 6px;
}

QSplitter#torrentDetailSplitter::handle:hover {
	border-top: 2px solid #387780;
}

#torrentSidebar {
	border-right: 1px solid #3b3d40;
	border-radius: 6px;
}

#torrentSidebarTitle,
#torrentAddSectionTitle,
#torrentSectionTitle {
	color: #a7b308;
	font-size: 12px;
	font-weight: 700;
}

#torrentSidebarButton {
	color: #dddddd;
	text-align: left;
	font-size: 12px;
	padding: 4px 6px;
	border-radius: 4px;
}

#torrentSidebarButton[active="true"],
#torrentSidebarButton:checked {
	background: #387780;
	color: #ffffff;
	font-weight: 600;
}

#torrentSidebarButton:hover,
#torrentToolButton:hover,
#torrentMiniButton:hover,
#torrentSecondaryButton:hover {
	background: #3b3d40;
}

#torrentSidebarButton:pressed,
#torrentToolButton:pressed,
#torrentMiniButton:pressed,
#torrentSecondaryButton:pressed {
	background: #111111;
}

#torrentToolButton {
	background: #1f2023;
	border: 1px solid #3b3d40;
	border-radius: 5px;
	min-width: 30px;
	min-height: 28px;
}

#torrentFilterInput,
#torrentAddPathInput {
	background: #1f2023;
	color: #dddddd;
	border: 1px solid #3b3d40;
	border-radius: 4px;
	font-size: 12px;
	padding: 4px 8px;
}

#torrentFilterCombo {
	min-width: 76px;
	text-align: center;
	padding-left: 4px;
	padding-right: 4px;
	color: #dddddd;
	background: #2b2d30;
	font-family: "Segoe UI";
	font-size: 14px;
	border: none;
	border-radius: 2px;
}

#torrentFilterCombo QAbstractItemView {
	color: white;
	background-color: #878389;
	selection-background-color: #105758;
	border: none;
}

#torrentFilterCombo::drop-down:button {
	border: none;
	padding: 0;
	width: 0;
}

#torrentTable,
#torrentOverviewTable,
#torrentFilesTree,
#torrentAddFilesTree,
#torrentTrackersTable,
#torrentPeersTable,
#torrentLogsTable {
	background: #202124;
	alternate-background-color: #26282c;
	color: #dddddd;
	border: 1px solid #3b3d40;
	border-radius: 5px;
	font-size: 12px;
	gridline-color: #3b3d40;
}

#torrentTable::item,
#torrentOverviewTable::item,
#torrentFilesTree::item,
#torrentAddFilesTree::item,
#torrentTrackersTable::item,
#torrentPeersTable::item,
#torrentLogsTable::item {
	padding-top: 1px;
	padding-bottom: 1px;
}

#torrentTable::item:selected,
#torrentOverviewTable::item:selected,
#torrentFilesTree::item:selected,
#torrentAddFilesTree::item:selected,
#torrentTrackersTable::item:selected,
#torrentPeersTable::item:selected,
#torrentLogsTable::item:selected {
	background: #387780;
	color: #ffffff;
}

QHeaderView#torrentHeader,
QTableCornerButton::section {
	background: #2f3136;
	color: #dddddd;
	border: 0px;
}

QHeaderView#torrentHeader::section,
QTableWidget#torrentTable QHeaderView::section,
QTableWidget#torrentOverviewTable QHeaderView::section,
QTreeWidget#torrentFilesTree QHeaderView::section,
QTreeWidget#torrentAddFilesTree QHeaderView::section,
QTableWidget#torrentTrackersTable QHeaderView::section,
QTableWidget#torrentPeersTable QHeaderView::section,
QTableWidget#torrentLogsTable QHeaderView::section {
	background: #2f3136;
	color: #dddddd;
	font-size: 12px;
	font-family: "Segoe UI";
	font-weight: 600;
	padding: 1px 6px;
	min-height: 18px;
	border: 0px;
	border-right: 1px solid #3b3d40;
	border-bottom: 1px solid #3b3d40;
}

QHeaderView#torrentHeader::section:pressed,
QHeaderView#torrentHeader::section:checked {
	background: #363941;
	color: #ffffff;
}

QTableWidget#torrentTable QScrollBar:horizontal,
QTableWidget#torrentOverviewTable QScrollBar:horizontal,
QTableWidget#torrentTrackersTable QScrollBar:horizontal,
QTableWidget#torrentPeersTable QScrollBar:horizontal,
QTableWidget#torrentLogsTable QScrollBar:horizontal,
QTreeWidget#torrentFilesTree QScrollBar:horizontal,
QTreeWidget#torrentAddFilesTree QScrollBar:horizontal,
QScrollArea#torrentOverviewScroll QScrollBar:horizontal {
	background: #202124;
	height: 8px;
	margin: 0px;
}

QTableWidget#torrentTable QScrollBar:vertical,
QTableWidget#torrentOverviewTable QScrollBar:vertical,
QTableWidget#torrentTrackersTable QScrollBar:vertical,
QTableWidget#torrentPeersTable QScrollBar:vertical,
QTableWidget#torrentLogsTable QScrollBar:vertical,
QTreeWidget#torrentFilesTree QScrollBar:vertical,
QTreeWidget#torrentAddFilesTree QScrollBar:vertical,
QScrollArea#torrentOverviewScroll QScrollBar:vertical {
	background: #202124;
	width: 8px;
	margin: 0px;
}

QTableWidget#torrentTable QScrollBar::handle,
QTableWidget#torrentOverviewTable QScrollBar::handle,
QTableWidget#torrentTrackersTable QScrollBar::handle,
QTableWidget#torrentPeersTable QScrollBar::handle,
QTableWidget#torrentLogsTable QScrollBar::handle,
QTreeWidget#torrentFilesTree QScrollBar::handle,
QTreeWidget#torrentAddFilesTree QScrollBar::handle,
QScrollArea#torrentOverviewScroll QScrollBar::handle {
	background: #3b3d40;
	border-radius: 3px;
	min-height: 18px;
	min-width: 18px;
}

QTableWidget#torrentTable QScrollBar::add-line,
QTableWidget#torrentTable QScrollBar::sub-line,
QTableWidget#torrentOverviewTable QScrollBar::add-line,
QTableWidget#torrentOverviewTable QScrollBar::sub-line,
QTableWidget#torrentTrackersTable QScrollBar::add-line,
QTableWidget#torrentTrackersTable QScrollBar::sub-line,
QTableWidget#torrentPeersTable QScrollBar::add-line,
QTableWidget#torrentPeersTable QScrollBar::sub-line,
QTableWidget#torrentLogsTable QScrollBar::add-line,
QTableWidget#torrentLogsTable QScrollBar::sub-line,
QTreeWidget#torrentFilesTree QScrollBar::add-line,
QTreeWidget#torrentFilesTree QScrollBar::sub-line,
QTreeWidget#torrentAddFilesTree QScrollBar::add-line,
QTreeWidget#torrentAddFilesTree QScrollBar::sub-line,
QScrollArea#torrentOverviewScroll QScrollBar::add-line,
QScrollArea#torrentOverviewScroll QScrollBar::sub-line {
	width: 0px;
	height: 0px;
}

QTableWidget#torrentTable QScrollBar::add-page,
QTableWidget#torrentTable QScrollBar::sub-page,
QTableWidget#torrentOverviewTable QScrollBar::add-page,
QTableWidget#torrentOverviewTable QScrollBar::sub-page,
QTableWidget#torrentTrackersTable QScrollBar::add-page,
QTableWidget#torrentTrackersTable QScrollBar::sub-page,
QTableWidget#torrentPeersTable QScrollBar::add-page,
QTableWidget#torrentPeersTable QScrollBar::sub-page,
QTableWidget#torrentLogsTable QScrollBar::add-page,
QTableWidget#torrentLogsTable QScrollBar::sub-page,
QTreeWidget#torrentFilesTree QScrollBar::add-page,
QTreeWidget#torrentFilesTree QScrollBar::sub-page,
QTreeWidget#torrentAddFilesTree QScrollBar::add-page,
QTreeWidget#torrentAddFilesTree QScrollBar::sub-page,
QScrollArea#torrentOverviewScroll QScrollBar::add-page,
QScrollArea#torrentOverviewScroll QScrollBar::sub-page {
	background: #202124;
}

#torrentDetailTabs::pane {
	border: 1px solid #3b3d40;
	background: #232528;
	border-radius: 5px;
}

#torrentDetailTabs QTabBar::tab {
	background: #1f2023;
	color: #dddddd;
	font-size: 12px;
	padding: 3px 9px;
	min-height: 20px;
	margin-right: 3px;
	border-top-left-radius: 4px;
	border-top-right-radius: 4px;
}

#torrentDetailTabs QTabBar::tab:selected {
	background: #387780;
	color: #ffffff;
}

#torrentRowProgress,
#torrentOverviewProgress,
#torrentMetadataProgress {
	background: #1a1b1e;
	color: #dddddd;
	border: 1px solid #3b3d40;
	border-radius: 4px;
	font-size: 11px;
	text-align: center;
}

#torrentRowProgress::chunk,
#torrentOverviewProgress::chunk,
#torrentMetadataProgress::chunk {
	background: #a7b308;
	border-radius: 3px;
}

#torrentInfoSection,
#torrentAddSection {
	background: #2b2d30;
	border: 1px solid #3b3d40;
	border-radius: 6px;
}

#torrentInfoLabel,
#torrentInfoValue,
#torrentAddInfoLabel,
#torrentAddInfoValue,
#torrentAddStatusLabel,
#torrentAddCheck {
	color: #dddddd;
	font-size: 12px;
}

#torrentInfoLabel,
#torrentAddInfoLabel {
	font-weight: 400;
}

#torrentAddTitle {
	color: #ffffff;
	font-size: 16px;
	font-weight: 700;
}

#torrentAddCloseBtn,
#torrentAddBrowseBtn {
	background: #1f2023;
	border-radius: 5px;
	min-width: 28px;
	min-height: 28px;
}

#torrentAddCloseBtn:hover {
	background: #dd0000;
}

#torrentPrimaryButton {
	background: #387780;
	color: #ffffff;
	font-size: 13px;
	padding: 5px 14px;
	border-radius: 5px;
}

#torrentPrimaryButton:hover {
	background: #439099;
}

#torrentSecondaryButton,
#torrentMiniButton {
	background: #1f2023;
	color: #dddddd;
	border: 1px solid #3b3d40;
	font-size: 12px;
	padding: 4px 9px;
	border-radius: 5px;
}
"""

styles_retro = """
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
    background: #905522;
    border-radius: 2px;
}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #b07542;
    border-radius: 2px;
    min-height: 20px;
    min-width: 20px;
}

QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
    background: #c44900;
    border-radius: 2px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    background: transparent;
}

#leftMenuBar QPushButton {
	font-size: 18px;
	color: #ffffff;
	text-align: left;
	padding-left: 12px;
	padding-right: 12px;
	margin: 2px 2px;
}

#leftMenuBar QPushButton:hover {
	background: #b07542;
	border-radius: 4px;
}

#mainBtnWidget QPushButton:focus {
	background: #32746d;
	border-radius: 4px;
}

#leftMenuBar QPushButton:pressed {
	background: #ff8600;
	border-radius: 4px;
}

#someMoreBtnFrame QToolButton:hover {
	background: #3f4145;
	border-radius: 12px;
}

#someMoreBtnFrame QToolButton:pressed {
	background: #ff8600;
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
	background: #c08552;
}

#centerMainMenu {
	background: #ffc49b;
}

#headerContainer {
	background: #b07542;
}

#footer {
	background: #b07542;
	border-top: 1px solid #516335;
}

#footer QPushButton {
	font-size: 11px;
}

#footer QLabel{
	background: #516335;
	margin: 3px 3px; 
	color: #00dddd;
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
	border-bottom: 1px solid #516335;
}

#leftMenuBar {
	border-right: 1px solid #516335;
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
	background: #f2af29;
	border-radius: 12px;
}

#notificationTitleLabel {
	font-size: 16px;
	color: #080808;
}

#notificationTextLabel {
	font-size: 16px;
	color: #080808;
}

#searchWidget {
	background: #ffc49b;
}

#scrollAreaContents {
	background: #ffc49b;
	border-radius: 12px;
}

#searchScrollArea {
	background: #ffc49b;
	border-radius: 12px;
}

#searchInputText {
	font-size: 18px;
	background: #d9dcd6;
	color: #080808;
	padding: 0px 12px;
	border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}

#searchBtn {
	background-color: #8e9aaf;
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

#searchOutputFrame {
	background: #e9f5db;
	border-radius: 12px;
}

#searchOutputFrame QLabel {
	font-size: 16px;
	color: #000000;
}

#searchOutputBtnsFrame QPushButton {
	font-size: 14px;
	color: #dddddd;
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

#endOfSearchBtn {
	color: 080808;
}

#endOfSearchBtn:pressed {
	border-radius: 12px;
	background: #444444;
}

#filesStack {
	background: #ffc49b;
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
    background: #545454;
    border: 1px solid #516335;
    height: 6px;
    border-radius: 3px;
}

#mediaPlayBtn {
	background: #545454;
	border-radius: 24px;
	padding-left: 6px;
}

#mediaNextBtn {
	background: #545454;
	border-radius: 16px;
}

#mediaPreviousBtn {
	background: #545454;
	border-radius: 16px;
}

#seekForwardBtn {
	background: #545454;
	border-radius: 16px;
}

#seekBackwardBtn {
	background: #545454;
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
    background: #545454;
    border: 1px solid #516335;
    height: 6px;
    border-radius: 3px;
}

#mediaLeftSideControlFrames QComboBox {
	padding-left: 4px;
    color: #dddddd;
	background: #545454;
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
	background: #516335;
	border-radius: 4px;
}

#mediaRightSideControlFrames QPushButton:hover {
	background: #516335;
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
	background: #ffc49b;
}

#filesPathInput {
	font-size: 14px;
	background: #e9f5db;
	color: #080808;
	border-top-left-radius: 4px;
	border-bottom-left-radius: 4px;
	padding: 4px 10px;
	margin-left: 8px;
}

#filesPathDropdownBtn {
	background: #e9f5db;
	color: #080808;
	border-left: 1px solid #d8a06c;
	border-top-right-radius: 4px;
	border-bottom-right-radius: 4px;
	margin-right: 6px;
}

#filesPathDropdownBtn:hover {
	background: #f3ffe6;
}

#filesPathDropdownBtn:pressed {
	background: #d8a06c;
}

QMenu {
	background: #fff7e7;
	color: #080808;
	border: 1px solid #d8a06c;
	border-radius: 6px;
	padding: 2px 6px;
}

QMenu::item {
	font-size: 13px;
	min-height: 18px;
	padding: 2px 18px 2px 10px;
	border-radius: 4px;
}

QMenu::icon {
	padding-left: 6px;
	padding-right: 6px;
}

QMenu::item:selected {
	background: #b07542;
	color: #ffffff;
}

QMenu::item:disabled {
	color: #777777;
}

QMenu::separator {
	height: 1px;
	background: #d8a06c;
	margin: 2px 6px;
}

#filesUtilityFrame QPushButton {
	border-radius: 4px;
	color: #080808;
}

#filesUtilityFrame QPushButton:hover {
	background: #d8a06c;
}

#filesUtilityFrame QPushButton:pressed {
	background: #b07542;
}

#fileManagerRow {
	background: #e9f5db;
	border-radius: 8px;
}

#fileManagerRow:hover {
	background: #f3ffe6;
}

#fileManagerOpenBtn {
	background: #ffc49b;
	border-radius: 6px;
}

#fileManagerNameLabel {
	font-size: 15px;
	font-weight: 600;
	color: #000000;
}

#fileManagerMetaLabel,
#fileEmptyStateLabel {
	font-size: 12px;
	color: #313131;
}

#fileManagerRenameInput {
	font-size: 15px;
	font-weight: 600;
	color: #080808;
	background: #ffffff;
	border: 1px solid #b07542;
	border-radius: 4px;
	padding: 2px 6px;
}

#filePropertiesDialog {
	background: #ffc49b;
}

#filePropertiesHeader {
	background: transparent;
}

#filePropertiesHeaderTitle {
	color: #080808;
	font-size: 13px;
	font-weight: 600;
}

#filePropertiesDialog QLabel {
	color: #080808;
	font-size: 13px;
}

#filePropertiesTitle {
	color: #000000;
	font-size: 18px;
	font-weight: 600;
}

#filePropertiesCloseBtn {
	color: #ffffff;
	background: #b07542;
	border-radius: 4px;
	font-size: 13px;
	padding: 0px 10px;
}

#filePropertiesCloseBtn:hover {
	background: #905522;
}

#filePropertiesTitleCloseBtn {
	background: transparent;
	border-radius: 4px;
}

#filePropertiesTitleCloseBtn:hover {
	background: #d8a06c;
}

#fileEmptyStateFrame {
	background: #e9f5db;
	border-radius: 8px;
}

#eachFileFrame {
	background: #e9f5db;
	border-radius: 12px;
}

#eachFileFrame QLabel {
	font-size: 16px;
	color: #000000;
}

#eachFileFrame QPushButton {
	font-size: 12px;
	color: #000000;
}

#fileStackTitleBtn {
	font-size: 22px;
	color: #080808;
}

#playFileBtn {
	border-radius: 4px;
	background: #b07542; 
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
    color: #080808;
	background: #ffc49b;
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
	color: #080808;
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

#favoriteItemFrame {
	background: #e9f5db;
	border-radius: 12px;
}

#favoriteNameLabel {
	font-size: 14px;
	color: #000000;
}

#favoriteItemFrame QLabel {
	font-size: 16px;
	color: #000000;
}

#favoriteBtnFrame QPushButton {
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
	background: #b07542;
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
	background: #ffc49b;
}

#favoritesScrollAreaWidgetContents {
	background: #ffc49b;
}

#favoritesMenuTitleBtn {
	font-size: 22px;
	color: #080808;
}

#mediaPlayerShowBtn:checked {
	background: #000000;
}

#historyWidget {
	background: #ffc49b;
}

#historyNameLabel {
	font-size: 14px;
	color: #000000;
}

#historyItemFrame QLabel {
	font-size: 16px;
	color: #000000;
}

#historyItemFrame QPushButton {
	font-size: 14px;
	color: #ffffff;
}

#historyScrollAreaWidgetContents {
	background: #ffc49b;
}

#historyItemFrame {
	background: #e9f5db;
	border-radius: 12px;
}

#historyMenuTitleBtn {
	font-size: 18px;
	color: #080808;
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
	background: #b07542;
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
	background: #ffc49b;
}

#helpLabel {
	color: #ffffff;
}

#settingWidget {
	background: #ffc49b;
}

#settingLeftScrollWidget {
	background: #ffc49b;
}

#quickSettingsMenuLabel {
    font-size: 22px;
	color: #080808;
}

#settingLeftScrollWidget QPushButton {
	font-size: 16px;
	background: #fa9500;
	color: ffc49b;
	padding: 4px 12px;
	border-bottom-left-radius: 12px;
	border-bottom-right-radius: 12px;
	margin-bottom: 8px;
}

#settingLeftScrollWidget QComboBox {
	height: 21px;
	font-size: 16px;
	background: #fa9500;
	color: ffc49b;
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
	background: #b07542;
	color: #080808;
	padding: 4px 12px;
	border-top-left-radius: 12px;
	border-top-right-radius: 12px;
	margin-top: 8px;
}

#settingsWidget {
	background: #ffc49b;
}

#settingsRightScrollArea {
	background: #ffc49b;
	border-radius: 20px;
}

#settingsRightScrollWidget {
	background: #ffe4bb;
	border-radius: 20px;
}

#settingsRightScrollWidget QLabel {
	color: #080808;
}

#initAppWidget {
	background: #ffc49b;
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
	color: #037971;
	text-align: left;
	font-size: 14px;
}

#mediaPlayerWidget {
	background: #f7efe3;
	border: 1px solid #d8a06c;
	border-radius: 46px;
}

#mediaProgressFrame QLabel,
#mediaProgressFrame QPushButton,
#mediaPlayerWidget QPushButton {
	color: #080808;
}

#mediaPlayBtn,
#mediaNextBtn,
#mediaPreviousBtn,
#seekForwardBtn,
#seekBackwardBtn {
	background: #fff7e7;
}

#mediaLeftSideControlFrames QComboBox {
	color: #080808;
	background: #fff7e7;
	border: 8px solid #f7efe3;
}

#mediaLeftSideControlFrames QComboBox QAbstractItemView {
	color: #080808;
	background-color: #fff7e7;
	selection-background-color: #b07542;
}

#mediaProgressFrame QSlider::groove:horizontal,
#mediaRightSideControlFrames QSlider::groove:horizontal {
	background: #d8c7a8;
}

#mediaProgressFrame QSlider::add-page:horizontal,
#mediaRightSideControlFrames QSlider::add-page:horizontal {
	background: #fff7e7;
	border: 1px solid #d8a06c;
}

#torrentManagerWidget,
#torrentRightPane,
#torrentAddDialog,
#torrentMagnetDialog {
	background: #f6d7a8;
}

#torrentToolbar,
#torrentSidebar,
#torrentAddHeader,
#torrentAddFooter,
#torrentAddOptionsPane,
#torrentAddFilesPane,
#torrentFilesTab,
#torrentOverviewTab {
	background: #f6d7a8;
}

QSplitter#torrentMainSplitter::handle,
QSplitter#torrentAddSplitter::handle {
	background: #f6d7a8;
	border: 0px;
	width: 4px;
}

QSplitter#torrentDetailSplitter::handle {
	background: #f6d7a8;
	border-top: 2px solid #d8a06c;
	border-bottom: 1px solid #efc58d;
	height: 6px;
}

QSplitter#torrentDetailSplitter::handle:hover {
	border-top: 2px solid #b07542;
}

#torrentSidebar {
	border-right: 1px solid #d8a06c;
	border-radius: 6px;
}

#torrentSidebarTitle,
#torrentAddSectionTitle,
#torrentSectionTitle {
	color: #7b3f10;
	font-size: 12px;
	font-weight: 700;
}

#torrentSidebarButton {
	color: #080808;
	text-align: left;
	font-size: 12px;
	padding: 4px 6px;
	border-radius: 4px;
}

#torrentSidebarButton[active="true"],
#torrentSidebarButton:checked {
	background: #b07542;
	color: #ffffff;
	font-weight: 600;
}

#torrentSidebarButton:hover,
#torrentToolButton:hover,
#torrentMiniButton:hover,
#torrentSecondaryButton:hover {
	background: #efc58d;
}

#torrentSidebarButton:pressed,
#torrentToolButton:pressed,
#torrentMiniButton:pressed,
#torrentSecondaryButton:pressed {
	background: #b07542;
}

#torrentToolButton {
	background: #fff7e7;
	border: 1px solid #d8a06c;
	border-radius: 5px;
	min-width: 30px;
	min-height: 28px;
}

#torrentFilterInput,
#torrentAddPathInput {
	background: #fff7e7;
	color: #080808;
	border: 1px solid #d8a06c;
	border-radius: 4px;
	font-size: 12px;
	padding: 4px 8px;
}

#torrentFilterCombo {
	min-width: 76px;
	text-align: center;
	padding-left: 4px;
	padding-right: 4px;
	color: #080808;
	background: #ffc49b;
	font-family: "Segoe UI";
	font-size: 14px;
	border: none;
	border-radius: 2px;
}

#torrentFilterCombo QAbstractItemView {
	color: white;
	background-color: #878389;
	selection-background-color: #105758;
	border: none;
}

#torrentFilterCombo::drop-down:button {
	border: none;
	padding: 0;
	width: 0;
}

#torrentTable,
#torrentOverviewTable,
#torrentFilesTree,
#torrentAddFilesTree,
#torrentTrackersTable,
#torrentPeersTable,
#torrentLogsTable {
	background: #fff7e7;
	alternate-background-color: #f6e5c9;
	color: #080808;
	border: 1px solid #d8a06c;
	border-radius: 5px;
	font-size: 12px;
	gridline-color: #d8a06c;
}

#torrentTable::item,
#torrentOverviewTable::item,
#torrentFilesTree::item,
#torrentAddFilesTree::item,
#torrentTrackersTable::item,
#torrentPeersTable::item,
#torrentLogsTable::item {
	padding-top: 1px;
	padding-bottom: 1px;
}

#torrentTable::item:selected,
#torrentOverviewTable::item:selected,
#torrentFilesTree::item:selected,
#torrentAddFilesTree::item:selected,
#torrentTrackersTable::item:selected,
#torrentPeersTable::item:selected,
#torrentLogsTable::item:selected {
	background: #b07542;
	color: #ffffff;
}

QHeaderView#torrentHeader,
QTableCornerButton::section {
	background: #efc58d;
	color: #080808;
	border: 0px;
}

QHeaderView#torrentHeader::section,
QTableWidget#torrentTable QHeaderView::section,
QTableWidget#torrentOverviewTable QHeaderView::section,
QTreeWidget#torrentFilesTree QHeaderView::section,
QTreeWidget#torrentAddFilesTree QHeaderView::section,
QTableWidget#torrentTrackersTable QHeaderView::section,
QTableWidget#torrentPeersTable QHeaderView::section,
QTableWidget#torrentLogsTable QHeaderView::section {
	background: #efc58d;
	color: #080808;
	font-size: 12px;
	font-family: "Segoe UI";
	font-weight: 600;
	padding: 1px 6px;
	min-height: 18px;
	border: 0px;
	border-right: 1px solid #d8a06c;
	border-bottom: 1px solid #d8a06c;
}

QHeaderView#torrentHeader::section:pressed,
QHeaderView#torrentHeader::section:checked {
	background: #e2b276;
	color: #080808;
}

QTableWidget#torrentTable QScrollBar:horizontal,
QTableWidget#torrentOverviewTable QScrollBar:horizontal,
QTableWidget#torrentTrackersTable QScrollBar:horizontal,
QTableWidget#torrentPeersTable QScrollBar:horizontal,
QTableWidget#torrentLogsTable QScrollBar:horizontal,
QTreeWidget#torrentFilesTree QScrollBar:horizontal,
QTreeWidget#torrentAddFilesTree QScrollBar:horizontal,
QScrollArea#torrentOverviewScroll QScrollBar:horizontal {
	background: #fff7e7;
	height: 8px;
	margin: 0px;
}

QTableWidget#torrentTable QScrollBar:vertical,
QTableWidget#torrentOverviewTable QScrollBar:vertical,
QTableWidget#torrentTrackersTable QScrollBar:vertical,
QTableWidget#torrentPeersTable QScrollBar:vertical,
QTableWidget#torrentLogsTable QScrollBar:vertical,
QTreeWidget#torrentFilesTree QScrollBar:vertical,
QTreeWidget#torrentAddFilesTree QScrollBar:vertical,
QScrollArea#torrentOverviewScroll QScrollBar:vertical {
	background: #fff7e7;
	width: 8px;
	margin: 0px;
}

QTableWidget#torrentTable QScrollBar::handle,
QTableWidget#torrentOverviewTable QScrollBar::handle,
QTableWidget#torrentTrackersTable QScrollBar::handle,
QTableWidget#torrentPeersTable QScrollBar::handle,
QTableWidget#torrentLogsTable QScrollBar::handle,
QTreeWidget#torrentFilesTree QScrollBar::handle,
QTreeWidget#torrentAddFilesTree QScrollBar::handle,
QScrollArea#torrentOverviewScroll QScrollBar::handle {
	background: #d8a06c;
	border-radius: 3px;
	min-height: 18px;
	min-width: 18px;
}

QTableWidget#torrentTable QScrollBar::add-line,
QTableWidget#torrentTable QScrollBar::sub-line,
QTableWidget#torrentOverviewTable QScrollBar::add-line,
QTableWidget#torrentOverviewTable QScrollBar::sub-line,
QTableWidget#torrentTrackersTable QScrollBar::add-line,
QTableWidget#torrentTrackersTable QScrollBar::sub-line,
QTableWidget#torrentPeersTable QScrollBar::add-line,
QTableWidget#torrentPeersTable QScrollBar::sub-line,
QTableWidget#torrentLogsTable QScrollBar::add-line,
QTableWidget#torrentLogsTable QScrollBar::sub-line,
QTreeWidget#torrentFilesTree QScrollBar::add-line,
QTreeWidget#torrentFilesTree QScrollBar::sub-line,
QTreeWidget#torrentAddFilesTree QScrollBar::add-line,
QTreeWidget#torrentAddFilesTree QScrollBar::sub-line,
QScrollArea#torrentOverviewScroll QScrollBar::add-line,
QScrollArea#torrentOverviewScroll QScrollBar::sub-line {
	width: 0px;
	height: 0px;
}

QTableWidget#torrentTable QScrollBar::add-page,
QTableWidget#torrentTable QScrollBar::sub-page,
QTableWidget#torrentOverviewTable QScrollBar::add-page,
QTableWidget#torrentOverviewTable QScrollBar::sub-page,
QTableWidget#torrentTrackersTable QScrollBar::add-page,
QTableWidget#torrentTrackersTable QScrollBar::sub-page,
QTableWidget#torrentPeersTable QScrollBar::add-page,
QTableWidget#torrentPeersTable QScrollBar::sub-page,
QTableWidget#torrentLogsTable QScrollBar::add-page,
QTableWidget#torrentLogsTable QScrollBar::sub-page,
QTreeWidget#torrentFilesTree QScrollBar::add-page,
QTreeWidget#torrentFilesTree QScrollBar::sub-page,
QTreeWidget#torrentAddFilesTree QScrollBar::add-page,
QTreeWidget#torrentAddFilesTree QScrollBar::sub-page,
QScrollArea#torrentOverviewScroll QScrollBar::add-page,
QScrollArea#torrentOverviewScroll QScrollBar::sub-page {
	background: #fff7e7;
}

#torrentDetailTabs::pane {
	border: 1px solid #d8a06c;
	background: #f7efe3;
	border-radius: 5px;
}

#torrentDetailTabs QTabBar::tab {
	background: #fff7e7;
	color: #080808;
	font-size: 12px;
	padding: 3px 9px;
	min-height: 20px;
	margin-right: 3px;
	border-top-left-radius: 4px;
	border-top-right-radius: 4px;
}

#torrentDetailTabs QTabBar::tab:selected {
	background: #b07542;
	color: #ffffff;
}

#torrentRowProgress,
#torrentOverviewProgress,
#torrentMetadataProgress {
	background: #fff7e7;
	color: #080808;
	border: 1px solid #d8a06c;
	border-radius: 4px;
	font-size: 11px;
	text-align: center;
}

#torrentRowProgress::chunk,
#torrentOverviewProgress::chunk,
#torrentMetadataProgress::chunk {
	background: #037971;
	border-radius: 3px;
}

#torrentInfoSection,
#torrentAddSection {
	background: #fff7e7;
	border: 1px solid #d8a06c;
	border-radius: 6px;
}

#torrentInfoLabel,
#torrentInfoValue,
#torrentAddInfoLabel,
#torrentAddInfoValue,
#torrentAddStatusLabel,
#torrentAddCheck {
	color: #080808;
	font-size: 12px;
}

#torrentInfoLabel,
#torrentAddInfoLabel {
	font-weight: 400;
}

#torrentAddTitle {
	color: #080808;
	font-size: 16px;
	font-weight: 700;
}

#torrentAddCloseBtn,
#torrentAddBrowseBtn {
	background: #fff7e7;
	border-radius: 5px;
	min-width: 28px;
	min-height: 28px;
}

#torrentAddCloseBtn:hover {
	background: #cc3d2f;
}

#torrentPrimaryButton {
	background: #037971;
	color: #ffffff;
	font-size: 13px;
	padding: 5px 14px;
	border-radius: 5px;
}

#torrentPrimaryButton:hover {
	background: #0b8c83;
}

#torrentSecondaryButton,
#torrentMiniButton {
	background: #fff7e7;
	color: #080808;
	border: 1px solid #d8a06c;
	font-size: 12px;
	padding: 4px 9px;
	border-radius: 5px;
}
"""

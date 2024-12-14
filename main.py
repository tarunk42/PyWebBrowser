from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MyWebBrowser(QMainWindow):
    def __init__(self):
        super(MyWebBrowser, self).__init__()
        self.setWindowTitle('Web Browser')

        # Main layout and central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL")
        self.url_bar.setMaximumHeight(30)

        # Buttons
        self.go_btn = QPushButton("Go")
        self.go_btn.setMinimumHeight(30)

        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)

        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)

        # Adding widgets to the horizontal layout
        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)

        # WebEngine view
        self.browser = QWebEngineView()

        # Adding layouts to the main layout
        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.central_widget.setLayout(self.layout)

        # Default URL
        self.browser.setUrl(QUrl("http://google.com"))

        # Button actions
        self.go_btn.clicked.connect(self.navigate_to_url)
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))


app = QApplication([])
window = MyWebBrowser()
window.show()
app.exec_()

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings


class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        # Filter out specific warnings or errors
        if "Self-XSS" in message or "Uncaught (in promise) cancel" in message:
            return  # Ignore these specific messages
        print(f"JS Error [{level}]: {message} (Line {line_number} in {source_id})")


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
        self.browser.setPage(CustomWebEnginePage(self.browser))

        # Enable JavaScript and other settings
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)

        # Adding layouts to the main layout
        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.central_widget.setLayout(self.layout)

        # Default URL
        self.browser.setUrl(QUrl("https://google.com"))

        # Button actions
        self.go_btn.clicked.connect(self.navigate_to_url)
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Update URL bar when navigating
        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url  # Default to HTTPS for security
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())


app = QApplication([])
window = MyWebBrowser()
window.show()
app.exec_()

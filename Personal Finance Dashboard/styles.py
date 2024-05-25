duskStyle = """
QWidget {
    background-color: #282a36; /* Dark grey background */
    color: #f8f8f2; /* Bright text */
    font: 12pt "Arial";
}

QLabel, QCheckBox {
    color: #bd93f9; /* Soft purple */
}

QLineEdit, QDateEdit, QComboBox {
    background-color: #44475a;
    color: #f8f8f2;
    border: 1px solid #6272a4; /* Greyish blue border */
}

QPushButton {
    background-color: #6272a4; /* Greyish blue */
    color: #f8f8f2;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #bd93f9; /* Soft purple border */
    padding: 6px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #50fa7b; /* Bright green when hovered */
    border-color: #ff79c6; /* Pink border when hovered */
}

QPushButton:pressed {
    background-color: #ff5555; /* Bright red when pressed */
    border-color: #f1fa8c; /* Bright yellow border when pressed */
}

QTabBar::tab {
    background-color: #44475a;
    color: #f8f8f2;
    padding: 10px;
    margin: 2px;
}

QTabBar::tab:selected {
    background-color: #6272a4;
    color: #50fa7b;
}

QTableWidget {
    gridline-color: #bd93f9;
}

QHeaderView::section {
    background-color: #6272a4;
    color: #f8f8f2;
    border: 1px solid #bd93f9;
    padding: 4px;
}

QScrollBar:vertical {
    border: 1px solid #bd93f9;
    background: #282a36;
    width: 15px;
    margin: 15px 3px 15px 3px;
}

QScrollBar::handle:vertical {
    background-color: #6272a4; /* Scrollbar handle colour */
    min-height: 20px;
}

QScrollBar::add-line:vertical {
    border: 2px solid #bd93f9;
    background: #50fa7b;
    height: 20px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    border: 2px solid #bd93f9;
    background: #ff5555;
    height: 20px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
"""

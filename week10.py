import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt

class BookApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Buku - Andika Dhanan Jaya | F1D022111")
        self.resize(700, 500)
        self.setupUI()
        self.connectDB()
        self.load_data()

    def setupUI(self):
        layout = QVBoxLayout()

       
        form_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Judul Buku")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Kategori")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Tahun")
        self.save_btn = QPushButton("Simpan")
        self.save_btn.clicked.connect(self.save_data)

        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.category_input)
        form_layout.addWidget(self.year_input)
        form_layout.addWidget(self.save_btn)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Kategori", "Tahun"])
        self.table.cellDoubleClicked.connect(self.edit_data)


        bottom_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Hapus")
        self.delete_btn.clicked.connect(self.delete_data)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari Judul...")
        self.search_input.textChanged.connect(self.search_data)

        bottom_layout.addWidget(self.search_input)
        bottom_layout.addWidget(self.delete_btn)

        self.name_label = QLabel("Andika Dhanan Jaya - F1D022111")
        self.name_label.setStyleSheet("margin-top: 10px; font-weight: bold;")
        self.name_label.setAlignment(Qt.AlignCenter)

        layout.addLayout(form_layout)
        layout.addWidget(self.table)
        layout.addLayout(bottom_layout)
        layout.addWidget(self.name_label)

        self.setLayout(layout)

    def connectDB(self):
        self.conn = sqlite3.connect("buku.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS buku (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT,
                kategori TEXT,
                tahun INTEGER
            )
        """)
        self.conn.commit()

    def save_data(self):
        judul = self.title_input.text()
        kategori = self.category_input.text()
        tahun = self.year_input.text()
        if judul and kategori and tahun:
            self.cursor.execute("INSERT INTO buku (judul, kategori, tahun) VALUES (?, ?, ?)",
                                (judul, kategori, tahun))
            self.conn.commit()
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.warning(self, "Validasi", "Semua field harus diisi!")

    def load_data(self, query="SELECT * FROM buku"):
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(self.cursor.execute(query)):
            self.table.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def delete_data(self):
        selected = self.table.currentRow()
        if selected >= 0:
            id_item = self.table.item(selected, 0)
            if id_item:
                id_val = int(id_item.text())
                self.cursor.execute("DELETE FROM buku WHERE id = ?", (id_val,))
                self.conn.commit()
                self.load_data()

    def edit_data(self, row, col):
        id_val = int(self.table.item(row, 0).text())
        judul = self.table.item(row, 1).text()
        new_judul, ok = QInputDialog.getText(self, "Edit Judul", "Judul Buku:", text=judul)
        if ok and new_judul:
            self.cursor.execute("UPDATE buku SET judul = ? WHERE id = ?", (new_judul, id_val))
            self.conn.commit()
            self.load_data()

    def search_data(self, text):
        query = f"SELECT * FROM buku WHERE judul LIKE '%{text}%'"
        self.load_data(query)

    def clear_form(self):
        self.title_input.clear()
        self.category_input.clear()
        self.year_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookApp()
    window.show()
    sys.exit(app.exec_())

import sys
import random

import pandas as pd
from pandas import DataFrame
from DATA225utils import make_connection, dataframe_query

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 

from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QHeaderView, \
                            QTableWidget, QTableWidgetItem


class TeamList(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        Initialize private class attributes.
        """
        super().__init__()
        
        # Load the UI.
        self.ui = uic.loadUi('UIs/teamList.ui')

        self.ui.east.clicked.connect(lambda: self.get_team_data("east"))
        self.ui.west.clicked.connect(lambda: self.get_team_data("west"))
        self.ui.teamList.cellClicked.connect(self.handle_cell_clicked)
        
        self.ui.show();


    def get_team_data(conf):
        
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()
        
        sql = (
            """
            select concat(city, " ",name) as team_name from teams
            """
            f"where conference = '{conf}'"
            )
    
        cursor.execute(sql)
        rows = cursor.fetchall()

        self.ui.teamList.setRowCount(0)
        self.ui.teamList.setColumnCount(1)
        self.ui.teamList.setHorizontalHeaderLabels(['Teams'])
        for row_data in rows:
            row_number = self.ui.teamList.rowCount()
            self.ui.teamList.insertRow(row_number)
            item = QTableWidgetItem(str(row_data[0]))
            self.ui.teamList.setItem(row_number, 0, item)


    def handle_cell_clicked(self, row, column):
        item = self.ui.teamList.item(row, column)
        if item is not None:
            data = item.text()
            print(f"Clicked row {row}, column {column}: {data}")

        self.ui.next.clicked.connect(self.next_page)


    def next_page(self):
        print()

    #------#
    # Main #
    #------#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TeamList()
    sys.exit(app.exec_())
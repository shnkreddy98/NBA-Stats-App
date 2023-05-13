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


class Window(QWindow):
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
        self.ui = uic.loadUi('playersInfo.ui')
        
        self.ui.show();
        self._initialize_table()
        self.ui.SearchPlayer.clicked.connect(self.player_data)
        
        
    def _initialize_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.player_info.clear()

        col = ['  player_name  ', '   player_Id   ', '  Points  ', ' Rebounds  ', '  Assists  ', '  Block  ', ' Field Goal %']
        self.ui.player_info.setHorizontalHeaderLabels(col)        
       
    def player_data(self):   
        Search_term = str(self.ui.Player_name.text())
        
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()
        
        sql = (f"SELECT p.player_name, p.player_id, avg(s.PTS), avg(s.REB), avg(s.AST), avg(s.BLK), avg(s.FGM/s.FGA) as FG_PCT "
               f"FROM players p "
               f"JOIN player_game_stats s ON p.player_id = s.player_id "
               f"WHERE p.player_name Like '%{Search_term}%' "
               f"GROUP BY p.player_name, p.player_id")
    
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(rows)
        print(self.ui.Player_name.text())
        for row_number, row_data in enumerate(rows):
            self.ui.player_info.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.player_info.setItem(row_number, column_number, item)
            
    #------#
    # Main #
    #------#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Window()
    sys.exit(app.exec_())
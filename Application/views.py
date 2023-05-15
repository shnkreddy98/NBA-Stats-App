import sys
import random
import pandas as pd
from pandas import DataFrame
from DATA225utils import make_connection, dataframe_query

from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QHeaderView, \
                            QTableWidget, QTableWidgetItem


class viewData():
    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi('UIs/views.ui')
        self.ui.show()

        self._initialize_tables()

    def _initialize_tables(self):
        conn = make_connection(config_file = '../configFiles/temp.ini')
        cursor = conn.cursor()

        sql_players = ("""SELECT * from players LIMIT 15""")
        sql_games = ("""SELECT * from games LIMIT 15""")
        sql_teams = ("""SELECT * from teams LIMIT 15""")
        sql_ranking = ("""SELECT * from ranking LIMIT 15""")
        sql_game_stats = ("""SELECT * from game_stats LIMIT 15""")
        sql_player_stats = ("""SELECT * from player_game_stats LIMIT 15""")
    
        cursor.execute(sql_players)
        rows = cursor.fetchall()

        self.ui.players.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.players.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.players.setItem(row_number, column_number, item)

        cursor.execute(sql_games)
        rows = cursor.fetchall()

        self.ui.games.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.games.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.games.setItem(row_number, column_number, item)

        cursor.execute(sql_teams)
        rows = cursor.fetchall()

        self.ui.teams.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.teams.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.teams.setItem(row_number, column_number, item)

        cursor.execute(sql_ranking)
        rows = cursor.fetchall()

        self.ui.rank.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.rank.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.rank.setItem(row_number, column_number, item)


        cursor.execute(sql_game_stats)
        rows = cursor.fetchall()

        self.ui.game_stats.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.game_stats.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.game_stats.setItem(row_number, column_number, item)


        cursor.execute(sql_player_stats)
        rows = cursor.fetchall()

        self.ui.players_game_stats.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.players_game_stats.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.players_game_stats.setItem(row_number, column_number, item)

        cursor.close()
        conn.close()

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = viewData()
    sys.exit(app.exec_())
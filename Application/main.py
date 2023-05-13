import sys
import random

import pandas as pd
from pandas import DataFrame
from DATA225utils import make_connection, dataframe_query

from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QHeaderView, \
                            QTableWidget, QTableWidgetItem


class MainMenu(QWindow):
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
        self.ui = uic.loadUi('UIs/main.ui')
        
        self.ui.show();

        self.ui.mainNext.clicked.connect(self.next_page)


    def next_page(self):
        """
        Checking which radio button is selected and opening that page
        """
        if self.ui.update.isChecked():
            print("update")

        elif self.ui.view.isChecked():
            print("view")

        elif self.ui.search.isChecked():
            self.ui = uic.loadUi('UIs/searchMenu.ui')
            self.ui.show()

            self.ui.searchNext.clicked.connect(self.search_menu)

            self.ui.backToMainMenu.clicked.connect(self.show_main_menu)

        elif self.ui.analyze.isChecked():
            print("analyze")
            
        else:
            return


    def search_menu(self):

        if self.ui.searchByTeam.isChecked():
            self.ui = uic.loadUi('UIs/teamList.ui')
            self.ui.show()

            self.ui.east.clicked.connect(lambda: self.get_team_data("east"))
            self.ui.west.clicked.connect(lambda: self.get_team_data("west"))
            self.ui.teamList.cellClicked.connect(self.handle_cell_clicked)

            self.ui.backToMainMenu.clicked.connect(self.show_main_menu)

        elif self.ui.searchByPlayer.isChecked():
            self.ui = uic.loadUi('UIs/playersInfo.ui')
            self.ui.show()

        else:
            return


    def get_team_data(self, conf):
        
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
            # print(f"Clicked row {row}, column {column}: {data}")

        self.ui.teamListNext.clicked.connect(lambda: self.player_info(data))


    def player_info(self, teamName):
        self.ui = uic.loadUi("UIs/teams.ui")
        self.ui.show()

        self._initialize_team_menu(teamName)
        self._initialize_season_menu(teamName)

        self._enter_player_data()

        self.ui.teamMenu.currentIndexChanged.connect(lambda: self._enter_player_data())
        self.ui.teamMenu.currentIndexChanged.connect(lambda: self._enter_team_details())
        self.ui.seasonMenu.currentIndexChanged.connect(lambda: self._enter_player_data())

        self._enter_team_details()

        self.ui.backToMainMenu.clicked.connect(self.show_main_menu)


    def _initialize_team_menu(self, teamName):
        """
        Initialize the team menu with team names from the database.
        """
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()
        
        sql = ("""
                SELECT concat(city, " ", name)
                FROM teams
                """)
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            name = row[0]
            self.ui.teamMenu.addItem(name, row)

        index = self.ui.teamMenu.findText(teamName)
        self.ui.teamMenu.setCurrentIndex(index)


    def _initialize_season_menu(self, teamName):
        """
        Initialize the season menu with seasons where the team has played.
        """
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()
        
        sql = ("""
                      SELECT distinct(R.season) AS seasonPlayed FROM roster R
                      INNER JOIN teams T
                      WHERE T.team_id = R.team_id
                      """
                      f"AND concat(T.city, ' ', T.name) = '{teamName}'"
                      """
                      ORDER BY seasonPlayed
                      """
                )
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()


        for row in rows:
            name = str(row[0])
            self.ui.seasonMenu.addItem(name, row)


    def show_main_menu(self):
        """
        Load and show the main menu UI.
        """
        self.ui = uic.loadUi('UIs/main.ui')
        self.ui.show()
        
        self.ui.mainNext.clicked.connect(self.next_page)


    def _enter_player_data(self):
        teamName = self.ui.teamMenu.currentData()[0]
        season = self.ui.seasonMenu.currentData()[0]
        # print(season)
        
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()

        # print(teamName)

        sql = ("""
                SELECT
                  players.player_id,
                  player_name,
                  height,
                  weight,
                  draftyear
                FROM
                  roster
                  JOIN players ON roster.player_id = players.player_id
                  JOIN teams ON roster.team_id = teams.team_id
                WHERE
                """
                  f"concat(teams.city, ' ', teams.name) = '{teamName}'"
                  f"AND roster.season = '{season}'"
                  f"ORDER BY player_name"
                ) 
        
        cursor.execute(sql)
        rows = cursor.fetchall()
              
        cursor.close()
        conn.close()

        self.ui.playersTable.setRowCount(0)
       
        
        for row_number, row_data in enumerate(rows):
            self.ui.playersTable.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.playersTable.setItem(row_number, column_number, item)


    def _enter_team_details(self):
        teamName = self.ui.teamMenu.currentData()[0]
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()

        sql = ("""
                SELECT * FROM teams
                """
                f"WHERE CONCAT(city, ' ', name) = '{teamName}'"
                ) 
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        print(rows[0])

        self.ui.YearFounded.setText(f"Year Founded: '{rows[0][3]}'")
        self.ui.Arena.setText(f"Arena: '{rows[0][5]}'")
        self.ui.ArenaCapacity.setText(f"Arena Capacity: '{rows[0][6]}'")
        self.ui.Owner.setText(f"Owner: '{rows[0][7]}'")
        self.ui.GeneralManager.setText(f"General Manager: '{rows[0][8]}'")
        self.ui.HeadCoach.setText(f"Head Coach: '{rows[0][9]}'")
        self.ui.DLeagueAffiliation.setText(f"D-League Affiliation: '{rows[0][10]}'")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainMenu()
    sys.exit(app.exec_())
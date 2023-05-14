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
            self.ui = uic.loadUi('UIs/ranking.ui')
            self.ui.show()

            self.ui.dateEdit.setCalendarPopup(True)
            self.ui.dateEdit.setDateRange(QDate(2004, 1, 2), QDate(2022, 12, 22))
            self.ui.dateEdit.setDate(QDate(2004, 1, 2))

            self.ui.showResults.clicked.connect(self._enter_standings_data)

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
            self.ui = uic.loadUi('UIs/playerInfo.ui')
            self.ui.show()

            self.ui.searchButton.clicked.connect(lambda: self._initialize_player_stats("placeHolder", 1))

            self.ui.backToMainMenu.clicked.connect(self.show_main_menu)

        else:
            return

    def team_info(self, teamName):
        self.ui = uic.loadUi("UIs/teams.ui")
        self.ui.show()

        self._initialize_team_menu(teamName)

        self._enter_player_data()

        self.ui.teamMenu.currentIndexChanged.connect(lambda: self._enter_player_data())
        self.ui.teamMenu.currentIndexChanged.connect(lambda: self._enter_team_details())

        self.ui.playersTable.cellClicked.connect(self.handle_cell_clicked)

        self._enter_team_details()

        self.ui.backToMainMenu.clicked.connect(self.show_main_menu)

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
        try:
            item = self.ui.teamList.item(row, column)
            if item is not None:
                data = item.text()
                

            self.ui.teamListNext.clicked.connect(lambda: self.team_info(data))
        except:
            item = self.ui.playersTable.item(row, column)
            if item is not None:
                data = item.text()
            self.ui.playersInfoNext.clicked.connect(lambda: self.player_stats(data))


    def player_stats(self, playerName):
        """
        """
        self.ui = uic.loadUi("UIs/playerStats.ui")
        self.ui.show()

        self.ui.playerName.setText(playerName)

        self._initialize_player_stats(playerName, 0)

        self.ui.back.clicked.connect(lambda: self.team_info("Atlanta Hawks"))
        self.ui.backToMainMenu.clicked.connect(self.show_main_menu)


    def _initialize_player_stats(self, playerName, flag):
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()

        if flag == 1:
            playerName = self.ui.playerName.text()
            sql = ("""
                    SELECT P.player_name,
                      CONCAT (T.city, ' ', T.name) as TeamName,
                      AVG(PGS.seconds)/60 AS MINUTES,
                      AVG(PGS.pts) AS PTS,
                      AVG(PGS.reb) AS REB,
                      AVG(PGS.ast) AS AST,
                      AVG(PGS.fgm) AS FGM,
                      AVG(PGS.fga) AS FGA,
                      AVG(PGS.fgm/PGS.fga) AS FG_PCT,
                      AVG(PGS.fg3m) AS FG3M,
                      AVG(PGS.fg3a) AS FG3A,
                      AVG(PGS.fg3m/PGS.fg3a) AS FG3_PCT,
                      AVG(PGS.ftm) AS FTM,
                      AVG(PGS.fta) AS FTA,
                      AVG(PGS.ftm/PGS.fta) AS FT_PCT,
                      AVG(PGS.oreb) AS OREB,
                      AVG(PGS.dreb) AS DREB,
                      AVG(PGS.stl) AS STL,
                      AVG(PGS.blk) AS BLK,
                      AVG(PGS.turnover) AS TurnOver,
                      AVG(PGS.pf) AS PersonalFouls
                    FROM player_game_stats PGS
                    inner join players P
                    on PGS.player_id = P.player_id
                    inner join teams T
                    on T.team_id = PGS.team_id
                    """
                    f"where P.player_name LIKE '%{playerName}%'"
                    f"group by PGS.team_id, P.player_name, TeamName;"
                    )
        else:
            sql = ("""
                    SELECT P.player_name,
                      CONCAT (T.city, ' ', T.name) as TeamName,
                      AVG(PGS.seconds)/60 AS MINUTES,
                      AVG(PGS.pts) AS PTS,
                      AVG(PGS.reb) AS REB,
                      AVG(PGS.ast) AS AST,
                      AVG(PGS.fgm) AS FGM,
                      AVG(PGS.fga) AS FGA,
                      AVG(PGS.fgm/PGS.fga) AS FG_PCT,
                      AVG(PGS.fg3m) AS FG3M,
                      AVG(PGS.fg3a) AS FG3A,
                      AVG(PGS.fg3m/PGS.fg3a) AS FG3_PCT,
                      AVG(PGS.ftm) AS FTM,
                      AVG(PGS.fta) AS FTA,
                      AVG(PGS.ftm/PGS.fta) AS FT_PCT,
                      AVG(PGS.oreb) AS OREB,
                      AVG(PGS.dreb) AS DREB,
                      AVG(PGS.stl) AS STL,
                      AVG(PGS.blk) AS BLK,
                      AVG(PGS.turnover) AS TurnOver,
                      AVG(PGS.pf) AS PersonalFouls
                    FROM player_game_stats PGS
                    inner join players P
                    on PGS.player_id = P.player_id
                    inner join teams T
                    on T.team_id = PGS.team_id
                    """
                    f"where P.player_name = '{playerName}'"
                    f"group by PGS.team_id, P.player_name, TeamName;"
                    )


        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        self.ui.playerStats.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.playerStats.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.playerStats.setItem(row_number, column_number, item)


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



    def show_main_menu(self):
        """
        Load and show the main menu UI.
        """
        self.ui = uic.loadUi('UIs/main.ui')
        self.ui.show()
        
        self.ui.mainNext.clicked.connect(self.next_page)


    def _enter_player_data(self):
        teamName = self.ui.teamMenu.currentData()[0]
        
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()


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

        self.ui.YearFounded.setText(f"Year Founded: {rows[0][3]}")
        self.ui.Arena.setText(f"Arena: {rows[0][5]}")
        self.ui.ArenaCapacity.setText(f"Arena Capacity: {rows[0][6]}")
        self.ui.Owner.setText(f"Owner: {rows[0][7]}")
        self.ui.GeneralManager.setText(f"General Manager: {rows[0][8]}")
        self.ui.HeadCoach.setText(f"Head Coach: {rows[0][9]}")
        self.ui.DLeagueAffiliation.setText(f"D-League Affiliation: {rows[0][10]}")


    def _enter_standings_data(self):
        date = self.ui.dateEdit.date().toPyDate()

        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()
        
        sql = (
            """
                SELECT 
                    CONCAT(t.city, ' ', t.name) AS TeamName,
                    r.GP,
                    r.GW,
                    r.GL,
                    r.home_record AS HomeRecord,
                    r.away_record AS AwayRecord, 
                    t.conference AS Conference,
                    r.standings_date AS date
                FROM ranking r
                JOIN teams t ON r.team_id = t.team_id
                """
                f"WHERE r.standings_date = '{date}'"
                f"AND r.conference = 'east'"
                f"ORDER BY r.GW DESC, r.GL ASC"
            )
    
        cursor.execute(sql)
        rows = cursor.fetchall()

        self.ui.eastConfTable.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.eastConfTable.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.eastConfTable.setItem(row_number, column_number, item)


        sql = (
            """
                SELECT 
                    CONCAT(t.city, ' ', t.name) AS TeamName,
                    r.GP,
                    r.GW,
                    r.GL,
                    r.home_record AS HomeRecord,
                    r.away_record AS AwayRecord, 
                    t.conference AS Conference,
                    r.standings_date AS date
                FROM ranking r
                JOIN teams t ON r.team_id = t.team_id
                """
                f"WHERE r.standings_date = '{date}'"
                f"AND r.conference = 'west'"
                f"ORDER BY r.GW DESC, r.GL ASC"
            )
    
        cursor.execute(sql)
        rows = cursor.fetchall()

        self.ui.westConfTable.setRowCount(0)
        
        for row_number, row_data in enumerate(rows):
            self.ui.westConfTable.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.westConfTable.setItem(row_number, column_number, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainMenu()
    sys.exit(app.exec_())
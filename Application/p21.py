import sys
import mysql.connector
from DATA225utils import make_connection, dataframe_query
from PyQt5.QtWidgets import (QApplication, QDialog, QTableWidget, QTableWidgetItem, QComboBox, QWidget, QPushButton, QVBoxLayout)
from PyQt5.uic import loadUi


class MyDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Team Stats")
        loadUi('UIs/P21.ui', self)
        self.initUI()

    def initUI(self):
        self.Stats_team1.setColumnCount(17)
        self.Stats_team1.setHorizontalHeaderLabels(['TEAM ID', 'SECONDS', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TurnOver', 'PF', 'PTS', 'REB'])
        self.Stats_team2.setColumnCount(17)
        self.Stats_team2.setHorizontalHeaderLabels(['TEAM ID', 'SECONDS', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TurnOver', 'PF', 'PTS', 'REB'])

        
        self.Select_T1.clicked.connect(lambda: self.select_team(self.Team_1, self.Stats_team1, 'home_team_id'))
        self.Select_T2.clicked.connect(lambda: self.select_team(self.Team_2, self.Stats_team2, 'visitor_team_id'))


    def select_team(self, team_widget, stats_widget, team_column):
        try:
            conn = make_connection(config_file='snps_pro.ini')
            cursor = conn.cursor()

           
            query = f"SELECT SUM(Seconds), SUM(fgm), SUM(fga), SUM(fg3m), SUM(fg3a), SUM(ftm), SUM(fta), SUM(oreb), SUM(dreb), SUM(ast), SUM(stl), SUM(blk), SUM(turnover), SUM(pf), SUM(pts), SUM(reb) FROM games WHERE {team_column} = team_id GROUP BY team_id"
            cursor.execute(query)
            rows = cursor.fetchall()

            stats_widget.setRowCount(len(rows))
            stats_widget.setColumnCount(17)

            
            for i, row in enumerate(rows):
                for j in range(17):
                    stats_widget.setItem(i, j, QTableWidgetItem(str(row[j])))

        
            team_widget.setCurrentIndex(0)

        except mysql.connector.Error as error:
            print(f"Error while connecting to MySQL: {error}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


if __name__ == '__main__':
    app = QApplication([])
    dialog = MyDialog()
    dialog.show()
    app.exec_()

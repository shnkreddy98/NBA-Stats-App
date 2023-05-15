import mysql.connector
from DATA225utils import make_connection, dataframe_query
from PyQt5.QtWidgets import (QApplication, QDialog, QTableWidget, QTableWidgetItem, QComboBox)
from PyQt5.uic import loadUi


class MyDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        loadUi('UIs/P31.ui', self)

        self.setWindowTitle("Dialog")
        self.populate_table1()
        self.populate_table2()
        self.metrics.currentIndexChanged.connect(self.handle_combo_box)
        
        self.metrics.currentIndexChanged.connect(self.populate_table1)
        self.metrics.currentIndexChanged.connect(self.populate_table2)
        
    def handle_combo_box(self,team_name):
        if team_name == "TEAM 1":
            Stats_team1_2.setCurrentIndex(0)  
        elif team_name == "TEAM 2":
            Stats_team1_2.setCurrentIndex(1)
 
    
    def populate_table1(self):
        metric = self.metrics.currentText()
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()
        
        if metric == "TEAM 1":
            sql = "SELECT AVG(SECONDS), AVG(FGM), AVG(FGA), AVG(FG3M), AVG(FG3A), AVG(FTM), AVG(FTA), AVG(OREB), AVG(DREB), AVG(AST), AVG(STL), AVG(BLK), AVG(TurnOver), AVG(PF), AVG(PTS), AVG(REB) FROM player_game_stats;"
        
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.Stats_team1.setRowCount(len(rows))
            self.Stats_team1.setColumnCount(len(rows[0]))  # set column count based on the number of columns returned by the query
                
            header_labels = ['AVG(SECONDS)', 'AVG(FGM)', 'AVG(FGA)', 'AVG(FG3M)', 'AVG(FG3A)', 'AVG(FTM)', 'AVG(FTA)', 'AVG(OREB)', 'AVG(DREB)', 'AVG(AST)', 'AVG(STL)', 'AVG(BLK)', 'AVG(TurnOver)', 'AVG(PF)', 'AVG(PTS)', 'AVG(REB)']  # initialize header labels with the column names returned by the query
            self.Stats_team1.setHorizontalHeaderLabels(header_labels)
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.Stats_team1.setItem(i, j, item)

    def populate_table2(self):
        metric = self.metrics.currentText()
        conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
        cursor = conn.cursor()
        
        if metric == "TEAM 2":
            sql = "SELECT SUM(SECONDS), SUM(FGM), SUM(FGA), SUM(FG3M), SUM(FG3A), SUM(FTM), SUM(FTA), SUM(OREB), SUM(DREB), SUM(AST), SUM(STL), SUM(BLK), SUM(TurnOver), SUM(PF), SUM(PTS), SUM(REB) FROM player_game_stats;"
        
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.Stats_team2.setRowCount(len(rows))
            self.Stats_team2.setColumnCount(len(rows[0]))  # set column count based on the number of columns returned by the query
                
            header_labels = ['SUM(SECONDS)', 'SUM(FGM)', 'SUM(FGA)', 'SUM(FG3M)', 'SUM(FG3A)', 'SUM(FTM)', 'SUM(FTA)', 'SUM(OREB)', 'SUM(DREB)', 'SUM(AST)', 'SUM(STL)', 'SUM(BLK)', 'SUM(TurnOver)', 'SUM(PF)','SUM(PTS)', 'SUM(REB)']  # initialize header labels with the column names returned by the query
            self.Stats_team2.setHorizontalHeaderLabels(header_labels)
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.Stats_team2.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication([])
    dlg = MyDialog()
    dlg.show()
    app.exec()

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


class updateData():
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('UIs/create.ui')
        self.ui.show()

        
        
        # Connect update buttons
        self.ui.playersUpdateBtn.clicked.connect(self.update_player)
        self.ui.teamsUpdateBtn.clicked.connect(self.update_team)
        
    
        
    def update_player(self):
        try:
            name = self.ui.name_3.text()
            country = self.ui.country_2.text()
            height = self.ui.height_2.text()
            weight = self.ui.weight_2.text()
            draftyear = self.ui.lineEdit_5.text()
            
            conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
            cursor = conn.cursor()

            sql = ("""SELECT MAX(player_id) FROM players""")

            cursor.execute(sql)
            last_player_id = cursor.fetchall()[0][0]
            player_id = last_player_id+1
            
            query = ("""
                        INSERT INTO players(player_id, player_name, country, height, weight, draftyear)
                     """
                        f"VALUES ('{player_id}', '{name}', '{country}', '{height}', '{weight}', '{draftyear}')"
                    )
                       
            cursor.execute(query)
            conn.commit()

            self.ui.outputPlayers.setText("Data Added Successfully")

            cursor.close()
            conn.close()
        except Exception as e:
            self.ui.outputPlayers.setText(f"Error occured Please try again, '{e}'")
        
    def update_team(self):
        try:
            abbrevation = self.ui.abbrevation.text()
            name = self.ui.name_2.text()
            year_founded = self.ui.year_founded_2.text()
            city = self.ui.city_2.text()
            arena = self.ui.arena_2.text() 
            arena_capacity = self.ui.arena_capacity_2.text()
            owner = self.ui.owner_2.text()
            general_manager = self.ui.general_manager_2.text()
            head_coach = self.ui.lineEdit_9.text()
            d_league_affiliation = self.ui.d_league_affiliation.text()
            state = self.ui.state_2.text()
            conference = self.ui.conference_2.text()
            
            conn = make_connection(config_file = '../configFiles/local_snps_db.ini')
            cursor = conn.cursor()

            sql = ("""SELECT MAX(team_id) FROM teams""")

            cursor.execute(sql)
            last_team_id = cursor.fetchall()[0][0]
            team_id = last_team_id+1
            
            query = ("""INSERT INTO teams(team_id, abbrevation, name, year_founded, city, arena, arena_capacity, owner, general_manager, head_coach, d_league_affiliation, state, conference)
                     """
                     f"VALUES ('{team_id}', '{abbrevation}', '{name}', '{year_founded}', '{city}', '{arena}', '{arena_capacity}', '{owner}', '{general_manager}', '{head_coach}', '{d_league_affiliation}', '{state}', '{conference}')")
                       
            cursor.execute(query)
            conn.commit()

            self.ui.outputTeam.setText("Data Added Successfully")

            cursor.close()
            conn.close()

        except Exception as e:
            self.ui.outputTeam.setText(f"Error occured Please try again, '{e}'")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = updateData()
    sys.exit(app.exec_())
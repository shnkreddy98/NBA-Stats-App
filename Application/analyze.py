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

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 


class analyzePlayer():
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
        self.ui = uic.loadUi('UIs/graph.ui')
        
        self.ui.show();

        self.ui.search.clicked.connect(self._update_points_graph)
        self.ui.search.clicked.connect(self._update_rebounds_graph)
        self.ui.search.clicked.connect(self._update_assists_graph)


    def _initialize_pts_graph(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.pointsGraph.count()):
            child = self.ui.pointsGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_points_graph(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_pts_graph()
        
        # Add the figure to the UI.
        self.ui.pointsGraph.addWidget(FigureCanvas(plt.figure()))
        
        player_name = self.ui.playerName.text()

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
            SELECT
              c.yr,
              AVG(ps.points) as total_points
            FROM
              player p
              JOIN player_stats ps ON p.player_key = ps.player_key
              JOIN game g ON ps.game_key = g.game_key
              JOIN calendar c ON g.date_key = c.date_key
            WHERE
            """
              f"p.player_name = '{player_name}'"
            """
            GROUP BY
              p.player_name, c.yr
            ORDER BY
              c.yr;
            """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'Average points score by {player_name} over the years')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()



    def _initialize_reb_graph(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.reboundsGraph.count()):
            child = self.ui.reboundsGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_rebounds_graph(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_reb_graph()
        
        # Add the figure to the UI.
        self.ui.reboundsGraph.addWidget(FigureCanvas(plt.figure()))
        
        player_name = self.ui.playerName.text()

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
            SELECT
              c.yr,
              AVG(ps.rebounds) as total_rebounds
            FROM
              player p
              JOIN player_stats ps ON p.player_key = ps.player_key
              JOIN game g ON ps.game_key = g.game_key
              JOIN calendar c ON g.date_key = c.date_key
            WHERE
            """
              f"p.player_name = '{player_name}'"
            """
            GROUP BY
              p.player_name, c.yr
            ORDER BY
              c.yr;
            """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'Average points score by {player_name} over the years')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()


    def _initialize_ast_graph(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.assistsGraph.count()):
            child = self.ui.assistsGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_assists_graph(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_ast_graph()
        
        # Add the figure to the UI.
        self.ui.assistsGraph.addWidget(FigureCanvas(plt.figure()))

        player_name = self.ui.playerName.text()

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
            SELECT
              c.yr,
              AVG(ps.rebounds) as total_rebounds
            FROM
              player p
              JOIN player_stats ps ON p.player_key = ps.player_key
              JOIN game g ON ps.game_key = g.game_key
              JOIN calendar c ON g.date_key = c.date_key
            WHERE
            """
              f"p.player_name = '{player_name}'"
            """
            GROUP BY
              p.player_name, c.yr
            ORDER BY
              c.yr;
            """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'Average points score by {player_name} over the years')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()



class analyzeTeam():
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
        self.ui = uic.loadUi('UIs/graph2.ui')
        
        self.ui.show();

        self._initialize_team_menu()

        self.ui.teamMenu.currentIndexChanged.connect(lambda: self._enter_player_data())

        self.ui.search.clicked.connect(self._update_graph_1)
        self.ui.search.clicked.connect(self._update_graph_2)
        self.ui.search.clicked.connect(self._update_graph_3)
        self.ui.search.clicked.connect(self._update_graph_4)
        self.ui.search.clicked.connect(self._update_graph_5)
        self.ui.search.clicked.connect(self._update_graph_6)


    def _initialize_team_menu(self):
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


    def _initialize_graph_1(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.winPctGraph.count()):
            child = self.ui.winPctGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_graph_1(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph_1()
        
        # Add the figure to the UI.
        self.ui.winPctGraph.addWidget(FigureCanvas(plt.figure()))

        team_name = self.ui.teamMenu.currentData()[0]

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
                WITH game_stats AS (
                  SELECT
                    t.team_name,
                    g.date_key,
                    c.yr,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.home_score
                      ELSE g.away_score
                    END AS points_scored,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.away_score
                      ELSE g.home_score
                    END AS points_allowed,
                    (g.home_team_key = t.team_key) AS is_home,
                    (g.away_team_key = t.team_key) AS is_away,
                    (g.home_score > g.away_score) AS is_win
                  FROM game g
                  JOIN team t ON (g.home_team_key = t.team_key OR g.away_team_key = t.team_key)
                  JOIN calendar c ON g.date_key = c.date_key
                """
                  f"WHERE t.team_name = '{team_name}'"
                """
                )
                SELECT
                  yr,
                  SUM(is_win) / COUNT(*) AS win_percentage
                FROM game_stats
                GROUP BY yr
                ORDER BY yr
                """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()


    def _initialize_graph_2(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.ppgGraph.count()):
            child = self.ui.ppgGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_graph_2(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph_2()
        
        # Add the figure to the UI.
        self.ui.ppgGraph.addWidget(FigureCanvas(plt.figure()))

        team_name = self.ui.teamMenu.currentData()[0]

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
                WITH game_stats AS (
                  SELECT
                    t.team_name,
                    g.date_key,
                    c.yr,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.home_score
                      ELSE g.away_score
                    END AS points_scored,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.away_score
                      ELSE g.home_score
                    END AS points_allowed,
                    (g.home_team_key = t.team_key) AS is_home,
                    (g.away_team_key = t.team_key) AS is_away,
                    (g.home_score > g.away_score) AS is_win
                  FROM game g
                  JOIN team t ON (g.home_team_key = t.team_key OR g.away_team_key = t.team_key)
                  JOIN calendar c ON g.date_key = c.date_key
                """
                  f"WHERE t.team_name = '{team_name}'"
                """
                )
                SELECT
                  yr,
                  AVG(points_scored) AS points_per_game
                FROM game_stats
                GROUP BY yr
                ORDER BY yr
                """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()


    def _initialize_graph_3(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.pointsAllowedGraph.count()):
            child = self.ui.pointsAllowedGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_graph_3(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph_3()
        
        # Add the figure to the UI.
        self.ui.pointsAllowedGraph.addWidget(FigureCanvas(plt.figure()))

        team_name = self.ui.teamMenu.currentData()[0]

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
                WITH game_stats AS (
                  SELECT
                    t.team_name,
                    g.date_key,
                    c.yr,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.home_score
                      ELSE g.away_score
                    END AS points_scored,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.away_score
                      ELSE g.home_score
                    END AS points_allowed,
                    (g.home_team_key = t.team_key) AS is_home,
                    (g.away_team_key = t.team_key) AS is_away,
                    (g.home_score > g.away_score) AS is_win
                  FROM game g
                  JOIN team t ON (g.home_team_key = t.team_key OR g.away_team_key = t.team_key)
                  JOIN calendar c ON g.date_key = c.date_key
                """
                  f"WHERE t.team_name = '{team_name}'"
                """
                )
                SELECT
                  yr,
                  AVG(points_allowed) AS points_allowed_per_game
                FROM game_stats
                GROUP BY yr
                ORDER BY yr
                """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()


    def _initialize_graph_4(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.homeWinGraph.count()):
            child = self.ui.homeWinGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_graph_4(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph_4()
        
        # Add the figure to the UI.
        self.ui.homeWinGraph.addWidget(FigureCanvas(plt.figure()))

        team_name = self.ui.teamMenu.currentData()[0]

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
                WITH game_stats AS (
                  SELECT
                    t.team_name,
                    g.date_key,
                    c.yr,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.home_score
                      ELSE g.away_score
                    END AS points_scored,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.away_score
                      ELSE g.home_score
                    END AS points_allowed,
                    (g.home_team_key = t.team_key) AS is_home,
                    (g.away_team_key = t.team_key) AS is_away,
                    (g.home_score > g.away_score) AS is_win
                  FROM game g
                  JOIN team t ON (g.home_team_key = t.team_key OR g.away_team_key = t.team_key)
                  JOIN calendar c ON g.date_key = c.date_key
                """
                  f"WHERE t.team_name = '{team_name}'"
                """
                )
                SELECT
                  yr,
                  SUM(is_home * is_win) / SUM(is_home) AS home_win_percentage
                FROM game_stats
                GROUP BY yr
                ORDER BY yr
                """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()


    def _initialize_graph_5(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.awayWinGraph.count()):
            child = self.ui.awayWinGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_graph_5(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph_5()
        
        # Add the figure to the UI.
        self.ui.awayWinGraph.addWidget(FigureCanvas(plt.figure()))

        team_name = self.ui.teamMenu.currentData()[0]

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
                WITH game_stats AS (
                  SELECT
                    t.team_name,
                    g.date_key,
                    c.yr,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.home_score
                      ELSE g.away_score
                    END AS points_scored,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.away_score
                      ELSE g.home_score
                    END AS points_allowed,
                    (g.home_team_key = t.team_key) AS is_home,
                    (g.away_team_key = t.team_key) AS is_away,
                    (g.home_score > g.away_score) AS is_win
                  FROM game g
                  JOIN team t ON (g.home_team_key = t.team_key OR g.away_team_key = t.team_key)
                  JOIN calendar c ON g.date_key = c.date_key
                """
                  f"WHERE t.team_name = '{team_name}'"
                """
                )
                SELECT
                  yr,
                  SUM(is_away * is_win) / SUM(is_away) AS away_win_percentage
                FROM game_stats
                GROUP BY yr
                ORDER BY yr
                """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()


    def _initialize_graph_6(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.marginVictoryGraph.count()):
            child = self.ui.marginVictoryGraph.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _update_graph_6(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph_6()
        
        # Add the figure to the UI.
        self.ui.marginVictoryGraph.addWidget(FigureCanvas(plt.figure()))

        team_name = self.ui.teamMenu.currentData()[0]

        conn = make_connection(config_file = '../configFiles/local_snps_wh.ini')
        cursor = conn.cursor()

        sql = ("""
                WITH game_stats AS (
                  SELECT
                    t.team_name,
                    g.date_key,
                    c.yr,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.home_score
                      ELSE g.away_score
                    END AS points_scored,
                    CASE
                      WHEN g.home_team_key = t.team_key THEN g.away_score
                      ELSE g.home_score
                    END AS points_allowed,
                    (g.home_team_key = t.team_key) AS is_home,
                    (g.away_team_key = t.team_key) AS is_away,
                    (g.home_score > g.away_score) AS is_win
                  FROM game g
                  JOIN team t ON (g.home_team_key = t.team_key OR g.away_team_key = t.team_key)
                  JOIN calendar c ON g.date_key = c.date_key
                """
                  f"WHERE t.team_name = '{team_name}'"
                """
                )
                SELECT
                  yr,
                  AVG(points_scored - points_allowed) AS margin_of_victory
                FROM game_stats
                GROUP BY yr
                ORDER BY yr
                """
            )
            
        cursor.execute(sql)
        rows= cursor.fetchall()

        cursor.close()
        conn.close()


        x = [row[0] for row in rows]
        y = [row[1] for row in rows]
        
        plt.plot(x, y)

        
        title = (f'')
        
        plt.title(title)
        plt.xlabel('Year')
        plt.ylabel('Average Points')
        
        plt.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = analyzePlayer()
    sys.exit(app.exec_())
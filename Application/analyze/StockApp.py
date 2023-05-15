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

            #-----------------------------#
            # The Stock application class #
            #-----------------------------#

class StockApp(QWindow):
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
        self.ui = uic.loadUi('StockApp.ui')

        # Initializing company menu
        self._initialize_company_menu()

        # Initialize month menu
        self._initialize_month_menu()

        # Enter price data
        self.ui.search.clicked.connect(self._enter_price_data)
        self.ui.search.clicked.connect(self._update_graph)
        
        self._initialize_price_table()
        self._update_graph()
        
        self.ui.show();
        
    #------------------------#
    # Component initializers #
    #------------------------#
    
    def _initialize_price_table(self):
        """
        Initialize the price table.
        """
        self.ui.price_table.clear()
        
        columns = ['Symbol', 'Date', 'Open', 'High', 'Low', 
                   'Close', 'Volume', 'Company']
        self.ui.price_table.setHorizontalHeaderLabels(columns)
    
    def _initialize_graph(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.graph_layout.count()):
            child = self.ui.graph_layout.itemAt(i).widget()
            if child:
                children.append(child)
                
        # Delete the plots.
        for child in children:
            child.deleteLater()


    def _initialize_company_menu(self):
        """
        Initialize the company menu with company names from the database.
        """
        conn = make_connection(config_file = 'stocks.ini')
        cursor = conn.cursor()
        
        sql = """
                SELECT company
                FROM stocks
            """
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            name = row[0]
            self.ui.company_menu.addItem(name, row)


    def _initialize_month_menu(self):
        """
        Initialize the company menu with company names from the database.
        """
        conn = make_connection(config_file = 'stocks.ini')
        cursor = conn.cursor()
        
        sql = """
                SELECT month_name
                FROM months
            """
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            name = row[0]
            self.ui.month_menu.addItem(name, row)            


    #----------------#
    # Event handlers #
    #----------------#
            
    def _update_graph(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph()
        
        # Add the figure to the UI.
        self.ui.graph_layout.addWidget(FigureCanvas(plt.figure()))
        
        #-------------------#
        # PLACEHOLDER PLOTS #
        #-------------------#
        company = self.ui.company_menu.currentData()[0]
        month   = self.ui.month_menu.currentData()[0]
        alpha   = self.ui.alpha.value()

        conn = make_connection(config_file = 'stocks.ini')
        cursor = conn.cursor()

        conn.cursor().execute('SET @smoothed = NULL')

        sql_y1 = ("""
            SELECT P.low
            FROM prices P, stocks S, months M
            WHERE M.number = P.month
            AND S.symbol = P.symbol
            """
            f"AND M.month_name = '{month}'"
            f"AND S.company = '{company}'"
            )

        sql_y2 = (
            f"SELECT @smoothed := ('{alpha}'*P.low + (1-'{alpha}')*(IF (@smoothed IS NULL, P.low, @smoothed)))"
            """
            FROM prices P, stocks S, months M
            WHERE M.number = P.month
            AND S.symbol = P.symbol
            """
            f"AND M.month_name = '{month}'"
            f"AND S.company = '{company}'"
            )
            
        cursor.execute(sql_y1)
        rows_y1 = cursor.fetchall()

        cursor.execute(sql_y2)
        rows_y2 = cursor.fetchall()


        cursor.close()
        conn.close()

        # print(len(rows_y1))
        # print(rows_y2)

        x = list(range(1, len(rows_y1)+1))
        y1 = [row[0] for row in rows_y1]
        y2 = [row[0] for row in rows_y2]
        plt.plot(x, y1, label='Closing prices')        
        plt.plot(x, y2, label='Smoothed prices')

        
        title = (f'Closing {company} stock prices during {month} 2017\n'
                 f'Exponentially smoothed with alpha = {alpha:.2f}')
        
        plt.title(title)
        plt.xlabel('Day of the month')
        plt.ylabel('Closing price')
        plt.legend()
        
        plt.close()


    def _enter_price_data(self):
        """
        Enter Price data here
        """
        name = self.ui.company_menu.currentData()
        company_name = name[0]
        month = self.ui.month_menu.currentData()
        month_name = month[0]

        conn = make_connection(config_file = 'stocks.ini')
        cursor = conn.cursor()

        sql = ("""
            SELECT P.symbol, P.full_date, P.open, P.high, P.low, P.close, P.volume, S.company
            FROM prices P, stocks S, months M
            WHERE M.number = P.month
            AND S.symbol = P.symbol
            """
            f"AND M.month_name = '{month_name}'"
            f"AND S.company = '{company_name}'"
            )
            
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()         

        for row_number, row_data in enumerate(rows):
            self.ui.price_table.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.ui.price_table.setItem(row_number, column_number, item)



            
    #------#
    # Main #
    #------#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StockApp()
    sys.exit(app.exec_())
from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QTextEdit, QScrollArea, QListWidgetItem
import sys
import math
from functools import partial
from read_write_data import get_shares_list

from forms import *
from likes import *
from filter import find_shares_by_filters


class mywindow(QMainWindow):
	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.sharesListStatuses = {}
		self.isFiltering = False
		self.user = ""
		self.set_shares_list(get_shares_list())

		self.ui.btn_find.clicked.connect(self.btn_find_click)

		self.ui.frame_search.setVisible(True)
		self.ui.frame_cities.setVisible(True)
			
		
		self.frame_shaers = [self.ui.frame_city_1, self.ui.frame_city_2, self.ui.frame_city_3, \
							self.ui.frame_city_4, self.ui.frame_city_5, self.ui.frame_city_6]
		self.shares = [self.ui.name_1, self.ui.name_2, self.ui.name_3, \
							self.ui.name_4, self.ui.name_5, self.ui.name_6]
		self.properties = [self.ui.properties_1, self.ui.properties_2, self.ui.properties_3, \
							self.ui.properties_4, self.ui.properties_5, self.ui.properties_6]


		self.ui.sharesList.itemDoubleClicked.connect(self._handleDoubleClick)



	def set_shares_list(self, shares_arr):
		for item in shares_arr:
			elemList = QListWidgetItem(item)
			elemList.setBackground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
			elemList.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)))
			self.sharesListStatuses[item] = {"status":"none", "prevStatus":"none"}
			self.ui.sharesList.addItem(elemList)

	def _handleDoubleClick(self, item):
		self.clear_frames()
		self.create_frames(6)


		if self.sharesListStatuses[item.text()]["status"] == "none":
			if self.sharesListStatuses[item.text()]["prevStatus"] == "none":
				self.sharesListStatuses[item.text()]["status"] = "like"
				item.setBackground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.green)))
				like_shares, dislike_shares, shares = add_like(item.text())
			elif self.sharesListStatuses[item.text()]["prevStatus"] == "like":
				self.sharesListStatuses[item.text()]["status"] = "dislike"
				self.sharesListStatuses[item.text()]["prevStatus"] = "none"
				item.setBackground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.red)))
				like_shares, dislike_shares, shares = add_dislike(item.text())
			elif self.sharesListStatuses[item.text()]["prevStatus"] == "dislike":
				self.sharesListStatuses[item.text()]["status"] = "like"
				self.sharesListStatuses[item.text()]["prevStatus"] = "none"
				item.setBackground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.green)))
				like_shares, dislike_shares, shares = add_like(item.text())
		elif self.sharesListStatuses[item.text()]["status"] == "like":
			self.sharesListStatuses[item.text()]["status"] = "none"
			self.sharesListStatuses[item.text()]["prevStatus"] = "like"
			item.setBackground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
			like_shares, dislike_shares, shares = remove_like(item.text())
		else:
			self.sharesListStatuses[item.text()]["status"] = "none"
			self.sharesListStatuses[item.text()]["prevStatus"] = "dislike"
			item.setBackground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
			like_shares, dislike_shares, shares = remove_dislike(item.text())

		if (len(shares) > 1):
			self.output_recommend_cities(like_shares, dislike_shares, shares)
		global array_likes, array_dislikes
		print("AFTER UPDATE", array_likes, array_dislikes)
		item.setSelected(False)


#####################################################
# SEARCH BY FILTER
#####################################################
	def btn_find_click(self):
		self.isFiltering = True
		self.clear_frames()
		name = self.ui.line_city_input.text()
		in_ring = self.ui.check_in_ring.isChecked()
		out_ring = self.ui.check_out_ring.isChecked()
		distance = self.ui.combo_distance.currentText()
		theme = self.ui.combo_theme.currentText()

		have_divs = None
		if in_ring:
			have_divs = True
		if out_ring:
			have_divs = False

		cities, another_filter = find_shares_by_filters(name, theme, have_divs, distance)
		if (cities == None):
			self.output_warning2()
			return

		self.create_frames(len(cities))

		if another_filter:
			self.output_warning()

		if cities:
			self.output_shares(cities)


	def create_frames(self, num_frames):
		for i in range(num_frames):
			frame_city, name, properties = add_frame(self.ui.scrollAreaWidgetContents, i)   
			self.ui.gridLayout.addWidget(frame_city, math.floor((i+3) / 3), i % 3)   

			self.frame_shaers.append(frame_city)
			self.shares.append(name)
			self.properties.append(properties)

	def clear_frames(self):
		for i in range(len(self.frame_shaers)):
			self.frame_shaers[i].hide()

		del self.frame_shaers[0:]
		del self.shares[0:]
		del self.properties[0:]

	def output_warning(self):
		msg = QMessageBox()
		msg.setText("По вашему запросу ничего не найдено.\nВозможно, вам понравятся следующие бумаги...")
		msg.setIcon(QMessageBox.Information)
		msg.exec_()

	def output_warning2(self):
		msg = QMessageBox()
		msg.setText("По вашему запросу ничего не найдено.")
		msg.setIcon(QMessageBox.Information)
		msg.exec_()


#####################################################
# OUTPUT shares
#####################################################
	def output_recommend_cities(self, like_shares, dislike_shares, recommend_shares):
		self.clear_properties()
		self.output_shares(recommend_shares)

	def output_shares(self, shares):
		min_len = min(len(shares), len(self.shares))
		for i in range(min_len):
			cur_name = self.shares[i]
			cur_property = self.properties[i]
			cur_city = shares[i]
			self.output_share(cur_name, cur_property, cur_city)

	def output_share(self, name, properties, share):
		name.setText(share["Компания"])

		
		properties.append("Цена: " + str(share["Цена, руб"]) + " руб")
		if (share['Страна'] != None): 
			properties.append("Страна: " + share["Страна"])
		properties.append('ROE: ' + str(share["ROE, %"]) + "%")
		properties.append('Наличие дивидендов: ' + str(share["Наличие дивидендов"]))
		properties.append('Средний возраст владельцев: ' + str(share["Средний возраст владельцев"]))
		if (share['Сектор'] != None): 
			properties.append("Сектор: " + share["Сектор"])

		if (share['P/E'] > 0): 
			properties.append("P/E: " + str(share["P/E"]))
		
		if (share['Тип облигации'] != None): 
			properties.append("Тип облигации: " + share["Тип облигации"])

		if (share['Тип опциона'] != None): 
			properties.append("Тип опциона: " + share["Тип опциона"])

		if (share['Срок'] != None): 
			properties.append("Срок: " + str(share["Срок"]) + " мес.")
		
		properties.append("Риск: " + str(share["Риск"]) + "%")

	def clear_properties(self):
		for cur_property in self.properties:
			cur_property.clear()


if __name__ == "__main__":
	app = QApplication([])

	application = mywindow()
	application.show()

	sys.exit(app.exec())

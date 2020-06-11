import numpy as np
import xlwt

def generate_xls(N_sim, estimate_NLS, estimate_Median1, estimate_Median2, RSS_NLS, RSS_Median1, RSS_Median2):
 
	book = xlwt.Workbook(encoding="utf-8")
	sheet = book.add_sheet("Sheet 1")
	# Table formatting
	sheet.write(3, 2, 'Simulation', xlwt.easyxf("align: horiz center"))
	sheet.write_merge(2, 2, 3, 6, 'Non-linear Least Squares', xlwt.easyxf("align: horiz center")) #ch
	sheet.write_merge(2, 2, 7, 12, 'Median Method', xlwt.easyxf("align: horiz center")) #ch
	sheet.write(3, 3, "Vmax")
	sheet.write(3, 4, "Km")
	sheet.write(3, 5, "Kp")
	sheet.write(3, 6, "Error")
	sheet.write(3, 7, "Vmax")
	sheet.write(3, 8, "Km")
	sheet.write(3, 9, "Kp direct method")
	sheet.write(3, 10, "Error DM")
	sheet.write(3, 11, "Kp inverse method")
	sheet.write(3, 12, "Error IM")
	
	# Addding data
	for k in range(N_sim):
		row = sheet.row(k+4)
		row.write(2, k, xlwt.easyxf("align: horiz left"))
		row.write(3, estimate_NLS[k][0])
		row.write(4, estimate_NLS[k][1])
		row.write(5, estimate_NLS[k][2])
		row.write(6, RSS_NLS[k])
		row.write(7, estimate_Median1[k][0])
		row.write(8, estimate_Median1[k][1])
		row.write(9, estimate_Median1[k][2])
		row.write(10, RSS_Median1[k])
		row.write(11, estimate_Median2[k][2])
		row.write(12, RSS_Median2[k])	
	book.save("data.xls")

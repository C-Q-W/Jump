import cv2
import pyautogui
import math
import os
import time

def cal_area(contour):
	area = cv2.contourArea(contour)
	return area

def get_distance(pt1, pt2):
	"""
	计算两个点之间的直线距离
	通过屏幕中两个点的距离，乘以按压/距离的比例系数，就可以求出按压时间，并使用adb模拟按压
	"""
	distance_x = abs(pt1[0] - pt2[0])
	distance_y = abs(pt1[1] - pt2[1])
	distance = math.sqrt(distance_x * distance_x + distance_y * distance_y)
	return distance

if __name__ == '__main__':

	time.sleep(0.5)
	count = 0
	reborn = 0
	reborn_times = 5

	# 获取当前屏幕分辨率
	screenWidth, screenHeight = pyautogui.size()

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

	while True:

		ratio = 2.815
		
		time.sleep(1.5)

		# os.system("adb shell screencap -p /sdcard/img.png")
		# os.system("adb pull /sdcard/img.png")

		pyautogui.screenshot("img.png")
		img = cv2.imread("img.png")
		img = img[460 : 635, 792 : 1128]
		mask1 = cv2.inRange(img, (150, 200, 240), (200, 245, 255))
		mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)

		contours, hierarchy = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		contours = list(contours)
		contours.sort(key = cal_area, reverse = True)

		if len(contours) < 2:
			time.sleep(5)
			pyautogui.screenshot("img.png")
			img = cv2.imread("img.png")
			B, G, R = img[255][1105]
			if B > 100 and G > 100 and R > 100:
				pyautogui.click(1105, 255)
				continue
			elif reborn < reborn_times:
				reborn += 1
				print(f"第{reborn}次复活：{count - 1}步")
				pyautogui.click(1030, 730)
				time.sleep(37)
				pyautogui.click(900, 245)
				time.sleep(7)
				ratio -= 0.7
				continue
			else:
				print(f"游戏结束，共{count - 1}步")
				break

		(x0, y0, w0, h0) = cv2.boundingRect(contours[0])
		(x1, y1, w1, h1) = cv2.boundingRect(contours[1])

		c0 = (x0 + w0 // 2, y0 + h0 //2)
		c1 = (x1 + w1 // 2, y1 + h1 //2)
		target = c0 if c0[1] < c1[1] else c1

		half_img = img[100 : 165, : ]
		mask2 = cv2.inRange(half_img, (0, 30, 30), (80, 100, 100))

		contours, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		contours = list(contours)
		contours.sort(key = cal_area, reverse = True)

		if len(contours) == 0:
			time.sleep(5)
			pyautogui.screenshot("img.png")
			img = cv2.imread("img.png")
			B, G, R = img[255][1105]
			if B > 100 and G > 100 and R > 100:
				pyautogui.click(1105, 255)
				continue
			elif reborn < reborn_times:
				reborn += 1
				print(f"第{reborn}次复活：{count - 1}步")
				pyautogui.click(1030, 730)
				time.sleep(37)
				pyautogui.click(900, 245)
				time.sleep(7)
				ratio -= 0.7
				continue
			else:
				print(f"游戏结束，共{count - 1}步")
				break
				
		(x2, y2, w2, h2) = cv2.boundingRect(contours[0])
		position = (x2 + w2 // 2, y2 + h2 + 100)

		cv2.circle(img, position, 1, (255, 0, 0), 5)
		cv2.circle(img, target, 1, (255, 0, 0), 5)
		cv2.line(img, position, target, (255, 0, 0), 3)

		distance = get_distance(position, target)
		print("distance =", distance)

		if distance > 183:
			ratio += 0.075
		if distance > 193:
			ratio += 0.075
		if distance > 203:
			ratio += 0.05

		if distance < 130:
			ratio -= 0.1
		if distance < 110:
			ratio -= 0.1
		if distance < 100:
			ratio -= 0.1
		real_dis = distance * ratio

		cv2.imshow("img", img)
		cv2.imshow("mask", mask1)
		cv2.waitKey(1)

		# 保存图片，方便在调试时查看识别的准确性
		# cv2.imwrite(f"save/img{count}.png", img)
		# cv2.imwrite(f"save/mask{count}.png", mask1)
		count += 1

		# auto
		time.sleep(0.25)
		pyautogui.moveTo(screenWidth // 2, screenHeight // 2)
		time.sleep(0.25)
		pyautogui.mouseDown()
		time.sleep(real_dis * 0.001)
		pyautogui.mouseUp()

		# debug
		# key = cv2.waitKey()

		# # 等待按下Enter键
		# if key == 13:
		# 	# 使用adb对手机进行模拟按压，即完成跳动之前的蓄力动作
		# 	# os.system(f"adb shell input swipe 250 250 250 250 {real_dis}")
		# 	time.sleep(0.25)
		# 	pyautogui.moveTo(screenWidth // 2, screenHeight // 2)
		# 	time.sleep(0.25)
		# 	pyautogui.mouseDown()
		# 	time.sleep(real_dis * 0.001)
		# 	pyautogui.mouseUp()
		# elif key == 27:
		# 	break

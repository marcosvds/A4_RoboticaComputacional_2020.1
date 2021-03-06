#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = ["Rachel P. B. Moraes", "Igor Montagner", "Fabio Miranda"]


import rospy
import numpy as np
import tf
import math
import cv2
import time
from geometry_msgs.msg import Twist, Vector3, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cormodule
from sensor_msgs.msg import LaserScan

bridge = CvBridge()

mode = "Searching"
cv_image = None
dist = None
media = []
centro = []
atraso = 1.5E9 # 1 segundo e meio. Em nanossegundos

area = 0.0 # Variavel com a area do maior contorno

# Só usar se os relógios ROS da Raspberry e do Linux desktop estiverem sincronizados. 
# Descarta imagens que chegam atrasadas demais
check_delay = False 

def scaneou(dado):
    global dist #Definindo distância como uma variável global
    dist = np.array(dado.ranges).round(decimals=2)[0]

# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
	print("frame")
	global cv_image
	global media
	global dist
	global centro
	global mode

	now = rospy.get_rostime()
	imgtime = imagem.header.stamp
	lag = now-imgtime # calcula o lag
	delay = lag.nsecs
	print("delay ", "{:.3f}".format(delay/1.0E9))
	if delay > atraso and check_delay==True:
		print("Descartando por causa do delay do frame:", delay)
		return 
	try:
		antes = time.clock()
		cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
		# cv_image = cv2.flip(cv_image, -1)
		media, centro, maior_area =  cormodule.identifica_cor(cv_image, dist, mode)
		depois = time.clock()
		cv2.imshow("Camera", cv_image)
	except CvBridgeError as e:
		print('ex', e)
	
if __name__=="__main__":
	rospy.init_node("cor")

	# topico_imagem = "/kamera"
	topico_imagem = "/camera/rgb/image_raw/compressed"
	
	recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame,queue_size=4, buff_size = 2**24)
	recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)
	print("Usando ", topico_imagem)

	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

	try:


		while not rospy.is_shutdown():
			print(dist)
			vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
			if len(media) != 0 and len(centro) != 0:

				if mode != "Aproach started" and mode != "In front of object":
					if (media[0] > centro[0]):
						vel = Twist(Vector3(0,0,0), Vector3(0,0,-0.1))
						mode = "Searching"
					if (media[0] < centro[0]):
						vel = Twist(Vector3(0,0,0), Vector3(0,0,0.1))
						mode = "Searching"
					if (abs(media[0] - centro[0]) < 10):
						vel = Twist(Vector3(0.1,0,0), Vector3(0,0,0))
						mode = "Tracking"
				if dist < 1.5 and (mode == "Tracking" or mode == "Aproach started"):
					vel = Twist(Vector3(0.1,0,0), Vector3(0,0,0))
					mode = "Aproach started"
				if dist < 0.25 and (mode == "In front of object" or mode == "Aproach started"):
					vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
					mode = "In front of object"
			velocidade_saida.publish(vel)
			rospy.sleep(0.1)

	except rospy.ROSInterruptException:
	    print("Ocorreu uma exceção com o rospy")


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

	global cv_image
	global media
	global dist
	global centro
	global mode
	global area

	now = rospy.get_rostime()
	imgtime = imagem.header.stamp
	lag = now-imgtime # calcula o lag
	delay = lag.nsecs

	if delay > atraso and check_delay==True:
		print("Descartando por causa do delay do frame:", delay)
		return 
	try:
		antes = time.clock()
		cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
		# cv_image = cv2.flip(cv_image, -1)
		media, centro, maior_area =  cormodule.identifica_cor(cv_image, dist, mode)
		area = maior_area
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
	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

	try:
		while not rospy.is_shutdown():
			
			if notturn == True:
				current_angle = 0
			vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
			t0 = rospy.Time.now().to_sec()
			angular_speed = (math.pi/10)
			objects = []
			while current_angle < (2*math.pi):
				vel = Twist(Vector3(0,0,0), Vector3(0,0,angular_speed))
				velocidade_saida.publish(vel)
				rospy.sleep(0.2)
				print(area)
				#objects.append(area)
				t1 = rospy.Time.now().to_sec()
				current_angle = angular_speed*(t1-t0)
				print(current_angle)
			vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
			notturn = False
			velocidade_saida.publish(vel)
			rospy.sleep(0.1)

	except rospy.ROSInterruptException:
	    print("Ocorreu uma exceção com o rospy")


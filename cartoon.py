#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import subprocess

# Initialize ROS node
rospy.init_node('cartoonize_image_node')

# Initialize the image publisher and subscriber
image_pub = rospy.Publisher('cartoonized_image', Image, queue_size=10)

# Initialize the OpenCV bridge
bridge = CvBridge()

def main():
    # Load the image from the desktop
    file_path = os.path.join(os.path.expanduser('~'), 'Pictures', 'A1.png')
    image = cv2.imread(file_path)

    # Apply the cartoonize filter
    cartoon_image = cartoonize(image)

    # Publish the cartoonized image
    image_pub.publish(bridge.cv2_to_imgmsg(cartoon_image, "bgr8"))

    # Display the cartoonized image using image_view
    display_image(cartoon_image)

def cartoonize(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply median blur to reduce noise
    blur = cv2.medianBlur(gray, 9)

    # Apply adaptive thresholding to create a cartoon effect
    threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

    # Convert back to BGR format
    cartoon_image = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)

    return cartoon_image

def display_image(image):
    # Convert the image to ROS format
    ros_image = bridge.cv2_to_imgmsg(image, "bgr8")

    # Save the image to a temporary file
    file_path = os.path.join(os.path.expanduser('~'), 'Pictures', 'A2.png')
    cv2.imwrite(file_path, image)

    # Launch the image_view node to display the image
    
    #image_topic = ros_image.name()
    #subprocess.Popen(['rosrun', 'image_view', 'image_view', 'image:={}'.format(image_topic), '_name:=image_viewer'])



if __name__ == '__main__':
    main()
    
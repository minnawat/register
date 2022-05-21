# import the opencv library
from attr import NOTHING
import cv2
from cv2 import VideoCapture
import pytesseract
import requests
import re
import threading
import time
from command import *
from fuzzysearch import find_near_matches




#all varibles
img = cv2.imread('testimage0.jpg')
gray = get_grayscale(img)
thresh = thresholding(gray)
title = ["Mr." , "Mrs." , "Miss"]
month = ["Jan." , "Feb." , "Mar." , "Apr." , "May" , "Jun." , "Jul." , "Aug." , "Sep." , "Oct." , "Nov." , "Dec."]
month_num = ["01" , "02" , "03" , "04" , "05" , "06" , "07" , "08" , "09" , "10" , "11" ,"12"]
text = pytesseract.image_to_string(thresh)
text_norm = pytesseract.image_to_string(img)
uname = ''
uid = ''
udate = ''
uname_thresh_found = False
uname_norm_found = False
udate_thresh_found = False
udate_norm_found = False
payload = {'name': uname, 'id': uid , 'date': udate}
save_frame = NOTHING
event = threading.Event()




class Video(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = False
		self.vid = VideoCapture(0)

	def run(self):
		self.running = True
		global text
		global text_norm
		global fulltext
		global fulltext_norm
		global save_frame

		print("start video")
		# define a video capture object
		#vid = cv2.VideoCapture("v4l2src device=/dev/video1 ! video/x-raw, format=YUY2 ! videoconvert ! video/x-raw, format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
		self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		# define pytesseract
		print("camera define")
			# Capture the video frame
			# by frame
		while(self.running):
      
			# Capture the video frame
			# by frame
			ret, frame = self.vid.read()
			if ret == True:
				# Display the resulting frame
				#cv2.imshow('frame', frame)
				
				# the 'q' button is set as the
				# quitting button you may use any
				# desired button of your choice
				save_frame = frame
				time.sleep(0.1)
	
	def close(self):
		self.running = False
		# After the loop release the cap object
		self.vid.release()
		# Destroy all the windows
		cv2.destroyAllWindows()

	def find_name_norm(self):
		global uname_norm_found
		global uname
		global text_norm
		global fulltext_norm

		new_text = []
		uname = ''
		lastname = ''
		for x in title :
			matches = [match for match in text_norm if x in match]
			if matches:
				uname = uname.join(matches)
				for x in title :
				#print(x)
					location = uname.find(x)
					if(location != -1):
						location = location + len(x) + 1
						#name_local = text.find("Lastname",location)
						break
				uname = uname[location : len(uname)]
				uname.strip()
				if uname.find(' ') > 0:
					uname = 'void'
					break
			else:
				for x in title :
					if find_near_matches(x,fulltext_norm, max_l_dist=1) :
						data = ''.join(str(find_near_matches(x,fulltext_norm, max_l_dist=1)))
						location = data.find("matched=")
						if (location != -1):
							location = location + 8
							end_local = data.find(")",location)
							w_word = data[location : end_local]
							w_word = w_word.replace('\'',"")
							w_word = w_word.replace('\"',"")
							#print(w_word)
							for y in text_norm:
								new_udate = y.replace(w_word,x)
								new_text.append(new_udate)
							break
					matches = [match for match in new_text if x in match]
					if matches:
						uname = uname.join(matches)
						for x in title :
							location = uname.find(x)
							if(location != -1):
								location = location + len(x) + 1
								break
						uname = uname[location : len(uname)]
						if uname.find(" ") > 0:
							uname = 'void'
							break
					else :
						uname = 'void'


		matches = [match for match in text_norm if "Lastname" in match]
		if matches:
			lastname = lastname.join(matches)
			location = lastname.find("Lastname")
			if(location != -1):
				location = location + 8
				#name_local = text.find("Lastname",location)
			lastname = lastname[location : len(lastname)]
			if lastname.find(" "):
				lastname == 'void'
		elif not matches:
			matches = [match for match in text_norm if "Last name" in match]
			if matches:
				lastname = lastname.join(matches)
				location = lastname.find("Last name")
				if(location != -1):
					location = location + 10
					#name_local = text.find("Lastname",location)
				lastname = lastname[location : len(lastname)]
				if lastname.find(" "):
					lastname == 'void'
		elif(find_near_matches('last name',fulltext_norm, max_l_dist=1)):
			data = ''.join(str(find_near_matches('last name',fulltext_norm, max_l_dist=1)))
			location = data.find("matched=")
			if (location != -1):
				location = location + 9
				end_local = data.find(")",location)
				w_word = data[location : end_local]
				w_word = w_word.replace('\'',"")
				w_word = w_word.replace('\"',"")
			new_text = []
			for x in text:
				new_udate = x.replace(w_word,"last name")
				new_text.append(new_udate)
			matches = [match for match in new_text if "Lastname" in match]
			if matches:
				lastname = lastname.join(matches)
				location = lastname.find("Lastname")
				if(location != -1):
					location = location + 9
				lastname = lastname[location : len(lastname)]
				if lastname.find(" "):
					lastname == 'void'
		else:
			lastname = 'void'
		if uname != 'void' and lastname != 'void':
			uname = uname + " " + lastname
			uname_norm_found = True
		else:
			return 'void'
		return uname

	def find_name(self):
		global uname_thresh_found
		global uname
		global text
		global fulltext
		
		new_text = []
		uname = ''
		lastname = ''
		for x in title :
			matches = [match for match in text if x in match]
			if matches:
				uname = uname.join(matches)
				for x in title :
				#print(x)
					location = uname.find(x)
					if(location != -1):
						location = location + len(x) + 1
						#name_local = text.find("Lastname",location)
						break
				uname = uname[location : len(uname)]
				if uname.find(' ') > 0:
					uname = 'void'
					break

			
			else:
				for x in title :
					if find_near_matches(x,fulltext, max_l_dist=1) :
						data = ''.join(str(find_near_matches(x,fulltext, max_l_dist=1)))
						location = data.find("matched=")
						if (location != -1):
							location = location + 8
							end_local = data.find(")",location)
							w_word = data[location : end_local]
							w_word = w_word.replace('\'',"")
							w_word = w_word.replace('\"',"")
							#print(w_word)
							for y in text:
								new_udate = y.replace(w_word,x)
								new_text.append(new_udate)
							break
					matches = [match for match in new_text if x in match]
					if matches:
						uname = uname.join(matches)
						for x in title :
							location = uname.find(x)
							if(location != -1):
								location = location + len(x) + 1
								break
						uname = uname[location : len(uname)]
						if uname.find(" ") > 0:
							uname = 'void'
							break
					else :
						uname = 'void'

		matches = [match for match in text if "Lastname" in match]
		if matches:
			lastname = lastname.join(matches)
			location = lastname.find("Lastname")
			if(location != -1):
				location = location + 9
			lastname = lastname[location : len(lastname)]
		elif not matches:
			matches = [match for match in text_norm if "Last name" in match]
			if matches:
				lastname = lastname.join(matches)
				location = lastname.find("Last name")
				if(location != -1):
					location = location + 10
					#name_local = text.find("Lastname",location)
				lastname = lastname[location : len(lastname)]
				if lastname.find(" "):
					lastname == 'void'
		elif(find_near_matches('last name',fulltext, max_l_dist=1)):
			data = ''.join(str(find_near_matches('last name',fulltext_norm, max_l_dist=1)))
			location = data.find("matched=")
			if (location != -1):
				location = location + 9
				end_local = data.find(")",location)
				w_word = data[location : end_local]
				w_word = w_word.replace('\'',"")
				w_word = w_word.replace('\"',"")
			new_text = []
			for x in text:
				new_udate = x.replace(w_word,"lastname")
				new_text.append(new_udate)
			matches = [match for match in new_text if "Lastname" in match]
			if matches:
				lastname = lastname.join(matches)
				location = lastname.find("Lastname")
				if(location != -1):
					location = location + 9
				lastname = lastname[location : len(lastname)]
		else:
			lastname = 'void'
		if uname != 'void' and lastname != 'void':
			uname = uname + " " + lastname
			uname_thresh_found = True
		else: uname = 'void'
		#print(uname)
		return uname

	def find_date_norm(self):
		global udate_norm_found
		global udate
		global text_norm
		global fulltext_norm

		matches = [match for match in text_norm if "Date of Birth" in match]
		if matches:
			udate = udate.join(matches)
			i = 0
			for x in month :
					location = udate.find(x)
					if (location != -1):
						udate = udate.replace(x,month_num[i])
						break
					i = i+1
			udate = udate.replace("Date of Birth","")
			udate = udate.strip()
			temp = udate.split()
			udate = temp[2] + "-" + temp[1] + "-" + temp[0]

		elif(find_near_matches('Date of Birth',fulltext_norm, max_l_dist=2)):
			data = ''.join(str(find_near_matches('Date of Birth',fulltext_norm, max_l_dist=2)))
			location = data.find("matched=")
			if (location != -1):
				location = location + 8
				end_local = data.find(")",location)
				w_word = data[location : end_local]
				w_word = w_word.replace('\'',"")
				w_word = w_word.replace('\"',"")
				#print(w_word)
			new_text = []
			for x in text_norm:
				new_udate = x.replace(w_word,"Date of Birth")
				new_text.append(new_udate)
			#print(new_text)
			matches = [match for match in new_text if "Date of Birth" in match]
			if matches:
				udate = udate.join(matches)
				i = 0
				for x in month :
						location = udate.find(x)
						if (location != -1):
							udate = udate.replace(x,month_num[i])
							break
						i = i+1
				udate = udate.replace("Date of Birth","")
				udate = udate.strip()
				temp = udate.split()
				udate = temp[2] + "-" + temp[1] + "-" + temp[0]

				#print(udate)
		if udate == None or udate == '':
			udate_norm_found = False
			return 'void'
		udate_norm_found = True
		return udate

	def find_date(self):
		global udate_thresh_found
		global udate
		global text
		global fulltext
		'''
		for x in month:
			matches = [match for match in text if "\d{2} " + x + " \d{4}" in match]
			if matches:
				udate = udate.join(matches)
				return udate
		'''
		matches = [match for match in text if "Date of Birth" in match]
		if matches:
			udate = udate.join(matches)
			i = 0
			for x in month :
					location = udate.find(x)
					if (location != -1):
						udate = udate.replace(x,month_num[i])
						break
					i = i+1
			udate = udate.replace("Date of Birth","")
			udate = udate.strip()
			temp = udate.split()
			udate = temp[2] + "-" + temp[1] + "-" + temp[0]

		elif(find_near_matches('Date of Birth',fulltext, max_l_dist=2)):
			data = ''.join(str(find_near_matches('Date of Birth',fulltext, max_l_dist=2)))
			location = data.find("matched=")
			if (location != -1):
				location = location + 8
				end_local = data.find(")",location)
				w_word = data[location : end_local]
				w_word = w_word.replace('\'',"")
				w_word = w_word.replace('\"',"")
				#print(w_word)
			new_text = []
			for x in text:
				new_udate = x.replace(w_word,"Date of Birth")
				new_text.append(new_udate)
			#print(new_text)
			matches = [match for match in new_text if "Date of Birth" in match]
			if matches:
				udate = udate.join(matches)
				i = 0
				for x in month :
						location = udate.find(x)
						if (location != -1):
							udate = udate.replace(x,month_num[i])
							break
						i = i+1
				udate = udate.replace("Date of Birth","")
				udate = udate.strip()
				temp = udate.split()
				udate = temp[2] + "-" + temp[1] + "-" + temp[0]

				#print(udate)
		if udate == None or udate == '':
			udate_thresh_found = False
			return 'void'
		udate_thresh_found = True
		return udate


	def find_id(self):
		global uname_norm_found
		global uname_thresh_found
		global udate_norm_found
		global udate_thresh_found
		global uid
		global fulltext
		global fulltext_norm


		if(uname_norm_found == True and udate_norm_found == True):
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", fulltext_norm)
			uid = uid.join(id)
			uid = uid.replace(" ","")
		elif (uname_thresh_found == True and udate_thresh_found == True):
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", fulltext)
			uid = uid.join(id)
			uid = uid.replace(" ","")
		elif uname_thresh_found == True:
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", fulltext)
			uid = uid.join(id)
			uid = uid.replace(" ","")
		elif uname_norm_found == True:
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", fulltext_norm)
			uid = uid.join(id)
			uid = uid.replace(" ","")
		else :
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", fulltext)
			uid = uid.join(id)
			uid = uid.replace(" ","")
		if uid == '' :
			uid = 'void'
		return uid

	def search_send(self):
		global img
		global payload
		global uname
		global uid
		global udate
		global fulltext
		global fulltext_norm
		global save_frame


		cv2.imwrite('testimage0.jpg',save_frame)
		img = np.array(img)
		img = cv2.imread('testimage0.jpg')
		print("start to read image")
		gray = get_grayscale(img)
		print("got grayscale")
		thresh = thresholding(gray)
		print("got threshold")
		text = pytesseract.image_to_string(thresh)
		print("tesseract 1")
		text_norm = pytesseract.image_to_string(img)
		print("tesseract 2")
		text = text.splitlines()
		text_norm = text_norm.splitlines()
		#img_tha = img_tha.splitlines()
		#print(text)
		fulltext = ''.join(text)
		fulltext_norm = ''.join(text_norm)
		print(text)
		print(text_norm)
		print("word splited")
		
		if self.find_name() == 'void':
			print(self.find_name_norm())
		else: 
			print(self.find_name())
		if self.find_date() == 'void':
			print(self.find_date_norm())
		else: 
			print(self.find_date())
		print(self.find_id())
		if not uname:
			uname = 'void'
		if not uid:
			uid = 'void'
		if not udate:
			udate = '0000-00-00'
		payload = {"name" : uname , "id" : uid , "date" : udate}
		print(uname)
		print(uid)
		print(udate)
		r = requests.get('https://smartregis00.herokuapp.com/receive', params=payload)
		if r:
			print("send successful")
			print(r)
		else:
			print("something went wrong check response code")
			print(r)
		

capture = Video()
#thread = video()
#thread.start()
#print(text)
#cv2.imshow('',gray)
#cv2.waitKey(0)
##print(text)
#vide = video()
#vide.run()
#cap = search_send()
#cap.run()
# After the loop release the cap object
#vid.release()
# Destroy all the windows
#cv2.destroyAllWindows()

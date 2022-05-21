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





class Video(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = False
		self.reading = False
		self.vid = VideoCapture(1)
		self.img = cv2.imread('testimage0.jpg')
		self.gray = get_grayscale(img)
		self.thresh = thresholding(gray)
		self.title = ["Mr." , "Mrs." , "Miss"]
		self.month = ["Jan." , "Feb." , "Mar." , "Apr." , "May" , "Jun." , "Jul." , "Aug." , "Sep." , "Oct." , "Nov." , "Dec."]
		self.month_num = ["01" , "02" , "03" , "04" , "05" , "06" , "07" , "08" , "09" , "10" , "11" ,"12"]
		self.text = pytesseract.image_to_string(thresh)
		self.text_norm = pytesseract.image_to_string(img)
		self.uname = ''
		self.uid = ''
		self.udate = ''
		self.fulltext = NOTHING
		self.fulltext_norm = NOTHING
		self.uname_thresh_found = False
		self.uname_norm_found = False
		self.udate_thresh_found = False
		self.udate_norm_found = False
		self.payload = {'name': self.uname, 'id': self.uid , 'date': self.udate}
		self.save_frame = NOTHING

	def run(self):
		self.running = True

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
				cv2.imshow('frame', frame)
				cv2.waitKey(1)
				# the 'q' button is set as the
				# quitting button you may use any
				# desired button of your choice
				self.save_frame = frame
				#time.sleep(0.1)
			if self.reading == True:
				self.search_send()
				self.reading = False
	
	def close(self):
		self.running = False
		# After the loop release the cap object
		self.vid.release()
		# Destroy all the windows
		cv2.destroyAllWindows()
	
	def read(self):
		print("start function read")
		self.reading = True

	def find_name_norm(self):

		new_text = []
		self.uname = ''
		lastname = ''
		for x in title :
			matches = [match for match in self.text_norm if x in match]
			if matches:
				self.uname = self.uname.join(matches)
				for x in title :
				#print(x)
					location = uname.find(x)
					if(location != -1):
						location = location + len(x) + 1
						#name_local = text.find("Lastname",location)
						break
				self.uname = self.uname[location : len(self.uname)]
				self.uname = self.uname.strip()
				if self.uname.find(' ') > 0:
					self.uname = 'void'
					break
			else:
				for x in title :
					if find_near_matches(x,self.fulltext_norm, max_l_dist=1) :
						data = ''.join(str(find_near_matches(x,self.fulltext_norm, max_l_dist=1)))
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
						self.uname = self.uname.join(matches)
						for x in title :
							location = self.uname.find(x)
							if(location != -1):
								location = location + len(x) + 1
								break
						self.uname = self.uname[location : len(self.uname)]
						if uname.find(" ") > 0:
							self.uname = 'void'
							break
					else :
						self.uname = 'void'


		matches = [match for match in self.text_norm if "Lastname" in match]
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
			matches = [match for match in self.text_norm if "Last name" in match]
			if matches:
				lastname = lastname.join(matches)
				location = lastname.find("Last name")
				if(location != -1):
					location = location + 10
					#name_local = text.find("Lastname",location)
				lastname = lastname[location : len(lastname)]
				if lastname.find(" "):
					lastname == 'void'
		elif(find_near_matches('last name',self.fulltext_norm, max_l_dist=1)):
			data = ''.join(str(find_near_matches('last name',self.fulltext_norm, max_l_dist=1)))
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
		if self.uname != 'void' and lastname != 'void':
			self.uname = self.uname + " " + lastname
			self.uname_norm_found = True
		else:
			return 'void'
		return self.uname

	def find_name(self):
		
		new_text = []
		self.uname = ''
		lastname = ''
		for x in title :
			matches = [match for match in self.text if x in match]
			if matches:
				self.uname = self.uname.join(matches)
				for x in title :
				#print(x)
					location = self.uname.find(x)
					if(location != -1):
						location = location + len(x) + 1
						#name_local = text.find("Lastname",location)
						break
				self.uname = self.uname[location : len(self.uname)]
				self.uname = self.uname.strip()
				if self.uname.find(' ') > 0:
					self.uname = 'void'
					break
			else:
				for x in title :
					if find_near_matches(x,self.fulltext, max_l_dist=1) :
						data = ''.join(str(find_near_matches(x,self.fulltext, max_l_dist=1)))
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
						print("pass through break")
					matches = [match for match in new_text if x in match]
					if matches:
						self.uname = self.uname.join(matches)
						for x in title :
							location = self.uname.find(x)
							if(location != -1):
								location = location + len(x) + 1
								break
						self.uname = self.uname[location : len(self.uname)]
						self.uname = self.uname.strip()
						if self.uname.find(" ") > 0:
							self.uname = 'void'
							break
					else :
						self.uname = 'void'
		print("look for lastname")
		matches = [match for match in self.text if "Lastname" in match]
		print(matches)
		if matches:
			print("lastname match thresh")
			lastname = lastname.join(matches)
			location = lastname.find("Lastname")
			if(location != -1):
				location = location + 9
			lastname = lastname[location : len(lastname)]
		elif not matches:
			matches = [match for match in self.text_norm if "Last name" in match]
			if matches:
				lastname = lastname.join(matches)
				location = lastname.find("Last name")
				if(location != -1):
					location = location + 10
					#name_local = text.find("Lastname",location)
				lastname = lastname[location : len(lastname)]
				if lastname.find(" "):
					lastname == 'void'
		elif(find_near_matches('last name',self.fulltext, max_l_dist=1)):
			data = ''.join(str(find_near_matches('last name',self.fulltext_norm, max_l_dist=1)))
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
		if self.uname != 'void' and lastname != 'void':
			self.uname = self.uname + " " + lastname
			self.uname_thresh_found = True
		else: self.uname = 'void'
		#print(uname)
		return self.uname

	def find_date_norm(self):


		matches = [match for match in self.text_norm if "Date of Birth" in match]
		if matches:
			self.udate = self.udate.join(matches)
			i = 0
			for x in self.month :
					location = self.udate.find(x)
					if (location != -1):
						self.udate = self.udate.replace(x,self.month_num[i])
						break
					i = i+1
			self.udate = self.udate.replace("Date of Birth","")
			self.udate = self.udate.strip()
			temp = self.udate.split()
			self.udate = temp[2] + "-" + temp[1] + "-" + temp[0]

		elif(find_near_matches('Date of Birth',self.fulltext_norm, max_l_dist=2)):
			data = ''.join(str(find_near_matches('Date of Birth',self.fulltext_norm, max_l_dist=2)))
			location = data.find("matched=")
			if (location != -1):
				location = location + 8
				end_local = data.find(")",location)
				w_word = data[location : end_local]
				w_word = w_word.replace('\'',"")
				w_word = w_word.replace('\"',"")
				#print(w_word)
			new_text = []
			for x in self.text_norm:
				new_udate = x.replace(w_word,"Date of Birth")
				new_text.append(new_udate)
			#print(new_text)
			matches = [match for match in new_text if "Date of Birth" in match]
			if matches:
				self.udate = self.udate.join(matches)
				i = 0
				for x in self.month :
						location = self.udate.find(x)
						if (location != -1):
							self.udate = self.udate.replace(x,self.month_num[i])
							break
						i = i+1
				self.udate = self.udate.replace("Date of Birth","")
				self.udate = self.udate.strip()
				temp = self.udate.split()
				self.udate = temp[2] + "-" + temp[1] + "-" + temp[0]

				#print(udate)
		if not self.udate or self.udate == '':
			self.udate_norm_found = False
			return 'void'
		self.udate_norm_found = True
		return self.udate

	def find_date(self):
		'''
		for x in month:
			matches = [match for match in text if "\d{2} " + x + " \d{4}" in match]
			if matches:
				udate = udate.join(matches)
				return udate
		'''
		matches = [match for match in self.text if "Date of Birth" in match]
		if matches:
			self.udate = self.udate.join(matches)
			i = 0
			for x in self.month :
					location = self.udate.find(x)
					if (location != -1):
						self.udate = self.udate.replace(x,self.month_num[i])
						break
					i = i+1
			self.udate = self.udate.replace("Date of Birth","")
			self.udate = self.udate.strip()
			temp = self.udate.split()
			self.udate = temp[2] + "-" + temp[1] + "-" + temp[0]
		elif(find_near_matches('Date of Birth',self.fulltext, max_l_dist=2)):
			data = ''.join(str(find_near_matches('Date of Birth',self.fulltext, max_l_dist=2)))
			location = data.find("matched=")
			if (location != -1):
				location = location + 8
				end_local = data.find(")",location)
				w_word = data[location : end_local]
				w_word = w_word.replace('\'',"")
				w_word = w_word.replace('\"',"")
				#print(w_word)
			new_text = []
			for x in self.text:
				new_udate = x.replace(w_word,"Date of Birth")
				new_text.append(new_udate)
			print(new_text)
			matches = [match for match in new_text if "Date of Birth" in match]
			if matches:
				self.udate = self.udate.join(matches)
				i = 0
				for x in self.month :
						location = self.udate.find(x)
						if (location != -1):
							self.udate = self.udate.replace(x,self.month_num[i])
							break
						i = i+1
				self.udate = self.udate.replace("Date of Birth","")
				self.udate = self.udate.strip()
				temp = self.udate.split()
				self.udate = temp[2] + "-" + temp[1] + "-" + temp[0]

				#print(udate)
		if not self.udate or self.udate == '':
			self.udate_thresh_found = False
			return 'void'
		self.udate_thresh_found = True
		return self.udate


	def find_id(self):

		id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", self.fulltext_norm)
		if not id:
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", self.fulltext)
		self.uid = self.uid.join(id)
		self.uid = self.uid.replace(" ","")


		'''if(self.uname_norm_found == True and self.udate_norm_found == True):
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", self.fulltext_norm)
			self.uid = self.uid.join(id)
			self.uid = self.uid.replace(" ","")
		elif (self.uname_thresh_found == True and self.udate_thresh_found == True):
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", self.fulltext)
			self.uid = self.uid.join(id)
			self.uid = self.uid.replace(" ","")
		elif self.uname_thresh_found == True:
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", self.fulltext)
			self.uid = self.uid.join(id)
			self.uid = self.uid.replace(" ","")
		elif uname_norm_found == True:
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", self.fulltext_norm)
			self.uid = self.uid.join(id)
			self.uid = self.uid.replace(" ","")
		else :
			id = re.findall("\d{1} \d{4} \d{5} \d{2} \d{1}", self.fulltext)
			self.uid = self.uid.join(id)
			self.uid = self.uid.replace(" ","")
		if self.uid == '' :
			self.uid = 'void'''
		return self.uid

	def search_send(self):


		print("start search and send")
		cv2.imwrite('testimage0.jpg',self.save_frame)
		self.img = np.array(self.img)
		self.img = cv2.imread('testimage0.jpg')
		print("start to read image")
		self.gray = get_grayscale(self.img)
		print("got grayscale")
		self.thresh = thresholding(self.gray)
		print("got threshold")
		self.text = pytesseract.image_to_string(self.thresh)
		print("tesseract 1")
		self.text_norm = pytesseract.image_to_string(self.img)
		print("tesseract 2")
		self.text = self.text.splitlines()
		self.text_norm = self.text_norm.splitlines()
		#img_tha = img_tha.splitlines()
		#print(text)
		self.fulltext = ''.join(self.text)
		self.fulltext_norm = ''.join(self.text_norm)
		print(self.text)
		print(self.text_norm)
		print("word splited")
		
		if self.uname_norm_found:
			print(self.find_name_norm() + " norm")
		else: 
			print(self.find_name() + " thresh")
		if self.udate_norm_found and not self.udate_thresh_found:
			print(self.find_date_norm() + " norm")
		else: 
			print(self.find_date() + " thresh")
		print(self.find_id())
		if not self.uname:
			self.uname = 'void'
		if not self.uid:
			self.uid = 'void'
		if not self.udate:
			self.udate = '2000-01-01'
		self.payload = {"name" : self.uname , "id" : self.uid , "date" : self.udate}
		print(self.uname)
		print(self.uid)
		print(self.udate)
		r = requests.get('https://smartregis00.herokuapp.com/receive', params=self.payload)
		if r:
			print("send successful")
			print(r)
		else:
			print("something went wrong check response code")
			print(r)
		

#capture = Video()
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

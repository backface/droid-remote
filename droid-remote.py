#!/usr/bin/env python

#------------------------------
# droid-remote
#------------------------------
# Copyright (C) 2015 Michael Aschauer
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os.path
import time
import pyglet
import subprocess
from pyglet.window import key

adb_path = ""
tmp_img_path = "/tmp"
tmp_img = "screen.png"
width = 360
height = 640

# these are some but not all avaible keycode 
# convert from pyglet to android
key_codes = {
	key.BACKSPACE : "KEYCODE_BACKSPACE",
	key.TAB : "KEYCODE_TAB",
	key.CLEAR : "KEYCODE_CLEAR",
	key.RETURN : "KEYCODE_ENTER",
	key.ENTER : "KEYCODE_ENTER",
	key.PAUSE : "KEYCODE_MEDIA_PLAY_PAUSE",
	key.SCROLLLOCK : "KEYCODE_SCROLL_LOCK",
	key.ESCAPE : "KEYCODE_ESCAPE",
	key.HOME : "KEYCODE_HOME",
	key.LEFT : "KEYCODE_DPAD_LEFT",
	key.UP : "KEYCODE_DPAD_UP",
	key.RIGHT : "KEYCODE_DPAD_RIGHT",
	key.DOWN : "KEYCODE_DPAD_DOWN",
	key.PAGEUP : "KEYCODE_PAGE_UP",
	key.PAGEDOWN : "KEYCODE_PAGE_DOWN",
	key.DELETE : "KEYCODE_DEL",
	key.SELECT : "KEYCODE_BUTTON_SELECT",
	key.PRINT : "KEYCODE_CAMERA",
	key.INSERT : "KEYCODE_INSERT",
	key.MENU : "KEYCODE_MENU",
	key.FIND : "KEYCODE_SEARCH",
	key.HELP : "KEYCODE_HELP",
	key.BREAK : "KEYCODE_BREAK",
	key.NUMLOCK : "KEYCODE_NUM_LOCK",
	key.NUM_SPACE : "KEYCODE_SPACE",
	key.NUM_TAB : "KEYCODE_TAB",
	key.NUM_ENTER : "KEYCODE_ENTER",
	key.NUM_F1 : "KEYCODE_F1",
	key.NUM_F2 : "KEYCODE_F2",
	key.NUM_F3 : "KEYCODE_F3",
	key.NUM_F4 : "KEYCODE_F4",
	key.NUM_HOME : "KEYCODE_HOME",
	key.NUM_LEFT : "KEYCODE_DPAD_LEFT",
	key.NUM_UP : "KEYCODE_DPAD_UP",
	key.NUM_RIGHT : "KEYCODE_DPAD_RIGHT",
	key.NUM_DOWN : "KEYCODE_DPAD_DOWN",
	key.NUM_EQUAL : "KEYCODE_NUMPAD_EQUALS",
	key.NUM_MULTIPLY : "KEYCODE_NUMPAD_MULTIPLY",
	key.NUM_ADD : "KEYCODE_NUMPAD_ADD",
	key.NUM_SEPARATOR : "KEYCODE_NUMPAD_COMMA",
	key.NUM_SUBTRACT : "KEYCODE_NUMPAD_SUBTRACT",
	key.NUM_DECIMAL : "KEYCODE_NUMPAD_DOT",
	key.NUM_DIVIDE : "KEYCODE_NUMPAD_DIVIDE",
	key.NUM_0 : "KEYCODE_NUMPAD_0",
	key.NUM_1 : "KEYCODE_NUMPAD_1",
	key.NUM_2 : "KEYCODE_NUMPAD_2",
	key.NUM_3 : "KEYCODE_NUMPAD_3",
	key.NUM_4 : "KEYCODE_NUMPAD_4",
	key.NUM_5 : "KEYCODE_NUMPAD_5",
	key.NUM_6 : "KEYCODE_NUMPAD_6",
	key.NUM_7 : "KEYCODE_NUMPAD_7",
	key.NUM_8 : "KEYCODE_NUMPAD_8",
	key.NUM_9 : "KEYCODE_NUMPAD_9",
	key.LSHIFT : "KEYCODE_SHIFT_LEFT",
	key.RSHIFT : "KEYCODE_SHIFT_RIGHT",
	key.LCTRL : "KEYCODE_POWER",
	key.RCTRL : "KEYCODE_POWER",
	key.LALT : "KEYCODE_ALT_RIGHT",
	key.RALT : "KEYCODE_ALT_RIGHT",
	key.SPACE : "KEYCODE_SPACE",
	key.APOSTROPHE : "KEYCODE_APOSTROPHE",
	key.PARENLEFT : "KEYCODE_NUMPAD_LEFT_PAREN",
	key.PARENRIGHT : "KEYCODE_NUMPAD_RIGHT_PAREN",
	key.PLUS : "KEYCODE_PLUS",
	key.COMMA : "KEYCODE_COMMA",
	key.MINUS : "KEYCODE_MINUS",
	key.PERIOD : "KEYCODE_PERIOS",
	key.SLASH : "KEYCODE_SLASH",
	key.SEMICOLON : "KEYCODE_COLON",
	key.EQUAL : "KEYCODE_EQUALS",
	key.AT : "KEYCODE_AT",
	key.BRACKETLEFT : "KEYCODE_LEFT_BRACKET",
	key.BACKSLASH : "KEYCODE_BACKSLASH",
	key.BRACKETRIGHT : "KEYCODE_RIGHT_BRACKET",
	key.GRAVE : "KEYCODE_GRAVE",
	key.A : "KEYCODE_A",
	key.B : "KEYCODE_B",
	key.C : "KEYCODE_C",
	key.D : "KEYCODE_D",
	key.E : "KEYCODE_E",
	key.F : "KEYCODE_F",
	key.G : "KEYCODE_G",
	key.H : "KEYCODE_H",
	key.I : "KEYCODE_I",
	key.J : "KEYCODE_J",
	key.K : "KEYCODE_K",
	key.L : "KEYCODE_L",
	key.M : "KEYCODE_M",
	key.N : "KEYCODE_N",
	key.O : "KEYCODE_O",
	key.P : "KEYCODE_P",
	key.Q : "KEYCODE_Q",
	key.R : "KEYCODE_R",
	key.S : "KEYCODE_S",
	key.T : "KEYCODE_T",
	key.U : "KEYCODE_U",
	key.V : "KEYCODE_V",
	key.W : "KEYCODE_W",
	key.X : "KEYCODE_X",
	key.Y : "KEYCODE_Y",
	key.Z : "KEYCODE_Z"
}

class DroidRemote(pyglet.window.Window):

	def __init__(self):
		super(DroidRemote, self).__init__( 
			width=width, 
			height=height, 
			resizable=False,
			caption="Droid Remote")
		self.image = None
		self.swipe  = False
		self.mx = 0
		self.my = 0
		self.andwidth = 0
		self.andheight= 0
		self.orientation = 0
					
	def on_mouse_press(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			x = int(float(x) / width * self.andwidth)
			y = self.andheight - int(float(y) / height * self.andheight)	
			if self.orientation % 2 == 1:
				tmp = x
				x = y
				y = tmp	
				if self.orientation == 3:
					x = self.andheight - x
					y = self.andwidth - y 
			self.mx = x
			self.my = y
			
	def on_mouse_release(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			x = int(float(x) / width * self.andwidth)
			y = self.andheight - int(float(y) / height * self.andheight)
			if self.orientation % 2 == 1:
				tmp = x
				x = y
				y = tmp	
				if self.orientation == 3:
					x = self.andheight - x
					y = self.andwidth - y 			
			if x == self.mx and y == self.my:
				cmd = "%sadb shell input touchscreen tap %d %d" % (adb_path, x, y)
				subprocess.call(cmd, shell=True)
			else:
				cmd = "%sadb shell input touchscreen swipe %d %d %d %d" % (adb_path, self.mx, self.my, x, y)
				subprocess.call(cmd, shell=True)				

	def on_mouse_drag(self,x, y, dx, dy, button, modifiers):
		pass
		 
	def on_key_press(self, symbol, modifiers):
		cmd = "%sadb shell input keyevent %s" % (adb_path, key_codes[symbol])
		subprocess.call(cmd, shell=True)	
		if not key_codes.has_key(symbol):
			print "unknown key code", symbol
	
	#def on_resize(self,x,y):
	#	print "on_resize"
	#	width = x
	#	height = y
	#	#if self.image != None:
	#	#	self.image.width=width
	#	#	self.image.height=height		
	#	super(DroidRemote, self).on_resize(x, y)
						
	def on_draw(self):
		window.clear()
		if self.image != None:
			self.image.blit(0, 0)
	
	def update_image(self,df):
		cmd = adb_path + "adb shell screencap -p"
		adb_img_data = subprocess.check_output(cmd, shell=True)
		if not os.path.exists("%s/%s" % (pyglet.resource.path[0], tmp_img)):
			f = open("%s/%s" % (pyglet.resource.path[0], tmp_img), 'w')
			f.close()
			pyglet.resource.reindex()
		f = open("%s/%s" % (pyglet.resource.path[0], tmp_img), 'w')
		f.write(adb_img_data.replace("\r\n","\n"))
		f.close()
		self.image = pyglet.resource.image(tmp_img)
		self.andwidth = self.image.width
		self.andheight = self.image.height
		self.image.width=width
		self.image.height=height
		self.clear_cache(tmp_img)		
		cmd = adb_path + "adb shell dumpsys input | grep 'SurfaceOrientation' | awk '{ print $2 }'"
		adb_orientation = subprocess.check_output(cmd, shell=True)
		adb_orientation.split("\n");
		self.orientation = int(adb_orientation[0])

	def clear_cache(self, filename):
		if filename in pyglet.resource._default_loader._cached_images:
			del pyglet.resource._default_loader._cached_images[filename]
		
if __name__ == "__main__":
	cmd = adb_path + "adb devices"
	try:
		subprocess.check_output(cmd, shell=True)
	except subprocess.CalledProcessError:
		print "Error trying to run adb - Is it in your path?"
		exit(1)		

	pyglet.resource.path = [tmp_img_path]
	pyglet.resource.reindex()
	tmp_img = "screen.png"
	window = DroidRemote()
	pyglet.clock.schedule(window.update_image)
	pyglet.app.run()

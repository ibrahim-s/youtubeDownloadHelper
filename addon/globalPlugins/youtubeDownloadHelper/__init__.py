# -*- coding: utf-8 -*-
# youtubeDownloadHelper add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 Ibrahim Hamadeh <ibra.hamadeh@hotmail.com>

import gui, wx
import re
import time
import api
import globalPluginHandler
import browseMode
import ui
from tones import beep
from scriptHandler import script
from .geturl import GetUrl
from .getbrowsers import getBrowsers

import addonHandler
addonHandler.initTranslation()

def processUrl(url):
	"""Check if the url is valid youtube url
	and if it is, prepend to youtube word the 'ss' letters.
	@return: the url string if valid, else None.
	"""
	url_re = re.compile(r"(?:https?://|www\.|https?://www\.)youtube\.com")
	match= url_re.match(url)
	if match:
		result= re.sub(r'youtube', 'ssyoutube', url, count=1)
		return result

browsers= getBrowsers()
browserNames= [name for name, exePath in browsers]

# Instane of download helper dialog, that consists of chooseBrowserComboBox and OK and CANCEL buttons.
downloadHelperInstance= None

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Translators: The category name displayed in the input gesture dialog
	scriptCategory = _("Youtube download helper")

	def __init__(self):
		super().__init__()

	@script(
		description=_(
		# Translators: Message displayed in input help mode.
		"Open Savefrom.net site, with the download link for the youtube video on it."),
		gesture="KB:NVDA+alt+d"
	)
	def script_openSavefromPage(self, gesture):
		obj = api.getNavigatorObject().treeInterceptor
		if not isinstance(obj, browseMode.BrowseModeTreeInterceptor):
			gesture.send()
			return
		youtubeUrl= obj.documentConstantIdentifier
		youtubeUrl = processUrl(youtubeUrl)
		if not youtubeUrl:
			ui.message(_("Sorry, but the url is not a valid youtube url"))
			return
		# The url is valid and processed url(added to it 'ss').
		def run():
			global downloadHelperInstance
			if not downloadHelperInstance:
				gui.mainFrame.prePopup()
				d = DownloadHelper(gui.mainFrame, url= youtubeUrl)
				d.Show()
				downloadHelperInstance= d
				gui.mainFrame.postPopup()
			else:
				downloadHelperInstance.Raise()
		wx.CallAfter(run)

class DownloadHelper(wx.Dialog):

	def __init__(self, parent, url=None):
		# Translators: The title of the Download Helper dialog.
		super(DownloadHelper, self).__init__(parent, title=_("Download Helper"))
		self.url= url

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		# Translators: The label of a combo box in the Download Helper dialog.
		chooseBrowserLabel = _("Choose browser:")
		self.chooseBrowserComboBox = sHelper.addLabeledControl(chooseBrowserLabel, wx.Choice, choices=browserNames)
		self.chooseBrowserComboBox.SetSelection(0)

		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()
		self.chooseBrowserComboBox.SetFocus()

	def onOk(self, evt):
		# Get the executable path of the browser
		indx= self.chooseBrowserComboBox.GetSelection()
		exePath= browsers[indx][1]
		# Get the save From url page that has the download link.
		t= GetUrl(self.url)
		t.start()
		while t.is_alive():
			beep(500, 100)
			time.sleep(0.7)
		t.join()
		saveFromUrl= t.response.url
		import subprocess
		subprocess.Popen(exePath+' '+saveFromUrl)
		wx.CallAfter(self.Destroy)

	def onCancel(self, event):
		self.Destroy()

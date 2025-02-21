# -*- coding: utf-8 -*-
# youtubeDownloadHelper add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 Ibrahim Hamadeh <ibra.hamadeh@hotmail.com>

import webbrowser
import re
import api
import globalPluginHandler
import browseMode
import ui
from scriptHandler import script
from .geturl import GetUrl
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
		t= GetUrl(youtubeUrl)
		t.start()
		t.join()
		webbrowser.open(t.response.url, new=2)

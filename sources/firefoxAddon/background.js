var isExtEnabled = false;

var lastSongTitle = "";
var port;
updateExtensionState(isExtEnabled);

function replaceStrangeCh(str) {
	str = str
		.replace('Æ', 'AE')
		.replace('æ', 'ae')
		.replace('Ð', 'D')
		.replace('ð', 'd')
		.replace('Ø', 'O')
		.replace('ø', 'o')
		.replace('Þ', 'TH')
		.replace('þ', 'th')
		.replace('Œ', 'OE')
		.replace('œ', 'oe')
		.replace('ß', 'ss')
		.replace('ƒ', 'f');
	return str;
}

//sends song to the native app
function getSong(message) {
	if(message.song != lastSongTitle) {
		console.log("got and now sending: " + message.song);
		lastSongTitle = message.song;
		port.postMessage(replaceStrangeCh(message.song));
	}
}

function getResponceFromApp(response) {
	console.log("answer: " + response);
}

// enables\disables extension listeners and native app.
function updateExtensionState(isEnabled) {
	if(isEnabled) {
		//connect to the "Get_Song_Title_To_File" app.
		port = browser.runtime.connectNative("Get_Song_Title_To_File");
		//Listen for messages from the app.
		port.onMessage.addListener(getResponceFromApp);
		//Listen for messages from content script
		browser.runtime.onMessage.addListener(getSong);
		browser.browserAction.setIcon({
			path : "icons/iconColor.ico"
		});
		console.log("Extension is enabled");
	} else {
		if (port) {
			port.onMessage.removeListener(getResponceFromApp);
			port.disconnect();
		}
		browser.runtime.onMessage.removeListener(getSong);
		browser.browserAction.setIcon({
			path : "icons/iconGray.ico"
		});
		console.log("Extension is disabled");
	}
}

/*
On a click on the browser action, disable\enable extension
*/
browser.browserAction.onClicked.addListener(() => {
	isExtEnabled = !isExtEnabled;
	updateExtensionState(isExtEnabled);
	browser.storage.local.set({isEnabled: isExtEnabled});
});
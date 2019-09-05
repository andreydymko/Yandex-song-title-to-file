var isExtEnabled;

var gettingPreference = browser.storage.local.get(null);
gettingPreference.then(function(res) {
	isExtEnabled = res["isEnabled"];
},	function() {
	browser.storage.local.set({isEnabled: true});
	isExtEnabled = true;
});

var lastSongTitle = "";
var port;
updateExtensionState(isExtEnabled);

//sends song to the native app
function getSong(message) {
	if(message.song != lastSongTitle) {
		console.log("got and now sending: " + message.song);
		lastSongTitle = message.song;
		port.postMessage(message.song);
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
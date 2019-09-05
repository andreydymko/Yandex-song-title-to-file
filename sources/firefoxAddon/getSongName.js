// we can use internal site api only if we inject code to site
function injectFunction(injectionFunction) {
        injectCode('(' + injectionFunction + ')()');
}

function injectCode(injection) {
    var injectedScript = document.createElement('script');
    injectedScript.textContent = injection;
    (document.head || document.documentElement).appendChild(injectedScript);
	injectedScript.parentNode.removeChild(injectedScript);
}

// function that observe song changing and send song name to getSongName.js
function funToInject() {
	var api = externalAPI;
    api.on(api.EVENT_TRACK, function() {
		var currTrack = api.getCurrentTrack();
		var strSong = currTrack.artists[0].title;
		for(let i = 1; i < currTrack.artists.length; i++) {
			strSong += ", " + currTrack.artists[i].title;
		}
		strSong += " - " + currTrack.title;
		window.postMessage({
			direction: "IQvw1OikU3lXXP965bEdtLWXdo9mBjLO",
			message: strSong
		}, "*");
	});
}

injectFunction(funToInject);

//sending song name to background.js
window.addEventListener("message", function(event) {
	if (event.source == window &&
		event.data &&
		event.data.direction == "IQvw1OikU3lXXP965bEdtLWXdo9mBjLO") {
    browser.runtime.sendMessage({song: event.data.message});
	}
});
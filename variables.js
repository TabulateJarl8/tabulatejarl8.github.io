function setCookie(name, value, daysToLive) {
	var cookie = name + "=" + encodeURIComponent(value);
	if(typeof daysToLive === "number") {
		cookie += "; max-age=" + (daysToLive*24*60*60);
		cookie += "; path=/";
		document.cookie = cookie;
	}
}

function getCookie(name) {
	var cookieArr = document.cookie.split(";");
	for(var i = 0; i < cookieArr.length; i++) {
		var cookiePair = cookieArr[i].split("=");
		if(name == cookiePair[0].trim()) {
			return decodeURIComponent(cookiePair[1]);
		}
	}
	return null;
}

function checkCookie(name) {
	var value = getCookie(name);
	if(value != null) {
		return true;
	} else {
		return false;
		}
	}

function deleteCookie(name){
	document.cookie = name += "=; max-age=0";
}

function getUrlVars() {
	var vars = {};
	var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
		vars[key] = value;
	});
	return vars;
}

function getUrlParam(parameter, defaultvalue){
	var urlparameter = defaultvalue;
	if(window.location.href.indexOf(parameter) > -1){
		urlparameter = getUrlVars()[parameter];
	}
	return urlparameter;
}

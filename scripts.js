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
	if(value == null) {
		return false;
	} else {
	    return true;
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

function signOut(redirect) {
  if (checkCookie("username")) {
    deleteCookie("username");
    deleteCookie("token");
    if(redirect == true){
      window.location.href = "/login";
    }
  } else if (sessionStorage.getItem("username") != null) {
    sessionStorage.removeItem("username");
    sessionStorage.removeItem("token");
  if(redirect == true){
    window.location.href = "/login";
  }
    
  }
}

function returnVerify(token, user) {
  verify(token, user, function(d) {
    return d;
  });
}

function verify(token, user, callback) {
  $.ajax(
  {
    url: 'https://tabulatephp.azurewebsites.net/checklogin.php',
    type: 'POST',
    dataType: 'text',
    data: {token: token, name: user },
    success: function(response)
    {
      callback(response);
    }
  });
}

function checkLogin(){
  if(checkCookie("token")){
    if(checkCookie("username")){
      var check = returnVerify(getCookie("token"), getCookie("username"));
      if(check != "false"){
        console.log(check);
      setCookie("token", check, 30);
      return true;
      }else{
        return false;
      }
    }else{
      return false;
    }
  }else if(sessionStorage.getItem("token") != null){
    if(sessionStorage.getItem("username") != null){
      var check = returnVerify(sessionStorage.getItem("token"), sessionStorage.getItem("username"));
      if(check != "false"){
        sessionStorage.removeItem("token");
        sessionStorage.setItem("token", check);
        return true;
      }else{
        return false;
      }
    }else{
      return false;
    }
  }else{
    return false;
  }
}


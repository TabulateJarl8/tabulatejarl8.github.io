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

function checkLogin(){
  //if(checkCookie("token")){
    
  //}else if(sessionStorage.getItem("token") != null){
    
  //}else{
    //return false;
  //}
  document.write(verify(getCookie("token"), getCookie("username")));
}

function verify(token, user){
  //var xmlhttp = new XMLHttpRequest();
  //xmlhttp.onreadystatechange = function(){
    //if(this.readyState == 4 && this.status == 200){
      //return this.responseText;
    //}
  //};
  //xmlhttp.open("GET", "https://tabulatephp.azurewebsites.net/checklogin.php?token=" + token + "&name=" + user, true);
  //xmlhttp.send();
  $.ajax(
  {
    url: 'https://tabulatephp.azurewebsites.net/checklogin.php',
    type: 'POST',
    dataType: 'text',
    data: { token: token, name: user},
    success: function(response)
    {
        document.write(response);
    }
  });
}
var url = window.location.href.split("/");
var secondurl = window.location.href.split("/");
if (secondurl[secondurl.length - 1] === "") {
  secondurl.pop();
}
secondurl.shift();
secondurl.shift();
secondurl[0] = "";
if (url[url.length - 1] === "") {
  url.pop();
}
url.shift();
url.shift();
url.shift();
url.unshift("home");
for (var i = 0; i < url.length; i++) {
  url[i] = url[i].replace("_", " ");
  if (url[i].endsWith(".html")) {
    url[i] = url[i].replace(".html", "");
  }
  url[i] = url[i].charAt(0).toUpperCase() + url[i].substr(1);
}
for (i = 0; i < url.length - 1; i++) {
  var path = window.location.href.slice(0, -1);
  path = path.split("/");
  path.shift();
  path.shift();
  path.shift();
  path = "/" + path[0];
  for (k = 0; k < secondurl.length - 1; k++) {
    path = path.substring(0, path.indexOf('/'));
  }
  if (path === "") {
    path = "/";
  }
  var crumburl = path;
  var element = "<li class='breadcrumb-item'><a href='" + crumburl + "'>" + url[i] + "</a></li>";
  secondurl.pop();
  $(".breadcrumb").append(element);
}
element = "<li class='breadcrumb-item active'>" + url.pop() + "</li>";
$(".breadcrumb").append(element);
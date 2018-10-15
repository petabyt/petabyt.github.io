var x = 0;
var y = 0;

function getMouse(event) {
	if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
		x = 60 - (event.clientX + (window.innerWidth))/30;
		y = 30 - (event.clientY + (window.innerHeight))/30;

		document.getElementById('main').style.backgroundPosition = x + "px " + y + "px" ;
		//document.getElementsByTagName('body')[0].style.textShadow = "" + ((event.clientX + (window.innerWidth))/30) + "px " + (60 + (event.clientY + (window.innerHeight))/30) + "px 1px black";
	}
}

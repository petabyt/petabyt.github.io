var thingies = ["Don't Press The Green Button","I told you not to click it.","Do you ever listen to anybody?","Oh wait, I'm not a person. But anyway, please don't click the button anymore.","Just stop it.","Stop it now.","But please just stop clicking the darn button!","Go do something more useful with your life, and stop clicking a green button you found on the internet.","You are addicted to clicking this button. You just HAVE to see what's next.","Click the button one more time and there will be no more green button.","","Stop clicking.","Why won't you stop?","Since you aren't stopping, let me tell you a story.","Once apon a time, a person was browsing the internet.", "They visited a random website, and that person was told NOT to click a green button.","They clicked it anyway, and this is what they saw:"];
var current = 0;
setInterval(function() {
	if (current == 10) {
		document.getElementById('button').style.backgroundColor = "white";
	} else if (current == 12) {
		document.getElementById('button').style.backgroundColor = "blue";
	} else if (current == 17) {
		current = 0;
		document.getElementById('button').style.backgroundColor = "green";
	} else {
		document.getElementById('text').innerHTML = thingies[current];
	}
},1);
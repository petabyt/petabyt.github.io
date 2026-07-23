---
title: "JSCraft"
date: 2017-10-19
draft: false
---

I started to experiment with the Html5 canvas today. After some fliddling, I came up with a mini 2D terrarian generator. Here it is:

<!--more-->

<canvas id="canvas" width="600" height="300"></canvas>
<script type="text/javascript">
var currentline = 0;
var current_y;
var current_x;
var currentgenline = 0;
var world = [];
var grass_y = [];
var i;
var b;
var d;
var current_grass_y = 0;
var x = 0;
var y = 280;
var c = document.getElementById("canvas");
var ctx = c.getContext("2d");
gen_world();
function gen_world() {
	ctx.fillText("JScraft Alpha",10,20);
ctx.fillStyle = "grey";
// Generate Stone
for (b = 0; b < 30; b++) {
for (i = 0; i < Math.floor(Math.random() * 3) + 1; i++) {
ctx.fillRect(x, y, 30, 30);
world.push(x + "," + y)
y = y - 30;
}

grass_y.push(y);
x = x + 30;
y = 280;

}
world.push("grass_break")
x = 0;
ctx.fillStyle = "green";
// Generate Grass
for (d = 0; d < 30; d++) {
ctx.fillRect(x, grass_y[current_grass_y], 30, 30);
world.push(x + "," + grass_y[current_grass_y]);
current_grass_y = current_grass_y + 1;
x = x + 30;
}

}
function generate_again() {
	y = 280;
	x = 0;
i = 0;
b = 0;
d = 0;
	world = [];
	ctx.fillText("JScraft Alpha",10,20);
ctx.fillStyle = "grey";
// Generate Stone
for (b = 0; b < 30; b++) {
for (i = 0; i < grass_y[currentgenline]; i++) {
	current_x = world[currentline].split(',')[0]; 
	current_y = world[currentline].split(',')[1]; 
ctx.fillRect(current_x, current_y, 30, 30);
world.push(x + "," + y)
y = y - 30;
currentline++;
}
x = x + 30;
y = 280;

}
world.push("grass_break")
x = 0;
ctx.fillStyle = "green";
// Generate Grass
for (d = 0; d < 30; d++) {
ctx.fillRect(x, grass_y[current_grass_y], 30, 30);
world.push(x + "," + grass_y[current_grass_y]);
current_grass_y = current_grass_y + 1;
x = x + 30;
}

}
</script>
<style type="text/css">
#canvas {
border:transparent;
background-color:lightblue;
}
</style>

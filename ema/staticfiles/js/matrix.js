// var ema, matrix, canX, canY, mouseIsDown = 0;
var circleObjects = [];
var redrawCircle = false;
// später aus der Datenbank
var circles = [[850,600,'red'],[100,100,'red'],[200,200,'green'],[400,500,'black'],[700,100,'blue'],[90,300,'pink'],[600,200,'brown']];
// ema = document.getElementById("ema");
// matrix = ema.getContext("2d");

// constructor for a task / circle
function Circle(x,y,topicC) {
	this.x = x || width-50;
	this.y = y || height-50;
	this.topicC = topicC || "black";
	this.touched = false;
	this.drawn = false;
}

// draw that particular circle
Circle.prototype.drawCircle = function (field) {
	field.beginPath();
	field.arc(this.x, this.y, 5, 0, 2*Math.PI);
	field.lineWidth = 2;
	field.strokeStyle = this.topicC;
	field.stroke();
	this.drawn = true;
}

// when the mouse cursor howers over a circle, the middle of the circle is filled
// TODO opens up div with description of the task
Circle.prototype.howerCircle = function (field) {
	field.beginPath();
	field.arc (this.x, this.y, 1, 0, 2*Math.PI);
	field.Width = 0.1;
	field.strokeStyle = this.topicC;
	field.stroke();
	this.touched = true;
}

// when the mouse cursor is no longer on the circle, the circle should be unfilled again
// TODO and the div should disappear
Circle.prototype.emptyCircle = function (field) {
	field.clearRect(this.x-7,this.y-7,14,14);
	this.touched = false;
	this.drawCircle(field);
}

// uses the property method drawCircle to draw all circles in the beginning
function drawCircles(field, array) {
	for (i = 0; i < array.length; i++) {
		array[i].drawCircle(field);
	}
}

// start
function init() {
	ema.addEventListener("mousedown", mouseDown, false);
	ema.addEventListener("mousemove", mouseXY, false);
	ema.addEventListener("touchstart", touchDown, false);
	ema.addEventListener("touchmove", touchXY, true);
	ema.addEventListener("touchend", touchUp, false);

	document.body.addEventListener("mouseup", mouseUp, false);
	document.body.addEventListener("touchcancel", touchUp, false);

	var width = ema.width;
	var height = ema.height;

	for (i=0; i<circles.length; i++) {
		circleObjects.push(new Circle(circles[i][0], circles[i][1], circles[i][2]));
	}

	// Matrix Achsen und Tasks zeichnen
	drawAxes(matrix, width, height);
	drawCircles(matrix, circleObjects);

}

function mouseUp() {
	mouseIsDown = 0;
	mouseXY();
}

function touchUp() {
	mouseIsDown = 0;
	// no touch to track, so just show state
	showPos();
}

function mouseDown() {
	mouseIsDown = 1;
	mouseXY();
}

function touchDown() {
	mouseIsDown = 1;
	touchXY();
}

function mouseXY(e) {
	if (!e)
		var e = event;
	canX = e.pageX - ema.offsetLeft;
	canY = e.pageY - ema.offsetTop;
	showPos();
}

function touchXY(e) {
	if (!e)
		var e = event;
	e.preventDefault();
	canX = e.targetTouches[0].pageX - ema.offsetLeft;
	canY = e.targetTouches[0].pageY - ema.offsetTop;
	showPos();
}

function showPos() {
	// large, centered, bright green text
	matrix.font = "12pt Helvetica";
	matrix.textAlign = "left";
	matrix.textBaseline = "top";
	matrix.fillStyle = "black";
	var str = canX + ", " + canY;
	if (mouseIsDown)
		str += " down";
	if (!mouseIsDown)
		str += " up";
	// var touched;
	for (i=0; i<circleObjects.length; i++) {
		if (canX >= circleObjects[i].x-5 && canX <= circleObjects[i].x+5 && canY >= circleObjects[i].y-5 && canY <= circleObjects[i].y+5) {
			if (!circleObjects[i]["touched"]) {
				circleObjects[i].howerCircle(matrix);
			}
		} else {
			if (circleObjects[i]["touched"]) {
				circleObjects[i].emptyCircle(matrix);
			}
		}
	}
	// control to display correct coordinates
	matrix.clearRect(850,625,50,40);
	matrix.fillText(str, 850, 625, 50);
}

function drawAxes(field, width, height) {

}

var s,
Matrix = {
	settings: {
		canvas: $('canvas'),
		drawing: document.getElementById('ema').getContext("2d"),
		width: $('canvas').width(),
		height: $('canvas').height()
	},
	init: function() {
		s = this.settings;
	},
	drawAxes: function(field, width, height) {
		// untere Ecke y-Wert
		var uEy = height-25;
		// rechte Ecke x-Wert
		var rEx = width-20;
		// Mitte y-Achse
		var my = (height-20-25)/2 + 20;
		// Mitte x-Achse
		var mx = (width-25-20)/2 + 25;

		// Spitze senkrechter Pfeil
		field.moveTo(25,20);
		// zur untere Ecke
		field.lineTo(25,uEy);
		field.stroke();
		// zur rechten Spitze
		field.lineTo(rEx,uEy);
		field.stroke();

		// Pfeil oben linke Seite
		field.moveTo(15,30);

		field.lineTo(25,20);
		field.stroke();

		// Pfeil oben rechte Seite
		field.lineTo(35,30);
		field.stroke();

		// Pfeil rechts oberer Teil
		field.moveTo(rEx-10,uEy-10);
		// zur rechten Spitze
		field.lineTo(rEx,uEy);
		field.stroke();
		// zum Pfeil rechts unterer Teil
		field.lineTo(rEx-10,uEy+10);
		field.stroke();

		// Mittellinie y-Achse
		field.moveTo(25,my);
		field.lineTo(rEx,my);
		field.stroke;

		// Mittellinie x-Achse
		field.moveTo(mx,20);
		field.lineTo(mx,uEy);
		field.stroke();

		// Beschriftung x-Achse
		field.font = "20px Arial";
		// field.textAlign = "center";
		field.fillText("U R G E N T", width/2-50, height);

		field.save();
		field.translate(width/2,height/2);
		// Beschriftung y-Achse
		field.font = "20px Arial";
		field.rotate(-Math.PI/2);
		field.translate(height/2,-width/2);
		field.fillText("I M P O R T A N T", -height/2-50, 15);

		field.restore();
	},
	drawTasks: function(taskData) {

	}
};

// init();

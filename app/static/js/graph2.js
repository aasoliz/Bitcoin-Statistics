// Get and format data
var scripts = document.getElementsByTagName("script");

// Script that is referencing this file
var lastScript = scripts[scripts.length-1];

// Get passed in attribute
var data = lastScript.getAttribute("data") ;

// Make pretty
var rm = data.replace(/00000000/g, "")
    .replace(/: \'/g, ": ")
    .replace(/\', /g, ", ")
    .replace(/\'}/g, "}")
    .replace(/\'/g, "\"");

// Parse JSON from String
var js = JSON.parse(rm);

var MARGIN = {top: 30, right: 30, bottom: 70, left: 30},
    WIDTH = 1000 - MARGIN.left - MARGIN.right,
    HEIGHT = 500 - MARGIN.top - MARGIN.bottom;

// X-Axis Scale
var xScale = d3.scale.linear()
    .domain([0, 23])
    .range([0, WIDTH]);

// Y-Axis Scale
var yScale = d3.scale.linear()
    .domain([0, 500])
    .range([0, HEIGHT]);

// Create X-Axis
var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom")
    .ticks(24);

var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left");

var svgContainer = d3.select("div")
    .append("svg")
    .attr("width", WIDTH + MARGIN.left + MARGIN.right)
    .attr("height", HEIGHT + MARGIN.top + MARGIN.bottom)
    .append("g")
    .attr("transform", "translate(" + MARGIN.left + "," + MARGIN.top + ")");

// Append X-Axis to container 
svgContainer.append("g")
    .attr("transform", "translate(0," + HEIGHT + ")")
    .call(xAxis);

// Append Y-Axis to container 
svgContainer.append("g")
    .call(yAxis);

// Create a line 
var line = d3.svg.line()
    .x(function(d) {
        return xScale(d.hour);
    })
    .y(function(d) {
        return yScale(d.buy);
    })
    .interpolate('linear');

// Append path for line
svgContainer.append("svg:path")
    .attr("d", line(js))
    .attr("stroke", "blue")
    .attr("stroke-width", 2)
    .attr("fill", "none");
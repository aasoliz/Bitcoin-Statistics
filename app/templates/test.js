// Get and format data
var scripts = document.getElementsByTagName("script");

// Script that is referencing this file
var lastScript = scripts[scripts.length-1];

// Get passed in attribute
var data = lastScript.getAttribute("data");

// Make pretty
var rm = data.replace(/00000000/g, "")
    .replace(/: \'/g, ": ")
    .replace(/\', /g, ", ")
    .replace(/\'}/g, "}")
    .replace(/\'/g, "\"");

// Parse JSON from String
var dataset = JSON.parse(rm);
console.log(dataset);

var color_hash = {  0 : ["apple", "green"],
                    1 : ["mango", "orange"]
                  }

var WIDTH = 1000;
var HEIGHT = 500;
var MARGIN = 50;               

// Define axis ranges & scales        
var xExtents = d3.extent(d3.merge(dataset), function (d) { return d.hour; });
var yExtents = d3.extent(d3.merge(dataset), function (d) { return d.price; });
     
var xScale = d3.scale.linear()
       .domain([xExtents[0], xExtents[1]])
       .range([MARGIN, WIDTH - MARGIN * 2]);

var yScale = d3.scale.linear()
       .domain([0, yExtents[1]])
       .range([HEIGHT - MARGIN, MARGIN]);


// Create SVG element
var svg = d3.select("body")
    .append("svg")
    .attr("width", WIDTH)
    .attr("height", HEIGHT);


// Define lines
var line = d3.svg.line()
       .x(function(d) { return x(d.x); })
       .y(function(d) { return y(d.y1, d.y2, d.y3); });

var pathContainers = svg.selectAll('g.line')
.data(dataset);

pathContainers.enter().append('g')
.attr('class', 'line')
.attr("style", function(d) {
    return "stroke: " + color_hash[dataset.indexOf(d)][1]; 
});

pathContainers.selectAll('path')
.data(function (d) { return [d]; }) // continues the data from the pathContainer
.enter().append('path')
  .attr('d', d3.svg.line()
    .x(function (d) { return xScale(d.hour); })
    .y(function (d) { return yScale(d.price); })
  );

// add circles
pathContainers.selectAll('circle')
.data(function (d) { return d; })
.enter().append('circle')
.attr('cx', function (d) { return xScale(d.hour); })
.attr('cy', function (d) { return yScale(d.price); })
.attr('r', 3); 
  
//Define X axis
var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .ticks(24);

//Define Y axis
var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");
        
//Add X axis
svg.append("g")
.attr("class", "axis")
.attr("transform", "translate(0," + (HEIGHT - MARGIN) + ")")
.call(xAxis);

//Add Y axis
svg.append("g")
.attr("class", "axis")
.attr("transform", "translate(" + MARGIN + ",0)")
.call(yAxis);

// Add title      
svg.append("svg:text")
       .attr("class", "title")
   .attr("x", 20)
   .attr("y", 20)
   .text("hour price Per Hour");


// add legend   
var legend = svg.append("g")
  .attr("class", "legend")
    //.attr("x", WIDTH - 65)
    //.attr("y", 50)
  .attr("height", 100)
  .attr("width", 100)
.attr('transform', 'translate(-20,50)')    
  

legend.selectAll('rect')
  .data(dataset)
  .enter()
  .append("rect")
  .attr("x", WIDTH - 65)
  .attr("y", function(d, i){ return i *  20;})
  .attr("width", 10)
  .attr("height", 10)
  .style("fill", function(d) { 
    var color = color_hash[dataset.indexOf(d)][1];
    return color;
  })
  
legend.selectAll('text')
  .data(dataset)
  .enter()
  .append("text")
  .attr("x", WIDTH - 52)
  .attr("y", function(d, i){ return i *  20 + 9;})
  .text(function(d) {
    var text = color_hash[dataset.indexOf(d)][0];
    return text;
  });

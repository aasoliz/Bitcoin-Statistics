// Get and format data
var scripts = document.getElementsByTagName("script");

// Get passed in attribute from script that is referencing this file
var data = scripts[scripts.length-1].getAttribute("data");

// Remove unnecessary (', ")
var rm = data.replace(/00000000/g, "")
    .replace(/: \'/g, ": ")
    .replace(/\', /g, ", ")
    .replace(/\'}/g, "}")
    .replace(/\'/g, "\"");

// Parse JSON from String
var prices = JSON.parse(rm);

var color = {
    0 : ["Buy Price", "#D1FF63"],
    1 : ["Sell Price", "#BB91FF"]
}

var MARGIN = {top: 70, right: 20, bottom: 93, left: 50},
    WIDTH = (window.screen.availWidth * 0.75) - MARGIN.left - MARGIN.right,
    HEIGHT = (window.screen.availHeight * 0.7) - MARGIN.top - MARGIN.bottom;

// Limit of X-Axis
var xExtent = d3.extent(d3.merge(prices), function (d) { 
    return d.hour; 
});

// Limit of Y-Axis
var yExtent = d3.extent(d3.merge(prices), function (d) { 
    return d.price; 
});

// X-Axis Scale
var xScale = d3.scale.linear()
    .domain([xExtent[0], xExtent[1]])
    .range([0, WIDTH]);

// Y-Axis Scale
var yScale = d3.scale.linear()
    .domain([yExtent[0], yExtent[1]])
    .range([HEIGHT, 0]);

// Create X-Axis
var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom")
    .ticks(24);

// Create Y-Axis
var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left");

d3.select("div")
    .attr("class", "graph")
    .attr("width", WIDTH + MARGIN.left + MARGIN.right)
    .attr("height", HEIGHT + MARGIN.top + MARGIN.bottom);

// Container
var svgContainer = d3.select("div")
    .append("svg")
    .attr("width", WIDTH + MARGIN.left + MARGIN.right)
    .attr("height", HEIGHT + MARGIN.top + MARGIN.bottom)
    .append("g")
    .attr("transform", "translate(" + MARGIN.left + "," + MARGIN.top + ")");

// Append X-Axis to container 
svgContainer.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + HEIGHT + ")")
    .call(xAxis);

// Append Y-Axis to container 
svgContainer.append("g")
    .attr("class", "axis")
    .call(yAxis);

// Create a line
var line = d3.svg.line()
    .x(function (d) { return x(d.x); })
    .y(function (d) { return y(d.y1, d.y2); });

var pathContainer = svgContainer.selectAll("g.line")
    .data(prices);

// Set color of the lines
pathContainer.enter()
    .append("g")
    .attr("class", "line")
    .attr("style", function (d) {
        return "stroke: " + color[prices.indexOf(d)][1];
    });

// Add the data points
pathContainer.selectAll("path")
    .data(function (d) { return [d]; })
    .enter()
    .append("path")
    .attr("d", d3.svg.line()
        .x(function (d) { return xScale(d.hour); })
        .y(function (d) { return yScale(d.price); })
    );

// Add circles to points on graph
pathContainer.selectAll("circle")
    .data(function (d) { return d; })
    .enter()
    .append("circle")
    .attr("cx", function (d) { return xScale(d.hour); })
    .attr("cy", function (d) { return yScale(d.price); })
    .attr("r", 3);

// Create Legend
var legend = svgContainer.append("g")
    .attr("class", "wrap")
    .attr("transform", "translate(-20,50)");

legend.selectAll("rect")
    .data(prices)
    .enter()
    .append("rect")
    .attr("x", WIDTH - 75)
    .attr("y", function (d, i) {
        return i * 20 - 93;
    })
    .attr("width", 13)
    .attr("height", 13)
    .style("fill", function (d) {
        return color[prices.indexOf(d)][1];
    })
    .attr("class", "legend");

legend.selectAll("text")
    .data(prices)
    .enter()
    .append("text")
    .attr("x", WIDTH - 55)
    .attr("y", function (d, i) {
        return i * 20 - 80;
    })
    .text(function (d) {
        return color[prices.indexOf(d)][0];
    });

// Expand Circle when mouse touches
d3.selectAll("circle")
    .on("mouseover", function() {
        return d3.select(this)
            .transition()
            .duration(750)
            .attr("r", 1700)
            .attr("opacity", 0.5);
    });

// Return circle when mouse leaves
d3.selectAll("circle")
    .on("mouseout", function() {
        return d3.select(this)
            .transition()
            .delay(400)
            .duration(650)
            .attr("r", 3)
            .attr("opacity", 1);
    });

// Focus on the line specified in the legend
d3.selectAll(".legend")
    .on("mouseover", function (color) {
        return d3.selectAll(".line")
            .filter(function (d) {
                return color != d;
            })
            .transition()
            .attr("opacity", 0.2);
    });

//  Unfocus
d3.selectAll(".legend")
    .on("mouseout", function (color) {
        return d3.selectAll(".line")
            .filter(function (d) {
                return color != d;
            })
            .transition()
            .attr("opacity", 1);
    });

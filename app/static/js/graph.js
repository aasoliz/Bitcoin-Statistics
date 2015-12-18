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
    0 : ["Buy", "#D1FF63"],
    1 : ["Sell", "#FFC20A"]
}

var MARGIN = {top: 55, right: 20, bottom: 70, left: 50},
    WIDTH = 1000 - MARGIN.left - MARGIN.right,
    HEIGHT = 550 - MARGIN.top - MARGIN.bottom;


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

pathContainer.enter()
    .append("g")
    .attr("class", "line")
    .attr("style", function (d) {
        return "stroke: " + color[prices.indexOf(d)][1];
    });

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
    .attr("height", 100)
    .attr("width", 100)
    .attr("transform", "translate(-20,50)");

legend.selectAll("rect")
    .data(prices)
    .enter()
    .append("rect")
    .attr("x", WIDTH - 65)
    .attr("y", function (d, i) {
        return i * 20;
    })
    .attr("width", 10)
    .attr("height", 10)
    .style("fill", function (d) {
        return color[prices.indexOf(d)][1];
    });

legend.selectAll("text")
    .data(prices)
    .enter()
    .append("text")
    .attr("x", WIDTH - 52)
    .attr("y", function (d, i) {
        return i * 20 + 9;
    })
    .text(function (d) {
        return color[prices.indexOf(d)][0];
    });

// Extra rectangle for banner
legend.insert("rect", "rect")
    .attr("class", "st")
    .attr("width", 300)
    .attr("height", 65)
    .attr("x", WIDTH - 150)
    .attr("y", function (d, i) {
        return i - 75;
    });

d3.selectAll("circle")
    .on("mouseover", function() {
        return d3.select(this)
            .transition()
            .duration(750)
            .attr("r", 1000)
            .attr("opacity", 0.5);
    });

d3.selectAll("circle")
    .on("mouseout", function() {
        return d3.select(this)
            .transition()
            .delay(400)
            .duration(650)
            .attr("r", 3)
            .attr("opacity", 1);
    });

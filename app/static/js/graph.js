var main = function() {
  d3.select("div").transition
    .style("background-color", "black");

  var margin = {top: 30, right: 20, bottom: 70, left: 50},
    width = 600 - margin.left - margin.right,
    height = 270 - margin.top - margin.bottom;


    //Create the Scale we will use for the Axis
    var axisScale = d3.scale.linear()
     .domain([0, 500])
     .range([0, width]);


    var yaxisScale = d3.scale.linear()
    .domain([0, 5])
    .range([ height,0]);

    var xAxis = d3.svg.axis()
    .scale(axisScale)
    .orient("bottom");

    var yAxis = d3.svg.axis()
    .scale(yaxisScale)
    .orient("left");

    var svgContainer = d3.select("div").
    append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svgContainer.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

    svgContainer.append("g")
    .attr("class", "y axis")
    .call(yAxis);

    // create a line
    var line = d3.svg.line()
    .x(function(d,i) {
      console.log(d.x);
      return axisScale(d.x);
    })
    .y(function(d,i) {
      console.log(d.y);
      return yaxisScale(d.y);
    })
    var data = {{ data|safe }}
    svgContainer.append("svg:path").attr("class", "line").attr("d", line(data));
};

$(document).ready(main);
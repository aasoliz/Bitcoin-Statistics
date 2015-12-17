d3.select("body").append("p").text("Hello, World!");
// d3.select("div").transition()
//   .style("background-color", "black");

var margin = {top: 30, right: 20, bottom: 70, left: 50},
    width = 1000 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;


    //Create the Scale we will use for the Axis
    var axisScale = d3.scale.linear()
      .domain([0, 22])
      .range([0, width]);


    var yaxisScale = d3.scale.linear()
    .domain([0, 500])
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
    //.attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

    svgContainer.append("g")
    //.attr("class", "y axis")
    .call(yAxis);

    // create a line
    var line = d3.svg.line()
    .x(function(d,i) {
      console.log(d.hour);
      return axisScale(d.hour);
    })
    .y(function(d,i) {
      console.log(d.buy);
      return yaxisScale(d.buy);
    })
    .interpolate('linear');

    var scripts = document.getElementsByTagName('script');
    var lastScript = scripts[scripts.length-1];
    console.log(scripts);
    var scriptName = lastScript;

    var data = scriptName.getAttribute('data') ;
    console.log(data);
    var rm = data.replace(/00000000/g, "").replace(/: \'/g, ": ")
        .replace(/\', /g, ", ").replace(/\'}/g, "}").replace(/\'/g, "\"");
    console.log(rm);


    var js = JSON.parse(rm);
    console.log(js);
    svgContainer.append("svg:path").attr("d", line(js)).attr('stroke', 'blue')
        .attr('stroke-width', 2).attr('fill', 'none');
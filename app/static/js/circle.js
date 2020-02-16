
var width = 1000;
var height = 700;
var MOUSEOVER = false;

var svgContainer = d3.select("body").append("svg")
						.attr("height", height)
						.attr("width", width);

var circle = svgContainer.append("circle")
						.attr("cx", 500)
						.attr("cy", 350)
                        .attr("r", 200)
                        .attr("opacity", 0.5);

 var rectangle = circle.append("rect")
							.attr("x", 10)
							.attr("y", 10)
							.attr("width", 50)
                            .attr("height", 100)
                            .attr("color", 'red');
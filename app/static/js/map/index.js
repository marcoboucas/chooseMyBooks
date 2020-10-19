// Generate a map from a list of books
const width = window.window.innerWidth;
const height = window.window.innerHeight;
const border = 20;

let [labelOffsetX, labelOffsetY] = [5, -10];

const radius = 6;

console.log("D3.js map");
const svg = d3
  .select("#map")
  .append("svg")
  .style("background-color", "antiquewhite")
  .attr("width", width)
  .attr("height", height);

d3.json("api/getBooks").then(function (data) {
  data = data.map((x) => x.fields);
  let [xmin, xmax] = [Infinity, -Infinity];
  let [ymin, ymax] = [Infinity, -Infinity];

  data.forEach((ele) => {
    if (ele.x > xmax) xmax = ele.x;
    if (ele.x < xmin) xmin = ele.x;
    if (ele.y > ymax) ymax = ele.y;
    if (ele.y < ymin) ymin = ele.y;
  });

  xFactor = (width - 2 * border) / (xmax - xmin);
  yFactor = (height - 2 * border) / (ymax - ymin);

  data.forEach((ele) => {
    ele.x = (ele.x - xmin) * xFactor + border;
    ele.y = (ele.y - ymin) * yFactor + border;
  });

  let nodes = svg.append("g").selectAll("g").data(data).enter().append("g");

  let points = nodes
    .append("circle")
    .attr("cx", (d) => d.x)
    .attr("cy", (d) => d.y)
    .attr("r", radius)
    .attr("class", "point");

  let labels = nodes
    .append("text")
    .attr("class", "label")
    .attr("x", (d) => labelOffsetX + d.x)
    .attr("y", (d) => labelOffsetY + d.y)
    .text((d) => d.title)
    .style("display", "none");

  points.on("mouseover", function (event) {
    let ele = d3.select(this).attr("r", 1.5 * radius);
    console.log(ele._groups[0][0].__data__.title);
    //display the label
    d3.select(this.nextSibling).style("display", "block");
    console.log(this.nextSibling);
  });

  points.on("mouseout", function (event) {
    let ele = d3.select(this).attr("r", radius);
    //ele.selectAll("div").remove();
    d3.select(this.nextSibling).style("display", "none");
  });
});

function drawGraph(data) {

    console.log(data)
    const width = 800
    const height = 493

    const margin = {
        left: 50,
        right: 10,
        top: 10,
        bottom: 50
    }

    // var data = [["a", 1,1], ["b", 2,2], ["c", 3,3]];

    var plot_width = width - margin.left - margin.right;
    var plot_height = height - margin.top - margin.bottom;



    var scaleX = d3.scaleLinear()
        .domain([0, 4])
        .range([0, plot_width])

    var scaleY = d3.scaleLinear()
        .domain([0, 4])
        .range([plot_height, 0])

    var canvas = d3.select('#canvas')
        .append('svg')
        .style('background', '#b5fcb5')
        .attr('height', height)
        .attr('width', width)

    var plot = canvas.append('g')
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


    var dots = plot.selectAll('circle').data(data).enter()
        .append('circle')
        .attr('class', 'point-circle')
        .attr("cx", d => { return scaleX(d[1]) })
        .attr("cy", d => { return scaleY(d[2]) })
        .attr("r", 10)
        .style("stroke-width", 2)
        .style("fill", "blue")
        .style("stroke", "red")

    var tooltip = d3.select("body")
        .append('g')
        .attr('class', 'tooltip')
        .style('opacity', 0)


    dots.on("mouseover", function (d) {
        d3.select(event.currentTarget)
            .attr("r", 15);

        tooltip
            .style('opacity', 0.9)
            .style("left", (d3.event.pageX + 10) + "px")
            .style("top", (d3.event.pageY - 10) + "px")
            .html(tooltipFormatter(d))
    })
        .on("mouseout", function (d) {
            d3.select(event.currentTarget)
                .attr("r", 10);

            tooltip
                .style('opacity', 0)
        })


    var xAx = d3.axisBottom(scaleX);
    var yAx = d3.axisLeft(scaleY);

    plot.append('g')
        .attr("transform",
            "translate(0, " + scaleY(0) + ")")
        .attr('class', 'axes')
        .call(xAx);

    plot.append('g')
        .attr("transform",
            "translate(0, 0)")
        .attr('class', 'axes')
        .call(yAx);

    canvas.append('text')
        .attr("x", plot_width - 20)
        .attr("y", scaleY(0) + 40)
        .attr("class", "axis-label")
        .text('Points')

    canvas.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0)
        .attr("x", 0 - (plot_height / 2))
        .attr("dy", "1em") // nudge the text; see p 65 of Tips and Tricks
        .attr("class", "axis-label")
        .style("text-anchor", "middle")
        .text("Goal Difference");



    function tooltipFormatter(d) {
        var team = "<strong>" + d[0] + "</strong></br>"
        var gd = "GD: " + d[1]
        var points = "Points: " + d[2] + "</br>"
        return team + points + gd

    }

}

function draw() {
    d3.csv("./static/js/simpledata.csv")
    .then(function (data) {
        data.forEach(d=>{
            d.Alice = +d.Alice;
            d.Bob = +d.Bob;
            d.Carol = +d.Carol;
        })
    console.dir(data) // sanity check
    drawGraph(data);
    })
    .catch((err) => {
    console.log("data loading error")
    console.log(err)
    })
    }
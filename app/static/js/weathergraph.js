function drawGraph(data) {

    const width = 1050
    const height = 550

    const margin = {
        left: 50,
        right: 10,
        top: 10,
        bottom: 50
    }

    var rainfall_format = d3.format(",.0f")
    var plot_width = width - margin.left - margin.right;
    var plot_height = height - margin.top - margin.bottom;

    years = []
    for(var i = 1970; i < 2020; i++){
        temp = "'" + i.toString().slice(2,4)
        years.push(temp)
    }

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];


    var scaleX = d3.scaleBand()
        .domain(years)
        .range([0, plot_width])
        .padding(0.01);

    var scaleY = d3.scaleBand()
        .domain(months)
        .range([0, plot_height])
        .padding(0.01);

    var scaleColor = d3.scaleLinear()
                    .domain([0, d3.max(data, d=>{return d.Total})])
                    .range(['white', 'red'])

    var canvas = d3.select('#canvas')
        .append('svg')
        .attr('height', height)
        .attr('width', width)

    var plot = canvas.append('g')
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


    var heatmap = plot.selectAll('rect')
                .data(data, d=>{return d.Year+":"+d.Month;})
                .enter()
                .append('rect')
                .attr('class', 'heatmap-tile')
                .attr("x", d => { return scaleX(d.Year) })
                .attr("y", d => { return scaleY(d.Month) })
                .attr("width", d => { return scaleX.bandwidth() })
                .attr("height", d => { return scaleY.bandwidth() })
                .style("fill", d => { return scaleColor(d.Total) })

    var tooltip = d3.select("body")
        .append('g')
        .attr('class', 'tooltip-weather')
        .style('opacity', 0)


    heatmap.on("mouseover", function (d) {
        d3.select(event.currentTarget)
            .attr("stroke", 2);

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
            "translate(0, " + plot_height + ")")
        .attr('class', 'axes')
        .call(xAx);

    plot.append('g')
        .attr("transform",
            "translate(0, 0)")
        .attr('class', 'axes')
        .call(yAx);

    canvas.append('text')
        .attr("x", plot_width - 20)
        .attr("y", 0)
        .attr("class", "axis-label")
        .text('Year')

    canvas.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0)
        .attr("x", 0 - (plot_height / 2))
        .attr("dy", "1em") // nudge the text; see p 65 of Tips and Tricks
        .attr("class", "axis-label")
        .style("text-anchor", "middle")
        .text("Month");



    function tooltipFormatter(d) {
        return "<strong>"
                + d.Month + " "  + d.Year
                + "</strong></br>"
                + rainfall_format(d.Total) + " mm"
        
    }

}


function draw() {
    d3.csv("./static/js/rain.csv")
    .then(function (data) {
        data.forEach(d=>{
            d.Belmullet = +d.Belmullet;
            d.Valentia = +d.Valentia;
            d.Dublin = +d.Dublin;
            d.MalinHead = +d.MalinHead;
            d.Mullingar = +d.Mullingar;
            d.Shannon = +d.Shannon;
            d.Total = + d.Total;

        })
    drawGraph(data);
    })
    .catch((err) => {
    console.log("data loading error")
    console.log(err)
    })
    }
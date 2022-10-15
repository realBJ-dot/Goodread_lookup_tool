const container = d3.select('div')
.classed('container', true)
.style('border', '1px solid red');

const bars = container
.selectAll('.bar')
.data()
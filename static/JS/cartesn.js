
const width=900;
const height=600;

const svg=d3.select('.carteSn').append('svg')
                     .attr('width', width)
                     .attr('height',height );

const g=svg.append('g');

const projection=d3.geoMercator();

const path=d3.geoPath(projection)


d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")
    .then(data => {
        const countries=topojson.features(data,data.object.countries);

        g.selectAll('path').data(countries.features).enter()
                            .append('path')
                            .attr('class','country')
                            .attr('d',path)


    });

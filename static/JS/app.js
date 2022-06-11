
///////////////////////////Diagramme circulaire/////////////////////////////////////////
fetch('/nbrcommuneregion')
    .then(function (reponse){
        return reponse.json()
    }).then(function (text) {
   
var width=600,
height=500;


var couleur = d3.scaleOrdinal(["#035397","#F10086","#00FFC6","#F0A500","#FF6161"]); 
var svg = d3
  .select(".regparcom")
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  var data=[]
        
  for(i in text){
    console.log(text)
     data.push({ Region: i, Nbr:text[i]})
  }
  var base_diagramme = d3.pie().value(function (d) {
    return d.Nbr;
  })(data);
console.log(data);

var segments = d3
  .arc()
  .innerRadius(0)
  .outerRadius(200)
  .padAngle(0.05)
  .padRadius(50);

var sections = svg
  .append("g")
  .attr("transform", "translate(200,200)")
  .selectAll("path")
  .data(base_diagramme);
sections.enter().append("path").attr("d", segments)
 .attr("fill", function (d) {
    return couleur(d.data.Nbr);
  });
  var libelle = d3.select("g")
  .selectAll("text")
  .data(base_diagramme);
  libelle.enter()
    .append("text")
    .style("fill","white")
    .style("font-size","25px")
    .style("font-weight","bold")
    .classed("inside", true)
    .each(function(d){
  var center = segments.centroid(d);
   // console.log(center)
    d3.select(this)
    .attr("x", center[0])
    .attr("y", center[1])
    .text(d.data.Nbr);});
  
  var legends=svg.append("g")
  .attr("transform","translate(400,00)")
  .selectAll(".legends")
  .data(base_diagramme);
  var legend = legends.enter()
  .append("g")
  .classed("label", true)
  .attr("transform", function(d,i){
    return "translate(0," + (i+1)*30 + ")";
  });
  legend.append("circle")
    .attr("cx", 10)
    .attr("cy", 10)
    .attr("r",10)
    .attr("fill", function(d){
    return couleur(d.data.Nbr);
  });
  legend.append("text")
    .classed("label", true)
  .style("fill", "black")
  .style("font-size","15px")
    .text(function(d){
    return d.data.Region;
  })
  .attr("fill", function(d){
    return couleur(d.data.Nbr);
  })
  .attr("x", 25)
  .attr("y", 15);



})


/////////////////////////////Diagramme en barre des nombres de bureau de votes top 10 communes //////////////////////////////////////////
fetch('/bureaucom')
    .then(function (reponse){
        return reponse.json()
    }).then(function (text) {

        var data=[]
        
  for(i in text){
     data.push({ Commune: i, Nbr:text[i]})
  }



const width = 480;
const height = 460;
const margin = { top: 40, bottom: 90, left: 20, right: 20 };

var couleur = d3.scaleOrdinal(["#2F8F9D","#EB5353"," #5F7161","#F9D923","#541690","#F66B0E","#035397","#00FFC6","#DFDFDE","#05595B"]); 


const svg = d3.select('.nombrelieu')
  .append('svg')
  .attr('width', width - margin.left - margin.right)
  .attr('height', height - margin.top - margin.bottom)
  .attr("viewBox", [10, 20, width, height]);

const x = d3.scaleBand()
  .domain(d3.range(data.length))
  .range([margin.left, width - margin.right])
  .padding(0.3)

const y = d3.scaleLinear()
  .domain([0, 50])
  .range([height - margin.bottom, margin.top])


svg
  .append("g")
  .selectAll("rect")
  .data(data.sort((a, b) => d3.descending(a.Nbr, b.Nbr)))
  .join("rect")
    .attr("x", (d, i) => x(i))
    .attr("y", d => y(d.Nbr))
    .attr('title', (d) => d.Nbr)
    .attr("class", "rect")
    .attr("height", d => y(0) - y(d.Nbr))
    .attr("width", x.bandwidth())
    .attr("fill",couleur);

function yAxis(g) {
  g.attr("transform", `translate(${margin.left}, 0)`)
    .call(d3.axisLeft(y).ticks(null, data.format))
    .attr("font-size", '20px')
}

function xAxis(g) {
  g.attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickFormat(i => data[i].Commune))
    .attr("font-size", '12px')
    .selectAll("text")	
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-65)");
  
}

svg.append("g").call(xAxis);
svg.append("g").call(yAxis);
svg.node();

   

    })

//////////////////////////////////// Diagramme en barr top10 lieu de votes///////////////////////////////////

fetch('/datalieu')
    .then(function (reponse){
        return reponse.json()
    }).then(function (text) {

        var data=[]
        
  for(i in text){
     data.push({ lieu: i, Nbr:text[i]})
  }

const width = 630;
const height = 500;
const margin = { top: 50, bottom: 20, left: 200, right: 10};
const innerWidth=width-margin.left-margin.right;
const innerHeigh=height-margin.top-margin.bottom;


var couleur = d3.scaleOrdinal(["#B89E09","#FF7824"," #7315E6","#18F2BB","#7D2A19","#151D5C","#F6CD36","#6226E3","#FFFC40","#993487"]); 
const svg = d3.select('.top10bureau')
  .append('svg')
  .attr('width', width )
  .attr('height', height )

const render = data =>{
  

  const xScale=d3.scaleLinear()
        .domain([0,d3.max(data,d=>d.Nbr) ])
        .range([0,innerWidth]);


  const yScale=d3.scaleBand()
            .domain(data.map(d=>d.lieu))
            .range([0,innerHeigh])
            .padding(0.3)


  const g=svg.append('g')
            .attr("transform",`translate(${margin.left},${margin.top})`)

  g.append('g').call(d3.axisLeft(yScale))
                .selectAll("text")
                .style('font-size',"10px")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(30)");
  g.append('g').call(d3.axisBottom(xScale))
            .attr("transform",`translate(0,${innerHeigh})`)
 
  g.selectAll("rect")
    .data(data) 
    .enter().append("rect")
    .attr('y',d=>yScale(d.lieu))
      .attr("width", d => xScale(d.Nbr))
      .attr("height",d=> yScale.bandwidth())
      .style("fill",couleur)
      .selectAll('text')
      .style("font-size",'10px')
}
render(data)




    })


   ///////////////////////////////Carte Sénégal//////////////////////////////////
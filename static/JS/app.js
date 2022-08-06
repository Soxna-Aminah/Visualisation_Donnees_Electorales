
// //////////////////////////////////////////////////////////////////////////////////////
///////////////////////////Diagramme circulaire/////////////////////////////////////////
// ////////////////////////////////////////////////////////////////////////////////////

fetch('/nbrcommuneregion')
.then(reponse => reponse.json() )
.then( text => {
   
    let width = 570, height = 400
    let data=[]

    // let couleur = d3.scaleOrdinal(["#035397","#F10086","#00FFC6","#F0A500","#FF6161"])
    let couleur = d3.scaleOrdinal([ "#ff648c", "#b064f4", "#ffcc64", "#5ca4f4", "#202c74"])
    let svg = d3.select(".regparcom")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
      
    
    for(let i in text){
      data.push({ Region: i, Nbr:text[i]})
    }
    
    let base_diagramme = d3.pie().value( (d) => d.Nbr )(data);

    let segments = d3.arc()
      .innerRadius(0)
      .outerRadius(200)
      .padAngle(0.05)
      .padRadius(50);

    let sections = svg.append("g")
      .attr("transform", "translate(200,200)")
      .selectAll("path")
      .data(base_diagramme)
      

    sections.enter()
      .append("path")
      .attr("d", segments)
      .attr("fill", d => couleur(d.data.Nbr) )
      


    
    let libelle = d3.select("g")
      .selectAll("text")
      .data(base_diagramme)
      
    
    libelle.enter()
        .append("text")
        .style("fill","white")
        .style("font-size","25px")
        .style("font-weight","bold")
        .classed("inside", true)
        .each(function(d) {
          let center = segments.centroid(d)
          
          d3.select(this)
              .attr("x", center[0])
              .attr("y", center[1])
              .text(d.data.Nbr)
        })
        
      
    let legends = svg.append("g")
      .attr("transform","translate(400,00)")
      .selectAll(".legends")
      .data(base_diagramme)


    let legend = legends.enter()
      .append("g")
      .classed("label", true)
      .attr("transform", (d,i) =>"translate(0," + (i + 1) * 30 + ")" )

    legend.append("circle")
        .attr("cx", 10)
        .attr("cy", 10)
        .attr("r",10)
        .attr("fill", (d) => couleur(d.data.Nbr))

    legend.append("text")
        .classed("label", true)
        .style("fill", "black")
        .style("font-size","15px")
        .text(d => d.data.Region )
        .attr("fill", d => couleur(d.data.Nbr))
        .attr("x", 25)
        .attr("y", 15);
})







// ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////Diagramme en barre des nombres de bureau de votes top 10 communes //////////////////////////////////////////
// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
fetch('/bureaucom')
.then( reponse => reponse.json())
.then(text => {
  console.log(text);
    
    let data = []
    const width = 600;
    const height = 550;
    const margin = { top: 40, bottom: 90, left: 10, right: 0 };
        
    for(let i in text){
      data.push({ Commune: i, Nbr:text[i]})
    }

    // let couleur = d3.scaleOrdinal(["#2F8F9D","#EB5353"," #5F7161","#F9D923","#541690","#F66B0E","#035397","#00FFC6","#DFDFDE","#05595B"]); 
    // let couleur = d3.scaleOrdinal([ "#202c74"]); 202c74

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


    svg.append("g")
      .selectAll("rect")
      .data(data.sort((a, b) => d3.descending(a.Nbr, b.Nbr)))
      .join("rect")
        .attr("x", (d, i) => x(i))
        .attr("y", d => y(d.Nbr))
        .attr('title', (d) => d.Nbr)
        .attr("class", "rect")
        .transition()
        .duration(1500)
        .attr("height", d => y(0) - y(d.Nbr))
        .attr("width", x.bandwidth())
        .attr("fill","#202c74")
        
    

    function yAxis(g){
      g.attr("transform", `translate(${margin.left}, 0)`)
      .call(d3.axisLeft(y)
      .ticks(null, data.format))
      .attr("font-size", '20px')
    }

    
    function xAxis(g) {
      g.attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickFormat(i => data[i].Commune))
      .attr("font-size", '15px')
      .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)")
    }

    svg.append("g").call(xAxis);
    svg.append("g").call(yAxis);
    svg.node()
})



// ///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////// Diagramme en barr top10 lieu de votes///////////////////////////////////
// /////////////////////////////////////////////////////////////////////////////////////////////////////////

fetch('/datalieu')
.then(reponse => reponse.json())
.then( text => {
    let data=[]
    const width = 600;
    const height = 500;
    const margin = { top: 50, bottom: 20, left: 10, right: 50};
    const innerWidth=width-margin.left-margin.right;
    const innerHeigh=height-margin.top-margin.bottom;
        
    for(i in text){
       data.push({ lieu: i, Nbr:text[i]})
    }
    data.sort(function(a, b){
      return b.Nbr - a.Nbr;
  });


   
    const svg = d3.select('.top10bureau')
      .append('svg')
      .attr('width', width )
      .attr('height', height )

  let render = data => {

    const xScale = d3.scaleLinear()
      .domain([0, d3.max(data,d => d.Nbr)])
      .range([0,innerWidth])


    const yScale = d3.scaleBand()
      .domain(data.map(d => d.lieu))
      .range([0, innerHeigh])
      .padding(0.2)


    const g = svg.append('g')
      .attr("transform",`translate(${margin.left},${margin.top})`)
            
    let tick= g.append('g')
      .call(d3.axisLeft(yScale))
      .attr("class","bureaulabel")
      .selectAll("text")
        .attr("text-anchor", "start")
        .style('font-size',"0px")
        .attr("dx", "2em")
        .attr("dy", ".15em")
      

    g.append('g')
      .call(d3.axisBottom(xScale))
      .attr("transform",`translate(0,${innerHeigh} )`)
      
  
 
    let grect = g.selectAll("rect")
      .data(data) 
      .enter()
      .append("g")
      
      grect.append("rect")
          .transition()
          .duration(1000)
          .attr('y',d=>yScale(d.lieu) + 5)
          .attr("width", d => xScale(d.Nbr))
          .attr("height",d=> yScale.bandwidth() - 10)
          .style("fill","orangered")
          .style("opacity")

      grect.append("text")
            .transition()
            .duration(2000)
            .attr("class", "label" )
            .attr("y", d=> yScale(d.lieu) + margin.bottom + 2)
            .text(data => data.lieu )
            .attr("dx", "10px")
            .attr("fill","white");
      }

  render(data)

})
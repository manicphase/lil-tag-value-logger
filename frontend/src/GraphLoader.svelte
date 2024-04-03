<script>	
    import Graph from './graph.svelte';
    let graphData;
    let tempGraphData = [];
    let loadedData = 0;
    //let datas = [4,5,6,7,8,9]

    export let toFetch;

    function get_graph_data(prefix, session_id, tags, yAxis, lowerBound, upperBound) {
        console.log(session_id, prefix, tags, yAxis)
            let qs = "/get?session_id=" + session_id
            if (tags) {
                qs = qs + "&tags=" + tags.replace(/ /g, '');
            }
            fetch(qs)
            .then(r => r.json())
            .then(r => {
                for (let x =0; x<r.length; x++) {
                    r[x].tag = "" + prefix + " " + r[x].tag;
                    r[x].yAxis = yAxis;
                    r[x].upperBound = upperBound;
                    r[x].lowerBound = lowerBound;
                    console.log(r[x].tag)
                }
                tempGraphData = tempGraphData.concat(r);
                loadedData++;
                if (loadedData == toFetch.length) {
                    graphData = tempGraphData;
                    console.log("loaded", toFetch.length)
                    console.log(graphData)
                }
            })
        }
    
    for (let i = 0; i < toFetch.length; i++) {
        get_graph_data(toFetch[i][0], toFetch[i][1], toFetch[i][2], toFetch[i][3],
                       toFetch[i][4], toFetch[i][5], );
    }
</script>
{#if graphData != undefined}
    <Graph graphData={graphData}/>
{/if}

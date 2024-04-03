
<LibLoader url="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"
	on:loaded="{onLoaded}" />
<script>
    import LibLoader from './LibLoader.svelte';

    export let graphData = {};

    function makeid(length) {
        let result = '';
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const charactersLength = characters.length;
        let counter = 0;
        while (counter < length) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
            counter += 1;
        }
        return result;
    }

    const chart_id = makeid(10);

    function randomColour() {
        let colour = "#" + Math.floor(Math.random()*16777215).toString(16);
        console.log(colour)
        return colour
    }

    function getLongestLength(lists) {
        return lists.reduce(
            function (a, b) {
                return a.results.length > b.results.length ? a : b;
            }
        ).results.length
    }

    function makeXValues(lists) {
        console.log("hioihoihw")
        console.log(lists)
        let xValues = []; 
        let longestLength = getLongestLength(lists);
        console.log(lists[0].results.length)
        for (let i = 0; i < (longestLength); i++) {xValues.push(i)}
        return xValues;
    }
    
    function makeGraph(yValues) {
        let _datasets = []
        for (let i=0; i<yValues.length; i++) {
            _datasets.push({label: yValues[i].tag,
                            data: yValues[i].results.map(function (a) {return a.value}),
                            borderColor: randomColour(),
                            fill: false,
                            borderWidth: 1,
                            pointBorderWidth: 0.5,
                            pointRadius: 1,
                            yAxisID: yValues[i].yAxis,
                        })
        }
        let _scales = [];
        let scaleIDs = yValues.map((a) => {return a.yAxis})
                        .filter((value, index, array) => {return array.indexOf(value) === index});
        for (let i=0; i<scaleIDs.length; i++){
            _scales.push({
                id: scaleIDs[i],
                scaleLabel: {
                    display: true,
                    labelString: scaleIDs[i],
                },
                ticks: {
                    min: yValues[i].lowerBound ? parseInt(yValues[i].lowerBound): undefined,
                    max: yValues[i].upperBound ? parseInt(yValues[i].upperBound): undefined,
                }
            })
        }

        console.log(yValues);
        window.yValues = yValues;
        new Chart(chart_id, {
            type: "line",
            data: {
                labels: makeXValues(yValues),
                datasets: _datasets
            },
            options: {
                scales: {
                    yAxes: _scales,
                }
            }
        });
    }
    function onLoaded() {
        makeGraph(graphData)
    }
</script>
<div>
    <canvas id={chart_id} style="width:100%;max-width:1200px"></canvas>
</div>
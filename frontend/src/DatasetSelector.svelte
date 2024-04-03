<script>
    import GraphLoader from "./GraphLoader.svelte";

    export let rows = [["test", 9, "", 1, "", ""]];
    export let graph_name = "click here to edit graph name";
    let html_rows = [];
    let drawGraph = false;

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

    const table_id = makeid(10);
    const header_id = makeid(10);

    function addRow() {
        console.log(rows)
        rows = [...rows, ["", "", "", "", "", ""]]
        html_rows = document.getElementById(table_id).getElementsByTagName("tr")
        console.log(html_rows)
    }
    
    function editedCell() {
        html_rows = document.getElementById(table_id).getElementsByTagName("tr")
        let table_array = Array.from(html_rows).splice(1);
        console.log(table_array)
        for (let x=0; x<table_array.length; x++) {
            for (let y=0; y<table_array[x].children.length; y++) {
                rows[x][y] = table_array[x].children[y].children[0].value;
                console.log(rows[x][y])
            }
        }
        console.log(rows);
    }

    function makeGraph() {
        drawGraph = false;
        setTimeout(() => {drawGraph=true;}, 30)
        //drawGraph = true;
    }

    function cloneRow(row_id) {
        rows = [...rows, Array.from(rows[row_id])]
    }

    function deleteRow(row_id) {
        let new_rows = rows;
        new_rows.splice(row_id,1);
        rows = [...new_rows]
    }

    function saveGraph() {
        fetch("/graphing_session", {
            method: 'post',
            body: JSON.stringify(
                {name: document.getElementById(header_id).innerText,
                 data: JSON.stringify(rows)}
            ),
        })
        .then(r => r.json())
        .then(r => {
            console.log("saved data");
        })
    }

</script>
<h1 id={header_id} contenteditable=true>{graph_name}</h1>
<table id={table_id} style="max-width:100%" on:input={editedCell}>
    <tr><th>Prefix</th>
        <th>Session ID</th>
        <th>Tags</th>
        <th>Y Axis Group</th>
        <th>Lower Bound</th>
        <th>Upper Bound</th>
        <th></th></tr>
    {#each rows as row, index}
        <tr><td><input type="text" style="width: 100px;" value={row[0]} />
        </td><td><input type="text" style="width: 100px;"value={row[1]}/>
        </td><td><input type="text" style="width: 200px;"value={row[2]}/>
        </td><td><input type="text" style="width: 100px;"value={row[3]}/>
        </td><td><input type="text" style="width: 100px;"value={row[4]}/>
        </td><td><input type="text" style="width: 100px;"value={row[5]}/>
        </td><td><button on:click={() => {cloneRow(index)}}>Clone Row</button>
        </td><td><button on:click={() => {deleteRow(index)}}>Delete Row</button>
        </td></tr>
    {/each}
</table>

<button on:click={addRow}>Add row</button><button on:click={makeGraph}>Make Graph</button>
{#if drawGraph}
    <GraphLoader toFetch={rows} />
{/if}
<button on:click={saveGraph}>Save Graph</button>
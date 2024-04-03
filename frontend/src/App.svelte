<script>
    import DatasetSelector from './DatasetSelector.svelte';

    let saved_sessions = [];

    let graphs_to_load = [];

    let new_graph = {
        data: [["", 1, "", 1, "", ""]]
    }

    function get_index_of_row(row_id) {
        let ids = saved_sessions.map((a) => {return a.id});
        return ids.indexOf(row_id) ;
    }

    function is_already_listed(row_id) {
        let listed_ids = graphs_to_load.map((a) => {return a.id});
        return listed_ids.indexOf(row_id) < 0 ? false : true
    }

    fetch("/graphing_session")
            .then(r => r.json())
            .then(r => {saved_sessions = [...r]})

    function load_graph(row_id) {
        console.log(row_id)
        console.log(graphs_to_load)
        let index = get_index_of_row(row_id)
        if (!is_already_listed(row_id)) {
            graphs_to_load = [...graphs_to_load, saved_sessions[index]]
        }
    } 
    function add_graph() {
        graphs_to_load = [...graphs_to_load, new_graph]
    }
    function delete_graph(session_id) {
        console.log("delete")
        fetch("/graphing_session",{method:"delete",
                                   body: JSON.stringify({
                                    graph_id: session_id
                                   })})
            .then(r => r.json())
            .then(r => {saved_sessions = [...r]})
    }
</script>

<main>
    {#if saved_sessions.length > 0}
        {#each saved_sessions as session}
        <div><a href="javascript:void(0);" on:click={() => {load_graph(session.id)}} on:keypress={() => {load_graph(session.id)}}>{session.name} </a> 
            <a href="javascript:void(0);" on:click={() => {delete_graph(session.id)}} title="Delete">❌</a></div>
        {/each}
    {/if}
    {#if graphs_to_load.length > 0}
        {#each graphs_to_load as graph}
        <DatasetSelector rows={graph.data} graph_name={graph.name}/>
        {/each}
    {/if}
    <button on:click={add_graph}>Add new graph</button>
</main>


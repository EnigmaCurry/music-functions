<script>
 import Dropzone from "svelte-file-dropzone";

  let files = {
    accepted: [],
    rejected: []
  };

  function handleFilesSelect(e) {
    const { acceptedFiles, fileRejections } = e.detail;
    files.accepted = [...files.accepted, ...acceptedFiles];
    files.rejected = [...files.rejected, ...fileRejections];
  }
</script>

<h2>Coming Soon ... </h2>
<form action="/api/negative_harmony">
    <Dropzone on:drop={handleFilesSelect} multiple={false}>Drag and
    drop a single MIDI file here or click to select a file.</Dropzone>
    {#if files.accepted.length}
        Selected file: {files.accepted[0].name}
    {:else if files.rejected.length}
        Invalid MIDI file: {files.rejected[0].name}
    {/if}
</form>

<hr/>
<a href="https://youtu.be/DnBr070vcNE?t=1m31s">Watch this video to learn about negative harmony.</a>

<style>
 div {
     margin: 1em;
 }
 textarea {
     width: 40em;
     height: 8em;
 }
 table {
     margin: auto;
 }
</style>

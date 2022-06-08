<script>
 import Dropzone from "svelte-file-dropzone";

 let file;

 function handleFilesSelect(e) {
     const { acceptedFiles, fileRejections } = e.detail;
     if (acceptedFiles.length)
         file = acceptedFiles[0];
 }
</script>

<h2>Coming Soon ... </h2>
<form action="/api/negative_harmony">
    <Dropzone on:drop={handleFilesSelect} multiple={false}>Drag and
    drop a single MIDI file here or click to select a file.</Dropzone>
    {#if file != undefined}
        Selected file: {file.name}
    {/if}
</form>

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

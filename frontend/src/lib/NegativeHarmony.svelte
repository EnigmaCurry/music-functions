<script>
 import { tonics } from '../stores/negative_harmony.js'
 import { adjust_octaves } from '../stores/negative_harmony.js'
 import Dropzone from "svelte-file-dropzone";

 let files = {
     accepted: [],
     rejected: []
 };

 function handleFilesSelect(e) {
     const { acceptedFiles, fileRejections } = e.detail;
     files.accepted = [...acceptedFiles];
     files.rejected = [...fileRejections];
 }
</script>

<a href="https://youtu.be/DnBr070vcNE?t=1m31s">Watch this video to learn about negative harmony.</a>

<hr/>

<form action="/api/negative-harmony" method="post" enctype="multipart/form-data">
    <Dropzone on:drop={handleFilesSelect} multiple={false} accept="audio/midi" name="midi">Drag and
        drop a single MIDI file here or click to select a file.</Dropzone>
    {#if files.accepted.length}
        ✅ Selected file: {files.accepted[0].name}
    {:else if files.rejected.length}
        ❌ Invalid MIDI file: {files.rejected[0].name}
    {/if}
    <br/>
    <label for="tonics">Keyboard position to mirror (eg. C4 for the middle): <br/><small>(you can
        enter multiple notes to flip each one consecutively; separate by
        space)</small></label><br/>
    <input type="text" id="tonics" name="tonics" bind:value="{$tonics}" />
    <br/>
    <label for="adjust_octaves">Adjust octaves after flip?</label>
    <input type="checkbox" id="adjust_octaves" name="adjust_octaves" bind:checked="{$adjust_octaves}" />
    <br/>
    <br/>
    <button type="submit">
        Download MIDI
    </button>
</form>
<br/>

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

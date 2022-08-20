<script>
  import { start, num_bars } from "../stores/every_beat.js";
  import Markdown from "./Markdown.svelte";
  import help_text from "./Glicol.md?raw";
  import Glicol from "glicol";
  import { glicol_graph_src } from "../stores/glicol.js";

  const glicol = new Glicol();
  let audio_started = false;

  function toggleAudio() {
    audio_started = !audio_started;
    if (audio_started) {
      glicol.run($glicol_graph_src);
    } else {
      glicol.stop();
    }
  }

  function handleSourceChange(e) {
    console.log($glicol_graph_src);
    if (audio_started) {
      glicol.run($glicol_graph_src);
    }
  }

  function preventDirectEdit(e) {
    console.log(e);
    e.preventDefault();
    return false;
  }
</script>

<h3>Glicol DSP Graph</h3>
<textarea
  on:keydown={preventDirectEdit}
  bind:value={$glicol_graph_src}
  on:change={handleSourceChange}
/>
<br />
<button class="submit" on:click={toggleAudio}
  >{audio_started ? "Stop" : "Start"} Audio</button
>
<Markdown source={help_text} />
<br />

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

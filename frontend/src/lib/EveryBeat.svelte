<script>
  import { start, num_bars } from "../stores/every_beat.js";
  import Markdown from "./Markdown.svelte";
  import help_text from "./EveryBeat.md?raw";

  const random_start = (event) => {
    event.preventDefault();
    $start = Math.random() * 2 ** 64;
  };
</script>

<h3>Generate all possible 16 step drum loops (four instruments):</h3>

<form action="/api/every-beat">
  <label for="start"
    >Starting position:<br />
    <small>(Any number from 0 up to 2^64 (18446744073709551616))</small></label
  ><br />
  <input type="text" id="start" name="start" bind:value={$start} />
  <button on:click={random_start}>Randomize</button>
  <br />
  <label for="num_bars"
    >Number of bars to record? <br /><small>(Any number from 1 to 256)</small
    ></label
  ><br />
  <input type="text" id="num_bars" name="num_bars" bind:value={$num_bars} />
  <br />
  <br />
  <button class="submit" type="submit"> Download MIDI </button>
</form>
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

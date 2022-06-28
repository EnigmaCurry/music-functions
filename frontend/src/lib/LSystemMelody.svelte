<script>
  import { rule, root, scale, octaves } from "../stores/lsystem_melody.js";

  let keys = [
    "Ab",
    "A",
    "Bb",
    "B",
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
  ];
  let scales = [];
  if (scales.length === 0) {
    if (sessionStorage.scale_names) {
      scales = JSON.parse(sessionStorage.scale_names);
    } else {
      fetch("/api/info/scale_names")
        .then((resp) => resp.json())
        .then((s) => {
          scales = s["scales"];
          sessionStorage.scale_names = JSON.stringify(scales);
        });
    }
  }
</script>

<h3>Generate a fractal melody:</h3>

<form id="lsystem-form" action="/api/melody/lsystem">
  <label for="rule">L-system rule:</label><br />
  <input type="text" id="rule" name="rule" bind:value={$rule} />
  <br />
  <div class="options">
    <div>
      <label for="root">Root:</label><br />
      <select id="root" name="root" bind:value={$root}>
        {#each keys as r}
          <option value={r}>
            {r}
          </option>
        {/each}
      </select>
    </div>
    <div>
      <label for="rule">Scale:</label><br />
      <select id="scale" name="scale" bind:value={$scale}>
        {#each scales as s}
          <option value={s}>
            {s}
          </option>
        {/each}
      </select>
    </div>
  </div>
  <label for="rule">Octave Range:</label><br />
  <input type="text" id="octaves" name="octaves" bind:value={$octaves} />
  <br />
  <br />
  <button class="submit" type="submit"> Download MIDI </button>
  <hr />
</form>
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
  .options {
    width: 10em;
    display: flex;
    justify-content: space-around;
    margin: auto;
  }
</style>

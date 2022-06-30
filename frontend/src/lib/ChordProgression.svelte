<script>
  import { onMount, onDestroy } from "svelte";
  import { chord_progression } from "../stores/chord_progression.js";
  import { draw_keyboard } from "../piano_keyboard.js";
  import { get_closest_word, get_next_word_position } from "../string_util.js";
  import * as Tone from "tone";
  import { Piano } from "@tonejs/piano";
  import Markdown from "./Markdown.svelte";
  import help_text from "./ChordProgression.md?raw";

  let backslash_is_held = false;
  let shift_is_held = false;
  let tab_is_held = false;
  let piano;
  const piano_keys_held = new Set();
  let current_chord = null;

  const chord_cache_key = "chord_progression/chord_info";
  async function get_chord_info(chord) {
    const key = chord_cache_key + "/" + chord;
    const cachedInfo = sessionStorage.getItem(key);
    if (cachedInfo === "invalid") {
      return cachedInfo;
    } else if (cachedInfo != null) {
      return JSON.parse(cachedInfo);
    } else {
      const url = new URL(window.location.origin + "/api/info/chord");
      url.searchParams.append("chord", chord);
      const resp = await fetch(url);
      if (resp.status == 200) {
        const info = JSON.parse(await resp.text());
        sessionStorage.setItem(key, JSON.stringify(info));
        return info;
      } else if (resp.status == 400) {
        sessionStorage.setItem(key, "invalid");
        return "invalid";
      }
      return "invalid";
    }
  }

  async function updateChord(cursor_position) {
    let chord = get_closest_word($chord_progression, cursor_position);
    if (!chord.length || chord == " ") {
      //Try adjacent word:
      chord = get_closest_word($chord_progression, cursor_position - 1);
    }
    const info = await get_chord_info(chord);
    if (info === "invalid") {
      current_chord = { chord: chord, valid: false };
      draw_keyboard(keyboard_canvas);
    } else {
      current_chord = info;
      draw_keyboard(keyboard_canvas, current_chord.components_midi);
    }
  }

  async function handle_input(e) {
    if (e.code === "Backslash") {
      backslash_is_held = false;
      release_piano_keys();
    } else if (e.code === "ShiftLeft" || e.code === "ShiftRight") {
      shift_is_held = false;
    } else if (e.code === "Tab") {
      tab_is_held = false;
      return;
    }
    const cursor_position = e.target.selectionStart;
    updateChord(cursor_position);
  }

  async function handle_pointer(e) {
    const cursor_position = e.target.selectionStart;
    updateChord(cursor_position);
  }

  async function release_piano_keys() {
    if (typeof piano != "undefined") {
      for (let k of piano_keys_held) piano.keyUp({ note: k });
      piano_keys_held.clear();
    }
  }

  async function play_chord() {
    let t = 0;
    let note_delay = shift_is_held && !tab_is_held ? 0.35 : 0;
    release_piano_keys();
    console.debug(
      "playing chord:",
      current_chord.chord,
      current_chord.components_with_pitch
    );
    if (note_delay === 0) {
      // Add an extra bass note one octave below the root:
      /* const octave = current_chord.components_with_pitch[0].match(/[0-9]$/)[0];
       * const n = current_chord.components[0] + (octave - 1);
       * piano.keyDown({
       *   note: n,
       *   velocity: 0.75,
       *   time: "+0",
       * });
       * piano_keys_held.add(n); */
    }
    for (let i = 0; i < current_chord.components_with_pitch.length; i++) {
      t = t + note_delay;
      piano.keyDown({
        note: current_chord.components_with_pitch[i],
        time: "+" + t,
      });
      piano_keys_held.add(current_chord.components_with_pitch[i]);
    }
  }

  async function handle_keypress(e) {
    if (e.code === "Backslash") {
      e.preventDefault();
      if (backslash_is_held) return;
      backslash_is_held = true;
      await play_chord();
    } else if (e.code === "ShiftLeft" || e.code === "ShiftRight") {
      shift_is_held = true;
    } else if (e.code === "Tab" && e.target.id === "chords") {
      e.preventDefault();
      if (tab_is_held) return;
      tab_is_held = true;
      let direction = 1;
      if (shift_is_held) direction = -1;
      e.target.selectionStart = e.target.selectionEnd = get_next_word_position(
        $chord_progression,
        e.target.selectionStart,
        direction
      );
      await updateChord(e.target.selectionStart);
      if (backslash_is_held) {
        await play_chord();
      }
    }
  }

  let keyboard_canvas;
  onMount(async () => {
    keyboard_canvas = document.getElementById("chord_keyboard");
    draw_keyboard(keyboard_canvas);
    if (typeof piano === "undefined") {
      await Tone.start();
      piano = new Piano({
        url: "/samples/salamander-piano/",
        velocities: 1,
      });
      piano.toDestination();
      await piano.load();
    }
  });
  onDestroy(async () => {
    await release_piano_keys();
  });
</script>

<h3>Create a MIDI chord progression:</h3>

<form action="/api/chords/sequence">
  <div>
    <textarea
      id="chords"
      name="chords"
      placeholder="Enter a chord sequence"
      spellcheck="false"
      on:keyup={handle_input}
      on:click={handle_input}
      on:keydown={handle_keypress}
      on:selectionchange={handle_pointer}
      bind:value={$chord_progression}
    />
  </div>
  <div id="chord_info">
    <canvas id="chord_keyboard" width="650" height="72"
      >Your browser does not support the HTML5 canvas tag.</canvas
    ><br />
    {#if current_chord != null}
      {#if current_chord.valid === false}
        Invalid chord: ❌ <span style="color:#F00;">{current_chord.chord}</span>
      {:else}
        Chord: ✅ <span style="color:#0F0;">{current_chord.chord}</span> |
        Notes: {current_chord.components} | Quality: {current_chord.quality_components}
      {/if}
    {:else}
      <span>&nbsp;</span>
    {/if}
  </div>
  <div>
    <button class="submit" type="submit"> Download MIDI </button>
  </div>
</form>
<Markdown source={help_text} />

<style>
  div {
    margin: 1em;
  }
  textarea {
    width: 25em;
    height: 8em;
    font-size: 1.5em;
  }
  @media (max-width: 420px) {
    textarea {
      width: 18em;
      font-size: 1em;
    }
    canvas#chord_keyboard {
      margin-left: -90%;
    }
    div#chord_info {
      transform: scale(0.65);
    }
  }
  @media (max-width: 275px) {
    div#chord_info {
      transform: scale(0.5);
    }
  }
</style>

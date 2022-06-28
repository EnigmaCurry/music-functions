<script>
 import { onMount } from 'svelte'
 import { chord_progression } from '../stores/chord_progression.js'
 import { draw_keyboard } from '../piano_keyboard.js'
 import { get_closest_word, get_next_word_position } from '../string_util.js'
 import * as Tone from 'tone'
 import { Piano } from '@tonejs/piano'
 import Markdown from './Markdown.svelte'
 import help_text from './ChordProgression.md?raw'

 var backslash_is_held = false;
 var shift_is_held = false;
 var tab_is_held = false;
 var piano;
 var piano_keys_held = new Set();
 let current_chord = null;

 const chordCacheKey = "chord_progression/chord_info"
 async function get_chord_info(chord) {
     const key = chordCacheKey + "/" + chord
     const cachedInfo = sessionStorage.getItem(key)
     if (cachedInfo === "invalid") {
         return cachedInfo
     } else if (cachedInfo != null) {
         return JSON.parse(cachedInfo)
     } else {
         const url = new URL(window.location.origin + "/api/info/chord")
         url.searchParams.append("chord", chord)
         const resp = await fetch(url)
         if (resp.status == 200) {
             const info = JSON.parse(await resp.text())
             sessionStorage.setItem(key, JSON.stringify(info))
             return info
         } else if (resp.status == 400) {
             sessionStorage.setItem(key, "invalid")
             return "invalid"
         }
         return "invalid"
     }
 }

 async function updateChord(cursor_position) {
     let chord = get_closest_word($chord_progression, cursor_position)
     if (!chord.length || chord == " "){
         //Try adjacent word:
         chord = get_closest_word($chord_progression, cursor_position-1)
     }
     const info = await get_chord_info(chord)
     if (info === "invalid") {
         current_chord = {chord: chord, valid: false}
             draw_keyboard(keyboard_canvas)
     } else {
         current_chord = info
         draw_keyboard(keyboard_canvas, current_chord.components_midi)
     }
 }

 async function handleInput(e) {
     if (e.code === "Backslash") {
         backslash_is_held = false;
         if (piano != undefined){
             for(let k of piano_keys_held)
                 piano.keyUp({note: k})
             piano_keys_held.clear()
         }
     } else if (e.code === "ShiftLeft" || e.code === "ShiftRight") {
         shift_is_held = false
     } else if (e.code === "Tab") {
         tab_is_held = false
         return
     }
     const cursor_position = e.target.selectionStart
     updateChord(cursor_position)
 }

 async function handleKeypress(e) {
     if (e.code === "Backslash") {
         e.preventDefault()
         if (backslash_is_held)
             return
         if (piano === undefined) {
             await Tone.start()
             //synth = new Tone.PolySynth(Tone.Synth).toDestination();
             piano = new Piano({velocities: 1})
             piano.toDestination()
             await piano.load()
         }
         backslash_is_held = true
         let t = 0
         let note_delay = shift_is_held ? 0.35 : 0
         console.debug("playing chord:", current_chord.chord, current_chord.components_with_pitch)
         for (let i=0; i<current_chord.components_with_pitch.length; i++){
             t = t + note_delay
             piano.keyDown({note:current_chord.components_with_pitch[i], time: "+"+t})
             piano_keys_held.add(current_chord.components_with_pitch[i])
         }
     } else if (e.code === "ShiftLeft" || e.code === "ShiftRight") {
         shift_is_held = true
     } else if (e.code === "Tab" && e.target.id === "chords") {
         e.preventDefault()
         if (tab_is_held)
             return
         tab_is_held = true
         let direction = 1
         if (shift_is_held) direction = -1
         e.target.selectionStart = e.target.selectionEnd = get_next_word_position($chord_progression, e.target.selectionStart, direction)
         updateChord(e.target.selectionStart)
     }
 }

 var keyboard_canvas;
 onMount(async () => {
     keyboard_canvas = document.getElementById("chord_keyboard")
     draw_keyboard(keyboard_canvas)
 })

</script>
<h3>Create a MIDI chord progression:</h3>

<form action="/api/chords/sequence">
    <div>
        <textarea id="chords" name="chords" placeholder="Enter a chord sequence" spellcheck="false" on:keyup={handleInput} on:click={handleInput} on:keydown={handleKeypress} bind:value={$chord_progression} />
    </div>
    <div>
        <canvas id="chord_keyboard" width="650" height="72">Your browser does not support the HTML5 canvas tag.</canvas><br/>
        {#if current_chord != null}
            {#if current_chord.valid === false}
                Invalid chord: ❌ <span style="color:#F00;">{current_chord.chord}</span>
            {:else}
                Chord: ✅ <span style="color:#0F0;">{current_chord.chord}</span> |
                Notes: {current_chord.components} |
                Quality: {current_chord.quality_components}
            {/if}
        {:else}
        <span>&nbsp;</span>
        {/if}
    </div>
    <div>
        <button class="submit" type="submit">
            Download MIDI
        </button>
    </div>
</form>
<Markdown source={help_text} />

<style>
 div {
     margin: 1em;
 }
 textarea {
     width: 40em;
     height: 8em;
 }
</style>

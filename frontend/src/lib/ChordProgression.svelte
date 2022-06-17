<script>
 import { onMount } from 'svelte'
 import { chord_progression } from '../stores/chord_progression.js'
 import { draw_keyboard } from '../piano_keyboard.js'
 import { getClosestWord } from '../string_util.js'

 const chordCacheKey = "chord_progression/chord_info"
 async function getChordInfo(chord) {
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

 let current_chord = null;
 async function handleInput(e) {
     const cursor_position = e.target.selectionStart
     let chord = getClosestWord($chord_progression, cursor_position)
     if (!chord.length || chord == " "){
         //Try adjacent word:
         chord = getClosestWord($chord_progression, cursor_position-1)
     }
     const info = await getChordInfo(chord)
     if (info === "invalid") {
         current_chord = {chord: chord, valid: false}
         draw_keyboard(keyboard_canvas)
     } else {
         current_chord = info
         draw_keyboard(keyboard_canvas, current_chord.components_midi)
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
        <textarea id="chords" name="chords" placeholder="Enter a chord sequence" spellcheck="false" on:keyup={handleInput} on:click={handleInput} bind:value={$chord_progression} />
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
    <div>
        <ul>
            <li>Enter a sequence of any chords recognized by <a target="_new" href="https://github.com/yuma-m/pychord">pychord</a> separated by spaces and/or newlines.</li>
            <li>Each chord may be prefixed by a length, in beats
                (defaults to 4 beats, or 1 bar, if not specified.)</li>
            <li>Chords may by inverted by specifying <a target="_new" href="https://en.wikipedia.org/wiki/Slash_chord">a slash
                chord</a> (eg. C/E or C/G) or use C/1, C/2, C/3 etc.
                for 1st, 2nd, or 3rd order inversions. </li>
            <li>Click the Download MIDI button to generate the MIDI
            file containing your chords.</li>
        </ul>
        <table>
            <tr>
                <th>
                    Example chord
                </th>
                <th>
                    Beats
                </th>
                <th>
                    Description
                </th>
            </tr>
            <tr>
                <td>
                    C
                </td>
                <td>4</td>
                <td>
                    C Major
                </td>
            </tr>
            <tr>
                <td>
                    2C
                </td>
                <td>2</td>
                <td>
                    C Major
                </td>
            </tr>
            <tr>
                <td>
                    8Cm
                </td>
                <td>8</td>
                <td>
                    C Minor
                </td>
            </tr>
            <tr>
                <td>
                    C/E
                </td>
                <td>4</td>
                <td>
                    C Major<br/> (1st inversion with root of E)
                </td>
            </tr>
            <tr>
                <td>
                    C/G
                </td>
                <td>4</td>
                <td>
                    C Major <br/> (2nd inversion with root of G)
                </td>
            </tr>
            <tr>
                <td>
                    C/1
                </td>
                <td>4</td>
                <td>
                    C Major<br/> (1st inversion with root of E)
                </td>
            </tr>
            <tr>
                <td>
                    C/2
                </td>
                <td>4</td>
                <td>
                    C Major <br/> (2nd inversion with root of G)
                </td>
            </tr>
            <tr>
                <td>
                    Am7
                </td>
                <td>4</td>
                <td>
                    A Minor 7th
                </td>
            </tr>
            <tr>
                <td>
                    Abm7
                </td>
                <td>4</td>
                <td>
                    Ab Minor 7th
                </td>
            </tr>
            <tr>
                <td>
                    3C#maj7
                </td>
                <td>3</td>
                <td>
                    C# Major 7th
                </td>
            </tr>
        </table>
    </div>
    <div>
        <h3>Example chord sequences:</h3>
        <h4>Satin Doll (Duke Ellington):</h4>
        Dm7 G7 Dm7 G7 Em7 A7 Em7 A7 Am7 D7 Abm7 Db7 Cmaj7 Dm7 Em7 A7
    </div>
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
     border-spacing: 2em 0;
 }
</style>

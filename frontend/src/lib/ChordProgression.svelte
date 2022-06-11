<script>
 import { chord_progression } from '../stores/chord_progression.js'
</script>

<form action="/api/chords/sequence">
    <div>
        <textarea id="chords" name="chords" placeholder="Enter a chord sequence" bind:value={$chord_progression} />
    </div>
    <div>
        <button type="submit">
            Download MIDI
        </button>
    </div>
    <div>
        <h3>Create a MIDI chord progression:</h3>
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

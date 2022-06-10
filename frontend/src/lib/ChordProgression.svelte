<script>
  let count = 0
  const increment = () => {
    count += 1
  }
</script>

<form action="/api/chords/sequence">
    <div>
        <textarea id="chords" name="chords" value="" placeholder="Enter a chord sequence" />
    </div>
    <div>
        <button type="submit">
            Download MIDI
        </button>
    </div>
    <div>
        <h3>Create a MIDI chord progression:</h3>
        <ul>
            <li>Enter a sequence of any chords recognized by <a href="https://github.com/yuma-m/pychord">pychord</a> separated by spaces and/or newlines.</li>
            <li>Each chord may be prefixed by a length, in beats
                (defaults to 4 beats, or 1 bar, if not specified.)</li>
            <li>Chords may by inverted by specifying the root after a slash (eg. C/E or C/G)</li>
            <li>Click the Download MIDI button to generate the MIDI
            file containing your chords.</li>
        </ul>
        <table>
            <tr>
                <th>
                    Example chord
                </th>
                <th>
                    Description
                </th>
            </tr>
            <tr>
                <td>
                    C
                </td>
                <td>
                    C Major (4 beats)
                </td>
            </tr>
            <tr>
                <td>
                    2C
                </td>
                <td>
                    C Major (2 beats)
                </td>
            </tr>
            <tr>
                <td>
                    8Cm
                </td>
                <td>
                    C Minor (8 beats)
                </td>
            </tr>
            <tr>
                <td>
                    C/E
                </td>
                <td>
                    C Major (4 beats, 1st inversion with root of E)
                </td>
            </tr>
            <tr>
                <td>
                    C/G
                </td>
                <td>
                    C Major (4 beats, 2nd inversion with root of G)
                </td>
            </tr>
            <tr>
                <td>
                    Am7
                </td>
                <td>
                    A Minor 7th (4 beats)
                </td>
            </tr>
            <tr>
                <td>
                    Abm7
                </td>
                <td>
                    Ab Minor 7th (4 beats)
                </td>
            </tr>
            <tr>
                <td>
                    3C#maj7
                </td>
                <td>
                    C# Major 7th (3 beats)
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
 }
</style>

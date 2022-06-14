<script>
 import { start, num_bars } from '../stores/every_beat.js'
 const random_start = (event) => {
     event.preventDefault();
     $start = Math.random() * 2**64;
 }
</script>

<h3>Generate all 16 step (four instrument) drum loops possible:</h3>

<form action="/api/every-beat">
    <label for="start">Starting position:<br/>    <small>(Any number from 0 up to 2^64 (18446744073709551616))</small></label><br/>
    <input type="text" id="start" name="start" bind:value="{$start}" />
    <button on:click={random_start}>Randomize</button>
    <br/>
    <label for="num_bars">Number of bars to record? <br/><small>(Any number from 1 to 256)</small></label><br/>
    <input type="text" id="num_bars" name="num_bars" bind:value="{$num_bars}" />
    <br/>
    <br/>
    <button class="submit" type="submit">
        Download MIDI
    </button>
    <hr/>
    <ul>
        <li>
            <a href="https://github.com/monsieursquirrel/every_beat">Every Beat</a> is
            a simple MIDI drum machine that can create (ie. find) any
            possible 16 step (four instrument) drum sequence.
        </li>
        <li>
            Beats are limited to only these instruments: Kick, Snare,
            Closed Hat, Open Hat.
        </li>
        <li>
            You can derive any possible 16 step sequence by specifying
            a unique starting position (from 0 up to 2^64).
        </li>
        <li>
            The number of bars you specify will limit the size of the
            generated MIDI file (maximum 256 bars). If you specify a
            value greater than one, the subsequent bars will be
            modified slightly each time (starting with the open hats)
        </li>
        <li>
            When the starting position is 0, you get the famous <a href="https://en.wikipedia.org/wiki/Amen_break">Amen
            Break</a>.
        </li>
    </ul>
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

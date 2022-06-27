 * [Every Beat](https://github.com/monsieursquirrel/every_beat) is a
   simple MIDI drum machine that can create (ie. find) any possible 16
   step (four instrument) drum sequence.
 * Beats are limited to only these instruments: Kick, Snare, Closed
   Hat, Open Hat.
 * You can derive any possible 16 step sequence by specifying a unique
   starting position (from 0 up to 2^64).
 * The number of bars you specify will limit the size of the generated
   MIDI file (maximum 256 bars). If you specify a value greater than
   one, the subsequent bars will be modified slightly each time
   (starting with the open hats) 
 * When the starting position is 0, you get the famous [Amen
   Break](https://en.wikipedia.org/wiki/Amen_break).

import { writable, derived } from "svelte/store";

const chords_key = "chord_progression/chords";
export const chord_progression = writable(
  localStorage.getItem(chords_key) ||
    "Dm7 G7 Dm7/1 G7/1\nEm7 A7 Em7/1 A7/1\nAm7 D7 Abm7/1 Db7\nCmaj7 Dm7 Em7/2 A7"
);
chord_progression.subscribe((value) => localStorage.setItem(chords_key, value));

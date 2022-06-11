import { writable, derived } from 'svelte/store';

const chords_key = "chord_progression/chords"
export const chord_progression = writable(localStorage.getItem(chords_key) || '');
chord_progression.subscribe((value) => localStorage.setItem(chords_key, value));

import { writable, derived } from 'svelte/store';

const start_key = "every_beat/start"
export const start = writable(localStorage.getItem(start_key) || '0');
start.subscribe((value) => localStorage.setItem(start_key, value));

const num_bars_key = "every_beat/num_bars"
export const num_bars = writable(localStorage.getItem(num_bars_key) || '1');
num_bars.subscribe((value) => localStorage.setItem(num_bars_key, value));

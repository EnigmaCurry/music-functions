import { writable, derived } from 'svelte/store';

const tonics_key = "negative_harmony/tonics"
export const tonics = writable(localStorage.getItem(tonics_key) || 'C4');
tonics.subscribe((value) => localStorage.setItem(tonics_key, value));

const adjust_octaves_key = "negative_harmony/adjust_octaves"
export const adjust_octaves = writable(localStorage.getItem(adjust_octaves_key) === 'true');
adjust_octaves.subscribe((value) => localStorage.setItem(adjust_octaves_key, String(value)));


import { writable, derived } from 'svelte/store';

const rule_key = "melody/lsystem/rule"
export const rule = writable(localStorage.getItem(rule_key) || 'N[+N--?N]+N[+?N]');
rule.subscribe((value) => localStorage.setItem(rule_key, value));

const root_key = "melody/lsystem/root"
export const root = writable(localStorage.getItem(root_key) || 'C');
root.subscribe((value) => localStorage.setItem(root_key, value));

const scale_key = "melody/lsystem/scale"
export const scale = writable(localStorage.getItem(scale_key) || 'major');
scale.subscribe((value) => localStorage.setItem(scale_key, value));

const octaves_key = "melody/lsystem/octaves"
export const octaves = writable(localStorage.getItem(octaves_key) || '4');
octaves.subscribe((value) => localStorage.setItem(octaves_key, value));

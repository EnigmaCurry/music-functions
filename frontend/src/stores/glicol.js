import { writable, derived } from "svelte/store";

const glicol_key = "glicol/glicol_graph_src";
export const glicol_graph_src = writable(
  localStorage.getItem(glicol_key) ||
    "o: saw 50 >> lpf 300.0 1.0"
);
glicol_graph_src.subscribe((value) => localStorage.setItem(glicol_key, value));

<script>
 import logo from './assets/svelte.png'
 import ChordProgression from './lib/ChordProgression.svelte'
 import NegativeHarmony from './lib/NegativeHarmony.svelte'
 import Credits from './lib/Credits.svelte'
 import { Tabs, Tab, TabList, TabPanel } from 'svelte-tabs'

 const tabs = ["#chord-progressions","#negative-harmony","#credits"]

 let selectedTabIndex = 0
 $: if(tabs.indexOf(location.hash) >= 0) {
     selectedTabIndex = tabs.indexOf(location.hash)
 }

 function handleTabChange(event) {
     console.log(event)
     location.hash = tabs[event.detail.selectedTabIndex]
 }
</script>

<main>
  <h1>Music Functions</h1>

  <Tabs selectedTabIndex={selectedTabIndex} on:tabChanged={handleTabChange}>
      <TabList>
          <Tab>Chord Progression</Tab>
          <Tab>Negative Harmony</Tab>
          <Tab>Credits</Tab>
      </TabList>
      <TabPanel>
          <ChordProgression />
      </TabPanel>
      <TabPanel>
          <NegativeHarmony />
      </TabPanel>
      <TabPanel>
          <Credits />
      </TabPanel>
  </Tabs>
</main>

<style>
:root {
    --background-color: #000000;
    --primary-color: #ffffff;
    --secondary-color: #ff7549;
    --block-color: #222;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
                 Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    line-height: 1.75em;
    font-size: 1.2em;
    background-color: var(--background-color);
    color: var(--primary-color);
}

main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
    max-width: 40em;
    background-color: var(--background-color);
}

h1 {
    color: var(--secondary-color);
    text-transform: uppercase;
    font-size: 4rem;
    font-weight: 100;
    line-height: 1.1;
    margin: auto;
    max-width: 14rem;
}

:global(p) {
    max-width: 14rem;
    margin: 1rem auto;
    line-height: 1.35;
}

:global(a) {
    color: var(--secondary-color);
}
:global(ul.svelte-tabs__tab-list) {
    border-bottom: none !important;
}
:global(.svelte-tabs li.svelte-tabs__tab) {
    color: var(--secondary-color);
    line-height: 1.2em;
    max-width: 5em;
    outline: none !important;
}

:global(button) {
    font-family: inherit;
    font-size: inherit;
    padding: 1em 2em;
    border-radius: 2em;
    border: 2px solid rgba(255, 62, 0, 0);
    outline: none;
    width: 250px;
    font-variant-numeric: tabular-nums;
    cursor: pointer;
    color: #f7ff00;
    background-color: rgba(255, 84, 0, 0.26);
  }

:global(button:focus) {
    border: 2px solid #ff3e00;
}

:global(button:active) {
    background-color: rgba(255, 62, 0, 0.2);
}

:global(pre) {
    background-color: var(--block-color);
    padding-left: 2em;
    line-height: 1em;
}

:global(.dropzone, textarea) {
    background-color: var(--block-color) !important;
    color: var(--primary-color) !important;
}

@media (min-width: 480px) {
    h1 {
        max-width: none;
    }

    p {
        max-width: none;
    }
}
</style>

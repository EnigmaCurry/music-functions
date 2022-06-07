<script>
 import logo from './assets/svelte.png'
 import ChordProgression from './lib/ChordProgression.svelte'
 import Credits from './lib/Credits.svelte'
 import { Tabs, Tab, TabList, TabPanel } from 'svelte-tabs'

 const tabs = ["#chord-progressions","#credits"]

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
          <Tab>Credits</Tab>
      </TabList>
      <TabPanel>
          <ChordProgression />
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
    --block-color: #333333;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
                 Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: var(--background-color);
    color: var(--primary-color);
}

main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
    background-color: var(--background-color);
}

img {
    height: 16rem;
    width: 16rem;
}

h1 {
    color: var(--secondary-color);
    text-transform: uppercase;
    font-size: 4rem;
    font-weight: 100;
    line-height: 1.1;
    margin: 2rem auto;
    max-width: 14rem;
}

p {
    max-width: 14rem;
    margin: 1rem auto;
    line-height: 1.35;
}

a {
    color: var(--secondary-color);
}

:global(.svelte-tabs li.svelte-tabs__tab) {
    color: var(--secondary-color);
}

:global(button) {
    font-family: inherit;
    font-size: inherit;
    padding: 1em 2em;
    border-radius: 2em;
    border: 2px solid rgba(255, 62, 0, 0);
    outline: none;
    width: 200px;
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

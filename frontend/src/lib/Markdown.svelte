<script>
 export let source
 import SvelteMarkdown from 'svelte-markdown'
</script>


<div class="markdown">
    <SvelteMarkdown {source}/>
</div>

<style>
 div.markdown :global(pre) {
     background-color: var(--block-color);
     padding: 1em;
     padding-left: 1em;
     font-size: 1em;
     line-height: 1em;
     border-radius: 6px;
 }
 div.markdown :global(code):not(pre code) {
     background-color: var(--block-color);
     font-size: 1em;
     line-height: 1em;
     padding: .2em .4em;
     border-radius: 6px;
 }
 div.markdown {
     text-align: left;
 }
 div.markdown :global(table) {
     margin: auto;
     border-spacing: 2em 0;
 }

 div.markdown :global(th) {
     padding: 0 1em 0 1em;
 }

 div.markdown :global(td) {
     border-bottom: 2px dashed white;
     padding: .5em 0 .5em 0;
 }

</style>

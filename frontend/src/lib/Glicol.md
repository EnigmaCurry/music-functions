Program your own synthesizer using the [Glicol](https://glicol.org/)
Computer Music Language. Glicol is a domain specific language for
creating audio DSP graphs. You can connect components together just
like a modular synthesizer, but with simple code in place of physical
cables.

Before using this, you should get familiar with the main
[glicol.org](https://glicol.org/) website. If you wish to code by
typing directly in your browser window, that page is more suitable
than this one.

The interface on this page is designed exclusively for live coding
with an external editor (eg. Emacs) and with a web-browser extension
like [Edit with Emacs](https://github.com/stsquad/emacs_chrome). With
the browser extension installed, you will be able to edit the contents
of any webpage `<textarea>` elements, from the comfort of an external
text editor (right click the textarea above and choose `Edit with
Emacs`). Everytime you save the code in Emacs, the underlying audio
graph on this page will be updated automatically.

Click the `Start Audio` button above to toggle the DSP graph on or
off.

You must not directly type into the textarea (it will be ignored). You
must use an external editor (this is to ensure that the external
editor's buffer remains a true representation of the current state at
all times).


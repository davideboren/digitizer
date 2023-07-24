# Digitizer

This is a character management utility for the Tyrannomon project.

There are a huge number of sprites and evolution trees to include in Tyrannomon, and hardcoding them all by hand would be a giant pain.
This is a GUI utility to streamline the evolution tree building process with a simple drag and drop interface. Building evolution trees visually is way more fun!

In lieu of a traditional menu-based GUI, Digitizer uses a "microconsole." A small command line at the top of the app, accessible by pressing `
In the interest of simplicity, microconsole only has a single line of output, seen on the right side of the screen.

Output is a C++ header which can then be included in the Tyrannomon source files.

Digitizer also contains a function that automates the file conversions from transparent PNG to BMP, which is Tyrannomon's preferred file format.

Both Tyrannomon and Digitizer are built around the sprite format of Tortoiseshel's excellent 16x16 Digimon sprite resource.
https://withthewill.net/threads/full-color-digimon-dot-sprites.25843/




![Digitizer](https://github.com/davideboren/digitizer/assets/7462768/f7e51196-9383-4f93-b594-c215f80a48a5)

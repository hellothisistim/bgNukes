bgNukes README

# Overview
bgNukes is a tool for launching background renders from [The Foundry's Nuke](http://www.thefoundry.co.uk/products/nuke/). It is written by [Tim BOWMAN](http://hellothisistim.com).

This script exists because our company renderfarm wasn't alive yet and I was already frustrated with rendering in the Nuke UI and tired of typing out command-line render commands to background the renders. I am sharing it because I'm sure my situation was not unique.

Originally, I posted it as launchNukes_inNuke.py (I know -- awful name) on VFXTalk. As of now, the [official home](http://github.com/timbowman/bgRender) for bgRender will be on GitHub and it will be found also on [Nukepedia](http://www.nukepedia.com/).

# How to install
Put bgNukes in your .nuke directory (or somewhere else in your Nuke path if you're fancy), then add this line to your menu.py:

import bgNukes

Importing the module adds a "BG Render" item to the Render menu. 

# How to use
Select the Write node (or nodes) that you want to render. (If you don't select anything, that's the same as if you selected everything.) Now select the "BG Render" item from the Render menu. In the panel, tell it which frames and how many instances you want and click OK.

Happy Rendering!

# Details
This script launches a number of command-line render instances in the background and captures their output in log files which are saved to the same directory as the Nuke script. You are now free to keep working in the UI and have your renders happen in the background. 

bgNukes is tested in Nuke versions 13, 14, and 15 on Windows. If you try it on Linux or MacOS, please drop me a line and let me know how it went.

# Stop this crazy thing!!!

Sadly, the only way to stop a render in progress is to close Nuke's command prompt window. I realize this is less nifty than it could be.

# Thank you
Thanks go to Nathan Dunsworth. His localRender.py was (and continues to be) an excellent reference.

# LICENSE
Copyright (c) 2010-2024 Tim BOWMAN

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
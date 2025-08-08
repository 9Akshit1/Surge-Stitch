---
title: "Surge Stitch"
author: "Akshit Erukulla"
description: "A portable automatic surgical stitching tool for skin and in the future, tissues/organs."
created_at: "2025-02-01"
---
**TOTAL TIME SPENT: 3hrs**

# June 1st
Although technically, I started this project in 2024 and finished most of it then, I've only seriously locked in for the project today. 
Anyways, today, I worked on the CAD. I wanted to make a compact polished prototype, so I decided to make it 15x11cm for now, but the height is already too much to be "compact". It's mainly because of the electronic components, and that means that I might need to design my own electronic components to lower costs + size.
A few days ago, I decided on focusing on the "novel" stitching method that I had come up with, which was a scuffed servo moto + curved needle + heat rod method. Hypothetically, it should work, although I need to contineu working on thinkign about the alignment of the needles and the melting/string-transfer mechanism's effectiveness. 
Essentially, currently, the CAD has been built for x, y, and z-axis movement. I also implemented the "servo motors" (although they've been cut and stuff, which shows that I need to design my own servos). For the main stitching part, there are 3 arrrays, which are indepedent, and essentially its a needle, then the heat rod, then the needle. Its way too wide right now, so I need to work on that too.
Like I thought, the main issue will likely be minituarization and potentially the sketchiness of the stitching method (but I can always work out those details later).
I found that using a stepper motor is probably the most reasonable choice of action for the x and y axis movements, but even the smallest ones are too big. So, I need to build my own parts 😭, which is going to take a lot of time, since it's hard to just come up with a design that is magically smaller yet similar performance (especially since if it was possible, then people would ahve done it before).
One thing I learned today was about the different railway systems like the V-rail and the MGN9 rail. I also learned about bevel gears which allow for horizontal to vertical rotation, or vice-versa.
Will need to also fix the servo's attachment mounts because they are too big right now. I think if I just finish a basic CAD by the weekend, and then finish the circuit + some of the computer vision code, then I can present it to a professor (I think it was UC Berkely and JHK that are the only competitors?) possibly and ask for their advice. Since, I have the Ingenious grant as well, we should be able to make a IRL prototype, but before that, we definetily need advice.
My goal is to actually implement Surge Stitch into hospitals or somewhere in the real world, because that shows impactful community impact + it leaves my mark on the world (yippee).

https://github.com/9Akshit1/Surge-Stitch/blob/5864a22ebd408ecbbfb1fb9b35c7d2cac03f4a5c/CAD_au7.png

**Time Spent: 3h**

## Turtlebot Follower

### Introduction
a) The end goal of this project is to program a turtlebot with the ability to identify and follow the likeliest red target by pathfinding and controlling the angle and distance from it. </br>
b) This is an interesting project because we had to solve problems such as correctly identifying the red target from its surroundings and be able to follow in real time the target's change in movement. </br>
c) Our project can be applied to real-world robotic applciations that involves tracking and following, such as a robot suitcase. </br>

### Design
a) Design criteria: 
Our turtlebot should process the surroundings to identify the likeliest red quadrilateral as the target and use feedback control to minimize the error between the target's centroid and our centroid in the turtlebot's point of view.  </br>
b) Describe the design you chose.

c) What design choices did you make when you formulated your design? What trade-offs did you have to make?
We chose to implement basic signal processing algorithms to identify the red target in the turtlebot's environment because we could not getting ar_track_alvar to using the turtlebot camera, which required calibration.  The tradeoff that we had to make was to use computer vision and implement an algorithm from scratch to identify the moving red target.  </br>

d) How do these design choices impact how well the project meets design criteria that would be encountered in a real engineering application, such as robustness, durability, and efficiency?
Since we chose to identify a red target, a challenge in the design criteria is accurately identifying the target when there are multiple red objects in the turtlebot's view.  Possible distractors from the red target can arise from different room settings or lighting.  We strived to increase the robustness of our program by 

### Implementation
a) Describe any hardware you used or built. Illustrate with pictures and diagrams.
We attached a red target onto the ridgeback to create a moving target.  A turtlebot was programmed to follow this target.
Insert pic
b) What parts did you use to build your solution?

c) Describe any software you wrote in detail. Illustrate with diagrams, flow charts, and/or other appropriate visuals. This includes launch files, URDFs, etc.
d) How does your complete system work? Describe each step.

### Results
a) How well did your project work? What tasks did it perform? (b) Illustrate with pictures and at least one video.
### Conclusion

### Team
a) Include names and short bios of each member of your project group.
b) Describe the major contributions of each team member.

### Additional materials

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

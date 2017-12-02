## Turtlebot Follower

You can use the [editor on GitHub](https://github.com/cyin3/ee106a/edit/master/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Introduction
a) The end goal of this project is to program a turtlebot with the ability to identify and follow the likeliest red target by pathfinding and controlling the angle and distance from it. </br>
b) This is an interesting project because we had to solve problems such as correctly identifying the red target from its surroundings and be able to follow in real time the target's change in movement. </br>
c) Our project can be applied to real-world robotic applciations that involves tracking and following, such as a robot suitcase. </br>

### Design
a) Design criteria: 
Our turtlebot should process the surroundings to identify the likeliest red quadrilateral as the target and use feedback control to minimize the error between the target's centroid and our centroid in the turtlebot's point of view.  </br>
b) Describe the design you chose.

c) What design choices did you make when you formulated your design? What trade-offs did you have to make?

d) How do these design choices impact how well the project meets design criteria that would be encountered in a real engineering application, such as robustness, durability, and efficiency?

### Implementation
(a) Describe any hardware you used or built. Illustrate with pictures and diagrams.
We attached a red target onto the ridgeback to create a moving target.  A turtlebot was programmed to follow this target.
Insert pic
(b) What parts did you use to build your solution?

(c) Describe any software you wrote in detail. Illustrate with diagrams, flow charts, and/or other appropriate visuals. This includes launch files, URDFs, etc.
(d) How does your complete system work? Describe each step.

### Results
(a) How well did your project work? What tasks did it perform? (b) Illustrate with pictures and at least one video.
### Conclusion

### Team

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

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/cyin3/ee106a/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.

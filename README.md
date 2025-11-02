# Description

The goal is to upload a photo, and then convert it to a matrix of 1x1 Lego pieces (either plates or tiles).

The entire photo should be squared, and could fit various Lego board sizes.

# TODOs
- [X] Build structure with classes
- [X] Transform image to matrix
- [X] Use colors from Lego
- [X] Output a render 
- [X] List necessary pieces
- [X] Add a matrix index on photo border
- [ ] Connect with BrickLink
    - [X] Get colors from BrickLink
    - [X] Get stock from BrickLink for each piece
        - [X] When getting colors from Bricklink, get stock at the same time
        - [X] Do not list colors with no stock
        - [X] Only list solid colors
    - [ ] Make a want list -> so the user can press "Easy Buy" on BrickLink to buy from them
    - [ ] Print price with details
- [ ] Add argument to choose the type of brick used
...
- [ ] Add relief on some images

## What is BrickLink ?
BrickLink is a website where you can buy Lego pieces by unit. This app should build a basket with needed pieces.

# autoset

Tag: `<count><colour><filling><shape>`

* Count: `1`, `2`, `3`
* Colour: `R` (red), `G` (green), `B` (blue)
* Filling: `F` (full), `H` (hatched), `E` (empty)
* Shape: `W` (wave), `D` (diamond), `P` (pill)

Examples:

* `1RFD`: One red filled diamond

## Blender

Run `./generator.sh [--mask <card mask>] <number of images>` to generate a set of images.
The card mask is a regex to match a subset of the cards, e.g. `.[RG]F.` to use any number of Red or Green Filled shapes.

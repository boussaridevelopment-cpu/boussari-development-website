# Project gallery

The gallery retains all 427 project photos. It opens with 23 visually reviewed room or exterior sequences, each showing two or three directly related stages. Extra angles are available beneath the corresponding space. Extra angles and supplied comparisons share one visitor-facing View more photos control, with separate viewer groups. Individual photographs without a confident match remain available under Additional project views.

`assets/gallery.json` is the source of truth. Each `rooms` entry has an explicitly ordered `sequence`, optional `additional` images, and a matching-evidence note. `references` contains individual views; these must not be described as a chronological transformation. Do not infer a room match from the source archive alone. Missing before/during/after stages must not be invented.

After editing the manifest, run:

```sh
python scripts/build-gallery.py
```

The static page uses native details controls, lazy thumbnails, and full-resolution image links. The viewer stays within the chosen short sequence, extra-angle group, or collage group, so it does not jump from a finished primary image back into earlier construction photos. Main rows are left-to-right on desktop and top-to-bottom on mobile.

Existing image filenames remain available for other site pages. Original archives and private review material remain outside this repository. No photos were added or deleted in the room-sequence correction.

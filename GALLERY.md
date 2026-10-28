# Project gallery

The public gallery shows four complete project albums with 298 photographs: townhouse renovation (64), open-plan home (126), curved-stair home (52), and salon renovation (56). Each album runs through original conditions, construction progress and completed work, in that order. Include all distinct photos that can be matched to a complete project, including additional rooms and angles. An individual room does not need its own separate original photograph when its association with the complete project is established; do not invent a room-specific before/after comparison.

`assets/gallery.json` is the approved publication manifest. The legacy `rooms` key now contains one record per whole project, with its ordered `sequence`, source image IDs, completed cover, matching evidence and older link aliases. Evidence stays out of the visitor interface. Source archive order and file dates alone are not evidence of a matching renovation. Within construction, order follows visible progress; it does not assert unavailable capture dates.

Projects without a genuine starting condition or completed result are not published. There are no loose-photo or extra-angle sections: all images belong inside the project's Before, During or After section. Keep supplied comparison images only when they preserve a distinct view unavailable as a separate image, using ordinary descriptive captions. A mixed comparison containing completed work belongs under After. Retain originals and review history outside the site; never relabel unfinished construction as completed work. Existing asset filenames remain available to avoid breaking other pages.

After visually reviewing any changes, run:

```sh
python scripts/build-gallery.py
python scripts/test-gallery.py
```

The builder rejects missing stages, reversed stage order, unsequenced photos, duplicate assets, missing files and missing evidence. These checks protect structure; they do not replace looking at the photographs. Verify that every room has the same architectural features across its stages and that the last photo really shows completed work.

The page is static and readable without JavaScript. Desktop and mobile both show the full Before section, then During, then After, with navigation links to each stage. Images use a responsive grid within each stage. The photo viewer stays inside the selected project's entire ordered sequence and stops at its first and last photograph. Project covers show finished work and link to the full album.

# Project gallery

The public gallery shows four project albums with eleven complete renovation sequences. Each sequence contains a visually matched original condition, construction progress, and completed result, in that order. A main-floor sequence can include the connected living, dining and kitchen areas when captions identify each view.

`assets/gallery.json` is the approved publication manifest. Each room records its ordered `sequence`, source image IDs, matching evidence, and any older link aliases. Evidence stays out of the visitor interface. Source archive order and file dates alone are not evidence of a matching renovation.

Images without a defensible match, a genuine starting condition, or a completed result are not published in the gallery. There are no loose-photo, extra-angle or collage sections. Retain the originals and review history outside the site; do not invent missing stages or relabel construction as the original condition. Existing asset filenames remain available to avoid breaking other pages.

After visually reviewing any changes, run:

```sh
python scripts/build-gallery.py
python scripts/test-gallery.py
```

The builder rejects missing stages, reversed stage order, unsequenced photos, duplicate assets, missing files and missing evidence. These checks protect structure; they do not replace looking at the photographs. Verify that every room has the same architectural features across its stages and that the last photo really shows completed work.

The page is static and readable without JavaScript. Desktop columns and the mobile reading order both run Before → During → After. The photo viewer stays inside the selected room's entire ordered sequence and stops at its first and last photograph. Project covers show finished work and link to the full album.

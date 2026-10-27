# Project gallery

The gallery includes 427 project photos in seven renovation collections. Each collection follows the available stages: before, during renovation, after, then supplied comparison collages. Photos are grouped by visual review; missing stages are not invented.

`assets/gallery.json` is the ordered gallery manifest. Edit a collection's photo list to change its order, then run:

```sh
python scripts/build-gallery.py
```

The generated `projects.html` is static, so every photo remains accessible without JavaScript. The shared viewer follows the same order and stays inside the selected renovation. Thumbnails load lazily; full-resolution WebP files load when opened. Source images were orientation-normalized and exported without embedded camera metadata. Original archives are kept outside this repository.

Existing image filenames remain available for the homepage and service pages. The archive import reuses all 58 existing gallery images and adds 369 images, without repeating those existing images in the gallery.

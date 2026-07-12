# Image Credits

Sample images used in this repo (`assets/sample_images/`) are sourced from Wikimedia Commons under Creative Commons / public-domain-compatible licenses. Candidates were staged in `new_images/` and researched via the Commons API.

## Candidates researched so far (license-verified, not yet finalized)

| Local filename | Wikimedia Commons page | License | Author |
|---|---|---|---|
| `House_sparrow_male_in_Prospect_Park_(53532).jpg` | [File page](https://commons.wikimedia.org/wiki/File:House_sparrow_male_in_Prospect_Park_(53532).jpg) | CC BY-SA 4.0 | Rhododendrites |
| `Man_with_many_pigeons_in_Washington_Square_Park,_New_York.jpg` | [File page](https://commons.wikimedia.org/wiki/File:Man_with_many_pigeons_in_Washington_Square_Park,_New_York.jpg) | CC BY 2.0 | JoeInQueens (Flickr) |
| `Mouse_in_snow.jpg` | [File page](https://commons.wikimedia.org/wiki/File:Mouse_in_snow.jpg) | **CC0** | Alex Kard |
| `Pigeons_uptown.jpg` | [File page](https://commons.wikimedia.org/wiki/File:Pigeons_uptown.jpg) | CC BY 4.0 | צבוע לבנה |
| `Rat_in_NYC_subway_3_(cropped).jpg` | [File page](https://commons.wikimedia.org/wiki/File:Rat_in_NYC_subway_3_(cropped).jpg) | CC BY 2.0 | m01229 (Flickr) |
| `Squirrel_and_girl_at_228_Memorial_Park,_Taipei_20101127.jpg` | [File page](https://commons.wikimedia.org/wiki/File:Squirrel_and_girl_at_228_Memorial_Park,_Taipei_20101127.jpg) | CC BY 2.0 | Yi Chen |
| `Squirrel_in_New_York_-_NYC_-_USA_-_panoramio.jpg` | [File page](https://commons.wikimedia.org/wiki/File:Squirrel_in_New_York_-_NYC_-_USA_-_panoramio.jpg) | CC BY-SA 3.0 | diego_cue (Panoramio, archived) |
| `Stensved_-_mouse.jpg` | [File page](https://commons.wikimedia.org/wiki/File:Stensved_-_mouse.jpg) | CC BY-SA 2.0 | Bo Mertz (Flickr) |
| `pizza_rat.avif` | not a Wikimedia Commons file — provenance/license unverified | ⚠️ unverified | ⚠️ unverified |

## Proposed final picks (NOT yet copied into assets/sample_images/ — pending)

- **01_pigeon.jpg** ← `Man_with_many_pigeons_in_Washington_Square_Park,_New_York.jpg` (CC BY 2.0, JoeInQueens) — strong NYC narrative fit, also contains a person (bonus privacy-mask demo value)
- **02_squirrel.jpg** ← `Squirrel_in_New_York_-_NYC_-_USA_-_panoramio.jpg` (CC BY-SA 3.0, diego_cue) — explicit NYC squirrel
- **03_mouse.jpg** ← `Rat_in_NYC_subway_3_(cropped).jpg` (CC BY 2.0, m01229) — iconic NYC subway rat, thematically strong. **Note for README:** a real rodent photo will likely produce zero detections from `app.py`'s base pipeline (no manual-override mechanism exists there, unlike the web dashboard) since COCO's `mouse` class means a computer-mouse peripheral, not a rodent — this is worth calling out honestly as a teaching moment about pretrained model class definitions, not hidden.
- **04_pedestrians.jpg** ← **not yet found.** None of the 9 staged candidates show a crowded crosswalk/pedestrian scene. Still need to search Wikimedia Commons for a CC0/PD-preferred NYC pedestrian crosswalk photo (the same API-search approach used above works well: `commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srsearch=...`).

## Remaining work (Step 2 onward, not yet done)

- [ ] Find + verify a pedestrians/crosswalk image
- [ ] Resize all 4 finals to ~1024px wide, copy into `assets/sample_images/` with the standard filenames
- [ ] Finalize this file's credit table to match exactly what's copied in (remove candidates not used)
- [ ] Delete `seed_assets.py` and remove all references to it / to `"NYPL demo sample photos"` from every file in the repo
- [ ] Steps 3, 4, 5 of the cleanup plan (repo hygiene, README rewrite, verification) — not started

# Changelog

Dated notes on what changed on this page and why. Newest first.

## 2026-10-02

- **The two repairs of the stability term, measured** (new README section,
  `results/stability_repairs.json`). Both named repairs were scored on the same
  3,000 synthetic communities as the published term. Weighting each species' CV
  by its share of detections, or taking the CV of the pooled stream, makes the
  mean index fall from the first species lost (it took 8 before), and no
  community scores above its intact self with three species gone (31 of 40
  did).
- The cost, also measured. The pooled term loses 9 % of its value half-way
  through the going-quiet scenario where the published term loses 97 %, and
  still reads 0.330 at the most clumped level. Contamination needs 11 and 10
  noise sources instead of 7, which is no protection. With one species at 95 %
  of detections the repaired indices read 0.455 and 0.468 where the published
  one reads 0.000, because that collapse came from the same rarity penalty.
  The index defined on the page is unchanged.
- **Corrected:** the going-quiet Shannon values were printed in the wrong
  order. Steady is 2.686 and most clumped 2.688, not the reverse. The point
  (Shannon cannot see it) stands.
- Noted that 30 % of the index's fall in the going-quiet scenario happens in
  the first of 19 steps, so the clumping axis is not even.
- `tests/test_readme_numbers.py`: eight checks pin the new section, and the
  Shannon row, to the results files.
- The field recorder is described generically; links to related repositories
  use their current names.

## 2026-09-14

- **Species order.** Read level by level, the index rises from 0.724 to 0.742
  when the three rarest species fall silent and only drops below its intact
  value once eight of 24 are gone. Cause: the stability term penalises rarity,
  not burstiness. Earlier claim that richness outweighs it corrected to "end
  to end only". `results/species_loss_levels.json` added.

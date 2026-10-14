# SDP_CH1_presentation — EE499 Team 16

Smart Home Energy Management with Priority-Based Load Control: Report 1 (Problem & Design Requirements).

| File | What it is |
|---|---|
| `EE499_Team16_Presentation_F_v8.pptx` | **Latest deck**: F_v7 with the abnormal-warning card back to icons and the original wording |
| `EE499_Team16_Presentation_F_v7.pptx` | Built from the team's F_v5, with slides 6+7 and 8+9 merged (24 slides) |
| `EE499_Team16_Presentation_F_v5_team.pptx` | Team's F_v5 with their own edits |
| `EE499_Team16_Presentation_F_v6.pptx` | Simple native diagram on slide 8 (now replaced by the merged slide in F_v7) |
| `EE499_Team16_Presentation_F_v5.pptx` | Names and IDs spread evenly over the whole tower |
| `EE499_Team16_Presentation_F_v4.pptx` | F_v3 with smaller, black names and IDs in the opening video |
| `EE499_Team16_Presentation_F_v3.pptx` | F_v2 with the professor's notes applied |
| `EE499_Team16_Presentation_F_v2.pptx` | Team's revision before those notes |
| `EE499_Team16_Presentation_5.pptx` | **Final deck**: 24 slides, timed for about 9 minutes, with speaker notes |
| `EE499_Team16_Presentation_5_preview.pdf` | Quick preview (rendered with substitute fonts; open the .pptx for the real look) |
| `EE499_Team16_Presentation_4.pptx` | Previous version, with the review notes on the slides |
| `media/opening_names_tower.mp4` | Opening video (light city): the tower's windows spell each name and university ID, letter by letter |
| `media/summary_loop.mp4` | Looping summary of the content slides (plays on the last slide) |
| `scripts/` | Scripts that generated the videos and applied the edits |

## Changes from v4
- **Slide 1 is now the video**: a light city where the tower spells each name and ID, then stops. The title, logo, advisor and university sit beside it, so there is no separate title slide.
- **Slides 4–9 merged into 2**: *Where household electricity goes* and *What the single total hides*.
- **Slides 10 + 11 merged and shortened**: the meter's three unanswered questions now map to Cost, Continuity and Safety.
- **Per-appliance slide reworded**: dash list, and V · I · P · kWh · ON/OFF is no longer repeated.
- **Constraints renumbered**: C-02 → C-04 and C-03 → C-02 (so C-04 → C-03). The cards are back in order C-01 … C-06.
- **Engineering standards**: each standard has an icon, and the long GSO title fits.
- **Last slide**: Thank you, plus the looping summary and the priority-control demo, both playing on an infinite loop.
- **Slide numbers**: now live slide-number fields, so they stay correct if slides move.
- **Speaker notes**: a time budget and talking points on every slide.

## Changes F_v2 → F_v3 (professor's notes)
- Opening video: names and IDs are smaller and dark amber.
- New **Problem statement** slide: the full statement with its four parts highlighted and mapped to four cards. It closes the problem section (order 11 → 13 → 12); the slide before it is now titled *Two core problems*.
- "Heavy loads overlap" → "Heavy-demand loads may run at the same time".
- DS-03: the big number is now **120 / 80 %** of baseline (≥ 5 s, ≥ 90 % detected).
- DS-06: **±5 %** is now labelled as cost-estimate error (alerts at 50 · 80 · 100 %).
- Last slide: the priority-control video was stretched; it is now true 16:9 and large, with the key timing figures below it.

## F_v3 → F_v4
- Opening video: names and IDs are now black, and a little smaller than the presentation title.

## F_v4 → F_v5
- Opening video: the three name + ID blocks are spaced evenly over the full height of the tower.

## F_v5 → F_v6
- Slide 8: the reproduced demand-side-management figure is replaced by a simple native diagram (grid limit → smart controller ← user priorities → appliances P1–P4 with ON / SHED). The caption still credits [4].

## Team F_v5 → F_v7
- Slides 6 + 7 → one comparison slide: *Conventional meter* (three questions it can't answer) vs *Per-appliance monitoring* (three short points).
- Slides 8 + 9 → one slide: *Priority-based control* (core, 3 steps) and *Abnormal warning* (supporting, 3 points), with sources [4] and [5].
- 26 → 24 slides; slide numbers re-verified.

## F_v7 → F_v8
- Slide 7, *Abnormal warning* card: icon markers (pulse, bell, check) and the original points — *Deviation from baseline*, *User warning*, *Supports — not replaces — control*.

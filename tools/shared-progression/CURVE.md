# Proposed shared Hero / Hybrid progression

Design preview only; not installed. Class+ remains unchanged. Hero uses levels 1–80; Hybrid adopts the shared values at its current level when selected at level 10 or later.

Approved anchors: level 10 = 115 base health / 190 base mana; level 80 = 7,350 / 4,050. Proposed Hero level-1 anchor: 35 / 75 (rounded reference averages are approximately 34.44 / 76.14).

Method: use a consistent nine-class health average and seven-mana-class average at every level. Exclude Death Knight from the shaping cohort because it has no rows below 55, avoiding a cohort-change discontinuity at 55. The approved level-80 endpoint remains unchanged. For each resource, scale the reference average between anchors separately for levels 1–10 and 10–80:

`value(L) = startValue + (average(L)-average(startLevel)) / (average(endLevel)-average(startLevel)) * (endValue-startValue)`

Revision: keep levels 1–50 unchanged, then stretch the original 60–80 growth shape over levels 50–80. Sample the original curve at `60 + (L-50)*20/30` with linear interpolation, normalize its progress between original levels 60 and 80, and apply that progress between the unchanged level-50 values and approved level-80 values. The first increased gain occurs on reaching level 51. This moves accelerated growth ten levels earlier without increasing the endpoint.

Round to nearest whole point, halves upward. Every base attribute = 20 + level. Total columns include only that baseline Stamina/Intellect; exclude race, Primary Stat selection, equipment, talents and other modifiers.

| Level | Base health | Base mana | Health with baseline Stamina | Mana with baseline Intellect |
|---:|---:|---:|---:|---:|
| 1 | 35 | 75 | 65 | 110 |
| 2 | 43 | 83 | 83 | 133 |
| 3 | 52 | 92 | 102 | 157 |
| 4 | 61 | 102 | 121 | 182 |
| 5 | 71 | 113 | 141 | 208 |
| 6 | 79 | 128 | 159 | 238 |
| 7 | 89 | 141 | 179 | 266 |
| 8 | 97 | 155 | 197 | 295 |
| 9 | 106 | 174 | 216 | 329 |
| 10 | 115 | 190 | 235 | 360 |
| 11 | 124 | 204 | 254 | 389 |
| 12 | 134 | 219 | 274 | 419 |
| 13 | 144 | 239 | 294 | 454 |
| 14 | 152 | 258 | 312 | 488 |
| 15 | 162 | 276 | 332 | 521 |
| 16 | 172 | 301 | 352 | 561 |
| 17 | 181 | 319 | 371 | 594 |
| 18 | 194 | 340 | 394 | 630 |
| 19 | 206 | 366 | 416 | 671 |
| 20 | 219 | 389 | 439 | 709 |
| 21 | 231 | 410 | 461 | 745 |
| 22 | 245 | 437 | 485 | 787 |
| 23 | 261 | 463 | 511 | 828 |
| 24 | 276 | 490 | 536 | 870 |
| 25 | 292 | 518 | 562 | 913 |
| 26 | 310 | 549 | 590 | 959 |
| 27 | 330 | 574 | 620 | 999 |
| 28 | 350 | 606 | 650 | 1,046 |
| 29 | 368 | 634 | 678 | 1,089 |
| 30 | 392 | 663 | 712 | 1,133 |
| 31 | 413 | 691 | 743 | 1,176 |
| 32 | 434 | 722 | 774 | 1,222 |
| 33 | 461 | 756 | 811 | 1,271 |
| 34 | 485 | 778 | 845 | 1,308 |
| 35 | 511 | 807 | 881 | 1,352 |
| 36 | 535 | 832 | 915 | 1,392 |
| 37 | 563 | 865 | 953 | 1,440 |
| 38 | 592 | 894 | 992 | 1,484 |
| 39 | 622 | 916 | 1,032 | 1,521 |
| 40 | 653 | 945 | 1,073 | 1,565 |
| 41 | 683 | 972 | 1,113 | 1,607 |
| 42 | 716 | 998 | 1,156 | 1,648 |
| 43 | 750 | 1,025 | 1,200 | 1,690 |
| 44 | 785 | 1,054 | 1,245 | 1,734 |
| 45 | 821 | 1,077 | 1,291 | 1,772 |
| 46 | 857 | 1,103 | 1,337 | 1,813 |
| 47 | 895 | 1,128 | 1,385 | 1,853 |
| 48 | 934 | 1,150 | 1,434 | 1,890 |
| 49 | 970 | 1,177 | 1,480 | 1,932 |
| 50 | 1,015 | 1,197 | 1,535 | 1,967 |
| 51 | 1,134 | 1,292 | 1,664 | 2,077 |
| 52 | 1,260 | 1,387 | 1,800 | 2,187 |
| 53 | 1,393 | 1,483 | 1,943 | 2,298 |
| 54 | 1,530 | 1,578 | 2,090 | 2,408 |
| 55 | 1,671 | 1,673 | 2,241 | 2,518 |
| 56 | 1,816 | 1,767 | 2,396 | 2,627 |
| 57 | 1,966 | 1,863 | 2,556 | 2,738 |
| 58 | 2,120 | 1,958 | 2,720 | 2,848 |
| 59 | 2,279 | 2,053 | 2,889 | 2,958 |
| 60 | 2,446 | 2,148 | 3,066 | 3,068 |
| 61 | 2,616 | 2,243 | 3,246 | 3,178 |
| 62 | 2,791 | 2,338 | 3,431 | 3,288 |
| 63 | 2,971 | 2,433 | 3,621 | 3,398 |
| 64 | 3,156 | 2,529 | 3,816 | 3,509 |
| 65 | 3,344 | 2,624 | 4,014 | 3,619 |
| 66 | 3,535 | 2,718 | 4,215 | 3,728 |
| 67 | 3,733 | 2,814 | 4,423 | 3,839 |
| 68 | 3,936 | 2,909 | 4,636 | 3,949 |
| 69 | 4,156 | 3,004 | 4,866 | 4,059 |
| 70 | 4,384 | 3,099 | 5,104 | 4,169 |
| 71 | 4,619 | 3,194 | 5,349 | 4,279 |
| 72 | 4,872 | 3,289 | 5,612 | 4,389 |
| 73 | 5,134 | 3,385 | 5,884 | 4,500 |
| 74 | 5,406 | 3,480 | 6,166 | 4,610 |
| 75 | 5,697 | 3,575 | 6,467 | 4,720 |
| 76 | 5,999 | 3,669 | 6,779 | 4,829 |
| 77 | 6,311 | 3,764 | 7,101 | 4,939 |
| 78 | 6,646 | 3,860 | 7,446 | 5,050 |
| 79 | 6,993 | 3,955 | 7,803 | 5,160 |
| 80 | 7,350 | 4,050 | 8,170 | 5,270 |

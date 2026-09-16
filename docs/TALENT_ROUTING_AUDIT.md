# Talent routing audit — 0.26.0

Checked 829 catalogue talent positions and prerequisite IDs against the exported stock Talent.dbc. Two orphan prerequisite references were intentionally omitted in the catalogue: talent 1756 references missing talent 1409; talent 1993 references missing talent 1994. Neither prerequisite exists in the rendered stock class trees. These are not drawn as fabricated connections. All 829 row/column positions match; all other prerequisite IDs match.

The shared renderer now adapts stock TalentFrameBase.lua routing and texture-coordinate selection, including blocked diagonal routes, corners and junctions. Automated checks cover all 30 class trees and 122 dependency links, both with zero ranks and with full prerequisite ranks. Each link emits a target-owned arrowhead in the receiving button's OVERLAY layer, sublevel 7. Shafts remain below buttons. No per-class arrow offsets remain.

Tests validate data, routing execution, arrow counts and active/inactive atlas state. They do not substitute for in-game visual rendering. New NativeTalentRoutes.lua is loaded by the addon TOC; fully restart the client after installing this version.

"""The move plates' text for Find one by eye: site/moves/ stills, and src/moves.json for Actionary."""
import json, os
from PIL import Image
ALT = {
 'halve': 'A bar is cut in two again and again, keeping one half each time.',
 'ratchet': 'A row of tall bars counts down until only stubs are left.',
 'alternate': 'Solid and hatched stripes swap places on a fixed beat.',
 'saturate': 'Scattered dots multiply until the square is entirely white.',
 'sequence': 'Bars of different heights swap places until they rise in order.',
 'classify': 'Mixed circles, squares and triangles sort themselves into three columns.',
 'replicate': 'A zigzag on the left is copied line by line on the right.',
 'interrupt': 'A wave is drawn from left to right, stopped by a line, then carried on.',
 'recall': 'An outline disappears, then is redrawn slightly differently.',
 'roam': 'One thick line stays still while thin lines wander around it.',
 'reserve': 'A grid fills up while its last two rows stay empty.',
 'dissolve_and_rebuild': 'A square crumbles to dust and the dust forms a circle.',
 'find_the_keystone': 'Blocks are lifted out one at a time until one brings the wall down.',
 'join_through_a_third': 'Two blocks stay still while a third piece drops between them and joins them.',
 'exchange': 'A circle and a square trade places.',
 'hand_over': 'One figure passes a small block to another and walks away.',
 'leave_one_out': 'A row of bars with a different one missing each time.',
 'hedge': 'Three lines start out, two stop, and one carries on.',
 'scout': 'A bar extends in doubling steps until it breaks.',
 'leave_open': 'A wire cube flips between two ways of being seen.',
 'build_in_layers': 'A coarse image sharpens in stages into a figure.',
 'load_and_rest': 'A press rises and falls on a fixed rhythm, with rests between.',
 'plant': 'A small dot sits unnoticed until a figure reaches it, and then it bursts.',
 'pull': 'Items on a shelf go missing, and only the gap is refilled.',
 'keep_a_way_home': 'A dotted line loops far out and swings back to where it started.',
 'triangulate': 'Three lines from three corners meet at one point.',
 'raise_the_cost': 'A small block climbs steps that get taller each time.',
 'clear_and_refill': 'One field in a grid is blanked, then filled with something new.',
 'delay': 'A sealed box sinks into the ground while a bar counts time above.',
 'interlock': 'Three overlapping circles, each sharing a dot with the others.',
 'share_and_keep_apart': 'Three hatchings overlap on one surface, then each shows alone.',
 'breed': 'One blob is copied, changing slightly at every step.',
 'calibrate': 'A line drifts away from its mark and is pulled back at fixed points.',
 'allow_a_margin': 'Dots inside a band stay put; the ones outside are moved in.',
 'favour_the_rare': 'Tall bars shrink and short bars grow until they nearly match.',
 'archive': 'A grid of small squares disappears until only three are left.',
 'cut_the_beaten': 'Points on a graph drop away until only the best on both counts stay.',
 'leave_no_winner': 'Three circles in a ring, each beating the next.',
 'suspend_the_rules': 'Dots march in order, except inside a ring, where they wander.',
 'feed_in_oddities': 'Squares pass on a belt, with one triangle among them.',
 'watch_for_clashes': 'Lines cross and part freely between two fixed banks.',
}
KEEP = {'saturate': .55, 'leave_open': 0, 'alternate': 0}
os.makedirs('site/moves', exist_ok=True)
out = []
for k, alt in ALT.items():
    p = f'site/moves/{k}.gif'
    im = Image.open(p)
    n = im.n_frames
    im.seek(int((n - 1) * KEEP.get(k, 1)))
    im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=8).save(f'site/moves/{k}-still.png', optimize=True)
    name = ' '.join(w.capitalize() for w in k.split('_'))
    out.append({'slug': k.replace('_', '-'), 'name': name, 'file': k, 'alt': alt})
json.dump(out, open('src/moves.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out))

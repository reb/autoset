import bpy, bpy_extras
import sys
import random
import re
import math
from PIL import Image, ImageFilter
import numpy as np
from itertools import combinations
import argparse


DIAGONAL = math.sqrt(1 + 0.647 ** 2)
CARD_SPREAD = 3
BLOCKER_SPREAD = 8


def intersect_simple(a, b):
    '''
    Super simple intersection detection that just checks that the smallest enclosing circles
    of the two cards do not intersect.
    '''
    distance = math.sqrt((a.location[0] - b.location[0]) ** 2 + (a.location[1] - b.location[1]) ** 2)
    return distance < DIAGONAL


def vertex_to_xy(vertex, matrix_world):
    world_vertex = matrix_world * vertex.co
    return [world_vertex[0], world_vertex[1]]


def intersect_projection(a, b):
    '''
    Return True and the MPV if the shapes collide. Otherwise, return False and
    None.

    p1 and p2 are lists of ordered pairs, the vertices of the polygons in the
    counterclockwise direction.
    '''
    
    p1 = [np.array(vertex_to_xy(a.data.vertices[v], a.matrix_world), 'float64') for v in a.data.polygons[0].vertices]
    p2 = [np.array(vertex_to_xy(b.data.vertices[v], b.matrix_world), 'float64') for v in b.data.polygons[0].vertices]

    edges = edges_of(p1)
    edges += edges_of(p2)
    orthogonals = [orthogonal(e) for e in edges]

    push_vectors = []
    for o in orthogonals:
        separates, pv = is_separating_axis(o, p1, p2)

        if separates:
            # they do not collide and there is no push vector
            return False
        else:
            push_vectors.append(pv)

    # they do collide and the push_vector with the smallest length is the MPV
    mpv =  min(push_vectors, key=(lambda v: np.dot(v, v)))

    # assert mpv pushes p1 away from p2
    d = centers_displacement(p1, p2) # direction from p1 to p2
    if np.dot(d, mpv) > 0: # if it's the same direction, then invert
        mpv = -mpv

    return True


def centers_displacement(p1, p2):
    """
    Return the displacement between the geometric center of p1 and p2.
    """
    # geometric center
    c1 = np.mean(np.array(p1), axis=0)
    c2 = np.mean(np.array(p2), axis=0)
    return c2 - c1


def edges_of(vertices):
    edges = []
    N = len(vertices)
    for i in range(N):
        edge = vertices[(i + 1) % N] - vertices[i]
        edges.append(edge)
    return edges


def orthogonal(v):
    """
    Return a 90 degree clockwise rotation of the vector v.
    """
    return np.array([-v[1], v[0]])


def is_separating_axis(o, p1, p2):
    """
    Return True and the push vector if o is a separating axis of p1 and p2.
    Otherwise, return False and None.
    """
    min1, max1 = float('+inf'), float('-inf')
    min2, max2 = float('+inf'), float('-inf')

    for v in p1:
        projection = np.dot(v, o)

        min1 = min(min1, projection)
        max1 = max(max1, projection)

    for v in p2:
        projection = np.dot(v, o)

        min2 = min(min2, projection)
        max2 = max(max2, projection)

    if max1 >= min2 and max2 >= min1:
        d = min(max2 - min1, max1 - min2)
        # push a bit more than needed so the shapes do not overlap in future
        # tests due to float precision
        d_over_o_squared = d/np.dot(o, o) + 1e-10
        pv = d_over_o_squared*o
        return False, pv
    else:
        return True, None


def bounding_box(card, camera):
    screen_vertices = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, camera, card.matrix_world * vertex.co) for vertex in card.data.vertices]
    xs = sorted([screen_vertex[0] for screen_vertex in screen_vertices])
    ys = sorted([screen_vertex[1] for screen_vertex in screen_vertices])
    return [(xs[1], 1 - ys[2]), (xs[2], 1 - ys[1])]


def cap(number):
    if (number < 0):
        return 0
    if (number > 1):
        return 1
    return number


def point_to_str(point):
    x, y = point
    return f'{round(cap(x), 2)},{round(cap(y), 2)}'


def move_to_random_position(object, spread, z):
    object.location = [random.random() * spread - (spread / 2), random.random() * spread - (spread / 2), z]


def move_blockers(blockers):
    for blocker in blockers:
        move_to_random_position(blocker, BLOCKER_SPREAD, 6)


def generate(number_of_images, card_mask, render_images):
    random.seed(1337)

    cardsGroup = [card for card in bpy.data.objects if re.match('[0-9][RGB][FHE][WPD]', card.name)]
    for card in cardsGroup:
        card.hide_render = True
    print(f'total cards: {len(cardsGroup)}')

    subset = [card for card in cardsGroup if re.match(card_mask, card.name)]
    print(f'using cards: {len(subset)}')

    blockers = [blocker for blocker in bpy.data.objects if re.match('Blocker.*', blocker.name)]
    print(f'total blockers: {len(blockers)}')

    with open('tags.csv', 'w') as tags_csv, open('bbs.csv', 'w') as bbs_csv:
        for i in range(number_of_images):
            print(f'generating image {i}')
            bpy.data.worlds['World'].light_settings.environment_energy = random.random() / 2
            bpy.data.objects.get('Plane').active_material.diffuse_color = (random.random(), random.random(), random.random())
            
            move_blockers(blockers)

            for card in subset:
                card.hide_render = False
                card.rotation_euler = [0, 0, 0]
                move_to_random_position(card, CARD_SPREAD, 0.01)
                card.active_material.specular_intensity = random.random()
             
            bpy.context.scene.update()
                
            random.shuffle(subset)
            for (a, b) in combinations(subset, 2):
                if not a.hide_render and not b.hide_render:
                    if intersect_projection(a, b):
                        if not b.hide_render:
                            a.hide_render = True
            
            filename = f'{i:04d}.jpg'  
            blur = random.randint(1, 2)

            if render_images:
                bpy.context.scene.render.filepath = f'training-set/{filename}'
                bpy.ops.render.render(write_still=True)           
                Image.open(bpy.context.scene.render.filepath).filter(ImageFilter.GaussianBlur(blur)).save(bpy.context.scene.render.filepath)
            
            visible_cards = [card for card in subset if not card.hide_render]

            tags = ','.join([card.name for card in visible_cards])
            tags_csv.write(f'gs://autoset-vcm/generated-blender/images/{filename},{tags}\n')

            camera = bpy.data.objects.get('Camera')
            for card in visible_cards:
                top_left, bottom_right = bounding_box(card, camera)
                bb = f'{point_to_str(top_left)},,,{point_to_str(bottom_right)},,'
                bbs_csv.write(f'UNASSIGNED,gs://autoset-vcm/generated-blender/images/{filename},{card.name},{bb}\n')

            bpy.ops.wm.save_as_mainfile(filepath=f'./debug-{filename}.blend')


parser = argparse.ArgumentParser(description = 'Generate awesome test data!', prog='./generator.sh')
parser.add_argument('images', type=int, help='Number of images to generate')
parser.add_argument('-m', '--mask', default='....', help='Mask for the cards to use (e.g. ".RFD" for any number of Red Filled Diamonds)')
parser.add_argument('-n', '--no-render', action='store_true', help='Mask for the cards to use (e.g. ".RFD" for any number of Red Filled Diamonds)')

allArgs = sys.argv
myArgs = parser.parse_args(allArgs[allArgs.index("--") + 1:])

generate(myArgs.images, myArgs.mask, not myArgs.no_render)

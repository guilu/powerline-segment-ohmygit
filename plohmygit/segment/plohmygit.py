# vim:fileencoding=utf-8:noet

from __future__ import absolute_import
from subprocess import Popen, PIPE
from powerline.theme import requires_segment_info

import os
import subprocess

icon = {
    'staged': ' ',
    'added':  ' ',
    'modified': ' ',
    'modified_cached': ' ',
    'renamed':  '☁',
    'deleted':  ' ',
    'deleted_cached':  ' ',
    'untracked': ' '
}

@requires_segment_info
def plohmygit(pl, segment_info,use_path_separator=False):

    branch = None

    has_modified = 0
    has_modified_cached = 0
    has_staged = 0
    has_deleted = 0
    has_deleted_cached = 0
    has_untracked = 0
    has_renamed = 0

    ret = []
    draw_inner_divider = not use_path_separator

    gitsym =  Popen(['git','branch','--l'],stdout=PIPE, stderr=PIPE)
    branch, error = gitsym.communicate()

    error_string = error.decode('utf-8')

    if 'fatal: Not a git repository' in error_string:
        return None

    lineas = Popen(['git','status','--porcelain'],stdout=PIPE).communicate()[0].splitlines()

    for line in lineas:
        #la linea empieza por:
        #.M has_modified
        #M has_modified_cached
        #A has_staged
        #.D has_deleted
        #D has_deleted_cached
        if line.startswith('A'):
            has_staged += 1
            if line.startswith('AM'):
                has_modified +=1
        if line.startswith(' M'):
            has_modified += 1
        if line.startswith('M'):
            has_modified_cached += 1
        if line.startswith('R'):
            has_renamed += 1
            if line.startswith('RM'):
                has_modified +=1
        if line.startswith('D'):
            has_deleted += 1
        if line.startswith(' D'):
            has_deleted_cached += 1
        if line.startswith('??'):
            has_untracked += 1

    if has_staged > 0:
        ret.append({
            'contents': "%s%s" % (icon['staged'],has_staged),
            'highlight_group': "staged",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_modified > 0:
        ret.append({
            'contents': "%s%s" % (icon['modified'],has_modified),
            'highlight_group': "modified",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_modified_cached > 0:
        ret.append({
            'contents': "%s%s" % (icon['modified_cached'],has_modified_cached),
            'highlight_group': "modified_cached",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_renamed > 0:
        ret.append({
            'contents': "%s%s" % (icon['renamed'],has_renamed),
            'highlight_group': "renamed",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_deleted > 0:
        ret.append({
            'contents': "%s%s" % (icon['deleted'],has_deleted),
            'highlight_group': "deleted",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_deleted_cached > 0:
        ret.append({
            'contents': "%s%s" % (icon['deleted_cached'],has_deleted_cached),
            'highlight_group': "deleted_cached",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_untracked > 0:
        ret.append({
            'contents': "%s%s" % (icon['untracked'],has_untracked),
            'highlight_group': "untracked",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    return ret


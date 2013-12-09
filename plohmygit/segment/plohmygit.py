# vim:fileencoding=utf-8:noet

from __future__ import absolute_import
from subprocess import Popen, PIPE
from powerline.theme import requires_segment_info

import os
import subprocess

icon_default = {
    'branch': ' ',
    'staged': ' ',
    'added':  ' ',
    'modified': ' ',
    'modified_cached': ' ',
    'renamed':  ' ',
    'deleted':  ' ',
    'deleted_cached':  ' ',
    'untracked': ' ',
    'tag': ' ',
    'stashed': ' ',
    'behind': ' ',
    'ahead': ' ',
    'diverged': ' ',
    'upstream': '  ',
    'will_merge': ' ',
    'will_rebase': ' ',
    'can_fast_forward': ' ',
    'should_push': ' ',
    'deatached_head': ' '
}

@requires_segment_info
def plohmygit(pl, segment_info,use_path_separator=False,icons=[]):

    current_branch = ''
    has_tag = False
    has_stashed = False
    has_diverged = False
    has_upstream = False
    can_fast_forward = False
    deatached_head = False
    just_init = False
    will_rebase = False
    will_merge = False

    has_modified = 0
    has_modified_cached = 0
    has_staged = 0
    has_deleted = 0
    has_deleted_cached = 0
    has_untracked = 0
    has_renamed = 0
    commits_ahead = 0
    commits_behind = 0


    ret = []
    draw_inner_divider = use_path_separator

    #iconos por defecto si no vienen
    if len(icons) == 0:
    	icons = icon_default

    #first we are going to check if it's a git repo....
    current_commit_line = Popen(['git', 'rev-parse', 'HEAD'], stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
    if len(current_commit_line) > 0:
        current_commit_hash = current_commit_line[0]
    else:
        #we are done
        return None

    ''' we are in a git repo
        Let's take a look over here...
    '''
    current_branch_line = Popen(['git', 'rev-parse','--abbrev-ref', 'HEAD'], stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
    if len(current_branch_line) > 0:
        current_branch = current_branch_line[0]

    if current_branch == 'HEAD':
        deatached_head = True

    hay_algun_log_line = Popen(['git', 'log','--pretty=oneline', '-n1'], stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
    if len(hay_algun_log_line) == 0:
        just_init = True

    upstream_line = Popen(['git', 'rev-parse', '--symbolic-full-name','--abbrev-ref','@{u}'], stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
    if len(upstream_line) > 0:
        has_upstream = True
        upstream = upstream_line[0]

    tag_at_current_commit_line = Popen(['git', 'describe', '--exact-match','--tags',current_commit_hash], stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
    if len(tag_at_current_commit_line) > 0:
        has_tag = True
        tag_at_current_commit = tag_at_current_commit_line[0]

    if has_upstream:
        commits_describe_line = Popen(['git', 'log', '--pretty=oneline','--no-color','--topo-order','--left-right','%s%s%s' % (current_commit_hash,'...',upstream)], stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
        #ahora tendría que hacer un grep para contar los commits ahead o commits behind, pero como no sé pasar la instruccion a Popen lo voy a hacer contando las lineas con startswith
        if commits_describe_line > 0:
            for line in commits_describe_line:
                if line.startswith('<'):
                    commits_ahead += 1
                if line.startswith('>'):
                    commits_behind += 1
    if commits_ahead > 0 and commits_behind > 0:
        has_diverged = True
    if commits_ahead == 0 and commits_behind > 0:
        can_fast_forward = True

    will_rebase_line = Popen(['git', 'config', '--get','%s.%s.%s' % ('branch',current_branch,'rebase')], stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
    if len(will_rebase_line) > 0:
        will_rebase = will_rebase_line[0]

    number_of_stashes = 0
    #stashed files
    stashed_lines = Popen(['git','stash','list'],stdout=PIPE,stderr=PIPE).communicate()[0].splitlines()
    if len(stashed_lines) > 0:
        has_stashed = True
        for line in stashed_lines:
            number_of_stashes += 1

    lineas = Popen(['git', 'status', '--porcelain'],stdout=PIPE).communicate()[0].splitlines()

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
			has_staged += 1
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


    dirty = has_staged + has_modified + has_modified_cached + has_renamed + has_deleted + has_deleted_cached + has_untracked

    if deatached_head:
        if just_init:
            current_branch = 'deatached'
        else:
            current_branch = current_commit_hash[:7]
        ret.append({
            'contents': "%s%s" % (icons['deatached_head'],current_branch),
            'highlight_group':   'deatached_head',
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
            })

    else:
        ret.append({
            'contents': "%s%s" % (icons['branch'],current_branch),
            'highlight_group':   'branch_dirty' if dirty else 'branch_clean',
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })

    if has_upstream:
        if will_rebase:
            ret.append({
                'contents': "%s%s %s" % (icons['upstream'],upstream,icons['will_rebase']),
                'highlight_group':   'upstream',
                'divider_highlight_group': 'cwd:divider',
                'draw_inner_divider': draw_inner_divider,
            })
        else:
            ret.append({
                'contents': "%s%s %s" % (icons['upstream'],upstream,icons['will_merge']),
                'highlight_group':   'upstream',
                'divider_highlight_group': 'cwd:divider',
                'draw_inner_divider': draw_inner_divider,
            })

        if has_diverged:
            ret.append({
                'contents': "-%s %s+%s" % (commits_behind,icons['diverged'],commits_ahead),
                'highlight_group':   "diverged",
                'divider_highlight_group': 'upstream',
                'draw_inner_divider': draw_inner_divider,
            })
        else:
            if commits_behind > 0:
                ret.append({
                    'contents': "%s-%s" % (icons['can_fast_forward'],commits_behind),
                    'highlight_group':   "commits:behind",
                    'divider_highlight_group': 'cwd:divider',
                    'draw_inner_divider': draw_inner_divider,
                })
            if commits_ahead > 0:
                ret.append({
                'contents': "%s+%s" % (icons['should_push'],commits_ahead),
                'highlight_group':   "commits:ahead",
                'divider_highlight_group': 'cwd:divider',
                'draw_inner_divider': draw_inner_divider,
            })

    if has_staged > 0:
        ret.append({
            'contents': "%s%s" % (icons['staged'],has_staged),
            'highlight_group': "staged",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })

    if has_modified > 0:
        ret.append({
            'contents': "%s%s" % (icons['modified'],has_modified),
            'highlight_group': "modified",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })


    if has_modified_cached > 0:
        ret.append({
            'contents': "%s%s" % (icons['modified_cached'],has_modified_cached),
            'highlight_group': "modified_cached",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_renamed > 0:
        ret.append({
            'contents': "%s%s" % (icons['renamed'],has_renamed),
            'highlight_group': "renamed",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_deleted > 0:
        ret.append({
            'contents': "%s%s" % (icons['deleted'],has_deleted),
            'highlight_group': "deleted",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_deleted_cached > 0:
        ret.append({
            'contents': "%s%s" % (icons['deleted_cached'],has_deleted_cached),
            'highlight_group': "deleted_cached",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_untracked > 0:
        ret.append({
            'contents': "%s%s" % (icons['untracked'],has_untracked),
            'highlight_group': "untracked",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_tag:
        ret.append({
            'contents': "%s%s" % (icons['tag'],tag_at_current_commit),
            'highlight_group': "tagged",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })
    if has_stashed:
        ret.append({
            'contents': "%s%s" % (icons['stashed'],number_of_stashes),
            'highlight_group': "stashed",
            'divider_highlight_group': 'cwd:divider',
            'draw_inner_divider': draw_inner_divider,
        })

    return ret


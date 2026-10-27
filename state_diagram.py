import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.set_xlim(0, 18); ax.set_ylim(-0.8, 6.2); ax.axis('off')

def box(x, name, c):
    ax.add_patch(FancyBboxPatch((x - 1.1, 2.9), 2.2, 1.2, boxstyle='round,pad=0.1', fc=c, ec='black'))
    ax.text(x, 3.5, name, ha='center', va='center', fontsize=16)

def arrow(p, q, rad):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=18,
                                 connectionstyle=f'arc3,rad={rad}'))

box(3, 'RUN', '#d5f5d5'); box(9, 'IDLE', '#cfe8ff'); box(15, 'SLEEP', '#e0d4ff')
ax.add_patch(Circle((9, 5.4), 0.25, color='black'))
ax.text(9.6, 5.4, 'start', va='center')
arrow((9, 5.15), (9, 4.3), 0)

# IDLE <-> RUN
arrow((7.7, 3.95), (4.3, 3.95), 0.3)
ax.text(6, 5.25, 'right_down / left_down\n[방향키 누름]', ha='center', va='center')
arrow((4.3, 3.05), (7.7, 3.05), 0.3)
ax.text(6, 1.75, 'stop_run\n[방향키 뗌]', ha='center', va='center')
# IDLE <-> SLEEP
arrow((10.3, 3.95), (13.7, 3.95), -0.3)
ax.text(12, 5.25, 'time_out\n[5초 동안 입력 없음]', ha='center', va='center')
arrow((13.7, 3.05), (10.3, 3.05), -0.3)
ax.text(12, 1.75, 'space_down\n[SPACE 키]', ha='center', va='center')
arrow((14.5, 2.85), (3.5, 2.85), -0.55)
ax.text(9, -0.4, 'right_down / left_down [SLEEP 중 방향키 누름]', ha='center', fontsize=10, color='#a02020')
plt.savefig('boy_state_diagram.png', dpi=120, bbox_inches='tight')

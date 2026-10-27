import math
from pico2d import (load_image, get_time, SDL_KEYDOWN, SDL_KEYUP,
                    SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_a)
from transitions.extensions import GraphMachine

SLEEP_TIME = 5.0
RUN_SPEED = 5
AUTORUN_TIME = 5.0
AUTORUN_SPEED = 15
AUTORUN_SCALE = 2


class AutoRun:
    def __init__(self, boy):
        self.boy = boy
        self.start_time = 0.0

    def enter(self):
        self.start_time = get_time()

    def exit(self):
        pass

    def do(self):
        boy = self.boy
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.face_dir * AUTORUN_SPEED

    def is_timeout(self):
        return get_time() - self.start_time >= AUTORUN_TIME

    def draw(self):
        pass


class Boy:
    states = ['IDLE', 'RUN', 'SLEEP', 'AUTORUN']

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.idle_start_time = get_time()
        self.right_held = False
        self.left_held = False
        self.autorun = AutoRun(self)

        self.machine = GraphMachine(
            model=self, states=Boy.states, initial='IDLE',
            auto_transitions=False, show_conditions=True
        )
        self.machine.add_transition(
            'time_out', 'IDLE', 'SLEEP', conditions='is_sleep_time')
        self.machine.add_transition(
            'space_down', 'SLEEP', 'IDLE', after='reset_idle_timer')
        self.machine.add_transition(
            'start_run', ['IDLE', 'SLEEP', 'AUTORUN'], 'RUN')
        self.machine.add_transition(
            'a_down', ['IDLE', 'RUN', 'SLEEP'], 'AUTORUN',
            after='autorun_enter')
        self.machine.add_transition(
            'autorun_timeout', 'AUTORUN', 'IDLE',
            conditions='autorun_expired', after='reset_idle_timer')
        self.machine.add_transition(
            'stop_run', 'RUN', 'IDLE', after='reset_idle_timer')

    def autorun_enter(self):
        self.autorun.enter()

    def autorun_expired(self):
        return self.autorun.is_timeout()

    def is_sleep_time(self):
        return get_time() - self.idle_start_time >= SLEEP_TIME

    def reset_idle_timer(self):
        self.idle_start_time = get_time()

    def move_dir(self):
        return int(self.right_held) - int(self.left_held)

    def handle_event(self, event):
        if event.type not in (SDL_KEYDOWN, SDL_KEYUP):
            return
        down = event.type == SDL_KEYDOWN
        if event.key == SDLK_RIGHT:
            self.right_held = down
        elif event.key == SDLK_LEFT:
            self.left_held = down

        if down and event.key == SDLK_a and self.state != 'AUTORUN':
            self.a_down()
            return

        if self.state == 'SLEEP':
            # 스페이스바는 IDLE로, 방향키는 바로 RUN으로 깨움
            if down and event.key == SDLK_SPACE:
                self.space_down()
            elif down and self.move_dir() != 0:
                self.face_dir = self.move_dir()
                self.start_run()
            return

        d = self.move_dir()
        if d != 0:
            self.face_dir = d
            if self.state == 'IDLE':
                self.start_run()
        elif self.state == 'RUN':
            self.stop_run()
        elif down:
            # IDLE 중 다른 입력이 있으면 "아무것도 하지 않은" 시간이 초기화됨
            self.reset_idle_timer()

    def update(self):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            self.time_out()
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x = max(0, min(800, self.x + self.face_dir * RUN_SPEED))
        elif self.state == 'AUTORUN':
            self.autorun.do()

    def draw(self):
        if self.state == 'SLEEP':
            # 서 있는 모습을 90도 눕혀서 누워있는 모습으로 표현
            angle = math.pi / 2 if self.face_dir == 1 else -math.pi / 2
            row = 300 if self.face_dir == 1 else 200
            self.image.clip_composite_draw(
                0, row, 100, 100, angle, '', self.x, self.y - 30, 100, 100)
        elif self.state == 'RUN':
            row = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
        elif self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)

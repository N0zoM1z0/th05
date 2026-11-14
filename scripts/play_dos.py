#!/usr/bin/env python3
"""Boot TH05 (original or rebuilt products) in a disposable HDI under DOSBox-X.

Run under xvfb-run. The image, captures, saves and emulator state stay in a
fresh .analysis/runtime directory. Adapted from TH03's play_th03_dos.py.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ("OP.EXE", "MAIN.EXE", "MAINE.EXE", "ZUN.COM")
PROFILE = '''[sdl]
fullscreen=false
output=surface
videodriver=x11
autolock=false
waitonerror=false
priority=normal,normal
showmenu=false
[dosbox]
machine=pc98
memsize=16
fastbioslogo=true
startbanner=false
synchronize time=false
working directory option=noprompt
quit warning=false
[pc98]
pc-98 fm board=board86c
pc-98 sound bios=false
pc-98 load sound bios rom file=false
pc-98 enable 256-color=false
pc-98 enable 16-color=true
pc-98 enable grcg=true
pc-98 enable egc=true
pc-98 start gdc at 5mhz=false
pc-98 timer always cycles=true
pc-98 timer master frequency=5
pc-98 force ibm keyboard layout=false
pc-98 force JIS keyboard layout=false
pc-98 try font rom=false
[cpu]
core=normal
cputype=pentium
fpu=true
cycles=fixed {cycles}
turbo=false
[mixer]
nosound={nosound}
[midi]
mpu401=none
mididevice=none
[dos]
keyboardlayout=none
'''


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(value, message):
    if not value:
        raise ValueError(message)


def timed(spec):
    name, second = spec.rsplit('@', 1)
    need(bool(re.fullmatch(r'[A-Za-z0-9_+:.-]+', name)), 'invalid event/checkpoint name')
    return float(second), name


class Image:
    def __init__(self, path, offset):
        self.path, self.offset = path, offset

    def run(self, operation, *args):
        return subprocess.check_output([operation, '-i', f'{self.path}@@{self.offset}', *args],
                                       env=os.environ | {'MTOOLS_SKIP_CHECK': '1'}, stderr=subprocess.PIPE)

    def read(self, name):
        return self.run('mtype', '::/' + name)

    def write(self, name, data, scratch):
        scratch.write_bytes(data)
        self.run('mcopy', '-o', str(scratch), '::/' + name)
        need(self.read(name) == data, 'complete installed readback: ' + name)


def prepare(args, output, config):
    pin = config['image']
    original = ROOT / pin['path']
    need(sha(original.read_bytes()) == pin['sha256'], 'pinned runtime HDI identity')
    image_path = output / 'execution.hdi'
    image_path.write_bytes(original.read_bytes())
    image = Image(image_path, pin['fat_partition_offset'])
    game = pin['game_directory']
    targets = {t['dos_path'].split('/')[-1]: t for t in tomllib.loads(
        (ROOT / 'config/targets.toml').read_text())['artifacts'] if t['game'] == 'th05'}
    scratch = output / 'stage.bin'
    products = {}
    for name in PRODUCTS:
        target = targets[name]
        need(sha(image.read(f'{game}/{name}')) == target['sha256'], 'original-data product identity: ' + name)
        source = None if args.original else args.products / name
        if source is None or not source.exists():
            products[name] = dict(role='original', sha256=target['sha256'])
            continue
        raw = source.read_bytes()
        image.write(f'{game}/{name}', raw, scratch)
        products[name] = dict(role='rebuilt', path=str(source), bytes=len(raw), sha256=sha(raw),
                              original_equal=sha(raw) == target['sha256'])
    image.write('AUTOEXEC.BAT', b'@ECHO OFF\r\nPATH A:\\DOS;A:\\\r\nSET TEMP=A:\\DOS\r\nSET DOSDIR=A:\\DOS\r\n'
                b'CD \\' + game.encode() + b'\r\nECHO START > A:\\TH05RUN.TXT\r\nCALL GAME.BAT\r\n'
                b'ECHO EXIT >> A:\\TH05RUN.TXT\r\n\x1a', scratch)
    scratch.unlink()
    return original, image, products


def run(args):
    config = tomllib.loads((ROOT / 'config/runtime.toml').read_text())
    output = args.output.resolve()
    need(output.is_relative_to(ROOT / '.analysis/runtime') and not output.exists(),
         'use a fresh directory under .analysis/runtime')
    need(bool(os.environ.get('DISPLAY')), 'run through xvfb-run with a private display')
    need(args.original or (args.products and args.products.is_dir()), '--products DIR or --original')
    emulator = args.emulator.resolve()
    digest = sha(emulator.read_bytes())
    need(digest == config['emulator']['binary_sha256'], 'uncalibrated emulator binary')
    font = (ROOT / config['font']['path']).read_bytes()
    need(sha(font) == config['font']['sha256'], 'pinned FREECG98 bitmap font')
    timeline = sorted([(second, 'input', name) for second, name in map(timed, args.event)] +
                      [(second, 'frame', name) for second, name in map(timed, args.frame)])
    need(all(0 <= second < args.seconds for second, _, _ in timeline), 'events/checkpoints must precede stop')
    need(len({name for _, kind, name in timeline if kind == 'frame'}) == len(args.frame), 'unique frame names')
    output.mkdir(parents=True)
    original, image, products = prepare(args, output, config)
    game = config['image']['game_directory']
    (output / 'FREECG98.BMP').write_bytes(font)
    (output / 'captures').mkdir()
    conf = output / 'dosbox-x.conf'
    conf.write_text(PROFILE.format(cycles=args.cycles, nosound='false' if args.sound else 'true').replace(
        '[dosbox]\n', '[dosbox]\ncaptures=' + str(output / 'captures') + '\n'))
    argv = [str(emulator), '-defaultconf', '-defaultmapper', '-conf', str(conf), '-fastlaunch', '-nogui', '-nomenu',
            '-exit', '-c', f'imgmount 2 "{image.path}" -t hdd -fs none', '-c', 'boot -l c']
    env = {k: v for k, v in os.environ.items() if not k.startswith(('TH03_', 'TH04_'))}
    env.update(SDL_VIDEODRIVER='x11', SDL_AUDIODRIVER='dummy', WAYLAND_DISPLAY='',
               XDG_CACHE_HOME=str(output / 'cache'), XDG_CONFIG_HOME=str(output / 'config'),
               XDG_DATA_HOME=str(output / 'data'))
    record = dict(emulator=str(emulator), emulator_sha256=digest, config_sha256=sha(conf.read_bytes()),
                  cycles=args.cycles, products=products, role='original' if args.original else 'rebuilt',
                  argv=argv, events=[], frames={}, starting_hdi_sha256=sha(image.path.read_bytes()))
    for name in config['image']['saves']:
        (output / ('before-' + name)).write_bytes(image.read(f'{game}/{name}'))
    window = None

    def control(action, key):
        need(window is not None, 'emulator window missing')
        subprocess.run(['xdotool', 'windowfocus', '--sync', window], check=True, env=env, capture_output=True)
        command = ['xdotool', action] + (['--delay', '300'] if action == 'key' else [])
        subprocess.run([*command, key], check=True, env=env, capture_output=True)

    with (output / 'boot.log').open('wb') as log:
        process = subprocess.Popen(argv, cwd=output, env=env, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        started = time.monotonic()
        pending = list(timeline)
        try:
            while process.poll() is None and time.monotonic() - started < args.seconds:
                if window is None:
                    found = subprocess.run(['xdotool', 'search', '--onlyvisible', '--pid', str(process.pid),
                                            '--name', 'DOSBox-X'], env=env, capture_output=True, text=True).stdout.split()
                    if found:
                        window = found[0]
                while pending and time.monotonic() - started >= pending[0][0]:
                    second, kind, name = pending.pop(0)
                    if kind == 'frame':
                        path = output / (name + '.png')
                        need(window is not None, 'frame window missing')
                        subprocess.run(['import', '-window', window, str(path)], env=env, check=True,
                                       capture_output=True)
                        record['frames'][path.name] = sha(path.read_bytes())
                    else:
                        action, key = ('keydown', name[5:]) if name.startswith('down:') else (
                            ('keyup', name[3:]) if name.startswith('up:') else ('key', name))
                        control(action, key)
                    record['events'].append(dict(requested=second, observed=time.monotonic() - started,
                                                 kind=kind, name=name))
                time.sleep(.03)
            need(not pending, 'emulator exited before all requested events/checkpoints')
            control('key', 'ctrl+F9')
            process.wait(timeout=10)
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
    record['exit_code'] = process.returncode
    try:
        record['dos_markers'] = image.read('TH05RUN.TXT').decode('ascii').strip()
    except subprocess.CalledProcessError:
        record['dos_markers'] = None
    for name in config['image']['saves']:
        (output / ('after-' + name)).write_bytes(image.read(f'{game}/{name}'))
    for name, row in products.items():
        need(sha(image.read(f'{game}/{name}')) == row['sha256'], 'executed product changed: ' + name)
    need(sha(original.read_bytes()) == config['image']['sha256'], 'original media changed')
    (output / 'run.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(dict(output=str(output), frames=list(record['frames']), dos_markers=record['dos_markers'],
                          exit_code=record['exit_code']), indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--products', type=Path, help='directory holding rebuilt OP.EXE/MAIN.EXE/MAINE.EXE/ZUN.COM')
    p.add_argument('--original', action='store_true')
    p.add_argument('--seconds', type=float, default=60)
    p.add_argument('--cycles', type=int, default=24000)
    p.add_argument('--sound', action='store_true')
    p.add_argument('--event', action='append', default=[], help='KEY@SECOND, down:KEY@SECOND or up:KEY@SECOND')
    p.add_argument('--frame', action='append', default=[], help='NAME@SECOND; save an actual window PNG')
    p.add_argument('--emulator', type=Path, default=Path('/usr/bin/dosbox-x'))
    args = p.parse_args()
    need(0 < args.seconds <= 1800, 'bounded duration')
    os.sched_setaffinity(0, {max(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    run(args)


if __name__ == '__main__':
    main()

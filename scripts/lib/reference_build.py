"""Small dependency planner for the pinned ReC98 calibration build script.

The reference supplies linking scaffolding, never authored progress. Only
explicitly overlaid maintained source can acquire credit through a separate oracle.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess


def canonical(value: str) -> str:
    return value.replace("\\", "/").lower()


@dataclass(frozen=True)
class Rule:
    kind: str
    arguments: tuple[str, ...]
    dependencies: tuple[str, ...]
    response: str = ""


def rules_from_batch(text: str) -> dict[str, Rule]:
    responses: dict[str, str] = {}
    rules: dict[str, Rule] = {}
    for line in text.splitlines():
        if line.startswith("echo ") and ">" in line:
            match = re.fullmatch(r"echo (.*?)(>>?)([^>]+)", line)
            if not match:
                raise ValueError(f"unsupported echo: {line}")
            content, mode, destination = match.groups()
            key = canonical(destination)
            responses[key] = (responses.get(key, "") if mode == ">>" else "") + content + "\n"
        elif line.startswith("tcc @"):
            response = responses[canonical(line[5:])]
            arguments = response.split()
            flags = tuple(a for a in arguments if a.startswith("-"))
            output = next(a[2:] for a in flags if a.startswith("-n"))
            for source in (a for a in arguments if not a.startswith("-")):
                obj = canonical(output + Path(source.replace("\\", "/")).stem + ".obj")
                rules[obj] = Rule("tcc", (*flags, source), (canonical(source),))
        elif line.startswith("tasm32 "):
            args = line.split()[1:]
            rules[canonical(args[-1])] = Rule("tasm32", tuple(args), (canonical(args[-2]),))
        elif line.startswith("tlink @"):
            response = responses[canonical(line[7:])]
            fields = response.split(",")
            if len(fields) != 4:
                raise ValueError(f"unsupported linker response: {response}")
            output = canonical(fields[1].strip())
            dependencies = tuple(canonical(a) for a in fields[0].replace("+", " ").split()
                                 if a.lower().startswith("obj") and a.lower().endswith(".obj"))
            rules[output] = Rule("tlink", (), dependencies, response)
        elif line.startswith("bin\\Pipeline\\bmp2arr.com "):
            args = line.split()
            output = canonical(args[args.index("-o") + 1])
            source = canonical(args[args.index("-i") + 1])
            rules[output] = Rule("generator", tuple(args), (canonical(args[0]), source))
    return rules


INCLUDE = re.compile(rb'^\s*(?:#\s*include\s*[<"]([^>"\r\n]+)[>"]|include\s+([^\s;]+))',
                     re.IGNORECASE | re.MULTILINE)


class Builder:
    def __init__(self, root: Path, prefix: Path, msdos: Path):
        self.root, self.prefix, self.msdos = root, prefix, msdos
        self.rules = rules_from_batch((root / "build_dumb.bat").read_text())
        self.done: set[str] = set()
        self.includes: set[str] = set()
        self.records: list[dict] = []
        self.environment = {**os.environ, "WINEPREFIX": str(prefix), "WINEDEBUG": "-all",
                            "MSDOS_PATH": r"C:\TC4\BIN"}

    def resolve(self, relative: str) -> Path:
        # Windows includes are case insensitive. Resolve against the immutable
        # archive, retaining the real Linux filename for reading dependencies.
        path = self.root
        for component in relative.replace("\\", "/").split("/"):
            if component in {"", "."}:
                continue
            if component == "..":
                raise ValueError("dependency escapes the scaffold")
            exact = path / component
            if exact.exists():
                path = exact
                continue
            if not path.is_dir():
                return exact
            matches = [p for p in path.iterdir() if p.name.casefold() == component.casefold()]
            path = matches[0] if len(matches) == 1 else exact
        return path

    def scan_includes(self, name: str) -> None:
        if name in self.includes:
            return
        self.includes.add(name)
        path = self.resolve(name)
        if not path.is_file() or path.suffix.lower() not in {".cpp", ".c", ".h", ".hpp", ".asm", ".inc", ".inl"}:
            return
        for match in INCLUDE.finditer(path.read_bytes()):
            value = (match.group(1) or match.group(2)).decode("ascii", errors="replace")
            child = canonical(value)
            if child in self.rules and not self.resolve(child).exists():
                self.build(child)
            if self.resolve(child).exists():
                self.scan_includes(child)
            else:
                local = canonical(str(Path(name).parent / child))
                if self.resolve(local).exists():
                    self.scan_includes(local)

    def execute(self, label: str, command: list[str]) -> None:
        logdir = self.root.parent / "logs"
        logdir.mkdir(exist_ok=True)
        logfile = logdir / (label.replace("/", "_") + ".log")
        with logfile.open("wb") as stream:
            result = subprocess.run(command, cwd=self.root, env=self.environment,
                                    stdout=stream, stderr=subprocess.STDOUT, timeout=180)
        self.records.append({"output": label, "command": command,
                             "returncode": result.returncode,
                             "log": str(logfile.relative_to(self.root.parent))})
        if result.returncode:
            raise RuntimeError(f"{label} failed: {logfile}\n" + logfile.read_text(errors="replace")[-2500:])

    def build(self, output: str) -> Path:
        output = canonical(output)
        if output in self.done:
            return self.resolve(output)
        if output not in self.rules:
            raise ValueError(f"no pinned producer for {output}")
        rule = self.rules[output]
        for dependency in rule.dependencies:
            if dependency in self.rules:
                self.build(dependency)
            elif not self.resolve(dependency).is_file():
                raise FileNotFoundError(dependency)
            self.scan_includes(dependency)
        destination = self.root / output
        destination.parent.mkdir(parents=True, exist_ok=True)
        dos = ["wine", str(self.msdos), "-e", "-x"]
        if rule.kind == "tcc":
            command = [*dos, "tcc", *rule.arguments]
        elif rule.kind == "tasm32":
            command = ["wine", r"C:\TASM50\bin\TASM32.EXE", *rule.arguments]
        elif rule.kind == "tlink":
            response = destination.with_suffix(".rsp")
            response.write_bytes(rule.response.replace("\n", "\r\n").encode("ascii"))
            command = [*dos, "tlink", "@" + str(response.relative_to(self.root)).replace("/", "\\")]
        else:
            command = [*dos, *rule.arguments]
        self.execute(output, command)
        resolved = self.resolve(output)
        if not resolved.is_file() or not resolved.stat().st_size:
            raise RuntimeError(f"producer returned success without {output}")
        self.done.add(output)
        return resolved

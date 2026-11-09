"""Minimal AST code graph (functions/classes + call edges) for the graph-guided arm.

NOTE: this is our own re-implementation. The official competition tools of the same names
(get_code_neighbors / get_code_subgraph) use dataset-provided prebuilt graphs whose exact
output format has NOT been verified in this session (HARNESS_README.md not readable without
joining the competition). Do not describe results from this module as using the official tools.
"""
import ast, re


class CodeGraph:
    def __init__(self, source: str):
        self.tree = ast.parse(source)
        self.nodes = {}   # qualname -> {kind, start, end, sig}
        self.calls = {}   # qualname -> set(raw callee names)
        self._collect(self.tree.body, "")

    def _collect(self, body, prefix):
        for n in body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                q = f"{prefix}{n.name}"
                kind = "class" if isinstance(n, ast.ClassDef) else "function"
                sig = f"class {n.name}" if kind == "class" else f"def {n.name}({', '.join(a.arg for a in n.args.args)})"
                self.nodes[q] = {"kind": kind, "start": n.lineno, "end": getattr(n, "end_lineno", n.lineno), "sig": sig}
                called = set()
                for sub in ast.walk(n):
                    if isinstance(sub, ast.Call):
                        f = sub.func
                        if isinstance(f, ast.Name):
                            called.add(f.id)
                        elif isinstance(f, ast.Attribute):
                            called.add(f.attr)
                self.calls[q] = called
                if kind == "class":
                    self._collect(n.body, q + ".")

    def _resolve(self, raw):
        return sorted(q for q in self.nodes if q.split(".")[-1] == raw)

    def callees(self, q):
        out = []
        for raw in self.calls.get(q, ()):
            out.extend(r for r in self._resolve(raw) if r != q or True)
        return sorted(set(out))

    def callers(self, q):
        short = q.split(".")[-1]
        return sorted(k for k, v in self.calls.items() if short in v)

    def external_calls(self, q):
        return sorted(r for r in self.calls.get(q, ()) if not self._resolve(r))

    def enclosing(self, lineno):
        best = None
        for q, d in self.nodes.items():
            if d["start"] <= lineno <= d["end"] and (best is None or d["start"] >= self.nodes[best]["start"]):
                best = q
        return best

    def _fmt(self, q):
        d = self.nodes[q]
        return f"{d['sig']}  [lines {d['start']}-{d['end']}]"

    def overview(self):
        return "\n".join(f"- {self._fmt(q)} calls: {', '.join(self.callees(q)) or '(none internal)'}"
                         for q in self.nodes)

    def neighbors_text(self, symbol):
        if symbol not in self.nodes:
            return f"ERROR: unknown symbol '{symbol}'. Known: {', '.join(self.nodes)}"
        return (f"{self._fmt(symbol)}\n callers: {', '.join(self.callers(symbol)) or '(none)'}\n"
                f" callees: {', '.join(self.callees(symbol)) or '(none)'}\n"
                f" external/builtin calls: {', '.join(self.external_calls(symbol)) or '(none)'}")

    def subgraph_text(self, symbol, depth=1):
        if symbol not in self.nodes:
            return f"ERROR: unknown symbol '{symbol}'. Known: {', '.join(self.nodes)}"
        depth = max(0, min(int(depth), 3))
        seen, lines = set(), []

        def walk(q, d, ind):
            lines.append("  " * ind + self._fmt(q) + (" (seen)" if q in seen else ""))
            if q in seen or d == 0:
                return
            seen.add(q)
            for c in self.callees(q):
                walk(c, d - 1, ind + 1)
        walk(symbol, depth, 0)
        return "\n".join(lines)


def suspects_from_failure(graph: CodeGraph, name: str, failure_text: str):
    """Map traceback line numbers inside the target file to enclosing functions."""
    pat = re.compile(r"python_programs[\\/]" + re.escape(name) + r"\.py:(\d+)")
    found = []
    for m in pat.finditer(failure_text or ""):
        q = graph.enclosing(int(m.group(1)))
        if q and q not in found:
            found.append(q)
    return found

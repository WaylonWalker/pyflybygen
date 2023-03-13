from tree_sitter_languages import get_language, get_parser


class CapturePoint:
    def __init__(self, node):
        self.start_point = node[0].start_point[0]
        self.end_point = node[0].end_point[0]

    def __eq__(self, o):
        return self.start_point == o.start_point and self.end_point == o.end_point

    def __repr__(self):
        return f"{self.start_point}:{self.end_point}"

    def __hash__(self):
        return hash(repr(self))


def get_imports(content):
    language = get_language("python")
    content = content
    content_lines = content.split("\n")
    parser = get_parser("python")
    tree = parser.parse(content.encode())
    wild_imports = set(
        CapturePoint(n)
        for n in language.query(
            "(import_from_statement (wildcard_import) @wildcard) @import_wild"
        ).captures(tree.root_node)
    )
    import_froms = list(
        set(
            CapturePoint(n)
            for n in language.query("(import_from_statement) @import_from").captures(
                tree.root_node
            )
        )
        - wild_imports
    )
    imports = list(
        set(
            CapturePoint(n)
            for n in language.query("(import_statement) @import").captures(
                tree.root_node
            )
        )
    )
    import_lines = [
        (" ".join(content_lines[s.start_point : s.end_point + 1])).strip()
        for s in imports + import_froms
    ]

    return import_lines

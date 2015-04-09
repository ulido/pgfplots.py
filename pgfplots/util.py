class _Packages(dict):
    def __str__(self):
        if len(self) == 0:
            return ""
        str_packages = []
        for k, v in self.iteritems():
            if v is None:
                str_packages.append("\usepackage{{{}}}".format(k))
            else:
                str_packages.append("\usepackage{{{}}}[{}]".format(k, v))
        return "\n".join(str_packages)


class _OptionsDict(dict):
    def __str__(self):
        if len(self) == 0:
            return ""
        str_options = []
        for k, v in self.iteritems():
            if v is None:
                str_options.append(k)
            else:
                str_options.append("{}={{{}}}".format(k, v))
        return ",".join(str_options)


def note_pdf_encode(note):
    "TeX-encode the given string."
    replacement = {
        "\n": r"\textLF",
        "{": r"\{",
        "}": r"\}",
        "_": r"\_",
        "&": r"\&",
        "%": r"\%",
        " ": r"~",
        }
    for k, v in replacement.iteritems():
        note = note.replace(k, v)
    return note

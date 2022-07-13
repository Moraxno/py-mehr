import pyfiglet
from argparse import ArgumentParser, RawTextHelpFormatter
import shutil
from enum import Enum

COLOR_LUT = {
    "green": "\033[92m",
    "default": "\033[0m"
}

class ArgumentIdentifierType(Enum):
    CONFLICTING = 0
    NON_POSITIONAL = 1
    POSITIONAL = 2

NON_POSITIONAL_PREFIXES = ["-", "--"]

def get_argument_identifier_type(*name_or_flags: str) -> ArgumentIdentifier:
    if len(name_or_flags) == 1 and not name_or_flags[0].startswith(NON_POSITIONAL_PREFIXES):
        return ArgumentIdentifier.POSITIONAL
    else:
        all_positional = True
        for nof in name_or_flags:
            all_positional = all_positional and nof.startswith(NON_POSITIONAL_PREFIXES)
        if all_positional:
            return ArgumentIdentifier.NON_POSITIONAL
        else:
            return ArgumentIdentifier.CONFLICTING


class AcronymArgParser:
    def __init__(self, toolname, acro=None, font="small"):
        self.acro = "".join([c for c in toolname if c.isupper()]).capitalize()
        self.ap = ArgumentParser(
            formatter_class=RawTextHelpFormatter, 
            description=AcronymArgParser.generate_banner(toolname, acro, font, color="green")
        )

        self.ap._action_groups.pop()
        self.required_group = self.ap.add_argument_group('required arguments')
        self.optional_group = self.ap.add_argument_group('optional arguments')

    def add_required_argument(self, *name_or_flags, **kwargs):
        arg_id_type = get_argument_identifier_type(*name_or_flags)

        if arg_id_type == ArgumentIdentifier.CONFLICTING:
            raise RuntimeError(f"Identifiers {', '.join(name_or_flags)} mixes positional and non-positional syntax.")
        
        if arg_id_type == ArgumentIdentfier.NON_POSITIONAL:
            kwargs["required"] = True
        
        return self.required_group.add_argument(name, *name_or_flags, **kwargs)
    
    def add_optional_argument(self, *name_or_flags, **kwargs):
        arg_id_type = get_argument_identifier_type(*name_or_flags)

        if arg_id_type == ArgumentIdentifier.CONFLICTING:
            raise RuntimeError(f"Identifiers {', '.join(name_or_flags)} mixes positional and non-positional syntax.")
        
        if arg_id_type == ArgumentIdentfier.POSITIONAL:
            raise RuntimeError(f"Identifier {name_or_flags[0]} is postional and can therefore not be optional.")

        kwargs["required"] = False
        return self.optional_group.add_argument(name, *name_or_flags, **kwargs)

    def parse_args(self, *args, **kwargs):
        return self.ap.parse_args(*args, **kwargs)

    @staticmethod
    def generate_banner(toolname, acro=None, font="small", color="default"):
        side_padding = 4
        if acro is None:
            acro = "".join([c for c in toolname if c.isupper()]).capitalize()
        art = pyfiglet.figlet_format(acro, font=font)
        art_lines = art.split("\n")
        art_width = len(art_lines[0])

        txt_width = len(toolname)

        cmd_width = max(art_width, txt_width) + 2 * side_padding
        
        art_left_pad = (cmd_width - art_width) // 2
        art_right_pad = cmd_width - art_width - art_left_pad

        txt_left_pad = (cmd_width - txt_width) // 2
        txt_right_pad = cmd_width - txt_width - txt_left_pad

        styled_art_lines = [f"{' ' * art_left_pad}{COLOR_LUT[color]}{art_line}{COLOR_LUT['default']}{' ' * art_right_pad}" for art_line in art_lines]
        styled_art = "\n".join(styled_art_lines)

        padded_txt = f"{' ' * txt_left_pad}{COLOR_LUT[color]}{toolname}{COLOR_LUT['default']}{' ' * txt_right_pad}" 

        banner = styled_art + "\n" + padded_txt
        return banner

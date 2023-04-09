from enum import Enum

class Colors(Enum):
  '''
  a group of constants, each color maps to its procedance
  '''
  RED = 7
  ORANGE = 6
  YELLOW = 5
  GREEN = 4
  BLUE = 3
  INDIGO = 2
  VIOLET = 1

  @staticmethod
  def printColored(color: 'Colors', text, **kwargs):
    '''
    print colored text using unix shell escape sequences
    format: \33[48;2;fore_r;fore_g;fore_b;38;2;back_r;back_g;back_bm]
    '''
    colors = { 
      "RED":'\033[48;2;196;0;0;38;2;59;255;255m',
      "ORANGE":'\033[48;2;245;82;0;38;2;10;173;255m',
      "YELLOW":'\033[48;2;255;217;0;38;2;0;38;255m',
      "GREEN":'\033[48;2;14;204;0;38;2;241;51;255m',
      "BLUE":'\033[48;2;0;51;255;38;2;255;204;0m',
      "INDIGO":'\033[48;2;29;0;135;38;2;226;255;120m',
      "VIOLET":'\033[48;2;130;0;237;38;2;125;255;18m',
    }
    end_color = "\033[0m"
    print(f"{colors[color.name]}{text}{end_color}", **kwargs)
    
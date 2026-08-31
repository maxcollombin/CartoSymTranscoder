# Generated from vendor/cartosymcss-grammar/CQL2Text.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,72,508,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,1,0,1,0,1,
        0,1,1,1,1,1,1,5,1,111,8,1,10,1,12,1,114,9,1,1,2,1,2,1,2,5,2,119,
        8,2,10,2,12,2,122,9,2,1,3,5,3,125,8,3,10,3,12,3,128,9,3,1,3,1,3,
        1,4,1,4,1,4,1,4,1,4,3,4,137,8,4,1,4,1,4,1,4,1,4,3,4,143,8,4,1,5,
        1,5,1,5,1,5,3,5,149,8,5,1,5,1,5,1,5,3,5,154,8,5,1,5,1,5,1,5,1,5,
        1,5,1,5,3,5,162,8,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,3,5,171,8,5,1,5,
        3,5,174,8,5,1,6,1,6,1,7,1,7,1,7,5,7,181,8,7,10,7,12,7,184,9,7,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,10,1,10,1,10,1,10,1,10,1,10,
        1,10,1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,14,
        1,14,1,15,1,15,1,15,5,15,218,8,15,10,15,12,15,221,9,15,1,16,1,16,
        1,16,5,16,226,8,16,10,16,12,16,229,9,16,1,17,1,17,1,17,3,17,234,
        8,17,1,18,1,18,1,18,1,18,1,18,3,18,241,8,18,1,18,3,18,244,8,18,1,
        19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,3,19,254,8,19,1,20,1,20,1,
        21,1,21,1,22,1,22,1,22,3,22,263,8,22,1,22,1,22,1,23,1,23,1,23,5,
        23,270,8,23,10,23,12,23,273,9,23,1,24,1,24,1,24,1,24,1,24,1,24,4,
        24,281,8,24,11,24,12,24,282,1,24,1,24,3,24,287,8,24,1,25,1,25,1,
        25,1,25,1,25,1,25,1,25,1,25,1,25,1,25,1,25,3,25,300,8,25,1,26,1,
        26,1,26,3,26,305,8,26,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,3,
        27,315,8,27,1,28,1,28,3,28,319,8,28,1,28,1,28,1,29,1,29,3,29,325,
        8,29,1,29,1,29,1,30,1,30,3,30,331,8,30,1,30,1,30,1,31,1,31,3,31,
        337,8,31,1,31,1,31,1,32,1,32,3,32,343,8,32,1,32,1,32,1,33,1,33,3,
        33,349,8,33,1,33,1,33,1,34,1,34,3,34,355,8,34,1,34,1,34,1,35,1,35,
        1,35,1,35,1,36,1,36,1,36,3,36,366,8,36,1,37,1,37,1,37,1,37,4,37,
        372,8,37,11,37,12,37,373,1,37,1,37,1,38,1,38,1,38,1,38,1,38,1,38,
        1,38,1,38,1,38,1,38,1,38,1,38,5,38,390,8,38,10,38,12,38,393,9,38,
        1,38,1,38,3,38,397,8,38,1,39,1,39,1,39,1,39,5,39,403,8,39,10,39,
        12,39,406,9,39,1,39,1,39,1,40,1,40,1,40,1,40,5,40,414,8,40,10,40,
        12,40,417,9,40,1,40,1,40,1,41,1,41,1,41,1,41,5,41,425,8,41,10,41,
        12,41,428,9,41,1,41,1,41,1,42,1,42,1,42,1,42,5,42,436,8,42,10,42,
        12,42,439,9,42,1,42,1,42,1,43,1,43,1,43,1,43,5,43,447,8,43,10,43,
        12,43,450,9,43,1,43,1,43,1,44,1,44,1,44,1,45,1,45,1,45,1,45,1,45,
        1,45,1,45,1,45,3,45,465,8,45,1,45,1,45,1,45,1,45,1,45,3,45,472,8,
        45,1,45,1,45,1,46,3,46,477,8,46,1,46,1,46,1,47,1,47,1,47,3,47,484,
        8,47,1,48,1,48,1,48,1,48,1,48,1,49,1,49,1,49,1,49,1,49,1,50,1,50,
        1,50,1,50,1,50,1,50,1,50,1,51,1,51,1,51,3,51,506,8,51,1,51,0,0,52,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,
        46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,
        90,92,94,96,98,100,102,0,8,1,0,56,61,1,0,13,20,1,0,21,35,1,0,36,
        39,1,0,62,63,2,0,52,52,64,66,1,0,9,10,1,0,70,71,522,0,104,1,0,0,
        0,2,107,1,0,0,0,4,115,1,0,0,0,6,126,1,0,0,0,8,142,1,0,0,0,10,173,
        1,0,0,0,12,175,1,0,0,0,14,177,1,0,0,0,16,185,1,0,0,0,18,192,1,0,
        0,0,20,194,1,0,0,0,22,201,1,0,0,0,24,203,1,0,0,0,26,210,1,0,0,0,
        28,212,1,0,0,0,30,214,1,0,0,0,32,222,1,0,0,0,34,230,1,0,0,0,36,243,
        1,0,0,0,38,253,1,0,0,0,40,255,1,0,0,0,42,257,1,0,0,0,44,259,1,0,
        0,0,46,266,1,0,0,0,48,286,1,0,0,0,50,299,1,0,0,0,52,304,1,0,0,0,
        54,314,1,0,0,0,56,316,1,0,0,0,58,322,1,0,0,0,60,328,1,0,0,0,62,334,
        1,0,0,0,64,340,1,0,0,0,66,346,1,0,0,0,68,352,1,0,0,0,70,358,1,0,
        0,0,72,362,1,0,0,0,74,367,1,0,0,0,76,396,1,0,0,0,78,398,1,0,0,0,
        80,409,1,0,0,0,82,420,1,0,0,0,84,431,1,0,0,0,86,442,1,0,0,0,88,453,
        1,0,0,0,90,456,1,0,0,0,92,476,1,0,0,0,94,483,1,0,0,0,96,485,1,0,
        0,0,98,490,1,0,0,0,100,495,1,0,0,0,102,505,1,0,0,0,104,105,3,2,1,
        0,105,106,5,0,0,1,106,1,1,0,0,0,107,112,3,4,2,0,108,109,5,2,0,0,
        109,111,3,4,2,0,110,108,1,0,0,0,111,114,1,0,0,0,112,110,1,0,0,0,
        112,113,1,0,0,0,113,3,1,0,0,0,114,112,1,0,0,0,115,120,3,6,3,0,116,
        117,5,1,0,0,117,119,3,6,3,0,118,116,1,0,0,0,119,122,1,0,0,0,120,
        118,1,0,0,0,120,121,1,0,0,0,121,5,1,0,0,0,122,120,1,0,0,0,123,125,
        5,3,0,0,124,123,1,0,0,0,125,128,1,0,0,0,126,124,1,0,0,0,126,127,
        1,0,0,0,127,129,1,0,0,0,128,126,1,0,0,0,129,130,3,8,4,0,130,7,1,
        0,0,0,131,143,3,16,8,0,132,143,3,20,10,0,133,143,3,24,12,0,134,136,
        3,28,14,0,135,137,3,10,5,0,136,135,1,0,0,0,136,137,1,0,0,0,137,143,
        1,0,0,0,138,139,5,53,0,0,139,140,3,2,1,0,140,141,5,54,0,0,141,143,
        1,0,0,0,142,131,1,0,0,0,142,132,1,0,0,0,142,133,1,0,0,0,142,134,
        1,0,0,0,142,138,1,0,0,0,143,9,1,0,0,0,144,145,3,12,6,0,145,146,3,
        28,14,0,146,174,1,0,0,0,147,149,5,3,0,0,148,147,1,0,0,0,148,149,
        1,0,0,0,149,150,1,0,0,0,150,151,5,4,0,0,151,174,3,50,25,0,152,154,
        5,3,0,0,153,152,1,0,0,0,153,154,1,0,0,0,154,155,1,0,0,0,155,156,
        5,5,0,0,156,157,3,30,15,0,157,158,5,1,0,0,158,159,3,30,15,0,159,
        174,1,0,0,0,160,162,5,3,0,0,161,160,1,0,0,0,161,162,1,0,0,0,162,
        163,1,0,0,0,163,164,5,6,0,0,164,165,5,53,0,0,165,166,3,14,7,0,166,
        167,5,54,0,0,167,174,1,0,0,0,168,170,5,7,0,0,169,171,5,3,0,0,170,
        169,1,0,0,0,170,171,1,0,0,0,171,172,1,0,0,0,172,174,5,8,0,0,173,
        144,1,0,0,0,173,148,1,0,0,0,173,153,1,0,0,0,173,161,1,0,0,0,173,
        168,1,0,0,0,174,11,1,0,0,0,175,176,7,0,0,0,176,13,1,0,0,0,177,182,
        3,28,14,0,178,179,5,55,0,0,179,181,3,28,14,0,180,178,1,0,0,0,181,
        184,1,0,0,0,182,180,1,0,0,0,182,183,1,0,0,0,183,15,1,0,0,0,184,182,
        1,0,0,0,185,186,3,18,9,0,186,187,5,53,0,0,187,188,3,28,14,0,188,
        189,5,55,0,0,189,190,3,28,14,0,190,191,5,54,0,0,191,17,1,0,0,0,192,
        193,7,1,0,0,193,19,1,0,0,0,194,195,3,22,11,0,195,196,5,53,0,0,196,
        197,3,28,14,0,197,198,5,55,0,0,198,199,3,28,14,0,199,200,5,54,0,
        0,200,21,1,0,0,0,201,202,7,2,0,0,202,23,1,0,0,0,203,204,3,26,13,
        0,204,205,5,53,0,0,205,206,3,28,14,0,206,207,5,55,0,0,207,208,3,
        28,14,0,208,209,5,54,0,0,209,25,1,0,0,0,210,211,7,3,0,0,211,27,1,
        0,0,0,212,213,3,30,15,0,213,29,1,0,0,0,214,219,3,32,16,0,215,216,
        7,4,0,0,216,218,3,32,16,0,217,215,1,0,0,0,218,221,1,0,0,0,219,217,
        1,0,0,0,219,220,1,0,0,0,220,31,1,0,0,0,221,219,1,0,0,0,222,227,3,
        34,17,0,223,224,7,5,0,0,224,226,3,34,17,0,225,223,1,0,0,0,226,229,
        1,0,0,0,227,225,1,0,0,0,227,228,1,0,0,0,228,33,1,0,0,0,229,227,1,
        0,0,0,230,233,3,36,18,0,231,232,5,67,0,0,232,234,3,36,18,0,233,231,
        1,0,0,0,233,234,1,0,0,0,234,35,1,0,0,0,235,236,5,53,0,0,236,237,
        3,30,15,0,237,238,5,54,0,0,238,244,1,0,0,0,239,241,5,63,0,0,240,
        239,1,0,0,0,240,241,1,0,0,0,241,242,1,0,0,0,242,244,3,38,19,0,243,
        235,1,0,0,0,243,240,1,0,0,0,244,37,1,0,0,0,245,254,3,54,27,0,246,
        254,3,94,47,0,247,254,3,50,25,0,248,254,5,68,0,0,249,254,3,40,20,
        0,250,254,3,42,21,0,251,254,3,44,22,0,252,254,3,48,24,0,253,245,
        1,0,0,0,253,246,1,0,0,0,253,247,1,0,0,0,253,248,1,0,0,0,253,249,
        1,0,0,0,253,250,1,0,0,0,253,251,1,0,0,0,253,252,1,0,0,0,254,39,1,
        0,0,0,255,256,7,6,0,0,256,41,1,0,0,0,257,258,7,7,0,0,258,43,1,0,
        0,0,259,260,5,71,0,0,260,262,5,53,0,0,261,263,3,46,23,0,262,261,
        1,0,0,0,262,263,1,0,0,0,263,264,1,0,0,0,264,265,5,54,0,0,265,45,
        1,0,0,0,266,271,3,28,14,0,267,268,5,55,0,0,268,270,3,28,14,0,269,
        267,1,0,0,0,270,273,1,0,0,0,271,269,1,0,0,0,271,272,1,0,0,0,272,
        47,1,0,0,0,273,271,1,0,0,0,274,275,5,53,0,0,275,287,5,54,0,0,276,
        277,5,53,0,0,277,280,3,28,14,0,278,279,5,55,0,0,279,281,3,28,14,
        0,280,278,1,0,0,0,281,282,1,0,0,0,282,280,1,0,0,0,282,283,1,0,0,
        0,283,284,1,0,0,0,284,285,5,54,0,0,285,287,1,0,0,0,286,274,1,0,0,
        0,286,276,1,0,0,0,287,49,1,0,0,0,288,289,5,11,0,0,289,290,5,53,0,
        0,290,291,3,52,26,0,291,292,5,54,0,0,292,300,1,0,0,0,293,294,5,12,
        0,0,294,295,5,53,0,0,295,296,3,52,26,0,296,297,5,54,0,0,297,300,
        1,0,0,0,298,300,5,69,0,0,299,288,1,0,0,0,299,293,1,0,0,0,299,298,
        1,0,0,0,300,51,1,0,0,0,301,305,3,50,25,0,302,305,3,42,21,0,303,305,
        3,44,22,0,304,301,1,0,0,0,304,302,1,0,0,0,304,303,1,0,0,0,305,53,
        1,0,0,0,306,315,3,56,28,0,307,315,3,58,29,0,308,315,3,60,30,0,309,
        315,3,62,31,0,310,315,3,64,32,0,311,315,3,66,33,0,312,315,3,68,34,
        0,313,315,3,88,44,0,314,306,1,0,0,0,314,307,1,0,0,0,314,308,1,0,
        0,0,314,309,1,0,0,0,314,310,1,0,0,0,314,311,1,0,0,0,314,312,1,0,
        0,0,314,313,1,0,0,0,315,55,1,0,0,0,316,318,5,40,0,0,317,319,5,48,
        0,0,318,317,1,0,0,0,318,319,1,0,0,0,319,320,1,0,0,0,320,321,3,70,
        35,0,321,57,1,0,0,0,322,324,5,41,0,0,323,325,5,48,0,0,324,323,1,
        0,0,0,324,325,1,0,0,0,325,326,1,0,0,0,326,327,3,74,37,0,327,59,1,
        0,0,0,328,330,5,42,0,0,329,331,5,48,0,0,330,329,1,0,0,0,330,331,
        1,0,0,0,331,332,1,0,0,0,332,333,3,78,39,0,333,61,1,0,0,0,334,336,
        5,43,0,0,335,337,5,48,0,0,336,335,1,0,0,0,336,337,1,0,0,0,337,338,
        1,0,0,0,338,339,3,80,40,0,339,63,1,0,0,0,340,342,5,44,0,0,341,343,
        5,48,0,0,342,341,1,0,0,0,342,343,1,0,0,0,343,344,1,0,0,0,344,345,
        3,82,41,0,345,65,1,0,0,0,346,348,5,45,0,0,347,349,5,48,0,0,348,347,
        1,0,0,0,348,349,1,0,0,0,349,350,1,0,0,0,350,351,3,84,42,0,351,67,
        1,0,0,0,352,354,5,46,0,0,353,355,5,48,0,0,354,353,1,0,0,0,354,355,
        1,0,0,0,355,356,1,0,0,0,356,357,3,86,43,0,357,69,1,0,0,0,358,359,
        5,53,0,0,359,360,3,72,36,0,360,361,5,54,0,0,361,71,1,0,0,0,362,363,
        3,92,46,0,363,365,3,92,46,0,364,366,3,92,46,0,365,364,1,0,0,0,365,
        366,1,0,0,0,366,73,1,0,0,0,367,368,5,53,0,0,368,371,3,72,36,0,369,
        370,5,55,0,0,370,372,3,72,36,0,371,369,1,0,0,0,372,373,1,0,0,0,373,
        371,1,0,0,0,373,374,1,0,0,0,374,375,1,0,0,0,375,376,5,54,0,0,376,
        75,1,0,0,0,377,378,5,53,0,0,378,397,5,54,0,0,379,380,5,53,0,0,380,
        381,3,72,36,0,381,382,5,55,0,0,382,383,3,72,36,0,383,384,5,55,0,
        0,384,385,3,72,36,0,385,386,5,55,0,0,386,391,3,72,36,0,387,388,5,
        55,0,0,388,390,3,72,36,0,389,387,1,0,0,0,390,393,1,0,0,0,391,389,
        1,0,0,0,391,392,1,0,0,0,392,394,1,0,0,0,393,391,1,0,0,0,394,395,
        5,54,0,0,395,397,1,0,0,0,396,377,1,0,0,0,396,379,1,0,0,0,397,77,
        1,0,0,0,398,399,5,53,0,0,399,404,3,76,38,0,400,401,5,55,0,0,401,
        403,3,76,38,0,402,400,1,0,0,0,403,406,1,0,0,0,404,402,1,0,0,0,404,
        405,1,0,0,0,405,407,1,0,0,0,406,404,1,0,0,0,407,408,5,54,0,0,408,
        79,1,0,0,0,409,410,5,53,0,0,410,415,3,70,35,0,411,412,5,55,0,0,412,
        414,3,70,35,0,413,411,1,0,0,0,414,417,1,0,0,0,415,413,1,0,0,0,415,
        416,1,0,0,0,416,418,1,0,0,0,417,415,1,0,0,0,418,419,5,54,0,0,419,
        81,1,0,0,0,420,421,5,53,0,0,421,426,3,74,37,0,422,423,5,55,0,0,423,
        425,3,74,37,0,424,422,1,0,0,0,425,428,1,0,0,0,426,424,1,0,0,0,426,
        427,1,0,0,0,427,429,1,0,0,0,428,426,1,0,0,0,429,430,5,54,0,0,430,
        83,1,0,0,0,431,432,5,53,0,0,432,437,3,78,39,0,433,434,5,55,0,0,434,
        436,3,78,39,0,435,433,1,0,0,0,436,439,1,0,0,0,437,435,1,0,0,0,437,
        438,1,0,0,0,438,440,1,0,0,0,439,437,1,0,0,0,440,441,5,54,0,0,441,
        85,1,0,0,0,442,443,5,53,0,0,443,448,3,54,27,0,444,445,5,55,0,0,445,
        447,3,54,27,0,446,444,1,0,0,0,447,450,1,0,0,0,448,446,1,0,0,0,448,
        449,1,0,0,0,449,451,1,0,0,0,450,448,1,0,0,0,451,452,5,54,0,0,452,
        87,1,0,0,0,453,454,5,47,0,0,454,455,3,90,45,0,455,89,1,0,0,0,456,
        457,5,53,0,0,457,458,3,92,46,0,458,459,5,55,0,0,459,460,3,92,46,
        0,460,464,5,55,0,0,461,462,3,92,46,0,462,463,5,55,0,0,463,465,1,
        0,0,0,464,461,1,0,0,0,464,465,1,0,0,0,465,466,1,0,0,0,466,467,3,
        92,46,0,467,468,5,55,0,0,468,471,3,92,46,0,469,470,5,55,0,0,470,
        472,3,92,46,0,471,469,1,0,0,0,471,472,1,0,0,0,472,473,1,0,0,0,473,
        474,5,54,0,0,474,91,1,0,0,0,475,477,5,63,0,0,476,475,1,0,0,0,476,
        477,1,0,0,0,477,478,1,0,0,0,478,479,5,68,0,0,479,93,1,0,0,0,480,
        484,3,96,48,0,481,484,3,98,49,0,482,484,3,100,50,0,483,480,1,0,0,
        0,483,481,1,0,0,0,483,482,1,0,0,0,484,95,1,0,0,0,485,486,5,49,0,
        0,486,487,5,53,0,0,487,488,5,69,0,0,488,489,5,54,0,0,489,97,1,0,
        0,0,490,491,5,50,0,0,491,492,5,53,0,0,492,493,5,69,0,0,493,494,5,
        54,0,0,494,99,1,0,0,0,495,496,5,51,0,0,496,497,5,53,0,0,497,498,
        3,102,51,0,498,499,5,55,0,0,499,500,3,102,51,0,500,501,5,54,0,0,
        501,101,1,0,0,0,502,506,5,69,0,0,503,506,3,42,21,0,504,506,3,44,
        22,0,505,502,1,0,0,0,505,503,1,0,0,0,505,504,1,0,0,0,506,103,1,0,
        0,0,45,112,120,126,136,142,148,153,161,170,173,182,219,227,233,240,
        243,253,262,271,282,286,299,304,314,318,324,330,336,342,348,354,
        365,373,391,396,404,415,426,437,448,464,471,476,483,505
    ]

class CQL2TextParser ( Parser ):

    grammarFileName = "CQL2Text.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'('", "')'", "','", "'='", "<INVALID>", 
                     "'<='", "'>='", "'<'", "'>'", "'+'", "'-'", "'*'", 
                     "'/'", "'%'", "'^'" ]

    symbolicNames = [ "<INVALID>", "AND", "OR", "NOT", "LIKE", "BETWEEN", 
                      "IN", "IS", "NULL", "TRUE", "FALSE", "CASEI", "ACCENTI", 
                      "S_INTERSECTS", "S_EQUALS", "S_DISJOINT", "S_TOUCHES", 
                      "S_WITHIN", "S_OVERLAPS", "S_CROSSES", "S_CONTAINS", 
                      "T_AFTER", "T_BEFORE", "T_CONTAINS", "T_DISJOINT", 
                      "T_DURING", "T_EQUALS", "T_FINISHEDBY", "T_FINISHES", 
                      "T_INTERSECTS", "T_MEETS", "T_METBY", "T_OVERLAPPEDBY", 
                      "T_OVERLAPS", "T_STARTEDBY", "T_STARTS", "A_EQUALS", 
                      "A_CONTAINS", "A_CONTAINEDBY", "A_OVERLAPS", "POINT", 
                      "LINESTRING", "POLYGON", "MULTIPOINT", "MULTILINESTRING", 
                      "MULTIPOLYGON", "GEOMETRYCOLLECTION", "BBOX", "ZSUFFIX", 
                      "DATE", "TIMESTAMP", "INTERVAL", "IDIV", "LPAR", "RPAR", 
                      "COMMA", "EQ", "NEQ", "LTEQ", "GTEQ", "LT", "GT", 
                      "PLUS", "MINUS", "MUL", "SLASH", "MOD", "POW", "NUMERIC_LITERAL", 
                      "STRING", "QUOTED_IDENTIFIER", "IDENTIFIER", "WS" ]

    RULE_cql2Text = 0
    RULE_booleanExpression = 1
    RULE_booleanTerm = 2
    RULE_booleanFactor = 3
    RULE_primary = 4
    RULE_predicateTail = 5
    RULE_comparisonOperator = 6
    RULE_inList = 7
    RULE_spatialPredicate = 8
    RULE_spatialFunction = 9
    RULE_temporalPredicate = 10
    RULE_temporalFunction = 11
    RULE_arrayPredicate = 12
    RULE_arrayFunction = 13
    RULE_operand = 14
    RULE_arithmeticExpr = 15
    RULE_arithmeticTerm = 16
    RULE_powerTerm = 17
    RULE_arithmeticFactor = 18
    RULE_atom = 19
    RULE_booleanLiteral = 20
    RULE_propertyName = 21
    RULE_functionCall = 22
    RULE_argumentList = 23
    RULE_arrayExpr = 24
    RULE_characterClause = 25
    RULE_characterClauseArg = 26
    RULE_geometryLiteral = 27
    RULE_pointTaggedText = 28
    RULE_linestringTaggedText = 29
    RULE_polygonTaggedText = 30
    RULE_multipointTaggedText = 31
    RULE_multilinestringTaggedText = 32
    RULE_multipolygonTaggedText = 33
    RULE_geometryCollectionTaggedText = 34
    RULE_pointText = 35
    RULE_point = 36
    RULE_lineStringText = 37
    RULE_linearRingText = 38
    RULE_polygonText = 39
    RULE_multiPointText = 40
    RULE_multiLineStringText = 41
    RULE_multiPolygonText = 42
    RULE_geometryCollectionText = 43
    RULE_bboxTaggedText = 44
    RULE_bboxText = 45
    RULE_signedNumber = 46
    RULE_temporalInstant = 47
    RULE_dateInstant = 48
    RULE_timestampInstant = 49
    RULE_intervalInstant = 50
    RULE_instantParameter = 51

    ruleNames =  [ "cql2Text", "booleanExpression", "booleanTerm", "booleanFactor", 
                   "primary", "predicateTail", "comparisonOperator", "inList", 
                   "spatialPredicate", "spatialFunction", "temporalPredicate", 
                   "temporalFunction", "arrayPredicate", "arrayFunction", 
                   "operand", "arithmeticExpr", "arithmeticTerm", "powerTerm", 
                   "arithmeticFactor", "atom", "booleanLiteral", "propertyName", 
                   "functionCall", "argumentList", "arrayExpr", "characterClause", 
                   "characterClauseArg", "geometryLiteral", "pointTaggedText", 
                   "linestringTaggedText", "polygonTaggedText", "multipointTaggedText", 
                   "multilinestringTaggedText", "multipolygonTaggedText", 
                   "geometryCollectionTaggedText", "pointText", "point", 
                   "lineStringText", "linearRingText", "polygonText", "multiPointText", 
                   "multiLineStringText", "multiPolygonText", "geometryCollectionText", 
                   "bboxTaggedText", "bboxText", "signedNumber", "temporalInstant", 
                   "dateInstant", "timestampInstant", "intervalInstant", 
                   "instantParameter" ]

    EOF = Token.EOF
    AND=1
    OR=2
    NOT=3
    LIKE=4
    BETWEEN=5
    IN=6
    IS=7
    NULL=8
    TRUE=9
    FALSE=10
    CASEI=11
    ACCENTI=12
    S_INTERSECTS=13
    S_EQUALS=14
    S_DISJOINT=15
    S_TOUCHES=16
    S_WITHIN=17
    S_OVERLAPS=18
    S_CROSSES=19
    S_CONTAINS=20
    T_AFTER=21
    T_BEFORE=22
    T_CONTAINS=23
    T_DISJOINT=24
    T_DURING=25
    T_EQUALS=26
    T_FINISHEDBY=27
    T_FINISHES=28
    T_INTERSECTS=29
    T_MEETS=30
    T_METBY=31
    T_OVERLAPPEDBY=32
    T_OVERLAPS=33
    T_STARTEDBY=34
    T_STARTS=35
    A_EQUALS=36
    A_CONTAINS=37
    A_CONTAINEDBY=38
    A_OVERLAPS=39
    POINT=40
    LINESTRING=41
    POLYGON=42
    MULTIPOINT=43
    MULTILINESTRING=44
    MULTIPOLYGON=45
    GEOMETRYCOLLECTION=46
    BBOX=47
    ZSUFFIX=48
    DATE=49
    TIMESTAMP=50
    INTERVAL=51
    IDIV=52
    LPAR=53
    RPAR=54
    COMMA=55
    EQ=56
    NEQ=57
    LTEQ=58
    GTEQ=59
    LT=60
    GT=61
    PLUS=62
    MINUS=63
    MUL=64
    SLASH=65
    MOD=66
    POW=67
    NUMERIC_LITERAL=68
    STRING=69
    QUOTED_IDENTIFIER=70
    IDENTIFIER=71
    WS=72

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Cql2TextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def booleanExpression(self):
            return self.getTypedRuleContext(CQL2TextParser.BooleanExpressionContext,0)


        def EOF(self):
            return self.getToken(CQL2TextParser.EOF, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_cql2Text

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCql2Text" ):
                listener.enterCql2Text(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCql2Text" ):
                listener.exitCql2Text(self)




    def cql2Text(self):

        localctx = CQL2TextParser.Cql2TextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_cql2Text)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.booleanExpression()
            self.state = 105
            self.match(CQL2TextParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def booleanTerm(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.BooleanTermContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.BooleanTermContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.OR)
            else:
                return self.getToken(CQL2TextParser.OR, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_booleanExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanExpression" ):
                listener.enterBooleanExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanExpression" ):
                listener.exitBooleanExpression(self)




    def booleanExpression(self):

        localctx = CQL2TextParser.BooleanExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_booleanExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.booleanTerm()
            self.state = 112
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 108
                self.match(CQL2TextParser.OR)
                self.state = 109
                self.booleanTerm()
                self.state = 114
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanTermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def booleanFactor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.BooleanFactorContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.BooleanFactorContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.AND)
            else:
                return self.getToken(CQL2TextParser.AND, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_booleanTerm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanTerm" ):
                listener.enterBooleanTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanTerm" ):
                listener.exitBooleanTerm(self)




    def booleanTerm(self):

        localctx = CQL2TextParser.BooleanTermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_booleanTerm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.booleanFactor()
            self.state = 120
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 116
                self.match(CQL2TextParser.AND)
                self.state = 117
                self.booleanFactor()
                self.state = 122
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanFactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self):
            return self.getTypedRuleContext(CQL2TextParser.PrimaryContext,0)


        def NOT(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.NOT)
            else:
                return self.getToken(CQL2TextParser.NOT, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_booleanFactor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanFactor" ):
                listener.enterBooleanFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanFactor" ):
                listener.exitBooleanFactor(self)




    def booleanFactor(self):

        localctx = CQL2TextParser.BooleanFactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_booleanFactor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3:
                self.state = 123
                self.match(CQL2TextParser.NOT)
                self.state = 128
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 129
            self.primary()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def spatialPredicate(self):
            return self.getTypedRuleContext(CQL2TextParser.SpatialPredicateContext,0)


        def temporalPredicate(self):
            return self.getTypedRuleContext(CQL2TextParser.TemporalPredicateContext,0)


        def arrayPredicate(self):
            return self.getTypedRuleContext(CQL2TextParser.ArrayPredicateContext,0)


        def operand(self):
            return self.getTypedRuleContext(CQL2TextParser.OperandContext,0)


        def predicateTail(self):
            return self.getTypedRuleContext(CQL2TextParser.PredicateTailContext,0)


        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def booleanExpression(self):
            return self.getTypedRuleContext(CQL2TextParser.BooleanExpressionContext,0)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_primary

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimary" ):
                listener.enterPrimary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimary" ):
                listener.exitPrimary(self)




    def primary(self):

        localctx = CQL2TextParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_primary)
        self._la = 0 # Token type
        try:
            self.state = 142
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 131
                self.spatialPredicate()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 132
                self.temporalPredicate()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 133
                self.arrayPredicate()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 134
                self.operand()
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 4539628424389460216) != 0):
                    self.state = 135
                    self.predicateTail()


                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 138
                self.match(CQL2TextParser.LPAR)
                self.state = 139
                self.booleanExpression()
                self.state = 140
                self.match(CQL2TextParser.RPAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateTailContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CQL2TextParser.RULE_predicateTail

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BetweenTailContext(PredicateTailContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CQL2TextParser.PredicateTailContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BETWEEN(self):
            return self.getToken(CQL2TextParser.BETWEEN, 0)
        def arithmeticExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.ArithmeticExprContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.ArithmeticExprContext,i)

        def AND(self):
            return self.getToken(CQL2TextParser.AND, 0)
        def NOT(self):
            return self.getToken(CQL2TextParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBetweenTail" ):
                listener.enterBetweenTail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBetweenTail" ):
                listener.exitBetweenTail(self)


    class ComparisonTailContext(PredicateTailContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CQL2TextParser.PredicateTailContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def comparisonOperator(self):
            return self.getTypedRuleContext(CQL2TextParser.ComparisonOperatorContext,0)

        def operand(self):
            return self.getTypedRuleContext(CQL2TextParser.OperandContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonTail" ):
                listener.enterComparisonTail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonTail" ):
                listener.exitComparisonTail(self)


    class InTailContext(PredicateTailContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CQL2TextParser.PredicateTailContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IN(self):
            return self.getToken(CQL2TextParser.IN, 0)
        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)
        def inList(self):
            return self.getTypedRuleContext(CQL2TextParser.InListContext,0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)
        def NOT(self):
            return self.getToken(CQL2TextParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInTail" ):
                listener.enterInTail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInTail" ):
                listener.exitInTail(self)


    class IsNullTailContext(PredicateTailContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CQL2TextParser.PredicateTailContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IS(self):
            return self.getToken(CQL2TextParser.IS, 0)
        def NULL(self):
            return self.getToken(CQL2TextParser.NULL, 0)
        def NOT(self):
            return self.getToken(CQL2TextParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIsNullTail" ):
                listener.enterIsNullTail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIsNullTail" ):
                listener.exitIsNullTail(self)


    class LikeTailContext(PredicateTailContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CQL2TextParser.PredicateTailContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LIKE(self):
            return self.getToken(CQL2TextParser.LIKE, 0)
        def characterClause(self):
            return self.getTypedRuleContext(CQL2TextParser.CharacterClauseContext,0)

        def NOT(self):
            return self.getToken(CQL2TextParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLikeTail" ):
                listener.enterLikeTail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLikeTail" ):
                listener.exitLikeTail(self)



    def predicateTail(self):

        localctx = CQL2TextParser.PredicateTailContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_predicateTail)
        self._la = 0 # Token type
        try:
            self.state = 173
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                localctx = CQL2TextParser.ComparisonTailContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 144
                self.comparisonOperator()
                self.state = 145
                self.operand()
                pass

            elif la_ == 2:
                localctx = CQL2TextParser.LikeTailContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 148
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==3:
                    self.state = 147
                    self.match(CQL2TextParser.NOT)


                self.state = 150
                self.match(CQL2TextParser.LIKE)
                self.state = 151
                self.characterClause()
                pass

            elif la_ == 3:
                localctx = CQL2TextParser.BetweenTailContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==3:
                    self.state = 152
                    self.match(CQL2TextParser.NOT)


                self.state = 155
                self.match(CQL2TextParser.BETWEEN)
                self.state = 156
                self.arithmeticExpr()
                self.state = 157
                self.match(CQL2TextParser.AND)
                self.state = 158
                self.arithmeticExpr()
                pass

            elif la_ == 4:
                localctx = CQL2TextParser.InTailContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 161
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==3:
                    self.state = 160
                    self.match(CQL2TextParser.NOT)


                self.state = 163
                self.match(CQL2TextParser.IN)
                self.state = 164
                self.match(CQL2TextParser.LPAR)
                self.state = 165
                self.inList()
                self.state = 166
                self.match(CQL2TextParser.RPAR)
                pass

            elif la_ == 5:
                localctx = CQL2TextParser.IsNullTailContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 168
                self.match(CQL2TextParser.IS)
                self.state = 170
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==3:
                    self.state = 169
                    self.match(CQL2TextParser.NOT)


                self.state = 172
                self.match(CQL2TextParser.NULL)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(CQL2TextParser.EQ, 0)

        def NEQ(self):
            return self.getToken(CQL2TextParser.NEQ, 0)

        def LTEQ(self):
            return self.getToken(CQL2TextParser.LTEQ, 0)

        def GTEQ(self):
            return self.getToken(CQL2TextParser.GTEQ, 0)

        def LT(self):
            return self.getToken(CQL2TextParser.LT, 0)

        def GT(self):
            return self.getToken(CQL2TextParser.GT, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_comparisonOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonOperator" ):
                listener.enterComparisonOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonOperator" ):
                listener.exitComparisonOperator(self)




    def comparisonOperator(self):

        localctx = CQL2TextParser.ComparisonOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_comparisonOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4539628424389459968) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.OperandContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.OperandContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_inList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInList" ):
                listener.enterInList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInList" ):
                listener.exitInList(self)




    def inList(self):

        localctx = CQL2TextParser.InListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_inList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self.operand()
            self.state = 182
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==55:
                self.state = 178
                self.match(CQL2TextParser.COMMA)
                self.state = 179
                self.operand()
                self.state = 184
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SpatialPredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def spatialFunction(self):
            return self.getTypedRuleContext(CQL2TextParser.SpatialFunctionContext,0)


        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.OperandContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.OperandContext,i)


        def COMMA(self):
            return self.getToken(CQL2TextParser.COMMA, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_spatialPredicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpatialPredicate" ):
                listener.enterSpatialPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpatialPredicate" ):
                listener.exitSpatialPredicate(self)




    def spatialPredicate(self):

        localctx = CQL2TextParser.SpatialPredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_spatialPredicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.spatialFunction()
            self.state = 186
            self.match(CQL2TextParser.LPAR)
            self.state = 187
            self.operand()
            self.state = 188
            self.match(CQL2TextParser.COMMA)
            self.state = 189
            self.operand()
            self.state = 190
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SpatialFunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def S_INTERSECTS(self):
            return self.getToken(CQL2TextParser.S_INTERSECTS, 0)

        def S_EQUALS(self):
            return self.getToken(CQL2TextParser.S_EQUALS, 0)

        def S_DISJOINT(self):
            return self.getToken(CQL2TextParser.S_DISJOINT, 0)

        def S_TOUCHES(self):
            return self.getToken(CQL2TextParser.S_TOUCHES, 0)

        def S_WITHIN(self):
            return self.getToken(CQL2TextParser.S_WITHIN, 0)

        def S_OVERLAPS(self):
            return self.getToken(CQL2TextParser.S_OVERLAPS, 0)

        def S_CROSSES(self):
            return self.getToken(CQL2TextParser.S_CROSSES, 0)

        def S_CONTAINS(self):
            return self.getToken(CQL2TextParser.S_CONTAINS, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_spatialFunction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpatialFunction" ):
                listener.enterSpatialFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpatialFunction" ):
                listener.exitSpatialFunction(self)




    def spatialFunction(self):

        localctx = CQL2TextParser.SpatialFunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_spatialFunction)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2088960) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TemporalPredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def temporalFunction(self):
            return self.getTypedRuleContext(CQL2TextParser.TemporalFunctionContext,0)


        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.OperandContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.OperandContext,i)


        def COMMA(self):
            return self.getToken(CQL2TextParser.COMMA, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_temporalPredicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemporalPredicate" ):
                listener.enterTemporalPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemporalPredicate" ):
                listener.exitTemporalPredicate(self)




    def temporalPredicate(self):

        localctx = CQL2TextParser.TemporalPredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_temporalPredicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.temporalFunction()
            self.state = 195
            self.match(CQL2TextParser.LPAR)
            self.state = 196
            self.operand()
            self.state = 197
            self.match(CQL2TextParser.COMMA)
            self.state = 198
            self.operand()
            self.state = 199
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TemporalFunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_AFTER(self):
            return self.getToken(CQL2TextParser.T_AFTER, 0)

        def T_BEFORE(self):
            return self.getToken(CQL2TextParser.T_BEFORE, 0)

        def T_CONTAINS(self):
            return self.getToken(CQL2TextParser.T_CONTAINS, 0)

        def T_DISJOINT(self):
            return self.getToken(CQL2TextParser.T_DISJOINT, 0)

        def T_DURING(self):
            return self.getToken(CQL2TextParser.T_DURING, 0)

        def T_EQUALS(self):
            return self.getToken(CQL2TextParser.T_EQUALS, 0)

        def T_FINISHEDBY(self):
            return self.getToken(CQL2TextParser.T_FINISHEDBY, 0)

        def T_FINISHES(self):
            return self.getToken(CQL2TextParser.T_FINISHES, 0)

        def T_INTERSECTS(self):
            return self.getToken(CQL2TextParser.T_INTERSECTS, 0)

        def T_MEETS(self):
            return self.getToken(CQL2TextParser.T_MEETS, 0)

        def T_METBY(self):
            return self.getToken(CQL2TextParser.T_METBY, 0)

        def T_OVERLAPPEDBY(self):
            return self.getToken(CQL2TextParser.T_OVERLAPPEDBY, 0)

        def T_OVERLAPS(self):
            return self.getToken(CQL2TextParser.T_OVERLAPS, 0)

        def T_STARTEDBY(self):
            return self.getToken(CQL2TextParser.T_STARTEDBY, 0)

        def T_STARTS(self):
            return self.getToken(CQL2TextParser.T_STARTS, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_temporalFunction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemporalFunction" ):
                listener.enterTemporalFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemporalFunction" ):
                listener.exitTemporalFunction(self)




    def temporalFunction(self):

        localctx = CQL2TextParser.TemporalFunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_temporalFunction)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 201
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 68717379584) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayPredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arrayFunction(self):
            return self.getTypedRuleContext(CQL2TextParser.ArrayFunctionContext,0)


        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.OperandContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.OperandContext,i)


        def COMMA(self):
            return self.getToken(CQL2TextParser.COMMA, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_arrayPredicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayPredicate" ):
                listener.enterArrayPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayPredicate" ):
                listener.exitArrayPredicate(self)




    def arrayPredicate(self):

        localctx = CQL2TextParser.ArrayPredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_arrayPredicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 203
            self.arrayFunction()
            self.state = 204
            self.match(CQL2TextParser.LPAR)
            self.state = 205
            self.operand()
            self.state = 206
            self.match(CQL2TextParser.COMMA)
            self.state = 207
            self.operand()
            self.state = 208
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayFunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def A_EQUALS(self):
            return self.getToken(CQL2TextParser.A_EQUALS, 0)

        def A_CONTAINS(self):
            return self.getToken(CQL2TextParser.A_CONTAINS, 0)

        def A_CONTAINEDBY(self):
            return self.getToken(CQL2TextParser.A_CONTAINEDBY, 0)

        def A_OVERLAPS(self):
            return self.getToken(CQL2TextParser.A_OVERLAPS, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_arrayFunction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayFunction" ):
                listener.enterArrayFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayFunction" ):
                listener.exitArrayFunction(self)




    def arrayFunction(self):

        localctx = CQL2TextParser.ArrayFunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_arrayFunction)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1030792151040) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arithmeticExpr(self):
            return self.getTypedRuleContext(CQL2TextParser.ArithmeticExprContext,0)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_operand

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperand" ):
                listener.enterOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperand" ):
                listener.exitOperand(self)




    def operand(self):

        localctx = CQL2TextParser.OperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_operand)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.arithmeticExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arithmeticTerm(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.ArithmeticTermContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.ArithmeticTermContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.PLUS)
            else:
                return self.getToken(CQL2TextParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.MINUS)
            else:
                return self.getToken(CQL2TextParser.MINUS, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_arithmeticExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticExpr" ):
                listener.enterArithmeticExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticExpr" ):
                listener.exitArithmeticExpr(self)




    def arithmeticExpr(self):

        localctx = CQL2TextParser.ArithmeticExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_arithmeticExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 214
            self.arithmeticTerm()
            self.state = 219
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==62 or _la==63:
                self.state = 215
                _la = self._input.LA(1)
                if not(_la==62 or _la==63):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 216
                self.arithmeticTerm()
                self.state = 221
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticTermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def powerTerm(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.PowerTermContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.PowerTermContext,i)


        def MUL(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.MUL)
            else:
                return self.getToken(CQL2TextParser.MUL, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.SLASH)
            else:
                return self.getToken(CQL2TextParser.SLASH, i)

        def IDIV(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.IDIV)
            else:
                return self.getToken(CQL2TextParser.IDIV, i)

        def MOD(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.MOD)
            else:
                return self.getToken(CQL2TextParser.MOD, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_arithmeticTerm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticTerm" ):
                listener.enterArithmeticTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticTerm" ):
                listener.exitArithmeticTerm(self)




    def arithmeticTerm(self):

        localctx = CQL2TextParser.ArithmeticTermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_arithmeticTerm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 222
            self.powerTerm()
            self.state = 227
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 52)) & ~0x3f) == 0 and ((1 << (_la - 52)) & 28673) != 0):
                self.state = 223
                _la = self._input.LA(1)
                if not(((((_la - 52)) & ~0x3f) == 0 and ((1 << (_la - 52)) & 28673) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 224
                self.powerTerm()
                self.state = 229
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PowerTermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arithmeticFactor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.ArithmeticFactorContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.ArithmeticFactorContext,i)


        def POW(self):
            return self.getToken(CQL2TextParser.POW, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_powerTerm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPowerTerm" ):
                listener.enterPowerTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPowerTerm" ):
                listener.exitPowerTerm(self)




    def powerTerm(self):

        localctx = CQL2TextParser.PowerTermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_powerTerm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 230
            self.arithmeticFactor()
            self.state = 233
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==67:
                self.state = 231
                self.match(CQL2TextParser.POW)
                self.state = 232
                self.arithmeticFactor()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticFactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def arithmeticExpr(self):
            return self.getTypedRuleContext(CQL2TextParser.ArithmeticExprContext,0)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def atom(self):
            return self.getTypedRuleContext(CQL2TextParser.AtomContext,0)


        def MINUS(self):
            return self.getToken(CQL2TextParser.MINUS, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_arithmeticFactor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticFactor" ):
                listener.enterArithmeticFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticFactor" ):
                listener.exitArithmeticFactor(self)




    def arithmeticFactor(self):

        localctx = CQL2TextParser.ArithmeticFactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_arithmeticFactor)
        self._la = 0 # Token type
        try:
            self.state = 243
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 235
                self.match(CQL2TextParser.LPAR)
                self.state = 236
                self.arithmeticExpr()
                self.state = 237
                self.match(CQL2TextParser.RPAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 240
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==63:
                    self.state = 239
                    self.match(CQL2TextParser.MINUS)


                self.state = 242
                self.atom()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def geometryLiteral(self):
            return self.getTypedRuleContext(CQL2TextParser.GeometryLiteralContext,0)


        def temporalInstant(self):
            return self.getTypedRuleContext(CQL2TextParser.TemporalInstantContext,0)


        def characterClause(self):
            return self.getTypedRuleContext(CQL2TextParser.CharacterClauseContext,0)


        def NUMERIC_LITERAL(self):
            return self.getToken(CQL2TextParser.NUMERIC_LITERAL, 0)

        def booleanLiteral(self):
            return self.getTypedRuleContext(CQL2TextParser.BooleanLiteralContext,0)


        def propertyName(self):
            return self.getTypedRuleContext(CQL2TextParser.PropertyNameContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(CQL2TextParser.FunctionCallContext,0)


        def arrayExpr(self):
            return self.getTypedRuleContext(CQL2TextParser.ArrayExprContext,0)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)




    def atom(self):

        localctx = CQL2TextParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_atom)
        try:
            self.state = 253
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 245
                self.geometryLiteral()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 246
                self.temporalInstant()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 247
                self.characterClause()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 248
                self.match(CQL2TextParser.NUMERIC_LITERAL)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 249
                self.booleanLiteral()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 250
                self.propertyName()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 251
                self.functionCall()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 252
                self.arrayExpr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(CQL2TextParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(CQL2TextParser.FALSE, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_booleanLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanLiteral" ):
                listener.enterBooleanLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanLiteral" ):
                listener.exitBooleanLiteral(self)




    def booleanLiteral(self):

        localctx = CQL2TextParser.BooleanLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_booleanLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 255
            _la = self._input.LA(1)
            if not(_la==9 or _la==10):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CQL2TextParser.IDENTIFIER, 0)

        def QUOTED_IDENTIFIER(self):
            return self.getToken(CQL2TextParser.QUOTED_IDENTIFIER, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_propertyName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyName" ):
                listener.enterPropertyName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyName" ):
                listener.exitPropertyName(self)




    def propertyName(self):

        localctx = CQL2TextParser.PropertyNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_propertyName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            _la = self._input.LA(1)
            if not(_la==70 or _la==71):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CQL2TextParser.IDENTIFIER, 0)

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def argumentList(self):
            return self.getTypedRuleContext(CQL2TextParser.ArgumentListContext,0)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)




    def functionCall(self):

        localctx = CQL2TextParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 259
            self.match(CQL2TextParser.IDENTIFIER)
            self.state = 260
            self.match(CQL2TextParser.LPAR)
            self.state = 262
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 9)) & ~0x3f) == 0 and ((1 << (_la - 9)) & 8664951519436603407) != 0):
                self.state = 261
                self.argumentList()


            self.state = 264
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.OperandContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.OperandContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_argumentList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgumentList" ):
                listener.enterArgumentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgumentList" ):
                listener.exitArgumentList(self)




    def argumentList(self):

        localctx = CQL2TextParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 266
            self.operand()
            self.state = 271
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==55:
                self.state = 267
                self.match(CQL2TextParser.COMMA)
                self.state = 268
                self.operand()
                self.state = 273
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.OperandContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.OperandContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_arrayExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayExpr" ):
                listener.enterArrayExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayExpr" ):
                listener.exitArrayExpr(self)




    def arrayExpr(self):

        localctx = CQL2TextParser.ArrayExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_arrayExpr)
        self._la = 0 # Token type
        try:
            self.state = 286
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 274
                self.match(CQL2TextParser.LPAR)
                self.state = 275
                self.match(CQL2TextParser.RPAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 276
                self.match(CQL2TextParser.LPAR)
                self.state = 277
                self.operand()
                self.state = 280 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 278
                    self.match(CQL2TextParser.COMMA)
                    self.state = 279
                    self.operand()
                    self.state = 282 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==55):
                        break

                self.state = 284
                self.match(CQL2TextParser.RPAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CASEI(self):
            return self.getToken(CQL2TextParser.CASEI, 0)

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def characterClauseArg(self):
            return self.getTypedRuleContext(CQL2TextParser.CharacterClauseArgContext,0)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def ACCENTI(self):
            return self.getToken(CQL2TextParser.ACCENTI, 0)

        def STRING(self):
            return self.getToken(CQL2TextParser.STRING, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_characterClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterClause" ):
                listener.enterCharacterClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterClause" ):
                listener.exitCharacterClause(self)




    def characterClause(self):

        localctx = CQL2TextParser.CharacterClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_characterClause)
        try:
            self.state = 299
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 288
                self.match(CQL2TextParser.CASEI)
                self.state = 289
                self.match(CQL2TextParser.LPAR)
                self.state = 290
                self.characterClauseArg()
                self.state = 291
                self.match(CQL2TextParser.RPAR)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 293
                self.match(CQL2TextParser.ACCENTI)
                self.state = 294
                self.match(CQL2TextParser.LPAR)
                self.state = 295
                self.characterClauseArg()
                self.state = 296
                self.match(CQL2TextParser.RPAR)
                pass
            elif token in [69]:
                self.enterOuterAlt(localctx, 3)
                self.state = 298
                self.match(CQL2TextParser.STRING)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterClauseArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def characterClause(self):
            return self.getTypedRuleContext(CQL2TextParser.CharacterClauseContext,0)


        def propertyName(self):
            return self.getTypedRuleContext(CQL2TextParser.PropertyNameContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(CQL2TextParser.FunctionCallContext,0)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_characterClauseArg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterClauseArg" ):
                listener.enterCharacterClauseArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterClauseArg" ):
                listener.exitCharacterClauseArg(self)




    def characterClauseArg(self):

        localctx = CQL2TextParser.CharacterClauseArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_characterClauseArg)
        try:
            self.state = 304
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 301
                self.characterClause()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 302
                self.propertyName()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 303
                self.functionCall()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GeometryLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pointTaggedText(self):
            return self.getTypedRuleContext(CQL2TextParser.PointTaggedTextContext,0)


        def linestringTaggedText(self):
            return self.getTypedRuleContext(CQL2TextParser.LinestringTaggedTextContext,0)


        def polygonTaggedText(self):
            return self.getTypedRuleContext(CQL2TextParser.PolygonTaggedTextContext,0)


        def multipointTaggedText(self):
            return self.getTypedRuleContext(CQL2TextParser.MultipointTaggedTextContext,0)


        def multilinestringTaggedText(self):
            return self.getTypedRuleContext(CQL2TextParser.MultilinestringTaggedTextContext,0)


        def multipolygonTaggedText(self):
            return self.getTypedRuleContext(CQL2TextParser.MultipolygonTaggedTextContext,0)


        def geometryCollectionTaggedText(self):
            return self.getTypedRuleContext(CQL2TextParser.GeometryCollectionTaggedTextContext,0)


        def bboxTaggedText(self):
            return self.getTypedRuleContext(CQL2TextParser.BboxTaggedTextContext,0)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_geometryLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGeometryLiteral" ):
                listener.enterGeometryLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGeometryLiteral" ):
                listener.exitGeometryLiteral(self)




    def geometryLiteral(self):

        localctx = CQL2TextParser.GeometryLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_geometryLiteral)
        try:
            self.state = 314
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [40]:
                self.enterOuterAlt(localctx, 1)
                self.state = 306
                self.pointTaggedText()
                pass
            elif token in [41]:
                self.enterOuterAlt(localctx, 2)
                self.state = 307
                self.linestringTaggedText()
                pass
            elif token in [42]:
                self.enterOuterAlt(localctx, 3)
                self.state = 308
                self.polygonTaggedText()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 4)
                self.state = 309
                self.multipointTaggedText()
                pass
            elif token in [44]:
                self.enterOuterAlt(localctx, 5)
                self.state = 310
                self.multilinestringTaggedText()
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 6)
                self.state = 311
                self.multipolygonTaggedText()
                pass
            elif token in [46]:
                self.enterOuterAlt(localctx, 7)
                self.state = 312
                self.geometryCollectionTaggedText()
                pass
            elif token in [47]:
                self.enterOuterAlt(localctx, 8)
                self.state = 313
                self.bboxTaggedText()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PointTaggedTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def POINT(self):
            return self.getToken(CQL2TextParser.POINT, 0)

        def pointText(self):
            return self.getTypedRuleContext(CQL2TextParser.PointTextContext,0)


        def ZSUFFIX(self):
            return self.getToken(CQL2TextParser.ZSUFFIX, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_pointTaggedText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPointTaggedText" ):
                listener.enterPointTaggedText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPointTaggedText" ):
                listener.exitPointTaggedText(self)




    def pointTaggedText(self):

        localctx = CQL2TextParser.PointTaggedTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_pointTaggedText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 316
            self.match(CQL2TextParser.POINT)
            self.state = 318
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 317
                self.match(CQL2TextParser.ZSUFFIX)


            self.state = 320
            self.pointText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LinestringTaggedTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LINESTRING(self):
            return self.getToken(CQL2TextParser.LINESTRING, 0)

        def lineStringText(self):
            return self.getTypedRuleContext(CQL2TextParser.LineStringTextContext,0)


        def ZSUFFIX(self):
            return self.getToken(CQL2TextParser.ZSUFFIX, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_linestringTaggedText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLinestringTaggedText" ):
                listener.enterLinestringTaggedText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLinestringTaggedText" ):
                listener.exitLinestringTaggedText(self)




    def linestringTaggedText(self):

        localctx = CQL2TextParser.LinestringTaggedTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_linestringTaggedText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 322
            self.match(CQL2TextParser.LINESTRING)
            self.state = 324
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 323
                self.match(CQL2TextParser.ZSUFFIX)


            self.state = 326
            self.lineStringText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PolygonTaggedTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def POLYGON(self):
            return self.getToken(CQL2TextParser.POLYGON, 0)

        def polygonText(self):
            return self.getTypedRuleContext(CQL2TextParser.PolygonTextContext,0)


        def ZSUFFIX(self):
            return self.getToken(CQL2TextParser.ZSUFFIX, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_polygonTaggedText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPolygonTaggedText" ):
                listener.enterPolygonTaggedText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPolygonTaggedText" ):
                listener.exitPolygonTaggedText(self)




    def polygonTaggedText(self):

        localctx = CQL2TextParser.PolygonTaggedTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_polygonTaggedText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 328
            self.match(CQL2TextParser.POLYGON)
            self.state = 330
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 329
                self.match(CQL2TextParser.ZSUFFIX)


            self.state = 332
            self.polygonText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultipointTaggedTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MULTIPOINT(self):
            return self.getToken(CQL2TextParser.MULTIPOINT, 0)

        def multiPointText(self):
            return self.getTypedRuleContext(CQL2TextParser.MultiPointTextContext,0)


        def ZSUFFIX(self):
            return self.getToken(CQL2TextParser.ZSUFFIX, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_multipointTaggedText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultipointTaggedText" ):
                listener.enterMultipointTaggedText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultipointTaggedText" ):
                listener.exitMultipointTaggedText(self)




    def multipointTaggedText(self):

        localctx = CQL2TextParser.MultipointTaggedTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_multipointTaggedText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 334
            self.match(CQL2TextParser.MULTIPOINT)
            self.state = 336
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 335
                self.match(CQL2TextParser.ZSUFFIX)


            self.state = 338
            self.multiPointText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultilinestringTaggedTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MULTILINESTRING(self):
            return self.getToken(CQL2TextParser.MULTILINESTRING, 0)

        def multiLineStringText(self):
            return self.getTypedRuleContext(CQL2TextParser.MultiLineStringTextContext,0)


        def ZSUFFIX(self):
            return self.getToken(CQL2TextParser.ZSUFFIX, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_multilinestringTaggedText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultilinestringTaggedText" ):
                listener.enterMultilinestringTaggedText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultilinestringTaggedText" ):
                listener.exitMultilinestringTaggedText(self)




    def multilinestringTaggedText(self):

        localctx = CQL2TextParser.MultilinestringTaggedTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_multilinestringTaggedText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 340
            self.match(CQL2TextParser.MULTILINESTRING)
            self.state = 342
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 341
                self.match(CQL2TextParser.ZSUFFIX)


            self.state = 344
            self.multiLineStringText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultipolygonTaggedTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MULTIPOLYGON(self):
            return self.getToken(CQL2TextParser.MULTIPOLYGON, 0)

        def multiPolygonText(self):
            return self.getTypedRuleContext(CQL2TextParser.MultiPolygonTextContext,0)


        def ZSUFFIX(self):
            return self.getToken(CQL2TextParser.ZSUFFIX, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_multipolygonTaggedText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultipolygonTaggedText" ):
                listener.enterMultipolygonTaggedText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultipolygonTaggedText" ):
                listener.exitMultipolygonTaggedText(self)




    def multipolygonTaggedText(self):

        localctx = CQL2TextParser.MultipolygonTaggedTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_multipolygonTaggedText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 346
            self.match(CQL2TextParser.MULTIPOLYGON)
            self.state = 348
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 347
                self.match(CQL2TextParser.ZSUFFIX)


            self.state = 350
            self.multiPolygonText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GeometryCollectionTaggedTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GEOMETRYCOLLECTION(self):
            return self.getToken(CQL2TextParser.GEOMETRYCOLLECTION, 0)

        def geometryCollectionText(self):
            return self.getTypedRuleContext(CQL2TextParser.GeometryCollectionTextContext,0)


        def ZSUFFIX(self):
            return self.getToken(CQL2TextParser.ZSUFFIX, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_geometryCollectionTaggedText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGeometryCollectionTaggedText" ):
                listener.enterGeometryCollectionTaggedText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGeometryCollectionTaggedText" ):
                listener.exitGeometryCollectionTaggedText(self)




    def geometryCollectionTaggedText(self):

        localctx = CQL2TextParser.GeometryCollectionTaggedTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_geometryCollectionTaggedText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 352
            self.match(CQL2TextParser.GEOMETRYCOLLECTION)
            self.state = 354
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 353
                self.match(CQL2TextParser.ZSUFFIX)


            self.state = 356
            self.geometryCollectionText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PointTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def point(self):
            return self.getTypedRuleContext(CQL2TextParser.PointContext,0)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_pointText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPointText" ):
                listener.enterPointText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPointText" ):
                listener.exitPointText(self)




    def pointText(self):

        localctx = CQL2TextParser.PointTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_pointText)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 358
            self.match(CQL2TextParser.LPAR)
            self.state = 359
            self.point()
            self.state = 360
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PointContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def signedNumber(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.SignedNumberContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.SignedNumberContext,i)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_point

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPoint" ):
                listener.enterPoint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPoint" ):
                listener.exitPoint(self)




    def point(self):

        localctx = CQL2TextParser.PointContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_point)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 362
            self.signedNumber()
            self.state = 363
            self.signedNumber()
            self.state = 365
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==63 or _la==68:
                self.state = 364
                self.signedNumber()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineStringTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def point(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.PointContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.PointContext,i)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_lineStringText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineStringText" ):
                listener.enterLineStringText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineStringText" ):
                listener.exitLineStringText(self)




    def lineStringText(self):

        localctx = CQL2TextParser.LineStringTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_lineStringText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 367
            self.match(CQL2TextParser.LPAR)
            self.state = 368
            self.point()
            self.state = 371 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 369
                self.match(CQL2TextParser.COMMA)
                self.state = 370
                self.point()
                self.state = 373 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==55):
                    break

            self.state = 375
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LinearRingTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def point(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.PointContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.PointContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_linearRingText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLinearRingText" ):
                listener.enterLinearRingText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLinearRingText" ):
                listener.exitLinearRingText(self)




    def linearRingText(self):

        localctx = CQL2TextParser.LinearRingTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_linearRingText)
        self._la = 0 # Token type
        try:
            self.state = 396
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,34,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 377
                self.match(CQL2TextParser.LPAR)
                self.state = 378
                self.match(CQL2TextParser.RPAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 379
                self.match(CQL2TextParser.LPAR)
                self.state = 380
                self.point()
                self.state = 381
                self.match(CQL2TextParser.COMMA)
                self.state = 382
                self.point()
                self.state = 383
                self.match(CQL2TextParser.COMMA)
                self.state = 384
                self.point()
                self.state = 385
                self.match(CQL2TextParser.COMMA)
                self.state = 386
                self.point()
                self.state = 391
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==55:
                    self.state = 387
                    self.match(CQL2TextParser.COMMA)
                    self.state = 388
                    self.point()
                    self.state = 393
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 394
                self.match(CQL2TextParser.RPAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PolygonTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def linearRingText(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.LinearRingTextContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.LinearRingTextContext,i)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_polygonText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPolygonText" ):
                listener.enterPolygonText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPolygonText" ):
                listener.exitPolygonText(self)




    def polygonText(self):

        localctx = CQL2TextParser.PolygonTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_polygonText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 398
            self.match(CQL2TextParser.LPAR)
            self.state = 399
            self.linearRingText()
            self.state = 404
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==55:
                self.state = 400
                self.match(CQL2TextParser.COMMA)
                self.state = 401
                self.linearRingText()
                self.state = 406
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 407
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiPointTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def pointText(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.PointTextContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.PointTextContext,i)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_multiPointText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiPointText" ):
                listener.enterMultiPointText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiPointText" ):
                listener.exitMultiPointText(self)




    def multiPointText(self):

        localctx = CQL2TextParser.MultiPointTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_multiPointText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 409
            self.match(CQL2TextParser.LPAR)
            self.state = 410
            self.pointText()
            self.state = 415
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==55:
                self.state = 411
                self.match(CQL2TextParser.COMMA)
                self.state = 412
                self.pointText()
                self.state = 417
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 418
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiLineStringTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def lineStringText(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.LineStringTextContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.LineStringTextContext,i)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_multiLineStringText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiLineStringText" ):
                listener.enterMultiLineStringText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiLineStringText" ):
                listener.exitMultiLineStringText(self)




    def multiLineStringText(self):

        localctx = CQL2TextParser.MultiLineStringTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_multiLineStringText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 420
            self.match(CQL2TextParser.LPAR)
            self.state = 421
            self.lineStringText()
            self.state = 426
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==55:
                self.state = 422
                self.match(CQL2TextParser.COMMA)
                self.state = 423
                self.lineStringText()
                self.state = 428
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 429
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiPolygonTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def polygonText(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.PolygonTextContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.PolygonTextContext,i)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_multiPolygonText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiPolygonText" ):
                listener.enterMultiPolygonText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiPolygonText" ):
                listener.exitMultiPolygonText(self)




    def multiPolygonText(self):

        localctx = CQL2TextParser.MultiPolygonTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_multiPolygonText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 431
            self.match(CQL2TextParser.LPAR)
            self.state = 432
            self.polygonText()
            self.state = 437
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==55:
                self.state = 433
                self.match(CQL2TextParser.COMMA)
                self.state = 434
                self.polygonText()
                self.state = 439
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 440
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GeometryCollectionTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def geometryLiteral(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.GeometryLiteralContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.GeometryLiteralContext,i)


        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_geometryCollectionText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGeometryCollectionText" ):
                listener.enterGeometryCollectionText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGeometryCollectionText" ):
                listener.exitGeometryCollectionText(self)




    def geometryCollectionText(self):

        localctx = CQL2TextParser.GeometryCollectionTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_geometryCollectionText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 442
            self.match(CQL2TextParser.LPAR)
            self.state = 443
            self.geometryLiteral()
            self.state = 448
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==55:
                self.state = 444
                self.match(CQL2TextParser.COMMA)
                self.state = 445
                self.geometryLiteral()
                self.state = 450
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 451
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BboxTaggedTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BBOX(self):
            return self.getToken(CQL2TextParser.BBOX, 0)

        def bboxText(self):
            return self.getTypedRuleContext(CQL2TextParser.BboxTextContext,0)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_bboxTaggedText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBboxTaggedText" ):
                listener.enterBboxTaggedText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBboxTaggedText" ):
                listener.exitBboxTaggedText(self)




    def bboxTaggedText(self):

        localctx = CQL2TextParser.BboxTaggedTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_bboxTaggedText)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 453
            self.match(CQL2TextParser.BBOX)
            self.state = 454
            self.bboxText()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BboxTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def signedNumber(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.SignedNumberContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.SignedNumberContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CQL2TextParser.COMMA)
            else:
                return self.getToken(CQL2TextParser.COMMA, i)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_bboxText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBboxText" ):
                listener.enterBboxText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBboxText" ):
                listener.exitBboxText(self)




    def bboxText(self):

        localctx = CQL2TextParser.BboxTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_bboxText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 456
            self.match(CQL2TextParser.LPAR)
            self.state = 457
            self.signedNumber()
            self.state = 458
            self.match(CQL2TextParser.COMMA)
            self.state = 459
            self.signedNumber()
            self.state = 460
            self.match(CQL2TextParser.COMMA)
            self.state = 464
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
            if la_ == 1:
                self.state = 461
                self.signedNumber()
                self.state = 462
                self.match(CQL2TextParser.COMMA)


            self.state = 466
            self.signedNumber()
            self.state = 467
            self.match(CQL2TextParser.COMMA)
            self.state = 468
            self.signedNumber()
            self.state = 471
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==55:
                self.state = 469
                self.match(CQL2TextParser.COMMA)
                self.state = 470
                self.signedNumber()


            self.state = 473
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SignedNumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMERIC_LITERAL(self):
            return self.getToken(CQL2TextParser.NUMERIC_LITERAL, 0)

        def MINUS(self):
            return self.getToken(CQL2TextParser.MINUS, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_signedNumber

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSignedNumber" ):
                listener.enterSignedNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSignedNumber" ):
                listener.exitSignedNumber(self)




    def signedNumber(self):

        localctx = CQL2TextParser.SignedNumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_signedNumber)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 476
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==63:
                self.state = 475
                self.match(CQL2TextParser.MINUS)


            self.state = 478
            self.match(CQL2TextParser.NUMERIC_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TemporalInstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dateInstant(self):
            return self.getTypedRuleContext(CQL2TextParser.DateInstantContext,0)


        def timestampInstant(self):
            return self.getTypedRuleContext(CQL2TextParser.TimestampInstantContext,0)


        def intervalInstant(self):
            return self.getTypedRuleContext(CQL2TextParser.IntervalInstantContext,0)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_temporalInstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemporalInstant" ):
                listener.enterTemporalInstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemporalInstant" ):
                listener.exitTemporalInstant(self)




    def temporalInstant(self):

        localctx = CQL2TextParser.TemporalInstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_temporalInstant)
        try:
            self.state = 483
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [49]:
                self.enterOuterAlt(localctx, 1)
                self.state = 480
                self.dateInstant()
                pass
            elif token in [50]:
                self.enterOuterAlt(localctx, 2)
                self.state = 481
                self.timestampInstant()
                pass
            elif token in [51]:
                self.enterOuterAlt(localctx, 3)
                self.state = 482
                self.intervalInstant()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateInstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DATE(self):
            return self.getToken(CQL2TextParser.DATE, 0)

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def STRING(self):
            return self.getToken(CQL2TextParser.STRING, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_dateInstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateInstant" ):
                listener.enterDateInstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateInstant" ):
                listener.exitDateInstant(self)




    def dateInstant(self):

        localctx = CQL2TextParser.DateInstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_dateInstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 485
            self.match(CQL2TextParser.DATE)
            self.state = 486
            self.match(CQL2TextParser.LPAR)
            self.state = 487
            self.match(CQL2TextParser.STRING)
            self.state = 488
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimestampInstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TIMESTAMP(self):
            return self.getToken(CQL2TextParser.TIMESTAMP, 0)

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def STRING(self):
            return self.getToken(CQL2TextParser.STRING, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_timestampInstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimestampInstant" ):
                listener.enterTimestampInstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimestampInstant" ):
                listener.exitTimestampInstant(self)




    def timestampInstant(self):

        localctx = CQL2TextParser.TimestampInstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_timestampInstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 490
            self.match(CQL2TextParser.TIMESTAMP)
            self.state = 491
            self.match(CQL2TextParser.LPAR)
            self.state = 492
            self.match(CQL2TextParser.STRING)
            self.state = 493
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntervalInstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTERVAL(self):
            return self.getToken(CQL2TextParser.INTERVAL, 0)

        def LPAR(self):
            return self.getToken(CQL2TextParser.LPAR, 0)

        def instantParameter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CQL2TextParser.InstantParameterContext)
            else:
                return self.getTypedRuleContext(CQL2TextParser.InstantParameterContext,i)


        def COMMA(self):
            return self.getToken(CQL2TextParser.COMMA, 0)

        def RPAR(self):
            return self.getToken(CQL2TextParser.RPAR, 0)

        def getRuleIndex(self):
            return CQL2TextParser.RULE_intervalInstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntervalInstant" ):
                listener.enterIntervalInstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntervalInstant" ):
                listener.exitIntervalInstant(self)




    def intervalInstant(self):

        localctx = CQL2TextParser.IntervalInstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_intervalInstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 495
            self.match(CQL2TextParser.INTERVAL)
            self.state = 496
            self.match(CQL2TextParser.LPAR)
            self.state = 497
            self.instantParameter()
            self.state = 498
            self.match(CQL2TextParser.COMMA)
            self.state = 499
            self.instantParameter()
            self.state = 500
            self.match(CQL2TextParser.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstantParameterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(CQL2TextParser.STRING, 0)

        def propertyName(self):
            return self.getTypedRuleContext(CQL2TextParser.PropertyNameContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(CQL2TextParser.FunctionCallContext,0)


        def getRuleIndex(self):
            return CQL2TextParser.RULE_instantParameter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInstantParameter" ):
                listener.enterInstantParameter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInstantParameter" ):
                listener.exitInstantParameter(self)




    def instantParameter(self):

        localctx = CQL2TextParser.InstantParameterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_instantParameter)
        try:
            self.state = 505
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,44,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 502
                self.match(CQL2TextParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 503
                self.propertyName()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 504
                self.functionCall()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






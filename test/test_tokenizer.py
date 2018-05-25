# -*- encoding: utf-8 -*-
"""

    test_tokenizer.py

    Tests for Tokenizer module

    Copyright(C) 2018 by Miðeind ehf.
    Original author: Vilhjálmur Þorsteinsson

    This software is licensed under the MIT License:

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without restriction,
        including without limitation the rights to use, copy, modify, merge,
        publish, distribute, sublicense, and/or sell copies of the Software,
        and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import tokenizer as t


TOK = t.TOK
Tok = t.Tok


def test_single_tokens():

    TEST_CASES = [
        (".", TOK.PUNCTUATION),
        (",", TOK.PUNCTUATION),
        ("!", TOK.PUNCTUATION),
        ("\"", [ Tok(TOK.PUNCTUATION, "“", None) ]),
        ("13:45", [ Tok(TOK.TIME, "13:45", (13,45,0)) ]),
        ("kl. 13:45", [ Tok(TOK.TIME, "kl. 13:45", (13,45,0)) ]),
        ("klukkan 13:45", [ Tok(TOK.TIME, "klukkan 13:45", (13,45,0)) ]),
        ("Klukkan 13:45", [ Tok(TOK.TIME, "Klukkan 13:45", (13,45,0)) ]),
        ("hálftólf", [ Tok(TOK.TIME, "hálftólf", (11,30,0)) ]),
        ("kl. hálfátta", [ Tok(TOK.TIME, "kl. hálfátta", (7,30,0)) ]),
        ("klukkan þrjú", [ Tok(TOK.TIME, "klukkan þrjú", (3,00,0)) ]),
        ("17/6", [ Tok(TOK.DATEREL, "17/6", (0, 6, 17)) ]),
        ("3. maí", [ Tok(TOK.DATEREL, "3. maí", (0, 5, 3)) ]),
        ("nóvember 1918", [ Tok(TOK.DATEREL, "nóvember 1918", (1918, 11, 0)) ]),
        ("sautjánda júní", [ Tok(TOK.DATEREL, "sautjánda júní", (0, 6, 17)) ]),
        ("sautjánda júní 1811", [ Tok(TOK.DATEABS, "sautjánda júní 1811", (1811, 6, 17)) ]),
        ("Sautjánda júní árið 1811", [ Tok(TOK.DATEABS, "Sautjánda júní árið 1811", (1811, 6, 17)) ]),
        ("Fimmtánda mars árið 44 f.Kr.",
            [
                Tok(TOK.DATEABS, "Fimmtánda mars árið 44 f.Kr", (-44, 3, 15)),
                Tok(TOK.PUNCTUATION, ".", None)
            ]
        ),
        ("17/6/2013", [ Tok(TOK.DATEABS, "17/6/2013", (2013, 6, 17)) ]),
        ("2013", [ Tok(TOK.YEAR, "2013", 2013) ]),
        ("874 e.Kr.", [ Tok(TOK.YEAR, "874 e.Kr", 874), Tok(TOK.PUNCTUATION, ".", None) ]),
        ("2013 f.Kr.", [ Tok(TOK.YEAR, "2013 f.Kr", -2013), Tok(TOK.PUNCTUATION, ".", None) ]),
        ("árið 2013", [ Tok(TOK.YEAR, "árið 2013", 2013) ]),
        ("árinu 874", [ Tok(TOK.YEAR, "árinu 874", 874) ]),
        ("ársins 2013", [ Tok(TOK.YEAR, "ársins 2013", 2013) ]),
        ("ársins 320 f.Kr.", [ Tok(TOK.YEAR, "ársins 320 f.Kr", -320), Tok(TOK.PUNCTUATION, ".", None) ]),
        ("213", [ Tok(TOK.NUMBER, "213", (213, None, None)) ]),
        ("2.013", [ Tok(TOK.NUMBER, "2.013", (2013, None, None)) ]),
        ("2,013", [ Tok(TOK.NUMBER, "2,013", (2.013, None, None)) ]),
        ("2.013,45", [ Tok(TOK.NUMBER, "2.013,45", (2013.45, None, None)) ]),
        ("2,013.45", [ Tok(TOK.NUMBER, "2.013,45", (2013.45, None, None)) ]),
        ("1/2", [ Tok(TOK.NUMBER, "1/2", (0.5, None, None)) ]),
        ("1/4", [ Tok(TOK.NUMBER, "1/4", (0.25, None, None)) ]),
        ("1sti", [ Tok(TOK.WORD, "fyrsti", None) ]),
        ("4ðu", [ Tok(TOK.WORD, "fjórðu", None) ]),
        ("2svar", [ Tok(TOK.WORD, "tvisvar", None) ]),
        ("þjóðhátíð", TOK.WORD),
        ("Þjóðhátíð", TOK.WORD),
        ("marg-ítrekað", TOK.WORD),
        ("750 þús.kr.",
            [
                Tok(TOK.NUMBER, "750", (750, None, None)),
                Tok(TOK.WORD, "þús.kr", [ ('þúsundir króna', 0, 'kvk', 'skst', 'þús.kr.', '-') ]),
                Tok(TOK.PUNCTUATION, ".", None)
            ]
        ),
        ("m.kr.",
            [
                Tok(TOK.WORD, "m.kr", [ ('milljónir króna', 0, 'kvk', 'skst', 'm.kr.', '-') ]),
                Tok(TOK.PUNCTUATION, ".", None)
            ]
        ),
        ("ma.kr.",
            [
                Tok(TOK.WORD, "ma.kr", [ ('milljarðar króna', 0, 'kk', 'skst', 'ma.kr.', '-') ]),
                Tok(TOK.PUNCTUATION, ".", None)
            ]
        ),
        ("30,7 mö.kr.",
            [
                Tok(TOK.NUMBER, "30,7", (30.7, None, None)),
                Tok(TOK.WORD, "mö.kr", [ ('milljörðum króna', 0, 'kk', 'skst', 'mö.kr.', '-') ]),
                Tok(TOK.PUNCTUATION, ".", None)
            ]
        ),
        ("t.d.", TOK.WORD, [ ('til dæmis', 0, 'ao', 'frasi', 't.d.', '-') ]),
        ("hr.", TOK.WORD, [ ('herra', 0, 'kk', 'skst', 'hr.', '-') ]),
        ("Hr.", TOK.WORD, [ ('herra', 0, 'kk', 'skst', 'hr.', '-') ]),
        ("o.s.frv.",
            [
                Tok(TOK.WORD, "o.s.frv", [ ('og svo framvegis', 0, 'ao', 'frasi', 'o.s.frv.', '-') ]),
                Tok(TOK.PUNCTUATION, ".", None)
            ]
        ),
        ("BSRB", TOK.WORD),
        ("stjórnskipunar- og eftirlitsnefnd", TOK.WORD),
        ("123-4444", TOK.TELNO),
        ("1234444", [ Tok(TOK.TELNO, "123-4444", None) ]),
        ("12,3%", TOK.PERCENT),
        ("12,3 %", [ Tok(TOK.PERCENT, "12,3%", (12.3, None, None)) ]),
        ("http://www.greynir.is", TOK.URL),
        ("https://www.greynir.is", TOK.URL),
        ("www.greynir.is", TOK.URL),
        ("19/3/1977 14:56:10",
            [ Tok(TOK.TIMESTAMP, "19/3/1977 14:56:10", (1977,3,19,14,56,10)) ]
        ),
        ("19/3/1977 kl. 14:56:10",
            [ Tok(TOK.TIMESTAMP, "19/3/1977 kl. 14:56:10", (1977,3,19,14,56,10)) ]
        ),
        ("$472,64", TOK.AMOUNT),
        ("€472,64", TOK.AMOUNT),
        ("$1.472,64", TOK.AMOUNT),
        ("€3.472,64", TOK.AMOUNT),
        ("$1,472.64", [ Tok(TOK.AMOUNT, "$1.472,64", (1472.64, "USD", None, None)) ]),
        ("€3,472.64", [ Tok(TOK.AMOUNT, "€3.472,64", (3472.64, "EUR", None, None)) ]),
        ("fake@news.is", TOK.EMAIL),
        ("100 mm", [ Tok(TOK.MEASUREMENT, "100 mm", ("m", 0.1)) ]),
        ("30,7°C", [ Tok(TOK.MEASUREMENT, "30,7 °C", ("K", 273.15 + 30.7)) ]),
        ("6.500 kg", [ Tok(TOK.MEASUREMENT, "6.500 kg", ("g", 6.5e6)) ]),
        ("220V", [ Tok(TOK.MEASUREMENT, "220 V", ("V", 220)) ]),
        ("690 MW", [ Tok(TOK.MEASUREMENT, "690 MW", ("W", 690e6)) ]),
    ]

    for test_case in TEST_CASES:
        if len(test_case) == 3:
            txt, kind, val = test_case
            c = [ Tok(kind, txt, val) ]
        elif isinstance(test_case[1], list):
            txt = test_case[0]
            c = test_case[1]
        else:
            txt, kind = test_case
            c = [ Tok(kind, txt, None) ]
        l = list(t.tokenize(txt))
        assert len(l) == len(c) + 2, repr(l)
        assert l[0].kind == TOK.S_BEGIN, repr(l[0])
        assert l[-1].kind == TOK.S_END, repr(l[-1])
        for tok, check in zip(l[1:-1], c):
            assert tok.kind == check.kind, tok.txt + ": " + repr(TOK.descr[tok.kind]) + " " + repr(TOK.descr[check.kind])
            assert tok.txt == check.txt, tok.txt + ": " + check.txt
            if check.val is not None:
                assert tok.val == check.val, repr(tok.val) + ": " + repr(check.val)


def test_sentences():

    KIND = {
        "B" : TOK.S_BEGIN,
        "E" : TOK.S_END,
        "W" : TOK.WORD,
        "P" : TOK.PUNCTUATION,
        "T" : TOK.TIME,
        "DR" : TOK.DATEREL,
        "DA" : TOK.DATEABS,
        "Y" : TOK.YEAR,
        "N" : TOK.NUMBER,
        "TEL" : TOK.TELNO,
        "PC" : TOK.PERCENT,
        "U" : TOK.URL,
        "O" : TOK.ORDINAL,
        "TS" : TOK.TIMESTAMP,
        "C" : TOK.CURRENCY,
        "A" : TOK.AMOUNT,
        "M" : TOK.EMAIL,
        "ME" : TOK.MEASUREMENT,
        "X" : TOK.UNKNOWN
    }

    def test_sentence(text, expected):

        exp = expected.split()
        s = t.tokenize(text)

        for token, e in zip(s, exp):
            assert e in KIND
            ekind = KIND[e]
            assert token.kind == ekind

    test_sentence(
        "  Málinu var vísað til stjórnskipunar- og eftirlitsnefndar "
        "skv. 3. gr. XVII. kafla laga nr. 10/2007 þann 3. janúar 2010.",
        "B W      W   W     W   W "
        "W    O  W   O     W     W    W   N P Y   W    DA            P E")

    test_sentence(
        "  Góðan daginn! Ég á 10.000 kr. í vasanum, €100 og $40.Gengi USD er 103,45. "
        "Í dag er 10. júlí. Klukkan er 15:40 núna.Ég fer kl. 13 niður á Hlemm o.s.frv. ",
        "B W     W     P E B W W N   W   W W      P A    W  A  P E B W W   W  N     P E "
        "B W W W  DR      P E B W   W  T     W   P E B W W T     W     W W     W      P E")

    test_sentence(
        "Málið um BSRB gekk marg-ítrekað til stjórnskipunar- og eftirlitsnefndar í 10. sinn "
        "skv. XVII. kafla þann 24. september 2015. Ál-verið notar 60 MWst á ári.",
        "B W   W  W    W    W            W   W                                   W O   W "
        "W    O     W     W    DA                P E B W P W W    N  W    W W  P E")

    test_sentence(
        "Ég er t.d. með tölvupóstfangið fake@news.com, vefföngin "
        "http://greynir.is og www.greynir.is, og síma 6638999. Hann gaf mér 1000 kr. Ég keypti mér 1/2 kaffi.",
        "B W W W    W   W               M            P W "
        "U                 W  U             P W  W    TEL    P E B W W  W   N    W P E B W W   W   N   W    P E")

    test_sentence(
        "Hann starfaði við stofnunina árin 1944-50.",
        "B W  W        W   W          W    Y   P N P E")

    test_sentence(
        "Landnám er talið hafa hafist um árið 874 e.Kr. en óvissa er nokkur.",
        "B W     W  W     W    W      W  Y              W  W      W  W     P E")

    test_sentence(
        "Hitinn í \"pottinum\" var orðinn 30,7 °C þegar 2.000 l voru komnir í hann.",
        "B W    W P W        P W   W      ME      W     ME      W    W      W W   P E")

    test_sentence(
        "Skrifað var undir friðarsamninga í nóvember 1918. Júlíus Sesar var myrtur "
        "þann fimmtánda mars árið 44 f.Kr. og þótti harmdauði.",
        "B W     W   W     W              W DR           P E B W  W     W   W "
        "W    DA                           W  W     W        P E")

    test_sentence(
        "1.030 hPa lægð gengur yfir landið árið 2019 e.Kr. Jógúrtin inniheldur 80 kcal.",
        "B ME      W    W      W    W      Y             P E B W    W          ME     P E")


def test_correction():
    SENT = [
        (
            """Hann sagði: "Þú ert fífl"! Ég mótmælti því.""",
            """Hann sagði: „Þú ert fífl“! Ég mótmælti því."""
        ),
        (
            """Hann sagði: Þú ert "fífl"! Ég mótmælti því.""",
            """Hann sagði: Þú ert „fífl“! Ég mótmælti því."""
        ),
        (
            """Hann sagði: Þú ert «fífl»! Ég mótmælti því.""",
            """Hann sagði: Þú ert „fífl“! Ég mótmælti því."""
        ),
        (
            """Hann sagði: ´Þú ert fífl´! Farðu í 3ja sinn.""",
            """Hann sagði: ‚Þú ert fífl‘! Farðu í þriðja sinn."""
        ),
        (
            """Hann sagði: Þú ert ´fífl´! Hringdu í 7771234.""",
            """Hann sagði: Þú ert ‚fífl‘! Hringdu í 777-1234."""
        ),
        (
            """Hann sagði: Þú ert (´fífl´)! Ég mótmælti því.""",
            """Hann sagði: Þú ert (´fífl‘)! Ég mótmælti því.""" # !!!
        ),
        (
            """Hann "gaf" mér 10,780.65 dollara.""",
            """Hann „gaf“ mér 10.780,65 dollara."""
        ),
    ]
    for sent, correct in SENT:
        s = t.tokenize(sent)
        txt = t.correct_spaces(" ".join(token.txt for token in s if token.txt))
        # print(txt)
        assert txt == correct


def test_correct_spaces():
    s = t.correct_spaces("Frétt \n  dagsins:Jón\t ,Friðgeir og Páll ! 100,8  /  2  =   50.4")
    assert s == 'Frétt dagsins: Jón, Friðgeir og Páll! 100,8/2 = 50.4'
    s = t.correct_spaces("Hitinn    var\n-7,4 \t gráður en   álverðið var  \n $10,348.55.")
    assert s == 'Hitinn var -7,4 gráður en álverðið var $10,348.55.'
    s = t.correct_spaces("\n Breytingin var   +4,10 þingmenn \t  en dollarinn er nú á €1,3455  .")
    assert s == 'Breytingin var +4,10 þingmenn en dollarinn er nú á €1,3455.'
    s = t.correct_spaces("Jón- sem var formaður — mótmælti málinu.")
    assert s == 'Jón-sem var formaður—mótmælti málinu.'


if __name__ == "__main__":

    test_single_tokens()
    test_sentences()
    test_correct_spaces()
    test_correction()

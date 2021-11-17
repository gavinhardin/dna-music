"""Parses through DNA genetic code, reads each nucleotide, and interprets nucleotide triplets
(codons) as amino acids. Using the detected nucleotides and acids, maps to music using MIDI
signals.

There are four DNA nucleotides (T, C, A, G), and each is assigned a unique MIDI note mapping.
Each nucleotide note is then sent to port 1 to be played.

Amino acids are made of triplets of nucleotides. There are 20 amino acids, and each falls
into one of 4 categories based on its biochemical properties: non-polar, polar, basic, or
acidic. Based on the category, one of ports 2-5 is chosen, and each amino acid in that
category is assigned a unique note to be played.

Each of ports 2-5 has a different waveshape, frequency, and ADSR combination."""
import mido
import time
from multiprocessing import Pool


class DNAMusic:
    nucleotides = {"T": 70, "C": 65, "A": 55, "G": 43}

    codons = {"TTT": "Phe", "TTC": "Phe", "TTA": "Leu", "TTG": "Leu", "CTT": "Leu", "CTC": "Leu",
              "CTA": "Leu", "CTG": "Leu", "ATT": "Ile", "ATC": "Ile", "ATA": "Ile", "ATG": "Met",
              "GTT": "Val", "GTC": "Val", "GTA": "Val", "GTG": "Val", "TCT": "Ser", "TCC": "Ser",
              "TCA": "Ser", "TCG": "Ser", "CCT": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
              "ACT": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr", "GCT": "Ala", "GCC": "Ala",
              "GCA": "Ala", "GCG": "Ala", "TAT": "Tyr", "TAC": "Tyr", "TAA": None, "TAG": None,
              "CAT": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln", "AAT": "Asn", "AAC": "Asn",
              "AAA": "Lys", "AAG": "Lys", "GAT": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
              "TGT": "Cys", "TGC": "Cys", "TGA": None, "TGG": "Trp", "CGT": "Arg", "CGC": "Arg",
              "CGA": "Arg", "CGG": "Arg", "AGT": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
              "GGT": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly"}

    acids = {"Phe": 45, "Leu": 38, "Ile": 55, "Met": 50, "Val": 59, "Ser": 71, "Pro": 42,
             "Thr": 74, "Ala": 48, "Tyr": 68, "His": 34, "Gln": 65, "Asn": 78, "Lys": 30,
             "Asp": 90, "Glu": 88, "Cys": 77, "Trp": 52, "Arg": 28, "Gly": 42}

    classes = {"Non-Polar": {"Phe", "Leu", "Ile", "Met", "Val", "Pro", "Ala", "Trp", "Gly"},
               "Polar": {"Ser", "Thr", "Tyr", "Gln", "Asn", "Cys"},
               "Basic": {"His", "Lys", "Arg"},
               "Acidic": {"Asp", "Glu"}}

    def __init__(self):
        self.ports = [mido.open_output('IAC Driver Bus 1'),
                      mido.open_output('IAC Driver IAC Bus 2'),
                      mido.open_output('IAC Driver IAC Bus 3'),
                      mido.open_output('IAC Driver IAC Bus 4'),
                      mido.open_output('IAC Driver IAC Bus 5')]

    # def map_string(self, args):
    #     port_num, string, mapping = args
    #     for char in string:
    #         if char == " ":
    #             time.sleep(.8)
    #         else:
    #             self.play_note(mapping[char], port_num)

    def play_note(self, note, port_num):
        msg = mido.Message('note_on', note=note)
        off_msg = mido.Message('note_off', note=note)

        self.ports[port_num].send(msg)
        time.sleep(.3)
        self.ports[port_num].send(off_msg)

    def play_code(self, code):
        # self.map_string((0, code, mapping))
        for index, char in enumerate(code, start=1):
            # Map nucleotide to note
            if char == " ":
                time.sleep(.8)
            else:
                self.play_note(self.nucleotides[char], 0)

            # Check if time to map a codon
            if index % 3 == 0 and index - 3 >= 0 and " " not in code[index - 3:index - 1]:
                # Assemble the nucleotide triplet
                triplet = code[index - 3] + code[index - 2] + code[index - 1]
                amino_acid = self.codons[triplet]
                port_num = None
                if amino_acid in self.classes["Non-Polar"]:
                    port_num = 1
                elif amino_acid in self.classes["Polar"]:
                    # Ports 2 and 3 combined due to technical limitations in VCV Rack
                    port_num = 1
                elif amino_acid in self.classes["Basic"]:
                    port_num = 3
                elif amino_acid in self.classes["Acidic"]:
                    port_num = 4

                # Map acid to note
                self.play_note(self.acids[amino_acid], port_num)

    def finish(self):
        for port in self.ports:
            port.reset()
            port.panic()
            port.close()


if __name__ == "__main__":
    example_code = "GATCCTCCAT ATACAACGGT"

    music = DNAMusic()
    music.play_code(example_code)
    music.finish()

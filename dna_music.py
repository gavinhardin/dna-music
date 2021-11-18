"""Parses through DNA genetic code, reads each nucleotide, and interprets nucleotide triplets
(codons) as amino acids. Using the detected nucleotides and acids, maps to music using MIDI
signals.

There are four DNA nucleotides (G, C, A, T), and each is assigned a unique MIDI note mapping.
Each nucleotide note is then sent to port 1 to be played.

Amino acids are made of triplets of nucleotides. There are 20 amino acids, and each falls
into one of 4 categories based on its biochemical properties: non-polar, polar, basic, or
acidic. Each category corresponds to a different MIDI port, and each amino acid in that
category is assigned a unique MIDI note to be played."""
import mido
import time


class DNAMusic:
    # Nucleotides and their MIDI mappings
    nucleotides = {"T": 70, "C": 65, "A": 55, "G": 43}
    # Codons and the amino acids they map to
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
    # Amino acids and their MIDI note mappings
    acids = {"Phe": 45, "Leu": 42, "Ile": 55, "Met": 50, "Val": 59, "Ser": 71, "Pro": 47,
             "Thr": 74, "Ala": 48, "Tyr": 68, "His": 40, "Gln": 65, "Asn": 78, "Lys": 45,
             "Asp": 90, "Glu": 88, "Cys": 77, "Trp": 52, "Arg": 37, "Gly": 42}
    # Biochemical classes and the amino acids contained in each
    classes = {"Non-Polar": {"Phe", "Leu", "Ile", "Met", "Val", "Pro", "Ala", "Trp", "Gly"},
               "Polar": {"Ser", "Thr", "Tyr", "Gln", "Asn", "Cys"},
               "Basic": {"His", "Lys", "Arg"},
               "Acidic": {"Asp", "Glu"}}

    def __init__(self):
        """Open ports used to send MIDI signals."""
        self.ports = [mido.open_output('IAC Driver Bus 1'),
                      mido.open_output('IAC Driver IAC Bus 2'),
                      mido.open_output('IAC Driver IAC Bus 3'),
                      mido.open_output('IAC Driver IAC Bus 4'),
                      mido.open_output('IAC Driver IAC Bus 5')]

    def play_note(self, note, port_num):
        """Play a single MIDI note, given the note to play and port to send it to."""
        msg = mido.Message('note_on', note=note)
        off_msg = mido.Message('note_off', note=note)

        self.ports[port_num].send(msg)
        time.sleep(.2)
        self.ports[port_num].send(off_msg)

    def play_code(self, code):
        """Play a given DNA code by mapping its nucleotides and codons."""
        code = code.upper()
        for index, char in enumerate(code, start=1):
            # Map nucleotide to note
            if char == " ":
                time.sleep(.6)
            else:
                self.play_note(self.nucleotides[char], 0)

            # Check if time to map a codon
            if index % 3 == 0 and index - 3 >= 0 and " " not in code[index - 3:index]:
                # Assemble the nucleotide triplet
                triplet = code[index - 3] + code[index - 2] + code[index - 1]
                amino_acid = self.codons[triplet]
                port_num = None
                bio_class = None
                if amino_acid in self.classes["Non-Polar"]:
                    bio_class = "Non-Polar"
                    port_num = 1
                elif amino_acid in self.classes["Polar"]:
                    bio_class = "Polar"
                    # Non-polar and polar ports combined due to technical limitations in VCV Rack
                    port_num = 1
                elif amino_acid in self.classes["Basic"]:
                    bio_class = "Basic"
                    port_num = 3
                elif amino_acid in self.classes["Acidic"]:
                    bio_class = "Acidic"
                    port_num = 4

                # Map acid to note
                if port_num:
                    print(f"{triplet} --> {amino_acid} ({bio_class})")
                    self.play_note(self.acids[amino_acid], port_num)

    def finish(self):
        for port in self.ports:
            port.reset()
            port.close()


if __name__ == "__main__":
    # End code of the honduran white bat's cytochrome b gene
    # https://www.ncbi.nlm.nih.gov/gene/39721076
    honduran_white_bat_cytb = "tctgaggagg cttctctgta gacaaagcaa ctctcactcg attttttgct tttcacttcc tattcccctt " \
                         "cattgtaaca gctcttgtaa tagtacatct actatttcta catgaaacag gatctaacaa cccaactgga " \
                         "atcccatcag acccagacat aattccattc cacccatatt acacaatcaa agatatttta ggatttataa " \
                         "ttatactaac agccctatca acactagtcc tattttcacc agaccttcta ggagacccag acaactatat " \
                         "tccagccaac cccctcagta cccctcccca tattaaaccc gaatgatatt tcctttttgc ctacgcaatc " \
                         "ctacgttcca tcccaaataa attgggagga gtactggcct taattatatc tatcttaatc ctagctattg " \
                         "tcccaatcat tcatatatcc aaacaacgaa gcataatatt tcgacccatc agccaatgcc tgttctgact " \
                         "tctagtagca gttctactca cattaacatg gatcggagga caaccagtcg aacaccctta cattattatc " \
                         "ggtcaaatag catccatcct atatttccta attattctaa tcctaatacc aattactagt ttaatagaaa " \
                         "actaccttct aaaatgaaga"
    music = DNAMusic()
    music.play_code(honduran_white_bat_cytb)
    music.finish()

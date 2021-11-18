# dna-music
A project for ARS 306 'Music Composition with Computers'. Maps a given DNA sequence to MIDI notes to create music.

I used this program to create a piece of computer music for ARS 306 at NCSU, of which the final mix is also included in the repository. Find the original program notes and bio that accompanied the piece below.

**Program Notes**  
I was inspired to create this piece after listening to Laurie Spiegel’s *A Strand of Life*, in which she mapped a potato tuber viroid’s genetic code into music. Wanting to expand on this idea, I created a Python program that takes in a DNA nucleotide sequence and maps it into music through creating and sending MIDI notes to a series of pre-configured ports (connected to VCV Rack). Each nucleotide is mapped to a MIDI note, and each codon is matched to the amino acid it corresponds to, which is then mapped to a MIDI note. The nucleotide notes are sent to port 1, and amino acid notes to one of 3 ports depending on the acid’s biochemical properties: ports 1 and 2 are set to produce sine waves; 3 produces saw waves; and 4 produces triangle waves.
The DNA code I used for the piece comes from a gene of the Honduran white bat. To accompany the musical DNA mapping, I created a soundscape using bat audio samples. The main sample is a Hoary bat echo call, which I’ve stretched by a factor of 10 using Audacity’s Paulstretch and applied heavy reverb to. The closing sample is a field recording of vocalizations from 18 bats.

**Biography**  
Gavin Hardin is a computer science undergraduate at NCSU. His academic interests focus on Python and Java programming, with a strong interest in machine learning and AI. Outside of academics, he enjoys viewing and learning about art, but has little to speak of in terms of creating any. This is his first musical composition.

Relevant to the piece is Gavin’s admiration and support of the work of Bat Conservation International, along with other bat advocacy groups. DNA Music may then be seen as a way of contributing to the framing of these creatures as beautiful, complex, and worthy of contemplation.

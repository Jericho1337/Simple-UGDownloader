import re as regex

#CLASS THAT GIVEN A TEXT WITH CHORD, TRANSPOSES CHORDS

class ChordTransposer:
    
    CHORD_REGEX="([CDEFGAB](#|##|b|bb)?)(?![cefghilnopqrtuvxyz|.])"
    CHORD_LIST_SHARP=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    CHORD_LIST=["C", "C#","Db", "D", "D#","Eb", "E", "F", "F#","Gb", "G", "G#","Ab", "A", "A#","Bb", "B"]
    CHORD_APPARENT_INDEX = [0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11]
    
    def chord_transposer(chord, offset):
        
        chord_index = ChordTransposer.CHORD_APPARENT_INDEX[ChordTransposer.CHORD_LIST.index(chord)] #USING APPARENT INDEX TO TRANSLATE b and # ONLY IN SHARP MONOTONIC SCALE
        if offset >= 0: # USE MODULUS TO CIRCULAR CHORD TRANSPOSITION
            transposing_index = (chord_index+offset)%12
        else: # NEGATIVE TRANSPOSITION MUST BE CONVERTED TO POSITIVE
            if chord_index+offset >= 0:
                transposing_index = chord_index+offset
            elif abs(offset)%12 == 0:
                transposing_index = chord_index
            else:
                transposing_index = 12 - chord_index - abs(offset)%12
        return ChordTransposer.CHORD_LIST_SHARP[transposing_index]

    def transpose(text_with_chords, offset):
        transposed_text_with_chords = ""
        for line in text_with_chords.split("\n"):
            line = line + "\n"
            
            matches = regex.finditer(ChordTransposer.CHORD_REGEX, line) #FIND ALL MATCHES
            if matches != []:
                chord_line = list(line) #USING A LIST INSTEAD OF A STRING BECAUSE STRINGS ARE IMMUTABLE IN PYTHON
                shift_counter = 0 #SHIFT COUNTER IS USED TO KEEP REFERENCES OF MATCHES, MATCHES DON'T CHANGE WITH INSERT AND POPS SO THEY MUST BE UPDATED MANUALLY WITH A COUNTER
                for match in matches:
                    transposed_chord = ChordTransposer.chord_transposer(match.string[match.start():match.end()], offset)

                    #MODIFY STRING
                    if len(transposed_chord) == 2 and len(line[match.start():match.end()]) == 2:
                        # EACH HAVE 2 CHARACTHER CHORD
                        chord_line[match.start()+shift_counter] = transposed_chord[0]
                        chord_line[match.start()+1+shift_counter] = transposed_chord[1]

                    elif len(transposed_chord) == 1 and len(line[match.start():match.end()]) == 1:
                        #EACH HAVE 1 CHARACTER CHORD
                        chord_line[match.start()+shift_counter] = transposed_chord

                    elif len(transposed_chord) == 2:
                        #TRANSPOSED CHORD IS BIGGER -> NEED TO SHIFT SECOND WITH INSERT
                        chord_line[match.start()+shift_counter] = transposed_chord[0]
                        chord_line.insert(match.start()+1+shift_counter, transposed_chord[1])
                        shift_counter += 1
                    else:
                        #ORIGINAL CHORD IS BIGGER -> NEED TO REMOVE SECOND CHARACTER AND SHIFT LEFT 
                        chord_line[match.start()+shift_counter] = transposed_chord
                        chord_line.pop(match.start()+1+shift_counter)
                        shift_counter -= 1

                transposed_text_with_chords = transposed_text_with_chords + "".join(chord_line) #join TRANSFORMS LIST INTO STRING
            else:
                transposed_text_with_chords = transposed_text_with_chords + line
        
        return transposed_text_with_chords
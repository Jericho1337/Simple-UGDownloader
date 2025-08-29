import re as regex

#CLASS THAT TRANSPOSES CHORDS IN DIFFERENT MODES

class ChordTransposer:
    
    #TO EXTRACT FUNDAMENTAL CHORD FROM COMPLETE CHORD
    START_CHORD_REGEX= "([CDEFGAB](#|##|b|bb)?)(?![cefghilnopqrtuvxyz|.])"
    START_CHORD_AFTER_SLASH = "(?<=\/)([CDEFGAB](#|##|b|bb)?)(?![cefghilnopqrtuvxyz|.])"
    
    #FOR TRANSPOSING
    CHORD_LIST_SHARP=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    CHORD_LIST=["C", "C#","Db", "D", "D#","Eb", "E", "F", "F#","Gb", "G", "G#","Ab", "A", "A#","Bb", "B"]
    CHORD_APPARENT_INDEX = [0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11]

    #FOR TRUEMODE PARSING
    UNCLEAN_TRUEMODE_CHORD_REGEX = "(\\\CHORD\[)(.*?)(\])" #\CHORD[] GARBAGE PRESENT IN THIS REGEX, IT IS STRUCTURED In 3 GROUPS -> USE 2nd GROUP TO TAKE THE CHORD ONLY

    def chord_transposer(chord, offset):
        
        #COMPLEX CHORD LIKE "C/G"
        if "/" in chord:
            #TRANSPOSE FIRST CHORD BEFORE /
            first_isolated_chord = regex.search(ChordTransposer.START_CHORD_REGEX, chord).group(0)
            first_chord_index = ChordTransposer.CHORD_APPARENT_INDEX[ChordTransposer.CHORD_LIST.index(first_isolated_chord)] #USING APPARENT INDEX TO TRANSLATE b and # ONLY IN SHARP MONOTONIC SCALE
            if offset >= 0: # USE MODULUS TO CIRCULAR CHORD TRANSPOSITION
                first_transposing_index = (first_chord_index+offset)%12
            else: # NEGATIVE TRANSPOSITION MUST BE CONVERTED TO POSITIVE
                if first_chord_index+offset >= 0:
                    first_transposing_index = first_chord_index+offset
                elif abs(offset)%12 == 0:
                    first_transposing_index = first_chord_index
                else:
                    first_transposing_index = 12 - first_chord_index - abs(offset)%12
            
            #TRANSPOSE SECOND CHORD AFTER /
            second_isolated_chord = regex.search(ChordTransposer.START_CHORD_AFTER_SLASH, chord).group(0)
            second_chord_index = ChordTransposer.CHORD_APPARENT_INDEX[ChordTransposer.CHORD_LIST.index(second_isolated_chord)] #USING APPARENT INDEX TO TRANSLATE b and # ONLY IN SHARP MONOTONIC SCALE
            if offset >= 0: # USE MODULUS TO CIRCULAR CHORD TRANSPOSITION
                second_transposing_index = (second_chord_index+offset)%12
            else: # NEGATIVE TRANSPOSITION MUST BE CONVERTED TO POSITIVE
                if second_chord_index+offset >= 0:
                    second_transposing_index = second_chord_index+offset
                elif abs(offset)%12 == 0:
                    second_transposing_index = second_chord_index
                else:
                    second_transposing_index = 12 - second_chord_index - abs(offset)%12
    
            chord = regex.sub(ChordTransposer.START_CHORD_REGEX, ChordTransposer.CHORD_LIST_SHARP[first_transposing_index], chord)
            chord = regex.sub(ChordTransposer.START_CHORD_AFTER_SLASH, ChordTransposer.CHORD_LIST_SHARP[second_transposing_index], chord)
            return chord
            
        else:
            #SIMPLE FUNDAMENTAL CHORD
            isolated_chord = regex.search(ChordTransposer.START_CHORD_REGEX, chord).group(0)
            chord_index = ChordTransposer.CHORD_APPARENT_INDEX[ChordTransposer.CHORD_LIST.index(isolated_chord)] #USING APPARENT INDEX TO TRANSLATE b and # ONLY IN SHARP MONOTONIC SCALE
            if offset >= 0: # USE MODULUS TO CIRCULAR CHORD TRANSPOSITION
                transposing_index = (chord_index+offset)%12
            else: # NEGATIVE TRANSPOSITION MUST BE CONVERTED TO POSITIVE
                if chord_index+offset >= 0:
                    transposing_index = chord_index+offset
                elif abs(offset)%12 == 0:
                    transposing_index = chord_index
                else:
                    transposing_index = 12 - chord_index - abs(offset)%12
            chord = regex.sub(ChordTransposer.START_CHORD_REGEX, ChordTransposer.CHORD_LIST_SHARP[transposing_index], chord)
            return chord

    def transpose(text_with_chords, offset):
        transposed_text_with_chords = ""
        for line in text_with_chords.split("\n"):
            line = line + "\n"
            
            matches = regex.finditer(ChordTransposer.START_CHORD_REGEX, line) #FIND ALL MATCHES
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

    #HELPER FUNCTION TO REPLACE CHORD IN TRUE TRANSPOSE
    def replace_chord(match,offset):
        chord = match.group(2)
        return "\\\CHORD["+ChordTransposer.chord_transposer(chord,offset)+"]"
    
    def true_transpose(true_text_with_chords, offset):
        transposed_true_text_with_chords = ""

        for line in true_text_with_chords.split("\n"):
            line = line + "\n"

            #CHECK IF THERE IS AT LEAST 1 MATCH
            if regex.search(ChordTransposer.UNCLEAN_TRUEMODE_CHORD_REGEX, line) != None:

                matches = regex.findall(ChordTransposer.UNCLEAN_TRUEMODE_CHORD_REGEX, line)
                if len(matches) == 1:
                    match = regex.search(ChordTransposer.UNCLEAN_TRUEMODE_CHORD_REGEX, line)
                    line = regex.sub(ChordTransposer.UNCLEAN_TRUEMODE_CHORD_REGEX, ChordTransposer.replace_chord(match,offset), line)    
                else:  
                    splits = line.split(" ")
                    line = ""
                    for split in splits:
                        match = regex.search(ChordTransposer.UNCLEAN_TRUEMODE_CHORD_REGEX, split)
                        if(match != None):
                            split = regex.sub(ChordTransposer.UNCLEAN_TRUEMODE_CHORD_REGEX, ChordTransposer.replace_chord(match,offset), split)
                        if(len(split) == 0): 
                            line = line + split + " " #SPLIT REMOVES WHITESPACES SO WE ADD THEM AFTER
                        elif(split[-1] == "\n"):
                            line = line + split #WE MUSN'T ADD WHITESPACE AFTER NEWLINE
                        else:
                            line = line + split + " " #SPLIT REMOVES WHITESPACES SO WE ADD THEM AFTER
            transposed_true_text_with_chords = transposed_true_text_with_chords + line
        return transposed_true_text_with_chords
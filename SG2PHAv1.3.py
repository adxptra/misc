def readfin(fin):
    with open(fin) as f:
        lines = [line.split() for line in f]
    return lines

def writefout(lines, fout):
    with open(fout, 'w') as f:
        picks = []
        current_event = []

        for i in range(len(lines)):
            if len(lines[i]) == 0:
                # A blank line indicates the end of an event
                if current_event:
                    picks.extend(current_event)
                    picks.append(None)  # Add a separator for events
                    current_event = []
                continue

            if lines[i][4] == 'P':
                try:
                    station = lines[i][0]
                    pick_time = float(lines[i][8])
                    weight = 1.000  # Assuming a constant weight, adjust if needed
                    phase = 'P'
                    current_event.append((station, pick_time, weight, phase))

                    if i + 1 < len(lines) and lines[i + 1][4] == 'S' and lines[i + 1][0] == lines[i][0]:
                        station = lines[i + 1][0]
                        pick_time = float(lines[i + 1][8])
                        phase = 'S'
                        current_event.append((station, pick_time, weight, phase))
                except Exception as e:
                    print(f"Error processing line {lines[i]}: {e}")

        # Add the last event if it exists
        if current_event:
            picks.extend(current_event)
            picks.append(None)

        # Write picks to file
        for pick in picks:
            if pick is None:
                f.write('\n')  # Write a newline to separate events
            else:
                f.write(f'{pick[0]:<5}  {pick[1]:>8.2f}   {pick[2]:.3f}   {pick[3]}\n')

lines = readfin('YOUR_PICK.pick')
writefout(lines, 'YOUR_Output_name.pha')

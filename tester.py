#En terminal, ejecutar pip install mido python-rtmidi
import mido

# Diccionario para conversión a notación conocida
notas_latinas = ['Do', 'Do♯', 'Re', 'Re♯', 'Mi', 'Fa', 'Fa♯', 'Sol', 'Sol♯', 'La', 'La♯', 'Si']

# Conversor de nota MIDI a nota conocida
def conversion_nota(numero_midi):
    # Calcular la octava y el semitono
    semitono = numero_midi % 12
    octava = (numero_midi // 12) - 1  # MIDI 0 es en octava -1
    
    # Obtener la nota y la octava en notación latina
    nota = notas_latinas[semitono] 
    return f"{nota}{octava}"


# Función para agrupar mensajes de notas que suenan simultáneamente (acordes)
def detect_chords(track):
    chords = []
    active_notes = []
    current_time = 0  # Tiempo absoluto en ticks

    for msg in track:
        current_time += msg.time  # Sumar el tiempo desde el último mensaje
        if msg.type == 'note_on' and msg.velocity > 0:
            # Añadir la nota activa con su tiempo de inicio
            active_notes.append((msg.note, current_time))
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            # Identificar la nota que se apaga y calcular su duración
            note_off_time = current_time
            for note, start_time in active_notes:
                if note == msg.note:
                    duration = note_off_time - start_time
                    chords.append((start_time, duration, note))
                    active_notes.remove((note, start_time))
                    break
    return chords


print(mido.get_input_names())

# Reemplaza con el nombre exacto de tu dispositivo AKM320
input_port_name = 'AKM320 0'

# Abre el puerto de entrada
with mido.open_input(input_port_name) as inport: 
    print("Listening for MIDI messages...")
    for msg in inport:
        #print(msg.bytes())
        print(conversion_nota(msg.bytes()[1]))
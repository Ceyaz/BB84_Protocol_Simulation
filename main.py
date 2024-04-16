import tkinter as tk
import numpy as np

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulation du protocole BB84")
        self.geometry("1000x600")  # Ajustez la taille selon vos besoins
        self.bits_alice = [0] * 12  # 0 et 1 pour les bits
        self.bases_alice = [0] * 12  # Utilisera X et + pour les bases
        self.bases_bob = [0] * 12
        self.create_widgets()

    def create_widgets(self):
        # Cadre pour les bits d'Alice
        frame_bits = tk.Frame(self)
        frame_bits.pack(pady=10)
        tk.Label(frame_bits, text="Bits d'Alice:").grid(row=0, columnspan=12)
        # Bouton pour choisir les bits aléatoirement
        self.btn_random_bits_alice = tk.Button(frame_bits, text="Choix aléatoire", command=self.randomize_bits_alice)
        self.btn_random_bits_alice.grid(row=1, column=12)  # Positionnement du bouton

        self.bits_buttons_alice = self.create_bit_buttons(frame_bits, self.update_bit_alice, 1, ['0', '1'])

        # Cadre pour les bases d'Alice
        frame_bases = tk.Frame(self)
        frame_bases.pack(pady=10)
        tk.Label(frame_bases, text="Bases d'Alice:").grid(row=0, columnspan=12)
        # Bouton pour choisir les bases aléatoirement
        self.btn_random_bases_alice = tk.Button(frame_bases, text="Choix aléatoire", command=self.randomize_bases_alice)
        self.btn_random_bases_alice.grid(row=1, column=12)  # Positionnement du bouton
        self.bases_buttons_alice = self.create_bit_buttons(frame_bases, self.update_base_alice, 1, ['+', 'X'])

        # Boutons de contrôle
        self.frame_controls = tk.Frame(self)
        self.frame_controls.pack(pady=10)
        self.btn_send_qubits = tk.Button(self.frame_controls, text="Envoi des qubits", command=self.result_qubits)
        self.btn_send_qubits.pack(side=tk.LEFT)
        self.btn_quit = tk.Button(self.frame_controls, text="Quitter", command=self.quit)
        self.btn_quit.pack(side=tk.LEFT)

    def randomize_bits_alice(self):
        self.bits_alice = np.random.randint(2, size=12).tolist()  # Génération aléatoire des bits
        for index, bit in enumerate(self.bits_alice):
            self.bits_buttons_alice[index].config(text=str(bit))  # Mise à jour des boutons avec les bits aléatoires

    def randomize_bases_alice(self):
        self.bases_alice = np.random.randint(2, size=12).tolist()
        for index, base in enumerate(self.bases_alice):
            self.bases_buttons_alice[index].config(text='+' if base == 0 else 'X')

    def create_bit_buttons(self, parent, update_function, row_start, labels):
        buttons = []
        for i in range(12):
            btn_text = labels[0]
            btn = tk.Button(parent, text=btn_text, width=5, height=3, font=("Arial", 13),
                            command=lambda i=i: update_function(i, labels))
            btn.grid(row=row_start, column=i, sticky='nsew', padx=8, pady=10)
            buttons.append(btn)
        return buttons

    def update_bit_alice(self, index, labels):
        self.bits_alice[index] = 1 - self.bits_alice[index]
        self.bits_buttons_alice[index].config(text=labels[self.bits_alice[index]])

    def update_base_alice(self, index, labels):
        self.bases_alice[index] = 1 - self.bases_alice[index]
        self.bases_buttons_alice[index].config(text=labels[self.bases_alice[index]])

    def translate_to_quantum_states(self):
        quantum_states = []
        for bit, base in zip(self.bits_alice, self.bases_alice):
            if bit == 0 and base == 0:
                state = "|↑〉"
            elif bit == 1 and base == 0:
                state = "|→〉"
            elif bit == 0 and base == 1:
                state = "|↗〉"
            elif bit == 1 and base == 1:
                state = "|↘〉"
            quantum_states.append(state)
        return quantum_states

    def result_qubits(self):
        for btn in self.bits_buttons_alice:
            btn.config(state=tk.DISABLED)
        for btn in self.bases_buttons_alice:
            btn.config(state=tk.DISABLED)
        self.btn_random_bases_alice.config(state=tk.DISABLED)
        self.btn_random_bits_alice.config(state=tk.DISABLED)

        self.btn_send_qubits.pack_forget()
        self.btn_quit.pack_forget()

        print("Simulation lancée!")
        intro_label = tk.Label(self.frame_controls, text="États quantiques d'Alice envoyés:\n",
                               font=("TkDefaultFont", 13))
        intro_label.pack()

        # Génération et affichage des états quantiques avec une taille de police plus grande
        quantum_states_str = "   ".join(self.translate_to_quantum_states())
        states_label = tk.Label(self.frame_controls, text=quantum_states_str, font=("TkDefaultFont", 23))
        states_label.pack()

        # Cadre pour les bases de Bob
        frame_bases = tk.Frame(self)
        frame_bases.pack(pady=10)
        tk.Label(frame_bases, text="Bases de Bob:").grid(row=0, columnspan=12)
        # Bouton pour choisir les bases aléatoirement
        self.btn_random_bases_bob = tk.Button(frame_bases, text="Choix aléatoire", command=self.randomize_bases_bob)
        self.btn_random_bases_bob.grid(row=1, column=12)  # Positionnement du bouton
        self.bases_buttons_bob = self.create_bit_buttons(frame_bases, self.update_base_bob, 1, ['+', 'X'])

        # Bouton pour mesurer les qubits
        self.frame_controls = tk.Frame(self)
        self.frame_controls.pack(pady=10)
        self.btn_measure_qubits = tk.Button(self.frame_controls, text="Mesure des qubits par Bob",
                                            command=self.measure_qubits)
        self.btn_measure_qubits.pack(side=tk.LEFT)
        self.btn_quit = tk.Button(self.frame_controls, text="Quitter", command=self.quit)
        self.btn_quit.pack(side=tk.LEFT)

    def update_base_bob(self, index, labels):
        self.bases_bob[index] = 1 - self.bases_bob[index]
        self.bases_buttons_bob[index].config(text=labels[self.bases_bob[index]])

    def randomize_bases_bob(self):
        self.bases_bob = np.random.randint(2, size=12).tolist()
        for index, base in enumerate(self.bases_bob):
            self.bases_buttons_bob[index].config(text='+' if base == 0 else 'X')

    def get_base_representation_alice(self):
        # Convertit les états de base en "+" pour 0 et "X" pour 1
        return ['+' if base == 0 else 'X' for base in self.bases_alice]

    def measure_qubits(self):
        # Implémentez la logique de mesure des qubits ici
        print("Mesure des qubits lancée!")
        bases_str = self.get_base_representation_alice()
        print("Bases d'Alice:", bases_str)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

import tkinter as tk
import numpy as np

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        self.title("Simulation du protocole BB84")
        self.geometry("1000x800")  # Ajustez la taille selon vos besoins

        # Créez un Canvas et une Scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Placez le Canvas et la Scrollbar dans la fenêtre
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((50, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Cadre pour les bits d'Alice
        frame_bits = tk.Frame(self.scrollable_frame)
        frame_bits.pack(pady=10)
        tk.Label(frame_bits, text="Bits d'Alice:").grid(row=0, columnspan=13)
        
        # Bouton pour choisir les bits aléatoirement
        self.btn_random_bits_alice = tk.Button(frame_bits, text="Choix aléatoire", command=self.randomize_bits_alice)
        self.btn_random_bits_alice.grid(row=1, column=12)  # Positionnement du bouton

        self.bits_buttons_alice = self.create_bit_buttons(frame_bits, self.update_bit_alice, 1, ['0', '1'])

        # Cadre pour les bases d'Alice
        frame_bases = tk.Frame(self.scrollable_frame)
        frame_bases.pack(pady=10)
        tk.Label(frame_bases, text="Bases d'Alice:").grid(row=0, columnspan=13)
        # Bouton pour choisir les bases aléatoirement
        self.btn_random_bases_alice = tk.Button(frame_bases, text="Choix aléatoire", command=self.randomize_bases_alice)
        self.btn_random_bases_alice.grid(row=1, column=12)  # Positionnement du bouton
        self.bases_buttons_alice = self.create_bit_buttons(frame_bases, self.update_base_alice, 1, ['+', 'X'])

        # Boutons de contrôle
        self.frame_controls = tk.Frame(self.scrollable_frame)
        self.frame_controls.pack(pady=10)
        self.btn_send_qubits = tk.Button(self.frame_controls, text="Envoi des qubits", command=self.result_qubits)
        self.btn_send_qubits.pack(side=tk.LEFT)

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

        print("Simulation lancée!")
        intro_label = tk.Label(self.frame_controls, text="États quantiques d'Alice envoyés:\n",
                               font=("TkDefaultFont", 13))
        intro_label.pack()

        # Génération et affichage des états quantiques avec une taille de police plus grande
        quantum_states_str = "   ".join(self.translate_to_quantum_states())
        states_label = tk.Label(self.frame_controls, text=quantum_states_str, font=("TkDefaultFont", 23))
        states_label.pack()

        # Cadre pour les bases de Bob
        frame_bases = tk.Frame(self.scrollable_frame)
        frame_bases.pack(pady=10)
        tk.Label(frame_bases, text="Bases de Bob:").grid(row=0, columnspan=13)
        # Bouton pour choisir les bases aléatoirement
        self.btn_random_bases_bob = tk.Button(frame_bases, text="Choix aléatoire", command=self.randomize_bases_bob)
        self.btn_random_bases_bob.grid(row=1, column=12)  # Positionnement du bouton
        self.bases_buttons_bob = self.create_bit_buttons(frame_bases, self.update_base_bob, 1, ['+', 'X'])

        # Bouton pour mesurer les qubits
        self.frame_controls = tk.Frame(self.scrollable_frame)
        self.frame_controls.pack(pady=10)
        self.btn_measure_qubits = tk.Button(self.frame_controls, text="Mesure des qubits par Bob",
                                            command=self.measure_qubits_no_intercept)
        self.btn_measure_qubits.pack(side=tk.LEFT)

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
    
    def get_bits_representation_alice(self):
        # Convertit les états de base en "+" pour 0 et "X" pour 1
        return ['0' if bits == 0 else '1' for bits in self.bits_alice]

    def measure_qubits_no_intercept(self):

        for btn in self.bases_buttons_bob:
            btn.config(state=tk.DISABLED)
        self.btn_random_bases_bob.config(state=tk.DISABLED)
        
        self.btn_measure_qubits.pack_forget()

        self.bits_bob = []
        for bit_alice, base_alice, base_bob in zip(self.bits_alice, self.bases_alice, self.bases_bob):
            if base_alice == base_bob:  # Si Alice et Bob utilisent la même base
                self.bits_bob.append(bit_alice)  # Le bit de Bob sera le même que celui d'Alice
            else:  # Si les bases sont différentes
                self.bits_bob.append(np.random.randint(2))  # Bob obtient un résultat aléatoire 0 ou 1

        # Affichage des résultats
        resultat_bob_label = tk.Label(self.frame_controls, text="Bits mesurés par Bob:\n",
                               font=("TkDefaultFont", 13))
        resultat_bob_label.pack()

        results_str = "   ".join([str(bit) for bit in self.bits_bob])
        states_label = tk.Label(self.frame_controls, text=results_str, font=("TkDefaultFont", 23))
        states_label.pack()

        print("Mesure des qubits lancée!")
        print("Bases d'Alice:", ['+' if base == 0 else 'X' for base in self.bases_alice])
        print("Bits d'Alice:", ['0' if bit == 0 else '1' for bit in self.bits_alice])
        print("Bases de Bob:", ['+' if base == 0 else 'X' for base in self.bases_bob])
        print("Mesures de Bob:", self.bits_bob)

        tk.Label(self.frame_controls, height=1).pack()
        self.btn_sup_some_bits = tk.Button(self.frame_controls, text="Alice et Bob ne gardent que les bits pour lesquels ils ont choisi les mêmes bases", command=self.sup_some_bits)
        self.btn_sup_some_bits.pack(side=tk.LEFT)

    def sup_some_bits(self):
        self.btn_sup_some_bits.pack_forget()

        # Texte explicatif
        explanation_text = (
            "Alice et Bob comparent publiquement leurs bases et "
            "ne conservent que les bits pour lesquels ils ont utilisé "
            "la même base. Cela garantit que si l'information a été interceptée, "
            "l'intercepteur ne peut pas connaître la clé secrète partagée car il "
            "ne peut pas distinguer les bases utilisées pour chaque bit."
        )
        explanation_label = tk.Label(self.frame_controls, text=explanation_text, font=("TkDefaultFont", 13),
                                    justify=tk.CENTER, wraplength=500, 
                                    borderwidth=2, relief="solid", fg="black", bg="#ffdddd")
        explanation_label.pack(pady=10, fill='x', padx=10)

        affichage_bits_label = tk.Label(self.frame_controls, text="Les bits gardés sont:",
                               font=("TkDefaultFont", 13))
        affichage_bits_label.pack()

        filtered_bits_alice = []
        filtered_bits_bob = []
        for bit_alice, base_alice, bit_bob, base_bob in zip(self.bits_alice, self.bases_alice, self.bits_bob, self.bases_bob):
            if base_alice == base_bob:
                filtered_bits_alice.append(str(bit_alice))
                filtered_bits_bob.append(str(bit_bob))

        # Afficher les bits restants
        bits_alice_str = " ".join(filtered_bits_alice)
        bits_bob_str = " ".join(filtered_bits_bob)

        print("Bits d'Alice après filtrage:", bits_alice_str)
        print("Bits de Bob après filtrage:", bits_bob_str)

        # Création des labels pour l'affichage
        filtered_alice_label = tk.Label(self.frame_controls, text=f"Bits d'Alice: {bits_alice_str}", font=("TkDefaultFont", 13))
        filtered_bob_label = tk.Label(self.frame_controls, text=f"Bits de Bob: {bits_bob_str}", font=("TkDefaultFont", 13))

        filtered_alice_label.pack()
        filtered_bob_label.pack()

        tk.Label(self.frame_controls, height=1).pack()

        self.btn_conclusion_no_intercept = tk.Button(self.frame_controls, text="Conclusion de la simulation",
                                            command=self.conclusion_no_intercept)
        self.btn_conclusion_no_intercept.pack()

    def conclusion_no_intercept(self):
        self.btn_conclusion_no_intercept.pack_forget()
        explanation_text = (
            "Lorsque la communication n'a pas été interceptée, Alice et Bob ont "
            "des séquences de bits identiques pour les bases correspondantes. Pour "
            "vérifier cela sans révéler leur clé, ils peuvent comparer publiquement "
            "une statistique de leur clé, comme le nombre de bits à '1'. Si la statistique "
            "est identique, ils peuvent être confiants que la clé n'a pas été compromise. "
            "Cette technique de validation est un élément crucial de la cryptographie quantique, "
            "garantissant la sécurité de la clé partagée tant que les principes de la mécanique "
            "quantique sont respectés."
        )
        explanation_label = tk.Label(self.frame_controls, text=explanation_text, font=("TkDefaultFont", 13),
                                    justify=tk.CENTER, wraplength=500, 
                                    borderwidth=2, relief="solid", fg="black", bg="#ffdddd")
        explanation_label.pack(pady=10, fill='x', padx=10)

        tk.Label(self.frame_controls, height=1).pack()

        self.btn_reload_simulation = tk.Button(self.frame_controls, text="Recommencer une simulation",
                                            command=self.reload_simulation)
        self.btn_reload_simulation.pack()

        tk.Label(self.frame_controls, height=2).pack()

    def reload_simulation(self):
        self.destroy()
        # Crée une nouvelle instance de la fenêtre
        new_app = Application()
        new_app.mainloop()

if __name__ == "__main__":
    app = Application()
    app.mainloop()

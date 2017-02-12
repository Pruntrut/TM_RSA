from tkinter import *
import os
import tkinter.messagebox
from TM_RSAText import *
from TM_RSAPrimeGen import generateTwoLargePrimes
from TM_RSAMaths import encrypt, decrypt, generatePrivateKey, generatePublicKey
if os.name == "nt":             # Si windows (pas mac)
    from tkinter.ttk import *   # Module qui rend les boutons windows plus jolis


class RSAApp(Tk):
    def __init__(self):
        Tk.__init__(self)

        # Widgets en rapport avec les clés privées/publiques

        self.var = IntVar()  # Variable du Radiobutton

        self.key_label = Label(self, text="Public Key")
        self.key_label.grid(row=0, column=0, columnspan=3)

        self.e_label = Label(self, text="e: ")
        self.e_label.grid(row=1, column=0, sticky=E)

        self.e_entry = Entry(self)
        self.e_entry.grid(row=1, column=1, sticky=EW)

        self.n_label = Label(self, text="n: ")
        self.n_label.grid(row=2, column=0, sticky=E)

        self.n_entry = Entry(self)
        self.n_entry.grid(row=2, column=1, sticky=EW)

        self.encr_radiobtn = Radiobutton(self, text="Encrypt", variable=self.var, value=0, command=self.select)
        self.encr_radiobtn.grid(row=1, column=2)

        self.decr_radiobtn = Radiobutton(self, text="Decrypt", variable=self.var, value=1, command=self.select)
        self.decr_radiobtn.grid(row=2, column=2)

        self.keygen_btn = Button(self, text="Generate keys", command=self.generate_keys)
        self.keygen_btn.grid(row=3, column=1, columnspan=2)

        # Widgets en rapport avec le message et la réponse

        self.msg_label = Label(self, text="Message")
        self.msg_label.grid(row=5, column=0, columnspan=3)

        self.txt_label = Label(self, text="Enter text: ")
        self.txt_label.grid(row=6, column=0, sticky=E)

        self.txt_entry = Entry(self)
        self.txt_entry.grid(row=6, column=1, sticky=EW)

        self.ok_button = Button(self, text="OK", command=self.cryptbtn_press)
        self.ok_button.grid(row=6, column=2)

        self.result_label = Label(self, text="Result: ")
        self.result_label.grid(row=7, column=0, sticky=E, padx=10)

        self.result_text = Text(self, width=25, height=2, state=DISABLED)
        self.result_text.grid(row=7, column=1, columnspan=3, sticky=NW)

        self.privkey_text = Text(self, width=50, height=25, state=DISABLED)
        self.privkey_text.grid(row=8, column=1, columnspan=3, sticky=NW)
        self.privkey_text.grid_remove()  # On le rend invisible

        self.hide_privkey_btn = Button(self, text="Hide", command=self.hide_privkey)
        self.hide_privkey_btn.grid(row=9, column=2)
        self.hide_privkey_btn.grid_remove()

    # Commande à exécuter si le bouton ok est pressé
    def cryptbtn_press(self):
        try:
            raw_message = self.txt_entry.get()
            result = ""

            if self.var.get() == 0:  # Crypter
                m = messageToNumber(raw_message)  # Conversion texte en nombre
                e = int(self.e_entry.get())
                n = int(self.n_entry.get())
                key = (e, n)
                if m >= n:  # Impossible de crypter avec RSA
                    raise Exception('Binary value of message cannot be bigger than n.')
                result = encrypt(m, key)
            elif self.var.get() == 1:  # Décrypter
                c = int(raw_message)
                d = int(self.e_entry.get())
                n = int(self.n_entry.get())
                key = (d, n)
                result = numberToMessage(decrypt(c, key))

            self.result_text.config(state=NORMAL)  # Permet d'écrire dedans
            self.result_text.delete(0.0, END)  # Apparment a besoin d'un float ? Ne marche pas avec int 0
            self.result_text.insert(INSERT, str(result))
            self.result_text.config(state=DISABLED)  # On empèche d'y écrire (mode lecture seule)

        except Exception as error:  # Montre boîte de dialogue avec message et erreur de la console python
            tkinter.messagebox.showerror('Value error', 'Please enter a valid key and message \nError: %s' % str(error))

        self.n_entry.delete(0, last=len(self.n_entry.get()))
        self.e_entry.delete(0, last=len(self.e_entry.get()))
        self.txt_entry.delete(0, last=len(self.txt_entry.get()))

    # Cache les champs de clé privée
    def hide_privkey(self):
        # On supprime les clés (question de plus de sécurité)
        self.privkey_text.config(state=NORMAL)
        self.privkey_text.delete(0.0, END)
        self.privkey_text.config(state=DISABLED)

        # On cache les widgets
        self.privkey_text.grid_remove()
        self.hide_privkey_btn.grid_remove()

    # Change les label clé pub/priv et e/d selon le radiobutton sélectionne
    def select(self):
        selection = self.var.get()

        if selection == 0:
            self.key_label.config(text="Public Key")
            self.e_label.config(text="e: ")
            self.txt_label.config(text="Enter text: ")
            self.keygen_btn.config(state=NORMAL)    # On active le bouton de génération des clés
        else:
            self.key_label.config(text="Private Key")
            self.e_label.config(text="d: ")
            self.txt_label.config(text="Enter int: ")
            self.keygen_btn.config(state=DISABLED)  # On le désactive (grisé)

    # Génère des clés RSA, place la clé publique dans les champs et donne la clé privée dans un popup
    def generate_keys(self):
        p, q = generateTwoLargePrimes()

        try:
            public_key = generatePublicKey(p, q)
            private_key = generatePrivateKey(p, q, public_key[0])
        except Exception as error:  # Si pgdc(e, phi(n)) != 1 par exmpl.
            tkinter.messagebox.showerror('An error occurred', 'Please try again...\nError: %s' % str(error))
        else:  # Exécuté que s'il n'y a pas eu d'erreur
            self.encr_radiobtn.invoke()  # Sélectionne le bouton radio "encrypt" (comme si on avait cliqué dessus)

            self.e_entry.delete(0, END)
            self.e_entry.insert(INSERT, str(public_key[0]))
            self.n_entry.delete(0, END)
            self.n_entry.insert(INSERT, str(public_key[1]))

            self.privkey_text.grid()
            self.privkey_text.config(state=NORMAL)
            self.hide_privkey_btn.grid()
            self.privkey_text.delete(0.0, END)

            result = "- Private Key - \nd: %d\n\nn: %d" % private_key
            self.privkey_text.insert(INSERT, result)

        self.privkey_text.config(state=DISABLED)


# - Programme principal -

if __name__ == "__main__":
    app = RSAApp()
    app.title('RSA Encrypt/decrypt')
    app.mainloop()

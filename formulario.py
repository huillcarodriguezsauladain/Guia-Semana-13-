import math
import re
import tkinter as tk
from tkinter import messagebox, ttk


class FormularioRegistro:
    """Formulario de registro de usuario con validaciones."""

    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Usuario")
        self.root.geometry("500x600")

        self.nombre = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm_pass = tk.StringVar()
        self.edad = tk.StringVar()
        self.genero = tk.StringVar(value="")
        self.acepto = tk.BooleanVar(value=False)

        self.campos_widgets = {}
        self.crear_widgets()
        self._configurar_atajos()

    def crear_widgets(self):
        """Construye los widgets en orden lógico de tabulación."""
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Registro de Usuario",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        campos = [
            ("nombre", "Nombre completo:", self.nombre, False, 35),
            ("email", "Email:", self.email, False, 35),
            ("password", "Contraseña:", self.password, True, 35),
            ("confirm_pass", "Confirmar contraseña:", self.confirm_pass, True, 35),
            ("edad", "Edad:", self.edad, False, 12),
        ]

        for i, (clave, label, var, oculto, ancho) in enumerate(campos, start=1):
            tk.Label(frame, text=label, anchor="e").grid(
                row=i, column=0, sticky="e", pady=5, padx=(0, 10)
            )
            entry = tk.Entry(
                frame,
                textvariable=var,
                width=ancho,
                show="*" if oculto else "",
            )
            entry.grid(row=i, column=1, pady=5, sticky="w")
            self.campos_widgets[clave] = entry

        # Género (radio buttons)
        tk.Label(frame, text="Género:").grid(
            row=6, column=0, sticky="e", pady=5, padx=(0, 10)
        )
        genero_frame = tk.Frame(frame)
        genero_frame.grid(row=6, column=1, sticky="w", pady=5)
        for idx, opcion in enumerate(["Masculino", "Femenino", "Otro"]):
            rb = tk.Radiobutton(
                genero_frame,
                text=opcion,
                variable=self.genero,
                value=opcion,
            )
            rb.pack(side="left", padx=5)
            if idx == 0:
                self.campos_widgets["genero"] = rb

        # Checkbox de términos
        self.chk_acepto = tk.Checkbutton(
            frame,
            text="Acepto los términos y condiciones",
            variable=self.acepto,
        )
        self.chk_acepto.grid(row=7, column=0, columnspan=2, pady=10)
        self.campos_widgets["acepto"] = self.chk_acepto

        # Retroalimentación visual en pantalla
        self.lbl_estado = tk.Label(
            frame,
            text="",
            font=("Arial", 9),
            wraplength=420,
            justify="left",
        )
        self.lbl_estado.grid(row=8, column=0, columnspan=2, pady=5)

        # Botones
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=15)
        tk.Button(
            btn_frame,
            text="Registrar",
            command=self.validar,
            width=15,
            bg="#4CAF50",
            fg="white",
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame,
            text="Limpiar",
            command=self.limpiar,
            width=15,
        ).pack(side="left", padx=10)

        # Botón de Google debajo de los botones principales
        self.google_icon = self._crear_icono_google()
        tk.Button(
            frame,
            text="  Continuar con Google",
            image=self.google_icon,
            compound="left",
            command=self.abrir_ventana_google,
            bg="#ffffff",
            fg="#3c4043",
            activebackground="#f8f9fa",
            font=("Arial", 10, "bold"),
            relief="solid",
            bd=1,
            padx=14,
            pady=6,
            cursor="hand2",
        ).grid(row=10, column=0, columnspan=2, pady=(0, 10))

        self.campos_widgets["nombre"].focus_set()

    def _configurar_atajos(self):
        """Vincula atajos de teclado básicos (rúbrica de accesibilidad)."""
        self.root.bind("<Return>", lambda _e: self.validar())
        self.root.bind("<Escape>", lambda _e: self.limpiar())

    @classmethod
    def validar_datos(
        cls,
        nombre: str,
        email: str,
        password: str,
        confirm_pass: str,
        edad_str: str,
        genero: str,
        acepto: bool,
    ) -> list[tuple[str, str]]:
        """Valida los campos y devuelve una lista de (campo, mensaje)."""
        errores: list[tuple[str, str]] = []

        if not nombre.strip():
            errores.append(("nombre", "El nombre es obligatorio"))

        if not cls.EMAIL_REGEX.match(email.strip()):
            errores.append(("email", "Email inválido (debe contener @ y dominio)"))

        if len(password) < 8:
            errores.append(("password", "La contraseña debe tener mínimo 8 caracteres"))

        if password != confirm_pass:
            errores.append(("confirm_pass", "Las contraseñas no coinciden"))

        try:
            edad = int(edad_str)
            if edad < 15 or edad > 99:
                errores.append(("edad", "La edad debe estar entre 15 y 99"))
        except ValueError:
            errores.append(("edad", "La edad debe ser un número"))

        if not genero:
            errores.append(("genero", "Seleccione un género"))

        if not acepto:
            errores.append(("acepto", "Debe aceptar los términos"))

        return errores

    def validar(self):
        """Valida el formulario y muestra retroalimentación visual y diálogo."""
        errores = self.validar_datos(
            self.nombre.get(),
            self.email.get(),
            self.password.get(),
            self.confirm_pass.get(),
            self.edad.get(),
            self.genero.get(),
            self.acepto.get(),
        )

        if errores:
            primer_campo = errores[0][0]
            mensajes = [msg for _, msg in errores]
            self.lbl_estado.config(
                text=f"Se encontraron {len(mensajes)} error(es): {mensajes[0]}",
                fg="#C62828",
            )
            widget = self.campos_widgets.get(primer_campo)
            if widget is not None:
                widget.focus_set()
            messagebox.showerror(
                "Errores de validación",
                "\n".join(f"• {e}" for e in mensajes),
            )
        else:
            self.lbl_estado.config(
                text=f"Registro válido para {self.nombre.get().strip()}.",
                fg="#2E7D32",
            )
            messagebox.showinfo(
                "Registro exitoso",
                f"¡Bienvenido {self.nombre.get()}!\n"
                f"Email: {self.email.get()}",
            )

    def limpiar(self):
        """Resetea todos los campos y devuelve el foco al primer campo."""
        for var in (
            self.nombre,
            self.email,
            self.password,
            self.confirm_pass,
            self.edad,
            self.genero,
        ):
            var.set("")
        self.acepto.set(False)
        self.lbl_estado.config(text="")
        self.campos_widgets["nombre"].focus_set()

    def _crear_icono_google(self) -> tk.PhotoImage:
        """Genera un ícono 20x20 con la 'G' multicolor de Google."""
        size = 20
        cx = cy = (size - 1) / 2.0
        img = tk.PhotoImage(width=size, height=size)
        for y in range(size):
            for x in range(size):
                dx, dy = x - cx, y - cy
                dist = math.hypot(dx, dy)
                angulo = (math.degrees(math.atan2(-dy, dx)) + 360) % 360

                # Barra horizontal derecha de la 'G'
                en_barra = (cy - 1.6 <= y <= cy + 1.6) and (cx - 0.5 <= x <= cx + 8.5)
                # Anillo exterior con abertura a la derecha (entre 18° y 48°)
                en_anillo = (5.0 <= dist <= 8.8) and not (18 <= angulo <= 48)

                if en_barra:
                    img.put("#4285F4", (x, y))
                elif en_anillo:
                    if 48 < angulo <= 150:
                        color = "#EA4335"  # Rojo (arriba)
                    elif 150 < angulo <= 215:
                        color = "#FBBC05"  # Amarillo (izquierda)
                    elif 215 < angulo <= 315:
                        color = "#34A853"  # Verde (abajo)
                    else:
                        color = "#4285F4"  # Azul (derecha inferior)
                    img.put(color, (x, y))
        return img

    def abrir_ventana_google(self):
        """Abre una ventana emergente con la barra de carga estándar de ttk."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Google")
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()

        ancho, alto = 300, 150
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - ancho) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - alto) // 2
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        tk.Label(
            ventana,
            text="Conectando con Google...",
            font=("Arial", 11, "bold"),
        ).pack(pady=(22, 12))

        barra = ttk.Progressbar(ventana, mode="indeterminate", length=220)
        barra.pack(pady=(0, 16))
        barra.start(15)

        tk.Button(
            ventana,
            text="Cancelar",
            command=ventana.destroy,
            width=12,
        ).pack()


if __name__ == "__main__":
    app = FormularioRegistro()
    app.root.mainloop()

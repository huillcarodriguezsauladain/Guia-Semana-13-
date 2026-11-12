import tkinter as tk
from tkinter import messagebox


class Calculadora:
    """Calculadora básica con interfaz gráfica Tkinter."""

    CARACTERES_VALIDOS = set("0123456789+-*/.() ")

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora - Semana 13")
        self.ventana.geometry("300x400")
        self.ventana.resizable(False, False)

        self.expresion = tk.StringVar(value="")
        self._crear_widgets()
        self._configurar_atajos()

    def _crear_widgets(self):
        """Construye la pantalla y la cuadrícula de botones 4x4."""
        for col in range(4):
            self.ventana.columnconfigure(col, weight=1)
        for row in range(5):
            self.ventana.rowconfigure(row, weight=1)

        self.display = tk.Entry(
            self.ventana,
            textvariable=self.expresion,
            font=("Arial", 24),
            justify="right",
            bd=5,
            state="readonly",
            readonlybackground="#FFFFFF",
            fg="#111827",
        )
        self.display.grid(
            row=0, column=0, columnspan=4,
            sticky="nsew", padx=5, pady=5
        )

        botones = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("C", "0", "=", "+"),
        ]

        for i, fila in enumerate(botones):
            for j, texto in enumerate(fila):
                btn = tk.Button(
                    self.ventana,
                    text=texto,
                    font=("Arial", 18),
                    width=4,
                    height=2,
                    command=lambda t=texto: self.click(t),
                    **self._estilo_boton(texto),
                )
                btn.grid(row=i + 1, column=j, sticky="nsew", padx=2, pady=2)

    @staticmethod
    def _estilo_boton(texto: str) -> dict:
        """Retorna los colores del botón según el diseño del wireframe."""
        if texto == "=":
            return {"bg": "#4CAF50", "fg": "white"}
        if texto == "C":
            return {"bg": "#FFEBEE", "fg": "#C62828"}
        if texto in {"/", "*", "-", "+"}:
            return {"bg": "#E3F2FD", "fg": "#1565C0"}
        return {"bg": "#F5F5F5", "fg": "#1F2937"}

    def _configurar_atajos(self):
        """Vincula atajos de teclado (rúbrica de accesibilidad)."""
        for tecla in "0123456789+-*/.":
            self.ventana.bind(tecla, lambda _e, t=tecla: self.click(t))
        self.ventana.bind("<Return>", lambda _e: self.click("="))
        self.ventana.bind("<Escape>", lambda _e: self.click("C"))

    @classmethod
    def evaluar_expresion(cls, expresion: str) -> str:
        """Evalúa una expresión aritmética y retorna el resultado como texto."""
        limpia = expresion.strip()
        if not limpia:
            return ""
        if not set(limpia).issubset(cls.CARACTERES_VALIDOS):
            raise ValueError("Expresión inválida")
        resultado = eval(limpia, {"__builtins__": None}, {})
        if isinstance(resultado, bool) or not isinstance(resultado, (int, float)):
            raise ValueError("Expresión inválida")
        return str(resultado)

    def click(self, valor: str):
        """Maneja los eventos de botones y teclado."""
        if valor == "C":
            self.expresion.set("")
        elif valor == "=":
            actual = self.expresion.get()
            if not actual.strip():
                return
            try:
                self.expresion.set(self.evaluar_expresion(actual))
            except ZeroDivisionError:
                messagebox.showerror("Error", "No se puede dividir entre cero")
                self.expresion.set("")
            except Exception:
                messagebox.showerror("Error", "Expresión inválida")
                self.expresion.set("")
        else:
            self.expresion.set(self.expresion.get() + valor)

    def run(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    Calculadora().run()

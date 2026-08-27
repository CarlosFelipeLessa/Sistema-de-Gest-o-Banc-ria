"""
Aplicação principal do Sistema de Gestão Bancária.
Gerencia a janela principal e a navegação entre telas.
"""
import customtkinter as ctk
from src.services.banco_service import BancoService
from src.views.gui.theme import Theme
from src.views.gui.login_frame import LoginFrame
from src.views.gui.cadastro_frame import CadastroFrame
from src.views.gui.dashboard_frame import DashboardFrame
from src.views.gui.conta_frame import ContaFrame


class BancoApp(ctk.CTk):
    """Janela principal da aplicação bancária com navegação por frames."""

    def __init__(self):
        super().__init__()

        # ── Configuração da Janela ─────────────────────────
        self.title("🏦 Sistema de Gestão Bancária")
        self.geometry(f"{Theme.WINDOW_WIDTH}x{Theme.WINDOW_HEIGHT}")
        self.minsize(900, 600)
        self.configure(fg_color=Theme.BG_DARK)

        # Centralizar na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - Theme.WINDOW_WIDTH) // 2
        y = (self.winfo_screenheight() - Theme.WINDOW_HEIGHT) // 2
        self.geometry(f"+{x}+{y}")

        # ── Tema Global ───────────────────────────────────
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ── Camada de Serviço ──────────────────────────────
        self.service = BancoService()

        # ── Container Principal ────────────────────────────
        self.container = ctk.CTkFrame(self, fg_color=Theme.BG_DARK)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.current_frame = None

        # Exibir tela de login
        self.show_frame("login")

    def show_frame(self, name, **kwargs):
        """
        Navega para uma nova tela, destruindo a anterior.
        
        Args:
            name: Nome da tela ("login", "cadastro", "dashboard", "conta")
            **kwargs: Argumentos passados ao construtor da tela
        """
        if self.current_frame:
            self.current_frame.destroy()

        frame_map = {
            "login": LoginFrame,
            "cadastro": CadastroFrame,
            "dashboard": DashboardFrame,
            "conta": ContaFrame,
        }

        frame_cls = frame_map.get(name)
        if not frame_cls:
            return

        frame = frame_cls(self.container, self, **kwargs)
        frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = frame


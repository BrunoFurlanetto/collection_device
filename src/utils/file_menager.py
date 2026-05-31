from tkinter import messagebox
from ..get_remote_files import get_test_files
from src.utils.validator import validate_modality_initials


def download_test_files(port, modality_initials):
    if not validate_modality_initials(modality_initials):
        messagebox.showwarning("Aviso", "As iniciais da modalidade estão incorretas. Verifique e tente novamente.")
        return

    try:
        get_test_files(port, modality_initials.lower().replace(" ", "_"))
        messagebox.showinfo("Sucesso", "Arquivos de teste baixados com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar arquivos: {e}")

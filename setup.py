from cx_Freeze import setup, Executable
import sys

# Base para Windows
base = "Win32GUI" if sys.platform == "win32" else None

# Arquivos adicionais que devem ser incluídos no executável
include_files = [
    ("dist/Recursos", "Recursos"),
    ("icon.ico", "icon.ico")  # Certifique-se de que icon.ico está na pasta
]

# Configuração cx_Freeze
setup(
    name="JogoHollowKnight",
    version="1.0",
    description="Jogo estilo Hollow Knight com Pygame",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": include_files
        }
    },
    executables=[
        Executable(
            script="main.py",
            base="Win32Gui",
            target_name="JogoHollowKnight.exe",
            icon="icon.ico"
        )
    ]
)

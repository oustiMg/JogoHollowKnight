import os, time, pyttsx3, random, datetime, pygame, speech_recognition as sr
def limpar_tela():
    os.system("cls")

def aguardarTempo(segundos):
    time.sleep(segundos)



def mensagem_vozinha(nome):
    engine = pyttsx3.init()
    mensagem = f"Bem-vindo, {nome}! Prepare-se para coletar almas no mundo de Hollow Knight!"
    engine.say(mensagem)
    engine.runAndWait()

def ouvir_comando():
    """Ouve o microfone e retorna texto reconhecido (ou None em caso de erro)."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Ouvindo comando...")
        try:
            audio = r.listen(source, timeout=4)
            comando = r.recognize_google(audio, language="pt-BR").lower()
            print("🗣️ Você disse:", comando)
            return comando
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
            print("⚠️ Não entendi o comando.")
            return None

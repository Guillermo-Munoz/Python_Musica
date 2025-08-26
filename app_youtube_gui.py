import tkinter as tk
from tkinter import messagebox, simpledialog
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import webbrowser

# Configura tu cliente Spotify aquí
SPOTIFY_CLIENT_ID=tu_client_id
SPOTIFY_CLIENT_SECRET=tu_client_secret

# Autenticación para solo búsquedas públicas (sin permisos de usuario)
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                      client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

mi_lista = []  # Lista local de canciones (nombre, artista, spotify_id)

# Función para buscar en Spotify y mostrar resultados
def buscar_spotify():
    termino = entrada_buscar.get().strip()
    if not termino:
        messagebox.showwarning("Campo vacío", "Escribe el nombre de la canción o artista.")
        return

    resultados = sp.search(q=termino, limit=50, type='track')
    lista_resultados.delete(0, tk.END)

    for item in resultados['tracks']['items']:
        nombre = item['name']
        artista = item['artists'][0]['name']
        spotify_id = item['id']
        lista_resultados.insert(tk.END, f"{nombre} - {artista} | ID:{spotify_id}")

# Añadir canción seleccionada de resultados a la lista personal
def añadir_a_mi_lista():
    sel = lista_resultados.curselection()
    if not sel:
        messagebox.showinfo("Selecciona canción", "Selecciona una canción de los resultados para añadir.")
        return
    texto = lista_resultados.get(sel[0])
    # Extraer info con ID
    partes = texto.split('| ID:')
    nombre_artista = partes[0].strip()
    spotify_id = partes[1].strip()
    # Evitar duplicados
    if any(c[2] == spotify_id for c in mi_lista):
        messagebox.showinfo("Ya en lista", "La canción ya está en tu lista.")
        return
    mi_lista.append((nombre_artista, spotify_id))
    lista_mi_lista.insert(tk.END, nombre_artista)
    estado.set(f"✅ Añadida: {nombre_artista}")

# Buscar y reproducir canción de la lista personal en YouTube
from youtube_search import YoutubeSearch
import webbrowser
from tkinter import messagebox

def reproducir_en_youtube():
    sel = lista_mi_lista.curselection()
    if not sel:
        messagebox.showinfo("Selecciona canción", "Selecciona una canción de tu lista para reproducir.")
        return
    nombre_artista = mi_lista[sel[0]][0]

    try:
        resultados = YoutubeSearch(nombre_artista, max_results=1).to_dict()
        if resultados:
            url = 'https://www.youtube.com' + resultados[0]['url_suffix']
            webbrowser.open(url)
            estado.set(f"▶️ Reproduciendo: {nombre_artista}")
        else:
            estado.set("❌ No se encontraron resultados en YouTube.")
    except Exception as e:
        estado.set("❌ Error buscando en YouTube.")
        print("Error:", e)


# Eliminar canción de mi lista
def eliminar_de_mi_lista():
    sel = lista_mi_lista.curselection()
    if not sel:
        messagebox.showinfo("Selecciona canción", "Selecciona una canción para eliminar.")
        return
    idx = sel[0]
    nombre = mi_lista[idx][0]
    del mi_lista[idx]
    lista_mi_lista.delete(idx)
    estado.set(f"❌ Eliminada: {nombre}")

# ===== Interfaz gráfica =====
ventana = tk.Tk()
ventana.title("🎵 Buscador y lista de canciones Spotify + YouTube")
ventana.geometry("700x500")

# Entrada búsqueda Spotify
tk.Label(ventana, text="Buscar canción o artista en Spotify:", font=("Arial", 12)).pack(pady=5)
entrada_buscar = tk.Entry(ventana, width=60, font=("Arial", 12))
entrada_buscar.pack()

boton_buscar = tk.Button(ventana, text="🔍 Buscar", command=buscar_spotify, bg="#1DB954", fg="white")
boton_buscar.pack(pady=5)

# Resultados búsqueda
tk.Label(ventana, text="Resultados en Spotify:", font=("Arial", 12, "bold")).pack()
lista_resultados = tk.Listbox(ventana, width=90, height=10)
lista_resultados.pack()

boton_añadir = tk.Button(ventana, text="➕ Añadir a mi lista", command=añadir_a_mi_lista)
boton_añadir.pack(pady=5)

# Lista personal
tk.Label(ventana, text="Mi lista de canciones:", font=("Arial", 12, "bold")).pack()
lista_mi_lista = tk.Listbox(ventana, width=90, height=10)
lista_mi_lista.pack()

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

boton_reproducir = tk.Button(frame_botones, text="▶️ Reproducir en YouTube", command=reproducir_en_youtube)
boton_reproducir.grid(row=0, column=0, padx=10)

boton_eliminar = tk.Button(frame_botones, text="❌ Eliminar de mi lista", command=eliminar_de_mi_lista)
boton_eliminar.grid(row=0, column=1, padx=10)

# Estado
estado = tk.StringVar()
estado.set("🎧 Listo...buscar canciones.")
tk.Label(ventana, textvariable=estado).pack(pady=5)

ventana.mainloop()

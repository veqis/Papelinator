import gi
import requests
import os
import glob
import subprocess
import simpleaudio as sa

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

class Janela_Main(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Papelinator 1.0")

        self.builder = Gtk.Builder()
        self.builder.add_from_file("menu.glade")

        self.window = self.builder.get_object("janela")
        self.image = self.builder.get_object("imagem")
        self.entry = self.builder.get_object("entrada")
        self.bt_download = self.builder.get_object("bt_dl")
        self.bt_mudar = self.builder.get_object("bt_md")

        self.bt_download.connect("clicked", self.botao_dl)
        self.bt_mudar.connect("clicked", self.botao_muda)

        self.window.connect("destroy", Gtk.main_quit)

        self.window.show_all()

        self.link_invalido = sa.WaveObject.from_wave_file("sadtrombone.wav")
        self.nova_img = sa.WaveObject.from_wave_file("yoda.wav")

    def dados(self):
        url = self.entry.get_text()

        pasta_downloads = os.path.expanduser('~/Downloads')
        local_dl = max(glob.glob(os.path.join(pasta_downloads, '*')), key=os.path.getctime)
        diretorio = os.path.dirname(local_dl)

        output_link = None
        try:
            output_link = requests.get(url)
        except requests.exceptions.InvalidSchema:
            self.trombone_triste()
        
        nome_img = os.path.basename(url)

        diretorio_imgs = os.path.join(diretorio, nome_img)

        return output_link, diretorio_imgs

    def botao_muda(self, button):
        _, diretorio_imgs = self.dados()
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://' + diretorio_imgs])

        self.yoda_img()

    def botao_dl(self, button):
        output_link, diretorio_imgs = self.dados()

        if output_link is None:
            return

        if output_link.status_code != 200:
            self.trombone_triste()
            return

        with open(diretorio_imgs, 'wb') as file:
            file.write(output_link.content)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(diretorio_imgs)
        pixbuf = pixbuf.scale_simple(500, 300, GdkPixbuf.InterpType.BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

    def trombone_triste(self):
        play_obj = self.link_invalido.play()
        play_obj.wait_done()

    def yoda_img(self):
        play_obj = self.nova_img.play()
        play_obj.wait_done()

janela = Janela_Main()
Gtk.main()
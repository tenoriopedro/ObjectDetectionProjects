# Módulo para mostrar resultados dos modelos

from IPython.display import HTML
from base64 import b64encode
import os
import moviepy.editor as moviepy


def exibir_video(video_caminho):

  mp4 = open(video_caminho, "rb").read()
  data_url = "data:video/mp4;base64," + b64encode(mp4).decode()

  return HTML("""
  <video width=500 controls>
    <source src='%s' type='video/mp4'>
    </video>
    """ % data_url)

video_salvo = "C:\\Desenvolvimento\\ProjetosEstagio\\ProjetoContagemYOLO\\compiled_files\\object_counting_output.mp4"
video_final = "C:\\Desenvolvimento\\ProjetosEstagio\\ProjetoContagemYOLO\\result_files\\video_countingCar_result01.mp4"

clip = moviepy.VideoFileClip(video_salvo)
clip.write_videofile(video_final)


exibir_video(video_final)
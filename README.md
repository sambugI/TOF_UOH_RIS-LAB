#  EXPERIENCIA E INVESTIGACIÓN APLICADA EN VISIÓN COMPUTACIONAL Y SENSORES DE PROFUNDIDAD
## Sobre las cámaras usadas
Este repositorio contiene información sobre las cámaras ToF, RGB y de polarización del LucidVisions usados en RisLab de la UOH junto con los experimentos realizados con estos para evaluar su aplicación a lo largo de la práctica del estudiante Samuel Bugueño. Los modelos de las cámaras usadas corresponden al kit de cámara ToF + RBG, a continuación se detallan los modelos específicos: 

- Kit: https://thinklucid.com/product/rgb-3d-kit-triton-3-2mp-helios2-kit/
- HElios 2 Ray (ToF): https://thinklucid.com/product/helios2-ray-outdoor-tof-ip67-3d-camera/
- Triton 3.2 (RGB) : https://thinklucid.com/product/triton-32-mp-imx265/

Las instrucciones del armado de las cámaras están en los siguientes links:

- https://support.thinklucid.com/getting-started/#gs-Helios-Connect
- https://www.youtube.com/watch?v=KyQD-z0Km00

Estas cámaras se pueden usar por medio de software de terceros o por el software del fabricante, que se llama Arena SDK, con su GUI Arena View. Para descargar ArenaView, se debe dirigir a esta página:

- https://thinklucid.com/downloads-hub/
- https://support.thinklucid.com/arena-sdk-documentation/
- https://support.thinklucid.com/knowledgebase/using-lucids-arenaview-with-jupyterlab/

Además, si para poder aprender cómo ajustar la captura de datos por la cámara Helios2 y los distintos fenómenos que lo afectan se pueden seguir los siguientes videos hechos por el fabricante:
- https://www.youtube.com/watch?v=f9dCo6SlCFU
- https://www.youtube.com/watch?v=I-QFjwmiwgk&t
- https://www.youtube.com/watch?v=1ZHcsbEsL6o

Si se desea obtener información adicional, se pueden observar las guías técnicas descargables en este link:

- https://thinklucid.com/downloads-hub/#tab-helios-tech-man

Una vez se descargue el paquete de Arena Sdk, se puede revisar en la siguiente ubicación del computador ejemplos de código para usar las cámaras: C:\ProgramData\Lucid Vision Labs\Examples\src\
# Archivos en el repositorio

En este repositorio se encuentran 3 carpetas principales, un archivo pdf y unos 2 archivos json. La primera carpeta corresponden a los códigos propios usados a lo largo de los experimentos, algunos de estos usando paquetes y basándose en los códigos de Lucid Visions. La segunda carpeta corresponde a los reportes de avance con el supervisor, explicando algunas falencias y problemas encontrados mientras se experimentaba con las cámaras junto con sus correcciones. 

La tercera carpeta corresponde a los resultados de los experimentos, organizados por semanas. Estos incluyen nubes de puntos en formato .ply, imágenes .png y archivos txt con algunas especificaciones de las configuraciones de los experimentos realizados. Por otro lado archivo pdf corresponde al informe de práctica con los estudios sobre el principio de funcionamiento de la cámara, los procedimientos específicos de cómo se realizaron los experimentos y finalmente un análisis de los resultados obtenidos. 

Finalmente, los 2 archivos .json que se encuentran corresponden a los parámetros extrínsecos e intrínsecos de las cámaras Helios y Tritón, usando como nombre el número de serie de cada cámara. Estos archivos se pueden agregar en la ubicación: C:\ProgramData\Lucid Vision Labs\ArenaView del computador en el que se tenga instalado Arena View para poder superponer la información de profundidad de la cámara ToF y la información de la cámara RGB si se monta una cámara sobre otra de acuerdo a las especificaciones del fabricante. Para esto, se debe cambiar el nombre de los archivos al número de serie de las cámaras a usar. El archivo para la cámara Tritón es el que contiene solo parámetros intrínsecos y el de la cámara Helios es el que además de parámetros intrínsecos de la cámara Tritón, posee los parámetros extrínsecos en milímetros (en realidad, corresponde a 1,04mm) respecto a la cámara Tritón.

# Experimentos realizados

Al inicio de la carpeta de resultados se tiene una imagen con los objetos usados para los experimentos. Entre estos se encuentran:


- Caja de color azul.
- Desindectante ambiental en spray.
- Taza de plástico de color negro.
- Jarrón de plástico.
- Juguete de dinosaurio.

Para entender la funcionalidad y probar la aplicación de las cámaras a usar se hicieron los siguientes experimentos:

- Superposición entre información cámara ToF y RGB para crear nube de puntos a color.
- Medición del alcance real de las cámaras a usar comparado entre el interior con el exterior.
- Captura de distintos puntos de vista de objetos para luego poder superponerlos en un modelo 3D.

Adicionalmente, se hizo otro experimento con la cámara de polarización para hacer una reconstrucción 3D de una cereza a partir de varias capturas con luces en distintas posiciones, pero no se va a detallar en este repositorio (aunque se mencionó en el informe).

# Software para procesamiento de datos

Para poder visualizar las nubes de puntos creadas a partir de las cámaras ToF y RGB, se usó el software de CloudCompare. Además, de permitir la visualización de la nube de puntos, permite su edición, traslación, unión entre estos e incluso crear modelos 3D. A continuación se va a mencionar links importantes usados para los experimentos:
- Descargar CloudCompare: https://www.cloudcompare.org/release/index.html#CloudCompare
- Información sobre el uso de CloudCompare: https://www.cloudcompare.org/doc/wiki/index.php/Main_Page
- Uso de CloudCompare para alinear 2 nubes de puntos de una misma escena: https://www.youtube.com/watch?v=0OcN-lNChlA
- Creación de modelo 3D a partir de nubes de puntos: https://www.youtube.com/watch?v=m43usERF33M





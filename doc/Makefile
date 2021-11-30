# @Autors       Brito Segura Angel, Tovar Herrera Carlos Eduardo & Zazueta Barájas Sebastián Pedro
# @Fecha        13/10/2021
# @Descripcion  Archivo deconfiguración para una compilación en Linux del archivo en LaTeX

#Declaración de variables
# Nombre del archivo principal escrito en LaTeX
PREFIX= "main"
SILENT= @
RUBBER= rubber
# Banderas para siempre generar el archivo con salida estándar PDF
FLAGS= --force --pdf
#Nombre del archivo
FILE= "manual_tecnico"

#Se llama en automático cada sección de este archivo
all:
	$(SILENT) make -s build
	$(SILENT) make -s clean
	$(SILENT) make -s launch

#Compilar el proyecto
build:
	$(SILENT) $(RUBBER) $(FLAGS) $(PREFIX).tex

#Quitar toda la basura
clean:
	$(SILENT) $(RUBBER) --clean $(PREFIX).tex

#Abrir el archivo
launch:
	#Cambiar de nombre
	mv $(PREFIX).pdf $(FILE).pdf
	#gnome-open
	$(SILENT) xdg-open $(FILE).pdf &> /dev/null &

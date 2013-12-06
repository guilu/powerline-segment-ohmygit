===========
Powerline
===========

Segmento para powerline que personaliza y muestra información de nuestros repositorios git (sustituye al branch que viene por defecto), me he inspirado en oh-my-git y he utilizando las fuentes patched de awesome-terminal-fonts

Instalación
===========

* First

	Lo primero que voy a asumir es que teneis instalado y funcionando vuestro powerline shell... (con zsh o bash, yo uso bash, pero creo que la instalación es básicamente la misma) y que, por lo tanto, también tenéis **pip** con las **setuptools** actualizadas.

* Second

	Lo segundo que asumiré es que conoceis como personalizar los temas y colores de powerline para mostrar cada segmento de una forma personalizada... (copiar la carpeta config_files a ~/.config/powerline y allí retocar los .json)
	
Una vez dicho esto lo único que tienes que hacer para instalar este segmento es ejecutar:

	pip install --user git+git://github.com/guilu/powerline-segment-ohmygit



Personalización
-------------

Una vez instalado tendrás que tocar el fichero de configuración del tema que estés usando, añadiendo el segmento:

			{
				"module": "plohmygit.segment.plohmygit",
			    "name": "plohmygit",
			    "args": {
			    	"use_path_separator": true
			    }
			},

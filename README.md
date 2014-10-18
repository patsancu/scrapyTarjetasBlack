Recolectar información tarjetas black
=======================================

**Derechos de los datos (no incluidos en proyecto) para El Pais, S.A.**


Introducción
----------

Script que recoge información sobre el caso de las tarjetas llamadas "black" de un conocido diario de información de España usando las bibliotecas de Scrapy.

Crea un archivo items.json en el directorio raíz, que contiene una lista de elementos json con la siguiente estructura:
```
item
	-nombreConsejero
	-cargo (Ej.: director financiero, consejero nombrado por partido ...)
	-gastos (array que contiene detalle de cada gasto)
		[]
			gasto
				-importe
				-fecha
				-hora
				-comercio
				-actividad
				-operacion

```



Requisitos
-----------

[Python](http://www.python.org/) 2.7+ 
[Pip](http://www.pip-installer.org/en/latest/installing.html)
[Scrapy](http://scrapy.org/)

Uso
-----

```
usuario@maquina:[DirectorioRaiz] $ scrapy crawl aranyaTarjetasBlack -o items.json
```


Dudas
------
Para cualquier duda, sugerencia o queja, escriba a info@corrompe.me
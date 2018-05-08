 
Sobre el Selector de CRS y transformacion
===========================================

Sin pensarlo demasiado, el API de este panel extenderia a los interfaces
del crsselector y del ctselector.

No se si precisaria algo especifico de el.

En lo que a implementacion se refiere, deberia ser bastante simple, ya que 
se limita a un tab que incluye a los otros dos paneles. Solo un algunas
consideraciones:

- Los selectores de crs en el panel de ct estaran desactivados.
- Si no se ha asignado un targetcrs la pestaña de transformacion
  estara desactivada.
- Si la proyeccion seleccionada en la pestaña de seleccion cd CRS
  es la misma que targetcrs la pestaña de transformacion estara
  desactivada.
- Si sourcecrs o targetcrs son null, getTransform() devolvera null.
- Si no hay ninguna transformacion seleccionada (noy hay ningun 
  elemento del tree seleccionado esta seleccionada una rama) 
  getTransform devolbera null.
  
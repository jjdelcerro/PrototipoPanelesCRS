 
 
API CT Selector
=================

El API de este panel estara representado por un Interface java que
extienda de Component (de org.gvsig.tools.swing).

El Api tendra metodos como:

- getTransform()
- getTargetCRS()
- getSourceCRS()
- setTransform()
- setTargetCRS()
- setSourceCRS()
- void addTransformSelectionListener(ActionListener listener)
- setEnabledCRSTargetSelector(boolean enabled)
- setEnabledCRSSourceSelector(boolean enabled)
- void setTransformAlphaFilter(String filter)
- String getTransformAlphaFilter()
- void applyTransformFilter()
  
Por defecto en el dialogo presentara el arbol con las ramas colapsadas 
viendose solo las de:

- Reciente
- favoritos
- EPSG
- Grids
- User

Si el usuario expande las ramas navegara por toda la BBDD del catalogo
de transformaciones.

Si el usuario introduce un filtro la informacion
a presentar en el arbol se restringira a las transformaciones que cumplan
el criterio.

Se utilizara el boton de la lupa con el aspa roja para eliminar el criterio
de filtro y volver a navegar por toda la BBDD del catalogo.




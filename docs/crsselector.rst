 
API CRS Selector
=================

.. figure:: images/crsselector2.png

El API de este panel estara representado por un Interface java que
extienda de Component (de org.gvsig.tools.swing).

Este panel permitira:

- Mantener una lista de "custom CRS". 

  Esta lista se presentara en la ultima rama del tree, y se le 
  podra asignar una etiqueta. Si no se le asigna una etiqueta
  usara "Custom". No se presentara la rama en el tree si esta vacia.

  Por ejemplo, se podria hacer algo como::

    panel.setCustomLabel("Layers")
    for layer in iter(mapContext.deepIterator()):
      panel.addCustomCRS(layer.getProjection())
      
  En caso que se añadan CRS duplicados a la lista de CRS custom
  se ignoraran los duplicados, no añadiendose a la lista.

  Habria que ver de añadir metodos para acceder a la estos atributos,
  algo como:

  - String getCustomLabel()
  - List<IProjection> getCustomCRSs()

    Que devolveria una lista inmutable de esos CRS. No se si seria
    interesante que devolviese directamente un List o un OrderedSet.

- Mantener una lista de "encuadres", Envelope, a usar en el filtro 
  espacial. 

  Por ejemplo, se podria hacer algo como::

    panel.addSpatialFilter("Current Visible Extent", currentView().getEnvelope())

  No añadiria filtros duplicados por nombre. Y habria que añadir algun getter,
  por ejemplo:

  - Map<String,IProjection> getSpatialFilters()

  Internamente habria que ver si deberia respetar el orden por el que se han
  añadido los filtros o si se ordenan por orden alfabetico.

  Tambien habria que ver en que CRS estan esos "encuadres". Supongo que se 
  precisara que esten en 4326.
  
Tambien deberia tener un metodo algo como::

  void addSelectionListener(ActionListener listener)

Para escuchar cuando se va seleccionando una proyeccion en el tree (usar
ActionListenerSupport de tools.swing).

En el manager de swing de proyecciones, habria que incluir algo como::

  public List<IProjection> getHistory();
  
  public List<IProjection> getFavorites();

  public List<String> getHistoryAlphaFilters()

Seran listas mutables y nunca seran null.
"getHistoryAlphaFilters" se usara para rellenar el combo "cboFilterAlpha"
con los ultimos valores usados como filtros alphanumericos.

Ademas se incluiran un par de metodos::

  public DynObject getPreferences();

  public void setPreferences(DynObject preferences);
  
Por defecto el manager tendra una instancia de ese DynObject que
mantendra en memoria. Sera algo como unas preferencias por defecto
que no persisten. En el contexto de la aplicacion "gvSIG desktop",
desde el plugin se asignara un DynObject que se obtendra de las
preferencias del plugin, de forma que sea andami quien se encargara
de persistirlo.

En la documentacion el API se definira en los javadocs de uno de
estos metodos la estructura que debera tener este DynObject.
Tendra como minimo dos campos de tipo lista de proyecciones 
para almacenar las listas de historico y favoritos.

Por defecto en el dialogo estara activada la busqueda por texto, 
y se presentara el arbol con las ramas colapsadas viendose solo las
de:

- Reciente
- favoritos
- Una rama por authority
- Y la rama custom si tiene elementos.

Si el usuario expande las ramas navegara por toda la BBDD del catalogo
de proyecciones.

Si el usuario introduce un filtro (alphanumerico o espacial) la informacion
a presentar en el arbol se restringira a las proyecciones que cumplan
el criterio.

Se utilizara el boton de la lupa con el aspa roja para eliminar el criterio
de filtro y volver a navegar por toda la BBDD del catalogo.

Se incluiran metodos como::

  public IProjection getProjection()

  public void setProjection(IProjection projection)

  public void setSpatialFilter(String filter)

  public String getSpatialFilter()

  public void setAlphaFilter(String filter)

  public String getAlphaFilter()


Los metodos setXXXFilter asignan y aplican el filtro.

El metodo getProjection seria el metodo usado para recuperar la proyeccion 
seleccionada por el usuario.



 
Sobre el manager de swing
=============================

En el manager de swing de proyecciones habria que incluir algo como::

  public List<IProjection> getCoordinateSystemHistory();
  
  public List<IProjection> getCoordinateSystemFavorites();

  public List<String> getCoordinateSystemHistoryAlphaFilters()

  public List<IProjection> getCoordinateTransformHistory();
  
  public List<IProjection> getCoordinateTransformFavorites();

  public List<String> getCoordinateTransformHistoryAlphaFilters()

Seran listas mutables y nunca seran null.
"getXXXHistoryAlphaFilters" se usara para rellenar los combos de los
filtros alfanumericos con los ultimos valores usados.

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
Tendra como minimo seis campos. dos de tipo lista de proyecciones 
para almacenar las listas de historico y favoritos. Dos mas para
almacenar las transformaciones, y dos mas para almacenar el
historico de las cadenas de busqueda.

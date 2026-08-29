<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <se:Name>Styling polygon vector features</se:Name>
    <UserStyle>
      <se:Description>
        <se:Title>Styling polygon vector features</se:Title>
        <se:Abstract>SLD/SE codec fixture: PolygonSymbolizer, Fill+Stroke, dataLayer.id sugar</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:FeatureTypeName>Landuse</se:FeatureTypeName>
        <se:Rule>
          <se:Name>Landuse</se:Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>FunctionCode</ogc:PropertyName>
              <ogc:Literal>parking</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#808080</se:SvgParameter>
              <se:SvgParameter name="fill-opacity">0.5</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#202020</se:SvgParameter>
              <se:SvgParameter name="stroke-width">2</se:SvgParameter>
              <se:SvgParameter name="stroke-opacity">1</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>

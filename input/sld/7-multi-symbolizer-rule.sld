<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <se:Name>Multi-symbolizer rule</se:Name>
    <UserStyle>
      <se:Description>
        <se:Title>Multi-symbolizer rule</se:Title>
        <se:Abstract>SLD/SE codec fixture: one se:Rule with Polygon + Text symbolizers</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:FeatureTypeName>Landuse</se:FeatureTypeName>
        <se:Rule>
          <se:Name>Landuse</se:Name>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#90ee90</se:SvgParameter>
              <se:SvgParameter name="fill-opacity">0.6</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#006400</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-opacity">1</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
          <se:TextSymbolizer>
            <se:Label>
              <ogc:PropertyName>FunctionTitle</ogc:PropertyName>
            </se:Label>
            <se:Font>
              <se:SvgParameter name="font-family">Arial</se:SvgParameter>
              <se:SvgParameter name="font-size">10</se:SvgParameter>
              <se:SvgParameter name="font-weight">normal</se:SvgParameter>
              <se:SvgParameter name="font-style">normal</se:SvgParameter>
            </se:Font>
            <se:Fill>
              <se:SvgParameter name="fill">#000000</se:SvgParameter>
            </se:Fill>
          </se:TextSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>

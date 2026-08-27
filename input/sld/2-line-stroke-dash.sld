<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <se:Name>Styling line vector features</se:Name>
    <UserStyle>
      <se:Description>
        <se:Title>Styling line vector features</se:Title>
        <se:Abstract>SLD/SE codec fixture: LineSymbolizer, stroke-dasharray, ogc:And</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:FeatureTypeName>Roads</se:FeatureTypeName>
        <se:Rule>
          <se:Name>Roads</se:Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>RoadClass</ogc:PropertyName>
              <ogc:Literal>highway</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <se:LineSymbolizer>
            <se:Stroke>
              <se:SvgParameter name="stroke">#a9a9a9</se:SvgParameter>
              <se:SvgParameter name="stroke-width">3</se:SvgParameter>
              <se:SvgParameter name="stroke-opacity">1</se:SvgParameter>
              <se:SvgParameter name="stroke-dasharray">4 2</se:SvgParameter>
            </se:Stroke>
          </se:LineSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
